"""
Control operations components (optimizers) for SoundByte.

This module provides implementations of various optimization algorithms
for training neural networks.
"""

import torch
import torch.optim as optim
from typing import Dict, Any, Optional, List
from torch.optim import Optimizer

from ...core.interfaces import ControlOps
from ...plugins.registry import register


@register('control_ops', 'adam')
class AdamControlOps(ControlOps):
    """Adam optimizer wrapper."""

    def __init__(self, lr: float = 0.001, betas: tuple = (0.9, 0.999),
                 eps: float = 1e-8, weight_decay: float = 0, amsgrad: bool = False, **kwargs):
        self.lr = lr
        self.betas = betas
        self.eps = eps
        self.weight_decay = weight_decay
        self.amsgrad = amsgrad

    def create_optimizer(self, model_parameters) -> Optimizer:
        """Create Adam optimizer."""
        return optim.Adam(
            model_parameters,
            lr=self.lr,
            betas=self.betas,
            eps=self.eps,
            weight_decay=self.weight_decay,
            amsgrad=self.amsgrad
        )

    def get_config(self) -> Dict[str, Any]:
        """Return configuration."""
        return {
            'lr': self.lr,
            'betas': self.betas,
            'eps': self.eps,
            'weight_decay': self.weight_decay,
            'amsgrad': self.amsgrad
        }


@register('control_ops', 'adamw')
class AdamWControlOps(ControlOps):
    """AdamW optimizer wrapper."""

    def __init__(self, lr: float = 0.001, betas: tuple = (0.9, 0.999),
                 eps: float = 1e-8, weight_decay: float = 0.01, amsgrad: bool = False, **kwargs):
        self.lr = lr
        self.betas = betas
        self.eps = eps
        self.weight_decay = weight_decay
        self.amsgrad = amsgrad

    def create_optimizer(self, model_parameters) -> Optimizer:
        """Create AdamW optimizer."""
        return optim.AdamW(
            model_parameters,
            lr=self.lr,
            betas=self.betas,
            eps=self.eps,
            weight_decay=self.weight_decay,
            amsgrad=self.amsgrad
        )

    def get_config(self) -> Dict[str, Any]:
        """Return configuration."""
        return {
            'lr': self.lr,
            'betas': self.betas,
            'eps': self.eps,
            'weight_decay': self.weight_decay,
            'amsgrad': self.amsgrad
        }


@register('control_ops', 'sgd')
class SGDControlOps(ControlOps):
    """SGD optimizer wrapper."""

    def __init__(self, lr: float = 0.01, momentum: float = 0, dampening: float = 0,
                 weight_decay: float = 0, nesterov: bool = False, **kwargs):
        self.lr = lr
        self.momentum = momentum
        self.dampening = dampening
        self.weight_decay = weight_decay
        self.nesterov = nesterov

    def create_optimizer(self, model_parameters) -> Optimizer:
        """Create SGD optimizer."""
        return optim.SGD(
            model_parameters,
            lr=self.lr,
            momentum=self.momentum,
            dampening=self.dampening,
            weight_decay=self.weight_decay,
            nesterov=self.nesterov
        )

    def get_config(self) -> Dict[str, Any]:
        """Return configuration."""
        return {
            'lr': self.lr,
            'momentum': self.momentum,
            'dampening': self.dampening,
            'weight_decay': self.weight_decay,
            'nesterov': self.nesterov
        }


@register('control_ops', 'rmsprop')
class RMSpropControlOps(ControlOps):
    """RMSprop optimizer wrapper."""

    def __init__(self, lr: float = 0.01, alpha: float = 0.99, eps: float = 1e-8,
                 weight_decay: float = 0, momentum: float = 0, centered: bool = False, **kwargs):
        self.lr = lr
        self.alpha = alpha
        self.eps = eps
        self.weight_decay = weight_decay
        self.momentum = momentum
        self.centered = centered

    def create_optimizer(self, model_parameters) -> Optimizer:
        """Create RMSprop optimizer."""
        return optim.RMSprop(
            model_parameters,
            lr=self.lr,
            alpha=self.alpha,
            eps=self.eps,
            weight_decay=self.weight_decay,
            momentum=self.momentum,
            centered=self.centered
        )

    def get_config(self) -> Dict[str, Any]:
        """Return configuration."""
        return {
            'lr': self.lr,
            'alpha': self.alpha,
            'eps': self.eps,
            'weight_decay': self.weight_decay,
            'momentum': self.momentum,
            'centered': self.centered
        }


