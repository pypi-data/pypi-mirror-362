"""
Train operations components (training strategies) for SoundByte.

This module provides implementations of various training paradigms
and strategies for neural network training.
"""

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from typing import Dict, Any, Optional, List
import time
import json
from pathlib import Path
from tqdm import tqdm

from ...core.interfaces import TrainOps, DataOps, ControlOps, PenaltyOps, ScheduleOps, AuditOps
from ...plugins.registry import register, load_custom_logic



@register('train_ops', 'distillation')
class DistillationTrainOps(TrainOps):
    """Knowledge distillation training strategy."""

    def __init__(self, max_epochs: int = 100, early_stopping_patience: int = 10,
                 save_best_model: bool = True, log_interval: int = 100,
                 validation_interval: int = 1, gradient_clipping: Optional[float] = None,
                 teacher_model_path: Optional[str] = None, **kwargs):
        self.max_epochs = max_epochs
        self.early_stopping_patience = early_stopping_patience
        self.save_best_model = save_best_model
        self.log_interval = log_interval
        self.validation_interval = validation_interval
        self.gradient_clipping = gradient_clipping
        self.teacher_model_path = teacher_model_path

    def train(self, model: nn.Module, data_ops: DataOps, control_ops: ControlOps,
              penalty_ops: PenaltyOps, audit_ops: AuditOps, device: str,
              schedule_ops: Optional[ScheduleOps] = None, output_dir: str = "outputs",
              teacher_model: Optional[nn.Module] = None, **kwargs) -> Dict[str, Any]:
        """Execute knowledge distillation training."""

        if teacher_model is None:
            raise ValueError("Teacher model required for distillation training")

        # Setup
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        student_model = model.to(device)
        teacher_model = teacher_model.to(device)
        teacher_model.eval()  # Teacher in eval mode

        optimizer = control_ops.create_optimizer(student_model.parameters())
        scheduler = schedule_ops.create_scheduler(optimizer) if schedule_ops else None

        # Data loaders
        train_loader = data_ops.get_train_loader()
        val_loader = data_ops.get_val_loader()

        # Check for custom minibatch logic
        train_custom_logic = getattr(data_ops, 'train_custom_logic', None)

        # Training tracking
        best_val_accuracy = 0.0
        patience_counter = 0
        training_history = []

        print(f"Starting knowledge distillation training for {self.max_epochs} epochs")
        print(f"Training samples: {len(train_loader.dataset)}")
        print(f"Validation samples: {len(val_loader.dataset)}")

        start_time = time.time()

        for epoch in range(self.max_epochs):
            # Training phase
            student_model.train()
            train_loss = 0.0
            train_correct = 0
            train_total = 0

            train_pbar = tqdm(train_loader, desc=f"Epoch {epoch+1}/{self.max_epochs} [Distill]")

            for batch_idx, batch in enumerate(train_pbar):
                data, targets = batch
                data, targets = data.to(device), targets.to(device)

                if train_custom_logic:
                    # Custom logic needs to handle teacher outputs
                    with torch.no_grad():
                        teacher_outputs = teacher_model(data)

                    # Note: Custom logic for distillation would need special handling
                    # For now, fall back to standard logic
                    optimizer.zero_grad()
                    student_outputs = student_model(data)
                    loss = penalty_ops.compute_loss(
                        student_outputs, targets, teacher_outputs=teacher_outputs
                    )
                    loss.backward()

                    if self.gradient_clipping:
                        torch.nn.utils.clip_grad_norm_(student_model.parameters(), self.gradient_clipping)

                    optimizer.step()
                    outputs = student_outputs
                else:
                    # Standard distillation logic
                    optimizer.zero_grad()

                    # Get teacher and student outputs
                    with torch.no_grad():
                        teacher_outputs = teacher_model(data)

                    student_outputs = student_model(data)

                    # Compute distillation loss
                    loss = penalty_ops.compute_loss(
                        student_outputs, targets, teacher_outputs=teacher_outputs
                    )
                    loss.backward()

                    if self.gradient_clipping:
                        torch.nn.utils.clip_grad_norm_(student_model.parameters(), self.gradient_clipping)

                    optimizer.step()
                    outputs = student_outputs

                # Statistics
                train_loss += loss.item()
                _, predicted = torch.max(outputs.data, 1)
                train_total += targets.size(0)
                train_correct += (predicted == targets).sum().item()

                # Logging
                if batch_idx % self.log_interval == 0:
                    current_acc = 100. * train_correct / train_total if train_total > 0 else 0
                    train_pbar.set_postfix({
                        'Loss': f'{loss.item():.4f}',
                        'Acc': f'{current_acc:.2f}%'
                    })

            # Calculate epoch training metrics
            epoch_train_loss = train_loss / len(train_loader)
            epoch_train_acc = 100. * train_correct / train_total

            # Validation phase
            if epoch % self.validation_interval == 0:
                val_metrics = audit_ops.evaluate(
                    student_model, val_loader, penalty_ops, device,
                    teacher_model=teacher_model
                )
                val_accuracy = val_metrics.get('student_accuracy', val_metrics.get('accuracy', 0))

                print(f"Epoch {epoch+1}: Train Loss: {epoch_train_loss:.4f}, "
                      f"Train Acc: {epoch_train_acc:.2f}%, Val Acc: {val_accuracy:.2f}%")

                # Save best model
                if self.save_best_model and val_accuracy > best_val_accuracy:
                    best_val_accuracy = val_accuracy
                    torch.save(student_model.state_dict(), output_path / 'best_student_model.pth')
                    patience_counter = 0
                else:
                    patience_counter += 1

                # Early stopping
                if patience_counter >= self.early_stopping_patience:
                    print(f"Early stopping triggered after {epoch+1} epochs")
                    break

                # Learning rate scheduling
                if scheduler:
                    if hasattr(scheduler, 'step'):
                        if 'ReduceLROnPlateau' in str(type(scheduler)):
                            scheduler.step(val_metrics.get('loss', epoch_train_loss))
                        else:
                            scheduler.step()

                # Record training history
                training_history.append({
                    'epoch': epoch + 1,
                    'train_loss': epoch_train_loss,
                    'train_accuracy': epoch_train_acc,
                    'val_loss': val_metrics.get('loss', 0),
                    'val_accuracy': val_accuracy,
                    'teacher_accuracy': val_metrics.get('teacher_accuracy', 0),
                    'agreement': val_metrics.get('agreement', 0)
                })

        training_time = time.time() - start_time

        # Final evaluation on test set
        test_loader = data_ops.get_test_loader()
        test_metrics = audit_ops.evaluate(
            student_model, test_loader, penalty_ops, device,
            teacher_model=teacher_model
        )

        # Save results
        results = {
            'training_history': training_history,
            'best_val_accuracy': best_val_accuracy,
            'test_metrics': test_metrics,
            'training_time': training_time,
            'total_epochs': len(training_history)
        }

        with open(output_path / 'distillation_results.json', 'w') as f:
            json.dump(results, f, indent=2)

        print(f"Distillation training completed in {training_time:.2f} seconds")
        print(f"Best student validation accuracy: {best_val_accuracy:.2f}%")
        print(f"Test student accuracy: {test_metrics.get('student_accuracy', 0):.2f}%")

        return results

    def get_config(self) -> Dict[str, Any]:
        """Return configuration."""
        return {
            'max_epochs': self.max_epochs,
            'early_stopping_patience': self.early_stopping_patience,
            'save_best_model': self.save_best_model,
            'log_interval': self.log_interval,
            'validation_interval': self.validation_interval,
            'gradient_clipping': self.gradient_clipping,
            'teacher_model_path': self.teacher_model_path
        }
