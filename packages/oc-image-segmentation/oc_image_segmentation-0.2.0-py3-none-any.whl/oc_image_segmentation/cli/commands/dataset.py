"""
Dataset commands for the CLI.
"""

import logging

import tensorflow as tf

from ...config import get_logging_config
from ...datasets import CityscapesDataset, create_cityscapes_datasets
from ...datasets.convert_labels import create_colored_label_image

# Configure logging
logging_config = get_logging_config()
logger = logging.getLogger(__name__)


def load_dataset(
    dataset_path: str,
    augment: bool = True,
    label_mode: str = "categoryId",
    split: str = "train",
    show_augmentation: bool = False,
    shuffle: bool = False,
):
    """
    Load and explore a Cityscapes dataset.

    Args:
        dataset_path: Path to the dataset root directory
        split: Dataset split to load ('train', 'val', 'test'). If None, uses config default
        show_augmentation: Whether to display sample images with augmentation applied
    """
    logger.info(f"Loading dataset from: {dataset_path}")
    logger.info(f"Split: {split}")

    try:
        # Create dataset
        dataset = CityscapesDataset(
            dataset_root=dataset_path,
            split=split,
            batch_size=1,
            shuffle=False if show_augmentation else shuffle,
            augment=augment,
            label_mode=label_mode,
        )

        logger.info("Dataset loaded successfully!")
        logger.info(f"Number of samples: {len(dataset)}")
        logger.info(f"Number of batches: {dataset.num_batches}")
        logger.info(f"Input size: {dataset.input_size}")

        # Show first few samples info
        logger.info("First few samples:")
        for i in range(min(5, len(dataset))):
            img_path = dataset.image_paths[i]
            label_path = dataset.label_paths[i]
            logger.info(f"  {i + 1}. Image: {img_path.name}")
            logger.info(f"     Label: {label_path.name}")

        # Test TensorFlow dataset creation
        logger.info("Creating TensorFlow dataset...")
        tf_dataset = dataset.create_tf_dataset()

        # Iterate through first batch
        logger.info("Testing first batch...")
        for batch_idx, (images, labels) in enumerate(tf_dataset.take(1)):
            logger.info(
                f"Batch {batch_idx}: Images shape {images.shape}, Labels shape {labels.shape}"
            )
            logger.info(f"Image dtype: {images.dtype}, Label dtype: {labels.dtype}")
            logger.info(
                f"Image range: [{images.numpy().min():.3f}, {images.numpy().max():.3f}]"
            )
            logger.info(f"Unique labels: {len(set(labels.numpy().flatten()))}")

        # Show augmentation visualization if requested
        if show_augmentation:
            if augment:
                logger.info("Displaying augmentation samples...")
                _show_augmentation_samples(dataset, tf_dataset)
            else:
                logger.info("Augmentation is not enabled in the dataset configuration.")
                logger.info(
                    "Set 'augment: true' in your settings to see augmentation effects."
                )

        logger.info("Dataset exploration completed successfully!")
        return True

    except FileNotFoundError as e:
        logger.error(f"Dataset not found: {e}")
        logger.info("Make sure your dataset follows the Cityscapes structure:")
        logger.info("dataset_root/")
        logger.info("├── leftImg8bit_trainvaltest/")
        logger.info("└── gtFine_trainvaltest/")
        return False
    except Exception as e:
        logger.error(f"Error loading dataset: {e}")
        return False


def create_all_datasets(dataset_path: str, batch_size: int = None):
    """
    Create and explore all dataset splits (train, val, test).

    Args:
        dataset_path: Path to the dataset root directory
        batch_size: Batch size for all datasets. If None, uses config default
    """
    logger.info(f"Creating all datasets from: {dataset_path}")

    try:
        train_ds, val_ds, test_ds = create_cityscapes_datasets(
            dataset_path,
            batch_size=batch_size,
        )

        logger.info("All datasets created successfully!")
        logger.info(
            f"Train dataset: {len(train_ds)} samples ({train_ds.num_batches} batches)"
        )
        logger.info(
            f"Validation dataset: {len(val_ds)} samples ({val_ds.num_batches} batches)"
        )

        if test_ds is not None:
            logger.info(
                f"Test dataset: {len(test_ds)} samples ({test_ds.num_batches} batches)"
            )
        else:
            logger.info("No test dataset found")

        return True

    except Exception as e:
        logger.error(f"Error creating datasets: {e}")
        return False


