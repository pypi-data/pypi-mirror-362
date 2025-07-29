"""
Base model class for Tiny AI.

This module provides the base class that all models should inherit from,
defining the common interface and functionality.
"""

import torch
import torch.nn as nn
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class BaseModel(nn.Module, ABC):
    """
    Base class for all models in Tiny AI Model Trainer.

    This class provides common functionality and defines the interface
    that all models must implement.
    """

    def __init__(self, config: Dict[str, Any], device: Optional[torch.device] = None):
        """
        Initialize the base model.

        Args:
            config: Model configuration dictionary
            device: Device to place the model on
        """
        super().__init__()
        self.config = config
        self.device = device or torch.device("cpu")
        self.to(self.device)

    @abstractmethod
    def forward(self, *args, **kwargs):
        """
        Forward pass of the model.

        This method must be implemented by all subclasses.
        """
        pass

    @abstractmethod
    def get_loss(self, outputs, targets):
        """
        Compute the loss for the given outputs and targets.

        Args:
            outputs: Model outputs
            targets: Ground truth targets

        Returns:
            Loss tensor
        """
        pass

    def save(self, path: str):
        """
        Save the model to disk.

        Args:
            path: Path to save the model
        """
        torch.save({
            'model_state_dict': self.state_dict(),
            'config': self.config,
        }, path)

    def load(self, path: str):
        """
        Load the model from disk.

        Args:
            path: Path to load the model from
        """
        checkpoint = torch.load(path, map_location=self.device)
        self.load_state_dict(checkpoint['model_state_dict'])
        return checkpoint.get('config', {})

    def get_num_parameters(self) -> int:
        """
        Get the total number of parameters in the model.

        Returns:
            Total number of parameters
        """
        return sum(p.numel() for p in self.parameters())

    def get_trainable_parameters(self) -> int:
        """
        Get the number of trainable parameters in the model.

        Returns:
            Number of trainable parameters
        """
        return sum(p.numel() for p in self.parameters() if p.requires_grad)
