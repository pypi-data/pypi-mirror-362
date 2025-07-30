"""
Custom loss functions for semantic segmentation.

This module provides loss functions that handle ignore labels and
class imbalance for segmentation tasks.
"""

import numpy as np
import tensorflow as tf


def sparse_categorical_crossentropy_with_ignore(
    ignore_label: int = 255,
    **_,
):
    """
    Create a sparse categorical crossentropy loss that ignores specific labels.

    Args:
        ignore_label: Label value to ignore (default: 255)

    Returns:
        Loss function that can be used with Keras model.compile()
    """

    def loss_fn(y_true, y_pred):
        # Cast y_true to int32 to ensure proper indexing
        y_true = tf.cast(y_true, tf.int32)

        # Create mask for non-ignored pixels
        mask = tf.not_equal(y_true, ignore_label)

        # Flatten the tensors for easier processing
        y_true_flat = tf.reshape(y_true, [-1])
        y_pred_flat = tf.reshape(y_pred, [-1, tf.shape(y_pred)[-1]])
        mask_flat = tf.reshape(mask, [-1])

        # Filter out ignored pixels
        y_true_valid = tf.boolean_mask(y_true_flat, mask_flat)
        y_pred_valid = tf.boolean_mask(y_pred_flat, mask_flat)

        # Compute loss only on valid pixels
        loss = tf.keras.losses.sparse_categorical_crossentropy(
            y_true_valid, y_pred_valid, from_logits=True
        )

        # Return mean loss (handle case where no valid pixels exist)
        return tf.cond(
            tf.greater(tf.size(y_true_valid), 0),
            lambda: tf.reduce_mean(loss),
            lambda: 0.0,
        )

    return loss_fn


def weighted_sparse_categorical_crossentropy_with_ignore(
    ignore_label: int = 255,
    class_weight=None,
    **_,
):
    """
    Create a weighted sparse categorical crossentropy loss that ignores specific labels.

    Args:
        class_weight: Weights for each class (list or tensor)
        ignore_label: Label value to ignore (default: 255)

    Returns:
        Loss function that can be used with Keras model.compile()
    """
    if class_weight:
        np_weights = [np.float32(v) for v in class_weight.values()]
        ts_weights = tf.convert_to_tensor(np_weights, dtype=tf.float32)
    else:
        ts_weights = None

    def loss_fn(y_true, y_pred):
        # Cast y_true to int32 to ensure proper indexing
        y_true = tf.cast(y_true, tf.int32)

        # Create mask for non-ignored pixels
        mask = tf.not_equal(y_true, ignore_label)

        # Flatten the tensors for easier processing
        y_true_flat = tf.reshape(y_true, [-1])
        y_pred_flat = tf.reshape(y_pred, [-1, tf.shape(y_pred)[-1]])
        mask_flat = tf.reshape(mask, [-1])

        # Filter out ignored pixels
        y_true_valid = tf.boolean_mask(y_true_flat, mask_flat)
        y_pred_valid = tf.boolean_mask(y_pred_flat, mask_flat)

        # Compute base loss
        loss = tf.keras.losses.sparse_categorical_crossentropy(
            y_true_valid, y_pred_valid, from_logits=True
        )

        # Apply class weights if provided
        if ts_weights is not None:
            weights = tf.gather(ts_weights, y_true_valid)
            loss = loss * weights

        # Return mean loss (handle case where no valid pixels exist)
        return tf.cond(
            tf.greater(tf.size(y_true_valid), 0),
            lambda: tf.reduce_mean(loss),
            lambda: 0.0,
        )

    return loss_fn


def focal_loss_with_ignore(
    alpha: float = 0.25,
    gamma: float = 2.0,
    ignore_label: int = 255,
    **_,
):
    """
    Create a focal loss that handles class imbalance and ignores specific labels.

    Args:
        alpha: Weighting factor for rare class (default: 0.25)
        gamma: Focusing parameter (default: 2.0)
        ignore_label: Label value to ignore (default: 255)

    Returns:
        Loss function that can be used with Keras model.compile()
    """

    def loss_fn(y_true, y_pred):
        # Cast y_true to int32 to ensure proper indexing
        y_true = tf.cast(y_true, tf.int32)

        # Create mask for non-ignored pixels
        mask = tf.not_equal(y_true, ignore_label)

        # Flatten the tensors for easier processing
        y_true_flat = tf.reshape(y_true, [-1])
        y_pred_flat = tf.reshape(y_pred, [-1, tf.shape(y_pred)[-1]])
        mask_flat = tf.reshape(mask, [-1])

        # Filter out ignored pixels
        y_true_valid = tf.boolean_mask(y_true_flat, mask_flat)
        y_pred_valid = tf.boolean_mask(y_pred_flat, mask_flat)

        # Convert to probabilities
        y_pred_softmax = tf.nn.softmax(y_pred_valid, axis=-1)

        # One-hot encode true labels
        num_classes = tf.shape(y_pred_valid)[-1]
        y_true_onehot = tf.one_hot(y_true_valid, num_classes)

        # Compute focal loss
        epsilon = tf.keras.backend.epsilon()
        y_pred_softmax = tf.clip_by_value(y_pred_softmax, epsilon, 1.0 - epsilon)

        # Compute cross-entropy
        ce_loss = -y_true_onehot * tf.math.log(y_pred_softmax)

        # Compute focal weight
        p_t = tf.reduce_sum(y_true_onehot * y_pred_softmax, axis=-1)
        focal_weight = alpha * tf.pow(1.0 - p_t, gamma)

        # Apply focal weight
        focal_loss = focal_weight * tf.reduce_sum(ce_loss, axis=-1)

        # Return mean loss (handle case where no valid pixels exist)
        return tf.cond(
            tf.greater(tf.size(y_true_valid), 0),
            lambda: tf.reduce_mean(focal_loss),
            lambda: 0.0,
        )

    return loss_fn


# Convenience functions
def get_cityscapes_loss(loss_type: str = "sparse_categorical_crossentropy", **kwargs):
    """
    Get a loss function suitable for Cityscapes dataset.

    Args:
        loss_type: Type of loss function
            - "sparse_categorical_crossentropy": Standard CE with ignore
            - "sparse_categorical_crossentropy_with_ignore": Alias for the above
            - "weighted": Weighted CE with ignore
            - "focal": Focal loss with ignore

    Returns:
        Loss function
    """
    if loss_type == "sparse_categorical_crossentropy":
        return sparse_categorical_crossentropy_with_ignore(ignore_label=255, **kwargs)
    elif loss_type == "sparse_categorical_crossentropy_with_ignore":
        return sparse_categorical_crossentropy_with_ignore(ignore_label=255, **kwargs)
    elif loss_type == "weighted":
        # You can customize these weights based on your dataset statistics
        return weighted_sparse_categorical_crossentropy_with_ignore(
            ignore_label=255, **kwargs
        )
    elif loss_type == "focal":
        return focal_loss_with_ignore(ignore_label=255, **kwargs)
    else:
        raise ValueError(f"Unknown loss type: {loss_type}")
