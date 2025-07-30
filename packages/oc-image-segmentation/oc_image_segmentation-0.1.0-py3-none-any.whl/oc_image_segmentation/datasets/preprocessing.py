"""
Preprocessing functions for images and labels.

This module contains functions for loading, preprocessing, and augmenting
images and labels for dataset creation.
"""

from typing import Dict, Optional, Tuple

import tensorflow as tf

try:
    import albumentations as A
    import numpy as np

    ALBUMENTATIONS_AVAILABLE = True
except ImportError:
    ALBUMENTATIONS_AVAILABLE = False

from ..config import settings
from .cityscapes_labels import (
    convert_labelids_to_categoryids,
    convert_labelids_to_trainids,
)


def load_image(image_path: str, input_size: Tuple[int, int]) -> tf.Tensor:
    """
    Load and preprocess an image.

    Args:
        image_path: Path to the image file
        input_size: Target size (height, width)

    Returns:
        tf.Tensor: Preprocessed image tensor
    """
    # Read image
    image = tf.io.read_file(image_path)
    image = tf.image.decode_image(image, channels=3, expand_animations=False)
    image = tf.cast(image, tf.float32)

    # Resize to target size
    image = tf.image.resize(image, input_size)

    # Normalize if enabled in config
    if settings.image.preprocessing.normalize:
        image = image / 255.0

    return image


def load_label(
    label_path: str,
    input_size: Tuple[int, int],
    label_mode: str = "trainId",
) -> tf.Tensor:
    """
    Load and preprocess a label mask, converting labelIds to trainIds or categoryIds.

    Args:
        label_path: Path to the label file
        input_size: Target size (height, width)
        label_mode: Label mapping mode ('trainId' for 19 classes or 'categoryId' for 8 categories)

    Returns:
        tf.Tensor: Preprocessed label tensor with trainIds (0-18, 255 for ignore)
                  or categoryIds (0-7, 0 for void)
    """
    # Read label
    label = tf.io.read_file(label_path)
    label = tf.image.decode_image(label, channels=1, expand_animations=False)
    label = tf.cast(label, tf.int32)

    # Resize to target size (using nearest neighbor for labels)
    label = tf.image.resize(
        label, input_size, method=tf.image.ResizeMethod.NEAREST_NEIGHBOR
    )

    # Squeeze the channel dimension
    label = tf.squeeze(label, axis=-1)

    # Convert labelIds to trainIds or categoryIds using TensorFlow operations
    if label_mode == "categoryId":
        # Convert to categoryIds (0-7, 0 for void)
        label = tf.py_function(
            func=convert_labelids_to_categoryids, inp=[label], Tout=tf.int32
        )
    else:
        # Convert to trainIds (0-18, 255 for ignore) - default behavior
        label = tf.py_function(
            func=convert_labelids_to_trainids, inp=[label], Tout=tf.int32
        )

    # Ensure the tensor has the correct shape
    label = tf.ensure_shape(label, input_size)

    return label


