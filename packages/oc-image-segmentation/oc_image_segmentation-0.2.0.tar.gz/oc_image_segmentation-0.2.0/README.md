# 🖼️ OC Image Segmentation

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange.svg)](https://tensorflow.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A comprehensive image segmentation library using deep learning,
with support for U-Net and DeepLabV3+ on the Cityscapes dataset.

## 🚀 Installation

```bash
git clone https://github.com/your-repo/oc-image-segmentation.git
cd oc-image-segmentation
pip install -e .
```

## 📖 Quick Start

### Command Line Interface (CLI)

```bash
# Segment an image
python -m oc_image_segmentation.cli segment input.jpg -o output.png

# With custom model
python -m oc_image_segmentation.cli segment input.jpg -o output.png --model unet_attention

# Train a model
python -m oc_image_segmentation.cli model train unet /path/to/cityscapes --epochs 50

# Evaluate a model
python -m oc_image_segmentation.cli model eval unet /path/to/cityscapes --model-path model.h5
```

### Python API

```python
from oc_image_segmentation import UNetModel, CityscapesDataset, segment_image

# Create and train a model
unet = UNetModel(input_size=(512, 512))
model = unet.build_model(use_attention=True)

# Load a dataset
dataset = CityscapesDataset("/path/to/cityscapes", split="train")

# Segment an image
result = segment_image("input.jpg", model="unet", output_path="output.png")
```

## 🏗️ Model Architectures

### U-Net

- **Standard U-Net**: Classic encoder-decoder architecture
- **U-Net Attention**: With attention gate mechanisms
- Optimized for urban image segmentation
- Support for skip connections and batch normalization

### DeepLabV3+

- **DeepLabV3+ ResNet50**: Standard version with ResNet50 backbone
- **DeepLabV3+ ResNet101**: High-performance version with ResNet101
- **DeepLabV3+ EfficientNetV2B4**: Efficient version with EfficientNetV2B4 backbone
- ASPP (Atrous Spatial Pyramid Pooling) module
- Depthwise separable convolutions for efficiency

## 📊 Dataset and Preparation

### Cityscapes Dataset

Required structure:

```text
dataset/
├── leftImg8bit_trainvaltest/
│   └── leftImg8bit/
│       ├── train/
│       ├── val/
│       └── test/
└── gtFine_trainvaltest/
    └── gtFine/
        ├── train/
        ├── val/
        └── test/
```

### Dataset Commands

```bash
# Load and explore a dataset
python -m oc_image_segmentation.cli dataset load /path/to/cityscapes

# Create all splits
python -m oc_image_segmentation.cli dataset create-all /path/to/cityscapes --batch-size 16
```

## 🎨 Data Augmentation

### TensorFlow Augmentation (Standard)

Configuration in `settings.yaml`:

```yaml
data_augmentation:
  enabled: true
  horizontal_flip: true
  vertical_flip: false
  rotation_range: 5
  zoom_range: 0.05
  brightness_range: [0.9, 1.1]
  contrast_range: [0.9, 1.1]
  noise_factor: 0.01
```

### Albumentations Augmentation (Advanced)

For more robust and performant augmentations:

```python
from oc_image_segmentation.datasets.preprocessing import (
    augment_data_albumentations,
    create_albumentations_config
)

# Use a predefined preset
config = create_albumentations_config("medium")
aug_image, aug_mask = augment_data_albumentations(image, mask, config)

# Custom configuration
custom_config = {
    "enabled": True,
    "horizontal_flip": True,
    "rotation_range": 10,
    "brightness_range": [0.8, 1.2],
    "elastic_transform": True,
    "weather_effects": True,
}
```

**Albumentations Advantages:**
- Consistent geometric transformations for image/mask
- Realistic weather effects
- Elastic and optical distortions
- Optimized performance
- Advanced segmentation support

Predefined profiles:

- **Urban driving**: Conservative augmentations
- **High precision**: Minimal augmentations
- **Robustness**: Extended augmentations

## 📈 Training and Evaluation

### Training

```bash
# Standard U-Net
python -m oc_image_segmentation.cli model train unet /path/to/cityscapes

# U-Net with attention (more parameters)
python -m oc_image_segmentation.cli model train unet_attention /path/to/cityscapes --epochs 100

# High-performance DeepLabV3+
python -m oc_image_segmentation.cli model train deeplabv3plus_resnet101 /path/to/cityscapes

# EfficientNet-based DeepLabV3+
python -m oc_image_segmentation.cli model train deeplabv3plus_efficientnet /path/to/cityscapes
```

### Metrics and Evaluation

- **mIoU (mean Intersection over Union)**: Primary metric
- **IoU per class**: Detailed analysis per Cityscapes class
- **Confusion matrix**: Error diagnosis
- **Callbacks**: EarlyStopping, ModelCheckpoint, ReduceLROnPlateau

```bash
# Complete evaluation
python -m oc_image_segmentation.cli model eval unet /path/to/cityscapes --model-path model.h5 --split val

# Prediction with mIoU
python -m oc_image_segmentation.cli model predict unet input.jpg output.png --model-path model.h5 --ground-truth gt.png
```

## ⚙️ Configuration

### Flexible Configuration System

- **settings.yaml**: Main configuration
- **Environment variables**: Override with `OC_SEGMENT_` prefix
- **Multiple files**: Cascading configuration support
- **Profiles**: Predefined configurations (development, production, test)

### Precision Profiles

- **Ultra-fast**: Maximum performance, reduced precision
- **Balanced**: Good speed/precision compromise
- **High precision**: Maximum precision for production

```bash
# View current configuration
python -m oc_image_segmentation.cli config

# Use specific profile
export OC_SEGMENT_SETTINGS_FILES="settings/prod_settings.yaml"
```

## 🔧 Advanced Features

### Pre-trained Models

- Available pre-trained models
- Simplified transfer learning
- Resume training (`--resume-from`)

### Detailed IoU Analysis

- Per-class IoU with Cityscapes names
- Analysis of problematic classes
- Automatic improvement recommendations

### Custom Callbacks

- Intelligent EarlyStopping on validation mIoU
- Automatic best model saving
- Training history in CSV
- Automatic visualizations

### Category Management

- Support for trainId and categoryId
- Automatic Cityscapes class mapping
- Configurable ignored classes

## 📝 Complete CLI Commands

### Segmentation

```bash
# Basic segmentation
segment input.jpg -o output.png

# With advanced options
segment input.jpg -o output.png --model deeplabv3plus --confidence-threshold 0.7 --no-overlay
```

### Model Management

```bash
# Create a model
model create unet_attention --no-summary

# Train
model train unet /dataset --epochs 50 --output-dir ./models/ --resume-from weights.h5

# Evaluate
model eval unet /dataset --model-path model.h5 --split test

# Predict
model predict unet input.jpg output.png --model-path model.h5 --ground-truth gt.png
```

### Dataset Management

```bash
# Load and explore
dataset load /path/to/cityscapes --split train --batch-size 32

# Create all splits
dataset create-all /path/to/cityscapes --batch-size 16
```

## 🐛 Debugging and Optimization

### Troubleshooting

- **AutoGraph correction guide**: Common TensorFlow issues
- **Test migration**: Updating existing tests
- **Memory optimization**: Memory usage reduction techniques
- **Profiling**: Detailed performance analysis

### Logging and Monitoring

- Structured logs with configurable levels
- Real-time metrics during training
- Automatic performance profiling
- Test cleanup reports

## 🤝 Contributing

1. Fork the project
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Cityscapes Dataset: [cityscapes-dataset.com](https://www.cityscapes-dataset.com/)
- U-Net Architecture: Ronneberger et al.
- DeepLabV3+ Architecture: Chen et al.
- EfficientNet Architecture: Tan & Le
- TensorFlow/Keras for the deep learning framework
