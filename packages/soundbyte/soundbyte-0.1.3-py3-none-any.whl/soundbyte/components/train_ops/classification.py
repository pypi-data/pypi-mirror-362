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


@register('train_ops', 'classification')
class ClassificationTrainOps(TrainOps):
    """Standard supervised classification training."""

    def __init__(self, max_epochs: int = 100, early_stopping_patience: int = 10,
                 save_best_model: bool = True, log_interval: int = 100,
                 validation_interval: int = 1, gradient_clipping: Optional[float] = None,
                 **kwargs):
        self.max_epochs = max_epochs
        self.early_stopping_patience = early_stopping_patience
        self.save_best_model = save_best_model
        self.log_interval = log_interval
        self.validation_interval = validation_interval
        self.gradient_clipping = gradient_clipping

    def train(self, model: nn.Module, data_ops: DataOps, control_ops: ControlOps,
              penalty_ops: PenaltyOps, audit_ops: AuditOps, device: str,
              schedule_ops: Optional[ScheduleOps] = None, output_dir: str = "outputs",
              **kwargs) -> Dict[str, Any]:
        """Execute classification training."""

        # Setup
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        model = model.to(device)
        optimizer = control_ops.create_optimizer(model.parameters())
        scheduler = schedule_ops.create_scheduler(optimizer) if schedule_ops else None

        # Data loaders
        train_loader = data_ops.get_train_loader()
        val_loader = data_ops.get_val_loader()

        # Check for custom minibatch logic
        train_custom_logic = getattr(data_ops, 'train_custom_logic', None)
        val_custom_logic = getattr(data_ops, 'val_custom_logic', None)

        # Training tracking
        best_val_accuracy = 0.0
        patience_counter = 0
        training_history = []

        print(f"Starting classification training for {self.max_epochs} epochs")
        print(f"Training samples: {len(train_loader.dataset)}")
        print(f"Validation samples: {len(val_loader.dataset)}")

        start_time = time.time()

        for epoch in range(self.max_epochs):
            # Training phase
            model.train()
            train_loss = 0.0
            train_correct = 0
            train_total = 0

            train_pbar = tqdm(train_loader, desc=f"Epoch {epoch+1}/{self.max_epochs} [Train]")

            for batch_idx, batch in enumerate(train_pbar):
                if train_custom_logic:
                    # Use custom minibatch logic
                    outputs, loss = train_custom_logic(
                        batch_idx, batch, model, penalty_ops, optimizer, scheduler, device
                    )
                    if torch.is_tensor(outputs):
                        # Extract predictions for accuracy calculation
                        data, targets = batch
                        data, targets = data.to(device), targets.to(device)
                        _, predicted = torch.max(outputs.data, 1)
                        train_total += targets.size(0)
                        train_correct += (predicted == targets).sum().item()
                else:
                    # Standard training logic
                    data, targets = batch
                    data, targets = data.to(device), targets.to(device)

                    optimizer.zero_grad()
                    outputs = model(data)
                    loss = penalty_ops.compute_loss(outputs, targets)
                    loss.backward()

                    if self.gradient_clipping:
                        torch.nn.utils.clip_grad_norm_(model.parameters(), self.gradient_clipping)

                    optimizer.step()

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
                val_metrics = audit_ops.evaluate(model, val_loader, penalty_ops, device)
                val_accuracy = val_metrics.get('accuracy', 0)

                print(f"Epoch {epoch+1}: Train Loss: {epoch_train_loss:.4f}, "
                      f"Train Acc: {epoch_train_acc:.2f}%, Val Acc: {val_accuracy:.2f}%")

                # Save best model
                if self.save_best_model and val_accuracy > best_val_accuracy:
                    best_val_accuracy = val_accuracy
                    torch.save(model.state_dict(), output_path / 'best_model.pth')
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
                    'val_accuracy': val_accuracy
                })

        training_time = time.time() - start_time

        # Final evaluation on test set
        test_loader = data_ops.get_test_loader()
        test_metrics = audit_ops.evaluate(model, test_loader, penalty_ops, device)

        # Save results
        results = {
            'training_history': training_history,
            'best_val_accuracy': best_val_accuracy,
            'test_metrics': test_metrics,
            'training_time': training_time,
            'total_epochs': len(training_history)
        }

        with open(output_path / 'results.json', 'w') as f:
            json.dump(results, f, indent=2)

        print(f"Training completed in {training_time:.2f} seconds")
        print(f"Best validation accuracy: {best_val_accuracy:.2f}%")
        print(f"Test accuracy: {test_metrics.get('accuracy', 0):.2f}%")

        return results

    def get_config(self) -> Dict[str, Any]:
        """Return configuration."""
        return {
            'max_epochs': self.max_epochs,
            'early_stopping_patience': self.early_stopping_patience,
            'save_best_model': self.save_best_model,
            'log_interval': self.log_interval,
            'validation_interval': self.validation_interval,
            'gradient_clipping': self.gradient_clipping
        }