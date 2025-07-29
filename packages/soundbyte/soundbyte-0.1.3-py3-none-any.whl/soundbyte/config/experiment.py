"""
Configuration management for SoundByte experiments.

This module provides Pydantic-based configuration classes for type-safe
experiment specification and validation.
"""

import json
import yaml
from typing import Dict, Any, Optional, List, Union
from pathlib import Path
from pydantic import BaseModel, Field, validator


class ComponentConfig(BaseModel):
    """Base configuration for all components."""
    name: str
    params: Dict[str, Any] = Field(default_factory=dict)


class DataOpsConfig(ComponentConfig):
    """Configuration for data operations."""
    train_minibatch_logic: Optional[str] = None  # Path to custom logic file
    val_minibatch_logic: Optional[str] = None    # Path to custom logic file


class ModelOpsConfig(ComponentConfig):
    """Configuration for model operations."""
    pass


class PenaltyOpsConfig(ComponentConfig):
    """Configuration for penalty operations."""
    pass


class ControlOpsConfig(ComponentConfig):
    """Configuration for control operations."""
    pass


class ScheduleOpsConfig(ComponentConfig):
    """Configuration for schedule operations."""
    pass


class TrainOpsConfig(ComponentConfig):
    """Configuration for training operations."""
    pass


class AuditOpsConfig(ComponentConfig):
    """Configuration for audit operations."""
    pass


class ExperimentConfig(BaseModel):
    """Complete experiment configuration."""
    experiment_type: str
    experiment_name: str
    seed: int = 42
    device: str = "auto"
    output_dir: str = "outputs"
    save_model: bool = True

    # Core components
    data_ops: DataOpsConfig
    penalty_ops: Optional[PenaltyOpsConfig] = None
    control_ops: ControlOpsConfig
    train_ops: TrainOpsConfig
    audit_ops: AuditOpsConfig

    # Model configurations (can have multiple for distillation)
    model_ops: Optional[ModelOpsConfig] = None
    teacher_model_ops: Optional[ModelOpsConfig] = None
    student_model_ops: Optional[ModelOpsConfig] = None

    # Optional components
    schedule_ops: Optional[ScheduleOpsConfig] = None
    distillation_penalty_ops: Optional[PenaltyOpsConfig] = None

    @validator('device')
    def validate_device(cls, v):
        if v == "auto":
            return v
        if v not in ['cpu', 'cuda', 'mps']:
            raise ValueError(f"Device must be 'auto', 'cpu', 'cuda', or 'mps', got: {v}")
        return v

    @validator('seed')
    def validate_seed(cls, v):
        if v < 0:
            raise ValueError("Seed must be non-negative")
        return v


def load_config(config_path: Union[str, Path]) -> ExperimentConfig:
    """Load configuration from JSON or YAML file."""
    config_path = Path(config_path)

    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    # Load based on file extension
    with open(config_path, 'r') as f:
        if config_path.suffix.lower() == '.yaml' or config_path.suffix.lower() == '.yml':
            config_dict = yaml.safe_load(f)
        else:
            config_dict = json.load(f)

    return ExperimentConfig(**config_dict)


def save_config(config: ExperimentConfig, config_path: Union[str, Path]):
    """Save configuration to JSON file."""
    config_path = Path(config_path)
    config_path.parent.mkdir(parents=True, exist_ok=True)

    with open(config_path, 'w') as f:
        json.dump(config.dict(), f, indent=2)


def override_config(config: ExperimentConfig, overrides: List[str]) -> ExperimentConfig:
    """Override configuration parameters from command line."""
    config_dict = config.dict()

    for override in overrides:
        if '=' not in override:
            raise ValueError(f"Invalid override format: {override}. Expected 'key=value'")

        key, value = override.split('=', 1)

        # Parse nested keys (e.g., "train_ops.params.max_epochs")
        keys = key.split('.')
        current = config_dict

        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]

        # Try to parse value as appropriate type
        try:
            if value.lower() in ['true', 'false']:
                current[keys[-1]] = value.lower() == 'true'
            elif value.isdigit():
                current[keys[-1]] = int(value)
            elif '.' in value and value.replace('.', '').isdigit():
                current[keys[-1]] = float(value)
            else:
                current[keys[-1]] = value
        except:
            current[keys[-1]] = value

    return ExperimentConfig(**config_dict)
