"""
Data loader utilities for Tiny AI.

This module provides factory functions for creating data loaders
for different types of datasets and models.
"""

import torch
from torch.utils.data import DataLoader
from typing import Dict, Any, Optional

from .datasets import TextDataset, ImageDataset, SimpleTextDataset, SimpleImageDataset
from .tokenizers import Tokenizer, SimpleTokenizer


def get_data_loader(config: Dict[str, Any], split: str = "train") -> DataLoader:
    """
    Factory function to create a data loader based on configuration.

    Args:
        config: Data configuration
        split: Dataset split ("train" or "val")

    Returns:
        PyTorch DataLoader
    """
    data_type = config.get("type", "text").lower()

    if data_type in ["text", "llm"]:
        return _create_text_dataloader(config, split)
    elif data_type in ["image", "vision"]:
        return _create_image_dataloader(config, split)
    else:
        raise ValueError(f"Unknown data type: {data_type}")


def _create_text_dataloader(config: Dict[str, Any], split: str) -> DataLoader:
    """
    Create a text data loader for language modeling.

    Args:
        config: Data configuration
        split: Dataset split

    Returns:
        DataLoader for text data
    """
    # Get data path
    if split == "train":
        data_path = config.get("train_path")
    else:
        data_path = config.get("val_path")

    # Use synthetic data if no path provided
    if not data_path:
        dataset = SimpleTextDataset(
            num_examples=config.get("num_examples", 1000),
            max_length=config.get("max_length", 128),
            vocab_size=config.get("vocab_size", 1000)
        )
    else:
        # Create tokenizer
        tokenizer = SimpleTokenizer(vocab_size=config.get("vocab_size", 1000))

        # For simplicity, we'll use synthetic data for now
        # In a real implementation, you'd load and tokenize the actual text
        dataset = SimpleTextDataset(
            num_examples=config.get("num_examples", 1000),
            max_length=config.get("max_length", 128),
            vocab_size=config.get("vocab_size", 1000)
        )

    # Create data loader
    batch_size = config.get("batch_size", 32)
    
    # Ensure we don't drop all batches with small datasets
    drop_last = (split == "train") and len(dataset) > batch_size
    
    return DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=(split == "train"),
        num_workers=config.get("num_workers", 0),
        pin_memory=config.get("pin_memory", True),
        drop_last=drop_last
    )


def _create_image_dataloader(config: Dict[str, Any], split: str) -> DataLoader:
    """
    Create an image data loader for vision tasks.

    Args:
        config: Data configuration
        split: Dataset split

    Returns:
        DataLoader for image data
    """
    # Get data path
    if split == "train":
        data_path = config.get("train_path")
    else:
        data_path = config.get("val_path")

    # Use synthetic data if no path provided
    if not data_path:
        dataset = SimpleImageDataset(
            num_examples=config.get("num_examples", 1000),
            image_size=config.get("image_size", 224),
            num_classes=config.get("num_classes", 10)
        )
    else:
        # Create image transformations
        transform = _get_image_transforms(config, split)

        # Create dataset
        dataset = ImageDataset(
            data_path=data_path,
            transform=transform,
            label_file=config.get("label_file")
        )

    # Create data loader
    batch_size = config.get("batch_size", 32)
    
    # Ensure we don't drop all batches with small datasets
    drop_last = (split == "train") and len(dataset) > batch_size
    
    return DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=(split == "train"),
        num_workers=config.get("num_workers", 0),
        pin_memory=config.get("pin_memory", True),
        drop_last=drop_last
    )


def _get_image_transforms(config: Dict[str, Any], split: str):
    """
    Get image transformations for vision tasks.

    Args:
        config: Data configuration
        split: Dataset split

    Returns:
        Image transformations
    """
    from torchvision import transforms

    image_size = config.get("image_size", 224)

    if split == "train":
        # Training transforms with augmentation
        transform = transforms.Compose([
            transforms.Resize((image_size, image_size)),
            transforms.RandomHorizontalFlip(p=0.5),
            transforms.RandomRotation(degrees=10),
            transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
    else:
        # Validation transforms (no augmentation)
        transform = transforms.Compose([
            transforms.Resize((image_size, image_size)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

    return transform


def collate_fn_text(batch):
    """
    Custom collate function for text data.

    Args:
        batch: Batch of text examples

    Returns:
        Collated batch
    """
    # Extract input_ids, attention_mask, and labels
    input_ids = [item['input_ids'] for item in batch]
    attention_mask = [item['attention_mask'] for item in batch]
    labels = [item['labels'] for item in batch]

    # Pad sequences
    max_length = max(len(ids) for ids in input_ids)

    padded_input_ids = []
    padded_attention_mask = []
    padded_labels = []

    for ids, mask, label in zip(input_ids, attention_mask, labels):
        # Pad input_ids
        if len(ids) < max_length:
            padding_length = max_length - len(ids)
            ids = torch.cat([ids, torch.zeros(padding_length, dtype=ids.dtype)])
            mask = torch.cat([mask, torch.zeros(padding_length, dtype=mask.dtype)])
            label = torch.cat([label, torch.full((padding_length,), -100, dtype=label.dtype)])

        padded_input_ids.append(ids)
        padded_attention_mask.append(mask)
        padded_labels.append(label)

    return {
        'input_ids': torch.stack(padded_input_ids),
        'attention_mask': torch.stack(padded_attention_mask),
        'labels': torch.stack(padded_labels)
    }


def collate_fn_image(batch):
    """
    Custom collate function for image data.

    Args:
        batch: Batch of image examples

    Returns:
        Collated batch
    """
    images = [item['image'] for item in batch]
    labels = [item['label'] for item in batch]

    return {
        'image': torch.stack(images),
        'label': torch.stack(labels)
    }
