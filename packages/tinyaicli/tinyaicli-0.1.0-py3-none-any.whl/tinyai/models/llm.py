"""
LLM model implementation for Tiny AI.

This module provides a transformer-based language model implementation
suitable for training small LLMs.
"""

import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Dict, Any, Optional

from .base import BaseModel


class MultiHeadAttention(nn.Module):
    """Multi-head attention mechanism."""

    def __init__(self, config: Dict[str, Any]):
        super().__init__()
        self.hidden_size = config['hidden_size']
        self.num_heads = config['num_heads']
        self.head_dim = self.hidden_size // self.num_heads

        assert self.hidden_size % self.num_heads == 0, "hidden_size must be divisible by num_heads"

        self.q_proj = nn.Linear(self.hidden_size, self.hidden_size)
        self.k_proj = nn.Linear(self.hidden_size, self.hidden_size)
        self.v_proj = nn.Linear(self.hidden_size, self.hidden_size)
        self.out_proj = nn.Linear(self.hidden_size, self.hidden_size)

        self.dropout = nn.Dropout(config.get("attention_dropout", 0.1))

    def forward(self, x, mask=None):
        batch_size, seq_len, hidden_size = x.shape

        # Project to Q, K, V
        q = self.q_proj(x).view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        k = self.k_proj(x).view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        v = self.v_proj(x).view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)

        # Compute attention scores
        scores = torch.matmul(q, k.transpose(-2, -1)) / math.sqrt(self.head_dim)

        if mask is not None:
            scores = scores.masked_fill(mask == 0, float('-inf'))

        attention_weights = F.softmax(scores, dim=-1)
        attention_weights = self.dropout(attention_weights)

        # Apply attention to values
        context = torch.matmul(attention_weights, v)
        context = context.transpose(1, 2).contiguous().view(batch_size, seq_len, self.hidden_size)

        return self.out_proj(context)


class TransformerBlock(nn.Module):
    """Transformer block with self-attention and feed-forward layers."""

    def __init__(self, config: Dict[str, Any]):
        super().__init__()
        self.hidden_size = config['hidden_size']
        self.ffn_size = config.get("ffn_size", 4 * config['hidden_size'])

        self.attention = MultiHeadAttention(config)
        self.attention_norm = nn.LayerNorm(self.hidden_size)

        self.ffn = nn.Sequential(
            nn.Linear(self.hidden_size, self.ffn_size),
            nn.GELU(),
            nn.Dropout(config.get("ffn_dropout", 0.1)),
            nn.Linear(self.ffn_size, self.hidden_size),
            nn.Dropout(config.get("ffn_dropout", 0.1))
        )
        self.ffn_norm = nn.LayerNorm(self.hidden_size)

    def forward(self, x, mask=None):
        # Self-attention with residual connection
        attn_out = self.attention(x, mask)
        x = self.attention_norm(x + attn_out)

        # Feed-forward with residual connection
        ffn_out = self.ffn(x)
        x = self.ffn_norm(x + ffn_out)

        return x


