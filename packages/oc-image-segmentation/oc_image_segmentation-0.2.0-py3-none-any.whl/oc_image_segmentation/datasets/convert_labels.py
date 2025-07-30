"""
Command for converting label images between different label modes.

This module provides functionality to convert label images from one format to another,
such as from 19-class trainId format to 8-class categoryId format.
"""

import logging
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image

try:
    from cityscapesscripts.helpers.labels import id2label, labels, trainId2label
except ImportError:
    labels = None
    id2label = None
    trainId2label = None

from .cityscapes_labels import (
    convert_labelids_to_categoryids,
    convert_labelids_to_trainids,
    convert_trainids_to_categoryids,
)

logger = logging.getLogger(__name__)


def convert_image_labels(
    input_image: Image,
    from_format: str = "labelId",
    to_format: str = "categoryId",
    verbose: bool = True,
) -> Image:
    label_array = np.array(input_image)

    if verbose:
        logger.info(f"Original image shape: {label_array.shape}")
        unique_original = np.unique(label_array)
        logger.info(f"Original unique labels: {unique_original}")

        # Display detailed label information with colors
        _display_labels_info(unique_original, from_format, verbose)

    # Convert based on formats
    if from_format == "labelId" and to_format == "trainId":
        converted_array = convert_labelids_to_trainids(label_array)
    elif from_format == "labelId" and to_format == "categoryId":
        converted_array = convert_labelids_to_categoryids(label_array)
    elif from_format == "trainId" and to_format == "categoryId":
        converted_array = convert_trainids_to_categoryids(label_array)
    elif from_format == to_format:
        logger.warning("Source and target formats are the same, copying file")
        converted_array = label_array
    else:
        logger.error(f"Unsupported conversion: {from_format} -> {to_format}")
        return False

    if verbose:
        logger.info(f"Converted image shape: {converted_array.shape}")
        unique_converted = np.unique(converted_array)
        logger.info(f"Converted unique labels: {unique_converted}")

        # Display detailed information about converted labels
        _display_labels_info(unique_converted, to_format, verbose)

    # Save the converted image
    # Convert to uint8 for proper saving, handling ignore values
    if to_format == "trainId":
        # trainId uses 255 for ignore, keep as is
        converted_image = Image.fromarray(converted_array.astype(np.uint8))
    elif to_format == "categoryId":
        # categoryId uses 0-7, convert to uint8
        converted_image = Image.fromarray(converted_array.astype(np.uint8))
    else:
        converted_image = Image.fromarray(converted_array.astype(np.uint8))

    return converted_image


def convert_labels(
    input_path: str,
    output_path: str,
    from_format: str = "labelId",
    to_format: str = "categoryId",
    verbose: bool = True,
    create_colored: bool = False,
) -> bool:
    """
    Convert label images between different label formats.

    Args:
        input_path: Path to input label image
        output_path: Path to save converted label image
        from_format: Source format ('trainId', 'categoryId', 'labelId')
        to_format: Target format ('trainId', 'categoryId')
        verbose: Whether to print conversion information
        create_colored: Whether to create colored visualization

    Returns:
        True if conversion successful, False otherwise
    """
    try:
        if verbose:
            logger.info(f"Converting labels from {from_format} to {to_format}")
            logger.info(f"Input: {input_path}")
            logger.info(f"Output: {output_path}")

        # Load the label image
        input_image = Image.open(input_path)

        converted_image = convert_image_labels(
            input_image,
            from_format,
            to_format,
            verbose=verbose,
        )

        # Create output directory if it doesn't exist
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)

        converted_image.save(output_path)

        # Create colored visualization if requested
        if create_colored:
            # Create colored version of the converted image
            converted_array = np.array(converted_image)
            colored_image = create_colored_label_image(converted_array, to_format)

            # Save colored image with _color suffix
            output_path_obj = Path(output_path)
            if "_labelIds.png" in output_path:
                colored_output_path = output_path.replace("_labelIds.png", "_color.png")
            elif "_trainIds.png" in output_path:
                colored_output_path = output_path.replace("_trainIds.png", "_color.png")
            elif "_categoryIds.png" in output_path:
                colored_output_path = output_path.replace(
                    "_categoryIds.png", "_color.png"
                )
            else:
                # Pour les noms génériques, ajouter _color avant l'extension
                colored_output_path = (
                    str(output_path_obj.with_suffix(""))
                    + "_color"
                    + output_path_obj.suffix
                )
            colored_image.save(colored_output_path)

            if verbose:
                logger.info(f"Colored visualization saved: {colored_output_path}")

        if verbose:
            logger.info(f"Conversion completed successfully: {output_path}")

        return True

    except Exception as e:
        logger.error(f"Failed to convert labels: {e}")
        return False


