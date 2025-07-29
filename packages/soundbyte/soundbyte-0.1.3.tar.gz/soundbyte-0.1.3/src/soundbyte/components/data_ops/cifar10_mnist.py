"""
Data operations components (datasets) for SoundByte.

This module provides implementations of various dataset loaders
and preprocessing operations.
"""

import torch
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import DataLoader, random_split
from typing import Dict, Any, Optional, Callable
import os
from pathlib import Path

from ...core.interfaces import DataOps
from ...plugins.registry import register, load_custom_logic


@register('data_ops', 'cifar10')
class CIFAR10DataOps(DataOps):
    """CIFAR-10 dataset operations."""

    def __init__(self, batch_size: int = 32, num_workers: int = 2, 
                 download: bool = True, data_dir: str = "./data",
                 train_minibatch_logic: Optional[str] = None,
                 val_minibatch_logic: Optional[str] = None,
                 **kwargs):
        self.batch_size = batch_size
        self.num_workers = num_workers
        self.download = download
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Load custom minibatch logic if provided
        self.train_custom_logic = None
        self.val_custom_logic = None

        if train_minibatch_logic:
            self.train_custom_logic = load_custom_logic(train_minibatch_logic)
        if val_minibatch_logic:
            self.val_custom_logic = load_custom_logic(val_minibatch_logic)

        # CIFAR-10 specific transforms
        self.train_transform = transforms.Compose([
            transforms.RandomHorizontalFlip(),
            transforms.RandomCrop(32, padding=4),
            transforms.ToTensor(),
            transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010))
        ])

        self.test_transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010))
        ])

        self._prepare_datasets()

    def _prepare_datasets(self):
        """Prepare train, validation, and test datasets."""
        # Load datasets
        train_dataset = torchvision.datasets.CIFAR10(
            root=str(self.data_dir), train=True, 
            download=self.download, transform=self.train_transform
        )

        test_dataset = torchvision.datasets.CIFAR10(
            root=str(self.data_dir), train=False,
            download=self.download, transform=self.test_transform
        )

        # Split training set into train and validation
        train_size = int(0.8 * len(train_dataset))
        val_size = len(train_dataset) - train_size
        self.train_dataset, self.val_dataset = random_split(
            train_dataset, [train_size, val_size],
            generator=torch.Generator().manual_seed(42)
        )

        self.test_dataset = test_dataset

    def _get_collate_fn(self, custom_logic: Optional[Callable]) -> Optional[Callable]:
        """Get collate function for custom minibatch logic."""
        if custom_logic is None:
            return None

        def collate_fn(batch):
            # Default collation
            data = torch.stack([item[0] for item in batch])
            targets = torch.tensor([item[1] for item in batch])
            return data, targets

        return collate_fn

    def get_train_loader(self) -> DataLoader:
        """Return training data loader."""
        return DataLoader(
            self.train_dataset,
            batch_size=self.batch_size,
            shuffle=True,
            num_workers=self.num_workers,
            pin_memory=torch.cuda.is_available(),
            collate_fn=self._get_collate_fn(self.train_custom_logic)
        )

    def get_val_loader(self) -> DataLoader:
        """Return validation data loader."""
        return DataLoader(
            self.val_dataset,
            batch_size=self.batch_size,
            shuffle=False,
            num_workers=self.num_workers,
            pin_memory=torch.cuda.is_available(),
            collate_fn=self._get_collate_fn(self.val_custom_logic)
        )

    def get_test_loader(self) -> DataLoader:
        """Return test data loader."""
        return DataLoader(
            self.test_dataset,
            batch_size=self.batch_size,
            shuffle=False,
            num_workers=self.num_workers,
            pin_memory=torch.cuda.is_available()
        )

    def get_num_classes(self) -> int:
        """Return number of classes."""
        return 10

    def get_config(self) -> Dict[str, Any]:
        """Return configuration."""
        return {
            'batch_size': self.batch_size,
            'num_workers': self.num_workers,
            'download': self.download,
            'data_dir': str(self.data_dir)
        }


@register('data_ops', 'mnist')
class MNISTDataOps(DataOps):
    """MNIST dataset operations."""

    def __init__(self, batch_size: int = 64, num_workers: int = 2,
                 download: bool = True, data_dir: str = "./data",
                 train_minibatch_logic: Optional[str] = None,
                 val_minibatch_logic: Optional[str] = None,
                 **kwargs):
        self.batch_size = batch_size
        self.num_workers = num_workers
        self.download = download
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Load custom minibatch logic if provided
        self.train_custom_logic = None
        self.val_custom_logic = None

        if train_minibatch_logic:
            self.train_custom_logic = load_custom_logic(train_minibatch_logic)
        if val_minibatch_logic:
            self.val_custom_logic = load_custom_logic(val_minibatch_logic)

        # MNIST specific transforms
        self.transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,))
        ])

        self._prepare_datasets()

    def _prepare_datasets(self):
        """Prepare train, validation, and test datasets."""
        # Load datasets
        train_dataset = torchvision.datasets.MNIST(
            root=str(self.data_dir), train=True,
            download=self.download, transform=self.transform
        )

        test_dataset = torchvision.datasets.MNIST(
            root=str(self.data_dir), train=False,
            download=self.download, transform=self.transform
        )

        # Split training set into train and validation
        train_size = int(0.8 * len(train_dataset))
        val_size = len(train_dataset) - train_size
        self.train_dataset, self.val_dataset = random_split(
            train_dataset, [train_size, val_size],
            generator=torch.Generator().manual_seed(42)
        )

        self.test_dataset = test_dataset

    def _get_collate_fn(self, custom_logic: Optional[Callable]) -> Optional[Callable]:
        """Get collate function for custom minibatch logic."""
        if custom_logic is None:
            return None

        def collate_fn(batch):
            # Default collation
            data = torch.stack([item[0] for item in batch])
            targets = torch.tensor([item[1] for item in batch])
            return data, targets

        return collate_fn

    def get_train_loader(self) -> DataLoader:
        """Return training data loader."""
        return DataLoader(
            self.train_dataset,
            batch_size=self.batch_size,
            shuffle=True,
            num_workers=self.num_workers,
            pin_memory=torch.cuda.is_available(),
            collate_fn=self._get_collate_fn(self.train_custom_logic)
        )

    def get_val_loader(self) -> DataLoader:
        """Return validation data loader."""
        return DataLoader(
            self.val_dataset,
            batch_size=self.batch_size,
            shuffle=False,
            num_workers=self.num_workers,
            pin_memory=torch.cuda.is_available(),
            collate_fn=self._get_collate_fn(self.val_custom_logic)
        )

    def get_test_loader(self) -> DataLoader:
        """Return test data loader."""
        return DataLoader(
            self.test_dataset,
            batch_size=self.batch_size,
            shuffle=False,
            num_workers=self.num_workers,
            pin_memory=torch.cuda.is_available()
        )

    def get_num_classes(self) -> int:
        """Return number of classes."""
        return 10

    def get_config(self) -> Dict[str, Any]:
        """Return configuration."""
        return {
            'batch_size': self.batch_size,
            'num_workers': self.num_workers,
            'download': self.download,
            'data_dir': str(self.data_dir)
        }
