"""
Learning Rate Finder for Tiny AI.

This module provides utilities for finding optimal learning rates
using the learning rate range test technique.
"""

import math
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from typing import Dict, Any, Optional, Tuple, List
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

from ..utils.logging import get_logger


class LRFinder:
    """
    Learning Rate Finder using the learning rate range test.

    This class implements the learning rate range test as described in
    "Cyclical Learning Rates for Training Neural Networks" by Leslie Smith.
    """

    def __init__(
        self,
        model: nn.Module,
        train_loader: DataLoader,
        optimizer: torch.optim.Optimizer,
        device: torch.device,
        start_lr: float = 1e-7,
        end_lr: float = 10.0,
        num_iter: int = 100,
        step_mode: str = "exp",
        diverge_thresh: float = 5.0,
        accumulation_steps: int = 1
    ):
        """
        Initialize the learning rate finder.

        Args:
            model: Model to train
            train_loader: Training data loader
            optimizer: Optimizer to use
            device: Device to train on
            start_lr: Starting learning rate
            end_lr: Ending learning rate
            num_iter: Number of iterations to run
            step_mode: Learning rate stepping mode ("exp" or "linear")
            diverge_thresh: Threshold for detecting divergence
            accumulation_steps: Gradient accumulation steps
        """
        self.model = model
        self.train_loader = train_loader
        self.optimizer = optimizer
        self.device = device
        self.start_lr = start_lr
        self.end_lr = end_lr
        self.num_iter = num_iter
        self.step_mode = step_mode
        self.diverge_thresh = diverge_thresh
        self.accumulation_steps = accumulation_steps

        self.logger = get_logger(__name__)

        # Store original learning rates
        self.original_lrs = [group['lr'] for group in self.optimizer.param_groups]

        # Results storage
        self.lrs = []
        self.losses = []
        self.best_loss = float('inf')
        self.diverged = False

        # Calculate learning rate multiplier
        if step_mode == "exp":
            self.lr_mult = (end_lr / start_lr) ** (1 / num_iter)
        else:
            self.lr_mult = (end_lr - start_lr) / num_iter

    def range_test(self) -> Tuple[List[float], List[float]]:
        """
        Run the learning rate range test.

        Returns:
            Tuple of (learning_rates, losses)
        """
        self.logger.info("Starting learning rate range test...")
        self.logger.info(f"LR range: {self.start_lr:.2e} to {self.end_lr:.2e}")
        self.logger.info(f"Iterations: {self.num_iter}")

        # Set initial learning rate
        self._set_lr(self.start_lr)

        # Training loop
        data_iter = iter(self.train_loader)
        progress_bar = tqdm(range(self.num_iter), desc="LR Range Test")

        for iteration in progress_bar:
            # Get batch
            try:
                batch = next(data_iter)
            except StopIteration:
                data_iter = iter(self.train_loader)
                batch = next(data_iter)

            # Move batch to device
            batch = self._move_batch_to_device(batch)

            # Forward pass
            self.optimizer.zero_grad()

            # Separate labels from input for forward pass
            labels = batch.pop('labels', None)
            if labels is None:
                labels = batch.pop('label', None)

            outputs = self.model(**batch)

            # Compute loss
            if hasattr(self.model, 'get_loss'):
                loss = self.model.get_loss(outputs, labels if labels is not None else batch.get('label'))
            else:
                if labels is not None:
                    loss = nn.CrossEntropyLoss()(outputs, labels)
                elif 'label' in batch:
                    loss = nn.CrossEntropyLoss()(outputs, batch['label'])
                else:
                    loss = outputs.mean()

            # Backward pass
            loss.backward()

            # Gradient accumulation
            if (iteration + 1) % self.accumulation_steps == 0:
                self.optimizer.step()
                self.optimizer.zero_grad()

            # Store results
            current_lr = self.optimizer.param_groups[0]['lr']
            self.lrs.append(current_lr)
            self.losses.append(loss.item())

            # Update best loss
            if loss.item() < self.best_loss:
                self.best_loss = loss.item()

            # Check for divergence
            if loss.item() > self.best_loss * self.diverge_thresh:
                self.logger.warning(f"Loss diverged at iteration {iteration}")
                self.diverged = True
                break

            # Update learning rate
            if iteration < self.num_iter - 1:
                if self.step_mode == "exp":
                    new_lr = current_lr * self.lr_mult
                else:
                    new_lr = current_lr + self.lr_mult
                self._set_lr(new_lr)

            # Update progress bar
            progress_bar.set_postfix({
                'lr': f"{current_lr:.2e}",
                'loss': f"{loss.item():.4f}",
                'best_loss': f"{self.best_loss:.4f}"
            })

        # Restore original learning rates
        self._restore_lrs()

        self.logger.info("Learning rate range test completed!")
        return self.lrs, self.losses

    def _set_lr(self, lr: float):
        """Set learning rate for all parameter groups."""
        for param_group in self.optimizer.param_groups:
            param_group['lr'] = lr

    def _restore_lrs(self):
        """Restore original learning rates."""
        for param_group, original_lr in zip(self.optimizer.param_groups, self.original_lrs):
            param_group['lr'] = original_lr

    def _move_batch_to_device(self, batch: Dict[str, torch.Tensor]) -> Dict[str, torch.Tensor]:
        """Move batch tensors to device."""
        return {k: v.to(self.device) if isinstance(v, torch.Tensor) else v for k, v in batch.items()}

    def plot(self, skip_start: int = 10, skip_end: int = 5, log_lr: bool = True) -> plt.Figure:
        """
        Plot the learning rate range test results.

        Args:
            skip_start: Number of iterations to skip at the start
            skip_end: Number of iterations to skip at the end
            log_lr: Whether to use log scale for learning rate

        Returns:
            Matplotlib figure
        """
        if len(self.lrs) == 0:
            raise ValueError("No data to plot. Run range_test() first.")

        # Skip iterations
        lrs = self.lrs[skip_start:-skip_end]
        losses = self.losses[skip_start:-skip_end]

        # Create plot
        fig, ax = plt.subplots(figsize=(10, 6))

        if log_lr:
            ax.semilogx(lrs, losses)
            ax.set_xlabel('Learning Rate')
        else:
            ax.plot(lrs, losses)
            ax.set_xlabel('Learning Rate')

        ax.set_ylabel('Loss')
        ax.set_title('Learning Rate Range Test')
        ax.grid(True, alpha=0.3)

        # Add annotations
        min_loss_idx = np.argmin(losses)
        ax.axvline(lrs[min_loss_idx], color='red', linestyle='--', alpha=0.5, label=f'Min Loss: {lrs[min_loss_idx]:.2e}')

        # Find steepest gradient (good learning rate)
        if len(losses) > 1:
            gradients = np.gradient(losses)
            steepest_idx = np.argmin(gradients)
            ax.axvline(lrs[steepest_idx], color='green', linestyle='--', alpha=0.5, label=f'Steepest: {lrs[steepest_idx]:.2e}')

        ax.legend()

        return fig

    def suggest(self, skip_start: int = 10, skip_end: int = 5) -> Dict[str, float]:
        """
        Suggest learning rates based on the range test.

        Args:
            skip_start: Number of iterations to skip at the start
            skip_end: Number of iterations to skip at the end

        Returns:
            Dictionary with suggested learning rates
        """
        if len(self.lrs) == 0:
            raise ValueError("No data available. Run range_test() first.")

        # Skip iterations
        lrs = self.lrs[skip_start:-skip_end]
        losses = self.losses[skip_start:-skip_end]

        if len(lrs) == 0:
            raise ValueError("No data after skipping iterations.")

        # Find minimum loss learning rate
        min_loss_idx = np.argmin(losses)
        min_loss_lr = lrs[min_loss_idx]

        # Find steepest gradient (good learning rate)
        if len(losses) > 1:
            gradients = np.gradient(losses)
            steepest_idx = np.argmin(gradients)
            steepest_lr = lrs[steepest_idx]
        else:
            steepest_lr = min_loss_lr

        # Suggest learning rates
        suggestions = {
            'min_loss_lr': min_loss_lr,
            'steepest_lr': steepest_lr,
            'suggested_lr': steepest_lr / 10,  # Conservative choice
            'max_lr': steepest_lr,
            'min_lr': steepest_lr / 100
        }

        self.logger.info("Learning rate suggestions:")
        for key, value in suggestions.items():
            self.logger.info(f"  {key}: {value:.2e}")

        return suggestions


