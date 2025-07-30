"""
Callbacks module for training models.

This module provides callback functions for model training including
EarlyStopping, ModelCheckpoint, and ReduceLROnPlateau.
"""

import logging
import os
from typing import Any, Dict, List, Optional

import tensorflow as tf

from ..config import get_settings
from ..datasets.cityscapes_labels import categoryId2label, trainId2label

logger = logging.getLogger(__name__)


def create_training_callbacks(
    save_path: Optional[str] = None,
    custom_config: Optional[Dict[str, Any]] = None,
    metrics: Optional[List[tf.keras.metrics.Metric]] = None,
) -> List[tf.keras.callbacks.Callback]:
    """
    Create training callbacks based on configuration.

    Args:
        model_name: Name of the model for callback configuration
        save_path: Path to save model checkpoints
        custom_config: Custom callback configuration (overrides settings)

    Returns:
        List of configured callbacks
    """
    settings = get_settings()
    callbacks = []

    # Use custom config or get from settings
    callback_config = (
        custom_config if custom_config else getattr(settings, "callbacks", {})
    )

    # EarlyStopping callback
    if "early_stopping" in callback_config:
        early_config = callback_config["early_stopping"]
        early_stopping = tf.keras.callbacks.EarlyStopping(
            monitor=early_config.get("monitor", "val_mean_iou"),
            patience=early_config.get("patience", 10),
            mode=early_config.get("mode", "max"),
            restore_best_weights=early_config.get("restore_best_weights", True),
            min_delta=early_config.get("min_delta", 0.001),
            verbose=early_config.get("verbose", 1),
        )
        callbacks.append(early_stopping)
        logger.info(
            f"Added EarlyStopping callback: monitor={early_config.get('monitor', 'val_mean_iou')}, patience={early_config.get('patience', 10)}"
        )

    # ModelCheckpoint callback
    if "model_checkpoint" in callback_config and save_path:
        checkpoint_config = callback_config["model_checkpoint"]

        # Ensure directory exists
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        model_checkpoint = tf.keras.callbacks.ModelCheckpoint(
            filepath=save_path,
            monitor=checkpoint_config.get("monitor", "val_mean_iou"),
            save_best_only=checkpoint_config.get("save_best_only", True),
            mode=checkpoint_config.get("mode", "max"),
            save_freq=checkpoint_config.get("save_freq", "epoch"),
            save_weights_only=checkpoint_config.get("save_weights_only", False),
            verbose=checkpoint_config.get("verbose", 1),
        )
        callbacks.append(model_checkpoint)
        logger.info(f"Added ModelCheckpoint callback: save_path={save_path}")

    # ReduceLROnPlateau callback
    if "reduce_lr" in callback_config:
        reduce_lr_config = callback_config["reduce_lr"]
        reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(
            monitor=reduce_lr_config.get("monitor", "val_mean_iou"),
            factor=reduce_lr_config.get("factor", 0.5),
            patience=reduce_lr_config.get("patience", 5),
            mode=reduce_lr_config.get("mode", "max"),
            min_lr=reduce_lr_config.get("min_lr", 1e-7),
            verbose=reduce_lr_config.get("verbose", 1),
        )
        callbacks.append(reduce_lr)
        logger.info(
            f"Added ReduceLROnPlateau callback: factor={reduce_lr_config.get('factor', 0.5)}"
        )

    # Cosine Decay scheduler (if configured)
    if "cosine_decay" in callback_config:
        cosine_config = callback_config["cosine_decay"]
        initial_lr = cosine_config.get("initial_learning_rate", 0.001)
        decay_steps = cosine_config.get("decay_steps", 1000)
        alpha = cosine_config.get("alpha", 0.1)

        def cosine_decay_schedule(epoch):
            """Cosine decay learning rate schedule."""
            import math

            lr = initial_lr * (
                alpha + (1 - alpha) * (1 + math.cos(math.pi * epoch / decay_steps)) / 2
            )
            return float(lr)  # Ensure we return a Python float

        cosine_scheduler = tf.keras.callbacks.LearningRateScheduler(
            cosine_decay_schedule
        )
        callbacks.append(cosine_scheduler)
        logger.info(f"Added CosineDecay scheduler: initial_lr={initial_lr}")

    for metric in metrics or []:
        if not hasattr(metric, "name"):
            continue

        if metric.name == "per_class_iou":
            per_class_iou_logger = PerClassIoULogger(metric)
            callbacks.append(per_class_iou_logger)

        if metric.name == "per_class_dice":
            per_class_dice_logger = PerClassDiceLogger(metric)
            callbacks.append(per_class_dice_logger)

    # Default callbacks if none configured
    if not callbacks:
        logger.warning("No callbacks configured, adding default EarlyStopping")
        default_early_stopping = tf.keras.callbacks.EarlyStopping(
            monitor="val_mean_iou",
            patience=10,
            mode="max",
            restore_best_weights=True,
            verbose=1,
        )
        callbacks.append(default_early_stopping)

    logger.info(f"Created {len(callbacks)} callbacks for training")
    return callbacks


