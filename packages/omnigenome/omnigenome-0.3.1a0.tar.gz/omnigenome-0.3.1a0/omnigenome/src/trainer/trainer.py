# -*- coding: utf-8 -*-
# file: trainer.py
# time: 14:40 06/04/2024
# author: YANG, HENG <hy345@exeter.ac.uk> (杨恒)
# github: https://github.com/yangheng95
# huggingface: https://huggingface.co/yangheng
# google scholar: https://scholar.google.com/citations?user=NPq5a_0AAAAJ&hl=en
# Copyright (C) 2019-2024. All Rights Reserved.
"""
Training utilities for OmniGenome models.

This module provides a comprehensive training framework for OmniGenome models,
including automatic mixed precision training, early stopping, metric tracking,
and model checkpointing.
"""
import os
import tempfile
import autocuda
import numpy as np
from torch.utils.data import DataLoader
from tqdm import tqdm

from ..misc.utils import env_meta_info, fprint, seed_everything

import torch
from torch.cuda.amp import GradScaler


def _infer_optimization_direction(metrics, prev_metrics):
    """
    Infer the optimization direction based on metric names and trends.

    This function determines whether larger or smaller values are better for
    the given metrics by analyzing metric names and their trends over time.

    Args:
        metrics (dict): Current metric values
        prev_metrics (list): Previous metric values from multiple epochs

    Returns:
        str: Either "larger_is_better" or "smaller_is_better"
    """
    larger_is_better_metrics = [
        "accuracy",
        "f1",
        "recall",
        "precision",
        "roc_auc",
        "pr_auc",
        "score",
        # ...
    ]
    smaller_is_better_metrics = [
        "loss",
        "error",
        "mse",
        "mae",
        "r2",
        "distance",
        # ...
    ]
    for metric in larger_is_better_metrics:
        if prev_metrics and metric in list(prev_metrics[0].keys())[0]:
            return "larger_is_better"
    for metric in smaller_is_better_metrics:
        if prev_metrics and metric in list(prev_metrics[0].keys())[0]:
            return "smaller_is_better"

    fprint(
        "Cannot determine the optimisation direction. Attempting inference from the metrics."
    )
    is_prev_increasing = np.mean(list(prev_metrics[0].values())[0]) < np.mean(
        list(prev_metrics[-1].values())[0]
    )
    is_still_increasing = np.mean(list(prev_metrics[1].values())[0]) < np.mean(
        list(metrics.values())[0]
    )
    fprint(
        "Cannot determine the optimisation direction. Attempting inference from the metrics."
    )

    if is_prev_increasing and is_still_increasing:
        return "larger_is_better"

    is_prev_decreasing = np.mean(list(prev_metrics[0].values())[0]) > np.mean(
        list(prev_metrics[-1].values())[0]
    )
    is_still_decreasing = np.mean(list(prev_metrics[1].values())[0]) > np.mean(
        list(metrics.values())
    )

    if is_prev_decreasing and is_still_decreasing:
        return "smaller_is_better"

    return "larger_is_better" if is_prev_increasing else "smaller_is_better"


