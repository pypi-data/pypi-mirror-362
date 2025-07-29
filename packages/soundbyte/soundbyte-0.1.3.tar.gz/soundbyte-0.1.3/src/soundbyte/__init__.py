"""
SoundByte: Modern Neural Network Research Toolkit

A sophisticated, modular framework for machine learning research built around
maximum modularity and JSON-driven configuration.
"""

__version__ = "1.0.0"
__author__ = "SoundByte Contributors"

# Import core functionality
from .config.experiment import ExperimentConfig, load_config, save_config
from .execution.runner import ExperimentRunner, run_experiment
from .plugins.registry import register, list_components, get_component
from .core.factory import ComponentFactory

# Import all component modules to ensure registration
from . import components

# Convenience imports
def load_experiment(config_path: str) -> ExperimentConfig:
    """Load experiment configuration from file."""
    return load_config(config_path)

def create_experiment(config_dict: dict) -> ExperimentConfig:
    """Create experiment configuration from dictionary."""
    return ExperimentConfig(**config_dict)

__all__ = [
    'ExperimentConfig',
    'ExperimentRunner', 
    'load_config',
    'save_config',
    'run_experiment',
    'register',
    'list_components',
    'get_component',
    'ComponentFactory',
    'load_experiment',
    'create_experiment'
]
