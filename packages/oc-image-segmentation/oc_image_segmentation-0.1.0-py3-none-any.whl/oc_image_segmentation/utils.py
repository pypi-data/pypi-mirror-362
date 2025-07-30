"""
Utilities for error handling and debugging in OC Image Segmentation.
"""

import functools
import logging
import re
from typing import Any, Callable, TypeVar

import matplotlib.pyplot as plt

from .config import settings

logger = logging.getLogger(__name__)

# Type variable for decorator return types
F = TypeVar("F", bound=Callable[..., Any])


def is_debug_mode() -> bool:
    """
    Check if DEBUG mode is enabled in settings.

    Returns:
        bool: True if DEBUG mode is enabled, False otherwise
    """
    return getattr(settings, "DEBUG", False)


def handle_exceptions(
    default_return: Any = None,
    log_message: str = "Operation failed",
    reraise_on_debug: bool = True,
):
    """
    Decorator to handle exceptions with optional reraising in DEBUG mode.

    Args:
        default_return: Value to return when an exception is caught (not in DEBUG mode)
        log_message: Base message to log when an exception occurs
        reraise_on_debug: Whether to reraise exceptions when DEBUG=True

    Returns:
        Decorated function

    Example:
        @handle_exceptions(default_return=False, log_message="Training failed")
        def train_model():
            # Training code that might raise exceptions
            pass
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"{log_message}: {e}")

                if reraise_on_debug and is_debug_mode():
                    logger.debug("Reraising exception due to DEBUG=True")
                    raise

                logger.debug(f"Returning default value: {default_return}")
                return default_return

        return wrapper

    return decorator


def safe_execute(
    func: Callable,
    *args,
    default_return: Any = None,
    log_message: str = "Operation failed",
    reraise_on_debug: bool = True,
    **kwargs,
) -> Any:
    """
    Execute a function safely with exception handling.

    Args:
        func: Function to execute
        *args: Positional arguments for the function
        default_return: Value to return when an exception is caught
        log_message: Base message to log when an exception occurs
        reraise_on_debug: Whether to reraise exceptions when DEBUG=True
        **kwargs: Keyword arguments for the function

    Returns:
        Function result or default_return

    Example:
        result = safe_execute(
            some_risky_function,
            arg1, arg2,
            default_return={},
            log_message="Failed to process data",
            kwarg1=value1
        )
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error(f"{log_message}: {e}")

        if reraise_on_debug and is_debug_mode():
            logger.debug("Reraising exception due to DEBUG=True")
            raise

        logger.debug(f"Returning default value: {default_return}")
        return default_return


class DebugContext:
    """
    Context manager for temporary DEBUG mode changes.

    Example:
        with DebugContext(True):
            # Code that runs with DEBUG=True
            risky_operation()
    """

    def __init__(self, debug_mode: bool):
        self.debug_mode = debug_mode
        self.original_debug = None

    def __enter__(self):
        self.original_debug = getattr(settings, "DEBUG", False)
        settings.DEBUG = self.debug_mode
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        settings.DEBUG = self.original_debug


def log_and_handle_exception(
    exception: Exception,
    message: str = "Operation failed",
    default_return: Any = None,
    reraise_on_debug: bool = True,
) -> Any:
    """
    Log an exception and optionally reraise it in DEBUG mode.

    Args:
        exception: The exception that was caught
        message: Base message to log
        default_return: Value to return if not reraising
        reraise_on_debug: Whether to reraise in DEBUG mode

    Returns:
        default_return or raises exception

    Example:
        try:
            risky_operation()
        except Exception as e:
            return log_and_handle_exception(
                e,
                "Risky operation failed",
                default_return=False
            )
    """
    logger.error(f"{message}: {exception}")

    if reraise_on_debug and is_debug_mode():
        logger.debug("Reraising exception due to DEBUG=True")
        raise exception

    logger.debug(f"Returning default value: {default_return}")
    return default_return


def with_error_logging(
    log_level: int = logging.ERROR, message: str = "Operation failed"
):
    """
    Decorator to automatically log exceptions without handling them.

    Args:
        log_level: Logging level to use
        message: Base message to log

    Returns:
        Decorated function
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.log(log_level, f"{message} in {func.__name__}: {e}")
                raise

        return wrapper

    return decorator


def plot_history(history):
    """
    Plot training history metrics with support for per-class metrics.
    """

    hist = history.history

    # Regrouper les métriques globales
    global_metrics = set()
    per_class_groups = {}

    for key in hist.keys():
        # Exemple : val_per_class_dice_road
        per_class_match = re.match(r"(val|train)_per_class_(dice|iou)_(.+)", key)
        if per_class_match:
            split, metric_type, class_name = per_class_match.groups()
            group_key = f"{split}_per_class_{metric_type}"
            if group_key not in per_class_groups:
                per_class_groups[group_key] = {}
            per_class_groups[group_key][class_name] = hist[key]
        else:
            # exemple : accuracy, val_accuracy, dice_coefficient, etc.
            base_key = re.sub(r"^val_|^train_", "", key)
            global_metrics.add(base_key)

    # Plot global metrics
    for metric in sorted(global_metrics):
        plt.figure()
        has_data = False

        if metric in hist:
            plt.plot(hist[metric], label=metric)
            has_data = True

        for prefix in ["train_", "val_"]:
            full_key = prefix + metric
            if full_key in hist:
                plt.plot(hist[full_key], label=full_key)
                has_data = True

        if has_data:
            plt.title(metric)
            plt.xlabel("Epochs")
            plt.ylabel(metric)
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            plt.show()
        else:
            print(f"⚠️ Metric '{metric}' not found in history.")

    # Plot per-class metrics
    for group_key, class_curves in per_class_groups.items():
        plt.figure(figsize=(10, 6))
        for class_name, values in class_curves.items():
            plt.plot(values, label=class_name)
        metric_name = group_key.replace("_", " ").title()
        plt.title(metric_name)
        plt.xlabel("Epochs")
        plt.ylabel(group_key.split("_")[-2])  # "dice" or "iou"
        plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        plt.grid(True)
        plt.tight_layout()
        plt.show()
