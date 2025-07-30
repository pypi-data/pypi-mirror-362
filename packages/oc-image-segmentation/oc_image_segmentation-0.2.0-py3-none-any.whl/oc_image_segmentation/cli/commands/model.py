"""
Model commands for the CLI.
"""

import logging
from typing import Optional

import numpy as np
from PIL import Image

from ...models import (
    create_deeplabv3plus_from_config,
    create_unet_from_config,
    evaluate_model_miou,
    get_model_summary,
    predict_with_miou,
    train_deeplabv3plus_model,
    train_unet_model,
)
from ...utils import handle_exceptions

# Configure logging
logger = logging.getLogger(__name__)


def create_model(model_name: str = "unet", show_summary: bool = True):
    """
    Create a model from configuration.

    Args:
        model_name: Name of the model to create
        show_summary: Whether to show model summary
    """
    logger.info(f"Creating model: {model_name}")

    try:
        if model_name in ["unet", "unet_attention"]:
            # Create U-Net model
            _ = create_unet_from_config(model_name)

            if show_summary:
                logger.info("Model architecture:")
                summary = get_model_summary(model_name)
                for line in summary.split("\n"):
                    logger.info(line)

            logger.info(f"Model '{model_name}' created successfully!")
            return True
        elif model_name in [
            "deeplabv3plus",
            "deeplabv3plus_resnet101",
            "deeplabv3plus_efficientnet",
        ]:
            # Create DeepLabV3+ model
            _ = create_deeplabv3plus_from_config(model_name)

            if show_summary:
                logger.info("Model architecture:")
                summary = get_model_summary(model_name)
                for line in summary.split("\n"):
                    logger.info(line)

            logger.info(f"Model '{model_name}' created successfully!")
            return True
        else:
            logger.error(f"Model creation not implemented for: {model_name}")
            logger.info(
                "Available models for creation: unet, unet_attention, deeplabv3plus, deeplabv3plus_resnet101, deeplabv3plus_efficientnet"
            )
            return False

    except ImportError as e:
        logger.error(f"Failed to import model dependencies: {e}")
        logger.info("Make sure TensorFlow is installed: pip install tensorflow")
        return False
    except Exception as e:
        logger.error(f"Error creating model: {e}")
        return False


@handle_exceptions(default_return=False, log_message="Model training failed")
def train_model(
    model_name: str,
    dataset_path: str,
    is_fine_tuning: bool = False,
    plot_history: bool = False,
    resume_from: str = None,
    save_path: str = None,
    epochs: Optional[int] = None,
):
    """
    Train a model with the specified dataset.

    Args:
        model_name: Name of the model to train
        dataset_path: Path to the dataset root directory
        epochs: Number of training epochs
        save_path: Path to save the trained model
        resume_from: Path to weights to resume training from
    """
    logger.info(f"Training model: {model_name}")
    logger.info(f"Dataset path: {dataset_path}")
    logger.info(f"Epochs: {epochs}")

    try:
        if model_name in ["unet", "unet_attention"]:
            # Train U-Net model
            success = train_unet_model(
                model_name=model_name,
                dataset_path=dataset_path,
                epochs=epochs,
                is_fine_tuning=is_fine_tuning,
                plot_history=plot_history,
                resume_from=resume_from,
                save_path=save_path,
            )

            if success:
                logger.info(f"Model '{model_name}' trained successfully!")
                return True
            else:
                logger.error(f"Training failed for model '{model_name}'")
                return False
        elif model_name in [
            "deeplabv3plus",
            "deeplabv3plus_resnet101",
            "deeplabv3plus_efficientnet",
        ]:
            # Train DeepLabV3+ model
            success = train_deeplabv3plus_model(
                model_name=model_name,
                dataset_path=dataset_path,
                epochs=epochs,
                is_fine_tuning=is_fine_tuning,
                plot_history=plot_history,
                save_path=save_path,
                resume_from=resume_from,
            )

            if success:
                logger.info(f"Model '{model_name}' trained successfully!")
                return True
            else:
                logger.error(f"Training failed for model '{model_name}'")
                return False
        else:
            logger.error(f"Training not implemented for model: {model_name}")
            logger.info(
                "Available models for training: unet, unet_attention, deeplabv3plus, deeplabv3plus_resnet101, deeplabv3plus_efficientnet"
            )
            return False

    except ImportError as e:
        logger.error(f"Failed to import training dependencies: {e}")
        logger.info("Make sure TensorFlow is installed: pip install tensorflow")
        return False
    except NameError as e:
        logger.error(f"Error training model: {e}")
        return False


