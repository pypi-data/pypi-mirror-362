"""
Vision model implementation for Tiny AI.

This module provides a CNN-based vision model implementation
suitable for image classification tasks.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Dict, Any, Optional

from .base import BaseModel


class ConvBlock(nn.Module):
    """Convolutional block with batch normalization and activation."""

    def __init__(self, in_channels, out_channels, kernel_size=3, stride=1, padding=1):
        super().__init__()
        self.conv = nn.Conv2d(in_channels, out_channels, kernel_size, stride, padding, bias=False)
        self.bn = nn.BatchNorm2d(out_channels)
        self.activation = nn.ReLU(inplace=True)

    def forward(self, x):
        return self.activation(self.bn(self.conv(x)))


class ResidualBlock(nn.Module):
    """Residual block for ResNet-style architecture."""

    def __init__(self, in_channels, out_channels, stride=1):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, 3, stride, 1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.conv2 = nn.Conv2d(out_channels, out_channels, 3, 1, 1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels)

        self.shortcut = nn.Sequential()
        if stride != 1 or in_channels != out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, 1, stride, bias=False),
                nn.BatchNorm2d(out_channels)
            )

    def forward(self, x):
        residual = self.shortcut(x)

        out = F.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += residual
        out = F.relu(out)

        return out


class VisionModel(BaseModel):
    """
    CNN-based Vision Model for Tiny AI Model Trainer.

    This model implements a ResNet-style architecture suitable
    for image classification tasks.
    """

    def __init__(self, config: Dict[str, Any], device: Optional[torch.device] = None):
        """
        Initialize the vision model.

        Args:
            config: Model configuration
            device: Device to place the model on
        """
        super().__init__(config, device)

        # Model parameters
        self.num_classes = config['num_classes']
        self.in_channels = config.get("in_channels", 3)
        self.hidden_size = config.get("hidden_size", 64)
        self.num_blocks = config.get("num_blocks", [2, 2, 2, 2])  # ResNet-18 style

        # Initial convolution
        self.conv1 = ConvBlock(self.in_channels, self.hidden_size, kernel_size=7, stride=2, padding=3)
        self.maxpool = nn.MaxPool2d(3, stride=2, padding=1)

        # Residual blocks
        self.layer1 = self._make_layer(self.hidden_size, self.hidden_size, self.num_blocks[0], stride=1)
        self.layer2 = self._make_layer(self.hidden_size, self.hidden_size * 2, self.num_blocks[1], stride=2)
        self.layer3 = self._make_layer(self.hidden_size * 2, self.hidden_size * 4, self.num_blocks[2], stride=2)
        self.layer4 = self._make_layer(self.hidden_size * 4, self.hidden_size * 8, self.num_blocks[3], stride=2)

        # Global average pooling and classifier
        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        self.classifier = nn.Linear(self.hidden_size * 8, self.num_classes)

        # Initialize weights
        self.apply(self._init_weights)

    def _make_layer(self, in_channels, out_channels, num_blocks, stride):
        """Create a layer of residual blocks."""
        layers = []
        layers.append(ResidualBlock(in_channels, out_channels, stride))
        for _ in range(1, num_blocks):
            layers.append(ResidualBlock(out_channels, out_channels))
        return nn.Sequential(*layers)

    def _init_weights(self, module):
        """Initialize model weights."""
        if isinstance(module, nn.Conv2d):
            nn.init.kaiming_normal_(module.weight, mode='fan_out', nonlinearity='relu')
        elif isinstance(module, nn.BatchNorm2d):
            nn.init.constant_(module.weight, 1)
            nn.init.constant_(module.bias, 0)
        elif isinstance(module, nn.Linear):
            nn.init.normal_(module.weight, 0, 0.01)
            nn.init.constant_(module.bias, 0)

    def forward(self, image=None, x=None):
        """
        Forward pass of the model.

        Args:
            image: Input images [batch_size, channels, height, width] (keyword argument)
            x: Input images [batch_size, channels, height, width] (positional argument)

        Returns:
            Logits [batch_size, num_classes]
        """
        # Handle both keyword and positional arguments
        if image is not None:
            x = image
        elif x is None:
            raise ValueError("Must provide either 'image' or 'x' argument")
        # Initial convolution and pooling
        x = self.conv1(x)
        x = self.maxpool(x)

        # Residual layers
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)

        # Global average pooling and classification
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)

        return x

    def get_loss(self, outputs, targets):
        """
        Compute the classification loss.

        Args:
            outputs: Model outputs (logits)
            targets: Target class labels

        Returns:
            Loss tensor
        """
        return F.cross_entropy(outputs, targets)

    def get_predictions(self, outputs):
        """
        Get class predictions from model outputs.

        Args:
            outputs: Model outputs (logits)

        Returns:
            Predicted class indices
        """
        return torch.argmax(outputs, dim=1)

    def get_probabilities(self, outputs):
        """
        Get class probabilities from model outputs.

        Args:
            outputs: Model outputs (logits)

        Returns:
            Class probabilities
        """
        return F.softmax(outputs, dim=1)
