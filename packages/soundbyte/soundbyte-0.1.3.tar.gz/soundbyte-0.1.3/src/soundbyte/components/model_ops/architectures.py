"""
Model operations components (neural architectures) for SoundByte.

This module provides implementations of various neural network architectures
for different tasks and datasets.
"""

import torch
import torchaudio
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models
from typing import Dict, Any, List

from ...core.interfaces import ModelOps
from ...plugins.registry import register


@register('model_ops', 'simple_convnet')
class SimpleConvNetOps(nn.Module, ModelOps):
    """Simple Convolutional Neural Network for CIFAR-10."""

    def __init__(self, num_classes: int = 10, channels: List[int] = None, **kwargs):
        super().__init__()
        self.num_classes = num_classes
        self.channels = channels or [32, 64, 128]

        # Convolutional layers
        self.conv1 = nn.Conv2d(3, self.channels[0], kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(self.channels[0], self.channels[1], kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(self.channels[1], self.channels[2], kernel_size=3, padding=1)

        # Batch normalization
        self.bn1 = nn.BatchNorm2d(self.channels[0])
        self.bn2 = nn.BatchNorm2d(self.channels[1])
        self.bn3 = nn.BatchNorm2d(self.channels[2])

        # Pooling and dropout
        self.pool = nn.MaxPool2d(2, 2)
        self.dropout = nn.Dropout(0.5)

        # Calculate the size for the first linear layer
        # After 3 conv layers with pooling: 32x32 -> 16x16 -> 8x8 -> 4x4
        self.fc1 = nn.Linear(self.channels[2] * 4 * 4, 256)
        self.fc2 = nn.Linear(256, self.num_classes)

    def forward(self, x):
        # First conv block
        x = self.pool(F.relu(self.bn1(self.conv1(x))))

        # Second conv block
        x = self.pool(F.relu(self.bn2(self.conv2(x))))

        # Third conv block
        x = self.pool(F.relu(self.bn3(self.conv3(x))))

        # Flatten and fully connected layers
        x = x.view(x.size(0), -1)
        x = self.dropout(F.relu(self.fc1(x)))
        x = self.fc2(x)

        return x

    def get_model(self) -> nn.Module:
        """Return the PyTorch model."""
        return self

    def get_config(self) -> Dict[str, Any]:
        """Return configuration."""
        return {
            'num_classes': self.num_classes,
            'channels': self.channels
        }


@register('model_ops', 'mnist_net')
class MNISTNetOps(nn.Module, ModelOps):
    """Neural network optimized for MNIST dataset."""

    def __init__(self, num_classes: int = 10, hidden_size: int = 128, **kwargs):
        super().__init__()
        self.num_classes = num_classes
        self.hidden_size = hidden_size

        # Convolutional layers
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)

        # Batch normalization
        self.bn1 = nn.BatchNorm2d(32)
        self.bn2 = nn.BatchNorm2d(64)

        # Pooling and dropout
        self.pool = nn.MaxPool2d(2, 2)
        self.dropout1 = nn.Dropout(0.25)
        self.dropout2 = nn.Dropout(0.5)

        # Fully connected layers
        # After 2 conv+pool layers: 28x28 -> 14x14 -> 7x7
        self.fc1 = nn.Linear(64 * 7 * 7, self.hidden_size)
        self.fc2 = nn.Linear(self.hidden_size, self.num_classes)

    def forward(self, x):
        # First conv block
        x = self.pool(F.relu(self.bn1(self.conv1(x))))
        self.dropout1(x)

        # Second conv block
        x = self.pool(F.relu(self.bn2(self.conv2(x))))
        self.dropout1(x)

        # Flatten and fully connected layers
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        x = self.dropout2(x)
        x = self.fc2(x)

        return x

    def get_model(self) -> nn.Module:
        """Return the PyTorch model."""
        return self

    def get_config(self) -> Dict[str, Any]:
        """Return configuration."""
        return {
            'num_classes': self.num_classes,
            'hidden_size': self.hidden_size
        }


@register('model_ops', 'resnet18')
class ResNet18Ops(ModelOps):
    """ResNet-18 architecture wrapper."""

    def __init__(self, num_classes: int = 10, pretrained: bool = False, 
                 in_channels: int = 3, **kwargs):
        self.num_classes = num_classes
        self.pretrained = pretrained
        self.in_channels = in_channels

        # Load ResNet-18
        self.model = models.resnet18(pretrained=pretrained)

        # Modify for different input channels if needed
        if in_channels != 3:
            self.model.conv1 = nn.Conv2d(
                in_channels, 64, kernel_size=7, stride=2, padding=3, bias=False
            )

        # Modify final layer for different number of classes
        self.model.fc = nn.Linear(self.model.fc.in_features, num_classes)

    def get_model(self) -> nn.Module:
        """Return the PyTorch model."""
        return self.model

    def get_config(self) -> Dict[str, Any]:
        """Return configuration."""
        return {
            'num_classes': self.num_classes,
            'pretrained': self.pretrained,
            'in_channels': self.in_channels
        }


@register('model_ops', 'vgg16')
class VGG16Ops(ModelOps):
    """VGG-16 architecture wrapper."""

    def __init__(self, num_classes: int = 10, pretrained: bool = False, **kwargs):
        self.num_classes = num_classes
        self.pretrained = pretrained

        # Load VGG-16
        self.model = models.vgg16(pretrained=pretrained)

        # Modify classifier for different number of classes
        self.model.classifier[6] = nn.Linear(
            self.model.classifier[6].in_features, num_classes
        )

    def get_model(self) -> nn.Module:
        """Return the PyTorch model."""
        return self.model

    def get_config(self) -> Dict[str, Any]:
        """Return configuration."""
        return {
            'num_classes': self.num_classes,
            'pretrained': self.pretrained
        }


@register('model_ops', 'densenet121')
class DenseNet121Ops(ModelOps):
    """DenseNet-121 architecture wrapper."""

    def __init__(self, num_classes: int = 10, pretrained: bool = False, **kwargs):
        self.num_classes = num_classes
        self.pretrained = pretrained

        # Load DenseNet-121
        self.model = models.densenet121(pretrained=pretrained)

        # Modify classifier for different number of classes
        self.model.classifier = nn.Linear(
            self.model.classifier.in_features, num_classes
        )

    def get_model(self) -> nn.Module:
        """Return the PyTorch model."""
        return self.model

    def get_config(self) -> Dict[str, Any]:
        """Return configuration."""
        return {
            'num_classes': self.num_classes,
            'pretrained': self.pretrained
        }


@register('model_ops', 'mobilenet_v2')
class MobileNetV2Ops(ModelOps):
    """MobileNet V2 architecture wrapper."""

    def __init__(self, num_classes: int = 10, pretrained: bool = False, **kwargs):
        self.num_classes = num_classes
        self.pretrained = pretrained

        # Load MobileNet V2
        self.model = models.mobilenet_v2(pretrained=pretrained)

        # Modify classifier for different number of classes
        self.model.classifier[1] = nn.Linear(
            self.model.classifier[1].in_features, num_classes
        )

    def get_model(self) -> nn.Module:
        """Return the PyTorch model."""
        return self.model

    def get_config(self) -> Dict[str, Any]:
        """Return configuration."""
        return {
            'num_classes': self.num_classes,
            'pretrained': self.pretrained
        }


@register('model_ops', 'pretrained_wavlm')
class WavLM(ModelOps):
    def __init__(self, model_name: str = 'WAVLM_BASE', **kwargs):
        try:
            self.bundle = getattr(torchaudio.pipelines, model_name)
            self.model = self.bundle.get_model()
        except Exception as e:
            raise Exception(e)

    def get_model(self):
        return self.model

    def get_config(self):
        return self.bundle._params
    