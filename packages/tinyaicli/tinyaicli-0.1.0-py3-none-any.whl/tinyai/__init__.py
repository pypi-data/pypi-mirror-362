"""
Tiny AI Model Trainer

A powerful CLI tool for training small Language Models (LLMs) and Vision models
using custom YAML configurations for reproducible research.
"""

__version__ = "0.1.0"
__author__ = "Nathan Heinstein"

from .train import main
from .models import LLMModel, VisionModel
from .training import Trainer

__all__ = [
    "main",
    "LLMModel",
    "VisionModel",
    "Trainer",
]