def create_default_callbacks(
    save_path: Optional[str] = None,
) -> List[tf.keras.callbacks.Callback]:
    """
    Create default callbacks for basic training.

    Args:
        save_path: Path to save model checkpoints

    Returns:
        List of default callbacks
    """
    callbacks = []

    # Default EarlyStopping
    early_stopping = tf.keras.callbacks.EarlyStopping(
        monitor="val_mean_iou",
        patience=10,
        mode="max",
        restore_best_weights=True,
        verbose=1,
    )
    callbacks.append(early_stopping)

    # Default ModelCheckpoint if save_path provided
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        model_checkpoint = tf.keras.callbacks.ModelCheckpoint(
            filepath=save_path,
            monitor="val_mean_iou",
            save_best_only=True,
            mode="max",
            verbose=1,
        )
        callbacks.append(model_checkpoint)

    # Default ReduceLROnPlateau
    reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(
        monitor="val_mean_iou",
        factor=0.5,
        patience=5,
        mode="max",
        min_lr=1e-7,
        verbose=1,
    )
    callbacks.append(reduce_lr)

    return callbacks


class ProgressiveUnfreezing(tf.keras.callbacks.Callback):
    """
    Callback to progressively unfreeze the backbone after a given number of epochs,
    and reduce the learning rate without recompiling the model.

    Parameters
    ----------
    freeze_backbone_epochs : int
        Epoch at which to unfreeze the backbone layers.
    freeze_layers : list of str
        List of layer groups to unfreeze. If it includes "backbone", unfreezing is triggered.
    metrics : list
        List of metrics (kept for compatibility if recompilation is later required).
    """

    def __init__(self, freeze_backbone_epochs, freeze_layers):
        super().__init__()
        self.freeze_backbone_epochs = freeze_backbone_epochs
        self.freeze_layers = freeze_layers
        self._already_unfrozen = False

    def on_epoch_begin(self, epoch, logs=None):
        if (
            not self._already_unfrozen
            and epoch == self.freeze_backbone_epochs
            and "backbone" in self.freeze_layers
        ):
            self._already_unfrozen = True
            logger.info(f"Epoch {epoch}: Unfreezing backbone layers")

            # Unfreeze backbone layers
            for layer in self.model.layers:
                name = layer.name.lower()
                if any(
                    b in name for b in ["resnet", "efficientnet", "mobilenet", "vgg"]
                ):
                    layer.trainable = True
                    logger.info(f"Unfrozen layer: {layer.name}")

            # Reduce learning rate (without recompiling)
            current_lr = float(
                tf.keras.backend.get_value(self.model.optimizer.learning_rate)
            )
            new_lr = current_lr * 0.1
            self.model.optimizer.learning_rate.assign(new_lr)

            logger.info(f"Reduced learning rate from {current_lr:.6f} to {new_lr:.6f}")


class PerClassIoULogger(tf.keras.callbacks.Callback):
    def __init__(self, metric, class_names=None):
        super().__init__()
        self.metric = metric
        if metric.num_classes == 8:
            self.class_names = {
                k: label.category for k, label in categoryId2label.items()
            }
        elif metric.num_classes == 19:
            self.class_names = {k: label.name for k, label in trainId2label.items()}
        else:
            self.class_names = class_names or [
                f"Class {i}" for i in range(metric.num_classes)
            ]
        logger.info(
            f"Initialized PerClassIoULogger with classes: {self.class_names.values()}"
        )

    def on_epoch_end(self, epoch, logs=None):
        per_class_iou = self.metric.per_class_result().numpy()
        for i, score in enumerate(per_class_iou):
            logs[f"val_per_class_iou_{self.class_names[i]}"] = float(score)


class PerClassDiceLogger(tf.keras.callbacks.Callback):
    def __init__(self, metric, class_names=None):
        super().__init__()
        self.metric = metric
        if metric.num_classes == 8:
            self.class_names = {
                k: label.category for k, label in categoryId2label.items()
            }
        elif metric.num_classes == 19:
            self.class_names = {k: label.name for k, label in trainId2label.items()}
        else:
            self.class_names = class_names or [
                f"Class {i}" for i in range(metric.num_classes)
            ]
        logger.info(
            f"Initialized PerClassDiceLogger with classes: {self.class_names.values()}"
        )

    def on_epoch_end(self, epoch, logs=None):
        dice_scores = self.metric.result().numpy()
        for i, score in enumerate(dice_scores):
            logs[f"val_per_class_dice_{self.class_names[i]}"] = float(score)
