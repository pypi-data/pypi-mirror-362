"""
Component factory system for SoundByte.

This module provides the factory classes that create component instances
based on configuration specifications.
"""

import torch
from typing import Dict, Any, Optional
from .interfaces import *
from ..plugins.registry import get_component
from ..config.experiment import *


def auto_device() -> str:
    """Automatically select best available device."""
    if torch.cuda.is_available():
        return 'cuda'
    elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
        return 'mps'
    else:
        return 'cpu'


class ComponentFactory:
    """Factory for creating SoundByte components."""

    @staticmethod
    def create_data_ops(config: DataOpsConfig) -> DataOps:
        """Create data operations component."""
        component_class = get_component('data_ops', config.name)
        return component_class(**config.params)

    @staticmethod
    def create_model_ops(config: ModelOpsConfig, device: str = 'cpu') -> ModelOps:
        """Create model operations component."""
        component_class = get_component('model_ops', config.name)
        instance = component_class(**config.params)

        # Move model to device
        model = instance.get_model()
        model.to(device)

        return instance

    @staticmethod
    def create_penalty_ops(config: PenaltyOpsConfig) -> PenaltyOps:
        """Create penalty operations component."""
        component_class = get_component('penalty_ops', config.name)
        return component_class(**config.params)

    @staticmethod
    def create_control_ops(config: ControlOpsConfig) -> ControlOps:
        """Create control operations component."""
        component_class = get_component('control_ops', config.name)
        return component_class(**config.params)

    @staticmethod
    def create_schedule_ops(config: Optional[ScheduleOpsConfig]) -> Optional[ScheduleOps]:
        """Create schedule operations component."""
        if config is None:
            return None
        component_class = get_component('schedule_ops', config.name)
        return component_class(**config.params)

    @staticmethod
    def create_train_ops(config: TrainOpsConfig) -> TrainOps:
        """Create training operations component."""
        component_class = get_component('train_ops', config.name)
        return component_class(**config.params)

    @staticmethod  
    def create_audit_ops(config: AuditOpsConfig) -> AuditOps:
        """Create audit operations component."""
        component_class = get_component('audit_ops', config.name)
        return component_class(**config.params)
