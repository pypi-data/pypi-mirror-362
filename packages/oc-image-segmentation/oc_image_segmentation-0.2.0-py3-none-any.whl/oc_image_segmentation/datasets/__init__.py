"""
Dataset modules for OC Image Segmentation.

This package provides dataset loading and processing functionality for image segmentation tasks.
The main components are:

- CityscapesDataset: Main dataset class for Cityscapes-style datasets
- create_cityscapes_datasets: Factory function to create train/val/test datasets
- Utility functions for filename parsing and preprocessing
"""

from .cityscapes import CityscapesDataset
from .factory import create_cityscapes_datasets
from .utils import get_matching_label_filename, parse_cityscapes_filename

__all__ = [
    "CityscapesDataset",
    "create_cityscapes_datasets",
    "parse_cityscapes_filename",
    "get_matching_label_filename",
]
