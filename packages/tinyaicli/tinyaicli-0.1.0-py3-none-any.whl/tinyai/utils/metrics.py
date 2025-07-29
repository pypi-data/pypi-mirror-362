"""
Metrics tracking utilities for Tiny AI.

This module provides utilities for tracking and computing
training and validation metrics.
"""

import time
from typing import Dict, List, Any, Optional
from collections import defaultdict
import numpy as np


class MetricsTracker:
    """
    Utility class for tracking training and validation metrics.

    This class provides methods for storing, computing, and retrieving
    various metrics during training.
    """

    def __init__(self):
        """Initialize the metrics tracker."""
        self.metrics = defaultdict(list)
        self.timestamps = defaultdict(list)
        self.start_time = time.time()

    def add_metric(self, name: str, value: float, step: Optional[int] = None):
        """
        Add a metric value.

        Args:
            name: Metric name
            value: Metric value
            step: Optional step number
        """
        self.metrics[name].append(value)
        self.timestamps[name].append(time.time() - self.start_time)

    def get_metric(self, name: str) -> List[float]:
        """
        Get all values for a metric.

        Args:
            name: Metric name

        Returns:
            List of metric values
        """
        return self.metrics.get(name, [])

    def get_latest_metric(self, name: str) -> Optional[float]:
        """
        Get the latest value for a metric.

        Args:
            name: Metric name

        Returns:
            Latest metric value or None
        """
        values = self.metrics.get(name, [])
        return values[-1] if values else None

    def get_best_metric(self, name: str, maximize: bool = True) -> Optional[float]:
        """
        Get the best value for a metric.

        Args:
            name: Metric name
            maximize: Whether to maximize (True) or minimize (False) the metric

        Returns:
            Best metric value or None
        """
        values = self.metrics.get(name, [])
        if not values:
            return None

        if maximize:
            return max(values)
        else:
            return min(values)

    def get_metric_stats(self, name: str) -> Dict[str, float]:
        """
        Get statistics for a metric.

        Args:
            name: Metric name

        Returns:
            Dictionary with metric statistics
        """
        values = self.metrics.get(name, [])
        if not values:
            return {}

        return {
            'mean': np.mean(values),
            'std': np.std(values),
            'min': np.min(values),
            'max': np.max(values),
            'latest': values[-1],
            'count': len(values)
        }

    def reset(self):
        """Reset all metrics."""
        self.metrics.clear()
        self.timestamps.clear()
        self.start_time = time.time()

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert metrics to dictionary.

        Returns:
            Dictionary representation of metrics
        """
        return {
            'metrics': dict(self.metrics),
            'timestamps': dict(self.timestamps),
            'start_time': self.start_time
        }


def compute_accuracy(predictions: np.ndarray, targets: np.ndarray) -> float:
    """
    Compute accuracy for classification tasks.

    Args:
        predictions: Predicted class labels
        targets: True class labels

    Returns:
        Accuracy score
    """
    return (predictions == targets).mean()


def compute_precision_recall_f1(predictions: np.ndarray, targets: np.ndarray, num_classes: int) -> Dict[str, float]:
    """
    Compute precision, recall, and F1 score for multi-class classification.

    Args:
        predictions: Predicted class labels
        targets: True class labels
        num_classes: Number of classes

    Returns:
        Dictionary with precision, recall, and F1 scores
    """
    from sklearn.metrics import precision_recall_fscore_support

    precision, recall, f1, _ = precision_recall_fscore_support(
        targets, predictions, average='weighted', zero_division=0
    )

    return {
        'precision': precision,
        'recall': recall,
        'f1': f1
    }


def compute_perplexity(loss: float) -> float:
    """
    Compute perplexity from cross-entropy loss.

    Args:
        loss: Cross-entropy loss

    Returns:
        Perplexity
    """
    return np.exp(loss)


def format_metric_value(value: float, metric_name: str) -> str:
    """
    Format a metric value for display.

    Args:
        value: Metric value
        metric_name: Metric name

    Returns:
        Formatted string
    """
    if metric_name in ['loss', 'perplexity']:
        return f"{value:.4f}"
    elif metric_name in ['accuracy', 'precision', 'recall', 'f1']:
        return f"{value:.4f}"
    elif metric_name in ['learning_rate']:
        return f"{value:.6f}"
    else:
        return f"{value:.4f}"


class EarlyStopping:
    """
    Early stopping utility to prevent overfitting.

    This class monitors a metric and stops training when the metric
    doesn't improve for a specified number of epochs.
    """

    def __init__(self, patience: int = 5, min_delta: float = 0.0, maximize: bool = True):
        """
        Initialize early stopping.

        Args:
            patience: Number of epochs to wait for improvement
            min_delta: Minimum change to qualify as improvement
            maximize: Whether to maximize (True) or minimize (False) the metric
        """
        self.patience = patience
        self.min_delta = min_delta
        self.maximize = maximize
        self.best_value = None
        self.counter = 0
        self.should_stop = False

    def __call__(self, value: float) -> bool:
        """
        Check if training should stop.

        Args:
            value: Current metric value

        Returns:
            True if training should stop
        """
        if self.best_value is None:
            self.best_value = value
            return False

        if self.maximize:
            improved = value > self.best_value + self.min_delta
        else:
            improved = value < self.best_value - self.min_delta

        if improved:
            self.best_value = value
            self.counter = 0
        else:
            self.counter += 1

        if self.counter >= self.patience:
            self.should_stop = True

        return self.should_stop

    def reset(self):
        """Reset the early stopping state."""
        self.best_value = None
        self.counter = 0
        self.should_stop = False
