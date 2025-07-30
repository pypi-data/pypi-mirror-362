"""
Factory functions for creating models.

This module contains factory functions for creating configured model instances
from configuration settings.
"""

import logging
import warnings
from pathlib import Path
from typing import Any, Dict, Optional, Type

import numpy as np
import tensorflow as tf

from ..config import (
    get_model_config,
    settings,
)
from .deeplabv3plus import DeepLabV3PlusModel
from .unet import UNetModel

logger = logging.getLogger(__name__)


def _create_model_from_config(
    model_name: str,
    model_class: Type,
    default_config: Dict[str, Any],
    class_weight: Optional[np.array] = None,
    num_classes: Optional[int] = 8,
) -> Any:
    """
    Create and compile a segmentation model from config.

    Parameters
    ----------
    model_name : str
        Name of the model in the settings config.
    model_class : Type
        The model class to instantiate (e.g., UNetModel, DeepLabV3PlusModel).
    default_config : dict
        Default configuration to use if not found in settings.

    Returns
    -------
    Any
        Instantiated and compiled model.
    """
    model_configs = getattr(settings, "models", {})
    model_config = model_configs.get(model_name, default_config)

    if model_name not in model_configs:
        logger.warning(
            f"Model '{model_name}' not found in config, using default settings"
        )

    # Instantiate the model
    model = model_class(
        input_size=tuple(model_config.get("input_size", [256, 256])),
        num_classes=num_classes,
        **{
            k: v
            for k, v in model_config.items()
            if k not in {"input_size", "classes", "optimizer"}
        },
    )

    # Build model
    model.build_model()

    # Compile model if needed
    optimizer_config = model_config.get("optimizer", {"name": "adam"})
    if optimizer_config:
        metrics = optimizer_config.get("metrics", []) or []

        model.compile_model(
            optimizer=optimizer_config.get("name", "adam"),
            class_weight=class_weight,
            learning_rate=optimizer_config.get("learning_rate", 1e-4),
            loss=optimizer_config.get("loss", "weighted"),
            metrics=metrics,
        )

    logger.info(f"Model '{model_name}' created successfully")
    return model


def create_unet_from_config(
    model_name: str = "unet",
    class_weight: Optional[np.array] = None,
    num_classes: Optional[int] = 8,
) -> UNetModel:
    """
    Create a U-Net model from configuration settings.

    Parameters
    ----------
    model_name : str
        Name of the model configuration in settings.

    Returns
    -------
    UNetModel
        Configured UNetModel instance.
    """
    default_config = {
        "input_size": [256, 256],
        "classes": 8,
        "filters": 64,
        "dropout_rate": 0.2,
        "batch_norm": True,
        "use_attention": False,
    }

    return _create_model_from_config(
        model_name=model_name,
        model_class=UNetModel,
        default_config=default_config,
        class_weight=class_weight,
        num_classes=num_classes,
    )


def create_deeplabv3plus_from_config(
    model_name: str = "deeplabv3plus",
    class_weight: Optional[np.array] = None,
    num_classes: Optional[int] = 8,
) -> DeepLabV3PlusModel:
    """
    Create a DeepLabV3+ model from configuration settings.

    Parameters
    ----------
    model_name : str
        Name of the model configuration in settings.

    Returns
    -------
    DeepLabV3PlusModel
        Configured DeepLabV3PlusModel instance.
    """
    from .deeplabv3plus import DeepLabV3PlusModel  # Avoid circular import

    default_config = {
        "input_size": [256, 256],
        "classes": 8,
        "backbone": "efficientnetv2b3",
        "aspp_filters": 128,
        "decoder_filters": 128,
        "dropout_rate": 0.2,
        "aspp_dilations": [6, 12, 18],
    }

    return _create_model_from_config(
        model_name=model_name,
        model_class=DeepLabV3PlusModel,
        default_config=default_config,
        class_weight=class_weight,
        num_classes=num_classes,
    )


