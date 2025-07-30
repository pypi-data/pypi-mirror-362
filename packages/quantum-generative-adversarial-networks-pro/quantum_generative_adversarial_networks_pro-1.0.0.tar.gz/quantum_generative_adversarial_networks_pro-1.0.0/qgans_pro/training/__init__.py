"""
Training module for QGANS Pro.
Contains GAN trainers for quantum, classical, and hybrid models.
"""

from .trainer import QuantumGAN, HybridGAN, ClassicalGAN

__all__ = ["QuantumGAN", "HybridGAN", "ClassicalGAN"]