class Trainer:
    """
    Comprehensive trainer for OmniGenome models.

    This trainer provides a complete training framework with automatic mixed precision,
    early stopping, metric tracking, and model checkpointing. It supports various
    training configurations and can handle different types of genomic sequence tasks.

    Attributes:
        model: The model to be trained
        train_loader: DataLoader for training data
        eval_loader: DataLoader for validation data
        test_loader: DataLoader for test data
        epochs: Number of training epochs
        patience: Early stopping patience
        optimizer: Optimizer for training
        loss_fn: Loss function
        compute_metrics: List of metric computation functions
        device: Device to run training on
        scaler: Gradient scaler for mixed precision training
        metrics: Dictionary to store training metrics
        predictions: Dictionary to store model predictions
    """

    def __init__(
        self,
        model,
        train_dataset: torch.utils.data.Dataset = None,
        eval_dataset: torch.utils.data.Dataset = None,
        test_dataset: torch.utils.data.Dataset = None,
        epochs: int = 3,
        batch_size: int = 8,
        patience: int = -1,
        gradient_accumulation_steps: int = 1,
        optimizer: torch.optim.Optimizer = None,
        loss_fn: torch.nn.Module = None,
        compute_metrics: list | str = None,
        seed: int = 42,
        device: [torch.device | str] = None,
        autocast: str = "float16",
        **kwargs,
    ):
        """
        Initialize the trainer.

        Args:
            model: The model to be trained
            train_dataset: Training dataset
            eval_dataset: Validation dataset
            test_dataset: Test dataset
            epochs (int): Number of training epochs (default: 3)
            batch_size (int): Batch size for training (default: 8)
            patience (int): Early stopping patience (default: -1, no early stopping)
            gradient_accumulation_steps (int): Gradient accumulation steps (default: 1)
            optimizer: Optimizer for training (default: None)
            loss_fn: Loss function (default: None)
            compute_metrics: Metric computation functions (default: None)
            seed (int): Random seed (default: 42)
            device: Device to run training on (default: None, auto-detect)
            autocast (str): Mixed precision type (default: "float16")
            **kwargs: Additional keyword arguments
        """
        # sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

        self.model = model

        # DataLoaders
        if kwargs.get("train_loader"):
            self.train_loader = kwargs.get("train_loader", None)
            self.eval_loader = kwargs.get("eval_loader", None)
            self.test_loader = kwargs.get("test_loader", None)
        else:
            self.train_loader = DataLoader(
                train_dataset, batch_size=batch_size, shuffle=True
            )
            self.eval_loader = (
                DataLoader(eval_dataset, batch_size=batch_size)
                if eval_dataset
                else None
            )
            self.test_loader = (
                DataLoader(test_dataset, batch_size=batch_size)
                if test_dataset
                else None
            )

        self.epochs = epochs
        self.patience = patience if patience > 0 else epochs
        self.gradient_accumulation_steps = gradient_accumulation_steps
        self.optimizer = optimizer
        self.loss_fn = loss_fn
        self.compute_metrics = (
            compute_metrics if isinstance(compute_metrics, list) else [compute_metrics]
        )
        self.seed = seed
        self.device = device if device else autocuda.auto_cuda()
        self.device = (
            torch.device(self.device) if isinstance(self.device, str) else self.device
        )

        self.fast_dtype = {
            "float32": torch.float32,
            "fp32": torch.float32,
            "float16": torch.float16,
            "fp16": torch.float16,
            "bfloat16": torch.bfloat16,
            "bf16": torch.bfloat16,
        }.get(autocast, torch.float16)
        self.scaler = GradScaler()
        if self.loss_fn is not None:
            self.model.set_loss_fn(self.loss_fn)

        self.model.to(self.device)

        self.metadata = env_meta_info()
        self.metrics = {}

        self._optimization_direction = None
        self.trial_name = kwargs.get("trial_name", self.model.__class__.__name__)

        self.predictions = {}

    def _is_metric_better(self, metrics, stage="valid"):
        """
        Check if the current metrics are better than the best metrics so far.

        Args:
            metrics (dict): Current metric values
            stage (str): Stage name ("valid" or "test")

        Returns:
            bool: True if current metrics are better than best metrics
        """
        assert stage in [
            "valid",
            "test",
        ], "The metrics stage should be either 'valid' or 'test'."

        prev_metrics = self.metrics.get(stage, None)
        if stage not in self.metrics:
            self.metrics.update({f"{stage}": [metrics]})
        else:
            self.metrics[f"{stage}"].append(metrics)

        if "best_valid" not in self.metrics:
            self.metrics.update({"best_valid": metrics})
            return True

        if prev_metrics is None:
            return False

        self._optimization_direction = (
            _infer_optimization_direction(metrics, prev_metrics)
            if self._optimization_direction is None
            else self._optimization_direction
        )

        if self._optimization_direction == "larger_is_better":
            if np.mean(list(metrics.values())[0]) > np.mean(
                list(self.metrics["best_valid"].values())[0]
            ):
                self.metrics.update({"best_valid": metrics})
                return True
        elif self._optimization_direction == "smaller_is_better":
            if np.mean(list(metrics.values())[0]) < np.mean(
                list(self.metrics["best_valid"].values())[0]
            ):
                self.metrics.update({"best_valid": metrics})
                return True

        return False

    def train(self, path_to_save=None, **kwargs):
        """
        Train the model.

        Args:
            path_to_save (str, optional): Path to save the best model
            **kwargs: Additional keyword arguments

        Returns:
            dict: Training metrics and results
        """
        seed_everything(self.seed)
        patience = 0

        if self.eval_loader is not None and len(self.eval_loader) > 0:
            valid_metrics = self.evaluate()
        else:
            valid_metrics = self.test()
        if self._is_metric_better(valid_metrics, stage="valid"):
            self._save_state_dict()
            patience = 0

        for epoch in range(self.epochs):
            self.model.train()
            train_loss = []
            train_it = tqdm(
                self.train_loader, desc=f"Epoch {epoch + 1}/{self.epochs} Loss"
            )
            for step, batch in enumerate(train_it):
                batch = batch.to(self.device)

                if step % self.gradient_accumulation_steps == 0:
                    self.optimizer.zero_grad()

                if self.fast_dtype:
                    with torch.autocast(
                        device_type=self.device.type, dtype=self.fast_dtype
                    ):
                        outputs = self.model(**batch)
                else:
                    outputs = self.model(**batch)
                if "loss" not in outputs:
                    # Generally, the model should return a loss in the outputs via OmniGenBench
                    # For the Lora models, the loss is computed separately
                    if hasattr(self.model, "loss_function") and callable(
                        self.model.loss_function
                    ):
                        loss = self.model.loss_function(
                            outputs["logits"], outputs["labels"]
                        )
                    elif (
                        hasattr(self.model, "model")
                        and hasattr(self.model.model, "loss_function")
                        and callable(self.model.model.loss_function)
                    ):
                        loss = self.model.model.loss_function(
                            outputs["logits"], outputs["labels"]
                        )
                    else:
                        raise ValueError(
                            "The model does not have a loss function defined. "
                            "Please provide a loss function or ensure the model has one."
                        )
                else:
                    # If the model returns a loss directly
                    loss = outputs["loss"]

                loss = loss / self.gradient_accumulation_steps

                if self.fast_dtype:
                    self.scaler.scale(loss).backward()
                else:
                    loss.backward()

                if (step + 1) % self.gradient_accumulation_steps == 0 or (
                    step + 1
                ) == len(self.train_loader):
                    if self.fast_dtype:
                        self.scaler.step(self.optimizer)
                        self.scaler.update()
                    else:
                        self.optimizer.step()

                train_loss.append(loss.item() * self.gradient_accumulation_steps)
                train_it.set_description(
                    f"Epoch {epoch + 1}/{self.epochs} Loss: {np.nanmean(train_loss):.4f}"
                )

            if self.eval_loader is not None and len(self.eval_loader) > 0:
                valid_metrics = self.evaluate()
            else:
                valid_metrics = self.test()

            if self._is_metric_better(valid_metrics, stage="valid"):
                self._save_state_dict()
                patience = 0
            else:
                patience += 1
                if patience >= self.patience:
                    fprint(f"Early stopping at epoch {epoch + 1}.")
                    break

            if path_to_save:
                _path_to_save = path_to_save + "_epoch_" + str(epoch + 1)

                if valid_metrics:
                    for key, value in valid_metrics.items():
                        _path_to_save += f"_seed_{self.seed}_{key}_{value:.4f}"

                self.save_model(_path_to_save, **kwargs)

        if self.test_loader is not None and len(self.test_loader) > 0:
            self._load_state_dict()
            test_metrics = self.test()
            self._is_metric_better(test_metrics, stage="test")

        if path_to_save:
            _path_to_save = path_to_save + "_final"
            if self.metrics["test"]:
                for key, value in self.metrics["test"][-1].items():
                    _path_to_save += f"_seed_{self.seed}_{key}_{value:.4f}"

            self.save_model(_path_to_save, **kwargs)

        self._remove_state_dict()

        return self.metrics

    def evaluate(self):
        """
        Evaluate the model on the validation set.

        Returns:
            dict: Evaluation metrics
        """
        with torch.no_grad():
            self.model.eval()
            val_truth = []
            val_preds = []
            it = tqdm(self.eval_loader, desc="Evaluating")
            for batch in it:
                batch.to(self.device)
                labels = batch["labels"]
                batch.pop("labels")
                if self.fast_dtype:
                    with torch.autocast(device_type="cuda", dtype=self.fast_dtype):
                        predictions = self.model.predict(batch)["predictions"]
                else:
                    predictions = self.model.predict(batch)["predictions"]
                val_truth.append(labels.float().cpu().numpy(force=True))
                val_preds.append(predictions.float().cpu().numpy(force=True))
            val_truth = (
                np.vstack(val_truth) if labels.ndim > 1 else np.hstack(val_truth)
            )
            val_preds = (
                np.vstack(val_preds) if predictions.ndim > 1 else np.hstack(val_preds)
            )
            if not np.all(val_truth == -100):
                valid_metrics = {}
                for metric_func in self.compute_metrics:
                    valid_metrics.update(metric_func(val_truth, val_preds))

                fprint(valid_metrics)
            else:
                valid_metrics = {
                    "Validation set labels may be NaN. No metrics calculated.": 0
                }

        self.predictions.update({"valid": {"pred": val_preds, "true": val_truth}})

        return valid_metrics

    def test(self):
        """
        Test the model on the test set.

        Returns:
            dict: Test metrics and predictions
        """
        with torch.no_grad():
            self.model.eval()
            preds = []
            truth = []
            it = tqdm(self.test_loader, desc="Testing")
            for batch in it:
                batch.to(self.device)
                labels = batch["labels"]
                batch.pop("labels")
                if self.fast_dtype:
                    with torch.autocast(device_type="cuda", dtype=self.fast_dtype):
                        predictions = self.model.predict(batch)["predictions"]
                else:
                    predictions = self.model.predict(batch)["predictions"]
                truth.append(labels.float().cpu().numpy(force=True))
                preds.append(predictions.float().cpu().numpy(force=True))
            truth = np.vstack(truth) if labels.ndim > 1 else np.hstack(truth)
            preds = np.vstack(preds) if predictions.ndim > 1 else np.hstack(preds)
            if not np.all(truth == -100):
                test_metrics = {}
                for metric_func in self.compute_metrics:
                    test_metrics.update(metric_func(truth, preds))

                fprint(test_metrics)
            else:
                test_metrics = {"Test set labels may be NaN. No metrics calculated.": 0}

        self.predictions.update({"test": {"pred": preds, "true": truth}})

        return test_metrics

    def predict(self, data_loader):
        """
        Generate predictions using the model.

        Args:
            data_loader: DataLoader for prediction data

        Returns:
            torch.Tensor: Model predictions
        """
        return self.model.predict(data_loader)

    def get_model(self, **kwargs):
        """
        Get the trained model.

        Args:
            **kwargs: Additional keyword arguments

        Returns:
            The trained model
        """
        return self.model

    def compute_metrics(self):
        """
        Get the metric computation functions.

        Returns:
            list: List of metric computation functions
        """
        return self.compute_metrics

    def unwrap_model(self, model=None):
        """
        Unwrap the model from any distributed training wrappers.

        Args:
            model: Model to unwrap (default: None, uses self.model)

        Returns:
            The unwrapped model
        """
        if model is None:
            model = self.model
        try:
            return self.accelerator.unwrap_model(model)
        except:
            try:
                return model.module
            except:
                return model

    def save_model(self, path, overwrite=False, **kwargs):
        """
        Save the model to disk.

        Args:
            path (str): Path to save the model
            overwrite (bool): Whether to overwrite existing files (default: False)
            **kwargs: Additional keyword arguments
        """
        self.unwrap_model().save(path, overwrite, **kwargs)

    def _load_state_dict(self):
        """
        Load model state dictionary from temporary file.

        Returns:
            dict: Model state dictionary
        """
        if os.path.exists(self._model_state_dict_path):
            self.unwrap_model().load_state_dict(
                torch.load(self._model_state_dict_path, map_location="cpu")
            )
            self.unwrap_model().to(self.device)

    def _save_state_dict(self):
        """
        Save model state dictionary to temporary file.

        Returns:
            str: Path to temporary file
        """
        if not hasattr(self, "_model_state_dict_path"):
            # 创建临时文件，并关闭以便写入
            tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pt")
            self._model_state_dict_path = tmp_file.name
            tmp_file.close()

        try:
            if os.path.exists(self._model_state_dict_path):
                os.remove(self._model_state_dict_path)
        except Exception as e:
            fprint(
                f"Failed to remove the temporary checkpoint file {self._model_state_dict_path}: {e}"
            )

        torch.save(self.unwrap_model().state_dict(), self._model_state_dict_path)

    def _remove_state_dict(self):
        """
        Remove temporary state dictionary file.
        """
        if hasattr(self, "_model_state_dict_path"):
            try:
                if os.path.exists(self._model_state_dict_path):
                    os.remove(self._model_state_dict_path)
            except Exception as e:
                fprint(
                    f"Failed to remove the temporary checkpoint file {self._model_state_dict_path}: {e}"
                )
