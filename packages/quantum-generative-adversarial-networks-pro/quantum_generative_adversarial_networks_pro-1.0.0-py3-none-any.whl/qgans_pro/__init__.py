"""
Quantum-Enhanced GANs Pro

A cutting-edge quantum-enhanced generative adversarial network framework
that leverages quantum computing techniques to improve fidelity, diversity,
and fairness of synthetic data generation.

Author: Krishna Bajpai
Email: bajpaikrishna715@gmail.com
GitHub: https://github.com/krish567366/quantum-generative-adversarial-networks-pro

⚠️  LICENSE REQUIRED: This package requires a valid license to use.
📧 Contact bajpaikrishna715@gmail.com for licensing information.
"""

# License validation - MUST BE FIRST
from .license import validate_package_license, create_license_request, get_machine_id

__version__ = "0.1.0"
__author__ = "Krishna Bajpai"
__email__ = "bajpaikrishna715@gmail.com"
__license_package__ = "quantum-generative-adversarial-networks-pro"

# Package-level license validation on import
if not validate_package_license():
    print("\n🔐 Quantum GANs Pro - License Required")
    print("=" * 50)
    print("This package requires a valid license to use.")
    print(f"📧 Contact: {__email__}")
    print(f"🔧 Your Machine ID: {get_machine_id()}")
    print("\n💡 To create a license request:")
    print("python -c \"from qgans_pro.license import create_license_request; create_license_request()\"")
    print("=" * 50)
    raise ImportError("Valid license required for Quantum GANs Pro")

# Core imports (only after license validation)
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
