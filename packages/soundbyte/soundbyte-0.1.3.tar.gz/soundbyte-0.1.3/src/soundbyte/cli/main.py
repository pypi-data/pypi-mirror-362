import argparse
import sys
import json
from pathlib import Path
from typing import List, Optional

from ..plugins.registry import list_components
from ..config.experiment import load_config, override_config
from ..execution.runner import ExperimentRunner


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="SoundByte: Modern Neural Network Research Toolkit",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  soundbyte run experiment.json
  soundbyte run experiment.json --override "train_ops.params.max_epochs=50"
  soundbyte validate experiment.json
  soundbyte list-components
  soundbyte list-components --type model_ops
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Run command
    run_parser = subparsers.add_parser('run', help='Run an experiment')
    run_parser.add_argument('config', help='Path to experiment configuration file')
    run_parser.add_argument('--output-dir', help='Output directory for results')
    run_parser.add_argument('--override', action='append', default=[],
                           help='Override configuration parameters (key=value)')

    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate configuration file')
    validate_parser.add_argument('config', help='Path to configuration file to validate')

    # List components command
    list_parser = subparsers.add_parser('list-components', help='List available components')
    list_parser.add_argument('--type', help='Component type to list (optional)')

    # Info command
    info_parser = subparsers.add_parser('info', help='Show experiment information')
    info_parser.add_argument('config', help='Path to configuration file')

    # Init command
    init_parser = subparsers.add_parser('init', help='Initialize example configurations')
    init_parser.add_argument('--template', choices=['classification', 'distillation'],
                            default='classification', help='Configuration template')
    init_parser.add_argument('--output', default='example_config.json',
                            help='Output configuration file')

    return parser


def run_experiment_command(args) -> int:
    """Handle the run experiment command."""
    try:
        # Load configuration
        config = load_config(args.config)

        # Apply overrides
        if args.override:
            config = override_config(config, args.override)

        # Set output directory
        if args.output_dir:
            config.output_dir = args.output_dir

        # Auto-detect device
        if config.device == "auto":
            import torch
            if torch.cuda.is_available():
                config.device = "cuda"
            elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
                config.device = "mps"
            else:
                config.device = "cpu"

        # Run experiment
        runner = ExperimentRunner(config)
        results = runner.run()

        return 0

    except Exception as e:
        print(f"Experiment failed: {e}")
        print(f"Error: {e}")
        return 1


def validate_config_command(args) -> int:
    """Handle the validate configuration command."""
    try:
        config = load_config(args.config)
        return 0
    except Exception as e:
        print(f"Configuration validation failed: {e}")
        return 1


def list_components_command(args) -> int:
    """Handle the list components command."""
    try:
        components = list_components(args.type)

        for component_type, names in components.items():
            print(f"{component_type.upper().replace('_', '')}:")
            if names:
                for name in sorted(names):
                    print(f"  {name}")
            else:
                print("  (none)")
            print()

        return 0
    except Exception as e:
        print(f"Failed to list components: {e}")
        return 1


def info_command(args) -> int:
    """Handle the info command."""
    try:
        config = load_config(args.config)

        print(f"Experiment Information: {config.name}")
        print(f"Seed: {config.seed}")
        print(f"Device: {config.device}")
        print(f"Output Directory: {config.output_dir}")
        print()

        print("Components:")
        print(f"  Data Operations: {config.data_ops.name}")

        if config.model_ops:
            print(f"  Model Operations: {config.model_ops.name}")
        if config.teacher_model_ops:
            print(f"  Teacher Model: {config.teacher_model_ops.name}")
        if config.student_model_ops:
            print(f"  Student Model: {config.student_model_ops.name}")

        if config.penalty_ops:
            print(f"  Penalty Operations: {config.penalty_ops.name}")
        if config.distillation_penalty_ops:
            print(f"  Distillation Penalty: {config.distillation_penalty_ops.name}")

        print(f"  Control Operations: {config.control_ops.name}")
        print(f"  Train Operations: {config.train_ops.name}")
        print(f"  Audit Operations: {config.audit_ops.name}")

        if config.schedule_ops:
            print(f"  Schedule Operations: {config.schedule_ops.name}")

        return 0
    except Exception as e:
        print(f"Failed to show info: {e}")
        return 1


def init_command(args) -> int:
    """Handle the init command."""
    try:
        if args.template == 'classification':
            template_config = {
                "name": "example_classification",
                "seed": 42,
                "device": "auto",
                "data_ops": {
                    "name": "cifar10",
                    "params": {
                        "batch_size": 128,
                        "num_workers": 4,
                        "download": True,
                        "data_dir": "./data"
                    }
                },
                "model_ops": {
                    "name": "simple_convnet",
                    "params": {
                        "num_classes": 10,
                        "channels": [32, 64, 128]
                    }
                },
                "penalty_ops": {
                    "name": "cross_entropy",
                    "params": {}
                },
                "control_ops": {
                    "name": "adam",
                    "params": {
                        "lr": 0.001,
                        "weight_decay": 0.0001
                    }
                },
                "train_ops": {
                    "name": "classification",
                    "params": {
                        "max_epochs": 20,
                        "early_stopping_patience": 5,
                        "save_best_model": True,
                        "log_interval": 50
                    }
                },
                "audit_ops": {
                    "name": "classification",
                    "params": {
                        "metrics": ["accuracy", "precision", "recall", "f1"]
                    }
                },
                "output_dir": "outputs/classification_example",
                "save_model": True
            }

        elif args.template == 'distillation':
            template_config = {
                "name": "example_distillation",
                "seed": 42,
                "device": "auto",
                "data_ops": {
                    "name": "cifar10",
                    "params": {
                        "batch_size": 128,
                        "num_workers": 4,
                        "download": True,
                        "data_dir": "./data"
                    }
                },
                "teacher_model_ops": {
                    "name": "resnet18",
                    "params": {
                        "num_classes": 10,
                        "in_channels": 3
                    }
                },
                "student_model_ops": {
                    "name": "simple_convnet",
                    "params": {
                        "num_classes": 10,
                        "channels": [16, 32, 64]
                    }
                },
                "distillation_penalty_ops": {
                    "name": "knowledge_distillation",
                    "params": {
                        "temperature": 4.0,
                        "alpha": 0.5
                    }
                },
                "control_ops": {
                    "name": "adam",
                    "params": {
                        "lr": 0.001,
                        "weight_decay": 0.0001
                    }
                },
                "train_ops": {
                    "name": "distillation",
                    "params": {
                        "max_epochs": 15,
                        "early_stopping_patience": 5,
                        "save_best_model": True,
                        "log_interval": 50
                    }
                },
                "audit_ops": {
                    "name": "distillation",
                    "params": {
                        "metrics": ["accuracy", "precision", "recall", "f1"],
                        "compute_agreement": True
                    }
                },
                "output_dir": "outputs/distillation_example",
                "save_model": True
            }

        # Save template configuration
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w') as f:
            json.dump(template_config, f, indent=2)

        print(f"Created {args.template} template: {output_path}")
        return 0

    except Exception as e:
        print(f"Failed to create template: {e}")
        return 1


def main():
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return 1

    # Import components to register them
    try:
        from .. import components
    except ImportError:
        print("Warning: Failed to import components")

    # Route to appropriate command handler
    if args.command == 'run':
        return run_experiment_command(args)
    elif args.command == 'validate':
        return validate_config_command(args)
    elif args.command == 'list-components':
        return list_components_command(args)
    elif args.command == 'info':
        return info_command(args)
    elif args.command == 'init':
        return init_command(args)
    else:
        print(f"Unknown command: {args.command}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
