"""
Model implementations for Tiny AI.

This module provides model implementations for both LLMs and Vision models,
along with a factory function to create models based on configuration.
"""

from .base import BaseModel
from .llm import LLMModel
from .vision import VisionModel

__all__ = ["BaseModel", "LLMModel", "VisionModel", "get_model"]


def get_model(config, device=None):
    """
    Factory function to create a model based on configuration.

    Args:
        config: Model configuration
        device: Device to place the model on

    Returns:
        Initialized model
    """
    model_type = config.get('type', 'transformer').lower()

    if model_type in ["llm", "transformer", "gpt"]:
        return LLMModel(config, device)
    elif model_type in ["vision", "cnn", "resnet"]:
        return VisionModel(config, device)
    else:
        raise ValueError(f"Unknown model type: {model_type}")
