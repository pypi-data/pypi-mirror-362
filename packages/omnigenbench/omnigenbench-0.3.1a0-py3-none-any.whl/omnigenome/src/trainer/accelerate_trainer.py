# -*- coding: utf-8 -*-
# file: trainer.py
# time: 14:40 06/04/2024
# author: YANG, HENG <hy345@exeter.ac.uk> (杨恒)
# github: https://github.com/yangheng95
# huggingface: https://huggingface.co/yangheng
# google scholar: https://scholar.google.com/citations?user=NPq5a_0AAAAJ&hl=en
# Copyright (C) 2019-2024. All Rights Reserved.

import os
import time
import numpy as np
from torch.utils.data import DataLoader
from tqdm import tqdm

import torch

from ..misc.utils import env_meta_info, fprint, seed_everything


def _infer_optimization_direction(metrics, prev_metrics):
    """
    Infer the optimization direction based on metric values.

    This function analyzes the trend of metric values to determine whether
    larger values are better (e.g., accuracy) or smaller values are better
    (e.g., loss).

    Args:
        metrics (dict): Current metric values
        prev_metrics (list): Previous metric values

    Returns:
        str: Either 'larger_is_better' or 'smaller_is_better'
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


class AccelerateTrainer:
    """
    A distributed training trainer using HuggingFace Accelerate.

    This trainer provides distributed training capabilities with automatic mixed precision,
    gradient accumulation, and early stopping. It supports both single and multi-GPU
    training with seamless integration with HuggingFace Accelerate.

    Attributes:
        model: The model to train
        train_loader: DataLoader for training data
        eval_loader: DataLoader for validation data
        test_loader: DataLoader for test data
        epochs: Number of training epochs
        patience: Early stopping patience
        gradient_accumulation_steps: Number of steps for gradient accumulation
        optimizer: The optimizer for training
        loss_fn: Loss function
        compute_metrics: List of metric functions to compute
        accelerator: HuggingFace Accelerate instance
        metrics: Dictionary to store training metrics
        predictions: Dictionary to store predictions

    Example:
        >>> from omnigenome.src.trainer import AccelerateTrainer
        >>> trainer = AccelerateTrainer(
        ...     model=model,
        ...     train_dataset=train_dataset,
        ...     eval_dataset=eval_dataset,
        ...     epochs=10,
        ...     batch_size=32,
        ...     optimizer=optimizer
        ... )
        >>> metrics = trainer.train()
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
        autocast: str = "float16",
        **kwargs,
    ):
        """
        Initialize the AccelerateTrainer.

        Args:
            model: The model to train
            train_dataset (torch.utils.data.Dataset, optional): Training dataset
            eval_dataset (torch.utils.data.Dataset, optional): Validation dataset
            test_dataset (torch.utils.data.Dataset, optional): Test dataset
            epochs (int, optional): Number of training epochs. Defaults to 3
            batch_size (int, optional): Batch size for training. Defaults to 8
            patience (int, optional): Early stopping patience. Defaults to -1 (no early stopping)
            gradient_accumulation_steps (int, optional): Number of steps for gradient accumulation. Defaults to 1
            optimizer (torch.optim.Optimizer, optional): Optimizer for training
            loss_fn (torch.nn.Module, optional): Loss function
            compute_metrics (list | str, optional): List of metric functions or single metric function
            seed (int, optional): Random seed for reproducibility. Defaults to 42
            autocast (str, optional): Mixed precision type. Options: 'float16', 'bfloat16', 'no'. Defaults to 'float16'
            **kwargs: Additional keyword arguments
        """
        self.model = model

        # DataLoaders
        if kwargs.get("train_loader"):
            self.train_loader = kwargs.get("train_loader")
            self.eval_loader = kwargs.get("eval_loader", None)
            self.test_loader = kwargs.get("test_loader", None)
        else:
            self.train_loader = (
                DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
                if train_dataset
                else None
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
            self.train_loader = (
                DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
                if train_dataset
                else None
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
        self.patience = patience
        self.gradient_accumulation_steps = gradient_accumulation_steps
        self.optimizer = optimizer
        self.loss_fn = loss_fn
        self.compute_metrics = (
            compute_metrics if isinstance(compute_metrics, list) else [compute_metrics]
        )
        self.compute_metrics = (
            compute_metrics if isinstance(compute_metrics, list) else [compute_metrics]
        )
        self.seed = seed
        self._optimization_direction = None
        self.trial_name = kwargs.get("trial_name", self.model.__class__.__name__)

        # Determine mixed precision from `autocast` argument if desired
        if autocast in ["float16", "fp16"]:
            mp_setting = "fp16"
        elif autocast in ["bfloat16", "bf16"]:
            mp_setting = "bf16"
        else:
            mp_setting = "no"

        # Prepare Accelerator
        from accelerate import Accelerator
        from accelerate import DistributedDataParallelKwargs

        ddp_kwargs = DistributedDataParallelKwargs(find_unused_parameters=True)

        self.accelerator = Accelerator(
            mixed_precision=mp_setting, kwargs_handlers=[ddp_kwargs]
        )

        self.accelerator = Accelerator(
            mixed_precision=mp_setting, kwargs_handlers=[ddp_kwargs]
        )
        if self.loss_fn is not None:
            self.model.set_loss_fn(self.loss_fn)
            # 创建 dataloaders
            if kwargs.get("train_loader"):
                self.train_loader = kwargs.get("train_loader")
                self.eval_loader = kwargs.get("eval_loader", None)
                self.test_loader = kwargs.get("test_loader", None)
            else:
                self.train_loader = (
                    DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
                    if train_dataset
                    else None
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

        # 让 accelerate 处理模型和优化器的准备
        to_prepare = [self.model]
        if optimizer is not None:
            to_prepare.append(optimizer)
        if self.train_loader is not None:
            to_prepare.append(self.train_loader)
        if self.eval_loader is not None:
            to_prepare.append(self.eval_loader)
        if self.test_loader is not None:
            to_prepare.append(self.test_loader)

        prepared = self.accelerator.prepare(*to_prepare)
        self.model = prepared[0]
        idx = 1
        if optimizer is not None:
            self.optimizer = prepared[idx]
            idx += 1
        if self.train_loader is not None:
            self.train_loader = prepared[idx]
            idx += 1
        if self.eval_loader is not None:
            self.eval_loader = prepared[idx]
            idx += 1
        if self.test_loader is not None:
            self.test_loader = prepared[idx]

        self.metadata = env_meta_info()
        self.metrics = {}

        self.predictions = {}

    def evaluate(self):
        """
        Evaluate the model on the validation dataset.

        This method runs the model in evaluation mode and computes metrics
        on the validation dataset. It handles distributed evaluation and
        gathers results from all processes.

        Returns:
            dict: Dictionary containing evaluation metrics

        Example:
            >>> metrics = trainer.evaluate()
            >>> print(f"Validation accuracy: {metrics['accuracy']:.4f}")
        """
        self.model.eval()
        all_truth = []
        all_preds = []

        # 禁用进度条在非主进程上显示
        it = tqdm(
            self.eval_loader,
            desc="Evaluating",
            disable=not self.accelerator.is_main_process,
        )

        with torch.no_grad():
            for batch in it:
                output = self.accelerator.unwrap_model(self.model).predict(batch)
                predictions = output["predictions"]
                labels = batch["labels"]

                # 收集所有进程的预测结果和标签
                gathered_predictions = self.accelerator.gather(predictions)
                gathered_labels = self.accelerator.gather(labels)

                # 只在主进程中处理收集到的数据
                if self.accelerator.is_main_process:
                    gathered_predictions = (
                        gathered_predictions.float().cpu().numpy(force=True)
                    )
                    gathered_labels = gathered_labels.float().cpu().numpy(force=True)
                    all_preds.append(gathered_predictions)
                    all_truth.append(gathered_labels)

        # # 同步所有进程
        # self.accelerator.wait_for_everyone()

        # 只在主进程中计算指标
        if self.accelerator.is_main_process:
            all_preds = np.concatenate(all_preds, axis=0)
            all_truth = np.concatenate(all_truth, axis=0)

            if not np.all(all_truth == -100):
                valid_metrics = {}
                for metric_func in self.compute_metrics:
                    valid_metrics.update(metric_func(all_truth, all_preds))
            else:
                valid_metrics = {
                    "Validation labels predictions may be NaN. No metrics calculated.": 0
                }

            # 打印指标信息
            fprint(valid_metrics)
        else:
            valid_metrics = None

        self.predictions.update({"valid": {"pred": all_preds, "true": all_truth}})

        return valid_metrics

    def test(self):
        """
        Test the model on the test dataset.

        This method runs the model in evaluation mode and computes metrics
        on the test dataset. It handles distributed testing and gathers
        results from all processes.

        Returns:
            dict: Dictionary containing test metrics

        Example:
            >>> metrics = trainer.test()
            >>> print(f"Test accuracy: {metrics['accuracy']:.4f}")
        """
        self.model.eval()
        all_truth = []
        all_preds = []

        it = tqdm(
            self.test_loader,
            desc="Testing",
            disable=not self.accelerator.is_main_process,
        )

        with torch.no_grad():
            for batch in it:
                output = self.accelerator.unwrap_model(self.model).predict(batch)
                predictions = output["predictions"]
                labels = batch["labels"]

                gathered_predictions = self.accelerator.gather(predictions)
                gathered_labels = self.accelerator.gather(labels)

                if self.accelerator.is_main_process:
                    gathered_predictions = (
                        gathered_predictions.float().cpu().numpy(force=True)
                    )
                    gathered_labels = gathered_labels.float().cpu().numpy(force=True)
                    all_preds.append(gathered_predictions)
                    all_truth.append(gathered_labels)

        # # 同步所有进程
        # self.accelerator.wait_for_everyone()

        # 只在主进程中计算指标
        if self.accelerator.is_main_process:
            all_preds = np.concatenate(all_preds, axis=0)
            all_truth = np.concatenate(all_truth, axis=0)

            if not np.all(all_truth == -100):
                test_metrics = {}
                for metric_func in self.compute_metrics:
                    test_metrics.update(metric_func(all_truth, all_preds))
            else:
                test_metrics = {
                    "Test labels predictions may be NaN. No metrics calculated.": 0
                }
            # 打印指标信息
            fprint(test_metrics)
        else:
            test_metrics = None

        self.predictions.update({"test": {"pred": all_preds, "true": all_truth}})

        return test_metrics

    def train(self, path_to_save=None, **kwargs):
        """
        Train the model using distributed training.

        This method performs the complete training loop with validation,
        early stopping, and model checkpointing. It handles distributed
        training across multiple GPUs and processes.

        Args:
            path_to_save (str, optional): Path to save the trained model
            **kwargs: Additional keyword arguments for model saving

        Returns:
            dict: Dictionary containing training metrics

        Example:
            >>> metrics = trainer.train(path_to_save="./checkpoints/model")
            >>> print(f"Best validation accuracy: {metrics['best_valid']['accuracy']:.4f}")
        """
        seed_everything(self.seed)
        # 在所有进程上创建早停标志
        early_stop_flag = torch.tensor(0, device=self.accelerator.device)

        # 确保所有进程同步启动
        self.accelerator.wait_for_everyone()

        # Initial validation or test
        if self.eval_loader is not None and len(self.eval_loader) > 0:
            valid_metrics = self.evaluate()
        else:
            valid_metrics = self.test()

        # 在主进程中更新指标和保存模型
        if self.accelerator.is_main_process:
            if self._is_metric_better(valid_metrics, stage="valid"):
                self._save_state_dict()
                early_stop_flag = torch.tensor(0, device=self.accelerator.device)

        # 使用 all_gather 同步早停标志
        gathered_flags = self.accelerator.gather(early_stop_flag)
        early_stop_flag = (
            gathered_flags if gathered_flags.ndim == 0 else gathered_flags[0]
        )  # 使用主进程的值

        for epoch in range(self.epochs):
            self.model.train()

            train_it = tqdm(
                self.train_loader,
                desc=f"Epoch {epoch + 1}/{self.epochs} Loss",
                disable=not self.accelerator.is_main_process,
            )
            # 使用 accelerator.accumulate 控制梯度累积
            for step, batch in enumerate(train_it):
                train_loss = []

                with self.accelerator.accumulate(self.model):
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

                train_loss.append(loss.item() * self.gradient_accumulation_steps)
                train_it.set_description(
                    f"Epoch {epoch + 1}/{self.epochs} Loss: {np.nanmean(train_loss):.4f}"
                )

            self.accelerator.backward(loss)

            self.optimizer.step()
            self.optimizer.zero_grad()

            # 同步所有进程后再进行评估
            self.accelerator.wait_for_everyone()

            if self.eval_loader is not None and len(self.eval_loader) > 0:
                valid_metrics = self.evaluate()
            else:
                valid_metrics = self.test()

            # 在主进程中更新指标和判断是否需要早停
            if self.accelerator.is_main_process:
                if self._is_metric_better(valid_metrics, stage="valid"):
                    self._save_state_dict()
                    early_stop_flag = torch.tensor(0, device=self.accelerator.device)
                else:
                    early_stop_flag += 1

            # 使用 all_gather 同步早停标志
            gathered_flags = self.accelerator.gather(early_stop_flag)
            early_stop_flag = (
                gathered_flags if gathered_flags.ndim == 0 else gathered_flags[0]
            )  # 使用主进程的值

            # 检查是否需要早停
            if early_stop_flag.item() > self.patience:
                if self.accelerator.is_main_process:
                    print(f"Early stopping at epoch {epoch + 1}.")
                    fprint(f"Early stopping at epoch {epoch + 1}.")
                break

            # 只在主进程中保存检查点
            if path_to_save and self.accelerator.is_main_process:
                _path_to_save = path_to_save + "_epoch_" + str(epoch + 1)
                if valid_metrics:
                    for key, value in valid_metrics.items():
                        _path_to_save += f"_seed_{self.seed}_{key}_{value:.4f}"
                self.save_model(_path_to_save, **kwargs)

            # 确保所有进程同步后再进入下一轮
            self.accelerator.wait_for_everyone()

        # Final test using the best checkpoint
        if self.test_loader is not None and len(self.test_loader) > 0:
            self._load_state_dict()
            self.accelerator.wait_for_everyone()  # 确保加载完成后再测试
            test_metrics = self.test()
            if self.accelerator.is_main_process:
                self._is_metric_better(test_metrics, stage="test")

        # 只在主进程中保存最终模型
        if path_to_save and self.accelerator.is_main_process:
            _path_to_save = path_to_save + "_final"
            if self.metrics.get("test"):
                for key, value in self.metrics["test"][-1].items():
                    _path_to_save += f"_seed_{self.seed}_{key}_{value:.4f}"
            self.save_model(_path_to_save, **kwargs)

        self._remove_state_dict()

        self.accelerator.free_memory()
        del (
            self.optimizer,
            self.train_loader,
            self.eval_loader,
            self.test_loader,
        )

        return self.metrics

    def _is_metric_better(self, metrics, stage="valid"):
        """
        Check if the current metrics are better than the best metrics so far.

        Args:
            metrics (dict): Current metrics
            stage (str): Stage of evaluation ('valid' or 'test')

        Returns:
            bool: True if current metrics are better, False otherwise
        """
        # 只在主进程中进行metric比较
        if not self.accelerator.is_main_process:
            return False

        assert stage in [
            "valid",
            "test",
        ], "The metrics stage should be either 'valid' or 'test'."
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

    def predict(self, data_loader):
        """
        Make predictions using the trained model.

        Args:
            data_loader: DataLoader containing data to predict on

        Returns:
            dict: Dictionary containing predictions
        """
        return self.accelerator.unwrap_model(self.model).predict(data_loader)

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
        Compute metrics for evaluation.

        This method should be implemented by subclasses to provide specific
        metric computation logic.

        Raises:
            NotImplementedError: If compute_metrics method is not implemented
        """
        raise NotImplementedError(
            "The compute_metrics() function should be implemented for your model."
            " It should return a dictionary of metrics."
        )

    def save_model(self, path, overwrite=False, **kwargs):
        """
        Save the trained model.

        Args:
            path (str): Path to save the model
            overwrite (bool, optional): Whether to overwrite existing files. Defaults to False
            **kwargs: Additional keyword arguments for model saving
        """
        # Make certain only one process saves, if you're in distributed mode
        if self.accelerator.is_main_process:
            self.accelerator.unwrap_model(self.model).save(path, overwrite, **kwargs)

    def _load_state_dict(self):
        """Load the best model state dictionary."""
        if hasattr(self, "_model_state_dict_path") and os.path.exists(
            self._model_state_dict_path
        ):
            weights = torch.load(self._model_state_dict_path, map_location="cpu")
            self.accelerator.unwrap_model(self.model).load_state_dict(weights)

    def _save_state_dict(self):
        """Save the current model state dictionary."""
        if not hasattr(self, "_model_state_dict_path"):
            from hashlib import sha256

            time_str = time.strftime("%Y%m%d_%H%M%S", time.localtime())
            hash_digest = sha256(self.__repr__().encode("utf-8")).hexdigest()
            self._model_state_dict_path = f"tmp_ckpt_{time_str}_{hash_digest}.pt"

        if os.path.exists(self._model_state_dict_path):
            os.remove(self._model_state_dict_path)

        # Use accelerator to gather model weights on one process
        if self.accelerator.is_main_process:
            torch.save(
                self.accelerator.unwrap_model(self.model).state_dict(),
                self._model_state_dict_path,
            )
            torch.save(
                self.accelerator.unwrap_model(self.model).state_dict(),
                self._model_state_dict_path,
            )

    def _remove_state_dict(self):
        """Remove the temporary model state dictionary file."""
        if not hasattr(self, "_model_state_dict_path"):
            from hashlib import sha256

            time_str = time.strftime("%Y%m%d_%H%M%S", time.localtime())
            hash_digest = sha256(self.__repr__().encode("utf-8")).hexdigest()
            self._model_state_dict_path = f"tmp_ckpt_{time_str}_{hash_digest}.pt"

        if (
            os.path.exists(self._model_state_dict_path)
            and self.accelerator.is_main_process
        ):
            os.remove(self._model_state_dict_path)
