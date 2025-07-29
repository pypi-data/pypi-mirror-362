"""
Data loading utilities for QGANS Pro.

This module provides utilities for loading and preprocessing datasets
for training quantum and classical GANs.
"""

from typing import Any, Dict, List, Optional, Tuple, Union, Callable
import numpy as np
import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader, Dataset, random_split
import torchvision.transforms as transforms
from torch.utils.data import TensorDataset

try:
    import torchvision.datasets as datasets
    TORCHVISION_AVAILABLE = True
except ImportError:
    TORCHVISION_AVAILABLE = False

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False


class QuantumDataPreprocessor:
    """
    Preprocessor for preparing data for quantum GANs.
    
    This class handles data normalization, encoding, and other transformations
    needed for quantum circuit compatibility.
    """
    
    def __init__(
        self,
        normalization: str = "minmax",
        target_range: Tuple[float, float] = (-1, 1),
        encoding_type: str = "amplitude",
    ):
        """
        Initialize quantum data preprocessor.
        
        Args:
            normalization: Normalization method ('minmax', 'standard', 'tanh')
            target_range: Target range for normalized data
            encoding_type: Quantum encoding type ('amplitude', 'angle', 'basis')
        """
        self.normalization = normalization
        self.target_range = target_range
        self.encoding_type = encoding_type
        
        # Statistics for normalization
        self.data_min = None
        self.data_max = None
        self.data_mean = None
        self.data_std = None
        self.fitted = False
    
    def fit(self, data: torch.Tensor):
        """
        Fit preprocessor to data.
        
        Args:
            data: Training data to fit on
        """
        if self.normalization == "minmax":
            self.data_min = torch.min(data)
            self.data_max = torch.max(data)
        elif self.normalization == "standard":
            self.data_mean = torch.mean(data)
            self.data_std = torch.std(data)
        
        self.fitted = True
    
    def transform(self, data: torch.Tensor) -> torch.Tensor:
        """
        Transform data using fitted parameters.
        
        Args:
            data: Data to transform
            
        Returns:
            Transformed data
        """
        if not self.fitted:
            raise RuntimeError("Preprocessor must be fitted before transform")
        
        if self.normalization == "minmax":
            # Min-max normalization
            normalized = (data - self.data_min) / (self.data_max - self.data_min + 1e-8)
            # Scale to target range
            normalized = normalized * (self.target_range[1] - self.target_range[0]) + self.target_range[0]
            
        elif self.normalization == "standard":
            # Z-score normalization
            normalized = (data - self.data_mean) / (self.data_std + 1e-8)
            # Clip to target range
            normalized = torch.clamp(normalized, self.target_range[0], self.target_range[1])
            
        elif self.normalization == "tanh":
            # Tanh normalization
            normalized = torch.tanh(data)
            
        else:
            normalized = data
        
        # Apply quantum encoding if needed
        if self.encoding_type == "amplitude":
            # Ensure data is suitable for amplitude encoding
            normalized = F.normalize(normalized, p=2, dim=-1)
            
        elif self.encoding_type == "angle":
            # Map to angle range [0, 2π]
            normalized = (normalized - self.target_range[0]) / (self.target_range[1] - self.target_range[0])
            normalized = normalized * 2 * np.pi
        
        return normalized
    
    def fit_transform(self, data: torch.Tensor) -> torch.Tensor:
        """
        Fit and transform data in one step.
        
        Args:
            data: Data to fit and transform
            
        Returns:
            Transformed data
        """
        self.fit(data)
        return self.transform(data)
    
    def inverse_transform(self, data: torch.Tensor) -> torch.Tensor:
        """
        Inverse transform data back to original scale.
        
        Args:
            data: Transformed data
            
        Returns:
            Data in original scale
        """
        if not self.fitted:
            raise RuntimeError("Preprocessor must be fitted before inverse transform")
        
        # Reverse quantum encoding
        if self.encoding_type == "angle":
            # Map back from angle range
            data = data / (2 * np.pi)
            data = data * (self.target_range[1] - self.target_range[0]) + self.target_range[0]
        
        # Reverse normalization
        if self.normalization == "minmax":
            # Reverse min-max normalization
            data = (data - self.target_range[0]) / (self.target_range[1] - self.target_range[0])
            data = data * (self.data_max - self.data_min) + self.data_min
            
        elif self.normalization == "standard":
            # Reverse z-score normalization
            data = data * self.data_std + self.data_mean
        
        return data


