import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from typing import Dict, Any, List, Optional
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import confusion_matrix, classification_report
from tqdm import tqdm

from ...core.interfaces import AuditOps, PenaltyOps
from ...plugins.registry import register


@register('audit_ops', 'classification')
class ClassificationAuditOps(AuditOps):
    """Classification evaluation and metrics computation."""

    def __init__(self, metrics: List[str] = None, **kwargs):
        self.metrics = metrics or ['accuracy', 'precision', 'recall', 'f1']
        self.supported_metrics = [
            'accuracy', 'precision', 'recall', 'f1', 
            'confusion_matrix', 'classification_report'
        ]

        # Validate metrics
        for metric in self.metrics:
            if metric not in self.supported_metrics:
                raise ValueError(f"Unsupported metric: {metric}. "
                               f"Supported: {self.supported_metrics}")

    def evaluate(self, model: nn.Module, data_loader: DataLoader, 
                 penalty_ops: PenaltyOps, device: str, **kwargs) -> Dict[str, Any]:
        """Evaluate model on given data loader."""
        model.eval()

        all_predictions = []
        all_targets = []
        total_loss = 0.0

        print("Evaluating model...")

        with torch.no_grad():
            eval_pbar = tqdm(data_loader, desc="Evaluation")
            for batch in eval_pbar:
                data, targets = batch
                data, targets = data.to(device), targets.to(device)

                outputs = model(data)
                loss = penalty_ops.compute_loss(outputs, targets)

                total_loss += loss.item()

                # Get predictions
                _, predicted = torch.max(outputs.data, 1)

                all_predictions.extend(predicted.cpu().numpy())
                all_targets.extend(targets.cpu().numpy())

        # Convert to numpy arrays
        predictions = np.array(all_predictions)
        targets = np.array(all_targets)

        # Compute metrics
        results = {
            'loss': total_loss / len(data_loader),
            'num_samples': len(targets)
        }

        # Accuracy
        if 'accuracy' in self.metrics:
            accuracy = accuracy_score(targets, predictions) * 100
            results['accuracy'] = accuracy

        # Precision
        if 'precision' in self.metrics:
            precision = precision_score(targets, predictions, average='weighted', zero_division=0) * 100
            results['precision'] = precision

        # Recall
        if 'recall' in self.metrics:
            recall = recall_score(targets, predictions, average='weighted', zero_division=0) * 100
            results['recall'] = recall

        # F1-score
        if 'f1' in self.metrics:
            f1 = f1_score(targets, predictions, average='weighted', zero_division=0) * 100
            results['f1'] = f1

        # Confusion matrix
        if 'confusion_matrix' in self.metrics:
            cm = confusion_matrix(targets, predictions)
            results['confusion_matrix'] = cm.tolist()

        # Classification report
        if 'classification_report' in self.metrics:
            report = classification_report(targets, predictions, output_dict=True, zero_division=0)
            results['classification_report'] = report

        return results

    def get_config(self) -> Dict[str, Any]:
        """Return configuration."""
        return {'metrics': self.metrics}


@register('audit_ops', 'regression')
class RegressionAuditOps(AuditOps):
    """Regression evaluation and metrics computation."""

    def __init__(self, metrics: List[str] = None, **kwargs):
        self.metrics = metrics or ['mse', 'mae', 'r2']
        self.supported_metrics = ['mse', 'mae', 'rmse', 'r2', 'explained_variance']

        # Validate metrics
        for metric in self.metrics:
            if metric not in self.supported_metrics:
                raise ValueError(f"Unsupported metric: {metric}. "
                               f"Supported: {self.supported_metrics}")

    def evaluate(self, model: nn.Module, data_loader: DataLoader,
                 penalty_ops: PenaltyOps, device: str, **kwargs) -> Dict[str, Any]:
        """Evaluate regression model on given data loader."""
        model.eval()

        all_predictions = []
        all_targets = []
        total_loss = 0.0

        print("Evaluating regression model...")

        with torch.no_grad():
            eval_pbar = tqdm(data_loader, desc="Regression Evaluation")
            for batch in eval_pbar:
                data, targets = batch
                data, targets = data.to(device), targets.to(device)

                outputs = model(data)
                loss = penalty_ops.compute_loss(outputs, targets)

                total_loss += loss.item()

                all_predictions.extend(outputs.cpu().numpy().flatten())
                all_targets.extend(targets.cpu().numpy().flatten())

        # Convert to numpy arrays
        predictions = np.array(all_predictions)
        targets = np.array(all_targets)

        # Compute metrics
        results = {
            'loss': total_loss / len(data_loader),
            'num_samples': len(targets)
        }

        # Mean Squared Error
        if 'mse' in self.metrics:
            mse = np.mean((predictions - targets) ** 2)
            results['mse'] = mse

        # Mean Absolute Error
        if 'mae' in self.metrics:
            mae = np.mean(np.abs(predictions - targets))
            results['mae'] = mae

        # Root Mean Squared Error
        if 'rmse' in self.metrics:
            rmse = np.sqrt(np.mean((predictions - targets) ** 2))
            results['rmse'] = rmse

        # R-squared
        if 'r2' in self.metrics:
            ss_res = np.sum((targets - predictions) ** 2)
            ss_tot = np.sum((targets - np.mean(targets)) ** 2)
            r2 = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
            results['r2'] = r2

        # Explained Variance Score
        if 'explained_variance' in self.metrics:
            variance_score = 1 - np.var(targets - predictions) / np.var(targets)
            results['explained_variance'] = variance_score

        return results

    def get_config(self) -> Dict[str, Any]:
        """Return configuration."""
        return {'metrics': self.metrics}