def find_lr(
    model: nn.Module,
    train_loader: DataLoader,
    optimizer: torch.optim.Optimizer,
    device: torch.device,
    start_lr: float = 1e-7,
    end_lr: float = 10.0,
    num_iter: int = 100,
    plot: bool = True,
    save_plot: Optional[str] = None
) -> Dict[str, float]:
    """
    Convenience function to find optimal learning rate.

    Args:
        model: Model to train
        train_loader: Training data loader
        optimizer: Optimizer to use
        device: Device to train on
        start_lr: Starting learning rate
        end_lr: Ending learning rate
        num_iter: Number of iterations to run
        plot: Whether to show the plot
        save_plot: Path to save the plot (optional)

    Returns:
        Dictionary with suggested learning rates
    """
    lr_finder = LRFinder(
        model=model,
        train_loader=train_loader,
        optimizer=optimizer,
        device=device,
        start_lr=start_lr,
        end_lr=end_lr,
        num_iter=num_iter
    )

    # Run the range test
    lrs, losses = lr_finder.range_test()

    # Get suggestions
    suggestions = lr_finder.suggest()

    # Plot if requested
    if plot or save_plot:
        fig = lr_finder.plot()
        if save_plot:
            fig.savefig(save_plot, dpi=300, bbox_inches='tight')
        if plot:
            plt.show()
        plt.close(fig)

    return suggestions