@register('control_ops', 'adagrad')
class AdagradControlOps(ControlOps):
    """Adagrad optimizer wrapper."""

    def __init__(self, lr: float = 0.01, lr_decay: float = 0, weight_decay: float = 0,
                 initial_accumulator_value: float = 0, eps: float = 1e-10, **kwargs):
        self.lr = lr
        self.lr_decay = lr_decay
        self.weight_decay = weight_decay
        self.initial_accumulator_value = initial_accumulator_value
        self.eps = eps

    def create_optimizer(self, model_parameters) -> Optimizer:
        """Create Adagrad optimizer."""
        return optim.Adagrad(
            model_parameters,
            lr=self.lr,
            lr_decay=self.lr_decay,
            weight_decay=self.weight_decay,
            initial_accumulator_value=self.initial_accumulator_value,
            eps=self.eps
        )

    def get_config(self) -> Dict[str, Any]:
        """Return configuration."""
        return {
            'lr': self.lr,
            'lr_decay': self.lr_decay,
            'weight_decay': self.weight_decay,
            'initial_accumulator_value': self.initial_accumulator_value,
            'eps': self.eps
        }


@register('control_ops', 'adadelta')
class AdadeltaControlOps(ControlOps):
    """Adadelta optimizer wrapper."""

    def __init__(self, lr: float = 1.0, rho: float = 0.9, eps: float = 1e-6,
                 weight_decay: float = 0, **kwargs):
        self.lr = lr
        self.rho = rho
        self.eps = eps
        self.weight_decay = weight_decay

    def create_optimizer(self, model_parameters) -> Optimizer:
        """Create Adadelta optimizer."""
        return optim.Adadelta(
            model_parameters,
            lr=self.lr,
            rho=self.rho,
            eps=self.eps,
            weight_decay=self.weight_decay
        )

    def get_config(self) -> Dict[str, Any]:
        """Return configuration."""
        return {
            'lr': self.lr,
            'rho': self.rho,
            'eps': self.eps,
            'weight_decay': self.weight_decay
        }


@register('control_ops', 'nadam')
class NAdamControlOps(ControlOps):
    """NAdam optimizer wrapper."""

    def __init__(self, lr: float = 0.002, betas: tuple = (0.9, 0.999),
                 eps: float = 1e-8, weight_decay: float = 0, momentum_decay: float = 0.004, **kwargs):
        self.lr = lr
        self.betas = betas
        self.eps = eps
        self.weight_decay = weight_decay
        self.momentum_decay = momentum_decay

    def create_optimizer(self, model_parameters) -> Optimizer:
        """Create NAdam optimizer."""
        return optim.NAdam(
            model_parameters,
            lr=self.lr,
            betas=self.betas,
            eps=self.eps,
            weight_decay=self.weight_decay,
            momentum_decay=self.momentum_decay
        )

    def get_config(self) -> Dict[str, Any]:
        """Return configuration."""
        return {
            'lr': self.lr,
            'betas': self.betas,
            'eps': self.eps,
            'weight_decay': self.weight_decay,
            'momentum_decay': self.momentum_decay
        }


@register('control_ops', 'radam')
class RAdamControlOps(ControlOps):
    """RAdam optimizer wrapper."""

    def __init__(self, lr: float = 0.001, betas: tuple = (0.9, 0.999),
                 eps: float = 1e-8, weight_decay: float = 0, **kwargs):
        self.lr = lr
        self.betas = betas
        self.eps = eps
        self.weight_decay = weight_decay

    def create_optimizer(self, model_parameters) -> Optimizer:
        """Create RAdam optimizer."""
        return optim.RAdam(
            model_parameters,
            lr=self.lr,
            betas=self.betas,
            eps=self.eps,
            weight_decay=self.weight_decay
        )

    def get_config(self) -> Dict[str, Any]:
        """Return configuration."""
        return {
            'lr': self.lr,
            'betas': self.betas,
            'eps': self.eps,
            'weight_decay': self.weight_decay
        }
