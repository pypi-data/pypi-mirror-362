"""
Qiskit backend implementation for QGANS Pro.
"""

from typing import Any, Dict, List, Optional, Tuple, Union
import numpy as np
import torch

try:
    from qiskit import QuantumCircuit, transpile
    from qiskit.circuit import Parameter, ParameterVector
    from qiskit.primitives import Sampler, Estimator
    from qiskit.quantum_info import SparsePauliOp, Statevector
    from qiskit_aer import AerSimulator
    from qiskit.visualization import plot_circuit_layout
    QISKIT_AVAILABLE = True
except ImportError:
    QISKIT_AVAILABLE = False

from .base import QuantumBackend


class QiskitBackend(QuantumBackend):
    """
    Qiskit implementation of the quantum backend.
    
    This backend uses IBM's Qiskit framework for quantum circuit construction
    and execution.
    """
    
    def __init__(self, device: str = "aer_simulator", **kwargs):
        """
        Initialize the Qiskit backend.
        
        Args:
            device: Qiskit device/backend name
            **kwargs: Additional Qiskit configuration
        """
        if not QISKIT_AVAILABLE:
            raise ImportError(
                "Qiskit is required for QiskitBackend. "
                "Please install it with: pip install qiskit qiskit-aer"
            )
        
        super().__init__(device, **kwargs)
        
        # Initialize the backend
        if device == "aer_simulator" or device == "default":
            self.backend = AerSimulator()
        else:
            # For real hardware, you would load the backend from IBMQ
            # For now, default to simulator
            self.backend = AerSimulator()
        
        # Initialize primitives
        self.sampler = Sampler()
        self.estimator = Estimator()
        
    def create_circuit(self, n_qubits: int, n_layers: int) -> QuantumCircuit:
        """
        Create a parameterized quantum circuit.
        
        Args:
            n_qubits: Number of qubits
            n_layers: Number of layers
            
        Returns:
            Parameterized QuantumCircuit
        """
        # Create parameter vectors for different gate types
        n_rotation_params = n_qubits * n_layers * 3  # RX, RY, RZ for each qubit
        
        # Create parameter vector
        params = ParameterVector('θ', n_rotation_params)
        
        # Create quantum circuit
        qc = QuantumCircuit(n_qubits)
        
        param_idx = 0
        
        # Build the variational circuit
        for layer in range(n_layers):
            # Rotation layer - RX, RY, RZ on each qubit
            for qubit in range(n_qubits):
                qc.rx(params[param_idx], qubit)
                param_idx += 1
                qc.ry(params[param_idx], qubit)  
                param_idx += 1
                qc.rz(params[param_idx], qubit)
                param_idx += 1
            
            # Entangling layer - CNOT gates
            if layer < n_layers - 1:  # No entangling after last layer
                self.add_entangling_layer(qc, layer)
        
        # Store parameter information
        qc._qgans_params = params
        qc._qgans_n_params = n_rotation_params
        
        return qc
    
    def add_rotation_layer(self, circuit: QuantumCircuit, params: torch.Tensor, layer_idx: int) -> QuantumCircuit:
        """
        Add rotation gates to the circuit.
        
        Args:
            circuit: Quantum circuit
            params: Rotation parameters
            layer_idx: Layer index
            
        Returns:
            Updated circuit
        """
        n_qubits = circuit.num_qubits
        start_idx = layer_idx * n_qubits * 3
        
        for qubit in range(n_qubits):
            base_idx = start_idx + qubit * 3
            circuit.rx(params[base_idx].item(), qubit)
            circuit.ry(params[base_idx + 1].item(), qubit)
            circuit.rz(params[base_idx + 2].item(), qubit)
            
        return circuit
    
    def add_entangling_layer(self, circuit: QuantumCircuit, layer_idx: int) -> QuantumCircuit:
        """
        Add entangling CNOT gates.
        
        Args:
            circuit: Quantum circuit
            layer_idx: Layer index
            
        Returns:
            Updated circuit
        """
        n_qubits = circuit.num_qubits
        
        # Circular entangling pattern
        for qubit in range(n_qubits):
            control = qubit
            target = (qubit + 1) % n_qubits
            circuit.cx(control, target)
            
        return circuit
    
    def execute_circuit(self, circuit: QuantumCircuit, shots: int = 1024) -> torch.Tensor:
        """
        Execute circuit and return measurement probabilities.
        
        Args:
            circuit: Quantum circuit
            shots: Number of shots
            
        Returns:
            Measurement probabilities
        """
        # Add measurements if not present
        if circuit.num_clbits == 0:
            circuit.add_register(ClassicalRegister(circuit.num_qubits))
            circuit.measure_all()
        
        # Execute using Sampler primitive
        job = self.sampler.run([circuit], shots=shots)
        result = job.result()
        
        # Convert to probabilities
        counts = result.quasi_dists[0]
        n_outcomes = 2 ** circuit.num_qubits
        probs = np.zeros(n_outcomes)
        
        for outcome, prob in counts.items():
            probs[outcome] = prob
            
        return torch.tensor(probs, dtype=torch.float32)
    
    def get_statevector(self, circuit: QuantumCircuit) -> torch.Tensor:
        """
        Get the statevector of the circuit.
        
        Args:
            circuit: Quantum circuit
            
        Returns:
            Complex statevector
        """
        # Use Qiskit's statevector simulator
        sv_sim = AerSimulator(method='statevector')
        
        # Transpile and run
        transpiled = transpile(circuit, sv_sim)
        job = sv_sim.run(transpiled)
        result = job.result()
        
        # Get statevector
        statevector = result.get_statevector()
        
        # Convert to torch tensor
        sv_array = np.array(statevector.data)
        return torch.tensor(sv_array, dtype=torch.complex64)
    
    def compute_expectation(self, circuit: QuantumCircuit, observable: SparsePauliOp) -> torch.Tensor:
        """
        Compute expectation value of observable.
        
        Args:
            circuit: Quantum circuit
            observable: Pauli observable
            
        Returns:
            Expectation value
        """
        # Use Estimator primitive
        job = self.estimator.run([circuit], [observable])
        result = job.result()
        
        expectation = result.values[0]
        return torch.tensor(expectation, dtype=torch.float32)
    
    def set_parameters(self, circuit: QuantumCircuit, params: torch.Tensor) -> QuantumCircuit:
        """
        Bind parameters to the circuit.
        
        Args:
            circuit: Parameterized circuit
            params: Parameter values
            
        Returns:
            Circuit with bound parameters
        """
        if hasattr(circuit, '_qgans_params'):
            # Create parameter binding dictionary
            param_dict = {}
            for i, param in enumerate(circuit._qgans_params):
                if i < len(params):
                    param_dict[param] = params[i].item()
            
            # Bind parameters
            bound_circuit = circuit.bind_parameters(param_dict)
            return bound_circuit
        
        return circuit
    
    def get_device_info(self) -> Dict[str, Any]:
        """
        Get Qiskit backend information.
        
        Returns:
            Device information dictionary
        """
        info = super().get_device_info()
        info.update({
            "backend_name": "QiskitBackend",
            "qiskit_backend": str(self.backend),
            "n_qubits": getattr(self.backend, 'num_qubits', 'unlimited'),
            "simulator": self.is_simulator(),
        })
        return info
    
    def supports_gradients(self) -> bool:
        """
        Check gradient support for Qiskit.
        
        Returns:
            True (Qiskit supports parameter shift gradients)
        """
        return True
    
    def visualize_circuit(self, circuit: QuantumCircuit, filename: Optional[str] = None):
        """
        Visualize the quantum circuit.
        
        Args:
            circuit: Circuit to visualize
            filename: Optional filename to save visualization
        """
        try:
            from matplotlib import pyplot as plt
            
            fig = circuit.draw(output='mpl', style='iqp')
            
            if filename:
                plt.savefig(filename, dpi=300, bbox_inches='tight')
            else:
                plt.show()
                
        except ImportError:
            print("Matplotlib not available for circuit visualization")