def get_model_summary(model_name: str = "unet") -> str:
    """
    Get a string summary of the model architecture.

    Args:
        model_name: Name of the model configuration

    Returns:
        Model summary as string
    """
    if model_name in ["unet", "unet_attention"]:
        # Create U-Net model
        unet = create_unet_from_config(model_name)
        model = unet.model
    elif model_name in ["deeplabv3plus", "deeplabv3plus_resnet101"]:
        # Create DeepLabV3+ model
        deeplabv3plus = create_deeplabv3plus_from_config(model_name)
        model = deeplabv3plus.model
    else:
        raise ValueError(f"Model summary not supported for: {model_name}")

    # Capture summary as string
    summary_lines = []
    model.summary(print_fn=lambda x: summary_lines.append(x))

    return "\n".join(summary_lines)


def load_model(
    model: str = "default",
    model_path: str = None,
) -> any:
    # Get model configuration
    try:
        model_config = get_model_config(model)
        logger.debug(f"Model config: {model_config}")
    except ValueError as e:
        logger.error(str(e))
        return False

    # Map model names to actual implementations
    model_mapping = {
        "default": "unet",
        "unet": "unet",
        "unet_attention": "unet_attention",
        "deeplabv3plus": "deeplabv3plus",
        "deeplabv3plus_resnet101": "deeplabv3plus_resnet101",
    }

    # Get actual model name
    actual_model = model_mapping.get(model, model)
    logger.info(f"Using model implementation: {actual_model}")

    # Create and load the model
    try:
        if actual_model in ["unet", "unet_attention"]:
            # Create U-Net model
            logger.info("Creating U-Net model...")
            model_instance = create_unet_from_config(actual_model)

        elif actual_model in ["deeplabv3plus", "deeplabv3plus_resnet101"]:
            # Create DeepLabV3+ model
            logger.info("Creating DeepLabV3+ model...")
            model_instance = create_deeplabv3plus_from_config(actual_model)

        else:
            logger.error(f"Unknown model: {actual_model}")
            return False

    except Exception as e:
        logger.error(f"Error creating/loading model: {e}")
        return False

    if Path(model_path).exists():
        logger.info(f"Loading weights from: {model_path}")
        if model_path.endswith(".weights.h5"):
            # Use our safe weight loading function
            load_model_weights_safe(model_instance, model_path)
        else:
            # For full model files, load and recompile to avoid optimizer issues
            loaded_model = load_model_and_recompile(model_path, model_config)
            if loaded_model:
                model_instance.model = loaded_model
            else:
                logger.warning("Failed to load model, using uninitialized weights")
    else:
        logger.warning(f"Model weights not found at {model_path}")
        logger.warning("Using randomly initialized weights - results may be poor")

    return model_instance


def save_model_weights_only(model, filepath: str, verbose: bool = True):
    """
    Save only model weights without optimizer state to avoid compatibility issues.

    Args:
        model: Keras model or model wrapper to save
        filepath: Path where to save the weights
        verbose: Whether to print save information

    Returns:
        True if successful, False otherwise
    """
    try:
        # Extract the Keras model if it's wrapped
        keras_model = getattr(model, "model", model)

        # Ensure the filepath has the correct extension
        if not filepath.endswith(".weights.h5"):
            if filepath.endswith(".h5"):
                filepath = filepath.replace(".h5", ".weights.h5")
            else:
                filepath = filepath + ".weights.h5"

        # Save only weights (no optimizer state)
        keras_model.save_weights(filepath)

        if verbose:
            logger.info(f"Model weights saved successfully to: {filepath}")
            logger.info("Optimizer state not saved - avoiding compatibility issues")

        return True

    except Exception as e:
        logger.error(f"Failed to save model weights to {filepath}: {e}")
        return False


def save_model_without_optimizer(model, filepath: str, verbose: bool = True):
    """
    Save complete model structure and weights but without optimizer state.

    Args:
        model: Keras model or model wrapper to save
        filepath: Path where to save the model
        verbose: Whether to print save information

    Returns:
        True if successful, False otherwise
    """
    try:
        # Extract the Keras model if it's wrapped
        keras_model = getattr(model, "model", model)

        # Save model without optimizer
        if filepath.endswith(".keras"):
            keras_model.save(filepath, include_optimizer=False)
        else:
            keras_model.save(filepath, include_optimizer=False)

        if verbose:
            logger.info(f"Model saved successfully to: {filepath}")
            logger.info("Optimizer state excluded - avoiding compatibility issues")

        return True

    except Exception as e:
        logger.error(f"Failed to save model to {filepath}: {e}")
        return False


