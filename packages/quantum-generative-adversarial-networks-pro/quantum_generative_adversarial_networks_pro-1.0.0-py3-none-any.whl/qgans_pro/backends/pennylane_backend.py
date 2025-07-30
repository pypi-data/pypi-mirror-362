"""
PennyLane backend implementation for QGANS Pro.
"""

from typing import Any, Dict, List, Optional, Tuple, Union
import numpy as np
import torch

try:
    import pennylane as qml
    from pennylane import numpy as pnp
    PENNYLANE_AVAILABLE = True
except ImportError:
    PENNYLANE_AVAILABLE = False

from .base import QuantumBackend


class PennyLaneBackend(QuantumBackend):
    """
    PennyLane implementation of the quantum backend.
    
    This backend uses Xanadu's PennyLane framework for quantum machine learning
    with automatic differentiation support.
    """
    
    def __init__(self, device: str = "default.qubit", **kwargs):
        """
        Initialize the PennyLane backend.
        
        Args:
            device: PennyLane device name
            **kwargs: Additional device configuration
        """
        if not PENNYLANE_AVAILABLE:
            raise ImportError(
                "PennyLane is required for PennyLaneBackend. "
                "Please install it with: pip install pennylane"
            )
        
        super().__init__(device, **kwargs)
        
        # Store device configuration for later use
        self.device_name = device
        self.device_kwargs = kwargs
        self._device = None
        self._qnode = None
        
    def _get_device(self, n_qubits: int):
        """Get or create PennyLane device."""
        if self._device is None or self._device.num_wires != n_qubits:
            self._device = qml.device(self.device_name, wires=n_qubits, **self.device_kwargs)
        return self._device
    
    def create_circuit(self, n_qubits: int, n_layers: int) -> callable:
        """
        Create a parameterized quantum circuit function.
        
        Args:
            n_qubits: Number of qubits
            n_layers: Number of layers
            
        Returns:
            Circuit function that can be used as QNode
        """
        def circuit(params):
            """Parameterized quantum circuit."""
            param_idx = 0
            
            # Build the variational circuit
            for layer in range(n_layers):
                # Rotation layer - RX, RY, RZ on each qubit
                for qubit in range(n_qubits):
                    qml.RX(params[param_idx], wires=qubit)
                    param_idx += 1
                    qml.RY(params[param_idx], wires=qubit)
                    param_idx += 1
                    qml.RZ(params[param_idx], wires=qubit)
                    param_idx += 1
                
                # Entangling layer - CNOT gates
                if layer < n_layers - 1:
                    for qubit in range(n_qubits):
                        control = qubit
                        target = (qubit + 1) % n_qubits
                        qml.CNOT(wires=[control, target])
            
            return qml.probs(wires=range(n_qubits))
        
        # Store circuit metadata
        circuit._qgans_n_qubits = n_qubits
        circuit._qgans_n_layers = n_layers
        circuit._qgans_n_params = n_qubits * n_layers * 3
        
        return circuit
    
    def add_rotation_layer(self, circuit: callable, params: torch.Tensor, layer_idx: int) -> callable:
        """
        This method is handled within the circuit function for PennyLane.
        
        Args:
            circuit: Circuit function
            params: Parameters
            layer_idx: Layer index
            
        Returns:
            Circuit function (unchanged for PennyLane)
        """
        return circuit
    
    def add_entangling_layer(self, circuit: callable, layer_idx: int) -> callable:
        """
        This method is handled within the circuit function for PennyLane.
        
        Args:
            circuit: Circuit function
            layer_idx: Layer index
            
        Returns:
            Circuit function (unchanged for PennyLane)
        """
        return circuit
    
    def execute_circuit(self, circuit: callable, shots: int = 1024) -> torch.Tensor:
        """
        Execute circuit and return measurement probabilities.
        
        Args:
            circuit: Circuit function
            shots: Number of shots (for finite shots simulation)
            
        Returns:
            Measurement probabilities
        """
        n_qubits = circuit._qgans_n_qubits
        device = self._get_device(n_qubits)
        
        # Set shots if device supports it
        if hasattr(device, 'shots') and shots != device.shots:
            device = qml.device(self.device_name, wires=n_qubits, shots=shots, **self.device_kwargs)
        
        # Create QNode
        qnode = qml.QNode(circuit, device, interface='torch')
        
        # Return the circuit function that computes probabilities
        def executor(params):
            return qnode(params)
        
        return executor
    
    def get_statevector(self, circuit: callable) -> callable:
        """
        Get a function that returns the statevector.
        
        Args:
            circuit: Circuit function
            
        Returns:
            Function that returns statevector
        """
        n_qubits = circuit._qgans_n_qubits
        
        # Create statevector circuit
        def sv_circuit(params):
            param_idx = 0
            n_layers = circuit._qgans_n_layers
            
            for layer in range(n_layers):
                for qubit in range(n_qubits):
                    qml.RX(params[param_idx], wires=qubit)
                    param_idx += 1
                    qml.RY(params[param_idx], wires=qubit)
                    param_idx += 1
                    qml.RZ(params[param_idx], wires=qubit)
                    param_idx += 1
                
                if layer < n_layers - 1:
                    for qubit in range(n_qubits):
                        control = qubit
                        target = (qubit + 1) % n_qubits
                        qml.CNOT(wires=[control, target])
            
            return qml.state()
        
        # Use statevector device
        sv_device = qml.device('default.qubit', wires=n_qubits)
        qnode = qml.QNode(sv_circuit, sv_device, interface='torch')
        
        return qnode
    
    def compute_expectation(self, circuit: callable, observable: Any) -> callable:
        """
        Create function to compute expectation value.
        
        Args:
            circuit: Circuit function
            observable: PennyLane observable
            
        Returns:
            Function that computes expectation value
        """
        n_qubits = circuit._qgans_n_qubits
        device = self._get_device(n_qubits)
        
        def exp_circuit(params):
            param_idx = 0
            n_layers = circuit._qgans_n_layers
            
            for layer in range(n_layers):
                for qubit in range(n_qubits):
                    qml.RX(params[param_idx], wires=qubit)
                    param_idx += 1
                    qml.RY(params[param_idx], wires=qubit)
                    param_idx += 1
                    qml.RZ(params[param_idx], wires=qubit)
                    param_idx += 1
                
                if layer < n_layers - 1:
                    for qubit in range(n_qubits):
                        control = qubit
                        target = (qubit + 1) % n_qubits
                        qml.CNOT(wires=[control, target])
            
            return qml.expval(observable)
        
        qnode = qml.QNode(exp_circuit, device, interface='torch')
        return qnode
    
    def set_parameters(self, circuit: callable, params: torch.Tensor) -> callable:
        """
        For PennyLane, parameters are passed directly to the circuit.
        
        Args:
            circuit: Circuit function
            params: Parameters
            
        Returns:
            Circuit function (unchanged)
        """
        return circuit
    
    def get_device_info(self) -> Dict[str, Any]:
        """
        Get PennyLane device information.
        
        Returns:
            Device information dictionary
        """
        info = super().get_device_info()
        
        device_info = {
            "backend_name": "PennyLaneBackend",
            "pennylane_device": self.device_name,
            "simulator": self.is_simulator(),
            "supports_gradients": True,
        }
        
        if self._device:
            device_info.update({
                "n_qubits": self._device.num_wires,
                "shots": getattr(self._device, 'shots', None),
            })
        
        info.update(device_info)
        return info
    
    def supports_gradients(self) -> bool:
        """
        PennyLane has excellent gradient support.
        
        Returns:
            True
        """
        return True
    
    def create_qnode(self, circuit: callable, n_qubits: int, interface: str = 'torch') -> callable:
        """
        Create a PennyLane QNode.
        
        Args:
            circuit: Circuit function
            n_qubits: Number of qubits
            interface: ML interface ('torch', 'tf', 'jax', etc.)
            
        Returns:
            QNode function
        """
        device = self._get_device(n_qubits)
        return qml.QNode(circuit, device, interface=interface)
    
    def visualize_circuit(self, circuit: callable, params: torch.Tensor, filename: Optional[str] = None):
        """
        Visualize the quantum circuit.
        
        Args:
            circuit: Circuit function
            params: Parameters for the circuit
            filename: Optional filename to save visualization
        """
        try:
            n_qubits = circuit._qgans_n_qubits
            device = self._get_device(n_qubits)
            qnode = qml.QNode(circuit, device)
            
            # Draw the circuit
            fig, ax = qml.draw_mpl(qnode)(params)
            
            if filename:
                fig.savefig(filename, dpi=300, bbox_inches='tight')
            else:
                fig.show()
                
        except ImportError:
            print("Matplotlib not available for circuit visualization")
        except Exception as e:
            print(f"Circuit visualization failed: {e}")
    
    def get_gradient_fn(self, circuit: callable, n_qubits: int) -> callable:
        """
        Get gradient function for the circuit.
        
        Args:
            circuit: Circuit function
            n_qubits: Number of qubits
            
        Returns:
            Gradient function
        """
        device = self._get_device(n_qubits)
        qnode = qml.QNode(circuit, device, interface='torch')
        
        return qml.grad(qnode, argnum=0)