def augment_data(
    image: tf.Tensor,
    label: tf.Tensor,
    aug_config: Optional[Dict] = None,
) -> Tuple[tf.Tensor, tf.Tensor]:
    """
    Apply data augmentation to image and label based on configuration settings.

    Args:
        image: Input image tensor
        label: Input label tensor

    Returns:
        Tuple[tf.Tensor, tf.Tensor]: Augmented image and label tensors
    """
    aug_config = aug_config or {}

    # Convert all config values to native Python types upfront
    enabled = bool(aug_config.get("enabled", True))
    horizontal_flip = bool(aug_config.get("horizontal_flip", False))
    vertical_flip = bool(aug_config.get("vertical_flip", False))
    rotation_range = float(aug_config.get("rotation_range", 0))
    zoom_range = float(aug_config.get("zoom_range", 0.0))

    brightness_range = (
        list(aug_config.get("brightness_range", []))
        if aug_config.get("brightness_range")
        else None
    )

    contrast_range = (
        list(aug_config.get("contrast_range", []))
        if aug_config.get("contrast_range")
        else None
    )

    noise_factor = float(aug_config.get("noise_factor", 0.0))

    # Skip if augmentation is explicitly disabled
    if not enabled:
        return image, label

    # Random horizontal flip
    if horizontal_flip and tf.random.uniform(()) > 0.5:
        image = tf.image.flip_left_right(image)
        label = tf.image.flip_left_right(tf.expand_dims(label, -1))
        label = tf.squeeze(label, -1)

    # Random vertical flip (usually disabled for street scenes)
    if vertical_flip and tf.random.uniform(()) > 0.5:
        image = tf.image.flip_up_down(image)
        label = tf.image.flip_up_down(tf.expand_dims(label, -1))
        label = tf.squeeze(label, -1)

    # Random rotation (simple implementation for small angles)
    if rotation_range > 0:
        # For small rotations, we can use a simplified approach
        # Note: For proper rotation, consider using tensorflow-addons
        angle = tf.random.uniform((), -rotation_range, rotation_range)

        # Only apply rotation if angle is significant (> 1 degree)
        if tf.abs(angle) > 1.0:
            # For now, skip rotation or implement with tensorflow-addons
            # This is a placeholder for proper rotation implementation
            pass

    # Random zoom (implemented as random crop and resize)
    if zoom_range > 0:
        # Get current shape
        shape = tf.shape(image)
        height, width = shape[0], shape[1]

        # Calculate crop size (zoom in = smaller crop, zoom out = enlarge then crop)
        zoom_factor = tf.random.uniform((), 1.0 - zoom_range, 1.0 + zoom_range)

        # For zoom in (factor < 1), make smaller crop
        # For zoom out (factor > 1), we'll pad then crop
        if tf.random.uniform(()) < 0.5:  # 50% chance for zoom in vs zoom out
            # Zoom in: smaller crop
            crop_height = tf.cast(tf.cast(height, tf.float32) / zoom_factor, tf.int32)
            crop_width = tf.cast(tf.cast(width, tf.float32) / zoom_factor, tf.int32)

            # Ensure crop is not larger than original
            crop_height = tf.minimum(crop_height, height) or 1
            crop_width = tf.minimum(crop_width, width) or 1

            # Random crop
            image = tf.image.random_crop(image, [crop_height, crop_width, 3])
            label = tf.image.random_crop(
                tf.expand_dims(label, -1), [crop_height, crop_width, 1]
            )
            label = tf.squeeze(label, -1)

            # Resize back to original size
            image = tf.image.resize(image, [height, width])
            label = tf.image.resize(
                tf.expand_dims(label, -1),
                [height, width],
                method=tf.image.ResizeMethod.NEAREST_NEIGHBOR,
            )
            label = tf.squeeze(label, -1)

    # Random brightness (only for image)
    if brightness_range and len(brightness_range) == 2:
        brightness_delta = brightness_range[1] - brightness_range[0]
        brightness_offset = brightness_range[0] - 1.0
        image = tf.image.random_brightness(image, brightness_delta) + brightness_offset

    # Random contrast (only for image)
    if contrast_range and len(contrast_range) == 2:
        image = tf.image.random_contrast(image, contrast_range[0], contrast_range[1])

    # Add noise (only for image)
    if noise_factor > 0:
        noise = tf.random.normal(tf.shape(image), stddev=noise_factor)
        image = image + noise

    # Ensure values are in valid range
    image = tf.clip_by_value(image, 0.0, 1.0)

    return image, label