def _plot_samples(
    aug_images,
    no_aug_images,
    aug_labels,
    no_aug_labels,
    label_mode: str = "categoryId",
    num_samples: int = 8,
):
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        logger.error("matplotlib is required for augmentation visualization.")
        logger.info("Install it with: pip install matplotlib")
        return False

    # Create the visualization
    fig, axes = plt.subplots(4, num_samples, figsize=(16, 8))
    fig.suptitle("Dataset Augmentation Comparison", fontsize=16, fontweight="bold")

    for i in range(min(num_samples, aug_images.shape[0], no_aug_images.shape[0])):
        # Original image (top row)
        axes[0, i].imshow(no_aug_images[i])
        axes[0, i].axis("off")

        # Original image (top row)
        axes[1, i].imshow(
            create_colored_label_image(
                no_aug_labels[i],
                format_type=label_mode,
                raw=True,
            )
        )
        axes[1, i].axis("off")

        # Augmented image (bottom row)
        axes[2, i].imshow(aug_images[i])
        axes[2, i].axis("off")

        # Augmented image (bottom row)
        axes[3, i].imshow(
            create_colored_label_image(
                aug_labels[i],
                format_type=label_mode,
                raw=True,
            )
        )
        axes[3, i].axis("off")

    plt.tight_layout()
    plt.subplots_adjust(top=0.9)

    # Try to display the plot
    try:
        plt.show()
        logger.info("Augmentation comparison displayed. Close the window to continue.")
        logger.info(
            "Note: The comparison shows the same base images with different augmentation applied."
        )
    except Exception as display_error:
        # Fallback: save to file if display fails
        import os
        import tempfile

        temp_file = os.path.join(tempfile.gettempdir(), "augmentation_comparison.png")
        plt.savefig(temp_file, dpi=150, bbox_inches="tight")
        logger.info(
            f"Could not display plot directly. Saved comparison to: {temp_file}"
        )
        logger.warning(f"Display error: {display_error}")
        return False

    return True


def _show_augmentation_samples(dataset, tf_dataset, num_samples: int = 8):
    """
    Show sample images with and without augmentation for comparison.

    Args:
        dataset: CityscapesDataset instance
        tf_dataset: TensorFlow dataset with augmentation
        num_samples: Number of samples to display
    """
    try:
        # Import here to avoid circular imports
        from ...datasets import CityscapesDataset

        logger.info(f"Generating {num_samples} augmentation comparison samples...")

        # Create a dataset without augmentation for comparison
        dataset_no_aug = CityscapesDataset(
            dataset_root=dataset.dataset_root,
            split=dataset.split,
            batch_size=1,
            shuffle=False,  # Don't shuffle for comparison
            augment=False,  # No augmentation either
            label_mode=dataset.label_mode,
        )
        tf_dataset_no_aug = dataset_no_aug.create_tf_dataset()

        aug_images = tf.constant([])
        aug_labels = tf.constant([])

        no_aug_images = tf.constant([])
        no_aug_labels = tf.constant([])

        tf_dataset_iter = tf_dataset.as_numpy_iterator()
        tf_dataset_no_aug_iter = tf_dataset_no_aug.as_numpy_iterator()

        # Get samples from both datasets
        while aug_images.shape[0] < num_samples:
            aug_img, aug_lab = tf_dataset_iter.next()
            if aug_images.shape[0] == 0:
                aug_images = aug_img
                aug_labels = aug_lab
            else:
                aug_images = tf.concat([aug_images, aug_img], 0)
                aug_labels = tf.concat([aug_labels, aug_lab], 0)

            no_aug_img, no_aug_lab = tf_dataset_no_aug_iter.next()
            if no_aug_images.shape[0] == 0:
                no_aug_images = no_aug_img
                no_aug_labels = no_aug_lab
            else:
                no_aug_images = tf.concat([no_aug_images, no_aug_img], 0)
                no_aug_labels = tf.concat([no_aug_labels, no_aug_lab], 0)

        return _plot_samples(
            aug_images,
            no_aug_images,
            aug_labels,
            no_aug_labels,
            label_mode=dataset.label_mode,
            num_samples=num_samples,
        )

    except Exception as e:
        logger.error(f"Error creating augmentation visualization: {e}")
        return False
