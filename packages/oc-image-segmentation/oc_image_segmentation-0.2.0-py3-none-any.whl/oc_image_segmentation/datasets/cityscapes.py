"""
Cityscapes dataset class for image segmentation.

This module contains the main CityscapesDataset class for loading and processing
Cityscapes-style image segmentation datasets.
"""

import logging
from pathlib import Path
from typing import List, Optional, Tuple, Union

import numpy as np
import tensorflow as tf

from ..config import settings
from .preprocessing import (
    augment_data,
    augment_data_albumentations,
    load_image,
    load_label,
)
from .utils import get_matching_label_filename

logger = logging.getLogger(__name__)


class CityscapesDataset:
    """
    Dataset loader for Cityscapes-style image segmentation datasets.

    Expected directory structure (following original Cityscapes format):
    dataset_root/
    ├── gtFine_trainvaltest/
    │   └── gtFine/
    │       ├── train/
    │       │   ├── aachen/
    │       │   ├── berlin/
    │       │   └── ...
    │       ├── val/
    │       └── test/
    └── leftImg8bit_trainvaltest/
        └── leftImg8bit/
            ├── train/
            │   ├── aachen/
            │   ├── berlin/
            │   └── ...
            ├── val/
            └── test/
    """

    def __init__(
        self,
        dataset_root: Union[str, Path],
        split: str = "train",
        input_size: Optional[Tuple[int, int]] = None,
        batch_size: int = 1,
        shuffle: bool = False,
        augment: bool = False,
        label_mode: str = "categoryId",
    ):
        """
        Initialize the Cityscapes dataset loader.

        Args:
            dataset_root: Path to the dataset root directory
            split: Dataset split ('train', 'val', 'test')
            input_size: Target input size (height, width). If None, uses config
            batch_size: Batch size for the dataset
            shuffle: Whether to shuffle the dataset
            augment: Whether to apply data augmentation
            label_mode: Label mapping mode ('trainId' for 19 classes or 'categoryId' for 8 categories)
        """
        self.dataset_root = Path(dataset_root)
        self.split = split
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.augment = augment
        self.label_mode = label_mode

        # Validate label_mode
        if label_mode not in ["trainId", "categoryId"]:
            raise ValueError(
                f"label_mode must be 'trainId' or 'categoryId', got: {label_mode}"
            )

        if label_mode == "categoryId":
            self.num_classes = 8
        elif label_mode == "trainId":
            self.num_classes = 19

        # Get input size from config if not provided
        if input_size is None:
            # Try to get config from cityscapes model, then default, or use fallback
            try:
                model_config = settings.models.get(
                    "cityscapes",
                    getattr(settings.models, "default", None),
                )
                if model_config is None:
                    # Use the first available model's input_size or fallback
                    available_models = list(settings.models.keys())
                    if available_models:
                        model_config = settings.models[available_models[0]]
                    else:
                        model_config = {"input_size": [256, 256]}  # Fallback
                self.input_size = tuple(model_config.input_size)
            except (AttributeError, KeyError):
                self.input_size = (256, 256)  # Fallback
        else:
            self.input_size = input_size

        # Validate dataset structure
        self._validate_dataset_structure()

        # Get file paths
        self.image_paths, self.label_paths = self._get_file_paths()

        logger.info(f"Loaded {len(self.image_paths)} samples for split '{split}'")

    def _validate_dataset_structure(self) -> None:
        """Validate that the dataset has the expected structure."""
        required_dirs = [
            self.dataset_root / "leftImg8bit_trainvaltest" / "leftImg8bit" / self.split,
            self.dataset_root / "gtFine_trainvaltest" / "gtFine" / self.split,
        ]

        for dir_path in required_dirs:
            if not dir_path.exists():
                raise FileNotFoundError(f"Required directory not found: {dir_path}")

    def _get_file_paths(self) -> Tuple[List[Path], List[Path]]:
        """Get lists of image and label file paths."""
        images_base_dir = (
            self.dataset_root / "leftImg8bit_trainvaltest" / "leftImg8bit" / self.split
        )
        labels_base_dir = (
            self.dataset_root / "gtFine_trainvaltest" / "gtFine" / self.split
        )

        # Get supported image formats from config
        supported_formats = settings.image.supported_formats

        image_paths = []
        label_paths = []

        # Iterate through city directories
        for city_dir in sorted(images_base_dir.iterdir()):
            if not city_dir.is_dir():
                continue

            city_name = city_dir.name
            labels_city_dir = labels_base_dir / city_name

            if not labels_city_dir.exists():
                logger.warning(f"No labels directory found for city: {city_name}")
                continue

            # Process images in this city
            for img_path in sorted(city_dir.iterdir()):
                if img_path.suffix.lower() in supported_formats:
                    try:
                        # Use utility function to get matching label filename
                        label_filename = get_matching_label_filename(
                            img_path.name, "labelIds"
                        )
                        potential_label = labels_city_dir / label_filename

                        if potential_label.exists():
                            image_paths.append(img_path)
                            label_paths.append(potential_label)
                        else:
                            logger.warning(f"No label found for image: {img_path}")
                    except ValueError as e:
                        logger.warning(
                            f"Skipping file with invalid name format: {img_path.name} - {e}"
                        )

        return image_paths, label_paths

    def _preprocess_sample(
        self, image_path: str, label_path: str
    ) -> Tuple[tf.Tensor, tf.Tensor]:
        """Preprocess a single sample (image, label pair)."""
        image = load_image(image_path, self.input_size)
        label = load_label(label_path, self.input_size, self.label_mode)

        # Apply augmentation if enabled
        if self.augment and settings.image.preprocessing.augmentation:
            aug_config = getattr(settings, "data_augmentation", {})

            if hasattr(aug_config, "to_dict"):
                aug_config = aug_config.to_dict()

            if aug_config.get("method", "albumentations") == "albumentations":
                augment_data_func = augment_data_albumentations
            # fallback
            else:
                augment_data_func = augment_data

            image, label = augment_data_func(
                image,
                label,
                aug_config=aug_config,
            )

        return image, label

    def create_tf_dataset(self) -> tf.data.Dataset:
        """Create a TensorFlow dataset."""
        # Convert paths to strings
        image_paths_str = [str(p) for p in self.image_paths]
        label_paths_str = [str(p) for p in self.label_paths]

        max_limit = getattr(settings.image, "max_limit", None)

        if max_limit is not None and len(image_paths_str) > max_limit:
            logger.info(
                f"Limiting dataset to {max_limit} samples (original size: {len(image_paths_str)})"
            )
            image_paths_str = image_paths_str[:max_limit]
            label_paths_str = label_paths_str[:max_limit]

        # Create dataset from file paths
        dataset = tf.data.Dataset.from_tensor_slices((image_paths_str, label_paths_str))

        # Shuffle if requested
        if self.shuffle:
            dataset = dataset.shuffle(buffer_size=len(self.image_paths))

        # Map preprocessing function
        dataset = dataset.map(
            self._preprocess_sample,
            num_parallel_calls=tf.data.AUTOTUNE,
        )

        # Batch the dataset
        dataset = dataset.batch(self.batch_size)

        # Prefetch for performance
        dataset = dataset.prefetch(tf.data.AUTOTUNE)

        return dataset

    def get_sample(self, index: int) -> Tuple[np.ndarray, np.ndarray]:
        """Get a single sample by index (for debugging/visualization)."""
        if index >= len(self.image_paths):
            raise IndexError(
                f"Index {index} out of range for dataset size {len(self.image_paths)}"
            )

        image_path = str(self.image_paths[index])
        label_path = str(self.label_paths[index])

        image, label = self._preprocess_sample(image_path, label_path)

        return image.numpy(), label.numpy()

    def __len__(self) -> int:
        """Return the number of samples in the dataset."""
        return len(self.image_paths)

    @property
    def num_batches(self) -> int:
        """Return the number of batches in the dataset."""
        return len(self) // self.batch_size + (1 if len(self) % self.batch_size else 0)
