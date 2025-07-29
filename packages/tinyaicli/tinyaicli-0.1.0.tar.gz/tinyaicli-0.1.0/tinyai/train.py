"""
Main training script for Tiny AI.

This module provides the CLI interface and orchestrates the training process
using Hydra for configuration management.
"""

import os
import sys
from pathlib import Path
from typing import Optional

import hydra
from hydra.core.config_store import ConfigStore
from omegaconf import DictConfig, OmegaConf
import torch
import wandb

from .models import get_model
from .data import get_data_loader
from .training import Trainer
from .utils.logging import setup_logging, get_logger
from .utils.metrics import MetricsTracker


@hydra.main(version_base=None, config_path="../configs", config_name="config")
def main(cfg: DictConfig) -> None:
    """
    Main training function with Hydra configuration.

    Args:
        cfg: Hydra configuration object
    """
    # Setup logging
    setup_logging(cfg.logging)
    logger = get_logger(__name__)

    logger.info("🚀 Starting Tiny AI Model Trainer")
    logger.info(f"Configuration:\n{OmegaConf.to_yaml(cfg)}")

    # Set random seeds for reproducibility
    if cfg.training.seed is not None:
        torch.manual_seed(cfg.training.seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed(cfg.training.seed)
            torch.cuda.manual_seed_all(cfg.training.seed)
        logger.info(f"Set random seed to {cfg.training.seed}")

    # Initialize wandb if enabled
    if cfg.logging.wandb:
        wandb.init(
            project=cfg.logging.project_name,
            name=cfg.logging.run_name,
            config=OmegaConf.to_container(cfg, resolve=True),
            tags=cfg.logging.tags if hasattr(cfg.logging, 'tags') else None,
        )
        logger.info(f"Initialized wandb run: {wandb.run.name}")

    try:
        # Get device
        device = torch.device(cfg.training.device if torch.cuda.is_available() else "cpu")
        logger.info(f"Using device: {device}")

        # Initialize model
        logger.info("📦 Initializing model...")
        model = get_model(cfg.model, device=device)
        logger.info(f"Model initialized: {model.__class__.__name__}")

        # Get data loaders
        logger.info("📊 Setting up data loaders...")
        
        # Auto-configure data type based on model type
        data_config = OmegaConf.to_container(cfg.data, resolve=True)
        if cfg.model.type.lower() in ["vision", "cnn", "resnet"]:
            data_config["type"] = "image"
            # Copy vision-specific parameters from model config if available
            if hasattr(cfg.model, 'num_classes'):
                data_config["num_classes"] = cfg.model.num_classes
            if hasattr(cfg.model, 'image_size'):
                data_config["image_size"] = cfg.model.image_size
            logger.info("Auto-configured data type to 'image' for vision model")
        elif cfg.model.type.lower() in ["llm", "transformer", "gpt"]:
            data_config["type"] = "text"
            # Copy LLM-specific parameters from model config if available
            if hasattr(cfg.model, 'vocab_size'):
                data_config["vocab_size"] = cfg.model.vocab_size
            if hasattr(cfg.model, 'max_length'):
                data_config["max_length"] = cfg.model.max_length
            logger.info("Auto-configured data type to 'text' for LLM model")
        
        # Copy training parameters to data config
        data_config["batch_size"] = cfg.training.batch_size
        if hasattr(cfg.training, 'num_workers'):
            data_config["num_workers"] = cfg.training.num_workers
        
        train_loader = get_data_loader(data_config, split="train")
        val_loader = get_data_loader(data_config, split="val")
        logger.info(f"Train samples: {len(train_loader.dataset)}")
        logger.info(f"Val samples: {len(val_loader.dataset)}")

        # Initialize metrics tracker
        metrics_tracker = MetricsTracker()

        # Initialize trainer
        logger.info("🏋️ Initializing trainer...")
        trainer = Trainer(
            model=model,
            train_loader=train_loader,
            val_loader=val_loader,
            config=cfg.training,
            device=device,
            metrics_tracker=metrics_tracker,
        )

        # Start training
        logger.info("🎯 Starting training...")
        trainer.train()

        # Save final model
        if cfg.training.save_model:
            save_path = Path(cfg.training.save_path)
            save_path.parent.mkdir(parents=True, exist_ok=True)
            trainer.save_model(save_path)
            logger.info(f"Model saved to: {save_path}")

        logger.info("✅ Training completed successfully!")

    except Exception as e:
        logger.error(f"❌ Training failed: {str(e)}")
        raise
    finally:
        if cfg.logging.wandb and wandb.run is not None:
            wandb.finish()


if __name__ == "__main__":
    main()