def get_data_loader(
    dataset_name: str,
    batch_size: int = 64,
    train: bool = True,
    download: bool = True,
    data_dir: str = "./data",
    transform: Optional[Callable] = None,
    quantum_preprocess: bool = False,
    **kwargs
) -> DataLoader:
    """
    Get data loader for specified dataset.
    
    Args:
        dataset_name: Name of dataset ('mnist', 'fashion-mnist', 'cifar10', 'celeba', 'custom')
        batch_size: Batch size for data loader
        train: Whether to load training or test set
        download: Whether to download dataset if not present
        data_dir: Directory to store/load data
        transform: Optional custom transform
        quantum_preprocess: Whether to apply quantum preprocessing
        **kwargs: Additional arguments for dataset loading
        
    Returns:
        DataLoader for the specified dataset
    """
    if not TORCHVISION_AVAILABLE and dataset_name in ['mnist', 'fashion-mnist', 'cifar10']:
        raise ImportError("torchvision is required for image datasets")
    
    # Default transforms
    if transform is None:
        if dataset_name in ['mnist', 'fashion-mnist']:
            transform = transforms.Compose([
                transforms.ToTensor(),
                transforms.Normalize((0.5,), (0.5,))
            ])
        elif dataset_name == 'cifar10':
            transform = transforms.Compose([
                transforms.ToTensor(),
                transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
            ])
        else:
            transform = transforms.ToTensor()
    
    # Load dataset
    if dataset_name.lower() == 'mnist':
        dataset = datasets.MNIST(
            root=data_dir,
            train=train,
            download=download,
            transform=transform
        )
        
    elif dataset_name.lower() == 'fashion-mnist':
        dataset = datasets.FashionMNIST(
            root=data_dir,
            train=train,
            download=download,
            transform=transform
        )
        
    elif dataset_name.lower() == 'cifar10':
        dataset = datasets.CIFAR10(
            root=data_dir,
            train=train,
            download=download,
            transform=transform
        )
        
    elif dataset_name.lower() == 'celeba':
        # CelebA dataset (requires manual download)
        dataset = datasets.CelebA(
            root=data_dir,
            split='train' if train else 'test',
            download=download,
            transform=transform
        )
        
    else:
        raise ValueError(f"Unsupported dataset: {dataset_name}")
    
    # Apply quantum preprocessing if requested
    if quantum_preprocess:
        dataset = QuantumDataset(dataset)
    
    # Create data loader
    data_loader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=train,
        num_workers=kwargs.get('num_workers', 0),
        pin_memory=kwargs.get('pin_memory', True),
        drop_last=kwargs.get('drop_last', True)
    )
    
    return data_loader


class QuantumDataset(Dataset):
    """
    Wrapper dataset that applies quantum preprocessing.
    
    This dataset wrapper automatically applies quantum-compatible
    preprocessing to the underlying dataset.
    """
    
    def __init__(
        self,
        base_dataset: Dataset,
        quantum_preprocessor: Optional[QuantumDataPreprocessor] = None
    ):
        """
        Initialize quantum dataset wrapper.
        
        Args:
            base_dataset: Underlying dataset
            quantum_preprocessor: Quantum preprocessor to apply
        """
        self.base_dataset = base_dataset
        
        if quantum_preprocessor is None:
            quantum_preprocessor = QuantumDataPreprocessor()
        
        self.preprocessor = quantum_preprocessor
        self._fit_preprocessor()
    
    def _fit_preprocessor(self):
        """Fit preprocessor to the dataset."""
        # Sample some data to fit preprocessor
        sample_size = min(1000, len(self.base_dataset))
        sample_indices = torch.randperm(len(self.base_dataset))[:sample_size]
        
        sample_data = []
        for idx in sample_indices:
            data, _ = self.base_dataset[idx]
            sample_data.append(data.flatten())
        
        sample_tensor = torch.stack(sample_data)
        self.preprocessor.fit(sample_tensor)
    
    def __len__(self):
        return len(self.base_dataset)
    
    def __getitem__(self, idx):
        data, label = self.base_dataset[idx]
        
        # Apply quantum preprocessing
        data_flat = data.flatten()
        processed_data = self.preprocessor.transform(data_flat.unsqueeze(0))[0]
        
        # Reshape back to original shape if possible
        try:
            processed_data = processed_data.reshape(data.shape)
        except:
            # Keep flattened if reshaping fails
            pass
        
        return processed_data, label


