"""
Segmentation commands for the CLI.
"""

import logging
from pathlib import Path

import numpy as np
from PIL import Image

from ...config import (
    get_logging_config,
    get_supported_formats,
    settings,
)
from ...datasets.convert_labels import create_colored_label_image
from ...models import load_model
from ...utils import handle_exceptions

# Configure logging
logging_config = get_logging_config()
logger = logging.getLogger(__name__)


@handle_exceptions(default_return=False, log_message="Image segmentation failed")
def segment_image(
    input_path: str,
    output_path: str,
    model: str = "default",
    model_path: str = None,
    model_instance: any = None,
    no_overlay: bool = False,
    confidence_threshold: float = 0.5,
):
    """
    Segment an image using the specified model.

    Args:
        input_path: Path to the input image
        output_path: Path to save the segmented image
        model: Model to use for segmentation (default: "default")
        model_path: Path to custom model weights
        no_overlay: Don't create colored overlay image
        confidence_threshold: Confidence threshold for binary segmentation
    """
    logger.info(f"Segmenting image: {input_path}")
    logger.info(f"Using model: {model}")
    logger.info(f"Output will be saved to: {output_path}")

    # Validate input file
    input_file = Path(input_path)
    if not input_file.exists():
        logger.error(f"Input file '{input_path}' does not exist.")
        return False

    # Validate file format
    supported_formats = get_supported_formats()
    if input_file.suffix.lower() not in supported_formats:
        logger.error(f"Unsupported file format: {input_file.suffix}")
        logger.info(f"Supported formats: {', '.join(supported_formats)}")
        return False

    # Create and load the model
    try:
        model_instance = model_instance or load_model(
            model=model, model_path=model_path
        )
    except Exception as e:
        logger.error(f"Error creating/loading model: {e}")
        return False

    # Load and preprocess the input image
    try:
        logger.info("Loading and preprocessing input image...")

        # Load image
        image = Image.open(input_path).convert("RGB")
        original_size = image.size
        logger.info(f"Original image size: {original_size}")

        # Get target input size from model config
        target_size = model_instance.input_size
        logger.info(f"Target input size: {target_size}")

        # Resize image to model input size
        image_resized = image.resize(target_size)

        # Convert to numpy array and normalize
        image_array = np.array(image_resized, dtype=np.float32) / 255.0

        # Add batch dimension
        image_batch = np.expand_dims(image_array, axis=0)

        logger.info(f"Preprocessed image shape: {image_batch.shape}")

    except Exception as e:
        logger.error(f"Error loading/preprocessing image: {e}")
        return False

    # Perform inference
    try:
        logger.info("Performing inference...")

        # Make prediction
        predictions = model_instance.model.predict(image_batch, verbose=0)
        logger.info(f"Prediction shape: {predictions.shape}")

        # Convert predictions to class indices
        if predictions.shape[-1] > 1:
            # Multi-class segmentation - take argmax
            predicted_mask = np.argmax(predictions[0], axis=-1)
        else:
            # Binary segmentation - use confidence threshold
            predicted_mask = (predictions[0, :, :, 0] > confidence_threshold).astype(
                np.uint8
            )

        logger.info(f"Predicted mask shape: {predicted_mask.shape}")
        logger.info(f"Unique classes predicted: {np.unique(predicted_mask)}")

    except Exception as e:
        logger.error(f"Error during inference: {e}")
        return False

    # Post-process and save the result
    try:
        logger.info("Post-processing and saving result...")

        # Create output directory if it doesn't exist
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Resize mask back to original image size
        mask_image = Image.fromarray(predicted_mask.astype(np.uint8))
        mask_resized = mask_image.resize(original_size, Image.NEAREST)

        # Convert to a better visualization format
        # Scale to 0-255 for better visibility
        mask_array = np.array(mask_resized)
        if mask_array.max() > 0:
            # Scale to full range for better visibility
            mask_scaled = (mask_array * 255 // mask_array.max()).astype(np.uint8)
        else:
            mask_scaled = mask_array.astype(np.uint8)

        # Save the segmentation mask
        result_image = Image.fromarray(mask_scaled, mode="L")
        result_image.save(output_path)

        # Create and save a colored overlay if requested
        if not no_overlay:
            overlay_path = output_path.replace(".png", "_overlay.png").replace(
                ".jpg", "_overlay.jpg"
            )
            mask_image_colored = create_colored_label_image(
                predicted_mask,
                settings.dataset.get("label_mode", "labelId"),
            )
            image_colored = mask_image_colored.resize(
                original_size,
                Image.NEAREST,
            )
            # Create colored overlay
            overlay_image = Image.blend(
                image.convert("RGBA"),
                image_colored.convert("RGBA"),
                alpha=0.5,
            )
            overlay_image.save(overlay_path)
            logger.info(f"Colored overlay saved to: {overlay_path}")

        logger.info(f"Segmentation mask saved to: {output_path}")
        logger.info(f"Mask size: {mask_resized.size}")
        logger.info(f"Classes found: {len(np.unique(mask_array))}")

    except Exception as e:
        logger.error(f"Error saving result: {e}")
        return False

    logger.info("Image segmentation completed successfully!")
    return True