def _apply_albumentations_augmentation(image_np, label_np, aug_config):
    """
    Internal function to apply Albumentations augmentation on numpy arrays.

    This function is designed to be called via tf.py_function.
    """
    # Ensure image is in uint8 format for Albumentations (0-255)
    if image_np.max() <= 1.0:
        image_np = (image_np * 255).astype(np.uint8)
    else:
        image_np = image_np.astype(np.uint8)

    # Ensure label is in correct format
    label_np = label_np.astype(np.uint8)

    # Create augmentation pipeline based on configuration
    transforms = []

    # Geometric transforms
    if aug_config.get("horizontal_flip", False):
        transforms.append(A.HorizontalFlip(p=0.5))

    if aug_config.get("vertical_flip", False):
        transforms.append(A.VerticalFlip(p=0.5))

    rotation_range = float(aug_config.get("rotation_range", 0))
    if rotation_range > 0:
        transforms.append(
            A.Rotate(
                limit=rotation_range,
                interpolation=1,  # cv2.INTER_LINEAR for image
                border_mode=0,  # cv2.BORDER_CONSTANT
                p=0.5,
            )
        )

    # Scale/Zoom transforms
    zoom_range = float(aug_config.get("zoom_range", 0))
    if zoom_range > 0:
        scale_limit = zoom_range
        transforms.append(A.RandomScale(scale_limit=scale_limit, p=0.5))

    # Shift, scale, rotate combined using Affine transform
    shift_limit = float(aug_config.get("shift_limit", 0.0))
    if shift_limit > 0:
        transforms.append(
            A.Affine(
                translate_percent={
                    "x": (-shift_limit, shift_limit),
                    "y": (-shift_limit, shift_limit),
                },
                scale=(1.0 - zoom_range, 1.0 + zoom_range),
                rotate=(-rotation_range, rotation_range),
                interpolation=1,
                p=0.3,
            )
        )

    # Elastic transform for more natural deformations
    if aug_config.get("elastic_transform", False):
        transforms.append(
            A.ElasticTransform(
                alpha=1.0,
                sigma=50.0,
                interpolation=1,
                border_mode=0,
                p=0.2,
            )
        )

    # Grid distortion
    if aug_config.get("grid_distortion", False):
        transforms.append(
            A.GridDistortion(
                num_steps=5,
                distort_limit=0.3,
                interpolation=1,
                border_mode=0,
                p=0.2,
            )
        )

    # Optical distortion
    if aug_config.get("optical_distortion", False):
        transforms.append(
            A.OpticalDistortion(
                distort_limit=0.2,
                interpolation=1,
                border_mode=0,
                p=0.2,
            )
        )

    # Color transforms (only applied to image, not mask)
    color_transforms = []

    brightness_range = aug_config.get("brightness_range")
    contrast_range = aug_config.get("contrast_range")

    if (
        brightness_range
        and len(brightness_range) == 2
        and contrast_range
        and len(contrast_range) == 2
    ):
        brightness_limit = max(
            abs(brightness_range[0] - 1.0), abs(brightness_range[1] - 1.0)
        )
        contrast_limit = max(abs(contrast_range[0] - 1.0), abs(contrast_range[1] - 1.0))
        color_transforms.append(
            A.RandomBrightnessContrast(
                brightness_limit=brightness_limit, contrast_limit=contrast_limit, p=0.5
            )
        )
    elif brightness_range and len(brightness_range) == 2:
        brightness_limit = max(
            abs(brightness_range[0] - 1.0), abs(brightness_range[1] - 1.0)
        )
        color_transforms.append(
            A.RandomBrightnessContrast(
                brightness_limit=brightness_limit, contrast_limit=0, p=0.5
            )
        )
    elif contrast_range and len(contrast_range) == 2:
        contrast_limit = max(abs(contrast_range[0] - 1.0), abs(contrast_range[1] - 1.0))
        color_transforms.append(
            A.RandomBrightnessContrast(
                brightness_limit=0, contrast_limit=contrast_limit, p=0.5
            )
        )

    # Additional color augmentations
    if aug_config.get("hue_shift", False):
        color_transforms.append(
            A.HueSaturationValue(
                hue_shift_limit=20, sat_shift_limit=30, val_shift_limit=20, p=0.3
            )
        )

    if aug_config.get("gamma", False):
        color_transforms.append(A.RandomGamma(gamma_limit=(80, 120), p=0.3))

    if aug_config.get("clahe", False):
        color_transforms.append(A.CLAHE(clip_limit=2.0, tile_grid_size=(8, 8), p=0.3))

    # Weather effects (simplified for compatibility)
    if aug_config.get("weather_effects", False):
        weather_transforms = [
            A.RandomRain(p=0.01),
            # A.RandomShadow(p=0.02),
        ]
        # Add fog and sun flare only if available
        try:
            weather_transforms.append(A.RandomFog(p=0.01))
        except Exception:
            pass
        try:
            weather_transforms.append(A.RandomSunFlare(p=0.01))
        except Exception:
            pass
        color_transforms.extend(weather_transforms)

    # Noise
    noise_factor = float(aug_config.get("noise_factor", 0.0))
    if noise_factor > 0:
        # Convert noise factor to albumentations scale (0-1 range)
        # noise_factor is typically 0.01-0.1, so we directly use it
        noise_scale = min(noise_factor, 1.0)  # Ensure it's ≤ 1.0
        color_transforms.append(A.GaussNoise(noise_scale_factor=noise_scale, p=0.3))

    # Blur effects
    if aug_config.get("blur", False):
        color_transforms.append(
            A.OneOf(
                [
                    A.MotionBlur(blur_limit=3, p=0.2),
                    A.MedianBlur(blur_limit=3, p=0.2),
                    A.GaussianBlur(blur_limit=3, p=0.2),
                ],
                p=0.2,
            )
        )

    # Apply color transforms only to image
    if color_transforms:
        transforms.append(A.OneOf(color_transforms, p=0.7))

    # Coarse dropout (cutout) with simplified parameters
    if aug_config.get("coarse_dropout", False):
        transforms.append(A.CoarseDropout(p=0.3))

    # Create the augmentation pipeline
    if transforms:
        augmentation = A.Compose(transforms)

        # Apply augmentation
        augmented = augmentation(image=image_np, mask=label_np)
        image_aug = augmented["image"]
        label_aug = augmented["mask"]
    else:
        image_aug = image_np
        label_aug = label_np

    # Normalize image back to [0, 1] range
    image_aug = image_aug.astype(np.float32) / 255.0
    label_aug = label_aug.astype(np.int32)

    return image_aug, label_aug


