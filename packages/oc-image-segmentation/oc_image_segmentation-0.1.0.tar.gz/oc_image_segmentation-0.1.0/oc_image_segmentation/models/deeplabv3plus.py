import logging
from typing import List, Optional, Tuple

from tensorflow import keras
from tensorflow.keras import layers

from .base_model import BaseSegmentationModel
from .layers import ResizeToMatch, ResizeToMatchLowLevel

logger = logging.getLogger(__name__)


class DeepLabV3PlusModel(BaseSegmentationModel):
    """
    DeepLabV3+ model for semantic segmentation.
    """

    def __init__(
        self,
        input_size: Tuple[int, int] = (256, 256),
        backbone: str = "efficientnetv2b3",
        output_stride: int = 8,
        aspp_filters: int = 128,
        decoder_filters: int = 128,
        dropout_rate: float = 0.2,
        aspp_dilations: List[int] = None,
        num_classes: Optional[int] = 8,
    ):
        super().__init__(num_classes)
        self.input_size = input_size
        self.backbone = backbone
        self.output_stride = output_stride
        self.aspp_filters = aspp_filters
        self.decoder_filters = decoder_filters
        self.dropout_rate = dropout_rate
        self.aspp_dilations = aspp_dilations or [6, 12, 18]

    def _depthwise_separable_conv(
        self,
        inputs,
        filters,
        kernel_size: int = 3,
        name=None,
    ):
        x = layers.DepthwiseConv2D(
            kernel_size=kernel_size,
            padding="same",
            use_bias=False,
            name=f"{name}_depthwise",
        )(inputs)
        x = layers.BatchNormalization(name=f"{name}_depthwise_bn")(x)
        x = layers.ReLU(name=f"{name}_depthwise_relu")(x)
        x = layers.Conv2D(
            filters,
            kernel_size=1,
            padding="same",
            use_bias=False,
            name=f"{name}_pointwise",
        )(x)
        x = layers.BatchNormalization(name=f"{name}_pointwise_bn")(x)
        x = layers.ReLU(name=f"{name}_pointwise_relu")(x)
        return x

    def _aspp_module(self, inputs, filters):
        image_pool = layers.GlobalAveragePooling2D()(inputs)
        image_pool = layers.Reshape((1, 1, -1))(image_pool)
        image_pool = layers.Conv2D(filters, 1, use_bias=False)(image_pool)
        image_pool = layers.BatchNormalization()(image_pool)
        image_pool = layers.ReLU()(image_pool)
        image_pool = ResizeToMatch()([image_pool, inputs])

        branches = [image_pool]

        for _, rate in enumerate(self.aspp_dilations, start=1):
            branch = layers.Conv2D(
                filters,
                3,
                padding="same",
                dilation_rate=rate,
                use_bias=False,
            )(inputs)

            branch = layers.BatchNormalization()(branch)
            branch = layers.ReLU()(branch)
            branches.append(branch)

        aspp = layers.Concatenate()(branches)
        aspp = layers.Conv2D(filters, 1, use_bias=False)(aspp)
        aspp = layers.BatchNormalization()(aspp)
        aspp = layers.ReLU()(aspp)

        return layers.Dropout(self.dropout_rate)(aspp)

    def _create_backbone(self, inputs):
        if self.backbone == "resnet50":
            backbone = keras.applications.ResNet50(
                include_top=False,
                input_tensor=inputs,
                weights="imagenet",
            )

            low = backbone.get_layer("conv2_block3_out").output
            high = backbone.get_layer("conv5_block3_out").output

        elif self.backbone == "resnet101":
            backbone = keras.applications.ResNet101(
                weights="imagenet", include_top=False, input_tensor=inputs
            )
            low = backbone.get_layer("conv2_block3_out").output
            high = backbone.get_layer("conv5_block3_out").output

        elif self.backbone == "resnet152":
            backbone = keras.applications.ResNet152(
                weights="imagenet", include_top=False, input_tensor=inputs
            )
            low = backbone.get_layer("conv2_block3_out").output
            high = backbone.get_layer("conv5_block3_out").output

        elif self.backbone == "efficientnetv2b3":
            # Note: EfficientNetV2B4 n'est pas disponible dans cette version de TensorFlow,
            # on utilise EfficientNetV2B3 comme fallback
            backbone = keras.applications.EfficientNetV2B3(
                weights="imagenet", include_top=False, input_tensor=inputs
            )
            # EfficientNetV2B3 feature extraction points
            # Low-level features from block2 (1/4 resolution - 56x56 pour input 224x224)
            low = backbone.get_layer("block2b_add").output
            # High-level features from block6 (1/32 resolution - 7x7 pour input 224x224)
            high = backbone.get_layer("block6h_add").output

        else:
            # Default to a simple backbone
            logger.warning(f"Backbone '{self.backbone}' not supported, use dummy one.")

            # Simple CNN backbone for demonstration
            x = layers.Conv2D(64, 3, strides=2, padding="same", use_bias=False)(inputs)
            x = layers.BatchNormalization()(x)
            x = layers.ReLU()(x)

            x = layers.Conv2D(128, 3, strides=2, padding="same", use_bias=False)(x)
            x = layers.BatchNormalization()(x)
            low = layers.ReLU()(x)  # 1/4 resolution

            x = layers.Conv2D(256, 3, strides=2, padding="same", use_bias=False)(low)
            x = layers.BatchNormalization()(x)
            x = layers.ReLU()(x)

            x = layers.Conv2D(512, 3, strides=2, padding="same", use_bias=False)(x)
            x = layers.BatchNormalization()(x)
            x = layers.ReLU()(x)

            x = layers.Conv2D(1024, 3, strides=2, padding="same", use_bias=False)(x)
            x = layers.BatchNormalization()(x)
            high = layers.ReLU()(x)  # 1/32 resolution

        return low, high

    def _decoder_module(self, high, low):
        low = layers.Conv2D(
            48,
            1,
            padding="same",
            use_bias=False,
        )(low)
        low = layers.BatchNormalization()(low)
        low = layers.ReLU()(low)

        high = layers.UpSampling2D(
            size=(4, 4),
            interpolation="bilinear",
        )(high)
        high = ResizeToMatchLowLevel()([high, low])

        x = layers.Concatenate()([high, low])
        x = self._depthwise_separable_conv(
            x,
            self.decoder_filters,
            name="decoder1",
        )
        x = self._depthwise_separable_conv(
            x,
            self.decoder_filters,
            name="decoder2",
        )

        return layers.UpSampling2D(
            size=(4, 4),
            interpolation="bilinear",
        )(x)

    def build_model(self) -> keras.Model:
        inputs = layers.Input(shape=(*self.input_size, 3))

        low, high = self._create_backbone(inputs)
        aspp = self._aspp_module(high, self.aspp_filters)
        decoded = self._decoder_module(aspp, low)

        outputs = layers.Conv2D(
            self.num_classes,
            1,
            activation="softmax",
        )(decoded)

        self.model = keras.Model(
            inputs=inputs,
            outputs=outputs,
            name="deeplabv3plus",
        )

        return self.model