def convert_labels_batch(
    input_dir: str,
    output_dir: str,
    from_format: str = "labelId",
    to_format: str = "categoryId",
    pattern: str = "*.png",
    verbose: bool = True,
    preserve_structure: bool = True,
    create_colored: bool = False,
) -> bool:
    """
    Convert multiple label images in a directory, preserving Cityscapes structure.

    Args:
        input_dir: Directory containing input label images
        output_dir: Directory to save converted images
        from_format: Source format ('trainId', 'categoryId', 'labelId')
        to_format: Target format ('trainId', 'categoryId')
        pattern: File pattern to match (default: "*.png")
        verbose: Whether to print conversion information
        preserve_structure: Whether to preserve the directory structure (default: True)
        create_colored: Whether to create colored visualizations

    Returns:
        True if all conversions successful, False if any failed
    """
    try:
        input_path = Path(input_dir)
        output_path = Path(output_dir)

        if not input_path.exists():
            logger.error(f"Input directory does not exist: {input_dir}")
            return False

        # Find all matching files recursively
        label_files = list(input_path.rglob(pattern))

        if not label_files:
            logger.warning(
                f"No files found matching pattern '{pattern}' in {input_dir}"
            )
            return False

        # Filter for specific label types if format is specified
        if from_format in ["labelId", "trainId", "categoryId"]:
            filtered_files = []
            for file in label_files:
                if from_format == "labelId" and "_labelIds" in file.name:
                    filtered_files.append(file)
                elif from_format == "trainId" and "_trainIds" in file.name:
                    filtered_files.append(file)
                elif from_format == "categoryId" and "_categoryIds" in file.name:
                    filtered_files.append(file)
                elif from_format in file.name or "_gtFine_" not in file.name:
                    # Include files that don't follow Cityscapes naming or contain the format
                    filtered_files.append(file)

            if filtered_files:
                label_files = filtered_files

        if verbose:
            logger.info(f"Found {len(label_files)} files to convert")
            logger.info(f"Converting from {from_format} to {to_format}")
            if preserve_structure:
                logger.info("Preserving directory structure")

        # Convert each file
        success_count = 0
        for label_file in label_files:
            if preserve_structure:
                # Preserve the relative directory structure
                relative_path = label_file.relative_to(input_path)
                output_file = output_path / relative_path

                # Update filename for target format if it's a Cityscapes file
                if "_gtFine_" in output_file.name:
                    # Replace the format suffix in the filename
                    old_suffix_map = {
                        "labelId": "_labelIds",
                        "trainId": "_trainIds",
                        "categoryId": "_categoryIds",
                    }
                    new_suffix = old_suffix_map.get(to_format, f"_{to_format}")

                    new_name = output_file.name
                    for format_name, suffix in old_suffix_map.items():
                        if suffix in new_name:
                            new_name = new_name.replace(suffix, new_suffix)
                            break

                    output_file = output_file.parent / new_name
            else:
                output_file = output_path / label_file.name

            # Create output directory if it doesn't exist
            output_file.parent.mkdir(parents=True, exist_ok=True)

            if verbose:
                print(
                    f"Converting: {relative_path if preserve_structure else label_file.name}"
                )

            success = convert_labels(
                str(label_file),
                str(output_file),
                from_format=from_format,
                to_format=to_format,
                verbose=False,  # Reduce verbosity for batch processing
                create_colored=create_colored,
            )

            if success:
                success_count += 1
            else:
                logger.error(f"Failed to convert: {label_file.name}")

        if verbose:
            logger.info(
                f"Conversion completed: {success_count}/{len(label_files)} files successful"
            )

        return success_count == len(label_files)

    except Exception as e:
        logger.error(f"Failed to convert labels batch: {e}")
        return False


def show_label_info(label_path: str) -> bool:
    """
    Show information about a label image.

    Args:
        label_path: Path to the label image

    Returns:
        True if successful, False otherwise
    """
    try:
        logger.info(f"Analyzing label image: {label_path}")

        # Load the image
        image = Image.open(label_path)
        label_array = np.array(image)

        # Basic info
        logger.info(f"Image shape: {label_array.shape}")
        logger.info(f"Image dtype: {label_array.dtype}")

        # Unique values
        unique_values = np.unique(label_array)
        logger.info(f"Number of unique label values: {len(unique_values)}")
        logger.info(f"Label value range: {unique_values.min()} - {unique_values.max()}")
        logger.info(f"Unique values: {unique_values}")

        # Try to guess the format
        if len(unique_values) <= 8 and unique_values.max() <= 7:
            logger.info("→ Likely format: categoryId (8 classes, 0-7)")
        elif len(unique_values) <= 20 and unique_values.max() <= 18:
            logger.info("→ Likely format: trainId (19 classes, 0-18)")
        elif 255 in unique_values:
            logger.info(
                "→ Contains ignore label (255), likely trainId or labelId format"
            )
        elif unique_values.max() > 20:
            logger.info("→ Likely format: labelId (original Cityscapes, 0-33)")
        else:
            logger.info("→ Format unclear, manual inspection recommended")

        return True

    except Exception as e:
        logger.error(f"Failed to analyze label image: {e}")
        return False


