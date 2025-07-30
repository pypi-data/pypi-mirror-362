"""
CLI main entry point for oc-image-segmentation.
"""

import logging
import sys

from ..config import get_logging_config
from ..datasets.convert_labels import convert_labels_batch
from .commands import (
    create_all_datasets,
    create_model,
    evaluate_model,
    load_dataset,
    predict_image,
    segment_image,
    train_model,
)
from .parsers import create_parser

# Configure logging
logging_config = get_logging_config()
logging.basicConfig(
    level=getattr(logging, logging_config["level"]), format=logging_config["format"]
)
logger = logging.getLogger(__name__)


def main():
    """Main entry point for the CLI."""
    parser = create_parser()

    # Parse arguments
    args = parser.parse_args()

    # Handle no command (backward compatibility)
    if args.command is None:
        parser.print_help()
        return

    try:
        if args.command == "segment":
            success = segment_image(
                input_path=args.input,
                output_path=args.output,
                model=args.model,
                model_path=getattr(args, "model_path", None),
                no_overlay=getattr(args, "no_overlay", False),
                confidence_threshold=getattr(args, "confidence_threshold", 0.5),
            )
            if not success:
                sys.exit(1)

        elif args.command == "model":
            if args.model_command == "create":
                success = create_model(args.name, not args.no_summary)
                if not success:
                    sys.exit(1)
            elif args.model_command == "train":
                success = train_model(
                    model_name=args.model_name,
                    dataset_path=args.dataset_path,
                    epochs=args.epochs,
                    save_path=args.output_dir,
                    resume_from=getattr(args, "resume_from", None),
                )
                if not success:
                    sys.exit(1)
            elif args.model_command == "eval":
                success = evaluate_model(
                    model_name=args.model_name,
                    dataset_path=args.dataset_path,
                    model_path=args.model_path,
                    split=getattr(args, "split", "val"),
                )
                if not success:
                    sys.exit(1)
            elif args.model_command == "predict":
                success = predict_image(
                    model_name=args.model_name,
                    image_path=args.input_path,
                    output_path=args.output_path,
                    model_path=args.model_path,
                    ground_truth_path=getattr(args, "ground_truth", None),
                )
                if not success:
                    sys.exit(1)
            else:
                print("Available model commands: create, train, eval, predict")
                print(
                    "Use 'oc-image-segmentation model <command> -h' for specific help."
                )

        elif args.command == "dataset":
            if args.dataset_command == "load":
                success = load_dataset(
                    args.path,
                    split=getattr(args, "split", None),
                    show_augmentation=getattr(args, "show_augmentation", False),
                )
                if not success:
                    sys.exit(1)
            elif args.dataset_command == "create-all":
                success = create_all_datasets(
                    args.path, getattr(args, "batch_size", None)
                )
                if not success:
                    sys.exit(1)
            else:
                print("Available dataset commands: load, create-all")
                print(
                    "Use 'oc-image-segmentation dataset <command> -h' for specific help."
                )

        elif args.command == "convert-labels":
            # Check if input is a file or directory
            from pathlib import Path

            input_path = Path(args.input)

            if input_path.is_file():
                # Single file conversion
                from ..datasets.convert_labels import convert_labels

                success = convert_labels(
                    input_path=args.input,
                    output_path=args.output,
                    from_format=args.from_format,
                    to_format=args.to_format,
                    verbose=not args.quiet,
                    create_colored=getattr(args, "create_colored", False),
                )
            else:
                # Directory batch conversion
                success = convert_labels_batch(
                    input_dir=args.input,
                    output_dir=args.output,
                    from_format=args.from_format,
                    to_format=args.to_format,
                    pattern=getattr(args, "pattern", "*.png"),
                    verbose=not args.quiet,
                    preserve_structure=not getattr(
                        args, "no_preserve_structure", False
                    ),
                    create_colored=getattr(args, "create_colored", False),
                )

            if not success:
                sys.exit(1)

    except NameError as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
