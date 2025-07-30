"""
Training functions for models.

This module contains functions for training different model architectures.
"""

import logging
from typing import Callable, List, Optional

import numpy as np
import tensorflow as tf

# Import here to avoid circular imports
from ..config import get_settings
from ..datasets import create_cityscapes_datasets
from ..datasets.utils import analyze_class_distribution
from ..utils import handle_exceptions
from ..utils import plot_history as plot
from .callbacks import (
    PerClassDiceLogger,
    PerClassIoULogger,
    ProgressiveUnfreezing,
    create_training_callbacks,
)
from .factory import (
    create_deeplabv3plus_from_config,
    create_unet_from_config,
)

logger = logging.getLogger(__name__)


def apply_fine_tuning_strategy(model, model_name: str, fine_tuning_config: dict):
    """
    Apply fine-tuning strategy to a model.

    Args:
        model: The Keras model to fine-tune
        model_name: Name of the model (unet, deeplabv3plus, etc.)
        fine_tuning_config: Fine-tuning configuration

    Returns:
        Tuple of (modified_model, fine_tuning_callbacks)
    """
    logger.info(f"Applying fine-tuning strategy for {model_name}")

    # Get model-specific fine-tuning config
    model_config = fine_tuning_config.get("models", {}).get(model_name, {})

    # Phase 1: Freeze specified layers
    freeze_layers = model_config.get("freeze_layers", [])
    freeze_backbone_epochs = model_config.get("freeze_backbone_epochs", 0)

    if freeze_layers:
        logger.info(f"Freezing layers: {freeze_layers}")

        for layer in model.layers:
            layer_name = layer.name.lower()

            # Freeze based on layer type
            should_freeze = False

            if "backbone" in freeze_layers:
                # Freeze backbone layers (ResNet, EfficientNet, etc.)
                if any(
                    backbone in layer_name
                    for backbone in ["resnet", "efficientnet", "mobilenet", "vgg"]
                ):
                    should_freeze = True

            if "encoder" in freeze_layers:
                # Freeze encoder layers for U-Net
                if any(
                    enc_layer in layer_name
                    for enc_layer in ["conv2d", "batch_normalization", "max_pooling"]
                ):
                    # Only freeze encoder part (first half of layers)
                    layer_idx = model.layers.index(layer)
                    if layer_idx < len(model.layers) // 2:
                        should_freeze = True

            if should_freeze:
                layer.trainable = False
                logger.info(f"Frozen layer: {layer.name}")

    # Create fine-tuning specific callbacks
    ft_callbacks = []

    # Progressive unfreezing callback
    if freeze_backbone_epochs > 0:
        ft_callbacks.append(
            ProgressiveUnfreezing(freeze_backbone_epochs, freeze_layers)
        )

    return model, ft_callbacks


def get_fine_tuning_optimizer(fine_tuning_config: dict, model_name: str):
    """
    Get optimizer configured for fine-tuning.

    Args:
        fine_tuning_config: Fine-tuning configuration
        model_name: Name of the model

    Returns:
        TensorFlow optimizer
    """
    # Get model-specific config
    model_config = fine_tuning_config.get("models", {}).get(model_name, {})
    general_config = fine_tuning_config.get("optimizer", {})

    # Get learning rate (model-specific overrides general)
    learning_rate = model_config.get(
        "learning_rate", general_config.get("learning_rate", 0.0001)
    )

    # Get optimizer type
    optimizer_name = general_config.get("name", "adam").lower()

    # Create optimizer
    if optimizer_name == "adamw":
        optimizer = tf.keras.optimizers.AdamW(
            learning_rate=learning_rate,
            beta_1=general_config.get("beta_1", 0.9),
            beta_2=general_config.get("beta_2", 0.999),
            epsilon=general_config.get("epsilon", 1e-7),
            weight_decay=general_config.get("weight_decay", 0.01),
        )
    else:  # Default to Adam
        optimizer = tf.keras.optimizers.Adam(
            learning_rate=learning_rate,
            beta_1=general_config.get("beta_1", 0.9),
            beta_2=general_config.get("beta_2", 0.999),
            epsilon=general_config.get("epsilon", 1e-7),
        )

    logger.info(
        f"Created {optimizer_name} optimizer with learning_rate={learning_rate}"
    )
    return optimizer


