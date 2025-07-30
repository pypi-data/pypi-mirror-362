"""
Quantum backends for the QGANS Pro framework.
Provides abstractions for different quantum computing backends.
"""

from .base import QuantumBackend
from .qiskit_backend import QiskitBackend
from .pennylane_backend import PennyLaneBackend

__all__ = ["QuantumBackend", "QiskitBackend", "PennyLaneBackend"]
