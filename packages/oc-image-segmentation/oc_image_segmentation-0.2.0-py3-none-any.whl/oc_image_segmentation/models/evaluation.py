"""
Evaluation functions for models.

This module contains functions for evaluating model performance.
"""

import logging
from typing import Any, Optional, Tuple

import numpy as np
import tensorflow as tf
from PIL import Image

from ..datasets.cityscapes_labels import categoryId2label, trainId2label
from ..datasets.convert_labels import convert_image_labels
from ..utils import handle_exceptions
from .factory import load_model

logger = logging.getLogger(__name__)

# Cityscapes class names for IoU analysis
CITYSCAPES_CLASSES = [
    "road",
    "sidewalk",
    "building",
    "wall",
    "fence",
    "pole",
    "traffic_light",
    "traffic_sign",
    "vegetation",
    "terrain",
    "sky",
    "person",
    "rider",
    "car",
    "truck",
    "bus",
    "train",
    "motorcycle",
    "bicycle",
]


@handle_exceptions(default_return=0.0, log_message="Model evaluation failed")
def evaluate_model_miou(
    model_name: str,
    dataset_path: str,
    model_path: str = None,
    split: str = "val",
) -> float:
    """
    Evaluate a model using mean IoU metric.

    Args:
        model_path: Path to the saved model
        dataset_path: Path to the dataset
        split: train, val or test (default: val)

    Returns:
        Mean IoU score
    """
    from ..datasets import create_cityscapes_datasets

    logger.info(f"Evaluating model: {model_path}")
    logger.info(f"Dataset: {dataset_path}")

    # Load model
    try:
        model = load_model(model_name, model_path=model_path)
        keras_model = model.model
        logger.info("Model loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        return 0.0

    # Load dataset
    train_dataset, val_dataset, test_dataset = create_cityscapes_datasets(
        dataset_root=dataset_path,
    )

    if split == "val":
        eval_dataset = val_dataset
    elif split == "train":
        eval_dataset = train_dataset
    elif split == "test":
        eval_dataset = test_dataset
    else:
        logger.error(f"Invalid split value '{split}'")
        return 0.0

    if eval_dataset is None:
        logger.error("No evaluation dataset available")
        return 0.0

    # Compile model with mIoU metric
    from .metrics import MeanIoU

    miou_metric = MeanIoU(num_classes=eval_dataset.num_classes)

    keras_model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=[miou_metric],
    )

    # Evaluate
    try:
        results = keras_model.evaluate(eval_dataset.create_tf_dataset(), verbose=1)

        # Extract mIoU score (usually the last metric)
        miou_score = results[-1] if isinstance(results, list) else results

        logger.info(f"Mean IoU: {miou_score:.4f}")
        return float(miou_score)

    except Exception as e:
        logger.error(f"Evaluation failed: {e}")
        return 0.0


