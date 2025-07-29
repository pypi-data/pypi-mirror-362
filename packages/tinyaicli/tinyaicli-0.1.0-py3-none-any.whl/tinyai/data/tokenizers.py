"""
Tokenizer implementation for Tiny AI.

This module provides a simple tokenizer for text processing,
suitable for training language models.
"""

import re
from typing import List, Dict, Optional
from collections import Counter


class Tokenizer:
    """
    Simple tokenizer for text processing.

    This tokenizer implements basic word-level tokenization
    with vocabulary building capabilities.
    """

    def __init__(self, vocab_size: int = 10000):
        """
        Initialize the tokenizer.

        Args:
            vocab_size: Maximum vocabulary size
        """
        self.vocab_size = vocab_size
        self.word_to_id = {}
        self.id_to_word = {}
        self.unk_token_id = 0
        self.pad_token_id = 1
        self.eos_token_id = 2
        self.bos_token_id = 3

        # Initialize special tokens
        self.word_to_id['<UNK>'] = self.unk_token_id
        self.word_to_id['<PAD>'] = self.pad_token_id
        self.word_to_id['<EOS>'] = self.eos_token_id
        self.word_to_id['<BOS>'] = self.bos_token_id

        self.id_to_word[self.unk_token_id] = '<UNK>'
        self.id_to_word[self.pad_token_id] = '<PAD>'
        self.id_to_word[self.eos_token_id] = '<EOS>'
        self.id_to_word[self.bos_token_id] = '<BOS>'

    def fit(self, texts: List[str]):
        """
        Build vocabulary from a list of texts.

        Args:
            texts: List of text strings
        """
        # Tokenize all texts
        all_tokens = []
        for text in texts:
            tokens = self._tokenize(text)
            all_tokens.extend(tokens)

        # Count word frequencies
        word_counts = Counter(all_tokens)

        # Build vocabulary (excluding special tokens)
        vocab_words = ['<UNK>', '<PAD>', '<EOS>', '<BOS>']
        vocab_words.extend([word for word, _ in word_counts.most_common(self.vocab_size - 4)])

        # Create mappings
        for i, word in enumerate(vocab_words):
            self.word_to_id[word] = i
            self.id_to_word[i] = word

    def _tokenize(self, text: str) -> List[str]:
        """
        Tokenize a single text string.

        Args:
            text: Input text string

        Returns:
            List of tokens
        """
        # Convert to lowercase and split on whitespace
        text = text.lower()
        tokens = re.findall(r'\b\w+\b', text)
        return tokens

    def encode(self, text: str) -> List[int]:
        """
        Encode text to token IDs.

        Args:
            text: Input text string

        Returns:
            List of token IDs
        """
        tokens = self._tokenize(text)
        token_ids = []

        for token in tokens:
            if token in self.word_to_id:
                token_ids.append(self.word_to_id[token])
            else:
                token_ids.append(self.unk_token_id)

        return token_ids

    def decode(self, token_ids: List[int]) -> str:
        """
        Decode token IDs back to text.

        Args:
            token_ids: List of token IDs

        Returns:
            Decoded text string
        """
        tokens = []
        for token_id in token_ids:
            if token_id in self.id_to_word:
                token = self.id_to_word[token_id]
                if token not in ['<UNK>', '<PAD>', '<EOS>', '<BOS>']:
                    tokens.append(token)

        return ' '.join(tokens)

    def encode_batch(self, texts: List[str], max_length: Optional[int] = None) -> List[List[int]]:
        """
        Encode a batch of texts.

        Args:
            texts: List of text strings
            max_length: Maximum sequence length (None for no padding)

        Returns:
            List of token ID sequences
        """
        encoded = [self.encode(text) for text in texts]

        if max_length is not None:
            # Pad or truncate sequences
            for i in range(len(encoded)):
                if len(encoded[i]) > max_length:
                    encoded[i] = encoded[i][:max_length]
                elif len(encoded[i]) < max_length:
                    encoded[i].extend([self.pad_token_id] * (max_length - len(encoded[i])))

        return encoded

    def get_vocab_size(self) -> int:
        """Get the vocabulary size."""
        return len(self.word_to_id)

    def save(self, path: str):
        """
        Save the tokenizer to disk.

        Args:
            path: Path to save the tokenizer
        """
        import json
        data = {
            'vocab_size': self.vocab_size,
            'word_to_id': self.word_to_id,
            'id_to_word': {int(k): v for k, v in self.id_to_word.items()},
            'unk_token_id': self.unk_token_id,
            'pad_token_id': self.pad_token_id,
            'eos_token_id': self.eos_token_id,
            'bos_token_id': self.bos_token_id,
        }

        with open(path, 'w') as f:
            json.dump(data, f, indent=2)

    def load(self, path: str):
        """
        Load the tokenizer from disk.

        Args:
            path: Path to load the tokenizer from
        """
        import json
        with open(path, 'r') as f:
            data = json.load(f)

        self.vocab_size = data['vocab_size']
        self.word_to_id = data['word_to_id']
        self.id_to_word = {int(k): v for k, v in data['id_to_word'].items()}
        self.unk_token_id = data['unk_token_id']
        self.pad_token_id = data['pad_token_id']
        self.eos_token_id = data['eos_token_id']
        self.bos_token_id = data['bos_token_id']


class SimpleTokenizer(Tokenizer):
    """
    Simple character-level tokenizer for demonstration.

    This tokenizer treats each character as a token,
    useful for simple language modeling tasks.
    """

    def __init__(self, vocab_size: int = 256):
        """
        Initialize the simple tokenizer.

        Args:
            vocab_size: Maximum vocabulary size (default 256 for ASCII)
        """
        super().__init__(vocab_size)

    def _tokenize(self, text: str) -> List[str]:
        """
        Tokenize text into characters.

        Args:
            text: Input text string

        Returns:
            List of characters
        """
        return list(text)

    def fit(self, texts: List[str]):
        """
        Build vocabulary from a list of texts.

        Args:
            texts: List of text strings
        """
        # Get all unique characters
        all_chars = set()
        for text in texts:
            all_chars.update(text)

        # Build vocabulary
        vocab_chars = ['<UNK>', '<PAD>', '<EOS>', '<BOS>']
        vocab_chars.extend(sorted(list(all_chars))[:self.vocab_size - 4])

        # Create mappings
        for i, char in enumerate(vocab_chars):
            self.word_to_id[char] = i
            self.id_to_word[i] = char