class LLMModel(BaseModel):
    """
    Transformer-based Language Model for Tiny AI Model Trainer.

    This model implements a GPT-style transformer architecture suitable
    for training small language models.
    """

    def __init__(self, config: Dict[str, Any], device: Optional[torch.device] = None):
        """
        Initialize the LLM model.

        Args:
            config: Model configuration
            device: Device to place the model on
        """
        super().__init__(config, device)

        # Model parameters
        self.vocab_size = config['vocab_size']
        self.hidden_size = config['hidden_size']
        self.num_layers = config['num_layers']
        self.max_length = config.get("max_length", 512)

        # Embeddings
        self.token_embedding = nn.Embedding(self.vocab_size, self.hidden_size)
        self.position_embedding = nn.Embedding(self.max_length, self.hidden_size)

        # Transformer blocks
        self.transformer_blocks = nn.ModuleList([
            TransformerBlock(config) for _ in range(self.num_layers)
        ])

        # Output layer
        self.output_norm = nn.LayerNorm(self.hidden_size)
        self.output_proj = nn.Linear(self.hidden_size, self.vocab_size, bias=False)

        # Initialize weights
        self.apply(self._init_weights)

    def _init_weights(self, module):
        """Initialize model weights."""
        if isinstance(module, nn.Linear):
            torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)
            if module.bias is not None:
                torch.nn.init.zeros_(module.bias)
        elif isinstance(module, nn.Embedding):
            torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)
        elif isinstance(module, nn.LayerNorm):
            torch.nn.init.zeros_(module.bias)
            torch.nn.init.ones_(module.weight)

    def forward(self, input_ids, attention_mask=None):
        """
        Forward pass of the model.

        Args:
            input_ids: Input token IDs [batch_size, seq_len]
            attention_mask: Attention mask [batch_size, seq_len]

        Returns:
            Logits [batch_size, seq_len, vocab_size]
        """
        batch_size, seq_len = input_ids.shape

        # Create position IDs
        position_ids = torch.arange(seq_len, device=input_ids.device).unsqueeze(0).expand(batch_size, -1)

        # Get embeddings
        token_embeddings = self.token_embedding(input_ids)
        position_embeddings = self.position_embedding(position_ids)
        embeddings = token_embeddings + position_embeddings

        # Create causal mask for autoregressive generation
        if attention_mask is None:
            attention_mask = torch.ones(batch_size, seq_len, device=input_ids.device)

        causal_mask = torch.triu(torch.ones(seq_len, seq_len, device=input_ids.device), diagonal=1)
        causal_mask = causal_mask.bool()

        # Apply transformer blocks
        hidden_states = embeddings
        for block in self.transformer_blocks:
            hidden_states = block(hidden_states, causal_mask)

        # Output projection
        hidden_states = self.output_norm(hidden_states)
        logits = self.output_proj(hidden_states)

        return logits

    def get_loss(self, outputs, targets):
        """
        Compute the language modeling loss.

        Args:
            outputs: Model outputs (logits)
            targets: Target token IDs

        Returns:
            Loss tensor
        """
        # Shift targets for next token prediction
        if targets.shape[1] == outputs.shape[1]:
            targets = targets[:, 1:]
            outputs = outputs[:, :-1, :]

        # Compute cross-entropy loss
        loss = F.cross_entropy(
            outputs.reshape(-1, self.vocab_size),
            targets.reshape(-1),
            ignore_index=-100
        )

        return loss

    def generate(self, input_ids, max_length=100, temperature=1.0, top_k=50, top_p=0.9):
        """
        Generate text using the model.

        Args:
            input_ids: Starting token IDs
            max_length: Maximum generation length
            temperature: Sampling temperature
            top_k: Top-k sampling parameter
            top_p: Top-p sampling parameter

        Returns:
            Generated token IDs
        """
        self.eval()
        with torch.no_grad():
            batch_size = input_ids.shape[0]
            generated = input_ids.clone()

            for _ in range(max_length - input_ids.shape[1]):
                # Get model predictions
                outputs = self.forward(generated)
                next_token_logits = outputs[:, -1, :] / temperature

                # Apply top-k filtering
                if top_k > 0:
                    top_k_logits, top_k_indices = torch.topk(next_token_logits, top_k)
                    next_token_logits = torch.full_like(next_token_logits, float('-inf'))
                    next_token_logits.scatter_(1, top_k_indices, top_k_logits)

                # Apply top-p filtering
                if top_p < 1.0:
                    sorted_logits, sorted_indices = torch.sort(next_token_logits, descending=True)
                    cumulative_probs = torch.cumsum(F.softmax(sorted_logits, dim=-1), dim=-1)
                    sorted_indices_to_remove = cumulative_probs > top_p
                    sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
                    sorted_indices_to_remove[..., 0] = 0
                    indices_to_remove = sorted_indices_to_remove.scatter(1, sorted_indices, sorted_indices_to_remove)
                    next_token_logits[indices_to_remove] = float('-inf')

                # Sample next token
                probs = F.softmax(next_token_logits, dim=-1)
                next_token = torch.multinomial(probs, num_samples=1)

                # Append to generated sequence
                generated = torch.cat([generated, next_token], dim=1)

                # Stop if all sequences have EOS token
                if (next_token == self.config.get("eos_token_id", 2)).all():
                    break

        return generated