@handle_exceptions(default_return=(None, 0.0), log_message="Prediction failed")
def predict_with_miou(
    model_path: str,
    image_path: str,
    output_path: str = None,
    model_name: str = "unet",
    **kwargs,
) -> Tuple[np.ndarray, float]:
    """
    Make a prediction and compute IoU if ground truth is available.

    Args:
        model_path: Path to the saved model
        image_path: Path to the input image
        output_path: Path to save the prediction
        model_name: Name of the model type
        **kwargs: Additional prediction arguments

    Returns:
        Tuple of (prediction_mask, miou_score)
    """
    logger.info(f"Making prediction with model: {model_path}")
    logger.info(f"Input image: {image_path}")

    # Load model
    try:
        model = tf.keras.models.load_model(model_path, compile=False)
        logger.info("Model loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        return None, 0.0

    # Load and preprocess image
    try:
        image = Image.open(image_path)
        image = image.convert("RGB")

        # Resize to model input size
        input_size = kwargs.get("input_size", (512, 512))
        image_resized = image.resize(input_size)

        # Convert to array and normalize
        image_array = np.array(image_resized) / 255.0
        image_batch = np.expand_dims(image_array, axis=0)

        logger.info(f"Image preprocessed: {image_batch.shape}")

    except Exception as e:
        logger.error(f"Failed to load image: {e}")
        return None, 0.0

    # Make prediction
    try:
        prediction = model.predict(image_batch, verbose=0)

        # Convert to class indices
        prediction_mask = np.argmax(prediction[0], axis=-1)

        logger.info("Prediction completed successfully")

        # Save prediction if output path provided
        if output_path:
            pred_image = Image.fromarray(prediction_mask.astype(np.uint8))
            pred_image.save(output_path)
            logger.info(f"Prediction saved to: {output_path}")

        # For now, return 0.0 for mIoU since we don't have ground truth
        # In a real implementation, this would compute IoU against ground truth
        return prediction_mask, 0.0

    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        return None, 0.0


@handle_exceptions(default_return=None, log_message="IoU scores calculation failed")
def get_iou_scores_df(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    class_names: list = None,
    num_classes: Optional[int] = 8,
):
    """
    Calculate IoU scores for each class and return as DataFrame.

    Args:
        y_true: Ground truth labels (flattened)
        y_pred: Predicted labels (flattened)
        num_classes: Number of classes (default: 8 for Cityscapes)
        class_names: List of class names (default: Cityscapes classes)

    Returns:
        DataFrame with IoU scores per class and mean IoU
    """
    try:
        from sklearn.metrics import confusion_matrix

        if num_classes == 8:
            class_names = [categoryId2label[i].category for i in range(num_classes)]
        else:
            class_names = [trainId2label[i].name for i in range(num_classes)]

        cm = confusion_matrix(
            y_true.flatten(),
            y_pred.flatten(),
            labels=list(range(num_classes)),
        )

        # Calculate IoU for each class
        intersection = np.diag(cm)
        predicted_set = cm.sum(axis=0)
        ground_truth_set = cm.sum(axis=1)
        union = ground_truth_set + predicted_set - intersection

        # Avoid division by zero
        iou_scores = intersection / np.maximum(union, 1)

        import pandas as pd

        # Create DataFrame
        df_iou = pd.DataFrame(
            {
                "Class": class_names[:num_classes],
                "IoU": iou_scores,
                "Intersection": intersection,
                "Union": union,
                "GT_Pixels": ground_truth_set,
                "Pred_Pixels": predicted_set,
            }
        )

        # Add mean IoU
        mean_iou = np.mean(
            iou_scores[union > 0]
        )  # Only consider classes present in data
        df_iou.loc[len(df_iou)] = {
            "Class": "Mean IoU",
            "IoU": mean_iou,
            "Intersection": np.sum(intersection),
            "Union": np.sum(union),
            "GT_Pixels": np.sum(ground_truth_set),
            "Pred_Pixels": np.sum(predicted_set),
        }

        logger.info(f"IoU scores calculated successfully. Mean IoU: {mean_iou:.4f}")
        return df_iou

    except Exception as e:
        logger.error(f"Failed to calculate IoU scores: {e}")
        return None


@handle_exceptions(
    default_return=(None, None), log_message="Prediction with IoU analysis failed"
)
def predict_with_iou_analysis(
    image_path: str,
    ground_label_mode: str = "labelId",
    ground_truth_path: str = None,
    input_size: Optional[Tuple[int, int]] = None,
    label_mode: Optional[str] = None,
    model_instance: any = None,
    model_name: str = "unet",
    model_path: str = None,
    output_path: str = None,
) -> Tuple[np.ndarray, object]:
    """
    Make a prediction and compute detailed IoU analysis if ground truth is available.

    Args:
        model_path: Path to the saved model
        image_path: Path to the input image
        ground_truth_path: Path to the ground truth mask (optional)
        output_path: Path to save the prediction
        model_name: Name of the model type
        num_classes: Number of classes

    Returns:
        Tuple of (prediction_mask, iou_dataframe)
    """

    from ..config import settings

    model_config = getattr(settings.models, model_name, None)

    if model_config is None:
        raise

    input_size = (
        input_size
        or (
            getattr(settings.dataset, "input_size", None)
            and tuple(settings.dataset.input_size)
        )
        or tuple(model_config.input_size)
    )
    label_mode = label_mode or settings.dataset.label_mode or "categoryId"

    if label_mode == "categoryId":
        num_classes = 8
    elif label_mode == "trainId":
        num_classes = 19

    logger.info(f"Making prediction with IoU analysis: {model_path}")
    logger.info(f"Input image: {image_path}")

    # Create and load the model
    try:
        model_instance = model_instance or load_model(
            model=model_name, model_path=model_path
        )
    except Exception as e:
        logger.error(f"Error creating/loading model: {e}")
        return False

    # Load and preprocess image
    try:
        image = Image.open(image_path)
        image = image.convert("RGB")

        # Resize to model input size
        image_resized = image.resize(input_size)

        # Convert to array and normalize
        image_array = np.array(image_resized) / 255.0
        image_batch = np.expand_dims(image_array, axis=0)

        logger.info(f"Image preprocessed: {image_batch.shape}")

    except Exception as e:
        logger.error(f"Failed to load image: {e}")
        return None, None

    # Make prediction
    try:
        prediction = model_instance.model.predict(image_batch, verbose=0)
        prediction_mask = np.argmax(prediction[0], axis=-1)

        logger.info("Prediction completed successfully")

        # Save prediction if output path provided
        if output_path:
            pred_image = Image.fromarray(prediction_mask.astype(np.uint8))
            pred_image.save(output_path)
            logger.info(f"Prediction saved to: {output_path}")

        # Calculate IoU if ground truth is available
        iou_df = None
        if ground_truth_path:
            try:
                # Load ground truth
                gt_image = Image.open(ground_truth_path)
                if ground_label_mode != label_mode:
                    gt_image = convert_image_labels(
                        gt_image,
                        from_format=ground_label_mode,
                        to_format=label_mode,
                        verbose=False,
                    )
                gt_image = gt_image.resize(input_size)
                gt_mask = np.array(gt_image)

                # Ensure ground truth is in the right format
                if len(gt_mask.shape) == 3:
                    gt_mask = gt_mask[:, :, 0]  # Take first channel if RGB

                # Calculate IoU scores
                iou_df = get_iou_scores_df(
                    y_true=gt_mask,
                    y_pred=prediction_mask,
                    num_classes=num_classes,
                )

                if iou_df is not None:
                    logger.info("IoU analysis completed")
                    logger.info(f"Mean IoU: {iou_df.iloc[-1]['IoU']:.4f}")
                else:
                    logger.warning("IoU analysis failed")

            except Exception as e:
                logger.error(f"Failed to compute IoU with ground truth: {e}")

        return prediction_mask, iou_df

    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        return None, None


def display_iou_results(iou_df: object, save_path: str = None) -> None:
    """
    Display IoU results in a formatted way and optionally save to file.

    Args:
        iou_df: DataFrame with IoU scores
        save_path: Optional path to save the results as CSV
    """
    if iou_df is None:
        logger.warning("No IoU DataFrame to display")
        return

    try:
        print("\n" + "=" * 60)
        print("IoU SCORES ANALYSIS")
        print("=" * 60)

        # Display class-wise IoU scores
        for idx, row in iou_df.iterrows():
            if row["Class"] == "Mean IoU":
                print("-" * 60)
                print(f"{row['Class']:20s}: {row['IoU']:.4f}")
            else:
                print(
                    f"{row['Class']:20s}: {row['IoU']:.4f} "
                    f"(GT: {int(row['GT_Pixels']):8d}, "
                    f"Pred: {int(row['Pred_Pixels']):8d})"
                )

        print("=" * 60)

        # Save to CSV if requested
        if save_path:
            iou_df.to_csv(save_path, index=False)
            logger.info(f"IoU results saved to: {save_path}")

    except Exception as e:
        logger.error(f"Failed to display IoU results: {e}")


def get_class_performance_summary(iou_df: object, threshold: float = 0.5) -> dict:
    """
    Get a summary of class performance based on IoU scores.

    Args:
        iou_df: DataFrame with IoU scores
        threshold: IoU threshold for good performance (default: 0.5)

    Returns:
        Dictionary with performance summary
    """
    if iou_df is None:
        return {}

    try:
        # Use the correct column names from the new DataFrame format
        class_scores = iou_df["IoU"].values
        class_names = iou_df["Class"].values

        good_classes = class_names[class_scores >= threshold]
        poor_classes = class_names[class_scores < threshold]

        summary = {
            "total_classes": len(class_scores),
            "good_classes": list(good_classes),
            "poor_classes": list(poor_classes),
            "good_count": len(good_classes),
            "poor_count": len(poor_classes),
            "best_class": class_names[np.argmax(class_scores)],
            "worst_class": class_names[np.argmin(class_scores)],
            "best_iou": float(np.max(class_scores)),
            "worst_iou": float(np.min(class_scores)),
            "mean_iou": float(np.mean(class_scores)),
        }

        return summary

    except Exception as e:
        logger.error(f"Failed to generate performance summary: {e}")
        return {}


@handle_exceptions(default_return=0.0, log_message="Mean IoU calculation failed")
def get_mean_iou(iou_df: Any, weighted: bool = False) -> float:
    """
    Calculate mean IoU from IoU DataFrame.

    Args:
        iou_df: DataFrame from get_iou_scores_df
        weighted: If True, weight by pixel count

    Returns:
        Mean IoU score
    """
    if len(iou_df) == 0:
        return 0.0

    if weighted:
        total_pixels = iou_df["GT_Pixels"].sum()
        if total_pixels == 0:
            return 0.0
        weighted_iou = (iou_df["IoU"] * iou_df["GT_Pixels"]).sum()
        return weighted_iou / total_pixels
    else:
        return iou_df["IoU"].mean()


@handle_exceptions(default_return=None, log_message="IoU summary printing failed")
def print_iou_summary(iou_df: Any, title: str = "IoU Summary") -> None:
    """
    Print a formatted summary of IoU scores.

    Args:
        iou_df: DataFrame from get_iou_scores_df
        title: Title for the summary
    """
    print(f"\n{title}")
    print("=" * len(title))

    if len(iou_df) == 0:
        print("No classes found.")
        return

    # Print per-class results
    print("\nPer-class IoU scores:")
    print("-" * 50)
    for _, row in iou_df.iterrows():
        print(
            f"{row['Class']:<20} | IoU: {row['IoU']:.4f} | Pixels: {row['GT_Pixels']:>8}"
        )

    # Print summary statistics
    mean_iou = get_mean_iou(iou_df, weighted=False)
    weighted_iou = get_mean_iou(iou_df, weighted=True)

    print("-" * 50)
    print(f"Mean IoU (unweighted): {mean_iou:.4f}")
    print(f"Mean IoU (weighted):   {weighted_iou:.4f}")
    print(f"Number of classes:     {len(iou_df)}")
    print(f"Total pixels:          {iou_df['GT_Pixels'].sum()}")