def convert_labels_color(
    input_path: str,
    output_path: str,
    from_format: str = "labelId",
    verbose: bool = True,
) -> bool:
    """
    Convert label images to color images using official Cityscapes colors.

    Args:
        input_path: Path to input label image
        output_path: Path to save colorized image
        from_format: Source format ('trainId', 'categoryId', 'labelId')
        verbose: Whether to print conversion information

    Returns:
        True if conversion successful, False otherwise
    """
    try:
        if verbose:
            logger.info(f"Colorizing labels from {from_format}")
            logger.info(f"Input: {input_path}")
            logger.info(f"Output: {output_path}")

        # Load the label image
        input_image = Image.open(input_path)

        label_array = np.array(input_image)

        # Create RGB image
        height, width = label_array.shape
        colored_image = np.zeros((height, width, 3), dtype=np.uint8)

        # Get unique labels
        unique_labels = np.unique(label_array)

        # Color each label with its official color
        for label_value in unique_labels:
            mask = label_array == label_value
            info = _get_label_info(int(label_value), from_format)
            colored_image[mask] = info["color"]

        converted_image = Image.fromarray(colored_image)

        # Create output directory if it doesn't exist
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)

        converted_image.save(output_path)

        if verbose:
            logger.info(f"Colorization completed successfully: {output_path}")

        return True

    except Exception as e:
        logger.error(f"Failed to colorize labels: {e}")
        return False


def create_colored_label_image(
    label_array: np.ndarray,
    format_type: str = "labelId",
    raw: bool = False,
) -> Any:
    """
    Create a colored version of the label image using official Cityscapes colors.

    Args:
        label_array: Label array with integer values
        format_type: The format type ('labelId', 'trainId', 'categoryId')

    Returns:
        RGB colored PIL Image
    """
    # Create RGB image
    height, width = label_array.shape
    colored_image = np.zeros((height, width, 3), dtype=np.uint8)

    # Get unique labels
    unique_labels = np.unique(label_array)

    # Color each label with its official color
    for label_value in unique_labels:
        mask = label_array == label_value
        info = _get_label_info(int(label_value), format_type)
        colored_image[mask] = info["color"]

    return colored_image if raw else Image.fromarray(colored_image)


def _get_label_info(label_value: int, format_type: str) -> dict:
    """
    Get label information including color from cityscapesscripts.

    Args:
        label_value: The label value
        format_type: The format type ('labelId', 'trainId', 'categoryId')

    Returns:
        Dictionary with label information
    """
    if labels is None:
        return {
            "name": f"label_{label_value}",
            "color": (128, 128, 128),
            "category": "unknown",
        }

    try:
        if format_type == "labelId" and label_value in id2label:
            label = id2label[label_value]
            return {
                "name": label.name,
                "color": label.color,
                "category": label.category,
                "categoryId": label.categoryId,
            }
        elif format_type == "trainId" and label_value in trainId2label:
            label = trainId2label[label_value]
            return {
                "name": label.name,
                "color": label.color,
                "category": label.category,
                "categoryId": label.categoryId,
            }
        elif format_type == "categoryId":
            # Find first label with this categoryId
            for label in labels:
                if label.categoryId == label_value:
                    return {
                        "name": label.category,
                        "color": label.color,
                        "category": label.category,
                        "categoryId": label.categoryId,
                    }

        # Fallback for special values
        if label_value == 255:
            return {"name": "ignore", "color": (0, 0, 0), "category": "void"}

        return {
            "name": f"unknown_{label_value}",
            "color": (128, 128, 128),
            "category": "unknown",
        }

    except Exception:
        return {
            "name": f"label_{label_value}",
            "color": (128, 128, 128),
            "category": "unknown",
        }


def _display_labels_info(
    unique_labels: np.ndarray, format_type: str, verbose: bool = True
):
    """
    Display information about labels including their colors.

    Args:
        unique_labels: Array of unique label values
        format_type: The format type ('labelId', 'trainId', 'categoryId')
        verbose: Whether to display detailed information
    """
    if not verbose or len(unique_labels) == 0:
        return

    logger.info(f"Found {len(unique_labels)} unique labels in {format_type} format:")

    # Limit to first 10 labels to avoid cluttering
    display_labels = unique_labels[:10] if len(unique_labels) > 10 else unique_labels

    for label_value in display_labels:
        if label_value == 255:  # Skip ignore label details
            continue

        info = _get_label_info(int(label_value), format_type)
        color_str = f"RGB{info['color']}"
        logger.info(
            f"  {label_value:3d}: {info['name']:20s} | {info['category']:15s} | {color_str}"
        )

    if len(unique_labels) > 10:
        logger.info(f"  ... and {len(unique_labels) - 10} more labels")

    if 255 in unique_labels:
        logger.info(f"  255: {'ignore':20s} | {'void':15s} | RGB(0, 0, 0)")
