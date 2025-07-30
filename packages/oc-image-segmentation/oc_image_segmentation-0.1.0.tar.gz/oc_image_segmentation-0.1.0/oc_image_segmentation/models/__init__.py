"""
Model modules for OC Image Segmentation.

This package provides model implementations and related functionality for image segmentation tasks.
The main components are:

- Model classes: UNetModel, DeepLabV3PlusModel
- Metrics: MeanIoU for segmentation evaluation
- Factory functions: create_unet_from_config, create_deeplabv3plus_from_config
- Training and evaluation utilities
- Transfer learning and Keras Hub integration
"""

from .deeplabv3plus import DeepLabV3PlusModel
from .evaluation import evaluate_model_miou, predict_with_miou
from .factory import (
    create_deeplabv3plus_from_config,
    create_unet_from_config,
    get_model_summary,
    load_model,
    load_model_and_recompile,
    load_model_weights_safe,
    save_model_weights_only,
    save_model_without_optimizer,
)
from .metrics import MeanIoU
from .training import train_deeplabv3plus_model, train_unet_model
from .unet import UNetModel

__all__ = [
    # Metrics
    "MeanIoU",
    # Model classes
    "UNetModel",
    "DeepLabV3PlusModel",
    # Factory functions
    "create_unet_from_config",
    "create_deeplabv3plus_from_config",
    "get_model_summary",
    "load_model",
    # Improved save/load functions (no optimizer warnings)
    "load_model_and_recompile",
    "load_model_weights_safe",
    "save_model_weights_only",
    "save_model_without_optimizer",
    # Training
    "train_unet_model",
    "train_deeplabv3plus_model",
    # Evaluation
    "evaluate_model_miou",
    "predict_with_miou",
    # Transfer learning
    "load_pretrained_weights",
    "create_transfer_learning_model",
    "fine_tune_pretrained_model",
]
