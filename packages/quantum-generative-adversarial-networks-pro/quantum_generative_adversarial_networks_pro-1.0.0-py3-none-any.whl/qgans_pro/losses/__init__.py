"""
Quantum-compatible loss functions for QGANS Pro.
"""

from .quantum_losses import QuantumWassersteinLoss, QuantumHingeLoss, QuantumBCELoss

__all__ = ["QuantumWassersteinLoss", "QuantumHingeLoss", "QuantumBCELoss"]
