"""
Schedule operations components (learning rate schedulers) for SoundByte.

This module provides implementations of various learning rate scheduling
algorithms for adaptive training.
"""

import torch.optim.lr_scheduler as lr_scheduler
from torch.optim import Optimizer
from torch.optim.lr_scheduler import _LRScheduler
from typing import Dict, Any, List, Optional

from ...core.interfaces import ScheduleOps
from ...plugins.registry import register


@register('schedule_ops', 'step_lr')
class StepLRScheduleOps(ScheduleOps):
    """Step learning rate scheduler."""

    def __init__(self, step_size: int = 30, gamma: float = 0.1, **kwargs):
        self.step_size = step_size
        self.gamma = gamma

    def create_scheduler(self, optimizer: Optimizer) -> _LRScheduler:
        """Create step LR scheduler."""
        return lr_scheduler.StepLR(
            optimizer,
            step_size=self.step_size,
            gamma=self.gamma
        )

    def get_config(self) -> Dict[str, Any]:
        """Return configuration."""
        return {
            'step_size': self.step_size,
            'gamma': self.gamma
        }


@register('schedule_ops', 'multi_step_lr')
class MultiStepLRScheduleOps(ScheduleOps):
    """Multi-step learning rate scheduler."""

    def __init__(self, milestones: List[int], gamma: float = 0.1, **kwargs):
        self.milestones = milestones
        self.gamma = gamma

    def create_scheduler(self, optimizer: Optimizer) -> _LRScheduler:
        """Create multi-step LR scheduler."""
        return lr_scheduler.MultiStepLR(
            optimizer,
            milestones=self.milestones,
            gamma=self.gamma
        )

    def get_config(self) -> Dict[str, Any]:
        """Return configuration."""
        return {
            'milestones': self.milestones,
            'gamma': self.gamma
        }


@register('schedule_ops', 'exponential_lr')
class ExponentialLRScheduleOps(ScheduleOps):
    """Exponential learning rate scheduler."""

    def __init__(self, gamma: float = 0.95, **kwargs):
        self.gamma = gamma

    def create_scheduler(self, optimizer: Optimizer) -> _LRScheduler:
        """Create exponential LR scheduler."""
        return lr_scheduler.ExponentialLR(
            optimizer,
            gamma=self.gamma
        )

    def get_config(self) -> Dict[str, Any]:
        """Return configuration."""
        return {'gamma': self.gamma}


@register('schedule_ops', 'cosine_annealing_lr')
class CosineAnnealingLRScheduleOps(ScheduleOps):
    """Cosine annealing learning rate scheduler."""

    def __init__(self, T_max: int, eta_min: float = 0, **kwargs):
        self.T_max = T_max
        self.eta_min = eta_min

    def create_scheduler(self, optimizer: Optimizer) -> _LRScheduler:
        """Create cosine annealing LR scheduler."""
        return lr_scheduler.CosineAnnealingLR(
            optimizer,
            T_max=self.T_max,
            eta_min=self.eta_min
        )

    def get_config(self) -> Dict[str, Any]:
        """Return configuration."""
        return {
            'T_max': self.T_max,
            'eta_min': self.eta_min
        }


@register('schedule_ops', 'cosine_annealing_warm_restarts')
class CosineAnnealingWarmRestartsScheduleOps(ScheduleOps):
    """Cosine annealing with warm restarts scheduler."""

    def __init__(self, T_0: int, T_mult: int = 1, eta_min: float = 0, **kwargs):
        self.T_0 = T_0
        self.T_mult = T_mult
        self.eta_min = eta_min

    def create_scheduler(self, optimizer: Optimizer) -> _LRScheduler:
        """Create cosine annealing warm restarts scheduler."""
        return lr_scheduler.CosineAnnealingWarmRestarts(
            optimizer,
            T_0=self.T_0,
            T_mult=self.T_mult,
            eta_min=self.eta_min
        )

    def get_config(self) -> Dict[str, Any]:
        """Return configuration."""
        return {
            'T_0': self.T_0,
            'T_mult': self.T_mult,
            'eta_min': self.eta_min
        }


