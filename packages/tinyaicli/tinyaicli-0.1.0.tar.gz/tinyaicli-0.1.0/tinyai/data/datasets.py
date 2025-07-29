"""
Dataset implementations for Tiny AI.

This module provides dataset classes for text and image data,
supporting both language modeling and image classification tasks.
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

import torch
from torch.utils.data import Dataset
from PIL import Image
import numpy as np


class TextDataset(Dataset):
    """
    Dataset for text data suitable for language modeling.

    This dataset loads text files and tokenizes them for training
    language models.
    """

    def __init__(self, data_path: str, tokenizer, max_length: int = 512, stride: int = 256):
        """
        Initialize the text dataset.

        Args:
            data_path: Path to the text file
            tokenizer: Tokenizer instance
            max_length: Maximum sequence length
            stride: Stride for sliding window
        """
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.stride = stride

        # Load text data
        with open(data_path, 'r', encoding='utf-8') as f:
            self.text = f.read()

        # Tokenize the entire text
        self.tokens = self.tokenizer.encode(self.text)

        # Create sliding windows
        self.examples = []
        for i in range(0, len(self.tokens) - max_length + 1, stride):
            self.examples.append(self.tokens[i:i + max_length])

    def __len__(self) -> int:
        return len(self.examples)

    def __getitem__(self, idx: int) -> Dict[str, torch.Tensor]:
        tokens = self.examples[idx]

        return {
            'input_ids': torch.tensor(tokens, dtype=torch.long),
            'attention_mask': torch.ones(len(tokens), dtype=torch.long),
            'labels': torch.tensor(tokens, dtype=torch.long)
        }


class ImageDataset(Dataset):
    """
    Dataset for image data suitable for image classification.

    This dataset loads images and their labels for training
    vision models.
    """

    def __init__(self, data_path: str, transform=None, label_file: Optional[str] = None):
        """
        Initialize the image dataset.

        Args:
            data_path: Path to the image directory or file
            transform: Image transformations
            label_file: Optional path to label file
        """
        self.transform = transform
        self.data_path = Path(data_path)

        # Load image paths and labels
        if self.data_path.is_file():
            # Single file
            self.image_paths = [self.data_path]
            self.labels = [0]  # Default label
        elif self.data_path.is_dir():
            # Directory with images
            self.image_paths = list(self.data_path.glob("*.jpg")) + list(self.data_path.glob("*.png"))
            self.labels = [0] * len(self.image_paths)  # Default labels

            # Load labels if provided
            if label_file and os.path.exists(label_file):
                with open(label_file, 'r') as f:
                    label_data = json.load(f)
                    for i, img_path in enumerate(self.image_paths):
                        img_name = img_path.name
                        if img_name in label_data:
                            self.labels[i] = label_data[img_name]
        else:
            raise ValueError(f"Invalid data path: {data_path}")

    def __len__(self) -> int:
        return len(self.image_paths)

    def __getitem__(self, idx: int) -> Dict[str, torch.Tensor]:
        # Load image
        img_path = self.image_paths[idx]
        image = Image.open(img_path).convert('RGB')

        # Apply transformations
        if self.transform:
            image = self.transform(image)

        # Get label
        label = self.labels[idx]

        return {
            'image': image,
            'label': torch.tensor(label, dtype=torch.long)
        }


class SimpleTextDataset(Dataset):
    """
    Simple text dataset for demonstration purposes.

    This dataset creates synthetic text data for testing
    language model training.
    """

    def __init__(self, num_examples: int = 1000, max_length: int = 128, vocab_size: int = 1000):
        """
        Initialize the simple text dataset.

        Args:
            num_examples: Number of examples to generate
            max_length: Maximum sequence length
            vocab_size: Vocabulary size
        """
        self.num_examples = num_examples
        self.max_length = max_length
        self.vocab_size = vocab_size

        # Generate synthetic data
        self.examples = []
        for _ in range(num_examples):
            # Generate random token sequence
            tokens = torch.randint(0, vocab_size, (max_length,))
            self.examples.append(tokens)

    def __len__(self) -> int:
        return self.num_examples

    def __getitem__(self, idx: int) -> Dict[str, torch.Tensor]:
        tokens = self.examples[idx]

        return {
            'input_ids': tokens,
            'attention_mask': torch.ones_like(tokens),
            'labels': tokens.clone()
        }


class SimpleImageDataset(Dataset):
    """
    Simple image dataset for demonstration purposes.

    This dataset creates synthetic image data for testing
    vision model training.
    """

    def __init__(self, num_examples: int = 1000, image_size: int = 224, num_classes: int = 10):
        """
        Initialize the simple image dataset.

        Args:
            num_examples: Number of examples to generate
            image_size: Image size (assumed square)
            num_classes: Number of classes
        """
        self.num_examples = num_examples
        self.image_size = image_size
        self.num_classes = num_classes

        # Generate synthetic data
        self.images = []
        self.labels = []

        for _ in range(num_examples):
            # Generate random image
            image = torch.randn(3, image_size, image_size)
            label = torch.randint(0, num_classes, (1,))

            self.images.append(image)
            self.labels.append(label)

    def __len__(self) -> int:
        return self.num_examples

    def __getitem__(self, idx: int) -> Dict[str, torch.Tensor]:
        return {
            'image': self.images[idx],
            'label': self.labels[idx].squeeze()
        }
