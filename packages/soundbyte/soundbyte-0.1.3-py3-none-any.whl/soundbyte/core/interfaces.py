"""
Abstract interfaces for SoundByte components.

This module defines the abstract base classes that all SoundByte components
must implement to ensure consistent behavior across the framework.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple, Union
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torch.optim import Optimizer
from torch.optim.lr_scheduler import _LRScheduler


class SoundByteComponent(ABC):
    """Base interface for all SoundByte components."""

    @abstractmethod
    def get_config(self) -> Dict[str, Any]:
        """Return component configuration."""
        pass


class DataOps(SoundByteComponent):
    """Abstract interface for data operations (datasets)."""

    @abstractmethod
    def get_train_loader(self) -> DataLoader:
        """Return training data loader."""
        pass

    @abstractmethod
    def get_val_loader(self) -> DataLoader:
        """Return validation data loader."""
        pass

    @abstractmethod
    def get_test_loader(self) -> DataLoader:
        """Return test data loader."""
        pass

    @abstractmethod
    def get_num_classes(self) -> int:
        """Return number of classes."""
        pass


class ModelOps(SoundByteComponent):
    """Abstract interface for model operations (neural architectures)."""

    @abstractmethod
    def get_model(self) -> nn.Module:
        """Return the PyTorch model."""
        pass


class PenaltyOps(SoundByteComponent):
    """Abstract interface for penalty operations (loss functions)."""

    @abstractmethod
    def compute_loss(self, outputs: torch.Tensor, targets: torch.Tensor, **kwargs) -> torch.Tensor:
        """Compute loss given outputs and targets."""
        pass


class ControlOps(SoundByteComponent):
    """Abstract interface for control operations (optimizers)."""

    @abstractmethod
    def create_optimizer(self, model_parameters) -> Optimizer:
        """Create optimizer for given model parameters."""
        pass


class ScheduleOps(SoundByteComponent):
    """Abstract interface for schedule operations (learning rate schedulers)."""

    @abstractmethod
    def create_scheduler(self, optimizer: Optimizer) -> _LRScheduler:
        """Create scheduler for given optimizer."""
        pass


class TrainOps(SoundByteComponent):
    """Abstract interface for training operations."""

    @abstractmethod
    def train(self, model: nn.Module, data_ops: DataOps, control_ops: ControlOps, 
              penalty_ops: PenaltyOps, audit_ops: 'AuditOps', device: str,
              schedule_ops: Optional[ScheduleOps] = None, **kwargs) -> Dict[str, Any]:
        """Execute training process."""
        pass


class AuditOps(SoundByteComponent):
    """Abstract interface for audit operations (evaluation and metrics)."""

    @abstractmethod
    def evaluate(self, model: nn.Module, data_loader: DataLoader, 
                 penalty_ops: PenaltyOps, device: str) -> Dict[str, Any]:
        """Evaluate model on given data."""
        pass