@register('schedule_ops', 'reduce_lr_on_plateau')
class ReduceLROnPlateauScheduleOps(ScheduleOps):
    """Reduce learning rate on plateau scheduler."""

    def __init__(self, mode: str = 'min', factor: float = 0.1, patience: int = 10,
                 threshold: float = 1e-4, threshold_mode: str = 'rel',
                 cooldown: int = 0, min_lr: float = 0, eps: float = 1e-8, **kwargs):
        self.mode = mode
        self.factor = factor
        self.patience = patience
        self.threshold = threshold
        self.threshold_mode = threshold_mode
        self.cooldown = cooldown
        self.min_lr = min_lr
        self.eps = eps

    def create_scheduler(self, optimizer: Optimizer) -> _LRScheduler:
        """Create reduce LR on plateau scheduler."""
        return lr_scheduler.ReduceLROnPlateau(
            optimizer,
            mode=self.mode,
            factor=self.factor,
            patience=self.patience,
            threshold=self.threshold,
            threshold_mode=self.threshold_mode,
            cooldown=self.cooldown,
            min_lr=self.min_lr,
            eps=self.eps
        )

    def get_config(self) -> Dict[str, Any]:
        """Return configuration."""
        return {
            'mode': self.mode,
            'factor': self.factor,
            'patience': self.patience,
            'threshold': self.threshold,
            'threshold_mode': self.threshold_mode,
            'cooldown': self.cooldown,
            'min_lr': self.min_lr,
            'eps': self.eps
        }


@register('schedule_ops', 'cyclic_lr')
class CyclicLRScheduleOps(ScheduleOps):
    """Cyclic learning rate scheduler."""

    def __init__(self, base_lr: float, max_lr: float, step_size_up: int = 2000,
                 step_size_down: Optional[int] = None, mode: str = 'triangular',
                 gamma: float = 1.0, scale_fn: Optional[str] = None,
                 scale_mode: str = 'cycle', cycle_momentum: bool = True,
                 base_momentum: float = 0.8, max_momentum: float = 0.9, **kwargs):
        self.base_lr = base_lr
        self.max_lr = max_lr
        self.step_size_up = step_size_up
        self.step_size_down = step_size_down
        self.mode = mode
        self.gamma = gamma
        self.scale_fn = scale_fn
        self.scale_mode = scale_mode
        self.cycle_momentum = cycle_momentum
        self.base_momentum = base_momentum
        self.max_momentum = max_momentum

    def create_scheduler(self, optimizer: Optimizer) -> _LRScheduler:
        """Create cyclic LR scheduler."""
        return lr_scheduler.CyclicLR(
            optimizer,
            base_lr=self.base_lr,
            max_lr=self.max_lr,
            step_size_up=self.step_size_up,
            step_size_down=self.step_size_down,
            mode=self.mode,
            gamma=self.gamma,
            scale_fn=None,  # Custom functions not supported in config
            scale_mode=self.scale_mode,
            cycle_momentum=self.cycle_momentum,
            base_momentum=self.base_momentum,
            max_momentum=self.max_momentum
        )

    def get_config(self) -> Dict[str, Any]:
        """Return configuration."""
        return {
            'base_lr': self.base_lr,
            'max_lr': self.max_lr,
            'step_size_up': self.step_size_up,
            'step_size_down': self.step_size_down,
            'mode': self.mode,
            'gamma': self.gamma,
            'scale_mode': self.scale_mode,
            'cycle_momentum': self.cycle_momentum,
            'base_momentum': self.base_momentum,
            'max_momentum': self.max_momentum
        }


@register('schedule_ops', 'linear_lr')
class LinearLRScheduleOps(ScheduleOps):
    """Linear learning rate scheduler."""

    def __init__(self, start_factor: float = 1.0 / 3, end_factor: float = 1.0,
                 total_iters: int = 5, **kwargs):
        self.start_factor = start_factor
        self.end_factor = end_factor
        self.total_iters = total_iters

    def create_scheduler(self, optimizer: Optimizer) -> _LRScheduler:
        """Create linear LR scheduler."""
        return lr_scheduler.LinearLR(
            optimizer,
            start_factor=self.start_factor,
            end_factor=self.end_factor,
            total_iters=self.total_iters
        )

    def get_config(self) -> Dict[str, Any]:
        """Return configuration."""
        return {
            'start_factor': self.start_factor,
            'end_factor': self.end_factor,
            'total_iters': self.total_iters
        }


@register('schedule_ops', 'polynomial_lr')
class PolynomialLRScheduleOps(ScheduleOps):
    """Polynomial learning rate scheduler."""

    def __init__(self, total_iters: int = 5, power: float = 1.0, **kwargs):
        self.total_iters = total_iters
        self.power = power

    def create_scheduler(self, optimizer: Optimizer) -> _LRScheduler:
        """Create polynomial LR scheduler."""
        return lr_scheduler.PolynomialLR(
            optimizer,
            total_iters=self.total_iters,
            power=self.power
        )

    def get_config(self) -> Dict[str, Any]:
        """Return configuration."""
        return {
            'total_iters': self.total_iters,
            'power': self.power
        }
