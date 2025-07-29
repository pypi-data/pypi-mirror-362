"""
Logging utilities for Tiny AI.

This module provides logging setup and utilities for
consistent logging throughout the training pipeline.
"""

import logging
import sys
from typing import Dict, Any
from rich.logging import RichHandler
from rich.console import Console


def setup_logging(config: Dict[str, Any]):
    """
    Setup logging configuration.

    Args:
        config: Logging configuration
    """
    # Create console for rich output
    console = Console()

    # Setup logging level
    log_level = getattr(logging, config.get("level", "INFO").upper())

    # Create rich handler
    rich_handler = RichHandler(
        console=console,
        show_time=True,
        show_path=False,
        markup=True,
        rich_tracebacks=True
    )

    # Setup root logger
    logging.basicConfig(
        level=log_level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[rich_handler]
    )

    # Suppress verbose logging from external libraries
    logging.getLogger("torch").setLevel(logging.WARNING)
    logging.getLogger("torchvision").setLevel(logging.WARNING)
    logging.getLogger("PIL").setLevel(logging.WARNING)
    logging.getLogger("matplotlib").setLevel(logging.WARNING)
    logging.getLogger("wandb").setLevel(logging.INFO)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance.

    Args:
        name: Logger name

    Returns:
        Logger instance
    """
    return logging.getLogger(name)


class TrainingLogger:
    """
    Custom logger for training progress.

    This class provides structured logging for training metrics
    and progress tracking.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the training logger.

        Args:
            config: Logging configuration
        """
        self.config = config
        self.logger = get_logger(__name__)
        self.console = Console()

        # Training state
        self.current_epoch = 0
        self.current_step = 0
        self.best_metrics = {}

    def log_epoch_start(self, epoch: int):
        """Log the start of an epoch."""
        self.current_epoch = epoch
        self.console.print(f"\n[bold blue]Epoch {epoch + 1}[/bold blue]")

    def log_training_step(self, step: int, loss: float, lr: float):
        """Log a training step."""
        self.current_step = step

        if step % self.config.get("log_interval", 100) == 0:
            self.console.print(
                f"  Step {step:6d} | Loss: {loss:.4f} | LR: {lr:.6f}",
                style="dim"
            )

    def log_epoch_end(self, train_loss: float, val_loss: float, val_metrics: Dict[str, float]):
        """Log the end of an epoch."""
        # Log to console
        self.console.print(
            f"  Train Loss: {train_loss:.4f} | Val Loss: {val_loss:.4f}",
            style="bold green"
        )

        if val_metrics:
            for metric_name, metric_value in val_metrics.items():
                self.console.print(f"  {metric_name}: {metric_value:.4f}")

        # Update best metrics
        if val_loss < self.best_metrics.get("val_loss", float('inf')):
            self.best_metrics["val_loss"] = val_loss
            self.console.print("  [bold green]New best validation loss![/bold green]")

    def log_training_complete(self):
        """Log training completion."""
        self.console.print("\n[bold green]Training completed![/bold green]")
        self.console.print(f"Best validation loss: {self.best_metrics.get('val_loss', 'N/A')}")

    def log_error(self, error: Exception):
        """Log an error."""
        self.console.print(f"\n[bold red]Error: {str(error)}[/bold red]")
        self.logger.exception("Training error occurred")
