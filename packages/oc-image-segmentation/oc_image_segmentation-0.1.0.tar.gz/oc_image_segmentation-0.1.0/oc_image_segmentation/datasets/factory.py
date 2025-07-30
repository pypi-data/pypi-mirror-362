"""
Factory functions for creating datasets.

This module contains factory functions for creating train, validation, and test datasets.
"""

import logging
from pathlib import Path
from typing import Optional, Tuple, Union

from ..config import settings
from ..utils import handle_exceptions
from .cityscapes import CityscapesDataset

logger = logging.getLogger(__name__)


@handle_exceptions(
    default_return=(None, None, None), log_message="Dataset creation failed"
)
def create_cityscapes_datasets(
    dataset_root: Union[str, Path],
    batch_size: Optional[int] = None,
    input_size: Optional[Tuple[int, int]] = None,
) -> Tuple[CityscapesDataset, CityscapesDataset, Optional[CityscapesDataset]]:
    """
    Create train, validation, and optionally test datasets.

    Args:
        dataset_root: Path to the dataset root directory
        batch_size: Batch size for all datasets (overrides config if provided)
        input_size: Target input size (height, width)

    Returns:
        Tuple of (train_dataset, val_dataset, test_dataset)
        test_dataset is None if test split doesn't exist
    """
    dataset_root = Path(dataset_root)

    # Get training configuration
    training_config = getattr(settings, "training", {})
    dataset_config = getattr(settings, "dataset", {})

    # Use config values with parameter overrides
    effective_batch_size = (
        batch_size
        if batch_size is not None
        else training_config.get("batch_size", dataset_config.get("batch_size", 2))
    )
    shuffle_config = training_config.get("shuffle", True)

    # Get label mode from dataset configuration
    label_mode = dataset_config.get("label_mode", "trainId")

    # Log configuration usage
    logger.info("Dataset factory using configuration:")
    logger.info(f"  - Batch size: {effective_batch_size}")
    logger.info(f"  - Shuffle: {shuffle_config}")
    logger.info(f"  - Input size: {input_size}")
    logger.info(f"  - Label mode: {label_mode}")

    # Create train dataset with augmentation
    train_dataset = CityscapesDataset(
        dataset_root=dataset_root,
        split="train",
        input_size=input_size,
        batch_size=effective_batch_size,
        shuffle=shuffle_config,
        augment=True,
        label_mode=label_mode,
    )

    # Create validation dataset without augmentation
    val_dataset = CityscapesDataset(
        dataset_root=dataset_root,
        split="val",
        input_size=input_size,
        batch_size=effective_batch_size,
        shuffle=False,
        augment=False,
        label_mode=label_mode,
    )

    # Create test dataset if it exists
    test_dataset = None
    test_dir = dataset_root / "leftImg8bit_trainvaltest" / "leftImg8bit" / "test"
    if test_dir.exists():
        test_dataset = CityscapesDataset(
            dataset_root=dataset_root,
            split="test",
            input_size=input_size,
            batch_size=batch_size,
            shuffle=False,
            augment=False,
            label_mode=label_mode,
        )

    return train_dataset, val_dataset, test_dataset
