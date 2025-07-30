import abc
import logging
from typing import List, Optional

from tensorflow import keras

from .metrics import (
    DiceCoefficient,
    PerClassDice,
    PerClassMeanIoU,
)

logger = logging.getLogger(__name__)


class BaseSegmentationModel(abc.ABC):
    """
    Abstract base class for segmentation models.
    """

    def __init__(self, num_classes: Optional[int] = 8):
        self.num_classes = num_classes
        self.model = None
        self._metrics = None

    @abc.abstractmethod
    def build_model(self):
        """Build the model architecture."""
        pass

    def compile_model(
        self,
        optimizer: str = "adam",
        learning_rate: float = 1e-4,
        loss: str = "sparse_categorical_crossentropy",
        metrics: Optional[List] = None,
        **kwargs,
    ):
        """
        Compile the model with optimizer, loss, and metrics.

        Parameters
        ----------
        optimizer : str
            Optimizer to use.
        learning_rate : float
            Learning rate.
        loss : str
            Loss function.
        metrics : list, optional
            List of metric names or metric objects.
        """
        metrics = metrics or []

        if "accuracy" not in metrics:
            metrics.append("accuracy")

        # Ajout automatique des métriques utiles
        metric_names = [m.name if hasattr(m, "name") else str(m) for m in metrics]

        if "per_class_iou" not in metric_names:
            metrics.append(PerClassMeanIoU(num_classes=self.num_classes))

        if "dice_coef" not in metric_names:
            metrics.append(DiceCoefficient(num_classes=self.num_classes))

        if "per_class_dice" not in metric_names:
            metrics.append(PerClassDice(num_classes=self.num_classes))

        if isinstance(optimizer, str):
            if optimizer.lower() == "adam":
                optimizer = keras.optimizers.Adam(learning_rate=learning_rate)
            elif optimizer.lower() == "sgd":
                optimizer = keras.optimizers.SGD(
                    learning_rate=learning_rate, momentum=0.9
                )
            else:
                raise ValueError(f"Unsupported optimizer: {optimizer}")

        if loss in [
            "focal",
            "sparse_categorical_crossentropy",
            "sparse_categorical_crossentropy_with_ignore",
            "weighted",
        ]:
            from .losses import get_cityscapes_loss

            loss_fn = get_cityscapes_loss(loss, **kwargs)
        else:
            loss_fn = loss

        self._metrics = metrics

        self.model.compile(
            optimizer=optimizer,
            loss=loss_fn,
            metrics=metrics,
        )

        logger.info(f"Model compiled with {optimizer.__class__.__name__}")
        logger.info(
            f"Loss: {loss}, Metrics: {[m.name if hasattr(m, 'name') else str(m) for m in metrics]}"
        )

    def summary(self):
        """Print model summary."""
        if self.model is None:
            raise ValueError("Model not built yet. Call build_model() first.")
        return self.model.summary()

    def save(self, filepath: str, save_optimizer: bool = False):
        """
        Save the model or weights.

        Parameters
        ----------
        filepath : str
            Path to save the model.
        save_optimizer : bool
            Whether to save the optimizer state.
        """
        if self.model is None:
            raise ValueError("Model not built yet. Call build_model() first.")

        if filepath.endswith(".weights.h5"):
            self.model.save_weights(filepath)
            logger.info(f"Model weights saved to {filepath}")
        else:
            self.model.save(filepath, include_optimizer=save_optimizer)
            logger.info(f"Model saved to {filepath}")

    def load_weights(self, filepath: str):
        """Load model weights from file."""
        if self.model is None:
            raise ValueError("Model not built yet. Call build_model() first.")
        self.model.load_weights(filepath)
        logger.info(f"Weights loaded from {filepath}")

    def predict(self, *args, **kwargs):
        return self.model.predict(*args, **kwargs)
