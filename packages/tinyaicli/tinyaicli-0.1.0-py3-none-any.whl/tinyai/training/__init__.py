"""
Training utilities for Tiny AI.

This module provides the main training loop and optimization utilities
for training both LLMs and vision models.
"""

from .trainer import Trainer
from .optimizer import get_optimizer, get_scheduler

__all__ = ["Trainer", "get_optimizer", "get_scheduler"]