def save_model_with_fresh_optimizer(model, filepath: str, verbose: bool = True):
    """
    Save model and reset optimizer to avoid state incompatibility.

    Args:
        model: Keras model or model wrapper to save
        filepath: Path where to save the model
        verbose: Whether to print save information

    Returns:
        True if successful, False otherwise
    """
    try:
        # Extract the Keras model if it's wrapped
        keras_model = getattr(model, "model", model)

        # Get current optimizer configuration
        optimizer_config = keras_model.optimizer.get_config()

        # Create a fresh optimizer with same configuration but no state
        fresh_optimizer = tf.keras.optimizers.get(optimizer_config)

        # Temporarily replace optimizer
        original_optimizer = keras_model.optimizer
        keras_model.optimizer = fresh_optimizer

        try:
            # Save with fresh optimizer (minimal state)
            if filepath.endswith(".keras"):
                keras_model.save(filepath)
            else:
                keras_model.save(filepath)

            if verbose:
                logger.info(f"Model saved successfully to: {filepath}")
                logger.info(
                    "Optimizer reset to fresh state - avoiding compatibility issues"
                )

            return True

        finally:
            # Restore original optimizer
            keras_model.optimizer = original_optimizer

    except Exception as e:
        logger.error(f"Failed to save model with fresh optimizer to {filepath}: {e}")
        return False


def load_model_weights_safe(model, filepath: str, verbose: bool = True):
    """
    Load model weights safely without optimizer state warnings.

    Args:
        model: Keras model or model wrapper to load weights into
        filepath: Path to the weights file
        verbose: Whether to print load information

    Returns:
        True if successful, False otherwise
    """
    try:
        # Extract the Keras model if it's wrapped
        keras_model = getattr(model, "model", model)

        with warnings.catch_warnings():
            # Suppress optimizer warnings during weight loading
            warnings.filterwarnings(
                "ignore", message=".*Skipping variable loading.*", category=UserWarning
            )
            warnings.filterwarnings("ignore", category=UserWarning, module="keras.*")

            # Load only weights
            keras_model.load_weights(filepath)

        if verbose:
            logger.info(f"Model weights loaded successfully from: {filepath}")
            logger.info("Optimizer warnings suppressed during loading")

        return True

    except Exception as e:
        logger.error(f"Failed to load model weights from {filepath}: {e}")
        return False


def load_model_and_recompile(
    filepath: str, model_config: dict = None, verbose: bool = True
):
    """
    Load a model and recompile with fresh optimizer to avoid compatibility issues.

    Args:
        filepath: Path to the saved model
        model_config: Optional model configuration for compilation
        verbose: Whether to print load information

    Returns:
        Loaded and recompiled model, or None if failed
    """
    try:
        with warnings.catch_warnings():
            # Suppress optimizer warnings during loading
            warnings.filterwarnings(
                "ignore", message=".*Skipping variable loading.*", category=UserWarning
            )
            warnings.filterwarnings("ignore", category=UserWarning, module="keras.*")

            # Load model without compilation first
            model = tf.keras.models.load_model(filepath, compile=False)

        # Recompile with fresh optimizer if config provided
        if model_config:
            optimizer_config = model_config.get("optimizer", {})
            if optimizer_config:
                model.compile(
                    optimizer=optimizer_config.get("name", "adam"),
                    loss=optimizer_config.get("loss", "weighted"),
                    # TODO: Handle metrics properly
                    metrics=optimizer_config.get("metrics", None) or [],
                )

                if verbose:
                    logger.info("Model recompiled with fresh optimizer configuration")

        if verbose:
            logger.info(f"Model loaded successfully from: {filepath}")

        return model

    except Exception as e:
        logger.error(f"Failed to load and recompile model from {filepath}: {e}")
        return None
