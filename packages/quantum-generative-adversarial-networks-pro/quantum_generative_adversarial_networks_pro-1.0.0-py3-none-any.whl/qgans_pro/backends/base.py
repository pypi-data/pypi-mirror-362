"""
Base quantum backend interface for QGANS Pro.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple, Union
import numpy as np
import torch


class QuantumBackend(ABC):
    """
    Abstract base class for quantum computing backends.
    
    This class defines the interface that all quantum backends must implement
    to work with the QGANS Pro framework.
    """
    
    def __init__(self, device: str = "default", **kwargs):
        """
        Initialize the quantum backend.
        
        Args:
            device: The device to run quantum computations on
            **kwargs: Backend-specific configuration parameters
        """
        self.device = device
        self.config = kwargs
        self._circuit = None
        
    @abstractmethod
    def create_circuit(self, n_qubits: int, n_layers: int) -> Any:
        """
        Create a parameterized quantum circuit.
        
        Args:
            n_qubits: Number of qubits in the circuit
            n_layers: Number of layers in the circuit
            
        Returns:
            The quantum circuit object
        """
        pass
    
    @abstractmethod
    def add_rotation_layer(self, circuit: Any, params: torch.Tensor, layer_idx: int) -> Any:
        """
        Add a rotation layer to the quantum circuit.
        
        Args:
            circuit: The quantum circuit
            params: Parameters for the rotation gates
            layer_idx: Index of the current layer
            
        Returns:
            Updated circuit
        """
        pass
    
    @abstractmethod
    def add_entangling_layer(self, circuit: Any, layer_idx: int) -> Any:
        """
        Add an entangling layer to the quantum circuit.
        
        Args:
            circuit: The quantum circuit
            layer_idx: Index of the current layer
            
        Returns:
            Updated circuit
        """
        pass
    
    @abstractmethod
    def execute_circuit(self, circuit: Any, shots: int = 1024) -> torch.Tensor:
        """
        Execute the quantum circuit and return measurement results.
        
        Args:
            circuit: The quantum circuit to execute
            shots: Number of measurement shots
            
        Returns:
            Measurement probabilities as a tensor
        """
        pass
    
    @abstractmethod
    def get_statevector(self, circuit: Any) -> torch.Tensor:
        """
        Get the statevector of the quantum circuit.
        
        Args:
            circuit: The quantum circuit
            
        Returns:
            Complex statevector as a tensor
        """
        pass
    
    @abstractmethod
    def compute_expectation(self, circuit: Any, observable: Any) -> torch.Tensor:
        """
        Compute expectation value of an observable.
        
        Args:
            circuit: The quantum circuit
            observable: The observable to measure
            
        Returns:
            Expectation value
        """
        pass
    
    def set_parameters(self, circuit: Any, params: torch.Tensor) -> Any:
        """
        Set parameters in the quantum circuit.
        
        Args:
            circuit: The quantum circuit
            params: Parameter values
            
        Returns:
            Updated circuit with parameters set
        """
        # Default implementation - can be overridden by specific backends
        return circuit
    
    def get_device_info(self) -> Dict[str, Any]:
        """
        Get information about the quantum device.
        
        Returns:
            Dictionary containing device information
        """
        return {
            "backend_name": self.__class__.__name__,
            "device": self.device,
            "config": self.config
        }
    
    def is_simulator(self) -> bool:
        """
        Check if the backend is a simulator.
        
        Returns:
            True if simulator, False if real hardware
        """
        return "simulator" in self.device.lower() or "sim" in self.device.lower()
    
    def supports_gradients(self) -> bool:
        """
        Check if the backend supports automatic differentiation.
        
        Returns:
            True if gradients are supported
        """
        # Default implementation - override in specific backends
        return True
