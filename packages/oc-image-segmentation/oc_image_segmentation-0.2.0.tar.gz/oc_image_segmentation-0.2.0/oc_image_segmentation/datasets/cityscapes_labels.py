"""
Cityscapes label definitions and mapping utilities.

This module provides label mappings for the Cityscapes dataset, converting
from original labelIds to trainIds for training.
Uses the official cityscapesscripts package for label definitions.
"""

from typing import Dict, List

import numpy as np

try:
    from cityscapesscripts.helpers.labels import labels
except ImportError:
    raise ImportError(
        "cityscapesscripts package is required. Install it with: pip install cityscapesscripts"
    )

# Create lookup dictionaries from official labels
name2label = {label.name: label for label in labels}
id2label = {label.id: label for label in labels}
trainId2label = {label.trainId: label for label in reversed(labels)}
categoryId2label = {label.categoryId: label for label in reversed(labels)}


def create_id_to_trainid_mapping() -> Dict[int, int]:
    """
    Create a mapping from labelId to trainId.

    Returns:
        Dictionary mapping labelId (0-33) to trainId (0-18 or 255 for ignore)
    """
    mapping = {}
    for label in labels:
        if label.id >= 0:  # Exclude -1 (license plate)
            mapping[label.id] = label.trainId
    return mapping


def create_id_to_categoryid_mapping() -> Dict[int, int]:
    """
    Create a mapping from labelId to categoryId.

    Returns:
        Dictionary mapping labelId (0-33) to categoryId (0-7)
    """
    mapping = {}
    for label in labels:
        if label.id >= 0:  # Exclude -1 (license plate)
            mapping[label.id] = label.categoryId
    return mapping


def create_trainid_to_categoryid_mapping() -> Dict[int, int]:
    """
    Create a mapping from trainId to categoryId.

    Returns:
        Dictionary mapping trainId (0-18) to categoryId (0-7) or 255 for ignore
    """
    mapping = {}
    for label in labels:
        if label.trainId >= 0:  # Valid trainIds (0-18)
            mapping[label.trainId] = label.categoryId
    # Handle ignore label
    mapping[255] = 255
    return mapping


def get_valid_train_ids() -> List[int]:
    """
    Get list of valid trainIds (0-18, excluding 255 and -1).

    Returns:
        List of valid trainIds for training
    """
    valid_ids = []
    for label in labels:
        if label.trainId >= 0 and label.trainId <= 18:  # Valid training IDs
            valid_ids.append(label.trainId)
    return sorted(list(set(valid_ids)))


def get_valid_category_ids() -> List[int]:
    """
    Get list of valid categoryIds (0-7).

    Returns:
        List of valid categoryIds for training
    """
    valid_ids = []
    for label in labels:
        if label.categoryId >= 0:
            valid_ids.append(label.categoryId)
    return sorted(list(set(valid_ids)))


def convert_labelids_to_trainids(label_image: np.ndarray) -> np.ndarray:
    """
    Convert a label image from labelIds to trainIds.

    Args:
        label_image: Input label image with labelIds (0-33)

    Returns:
        Label image with trainIds (0-18 for valid classes, 255 for ignore)
    """
    # Create the mapping
    id_to_trainid = create_id_to_trainid_mapping()

    # Initialize output with ignore value (255)
    output = np.full_like(label_image, 255, dtype=np.int32)

    # Apply mapping
    for label_id, train_id in id_to_trainid.items():
        mask = label_image == label_id
        output[mask] = train_id

    return output


def convert_labelids_to_categoryids(label_image: np.ndarray) -> np.ndarray:
    """
    Convert a label image from labelIds to categoryIds.

    Args:
        label_image: Input label image with labelIds (0-33)

    Returns:
        Label image with categoryIds (1-7 for valid categories, 0 for void/ignore)
    """
    # Create the mapping
    id_to_categoryid = create_id_to_categoryid_mapping()

    # Initialize output with void value (0)
    output = np.full_like(label_image, 0, dtype=np.int32)

    # Apply mapping
    for label_id, category_id in id_to_categoryid.items():
        mask = label_image == label_id
        output[mask] = category_id

    return output


