"""
Experiment runner for SoundByte.

This module orchestrates the complete ML experiment pipeline,
managing component creation, training, and evaluation.
"""

import torch
import random
import numpy as np
from types import SimpleNamespace
from typing import Dict, Any
from pathlib import Path

from ..config.experiment import ExperimentConfig
from ..core.factory import ComponentFactory, auto_device
from ..plugins.registry import get_registry_stats


class ExperimentRunner:
    """Main experiment orchestrator for SoundByte."""

    def __init__(self, config: ExperimentConfig):
        self.config = config
        self.components = {}
        self.models = {}
        self.default_scheduler_config = SimpleNamespace(**{"name": "reduce_lr_on_plateau",
                                                           "params": {}})

    def _set_random_seeds(self):
        """Set random seeds for reproducibility."""
        torch.manual_seed(self.config.seed)
        torch.cuda.manual_seed_all(self.config.seed)
        np.random.seed(self.config.seed)
        random.seed(self.config.seed)

        # Ensure deterministic behavior
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False

    def _setup_device(self) -> str:
        """Setup and return the device to use."""
        if self.config.device == "auto":
            device = auto_device()
        else:
            device = self.config.device

        # Validate device availability
        if device == "cuda" and not torch.cuda.is_available():
            print("Warning: CUDA not available, falling back to CPU")
            device = "cpu"
        elif device == "mps" and not (hasattr(torch.backends, 'mps') and torch.backends.mps.is_available()):
            print("Warning: MPS not available, falling back to CPU")
            device = "cpu"

        return device


    def _run_classification(self, device: str) -> Dict[str, Any]:
        data = ComponentFactory.create_data_ops(self.config.data_ops)
        model = ComponentFactory.create_model_ops(self.config.model_ops, device)
        loss_function = ComponentFactory.create_penalty_ops(self.config.penalty_ops)
        optimizer = ComponentFactory.create_control_ops(self.config.control_ops)
        if self.config.schedule_ops:
            scheduler = ComponentFactory.create_schedule_ops(self.config.schedule_ops)
        else:
            scheduler = ComponentFactory.create_schedule_ops(self.default_scheduler_config)
            
        trainer = ComponentFactory.create_train_ops(self.config.train_ops)
        evaluator = ComponentFactory.create_audit_ops(self.config.audit_ops)
        print("All components created successfully")


        return trainer.train(model=model,
                             data_ops=data,
                             control_ops=optimizer,
                             penalty_ops=loss_function,
                             audit_ops=evaluator,
                             device=device,
                             schedule_ops=scheduler,
                             output_dir=self.config.output_dir
                             )

    def _run_distillation(self, device: str) -> Dict[str, Any]:
        if not self.config.teacher_model_ops and not self.config.student_model_ops:
            raise ValueError("Both teacher and student models required for distillation")
        
        if not self.config.distillation_penalty_ops:
            raise ValueError(" 'distillation_penalty_loss' is needed")

        data = ComponentFactory.create_data_ops(self.config.data_ops)
        teacher_model = ComponentFactory.create_model_ops(self.config.teacher_model_ops, device)
        student_model = ComponentFactory.create_model_ops(self.config.student_model_ops, device)
        loss_function = ComponentFactory.create_penalty_ops(self.config.distillation_penalty_ops)
        optimizer = ComponentFactory.create_control_ops(self.config.control_ops)
        if self.config.schedule_ops:
            scheduler = ComponentFactory.create_schedule_ops(self.config.schedule_ops)
        else:
            scheduler = ComponentFactory.create_schedule_ops(self.default_scheduler_config)
            
        trainer = ComponentFactory.create_train_ops(self.config.train_ops)
        evaluator = ComponentFactory.create_audit_ops(self.config.audit_ops)
        print("All components created successfully")

        return trainer.train(teacher_model=teacher_model.get_model(),
                             model=student_model,
                             data_ops=data,
                             control_ops=optimizer,
                             penalty_ops=loss_function,
                             audit_ops=evaluator,
                             device=device,
                             schedule_ops=scheduler,
                             output_dir=self.config.output_dir,
                             )

    def _run_quantization(self, device):
        model = ComponentFactory.create_model_ops(self.config.model_ops, device)
        quantizer = ComponentFactory.create_audit_ops(self.config.audit_ops)
        return quantizer.quantize(model=model.get_model(), device=device)


    def run(self) -> Dict[str, Any]:
        """Run the complete experiment."""
        print(f"Initializing SoundByte Experiment: {self.config.experiment_name}")

        # Create output directory
        output_path = Path(self.config.output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        print(f"Output Directory: {self.config.output_dir}")

        # Set random seeds
        self._set_random_seeds()

        # Setup device
        device = self._setup_device()
        print(f"Device: {device}")
        print(f"Seed: {self.config.seed}")
        print()


        # Determine experiment type and run
        try:
            if self.config.experiment_type == "quantization":
                # Quantization
                print("Running Quantization...")
                results = self._run_quantization(device)
            
            elif self.config.experiment_type == "knowledge_distillation":
                # Knowledge distillation
                print("Running Knowledge Distillation Training...")
                results = self._run_distillation(device)

            elif self.config.experiment_type == "classification":
                # Standard classification
                print("Running Classification Training...")
                results = self._run_classification(device)
                
            else: raise ValueError("{} not implemented yet, Implentation is in progress".format(self.config.experiment_type))

            # Save final model if requested
            if self.config.save_model:
                if 'student' in self.models:
                    # Save student model for distillation
                    model_path = output_path / 'final_student_model.pth'
                    torch.save(self.models['student'].state_dict(), model_path)
                    print(f"Final student model saved: {model_path}")
                elif 'main' in self.models:
                    # Save main model for classification
                    model_path = output_path / 'final_model.pth'
                    torch.save(self.models['main'].state_dict(), model_path)
                    print(f"Final model saved: {model_path}")

            return results

        except Exception as e:
            print(f"Experiment failed: {e}")
            raise

    def get_component_summary(self) -> Dict[str, Any]:
        """Get summary of created components."""
        summary = {
            'experiment_name': self.config.experiment_name,
            'device': self.config.device,
            'seed': self.config.seed,
            'components': {},
            'models': list(self.models.keys()),
            'registry_stats': get_registry_stats()
        }

        for name, component in self.components.items():
            summary['components'][name] = {
                'type': type(component).__name__,
                'config': component.get_config()
            }

        return summary


def run_experiment(config_path: str) -> Dict[str, Any]:
    """Convenience function to run an experiment from a config file."""
    from ..config.experiment import load_config

    config = load_config(config_path)
    runner = ExperimentRunner(config)
    return runner.run()
