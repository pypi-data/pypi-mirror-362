"""
Plugin registry system for SoundByte components.

This module provides the registration and discovery mechanism for all
SoundByte components, enabling dynamic loading and instantiation.
"""

from typing import Dict, List, Type, Any, Optional
import importlib.util
import inspect
from pathlib import Path


# Global registry for all components
_registry: Dict[str, Dict[str, Type]] = {
    'data_ops': {},
    'model_ops': {},
    'penalty_ops': {},
    'control_ops': {},
    'schedule_ops': {},
    'train_ops': {},
    'audit_ops': {}
}


def register(component_type: str, name: Optional[str] = None):
    """Decorator to register a component in the registry."""
    def decorator(cls):
        component_name = name or cls.__name__.lower()

        if component_type not in _registry:
            raise ValueError(f"Unknown component type: {component_type}")

        _registry[component_type][component_name] = cls
        return cls

    return decorator


def get_component(component_type: str, name: str) -> Type:
    """Get a component class by type and name."""
    if component_type not in _registry:
        raise ValueError(f"Unknown component type: {component_type}")

    if name not in _registry[component_type]:
        available = list(_registry[component_type].keys())
        raise ValueError(f"Unknown {component_type}: {name}. Available: {available}")

    return _registry[component_type][name]


def list_components(component_type: Optional[str] = None) -> Dict[str, List[str]]:
    """List all registered components."""
    if component_type:
        if component_type not in _registry:
            raise ValueError(f"Unknown component type: {component_type}")
        return {component_type: list(_registry[component_type].keys())}

    return {k: list(v.keys()) for k, v in _registry.items()}


def load_custom_logic(file_path: str, device: str = 'cpu') -> callable:
    """Load custom minibatch logic from a Python file."""
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"Custom logic file not found: {file_path}")

    # Load the module
    spec = importlib.util.spec_from_file_location("custom_logic", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Get the custom_minibatch_logic function
    if not hasattr(module, 'custom_minibatch_logic'):
        raise AttributeError(f"Function 'custom_minibatch_logic' not found in {file_path}")

    custom_func = getattr(module, 'custom_minibatch_logic')

    # Validate function signature
    sig = inspect.signature(custom_func)
    expected_params = ['idx', 'minibatch', 'model', 'loss_fn', 'optimizer', 'scheduler', 'device']
    actual_params = list(sig.parameters.keys())

    if len(actual_params) != len(expected_params):
        raise ValueError(f"custom_minibatch_logic must have parameters: {expected_params}")

    return custom_func


def clear_registry():
    """Clear all registered components (mainly for testing)."""
    global _registry
    for component_type in _registry:
        _registry[component_type].clear()


def get_registry_stats() -> Dict[str, int]:
    """Get statistics about registered components."""
    return {k: len(v) for k, v in _registry.items()}