def convert_trainids_to_categoryids(label_image: np.ndarray) -> np.ndarray:
    """
    Convert trainId image to categoryId image.

    Args:
        label_image: Input image with trainId labels (0-18, 255)

    Returns:
        Image with categoryId labels (0-7, 255)
    """
    trainid_to_categoryid = create_trainid_to_categoryid_mapping()

    output = np.full_like(label_image, 255, dtype=np.uint8)  # Default to ignore

    for train_id, category_id in trainid_to_categoryid.items():
        mask = label_image == train_id
        output[mask] = category_id

    return output


def get_category_names() -> List[str]:
    """
    Get list of category names for valid categoryIds (0-7).

    Returns:
        List of category names corresponding to categoryIds 0-7
    """
    category_names = ["void"] * 8  # Initialize with 'void' for index 0

    for label in labels:
        if 0 <= label.categoryId <= 7:
            category_names[label.categoryId] = label.category

    return category_names


def get_category_colors() -> List[tuple]:
    """
    Get list of category colors for valid categoryIds (0-7).
    Uses the color of the first label found for each category.

    Returns:
        List of RGB color tuples corresponding to categoryIds 0-7
    """
    category_colors = [(0, 0, 0)] * 8  # Initialize with black

    for label in labels:
        if 0 <= label.categoryId <= 7:
            if category_colors[label.categoryId] == (0, 0, 0):  # Not set yet
                category_colors[label.categoryId] = label.color

    return category_colors


def get_class_names() -> List[str]:
    """
    Get list of class names for valid trainIds (0-18).

    Returns:
        List of class names corresponding to trainIds 0-18
    """
    class_names = [""] * 19  # Initialize with empty strings

    for label in labels:
        if 0 <= label.trainId <= 18:
            class_names[label.trainId] = label.name

    return class_names


def get_class_colors() -> List[tuple]:
    """
    Get list of class colors for valid trainIds (0-18).

    Returns:
        List of RGB color tuples corresponding to trainIds 0-18
    """
    class_colors = [(0, 0, 0)] * 19  # Initialize with black

    for label in labels:
        if -1 <= label.trainId <= 18:
            class_colors[label.trainId] = label.color

    return class_colors


# Constants for easy access
LABEL_ID_TO_TRAIN_ID = create_id_to_trainid_mapping()
LABEL_ID_TO_CATEGORY_ID = create_id_to_categoryid_mapping()
TRAIN_ID_TO_CATEGORY_ID = create_trainid_to_categoryid_mapping()
VALID_TRAIN_IDS = get_valid_train_ids()
VALID_CATEGORY_IDS = get_valid_category_ids()
CLASS_NAMES = get_class_names()
CLASS_COLORS = get_class_colors()
CATEGORY_NAMES = get_category_names()
CATEGORY_COLORS = get_category_colors()
IGNORE_LABEL = 255
VOID_CATEGORY = 0
NUM_CLASSES = 19  # Valid training classes (0-18)
NUM_CATEGORIES = 8  # Valid categories (0-7, but 0 is void)

if __name__ == "__main__":
    # Example usage and validation
    print("Cityscapes Label Mapping")
    print("=" * 50)
    print(f"Number of valid training classes: {NUM_CLASSES}")
    print(f"Number of valid categories: {NUM_CATEGORIES}")
    print(f"Valid train IDs: {VALID_TRAIN_IDS}")
    print(f"Valid category IDs: {VALID_CATEGORY_IDS}")
    print(f"Ignore label value: {IGNORE_LABEL}")
    print(f"Void category value: {VOID_CATEGORY}")
    print()

    print("Label mapping (labelId -> trainId):")
    print("-" * 40)
    for label_id, train_id in sorted(LABEL_ID_TO_TRAIN_ID.items()):
        label_name = id2label[label_id].name
        print(f"{label_id:3d} ({label_name:20s}) -> {train_id:3d}")

    print()
    print("Label mapping (labelId -> categoryId):")
    print("-" * 40)
    for label_id, category_id in sorted(LABEL_ID_TO_CATEGORY_ID.items()):
        label_name = id2label[label_id].name
        print(f"{label_id:3d} ({label_name:20s}) -> {category_id:3d}")

    print()
    print("Class names for training (trainId -> name):")
    print("-" * 45)
    for i, name in enumerate(CLASS_NAMES):
        print(f"{i:2d}: {name}")

    print()
    print("Category names for training (categoryId -> name):")
    print("-" * 45)
    for i, name in enumerate(CATEGORY_NAMES):
        print(f"{i:2d}: {name}")
