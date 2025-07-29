"""
Quantum-Enhanced GANs Pro

A cutting-edge quantum-enhanced generative adversarial network framework
that leverages quantum computing techniques to improve fidelity, diversity,
and fairness of synthetic data generation.

Author: Krishna Bajpai
Email: bajpaikrishna715@gmail.com
GitHub: https://github.com/krish567366/quantum-generative-adversarial-networks-pro
"""

__version__ = "0.1.0"
__author__ = "Krishna Bajpai"
__email__ = "bajpaikrishna715@gmail.com"

# Core imports
from .models.quantum_generator import QuantumGenerator
from .models.quantum_discriminator import QuantumDiscriminator
from .models.classical_generator import ClassicalGenerator
from .models.classical_discriminator import ClassicalDiscriminator
from .training.trainer import QuantumGAN, HybridGAN
from .losses.quantum_losses import QuantumWassersteinLoss, QuantumHingeLoss
from .utils.metrics import FIDScore, InceptionScore, QuantumFidelity
from .utils.data_loaders import get_data_loader, prepare_quantum_data

# Backend imports
from .backends import QiskitBackend, PennyLaneBackend

__all__ = [
    # Models
    "QuantumGenerator",
    "QuantumDiscriminator", 
    "ClassicalGenerator",
    "ClassicalDiscriminator",
    
    # Training
    "QuantumGAN",
    "HybridGAN",
    
    # Losses
    "QuantumWassersteinLoss",
    "QuantumHingeLoss",
    
    # Metrics
    "FIDScore",
    "InceptionScore", 
    "QuantumFidelity",
    
    # Utils
    "get_data_loader",
    "prepare_quantum_data",
    
    # Backends
    "QiskitBackend",
    "PennyLaneBackend",
]
