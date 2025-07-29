"""
Penalty operations components (loss functions) for SoundByte.

This module provides implementations of various loss functions
for different training paradigms.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Dict, Any, Optional

from ...core.interfaces import PenaltyOps
from ...plugins.registry import register


@register('penalty_ops', 'cross_entropy')
class CrossEntropyPenaltyOps(PenaltyOps):
    """Cross-entropy loss for classification."""

    def __init__(self, weight: Optional[torch.Tensor] = None, 
                 ignore_index: int = -100, reduction: str = 'mean', **kwargs):
        self.criterion = nn.CrossEntropyLoss(
            weight=weight, ignore_index=ignore_index, reduction=reduction
        )
        self.weight = weight
        self.ignore_index = ignore_index
        self.reduction = reduction

    def compute_loss(self, outputs: torch.Tensor, targets: torch.Tensor, **kwargs) -> torch.Tensor:
        """Compute cross-entropy loss."""
        return self.criterion(outputs, targets)

    def get_config(self) -> Dict[str, Any]:
        """Return configuration."""
        return {
            'weight': self.weight,
            'ignore_index': self.ignore_index,
            'reduction': self.reduction
        }


@register('penalty_ops', 'focal_loss')
class FocalPenaltyOps(PenaltyOps):
    """Focal loss for addressing class imbalance."""

    def __init__(self, alpha: float = 1.0, gamma: float = 2.0, 
                 reduction: str = 'mean', **kwargs):
        self.alpha = alpha
        self.gamma = gamma
        self.reduction = reduction

    def compute_loss(self, outputs: torch.Tensor, targets: torch.Tensor, **kwargs) -> torch.Tensor:
        """Compute focal loss."""
        ce_loss = F.cross_entropy(outputs, targets, reduction='none')
        pt = torch.exp(-ce_loss)
        focal_loss = self.alpha * (1 - pt) ** self.gamma * ce_loss

        if self.reduction == 'mean':
            return focal_loss.mean()
        elif self.reduction == 'sum':
            return focal_loss.sum()
        else:
            return focal_loss

    def get_config(self) -> Dict[str, Any]:
        """Return configuration."""
        return {
            'alpha': self.alpha,
            'gamma': self.gamma,
            'reduction': self.reduction
        }


@register('penalty_ops', 'label_smoothing')
class LabelSmoothingPenaltyOps(PenaltyOps):
    """Cross-entropy loss with label smoothing."""

    def __init__(self, smoothing: float = 0.1, **kwargs):
        self.smoothing = smoothing

    def compute_loss(self, outputs: torch.Tensor, targets: torch.Tensor, **kwargs) -> torch.Tensor:
        """Compute label smoothing loss."""
        log_prob = F.log_softmax(outputs, dim=-1)
        nll_loss = -log_prob.gather(dim=-1, index=targets.unsqueeze(1))
        nll_loss = nll_loss.squeeze(1)
        smooth_loss = -log_prob.mean(dim=-1)
        loss = (1.0 - self.smoothing) * nll_loss + self.smoothing * smooth_loss
        return loss.mean()

    def get_config(self) -> Dict[str, Any]:
        """Return configuration."""
        return {'smoothing': self.smoothing}


@register('penalty_ops', 'knowledge_distillation')
class KnowledgeDistillationPenaltyOps(PenaltyOps):
    """Knowledge distillation loss combining hard and soft targets."""

    def __init__(self, temperature: float = 4.0, alpha: float = 0.5, **kwargs):
        self.temperature = temperature
        self.alpha = alpha
        self.hard_loss = nn.CrossEntropyLoss()

    def compute_loss(self, outputs: torch.Tensor, targets: torch.Tensor, 
                     teacher_outputs: Optional[torch.Tensor] = None, **kwargs) -> torch.Tensor:
        """
        Compute knowledge distillation loss.

        Args:
            outputs: Student model outputs
            targets: Ground truth labels
            teacher_outputs: Teacher model outputs (required for distillation)
        """
        if teacher_outputs is None:
            raise ValueError("Teacher outputs required for knowledge distillation loss")

        # Hard loss (student vs ground truth)
        hard_loss = self.hard_loss(outputs, targets)

        # Soft loss (student vs teacher)
        student_soft = F.log_softmax(outputs / self.temperature, dim=1)
        teacher_soft = F.softmax(teacher_outputs / self.temperature, dim=1)
        soft_loss = F.kl_div(student_soft, teacher_soft, reduction='batchmean')
        soft_loss = soft_loss * (self.temperature ** 2)

        # Combine losses
        total_loss = self.alpha * hard_loss + (1 - self.alpha) * soft_loss
        return total_loss

    def get_config(self) -> Dict[str, Any]:
        """Return configuration."""
        return {
            'temperature': self.temperature,
            'alpha': self.alpha
        }


@register('penalty_ops', 'mse_loss')
class MSEPenaltyOps(PenaltyOps):
    """Mean Squared Error loss for regression."""

    def __init__(self, reduction: str = 'mean', **kwargs):
        self.criterion = nn.MSELoss(reduction=reduction)
        self.reduction = reduction

    def compute_loss(self, outputs: torch.Tensor, targets: torch.Tensor, **kwargs) -> torch.Tensor:
        """Compute MSE loss."""
        return self.criterion(outputs, targets)

    def get_config(self) -> Dict[str, Any]:
        """Return configuration."""
        return {'reduction': self.reduction}


@register('penalty_ops', 'huber_loss')
class HuberPenaltyOps(PenaltyOps):
    """Huber loss for robust regression."""

    def __init__(self, delta: float = 1.0, reduction: str = 'mean', **kwargs):
        self.criterion = nn.HuberLoss(delta=delta, reduction=reduction)
        self.delta = delta
        self.reduction = reduction

    def compute_loss(self, outputs: torch.Tensor, targets: torch.Tensor, **kwargs) -> torch.Tensor:
        """Compute Huber loss."""
        return self.criterion(outputs, targets)

    def get_config(self) -> Dict[str, Any]:
        """Return configuration."""
        return {
            'delta': self.delta,
            'reduction': self.reduction
        }


@register('penalty_ops', 'bce_loss')
class BCEPenaltyOps(PenaltyOps):
    """Binary Cross-Entropy loss."""

    def __init__(self, weight: Optional[torch.Tensor] = None, 
                 reduction: str = 'mean', **kwargs):
        self.criterion = nn.BCELoss(weight=weight, reduction=reduction)
        self.weight = weight
        self.reduction = reduction

    def compute_loss(self, outputs: torch.Tensor, targets: torch.Tensor, **kwargs) -> torch.Tensor:
        """Compute BCE loss."""
        return self.criterion(outputs, targets)

    def get_config(self) -> Dict[str, Any]:
        """Return configuration."""
        return {
            'weight': self.weight,
            'reduction': self.reduction
        }


@register('penalty_ops', 'bce_with_logits')
class BCEWithLogitsPenaltyOps(PenaltyOps):
    """Binary Cross-Entropy with Logits loss."""

    def __init__(self, weight: Optional[torch.Tensor] = None,
                 pos_weight: Optional[torch.Tensor] = None,
                 reduction: str = 'mean', **kwargs):
        self.criterion = nn.BCEWithLogitsLoss(
            weight=weight, pos_weight=pos_weight, reduction=reduction
        )
        self.weight = weight
        self.pos_weight = pos_weight
        self.reduction = reduction

    def compute_loss(self, outputs: torch.Tensor, targets: torch.Tensor, **kwargs) -> torch.Tensor:
        """Compute BCE with logits loss."""
        return self.criterion(outputs, targets)

    def get_config(self) -> Dict[str, Any]:
        """Return configuration."""
        return {
            'weight': self.weight,
            'pos_weight': self.pos_weight,
            'reduction': self.reduction
        }
