"""
Metrics for model evaluation.

This module contains custom metrics for evaluating segmentation models.
"""

import tensorflow as tf
from tensorflow import keras


class MeanIoU(keras.metrics.Metric):
    """
    Mean Intersection over Union (mIoU) metric for semantic segmentation.

    This metric computes the mean IoU across all classes, which is the
    standard evaluation metric for semantic segmentation tasks.
    """

    def __init__(self, num_classes: int, name: str = "mean_iou", **kwargs):
        """
        Initialize the mIoU metric.

        Args:
            num_classes: Number of segmentation classes
            name: Name of the metric
            **kwargs: Additional keyword arguments
        """
        super().__init__(name=name, **kwargs)
        self.num_classes = num_classes

        # Create confusion matrix to track predictions
        self.confusion_matrix = self.add_weight(
            name="confusion_matrix",
            shape=(num_classes, num_classes),
            initializer="zeros",
            dtype=tf.float32,
        )

    def update_state(self, y_true, y_pred, *a, **kw):
        """
        Update the confusion matrix with new predictions.

        Args:
            y_true: Ground truth labels (sparse format)
            y_pred: Predicted logits or probabilities
            sample_weight: Optional sample weights
        """
        # Convert predictions to class indices
        if y_pred.shape[-1] > 1:
            # If y_pred has multiple channels (one-hot or logits), take argmax
            y_pred = tf.argmax(y_pred, axis=-1)

        # Flatten the tensors
        y_true = tf.cast(tf.reshape(y_true, [-1]), tf.int32)
        y_pred = tf.cast(tf.reshape(y_pred, [-1]), tf.int32)

        # Create mask for valid predictions (ignore background or invalid classes)
        mask = tf.logical_and(
            tf.greater_equal(y_true, 0), tf.less(y_true, self.num_classes)
        )
        mask = tf.logical_and(
            mask,
            tf.logical_and(
                tf.greater_equal(y_pred, 0), tf.less(y_pred, self.num_classes)
            ),
        )

        # Apply mask
        y_true = tf.boolean_mask(y_true, mask)
        y_pred = tf.boolean_mask(y_pred, mask)

        # Compute confusion matrix
        indices = tf.stack([y_true, y_pred], axis=1)
        updates = tf.ones_like(y_true, dtype=tf.float32)

        # Update confusion matrix
        confusion_update = tf.scatter_nd(
            indices, updates, [self.num_classes, self.num_classes]
        )
        self.confusion_matrix.assign_add(confusion_update)

    def result(self):
        """
        Compute the mean IoU from the confusion matrix.

        Returns:
            Mean IoU value
        """
        # Compute IoU for each class
        # IoU = TP / (TP + FP + FN)
        # TP = diagonal elements
        # FP = column sum - diagonal
        # FN = row sum - diagonal

        true_positives = tf.linalg.diag_part(self.confusion_matrix)
        false_positives = tf.reduce_sum(self.confusion_matrix, axis=0) - true_positives
        false_negatives = tf.reduce_sum(self.confusion_matrix, axis=1) - true_positives

        # Compute IoU for each class
        denominator = true_positives + false_positives + false_negatives
        iou = tf.where(tf.greater(denominator, 0), true_positives / denominator, 0.0)

        # Return mean IoU (excluding classes with no ground truth)
        valid_classes = tf.greater(denominator, 0)
        mean_iou = tf.where(
            tf.reduce_any(valid_classes),
            tf.reduce_sum(iou) / tf.reduce_sum(tf.cast(valid_classes, tf.float32)),
            0.0,
        )

        return mean_iou

    def reset_state(self):
        """Reset the confusion matrix."""
        self.confusion_matrix.assign(tf.zeros_like(self.confusion_matrix))