def create_fine_tuning_callbacks(
    fine_tuning_config: dict,
    save_path: str,
    metrics: Optional[List[tf.keras.metrics.Metric]] = None,
):
    """
    Create callbacks optimized for fine-tuning.

    Args:
        fine_tuning_config: Fine-tuning configuration
        save_path: Path to save the model

    Returns:
        List of callbacks
    """
    callbacks = []
    callbacks_config = fine_tuning_config.get("callbacks", {})

    # Early stopping
    early_stopping_config = callbacks_config.get("early_stopping", {})
    if early_stopping_config:
        early_stopping = tf.keras.callbacks.EarlyStopping(
            monitor=early_stopping_config.get("monitor", "val_mean_iou"),
            patience=early_stopping_config.get("patience", 8),
            mode=early_stopping_config.get("mode", "max"),
            restore_best_weights=early_stopping_config.get(
                "restore_best_weights", True
            ),
            min_delta=early_stopping_config.get("min_delta", 0.0001),
            verbose=early_stopping_config.get("verbose", 1),
        )
        callbacks.append(early_stopping)
        logger.info("Added EarlyStopping callback for fine-tuning")

    # Model checkpoint
    checkpoint_config = callbacks_config.get("model_checkpoint", {})
    if checkpoint_config:
        checkpoint = tf.keras.callbacks.ModelCheckpoint(
            filepath=checkpoint_config.get("filepath", save_path),
            monitor=checkpoint_config.get("monitor", "val_mean_iou"),
            save_best_only=checkpoint_config.get("save_best_only", True),
            mode=checkpoint_config.get("mode", "max"),
            save_weights_only=checkpoint_config.get("save_weights_only", False),
            verbose=checkpoint_config.get("verbose", 1),
        )
        callbacks.append(checkpoint)
        logger.info("Added ModelCheckpoint callback for fine-tuning")

    # Reduce learning rate
    reduce_lr_config = callbacks_config.get("reduce_lr", {})
    if reduce_lr_config:
        reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(
            monitor=reduce_lr_config.get("monitor", "val_mean_iou"),
            factor=reduce_lr_config.get("factor", 0.2),
            patience=reduce_lr_config.get("patience", 5),
            mode=reduce_lr_config.get("mode", "max"),
            min_lr=reduce_lr_config.get("min_lr", 1e-9),
            verbose=reduce_lr_config.get("verbose", 1),
        )
        callbacks.append(reduce_lr)
        logger.info("Added ReduceLROnPlateau callback for fine-tuning")

    # Learning rate scheduler
    lr_scheduler_config = fine_tuning_config.get("lr_scheduler", {})
    if lr_scheduler_config:
        scheduler_type = lr_scheduler_config.get("type", "cosine_decay_restarts")

        if scheduler_type == "cosine_decay_restarts":
            initial_lr = lr_scheduler_config.get("initial_learning_rate", 0.0001)
            first_decay_steps = lr_scheduler_config.get("first_decay_steps", 1000)
            t_mul = lr_scheduler_config.get("t_mul", 2.0)
            m_mul = lr_scheduler_config.get("m_mul", 1.0)
            alpha = lr_scheduler_config.get("alpha", 0.0)

            def cosine_decay_restarts_schedule(epoch):
                """Cosine decay with restarts learning rate schedule."""
                import math

                # Calculate which restart cycle we're in
                total_epochs = epoch
                current_cycle_start = 0
                current_decay_steps = first_decay_steps

                while total_epochs >= current_decay_steps:
                    total_epochs -= current_decay_steps
                    current_cycle_start += current_decay_steps
                    current_decay_steps = int(current_decay_steps * t_mul)

                # Position within current cycle (0.0 to 1.0)
                cycle_progress = total_epochs / current_decay_steps

                # Cosine decay within cycle
                cosine_value = 0.5 * (1 + math.cos(math.pi * cycle_progress))
                lr = (
                    alpha
                    + (initial_lr * m_mul ** (epoch // first_decay_steps) - alpha)
                    * cosine_value
                )

                return float(max(lr, alpha))  # Ensure LR doesn't go below alpha

            lr_scheduler = tf.keras.callbacks.LearningRateScheduler(
                cosine_decay_restarts_schedule, verbose=1
            )
            callbacks.append(lr_scheduler)
            logger.info(
                f"Added CosineDecayRestarts scheduler: initial_lr={initial_lr}, first_decay_steps={first_decay_steps}"
            )

        elif scheduler_type == "cosine_decay":
            initial_lr = lr_scheduler_config.get("initial_learning_rate", 0.0001)
            decay_steps = lr_scheduler_config.get("decay_steps", 1000)
            alpha = lr_scheduler_config.get("alpha", 0.0)

            def cosine_decay_schedule(epoch):
                """Simple cosine decay learning rate schedule."""
                import math

                lr = alpha + (initial_lr - alpha) * 0.5 * (
                    1 + math.cos(math.pi * epoch / decay_steps)
                )
                return float(max(lr, alpha))

            lr_scheduler = tf.keras.callbacks.LearningRateScheduler(
                cosine_decay_schedule, verbose=1
            )
            callbacks.append(lr_scheduler)
            logger.info(
                f"Added CosineDecay scheduler: initial_lr={initial_lr}, decay_steps={decay_steps}"
            )

        else:
            logger.warning(f"Unsupported lr_scheduler type: {scheduler_type}")

    for metric in metrics or []:
        if not hasattr(metric, "name"):
            continue

        if metric.name == "per_class_iou":
            per_class_iou_logger = PerClassIoULogger(metric)
            callbacks.append(per_class_iou_logger)

        if metric.name == "per_class_dice":
            per_class_dice_logger = PerClassDiceLogger(metric)
            callbacks.append(per_class_dice_logger)

    return callbacks


def _train_segmentation_model(
    model_name: str,
    dataset_path: str,
    model_factory: Callable[[str], object],
    exception_msg: str,
    is_fine_tuning: bool = False,
    plot_history: bool = False,
    resume_from: Optional[str] = None,
    save_path: Optional[str] = None,
    epochs: Optional[int] = None,
) -> bool:
    """
    Train a segmentation model (generic function for U-Net, DeepLabV3+, etc.).

    Parameters
    ----------
    model_name : str
        Name of the model configuration.
    dataset_path : str
        Path to the dataset.
    model_factory : Callable
        Factory function to create the model from config.
    exception_msg : str
        Custom log message for exception handling.
    is_fine_tuning : bool, optional
        Whether to enable fine-tuning mode.
    plot_history : bool, optional
        Whether to plot the training history.
    resume_from : str, optional
        Checkpoint path to resume training.
    save_path : str, optional
        Path to save the trained model.
    epochs : int, optional
        Number of epochs to train.

    Returns
    -------
    bool
        True if training successful, False otherwise.
    """
    try:
        logger.info(f"Starting training for {model_name}")
        settings = get_settings()

        model_config = getattr(settings.models, model_name, None)
        training_config = getattr(settings, "training", {})

        if save_path is None:
            save_path = getattr(model_config, "path", f"models/{model_name}_trained.h5")
            logger.info(f"Using save path: {save_path}")

        train_dataset, val_dataset, _ = create_cityscapes_datasets(
            dataset_root=dataset_path
        )
        if train_dataset is None:
            logger.error("Failed to load training dataset")
            return False

        # -- class_weight

        train_tf_dataset = train_dataset.create_tf_dataset()
        val_tf_dataset = val_dataset.create_tf_dataset() if val_dataset else None

        class_weight = None
        class_weight_config = training_config.get("class_weight", "weighted")
        num_classes = train_dataset.num_classes

        if class_weight_config == "balanced":
            class_weight = {i: 1.0 for i in range(num_classes)}
        elif class_weight_config == "weighted":
            y_true_counts = np.zeros(num_classes, dtype=int)
            for _, mask in train_tf_dataset.take(100):
                labels = mask.numpy().flatten()
                for c in range(num_classes):
                    y_true_counts[c] += np.sum(labels == c)
            freqs = y_true_counts / np.sum(y_true_counts)
            weights = 1.0 / (freqs + 1e-6)
            weights = weights / np.sum(weights) * len(freqs)
            class_weight = {i: weights[i] for i in range(num_classes)}

        # -- model

        model_wrapper = model_factory(
            model_name,
            class_weight=class_weight,
            num_classes=train_dataset.num_classes,
        )
        fine_tuning_config = getattr(settings, "fine_tuning", {})
        is_fine_tuning = is_fine_tuning or fine_tuning_config.get("enabled", False)

        if is_fine_tuning:
            logger.info("Fine-tuning enabled")
            model_wrapper.model, ft_callbacks = apply_fine_tuning_strategy(
                model_wrapper.model, model_name, fine_tuning_config
            )
            ft_optimizer = get_fine_tuning_optimizer(fine_tuning_config, model_name)
            model_wrapper.model.compile(
                optimizer=ft_optimizer,
                loss=model_wrapper.model.loss,
                metrics=model_wrapper._metrics,
            )
            ft_specific_callbacks = create_fine_tuning_callbacks(
                fine_tuning_config, save_path, metrics=model_wrapper._metrics
            )
            callbacks = ft_specific_callbacks + ft_callbacks
        else:
            callbacks = create_training_callbacks(
                save_path=save_path, metrics=model_wrapper._metrics
            )

        if resume_from:
            try:
                model_wrapper.load_weights(resume_from)
                logger.info(f"Resumed from checkpoint: {resume_from}")
            except Exception as e:
                logger.error(f"Could not load weights: {e}")
                return False

        effective_epochs = (
            (
                fine_tuning_config.get("models", {}).get(model_name, {}).get("epochs")
                if is_fine_tuning
                else None
            )
            or (fine_tuning_config.get("epochs") if is_fine_tuning else None)
            or epochs
            or training_config.get("epochs", 10)
        )

        validation_split = training_config.get("validation_split", 0.2)

        logger.info("Training configuration:")
        logger.info(f"  - Epochs: {effective_epochs}")
        logger.info(f"  - Validation split: {validation_split}")
        logger.info(f"  - Class weight: {class_weight_config}")

        history = model_wrapper.model.fit(
            train_tf_dataset,
            epochs=effective_epochs,
            validation_data=val_tf_dataset,
            callbacks=callbacks,
            # class_weight=class_weight,  ? not work with label_mode categoryId
            verbose=1,
        )

        if plot_history:
            if val_tf_dataset:
                analyze_class_distribution(
                    val_tf_dataset,
                    num_classes=num_classes,
                )
            plot(history)

        if save_path:
            model_wrapper.save(save_path)
            logger.info(f"Model saved to {save_path}")

        logger.info("Training completed successfully")
        return True

    except Exception as e:
        logger.error(f"{exception_msg}: {e}")
        return False


@handle_exceptions(default_return=False, log_message="U-Net training failed")
def train_unet_model(
    model_name: str,
    dataset_path: str,
    is_fine_tuning: bool = False,
    plot_history: bool = False,
    resume_from: Optional[str] = None,
    save_path: Optional[str] = None,
    epochs: Optional[int] = None,
) -> bool:
    """
    Train a U-Net model (wrapper for backward compatibility).
    """
    return _train_segmentation_model(
        model_name=model_name,
        dataset_path=dataset_path,
        model_factory=create_unet_from_config,
        exception_msg="U-Net training failed",
        is_fine_tuning=is_fine_tuning,
        plot_history=plot_history,
        resume_from=resume_from,
        save_path=save_path,
        epochs=epochs,
    )


@handle_exceptions(default_return=False, log_message="DeepLabV3+ training failed")
def train_deeplabv3plus_model(
    model_name: str,
    dataset_path: str,
    is_fine_tuning: bool = False,
    plot_history: bool = False,
    resume_from: Optional[str] = None,
    save_path: Optional[str] = None,
    epochs: Optional[int] = None,
) -> bool:
    """
    Train a DeepLabV3+ model (wrapper for backward compatibility).
    """
    return _train_segmentation_model(
        model_name=model_name,
        dataset_path=dataset_path,
        model_factory=create_deeplabv3plus_from_config,
        exception_msg="DeepLabV3+ training failed",
        is_fine_tuning=is_fine_tuning,
        plot_history=plot_history,
        resume_from=resume_from,
        save_path=save_path,
        epochs=epochs,
    )
