"""
Main trainer class for Tiny AI.

This module provides the core training loop and utilities for
training both LLMs and vision models.
"""

import time
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from typing import Dict, Any, Optional
from tqdm import tqdm
import wandb

from .optimizer import get_optimizer, get_scheduler
from ..utils.logging import get_logger
from ..utils.metrics import MetricsTracker


class Trainer:
    """
    Main trainer class for Tiny AI Model Trainer.

    This class handles the training loop, validation, and logging
    for both LLMs and vision models.
    """

    def __init__(
        self,
        model: nn.Module,
        train_loader: DataLoader,
        val_loader: DataLoader,
        config: Dict[str, Any],
        device: torch.device,
        metrics_tracker: Optional[MetricsTracker] = None
    ):
        """
        Initialize the trainer.

        Args:
            model: Model to train
            train_loader: Training data loader
            val_loader: Validation data loader
            config: Training configuration
            device: Device to train on
            metrics_tracker: Optional metrics tracker
        """
        self.model = model
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.config = config
        self.device = device
        self.metrics_tracker = metrics_tracker or MetricsTracker()

        self.logger = get_logger(__name__)

        # Initialize optimizer and scheduler
        self.optimizer = get_optimizer(model, config)
        self.scheduler = get_scheduler(self.optimizer, config)

        # Training state
        self.current_epoch = 0
        self.global_step = 0
        self.best_val_loss = float('inf')

        # Mixed precision training
        self.use_amp = config.get('use_amp', False)

        # Log data loader info
        self.logger.info(f"Training data loader: {len(self.train_loader)} batches")
        self.logger.info(f"Validation data loader: {len(self.val_loader)} batches")
        
        # Log model info
        self.logger.info(f"Model parameters: {model.get_num_parameters():,}")
        self.logger.info(f"Trainable parameters: {model.get_trainable_parameters():,}")
        if self.use_amp:
            self.logger.info("Mixed precision training enabled")
        else:
            self.logger.info("Standard precision training")
        
        # Validate data loaders
        if len(self.train_loader) == 0:
            raise ValueError("Training data loader is empty! Check your data configuration.")
        if len(self.val_loader) == 0:
            raise ValueError("Validation data loader is empty! Check your data configuration.")

    def train(self):
        """Main training loop."""
        self.logger.info("Starting training...")

        for epoch in range(self.config.get('num_epochs', 10)):
            self.current_epoch = epoch

            # Training phase
            train_loss = self._train_epoch()

            # Validation phase
            val_loss, val_metrics = self._validate_epoch()

            # Update learning rate
            if self.scheduler:
                self.scheduler.step()

            # Log metrics
            self._log_metrics(train_loss, val_loss, val_metrics)

            # Save best model
            if val_loss < self.best_val_loss:
                self.best_val_loss = val_loss
                if self.config.get('save_best', False):
                    self.save_model(self.config.get('best_model_path', 'best_model.pt'))

            # Save checkpoint
            if self.config.get('save_checkpoints', False) and (epoch + 1) % self.config.get('checkpoint_interval', 1) == 0:
                self.save_checkpoint(f"checkpoint_epoch_{epoch + 1}.pt")

        self.logger.info("Training completed!")

    def _train_epoch(self) -> float:
        """Train for one epoch."""
        self.model.train()
        total_loss = 0.0
        num_batches = len(self.train_loader)
        
        # Check if data loader is empty
        if num_batches == 0:
            self.logger.warning("Training data loader is empty")
            return 0.0
        
        progress_bar = tqdm(
            self.train_loader,
            desc=f"Epoch {self.current_epoch + 1}",
            leave=False
        )

        for batch_idx, batch in enumerate(progress_bar):
            # Move batch to device
            batch = self._move_batch_to_device(batch)

            # Forward pass
            self.optimizer.zero_grad()

            # Separate inputs from labels
            labels = batch.pop('labels', None)
            if labels is None:
                labels = batch.pop('label', None)

            # Forward pass based on model type
            # Check model type rather than just batch contents
            if hasattr(self.model, '__class__') and 'LLM' in self.model.__class__.__name__:
                # LLM model - expect input_ids and attention_mask
                if 'input_ids' in batch and 'attention_mask' in batch:
                    outputs = self.model(input_ids=batch['input_ids'], attention_mask=batch['attention_mask'])
                else:
                    raise ValueError(f"LLM model expects 'input_ids' and 'attention_mask' but got: {batch.keys()}")
            elif hasattr(self.model, '__class__') and 'Vision' in self.model.__class__.__name__:
                # Vision model - expect image
                if 'image' in batch:
                    outputs = self.model(image=batch['image'])
                else:
                    raise ValueError(f"Vision model expects 'image' but got: {batch.keys()}")
            else:
                # Generic model call - fallback for unknown models
                outputs = self.model(**batch)

            # Compute loss
            if hasattr(self.model, 'get_loss'):
                loss = self.model.get_loss(outputs, labels)
            else:
                # Default loss computation
                if labels is not None:
                    loss = nn.CrossEntropyLoss()(outputs, labels)
                else:
                    loss = outputs.mean()  # Fallback

            # Backward pass
            loss.backward()

            # Gradient clipping
            if self.config.get('gradient_clip', 0) > 0:
                torch.nn.utils.clip_grad_norm_(self.model.parameters(), self.config.get('gradient_clip', 1.0))

            # Optimizer step
            self.optimizer.step()

            # Update metrics
            total_loss += loss.item()
            self.global_step += 1

            # Update progress bar
            progress_bar.set_postfix({
                'loss': f"{loss.item():.4f}",
                'lr': f"{self.optimizer.param_groups[0]['lr']:.6f}"
            })

            # Log to wandb
            if wandb.run is not None and self.global_step % self.config.get('log_interval', 10) == 0:
                wandb.log({
                    'train/loss': loss.item(),
                    'train/learning_rate': self.optimizer.param_groups[0]['lr'],
                    'train/step': self.global_step
                })

        return total_loss / num_batches

    def _validate_epoch(self) -> tuple[float, Dict[str, float]]:
        """Validate for one epoch."""
        self.model.eval()
        total_loss = 0.0
        all_predictions = []
        all_targets = []
        
        # Check if validation data loader is empty
        if len(self.val_loader) == 0:
            self.logger.warning("Validation data loader is empty")
            return 0.0, {}
        
        with torch.no_grad():
            for batch in tqdm(self.val_loader, desc="Validation", leave=False):
                # Move batch to device
                batch = self._move_batch_to_device(batch)

                # Forward pass
                # Separate inputs from labels
                labels = batch.pop('labels', None)
                if labels is None:
                    labels = batch.pop('label', None)
                # Check model type rather than just batch contents
                if hasattr(self.model, '__class__') and 'LLM' in self.model.__class__.__name__:
                    # LLM model - expect input_ids and attention_mask
                    if 'input_ids' in batch and 'attention_mask' in batch:
                        outputs = self.model(input_ids=batch['input_ids'], attention_mask=batch['attention_mask'])
                    else:
                        raise ValueError(f"LLM model expects 'input_ids' and 'attention_mask' but got: {batch.keys()}")
                elif hasattr(self.model, '__class__') and 'Vision' in self.model.__class__.__name__:
                    # Vision model - expect image
                    if 'image' in batch:
                        outputs = self.model(image=batch['image'])
                    else:
                        raise ValueError(f"Vision model expects 'image' but got: {batch.keys()}")
                else:
                    # Generic model call - fallback for unknown models
                    outputs = self.model(**batch)

                # Compute loss
                if hasattr(self.model, 'get_loss'):
                    loss = self.model.get_loss(outputs, labels)
                else:
                    if labels is not None:
                        loss = nn.CrossEntropyLoss()(outputs, labels)
                    else:
                        loss = outputs.mean()

                total_loss += loss.item()

                # Collect predictions and targets for metrics
                if labels is not None:
                    if hasattr(self.model, 'get_predictions'):
                        predictions = self.model.get_predictions(outputs)
                    else:
                        # Handle different output shapes
                        if len(outputs.shape) == 3:  # [batch, seq_len, vocab_size]
                            predictions = torch.argmax(outputs, dim=-1)  # [batch, seq_len]
                        else:  # [batch, num_classes]
                            predictions = torch.argmax(outputs, dim=1)  # [batch]

                    all_predictions.append(predictions.cpu())
                    all_targets.append(labels.cpu())

        # Compute metrics
        val_loss = total_loss / len(self.val_loader)
        metrics = {}

        if all_predictions and all_targets:
            all_predictions = torch.cat(all_predictions)
            all_targets = torch.cat(all_targets)

            # Compute accuracy
            accuracy = (all_predictions == all_targets).float().mean().item()
            metrics['accuracy'] = accuracy

        return val_loss, metrics

    def _move_batch_to_device(self, batch: Dict[str, torch.Tensor]) -> Dict[str, torch.Tensor]:
        """Move batch tensors to device."""
        return {k: v.to(self.device) if isinstance(v, torch.Tensor) else v for k, v in batch.items()}

    def _log_metrics(self, train_loss: float, val_loss: float, val_metrics: Dict[str, float]):
        """Log training and validation metrics."""
        # Log to console
        self.logger.info(
            f"Epoch {self.current_epoch + 1}: "
            f"Train Loss: {train_loss:.4f}, "
            f"Val Loss: {val_loss:.4f}"
        )

        if val_metrics:
            for metric_name, metric_value in val_metrics.items():
                self.logger.info(f"  {metric_name}: {metric_value:.4f}")

        # Log to wandb
        if wandb.run is not None:
            log_dict = {
                'epoch': self.current_epoch + 1,
                'train/epoch_loss': train_loss,
                'val/epoch_loss': val_loss,
            }
            log_dict.update({f'val/{k}': v for k, v in val_metrics.items()})
            wandb.log(log_dict)

    def save_model(self, path: str):
        """Save the model to disk."""
        if hasattr(self.model, 'save'):
            self.model.save(path)
        else:
            torch.save({
                'model_state_dict': self.model.state_dict(),
                'optimizer_state_dict': self.optimizer.state_dict(),
                'config': self.config,
                'epoch': self.current_epoch,
                'global_step': self.global_step,
                'best_val_loss': self.best_val_loss,
            }, path)

        self.logger.info(f"Model saved to: {path}")

    def save_checkpoint(self, path: str):
        """Save a training checkpoint."""
        checkpoint = {
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'scheduler_state_dict': self.scheduler.state_dict() if self.scheduler else None,
            'config': self.config,
            'epoch': self.current_epoch,
            'global_step': self.global_step,
            'best_val_loss': self.best_val_loss,
        }

        torch.save(checkpoint, path)
        self.logger.info(f"Checkpoint saved to: {path}")

    def load_checkpoint(self, path: str):
        """Load a training checkpoint."""
        checkpoint = torch.load(path, map_location=self.device)

        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])

        if self.scheduler and checkpoint['scheduler_state_dict']:
            self.scheduler.load_state_dict(checkpoint['scheduler_state_dict'])

        self.current_epoch = checkpoint['epoch']
        self.global_step = checkpoint['global_step']
        self.best_val_loss = checkpoint['best_val_loss']

        self.logger.info(f"Checkpoint loaded from: {path}")
        self.logger.info(f"Resuming from epoch {self.current_epoch + 1}, step {self.global_step}")
