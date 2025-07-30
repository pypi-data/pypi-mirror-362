"""
Argument parser configuration for the CLI.
"""

import argparse

from ... import __version__


def create_parser():
    """Create and return the argument parser."""
    parser = argparse.ArgumentParser(
        description="OC Image Segmentation - Segment images using deep learning models",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Version argument
    parser.add_argument(
        "--version", action="version", version=f"oc-image-segmentation {__version__}"
    )

    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Segment command (default behavior)
    segment_parser = subparsers.add_parser("segment", help="Segment an image")
    segment_parser.add_argument("input", help="Path to the input image file")
    segment_parser.add_argument(
        "-o", "--output", required=True, help="Path to save the segmented image"
    )
    segment_parser.add_argument(
        "-m",
        "--model",
        default="default",
        choices=[
            "default",
            "unet",
            "unet_attention",
            "deeplabv3plus",
            "deeplabv3plus_resnet101",
            "deeplabv3plus_efficientnet",
        ],
        help="Model to use for segmentation (default: default)",
    )
    segment_parser.add_argument(
        "--model-path", help="Path to custom trained model weights"
    )
    segment_parser.add_argument(
        "--no-overlay", action="store_true", help="Don't create colored overlay image"
    )
    segment_parser.add_argument(
        "--confidence-threshold",
        type=float,
        default=0.5,
        help="Confidence threshold for binary segmentation (default: 0.5)",
    )

    # Dataset command
    dataset_parser = subparsers.add_parser("dataset", help="Dataset operations")
    dataset_subparsers = dataset_parser.add_subparsers(
        dest="dataset_command", help="Dataset commands"
    )

    # Load dataset subcommand
    load_dataset_parser = dataset_subparsers.add_parser(
        "load", help="Load and explore a dataset"
    )
    load_dataset_parser.add_argument("path", help="Path to the dataset directory")
    load_dataset_parser.add_argument(
        "--split",
        choices=["train", "val", "test"],
        help="Dataset split to load (default: config default)",
    )
    load_dataset_parser.add_argument(
        "--batch-size",
        type=int,
        help="Batch size for dataset iteration (default: config default)",
    )
    load_dataset_parser.add_argument(
        "--show-augmentation",
        action="store_true",
        help="Display sample images with augmentation applied (requires matplotlib)",
    )

    # Create all datasets subcommand
    create_all_parser = dataset_subparsers.add_parser(
        "create-all", help="Create all dataset splits"
    )
    create_all_parser.add_argument("path", help="Path to the dataset directory")
    create_all_parser.add_argument(
        "--batch-size",
        type=int,
        help="Batch size for all datasets (default: config default)",
    )

    # Config command
    subparsers.add_parser("config", help="Show current configuration")

    # Model command
    model_parser = subparsers.add_parser("model", help="Model operations")
    model_subparsers = model_parser.add_subparsers(
        dest="model_command", help="Model commands"
    )

    # Create model subcommand
    create_model_parser = model_subparsers.add_parser(
        "create", help="Create a new model"
    )
    create_model_parser.add_argument(
        "name",
        choices=[
            "unet",
            "unet_attention",
            "deeplabv3plus",
            "deeplabv3plus_resnet101",
            "deeplabv3plus_efficientnet",
        ],
        help="Type of model to create",
    )
    create_model_parser.add_argument(
        "--no-summary", action="store_true", help="Don't print model summary"
    )

    # Train model subcommand
    train_model_parser = model_subparsers.add_parser("train", help="Train a model")
    train_model_parser.add_argument(
        "model_name",
        choices=[
            "unet",
            "unet_attention",
            "deeplabv3plus",
            "deeplabv3plus_resnet101",
            "deeplabv3plus_efficientnet",
        ],
        help="Type of model to train",
    )
    train_model_parser.add_argument(
        "dataset_path", help="Path to the dataset directory"
    )
    train_model_parser.add_argument(
        "--epochs", type=int, default=10, help="Number of training epochs (default: 10)"
    )
    train_model_parser.add_argument(
        "--output-dir",
        default="./models/saved_model.weights.h5",
        help="Directory to save the trained model (default: ./models/saved_model.weights.h5)",
    )
    train_model_parser.add_argument(
        "--resume-from", help="Path to weights to resume training from"
    )

    # Evaluate model subcommand
    eval_model_parser = model_subparsers.add_parser("eval", help="Evaluate a model")
    eval_model_parser.add_argument(
        "model_name",
        choices=[
            "unet",
            "unet_attention",
            "deeplabv3plus",
            "deeplabv3plus_resnet101",
            "deeplabv3plus_efficientnet",
        ],
        help="Type of model to evaluate",
    )
    eval_model_parser.add_argument("dataset_path", help="Path to the dataset directory")
    eval_model_parser.add_argument(
        "--model-path", required=True, help="Path to the trained model to evaluate"
    )
    eval_model_parser.add_argument(
        "--split",
        choices=["train", "val", "test"],
        default="val",
        help="Dataset split to evaluate on (default: val)",
    )

    # Predict model subcommand
    predict_model_parser = model_subparsers.add_parser(
        "predict", help="Make predictions with a model"
    )
    predict_model_parser.add_argument(
        "model_name",
        choices=[
            "unet",
            "unet_attention",
            "deeplabv3plus",
            "deeplabv3plus_resnet101",
            "deeplabv3plus_efficientnet",
        ],
        help="Type of model to use for prediction",
    )
    predict_model_parser.add_argument(
        "input_path", help="Path to the input image or directory"
    )
    predict_model_parser.add_argument(
        "output_path", help="Path to save the prediction results"
    )
    predict_model_parser.add_argument(
        "--model-path",
        required=True,
        help="Path to the trained model to use for prediction",
    )
    predict_model_parser.add_argument(
        "--ground-truth", help="Path to ground truth for mIoU computation"
    )

    # Convert labels command
    convert_labels_parser = subparsers.add_parser(
        "convert-labels", help="Convert label images between different formats"
    )
    convert_labels_parser.add_argument(
        "input", help="Path to input label image or directory"
    )
    convert_labels_parser.add_argument(
        "output", help="Path to save converted label image(s)"
    )
    convert_labels_parser.add_argument(
        "--from-format",
        choices=["labelId", "trainId", "categoryId"],
        default="labelId",
        help="Source label format (default: trainId)",
    )
    convert_labels_parser.add_argument(
        "--to-format",
        choices=["labelId", "trainId", "categoryId"],
        default="categoryId",
        help="Target label format (default: categoryId)",
    )
    convert_labels_parser.add_argument(
        "--quiet", action="store_true", help="Suppress verbose output"
    )
    convert_labels_parser.add_argument(
        "--no-preserve-structure",
        action="store_true",
        help="Don't preserve directory structure (flatten output)",
    )
    convert_labels_parser.add_argument(
        "--pattern",
        default="*.png",
        help="File pattern to match for batch processing (default: *.png)",
    )
    convert_labels_parser.add_argument(
        "--create-colored",
        action="store_true",
        help="Also create colored visualization using official Cityscapes colors",
    )

    return parser
