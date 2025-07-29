"""
Optimizer and scheduler utilities for Tiny AI.

This module provides factory functions for creating optimizers
and learning rate schedulers.
"""

import torch
import torch.optim as optim
from torch.optim.lr_scheduler import LambdaLR, StepLR, CosineAnnealingLR
from typing import Dict, Any


def get_optimizer(model: torch.nn.Module, config: Dict[str, Any]) -> torch.optim.Optimizer:
    """
    Create an optimizer based on configuration.

    Args:
        model: Model to optimize
        config: Training configuration

    Returns:
        PyTorch optimizer
    """
    optimizer_type = config.get("optimizer", "adam").lower()
    learning_rate = config.get("learning_rate", 1e-4)
    weight_decay = config.get("weight_decay", 0.0)

    if optimizer_type == "adam":
        return optim.Adam(
            model.parameters(),
            lr=learning_rate,
            weight_decay=weight_decay,
            betas=config.get("betas", (0.9, 0.999))
        )
    elif optimizer_type == "adamw":
        return optim.AdamW(
            model.parameters(),
            lr=learning_rate,
            weight_decay=weight_decay,
            betas=config.get("betas", (0.9, 0.999))
        )
    elif optimizer_type == "sgd":
        return optim.SGD(
            model.parameters(),
            lr=learning_rate,
            momentum=config.get("momentum", 0.9),
            weight_decay=weight_decay
        )
    elif optimizer_type == "rmsprop":
        return optim.RMSprop(
            model.parameters(),
            lr=learning_rate,
            weight_decay=weight_decay,
            momentum=config.get("momentum", 0.0)
        )
    else:
        raise ValueError(f"Unknown optimizer type: {optimizer_type}")


def get_scheduler(optimizer: torch.optim.Optimizer, config: Dict[str, Any]) -> torch.optim.lr_scheduler._LRScheduler:
    """
    Create a learning rate scheduler based on configuration.

    Args:
        optimizer: Optimizer to schedule
        config: Training configuration

    Returns:
        PyTorch learning rate scheduler
    """
    scheduler_type = config.get("scheduler", "none").lower()

    if scheduler_type == "none":
        return None
    elif scheduler_type == "step":
        return StepLR(
            optimizer,
            step_size=config.get("step_size", 30),
            gamma=config.get("gamma", 0.1)
        )
    elif scheduler_type == "cosine":
        return CosineAnnealingLR(
            optimizer,
            T_max=config.get("num_epochs", 100),
            eta_min=config.get("eta_min", 0.0)
        )
    elif scheduler_type == "warmup_cosine":
        return WarmupCosineScheduler(
            optimizer,
            warmup_steps=config.get("warmup_steps", 1000),
            total_steps=config.get("total_steps", 10000),
            min_lr=config.get("min_lr", 0.0)
        )
    elif scheduler_type == "warmup_linear":
        return WarmupLinearScheduler(
            optimizer,
            warmup_steps=config.get("warmup_steps", 1000),
            total_steps=config.get("total_steps", 10000)
        )
    else:
        raise ValueError(f"Unknown scheduler type: {scheduler_type}")


class WarmupCosineScheduler(LambdaLR):
    """
    Learning rate scheduler with warmup and cosine decay.

    This scheduler linearly increases the learning rate from 0 to the base
    learning rate during warmup, then decays it following a cosine curve.
    """

    def __init__(self, optimizer, warmup_steps: int, total_steps: int, min_lr: float = 0.0):
        """
        Initialize the warmup cosine scheduler.

        Args:
            optimizer: Optimizer to schedule
            warmup_steps: Number of warmup steps
            total_steps: Total number of training steps
            min_lr: Minimum learning rate
        """
        self.warmup_steps = warmup_steps
        self.total_steps = total_steps
        self.min_lr = min_lr

        def lr_lambda(step):
            if step < warmup_steps:
                # Linear warmup
                return float(step) / float(max(1, warmup_steps))
            else:
                # Cosine decay
                progress = float(step - warmup_steps) / float(max(1, total_steps - warmup_steps))
                return max(min_lr, 0.5 * (1.0 + torch.cos(torch.pi * progress)))

        super().__init__(optimizer, lr_lambda)


class WarmupLinearScheduler(LambdaLR):
    """
    Learning rate scheduler with warmup and linear decay.

    This scheduler linearly increases the learning rate from 0 to the base
    learning rate during warmup, then linearly decays it to 0.
    """

    def __init__(self, optimizer, warmup_steps: int, total_steps: int):
        """
        Initialize the warmup linear scheduler.

        Args:
            optimizer: Optimizer to schedule
            warmup_steps: Number of warmup steps
            total_steps: Total number of training steps
        """
        self.warmup_steps = warmup_steps
        self.total_steps = total_steps

        def lr_lambda(step):
            if step < warmup_steps:
                # Linear warmup
                return float(step) / float(max(1, warmup_steps))
            else:
                # Linear decay
                progress = float(step - warmup_steps) / float(max(1, total_steps - warmup_steps))
                return max(0.0, 1.0 - progress)

        super().__init__(optimizer, lr_lambda)
