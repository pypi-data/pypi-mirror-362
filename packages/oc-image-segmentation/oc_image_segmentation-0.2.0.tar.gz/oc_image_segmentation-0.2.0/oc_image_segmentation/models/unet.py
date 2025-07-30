from typing import Tuple

from tensorflow import keras
from tensorflow.keras import layers

from .base_model import BaseSegmentationModel


class UNetModel(BaseSegmentationModel):
    """
    U-Net model for semantic segmentation.
    """

    def __init__(
        self,
        batch_norm: bool = True,
        dropout_rate: float = 0.2,
        filters: int = 64,
        input_size: Tuple[int, int] = (256, 256),
        num_classes: int = 8,
        use_attention: bool = False,
    ):
        """
        Initialize U-Net model.
        """
        super().__init__(num_classes)
        self.batch_norm = batch_norm
        self.dropout_rate = dropout_rate
        self.filters = filters
        self.input_size = input_size
        self.use_attention = use_attention

    def _conv_block(self, inputs, filters: int, kernel_size: int = 3):
        x = layers.Conv2D(filters, kernel_size, padding="same")(inputs)
        if self.batch_norm:
            x = layers.BatchNormalization()(x)
        x = layers.ReLU()(x)

        x = layers.Conv2D(filters, kernel_size, padding="same")(x)
        if self.batch_norm:
            x = layers.BatchNormalization()(x)
        x = layers.ReLU()(x)

        return x

    def _encoder_block(self, inputs, filters: int):
        conv = self._conv_block(inputs, filters)
        pool = layers.MaxPooling2D(pool_size=(2, 2))(conv)
        if self.dropout_rate > 0:
            pool = layers.Dropout(self.dropout_rate)(pool)
        return pool, conv

    def _decoder_block(self, inputs, skip_connection, filters: int):
        up = layers.Conv2DTranspose(
            filters,
            (2, 2),
            strides=(2, 2),
            padding="same",
        )(inputs)

        concat = layers.Concatenate()([up, skip_connection])

        return self._conv_block(concat, filters)

    def _attention_gate(self, gating_signal, skip_connection, filters: int):
        g = layers.Conv2D(filters, 1, padding="same")(gating_signal)
        x = layers.Conv2D(filters, 1, padding="same")(skip_connection)

        if self.batch_norm:
            g = layers.BatchNormalization()(g)
            x = layers.BatchNormalization()(x)

        g = layers.UpSampling2D(size=(2, 2), interpolation="bilinear")(g)

        attention = layers.Add()([g, x])
        attention = layers.ReLU()(attention)
        attention = layers.Conv2D(1, 1, padding="same")(attention)
        attention = layers.Activation("sigmoid")(attention)

        return layers.Multiply()([skip_connection, attention])

    def build_model(self) -> keras.Model:
        inputs = layers.Input(shape=(*self.input_size, 3))

        pool1, conv1 = self._encoder_block(inputs, self.filters)
        pool2, conv2 = self._encoder_block(pool1, self.filters * 2)
        pool3, conv3 = self._encoder_block(pool2, self.filters * 4)
        pool4, conv4 = self._encoder_block(pool3, self.filters * 8)

        bottleneck = self._conv_block(pool4, self.filters * 16)

        if self.use_attention:
            conv4 = self._attention_gate(bottleneck, conv4, self.filters * 8)
        up5 = self._decoder_block(bottleneck, conv4, self.filters * 8)

        if self.use_attention:
            conv3 = self._attention_gate(up5, conv3, self.filters * 4)
        up6 = self._decoder_block(up5, conv3, self.filters * 4)

        if self.use_attention:
            conv2 = self._attention_gate(up6, conv2, self.filters * 2)
        up7 = self._decoder_block(up6, conv2, self.filters * 2)

        if self.use_attention:
            conv1 = self._attention_gate(up7, conv1, self.filters)
        up8 = self._decoder_block(up7, conv1, self.filters)

        outputs = layers.Conv2D(
            self.num_classes,
            1,
            activation="softmax",
        )(up8)

        self.model = keras.Model(
            inputs=inputs,
            outputs=outputs,
            name="unet",
        )

        return self.model
