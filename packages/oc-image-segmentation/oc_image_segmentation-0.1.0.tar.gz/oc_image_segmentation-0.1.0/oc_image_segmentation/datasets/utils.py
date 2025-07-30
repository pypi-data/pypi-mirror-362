"""
Utility functions for dataset handling.

This module contains utility functions for filename parsing, path handling,
and other dataset-related operations.
"""

from pathlib import Path


def parse_cityscapes_filename(filename: str) -> dict:
    """
    Parse a Cityscapes filename to extract metadata.

    Args:
        filename: Cityscapes filename (e.g., 'berlin_000543_000019_leftImg8bit.png')

    Returns:
        dict: Parsed metadata with keys: city, sequence, frame, suffix

    Example:
        >>> parse_cityscapes_filename('berlin_000543_000019_leftImg8bit.png')
        {'city': 'berlin', 'sequence': '000543', 'frame': '000019', 'suffix': 'leftImg8bit'}
    """
    parts = Path(filename).stem.split("_")
    if len(parts) >= 4:
        return {
            "city": parts[0],
            "sequence": parts[1],
            "frame": parts[2],
            "suffix": "_".join(parts[3:]),
        }
    else:
        raise ValueError(f"Invalid Cityscapes filename format: {filename}")


def get_matching_label_filename(
    image_filename: str, label_type: str = "labelIds"
) -> str:
    """
    Get the corresponding label filename for a Cityscapes image.

    Args:
        image_filename: Image filename (e.g., 'berlin_000543_000019_leftImg8bit.png')
        label_type: Type of label ('labelIds', 'instanceIds', 'polygons')

    Returns:
        str: Corresponding label filename

    Example:
        >>> get_matching_label_filename('berlin_000543_000019_leftImg8bit.png')
        'berlin_000543_000019_gtFine_labelIds.png'
    """
    parsed = parse_cityscapes_filename(image_filename)
    base_name = f"{parsed['city']}_{parsed['sequence']}_{parsed['frame']}"

    if label_type == "polygons":
        return f"{base_name}_gtFine_polygons.json"
    else:
        return f"{base_name}_gtFine_{label_type}.png"


def analyze_class_distribution(dataset, num_classes=8):
    import matplotlib.pyplot as plt
    import numpy as np

    class_counts = np.zeros(num_classes, dtype=int)

    for _, mask in dataset.take(100):  # analyser 100 images max
        labels = mask.numpy().flatten()
        for c in range(num_classes):
            class_counts[c] += np.sum(labels == c)

    plt.bar(range(num_classes), class_counts)
    plt.xlabel("Classe ID")
    plt.ylabel("Pixels")
    plt.title("Distribution des classes dans y_true")
    plt.show()

    for i, count in enumerate(class_counts):
        print(f"Classe {i}: {count} pixels")
