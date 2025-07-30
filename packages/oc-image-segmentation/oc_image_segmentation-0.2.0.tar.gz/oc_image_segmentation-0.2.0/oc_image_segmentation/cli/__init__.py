"""
CLI module for OC Image Segmentation.
"""

# Import main function from __main__.py to avoid circular imports
from .__main__ import main
from .commands.dataset import create_all_datasets, load_dataset
from .commands.model import create_model, evaluate_model, predict_image, train_model
from .commands.segment import segment_image
from .parsers.argument_parser import create_parser

__all__ = [
    "segment_image",
    "load_dataset",
    "create_all_datasets",
    "create_model",
    "train_model",
    "evaluate_model",
    "predict_image",
    "create_parser",
    "main",
]