def evaluate_model(
    model_name: str,
    dataset_path: str,
    model_path: str = None,
    split: str = "val",
):
    """
    Evaluate a trained model and compute mIoU metrics.

    Args:
        model_name: Name of the model to evaluate
        dataset_path: Path to the dataset root directory
        model_path: Path to the trained model
        split: Dataset split to evaluate on
    """
    logger.info(f"Evaluating model: {model_name}")
    logger.info(f"Dataset path: {dataset_path}")
    logger.info(f"Split: {split}")

    try:
        if model_name in [
            "unet",
            "unet_attention",
            "deeplabv3plus",
            "deeplabv3plus_resnet101",
            "deeplabv3plus_efficientnet",
        ]:
            # Evaluate model (works for both U-Net and DeepLabV3+)
            results = evaluate_model_miou(
                model_name,
                dataset_path,
                model_path=model_path,
                split=split,
            )

            if results:
                logger.info(f"Model '{model_name}' evaluated successfully!")
                logger.info(f"Mean IoU: {results}")
                return True
            else:
                logger.error(f"Evaluation failed for model '{model_name}'")
                return False
        else:
            logger.error(f"Evaluation not implemented for model: {model_name}")
            logger.info(
                "Available models for evaluation: unet, unet_attention, deeplabv3plus, deeplabv3plus_resnet101, deeplabv3plus_efficientnet"
            )
            return False

    except ImportError as e:
        logger.error(f"Failed to import evaluation dependencies: {e}")
        logger.info("Make sure TensorFlow is installed: pip install tensorflow")
        return False
    except Exception as e:
        logger.error(f"Error evaluating model: {e}")
        return False


def predict_image(
    model_name: str,
    image_path: str,
    output_path: str = None,
    model_path: str = None,
    ground_truth_path: str = None,
):
    """
    Make prediction on a single image with optional mIoU computation.

    Args:
        model_name: Name of the model to use
        image_path: Path to the input image
        output_path: Path to save the prediction
        model_path: Path to the trained model
        ground_truth_path: Path to ground truth for mIoU computation
    """
    logger.info(f"Making prediction with model: {model_name}")
    logger.info(f"Image: {image_path}")

    try:
        if model_name in [
            "unet",
            "unet_attention",
            "deeplabv3plus",
            "deeplabv3plus_resnet101",
            "deeplabv3plus_efficientnet",
        ]:
            # Make prediction (works for both U-Net and DeepLabV3+)
            results = predict_with_miou(
                model_name=model_name,
                image_path=image_path,
                ground_truth_path=ground_truth_path,
                model_path=model_path,
            )

            if results:
                logger.info("Prediction completed successfully!")

                # Save prediction if output path provided
                if output_path:
                    predicted_mask = results["predicted_mask"]
                    # Convert to 8-bit image for saving
                    mask_image = Image.fromarray(
                        (predicted_mask * 255 / predicted_mask.max()).astype(np.uint8)
                    )
                    mask_image.save(output_path)
                    logger.info(f"Prediction saved to: {output_path}")

                # Log mIoU if computed
                if "mean_iou" in results:
                    logger.info(f"Mean IoU: {results['mean_iou']:.4f}")

                return True
            else:
                logger.error(f"Prediction failed for model '{model_name}'")
                return False
        else:
            logger.error(f"Prediction not implemented for model: {model_name}")
            logger.info(
                "Available models for prediction: unet, unet_attention, deeplabv3plus, deeplabv3plus_resnet101, deeplabv3plus_efficientnet"
            )
            return False

    except ImportError as e:
        logger.error(f"Failed to import prediction dependencies: {e}")
        logger.info(
            "Make sure TensorFlow and PIL are installed: pip install tensorflow pillow"
        )
        return False
    except Exception as e:
        logger.error(f"Error making prediction: {e}")
        return False