def prepare_quantum_data(
    data: torch.Tensor,
    n_qubits: int,
    encoding_type: str = "amplitude"
) -> torch.Tensor:
    """
    Prepare classical data for quantum encoding.
    
    Args:
        data: Classical data tensor
        n_qubits: Number of qubits available
        encoding_type: Type of quantum encoding
        
    Returns:
        Quantum-ready data
    """
    batch_size = data.shape[0]
    data_flat = data.view(batch_size, -1)
    data_dim = data_flat.shape[1]
    
    # Determine quantum data dimension
    if encoding_type == "amplitude":
        # Amplitude encoding requires data dimension <= 2^n_qubits
        max_dim = 2 ** n_qubits
        
        if data_dim > max_dim:
            # Reduce dimensionality
            quantum_data = data_flat[:, :max_dim]
        elif data_dim < max_dim:
            # Pad with zeros
            padding = torch.zeros(batch_size, max_dim - data_dim, device=data.device)
            quantum_data = torch.cat([data_flat, padding], dim=1)
        else:
            quantum_data = data_flat
        
        # Normalize for amplitude encoding
        quantum_data = F.normalize(quantum_data, p=2, dim=1)
        
    elif encoding_type == "angle":
        # Angle encoding: one angle per qubit
        if data_dim > n_qubits:
            # Reduce to n_qubits dimensions
            quantum_data = data_flat[:, :n_qubits]
        elif data_dim < n_qubits:
            # Pad with zeros
            padding = torch.zeros(batch_size, n_qubits - data_dim, device=data.device)
            quantum_data = torch.cat([data_flat, padding], dim=1)
        else:
            quantum_data = data_flat
        
        # Map to angle range [0, 2π]
        quantum_data = torch.sigmoid(quantum_data) * 2 * np.pi
        
    else:
        # Default: truncate or pad to match qubit count
        if data_dim > n_qubits:
            quantum_data = data_flat[:, :n_qubits]
        elif data_dim < n_qubits:
            padding = torch.zeros(batch_size, n_qubits - data_dim, device=data.device)
            quantum_data = torch.cat([data_flat, padding], dim=1)
        else:
            quantum_data = data_flat
    
    return quantum_data


def load_tabular_data(
    file_path: str,
    target_column: Optional[str] = None,
    test_size: float = 0.2,
    random_state: int = 42,
    **kwargs
) -> Tuple[DataLoader, DataLoader]:
    """
    Load tabular data from CSV file.
    
    Args:
        file_path: Path to CSV file
        target_column: Name of target column (if any)
        test_size: Fraction of data for testing
        random_state: Random seed
        **kwargs: Additional arguments for DataLoader
        
    Returns:
        Tuple of (train_loader, test_loader)
    """
    if not PANDAS_AVAILABLE:
        raise ImportError("pandas is required for loading tabular data")
    
    # Load data
    df = pd.read_csv(file_path)
    
    # Separate features and target
    if target_column and target_column in df.columns:
        X = df.drop(columns=[target_column])
        y = df[target_column]
    else:
        X = df
        y = torch.zeros(len(df))  # Dummy labels
    
    # Convert to tensors
    X_tensor = torch.tensor(X.values, dtype=torch.float32)
    y_tensor = torch.tensor(y.values if hasattr(y, 'values') else y, dtype=torch.long)
    
    # Create dataset
    dataset = TensorDataset(X_tensor, y_tensor)
    
    # Split into train/test
    train_size = int((1 - test_size) * len(dataset))
    test_size = len(dataset) - train_size
    
    train_dataset, test_dataset = random_split(
        dataset, [train_size, test_size],
        generator=torch.Generator().manual_seed(random_state)
    )
    
    # Create data loaders
    batch_size = kwargs.get('batch_size', 64)
    num_workers = kwargs.get('num_workers', 0)
    
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=True
    )
    
    test_loader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True
    )
    
    return train_loader, test_loader


def create_synthetic_dataset(
    n_samples: int = 10000,
    n_features: int = 10,
    dataset_type: str = "gaussian",
    **kwargs
) -> DataLoader:
    """
    Create synthetic dataset for testing.
    
    Args:
        n_samples: Number of samples
        n_features: Number of features
        dataset_type: Type of synthetic data ('gaussian', 'uniform', 'bimodal')
        **kwargs: Additional parameters
        
    Returns:
        DataLoader for synthetic dataset
    """
    if dataset_type == "gaussian":
        # Gaussian distribution
        mean = kwargs.get('mean', 0.0)
        std = kwargs.get('std', 1.0)
        data = torch.randn(n_samples, n_features) * std + mean
        
    elif dataset_type == "uniform":
        # Uniform distribution
        low = kwargs.get('low', -1.0)
        high = kwargs.get('high', 1.0)
        data = torch.rand(n_samples, n_features) * (high - low) + low
        
    elif dataset_type == "bimodal":
        # Bimodal distribution
        # Half samples from each mode
        n_half = n_samples // 2
        
        data1 = torch.randn(n_half, n_features) * 0.5 - 1.0
        data2 = torch.randn(n_samples - n_half, n_features) * 0.5 + 1.0
        data = torch.cat([data1, data2], dim=0)
        
        # Shuffle
        perm = torch.randperm(n_samples)
        data = data[perm]
        
    else:
        raise ValueError(f"Unknown dataset type: {dataset_type}")
    
    # Create labels (dummy)
    labels = torch.zeros(n_samples, dtype=torch.long)
    
    # Create dataset and loader
    dataset = TensorDataset(data, labels)
    
    data_loader = DataLoader(
        dataset,
        batch_size=kwargs.get('batch_size', 64),
        shuffle=True,
        num_workers=kwargs.get('num_workers', 0),
        pin_memory=True
    )
    
    return data_loader
