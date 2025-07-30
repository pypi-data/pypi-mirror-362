import tensorflow as tf
from keras.saving import register_keras_serializable
from tensorflow.keras import layers


@register_keras_serializable(package="CustomLayers")
class ResizeToMatch(layers.Layer):
    def call(self, inputs_list):
        image_level, reference = inputs_list
        target_shape = tf.shape(reference)[1:3]  # Get height and width
        return tf.image.resize(image_level, target_shape, method="bilinear")


@register_keras_serializable(package="CustomLayers")
class ResizeToMatchLowLevel(layers.Layer):
    def call(self, inputs_list):
        high_level, low_level = inputs_list
        target_shape = tf.shape(low_level)[1:3]  # Get height and width
        return tf.image.resize(high_level, target_shape, method="bilinear")