class PerClassMeanIoU(tf.keras.metrics.Metric):
    """
    Mean IoU metric with per-class IoU tracking.

    Returns:
        - .result() : mean IoU over valid classes
        - .per_class_result() : tf.Tensor of IoU per class
    """

    def __init__(self, num_classes, name="per_class_iou", **kwargs):
        super().__init__(name=name, **kwargs)
        self.num_classes = num_classes
        self.confusion_matrix = self.add_weight(
            name="confusion_matrix",
            shape=(num_classes, num_classes),
            initializer="zeros",
            dtype=tf.float32,
        )

    def update_state(self, y_true, y_pred, *args, **kwargs):
        if y_pred.shape[-1] > 1:
            y_pred = tf.argmax(y_pred, axis=-1)

        y_true = tf.cast(tf.reshape(y_true, [-1]), tf.int32)
        y_pred = tf.cast(tf.reshape(y_pred, [-1]), tf.int32)

        mask = tf.logical_and(
            tf.greater_equal(y_true, 0), tf.less(y_true, self.num_classes)
        )
        mask = tf.logical_and(
            mask,
            tf.logical_and(
                tf.greater_equal(y_pred, 0), tf.less(y_pred, self.num_classes)
            ),
        )

        y_true = tf.boolean_mask(y_true, mask)
        y_pred = tf.boolean_mask(y_pred, mask)

        indices = tf.stack([y_true, y_pred], axis=1)
        updates = tf.ones_like(y_true, dtype=tf.float32)

        cm_update = tf.scatter_nd(
            indices, updates, [self.num_classes, self.num_classes]
        )
        self.confusion_matrix.assign_add(cm_update)

    def result(self):
        return tf.reduce_mean(self.per_class_result())

    def per_class_result(self):
        tp = tf.linalg.diag_part(self.confusion_matrix)
        fp = tf.reduce_sum(self.confusion_matrix, axis=0) - tp
        fn = tf.reduce_sum(self.confusion_matrix, axis=1) - tp
        denom = tp + fp + fn
        iou = tf.where(denom > 0, tp / denom, 0.0)
        return iou  # shape = (num_classes,)

    def reset_state(self):
        self.confusion_matrix.assign(tf.zeros_like(self.confusion_matrix))


class DiceCoefficient(tf.keras.metrics.Metric):
    """
    Custom Keras metric to compute the average Dice Coefficient
    for multi-class segmentation tasks.

    Parameters
    ----------
    num_classes : int
        Number of target classes.
    smooth : float, optional
        Smoothing constant to avoid division by zero (default is 1e-6).
    name : str, optional
        Name of the metric (default is "dice_coefficient").
    kwargs : dict
        Additional keyword arguments passed to the base class.
    """

    def __init__(self, num_classes, smooth=1e-6, name="dice_coef", **kwargs):
        super().__init__(name=name, **kwargs)
        self.num_classes = num_classes
        self.smooth = smooth
        self.dice = self.add_weight(name="dice", initializer="zeros")
        self.count = self.add_weight(name="count", initializer="zeros")

    def update_state(self, y_true, y_pred, *a, **kw):
        """
        Update the internal state of the metric with a new batch of data.

        Parameters
        ----------
        y_true : tf.Tensor
            Ground truth segmentation masks (shape: (batch_size, height, width)).
        y_pred : tf.Tensor
            Predicted logits or probabilities (shape: (batch_size, height, width, num_classes)).
        """
        y_true = tf.cast(y_true, tf.int32)
        y_true = tf.one_hot(y_true, depth=self.num_classes, dtype=tf.float32)

        y_pred = tf.argmax(y_pred, axis=-1)
        y_pred = tf.one_hot(y_pred, depth=self.num_classes, dtype=tf.float32)

        # Dice par classe
        intersection = tf.reduce_sum(y_true * y_pred, axis=[0, 1, 2])  # (num_classes,)
        union = tf.reduce_sum(y_true + y_pred, axis=[0, 1, 2])  # (num_classes,)
        dice = (2.0 * intersection + self.smooth) / (union + self.smooth)

        self.dice.assign_add(tf.reduce_sum(dice))
        self.count.assign_add(tf.cast(self.num_classes, tf.float32))

    def result(self):
        """
        Return the average Dice coefficient across all updates.
        """
        return self.dice / self.count

    def reset_states(self):
        """
        Reset all of the metric's state variables.
        """
        self.dice.assign(0.0)
        self.count.assign(0.0)


class PerClassDice(tf.keras.metrics.Metric):
    def __init__(self, num_classes, name="per_class_dice", **kwargs):
        super().__init__(name=name, **kwargs)
        self.num_classes = num_classes
        self.smooth = 1e-6
        self.intersections = self.add_weight(
            name="intersections", shape=(num_classes,), initializer="zeros"
        )
        self.unions = self.add_weight(
            name="unions", shape=(num_classes,), initializer="zeros"
        )

    def update_state(self, y_true, y_pred, *args, **kwargs):
        y_true = tf.cast(y_true, tf.int32)
        y_true = tf.one_hot(y_true, self.num_classes, dtype=tf.float32)

        y_pred = tf.argmax(y_pred, axis=-1)
        y_pred = tf.one_hot(y_pred, self.num_classes, dtype=tf.float32)

        intersection = tf.reduce_sum(
            y_true * y_pred, axis=[0, 1, 2]
        )  # sum over H, W, batch
        union = tf.reduce_sum(y_true + y_pred, axis=[0, 1, 2])

        self.intersections.assign_add(intersection)
        self.unions.assign_add(union)

    def result(self):
        dice = (2 * self.intersections + self.smooth) / (self.unions + self.smooth)
        return dice  # vecteur de taille (num_classes,)

    def reset_states(self):
        self.intersections.assign(tf.zeros_like(self.intersections))
        self.unions.assign(tf.zeros_like(self.unions))
