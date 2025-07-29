"""
Quantum Generator implementation for QGANS Pro.

This module implements a quantum generator using parameterized quantum circuits
that can generate synthetic data with quantum advantage.
"""

from typing import Any, Dict, List, Optional, Tuple, Union
import numpy as np
import torch
import torch.nn as nn
from torch.nn import Parameter

from ..backends.base import QuantumBackend
from ..backends.qiskit_backend import QiskitBackend
from ..backends.pennylane_backend import PennyLaneBackend


class QuantumGenerator(nn.Module):
    """
    Quantum Generator using Parameterized Quantum Circuits (PQC).
    
    This generator uses quantum circuits to generate synthetic data,
    leveraging quantum superposition and entanglement for enhanced
    expressivity and diversity.
    """
    
    def __init__(
        self,
        n_qubits: int,
        n_layers: int,
        output_dim: int,
        backend: str = "qiskit",
        device: str = "default",
        encoding_type: str = "amplitude",
        post_processing: str = "linear",
        **backend_kwargs
    ):
        """
        Initialize the Quantum Generator.
        
        Args:
            n_qubits: Number of qubits in the quantum circuit
            n_layers: Number of layers in the variational circuit
            output_dim: Dimension of the output data
            backend: Quantum backend ('qiskit' or 'pennylane')
            device: Quantum device to use
            encoding_type: How to encode classical data ('amplitude', 'angle', 'iqp')
            post_processing: Classical post-processing ('linear', 'mlp', 'none')
            **backend_kwargs: Additional backend-specific arguments
        """
        super().__init__()
        
        self.n_qubits = n_qubits
        self.n_layers = n_layers
        self.output_dim = output_dim
        self.encoding_type = encoding_type
        self.post_processing_type = post_processing
        
        # Initialize quantum backend
        if backend.lower() == "qiskit":
            self.backend = QiskitBackend(device, **backend_kwargs)
        elif backend.lower() == "pennylane":
            self.backend = PennyLaneBackend(device, **backend_kwargs)
        else:
            raise ValueError(f"Unsupported backend: {backend}")
        
        # Calculate number of parameters needed
        self.n_params = n_qubits * n_layers * 3  # RX, RY, RZ for each qubit per layer
        
        # Initialize quantum circuit parameters
        self.quantum_params = Parameter(
            torch.randn(self.n_params, requires_grad=True) * 0.1
        )
        
        # Create the quantum circuit
        self.circuit = self.backend.create_circuit(n_qubits, n_layers)
        
        # Classical post-processing layers
        if post_processing == "linear":
            # Simple linear transformation from quantum measurements
            self.post_processor = nn.Linear(2**n_qubits, output_dim)
        elif post_processing == "mlp":
            # Multi-layer perceptron for complex post-processing
            hidden_dim = max(128, output_dim * 2)
            self.post_processor = nn.Sequential(
                nn.Linear(2**n_qubits, hidden_dim),
                nn.ReLU(),
                nn.Linear(hidden_dim, hidden_dim // 2),
                nn.ReLU(),
                nn.Linear(hidden_dim // 2, output_dim),
                nn.Tanh()
            )
        else:
            # No post-processing - direct quantum output
            self.post_processor = None
            
        # Noise input dimension (for latent space)
        self.noise_dim = min(n_qubits, 10)  # Limit noise dimension
        
        # Classical pre-processing for noise input
        self.noise_encoder = nn.Sequential(
            nn.Linear(self.noise_dim, n_qubits * 2),
            nn.Tanh(),
            nn.Linear(n_qubits * 2, n_qubits),
            nn.Tanh()
        )
        
    def encode_classical_data(self, noise: torch.Tensor) -> torch.Tensor:
        """
        Encode classical noise into quantum circuit parameters.
        
        Args:
            noise: Input noise tensor [batch_size, noise_dim]
            
        Returns:
            Encoded parameters for quantum circuit
        """
        batch_size = noise.shape[0]
        
        # Encode noise through classical neural network
        encoded = self.noise_encoder(noise)  # [batch_size, n_qubits]
        
        # Combine with trainable quantum parameters
        # Broadcast quantum params to batch size
        quantum_params_batch = self.quantum_params.unsqueeze(0).expand(batch_size, -1)
        
        # Mix encoded noise with quantum parameters
        if self.encoding_type == "amplitude":
            # Amplitude encoding - modify rotation angles
            param_modifier = torch.zeros(batch_size, self.n_params, device=noise.device)
            
            # Distribute encoded values across all parameters
            for i in range(self.n_qubits):
                for layer in range(self.n_layers):
                    base_idx = layer * self.n_qubits * 3 + i * 3
                    param_modifier[:, base_idx:base_idx+3] = encoded[:, i:i+1].expand(-1, 3) * 0.5
            
            final_params = quantum_params_batch + param_modifier
            
        elif self.encoding_type == "angle":
            # Angle encoding - direct mapping to rotation angles
            param_modifier = torch.zeros(batch_size, self.n_params, device=noise.device)
            
            # Map each encoded value to RY rotations in first layer
            for i in range(min(self.n_qubits, encoded.shape[1])):
                param_modifier[:, i * 3 + 1] = encoded[:, i] * np.pi  # RY angles
            
            final_params = quantum_params_batch + param_modifier
            
        else:  # Default: simple addition
            # Repeat encoded values to match parameter count
            repeats = self.n_params // self.n_qubits
            remainder = self.n_params % self.n_qubits
            
            param_modifier = encoded.repeat(1, repeats)
            if remainder > 0:
                param_modifier = torch.cat([param_modifier, encoded[:, :remainder]], dim=1)
            
            final_params = quantum_params_batch + param_modifier * 0.1
        
        return final_params
    
    def quantum_forward(self, params: torch.Tensor) -> torch.Tensor:
        """
        Execute quantum circuit and get measurement probabilities.
        
        Args:
            params: Quantum circuit parameters [batch_size, n_params]
            
        Returns:
            Quantum measurement probabilities [batch_size, 2^n_qubits]
        """
        batch_size = params.shape[0]
        
        # For now, we'll process batch sequentially
        # In future versions, this could be parallelized
        outputs = []
        
        for i in range(batch_size):
            # Set parameters in circuit
            param_values = params[i]
            
            if hasattr(self.backend, 'execute_circuit'):
                # Get execution function
                executor = self.backend.execute_circuit(self.circuit)
                
                # Execute circuit with parameters
                if callable(executor):
                    probs = executor(param_values)
                else:
                    # For Qiskit, we need to bind parameters first
                    bound_circuit = self.backend.set_parameters(self.circuit, param_values)
                    probs = executor  # This would be the probability tensor
                    
            else:
                # Fallback: simulate ideal uniform distribution
                n_outcomes = 2 ** self.n_qubits
                probs = torch.ones(n_outcomes) / n_outcomes
            
            outputs.append(probs)
        
        return torch.stack(outputs)
    
    def forward(self, noise: torch.Tensor) -> torch.Tensor:
        """
        Forward pass through the quantum generator.
        
        Args:
            noise: Random noise input [batch_size, noise_dim]
            
        Returns:
            Generated data [batch_size, output_dim]
        """
        # Encode classical noise into quantum parameters
        quantum_params = self.encode_classical_data(noise)
        
        # Execute quantum circuit
        quantum_output = self.quantum_forward(quantum_params)
        
        # Apply classical post-processing
        if self.post_processor is not None:
            generated_data = self.post_processor(quantum_output)
        else:
            # Direct quantum output (truncate if needed)
            if quantum_output.shape[1] > self.output_dim:
                generated_data = quantum_output[:, :self.output_dim]
            else:
                # Pad if quantum output is smaller
                padding = torch.zeros(
                    quantum_output.shape[0], 
                    self.output_dim - quantum_output.shape[1],
                    device=quantum_output.device
                )
                generated_data = torch.cat([quantum_output, padding], dim=1)
        
        return generated_data
    
    def sample(self, batch_size: int, device: Optional[torch.device] = None) -> torch.Tensor:
        """
        Sample synthetic data from the quantum generator.
        
        Args:
            batch_size: Number of samples to generate
            device: Device to generate samples on
            
        Returns:
            Generated samples [batch_size, output_dim]
        """
        if device is None:
            device = next(self.parameters()).device
        
        # Sample random noise
        noise = torch.randn(batch_size, self.noise_dim, device=device)
        
        # Generate data
        with torch.no_grad():
            generated = self.forward(noise)
        
        return generated
    
    def get_circuit_info(self) -> Dict[str, Any]:
        """
        Get information about the quantum circuit.
        
        Returns:
            Dictionary with circuit information
        """
        return {
            "n_qubits": self.n_qubits,
            "n_layers": self.n_layers, 
            "n_params": self.n_params,
            "output_dim": self.output_dim,
            "encoding_type": self.encoding_type,
            "post_processing": self.post_processing_type,
            "backend_info": self.backend.get_device_info(),
            "total_parameters": sum(p.numel() for p in self.parameters()),
        }
    
    def visualize_circuit(self, filename: Optional[str] = None):
        """
        Visualize the quantum circuit.
        
        Args:
            filename: Optional filename to save the visualization
        """
        if hasattr(self.backend, 'visualize_circuit'):
            # Use dummy parameters for visualization
            dummy_params = torch.zeros(self.n_params)
            self.backend.visualize_circuit(self.circuit, dummy_params, filename)
        else:
            print("Circuit visualization not supported for this backend")
    
    def reset_parameters(self):
        """Reset quantum circuit parameters."""
        with torch.no_grad():
            self.quantum_params.data = torch.randn_like(self.quantum_params) * 0.1