def augment_data_albumentations(
    image: tf.Tensor,
    label: tf.Tensor,
    aug_config: Optional[Dict] = None,
) -> Tuple[tf.Tensor, tf.Tensor]:
    """
    Apply data augmentation to image and label using Albumentations library.

    Albumentations provides more advanced and efficient augmentations compared to
    TensorFlow's built-in functions, with better support for segmentation tasks.

    Args:
        image: Input image tensor (normalized to [0, 1] range)
        label: Input label tensor
        aug_config: Augmentation configuration dictionary

    Returns:
        Tuple[tf.Tensor, tf.Tensor]: Augmented image and label tensors

    Raises:
        ImportError: If albumentations is not installed
    """
    if not ALBUMENTATIONS_AVAILABLE:
        raise ImportError(
            "Albumentations is not installed. Install it with: pip install albumentations"
        )

    aug_config = aug_config or {}

    # Convert all config values to native Python types
    enabled = bool(aug_config.get("enabled", True))

    # Skip if augmentation is explicitly disabled
    if not enabled:
        return image, label

    # Use tf.py_function to handle the numpy conversion and albumentations processing
    def _augment_wrapper(img, lbl):
        result = tf.py_function(
            func=lambda i, label: _apply_albumentations_augmentation(
                i.numpy(), label.numpy(), aug_config
            ),
            inp=[img, lbl],
            Tout=[tf.float32, tf.int32],
        )
        # Set basic shapes so TensorFlow knows it's dealing with tensors
        # We'll set precise shapes after resizing
        result[0].set_shape([None, None, 3])  # image: H x W x 3
        result[1].set_shape([None, None])  # label: H x W
        return result[0], result[1]

    # Apply augmentation
    aug_image, aug_label = _augment_wrapper(image, label)

    # Get dynamic shapes for resizing
    original_shape = tf.shape(image)
    original_height, original_width = original_shape[0], original_shape[1]

    # Ensure aug_image and aug_label have valid shapes before resizing
    # This handles cases where tf.py_function doesn't properly infer shapes
    aug_image = tf.ensure_shape(aug_image, [None, None, 3])
    aug_label = tf.ensure_shape(aug_label, [None, None])

    # Force resize back to original dimensions to ensure shape consistency
    aug_image = tf.image.resize(aug_image, [original_height, original_width])
    aug_label = tf.image.resize(
        tf.expand_dims(aug_label, -1),
        [original_height, original_width],
        method=tf.image.ResizeMethod.NEAREST_NEIGHBOR,
    )
    aug_label = tf.squeeze(aug_label, -1)
    aug_label = tf.cast(aug_label, tf.int32)

    # Set the expected shapes for TensorFlow graph optimization
    aug_image.set_shape(image.shape)
    aug_label.set_shape(label.shape)

    return aug_image, aug_label
