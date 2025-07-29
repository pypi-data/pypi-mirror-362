"""
Quantum-compatible loss functions for QGANS Pro.

This module implements loss functions that are compatible with quantum
computing backends and provide better training dynamics for quantum GANs.
"""

from typing import Any, Dict, Optional, Tuple
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


class QuantumBCELoss(nn.Module):
    """
    Quantum-compatible Binary Cross Entropy Loss.
    
    This loss function includes quantum-specific regularization terms
    to improve training stability for quantum GANs.
    """
    
    def __init__(
        self,
        reduction: str = "mean",
        quantum_regularization: bool = True,
        reg_lambda: float = 0.001,
        smoothing: float = 0.1,
    ):
        """
        Initialize Quantum BCE Loss.
        
        Args:
            reduction: Reduction method ('mean', 'sum', 'none')
            quantum_regularization: Whether to apply quantum regularization
            reg_lambda: Regularization strength
            smoothing: Label smoothing factor
        """
        super().__init__()
        
        self.reduction = reduction
        self.quantum_regularization = quantum_regularization
        self.reg_lambda = reg_lambda
        self.smoothing = smoothing
        
        self.bce_loss = nn.BCELoss(reduction="none")
    
    def forward(
        self,
        predictions: torch.Tensor,
        targets: torch.Tensor,
        quantum_params: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        """
        Compute quantum BCE loss.
        
        Args:
            predictions: Model predictions [batch_size, 1]
            targets: Target labels [batch_size, 1]
            quantum_params: Quantum circuit parameters for regularization
            
        Returns:
            Loss value
        """
        # Apply label smoothing
        if self.smoothing > 0:
            targets = targets * (1 - self.smoothing) + 0.5 * self.smoothing
        
        # Compute BCE loss
        bce = self.bce_loss(predictions, targets)
        
        # Apply quantum regularization
        if self.quantum_regularization and quantum_params is not None:
            # Quantum parameter regularization
            # Penalize large parameter values to prevent over-rotation
            param_reg = torch.sum(torch.sin(quantum_params) ** 2)
            
            # Add regularization term
            bce = bce + self.reg_lambda * param_reg
        
        # Apply reduction
        if self.reduction == "mean":
            return torch.mean(bce)
        elif self.reduction == "sum":
            return torch.sum(bce)
        else:
            return bce


class QuantumWassersteinLoss(nn.Module):
    """
    Quantum-compatible Wasserstein Loss.
    
    This loss function is designed for quantum Wasserstein GANs,
    incorporating quantum-specific considerations.
    """
    
    def __init__(
        self,
        quantum_regularization: bool = True,
        reg_lambda: float = 0.001,
        gradient_penalty: bool = True,
        gp_lambda: float = 10.0,
    ):
        """
        Initialize Quantum Wasserstein Loss.
        
        Args:
            quantum_regularization: Whether to apply quantum regularization
            reg_lambda: Quantum regularization strength
            gradient_penalty: Whether to use gradient penalty
            gp_lambda: Gradient penalty strength
        """
        super().__init__()
        
        self.quantum_regularization = quantum_regularization
        self.reg_lambda = reg_lambda
        self.gradient_penalty = gradient_penalty
        self.gp_lambda = gp_lambda
    
    def forward(
        self,
        real_scores: torch.Tensor,
        fake_scores: torch.Tensor,
        real_data: Optional[torch.Tensor] = None,
        fake_data: Optional[torch.Tensor] = None,
        discriminator: Optional[nn.Module] = None,
        quantum_params: Optional[torch.Tensor] = None,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Compute Wasserstein loss for generator and discriminator.
        
        Args:
            real_scores: Discriminator scores for real data
            fake_scores: Discriminator scores for fake data
            real_data: Real data (needed for gradient penalty)
            fake_data: Fake data (needed for gradient penalty)
            discriminator: Discriminator model (needed for gradient penalty)
            quantum_params: Quantum parameters for regularization
            
        Returns:
            Tuple of (discriminator_loss, generator_loss)
        """
        # Wasserstein distance approximation
        d_loss = torch.mean(fake_scores) - torch.mean(real_scores)
        g_loss = -torch.mean(fake_scores)
        
        # Gradient penalty
        if self.gradient_penalty and real_data is not None and fake_data is not None and discriminator is not None:
            gp = self.compute_gradient_penalty(discriminator, real_data, fake_data)
            d_loss = d_loss + self.gp_lambda * gp
        
        # Quantum regularization
        if self.quantum_regularization and quantum_params is not None:
            # Encourage parameter diversity to prevent mode collapse
            param_entropy = -torch.sum(F.softmax(quantum_params, dim=0) * F.log_softmax(quantum_params, dim=0))
            quantum_reg = -self.reg_lambda * param_entropy
            
            d_loss = d_loss + quantum_reg
            g_loss = g_loss + quantum_reg
        
        return d_loss, g_loss
    
    def compute_gradient_penalty(
        self,
        discriminator: nn.Module,
        real_data: torch.Tensor,
        fake_data: torch.Tensor,
    ) -> torch.Tensor:
        """
        Compute gradient penalty for WGAN-GP.
        
        Args:
            discriminator: Discriminator model
            real_data: Real data samples
            fake_data: Generated data samples
            
        Returns:
            Gradient penalty value
        """
        batch_size = real_data.size(0)
        device = real_data.device
        
        # Random interpolation between real and fake data
        alpha = torch.rand(batch_size, 1, device=device)
        
        # Expand alpha to match data dimensions
        for _ in range(len(real_data.shape) - 2):
            alpha = alpha.unsqueeze(-1)
        
        interpolated = alpha * real_data + (1 - alpha) * fake_data
        interpolated.requires_grad_(True)
        
        # Compute discriminator output for interpolated data
        d_interpolated = discriminator(interpolated)
        
        # Compute gradients
        gradients = torch.autograd.grad(
            outputs=d_interpolated,
            inputs=interpolated,
            grad_outputs=torch.ones_like(d_interpolated),
            create_graph=True,
            retain_graph=True,
            only_inputs=True,
        )[0]
        
        # Reshape gradients
        gradients = gradients.view(batch_size, -1)
        
        # Compute gradient penalty
        gradient_norm = torch.sqrt(torch.sum(gradients ** 2, dim=1) + 1e-12)
        gradient_penalty = torch.mean((gradient_norm - 1) ** 2)
        
        return gradient_penalty


class QuantumHingeLoss(nn.Module):
    """
    Quantum-compatible Hinge Loss.
    
    This loss function implements hinge loss with quantum-specific
    modifications for improved training dynamics.
    """
    
    def __init__(
        self,
        quantum_regularization: bool = True,
        reg_lambda: float = 0.001,
        margin: float = 1.0,
    ):
        """
        Initialize Quantum Hinge Loss.
        
        Args:
            quantum_regularization: Whether to apply quantum regularization
            reg_lambda: Regularization strength
            margin: Hinge loss margin
        """
        super().__init__()
        
        self.quantum_regularization = quantum_regularization
        self.reg_lambda = reg_lambda
        self.margin = margin
    
    def forward(
        self,
        real_scores: torch.Tensor,
        fake_scores: torch.Tensor,
        quantum_params: Optional[torch.Tensor] = None,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Compute hinge loss for generator and discriminator.
        
        Args:
            real_scores: Discriminator scores for real data
            fake_scores: Discriminator scores for fake data
            quantum_params: Quantum parameters for regularization
            
        Returns:
            Tuple of (discriminator_loss, generator_loss)
        """
        # Hinge loss for discriminator
        d_loss_real = torch.mean(F.relu(self.margin - real_scores))
        d_loss_fake = torch.mean(F.relu(self.margin + fake_scores))
        d_loss = d_loss_real + d_loss_fake
        
        # Hinge loss for generator
        g_loss = -torch.mean(fake_scores)
        
        # Quantum regularization
        if self.quantum_regularization and quantum_params is not None:
            # Regularize quantum parameters to prevent over-fitting
            param_var = torch.var(quantum_params)
            quantum_reg = self.reg_lambda * (1.0 / (param_var + 1e-8))
            
            d_loss = d_loss + quantum_reg
            g_loss = g_loss + quantum_reg
        
        return d_loss, g_loss


class QuantumLSGANLoss(nn.Module):
    """
    Quantum-compatible Least Squares GAN Loss.
    
    This loss function implements LSGAN loss with quantum regularization
    for stable training of quantum GANs.
    """
    
    def __init__(
        self,
        quantum_regularization: bool = True,
        reg_lambda: float = 0.001,
        real_label: float = 1.0,
        fake_label: float = 0.0,
    ):
        """
        Initialize Quantum LSGAN Loss.
        
        Args:
            quantum_regularization: Whether to apply quantum regularization
            reg_lambda: Regularization strength
            real_label: Label value for real data
            fake_label: Label value for fake data
        """
        super().__init__()
        
        self.quantum_regularization = quantum_regularization
        self.reg_lambda = reg_lambda
        self.real_label = real_label
        self.fake_label = fake_label
        
        self.mse_loss = nn.MSELoss()
    
    def forward(
        self,
        real_scores: torch.Tensor,
        fake_scores: torch.Tensor,
        quantum_params: Optional[torch.Tensor] = None,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Compute LSGAN loss for generator and discriminator.
        
        Args:
            real_scores: Discriminator scores for real data
            fake_scores: Discriminator scores for fake data
            quantum_params: Quantum parameters for regularization
            
        Returns:
            Tuple of (discriminator_loss, generator_loss)
        """
        # LSGAN loss for discriminator
        real_targets = torch.full_like(real_scores, self.real_label)
        fake_targets = torch.full_like(fake_scores, self.fake_label)
        
        d_loss_real = self.mse_loss(real_scores, real_targets)
        d_loss_fake = self.mse_loss(fake_scores, fake_targets)
        d_loss = (d_loss_real + d_loss_fake) / 2
        
        # LSGAN loss for generator
        real_targets_g = torch.full_like(fake_scores, self.real_label)
        g_loss = self.mse_loss(fake_scores, real_targets_g)
        
        # Quantum regularization
        if self.quantum_regularization and quantum_params is not None:
            # Encourage parameter exploration
            param_norm = torch.norm(quantum_params, p=2)
            quantum_reg = self.reg_lambda * torch.exp(-param_norm)
            
            d_loss = d_loss + quantum_reg
            g_loss = g_loss + quantum_reg
        
        return d_loss, g_loss


class QuantumFidelityLoss(nn.Module):
    """
    Quantum Fidelity-based Loss Function.
    
    This loss function uses quantum state fidelity as a metric
    for training quantum generators.
    """
    
    def __init__(self, target_fidelity: float = 0.9):
        """
        Initialize Quantum Fidelity Loss.
        
        Args:
            target_fidelity: Target fidelity value
        """
        super().__init__()
        self.target_fidelity = target_fidelity
    
    def quantum_fidelity(self, state1: torch.Tensor, state2: torch.Tensor) -> torch.Tensor:
        """
        Compute quantum state fidelity.
        
        Args:
            state1: First quantum state
            state2: Second quantum state
            
        Returns:
            Fidelity value
        """
        # Normalize states
        state1_norm = state1 / (torch.norm(state1, dim=-1, keepdim=True) + 1e-8)
        state2_norm = state2 / (torch.norm(state2, dim=-1, keepdim=True) + 1e-8)
        
        # Compute fidelity |<ψ1|ψ2>|²
        overlap = torch.sum(torch.conj(state1_norm) * state2_norm, dim=-1)
        fidelity = torch.abs(overlap) ** 2
        
        return fidelity
    
    def forward(
        self,
        generated_states: torch.Tensor,
        target_states: torch.Tensor,
    ) -> torch.Tensor:
        """
        Compute fidelity-based loss.
        
        Args:
            generated_states: Generated quantum states
            target_states: Target quantum states
            
        Returns:
            Fidelity loss
        """
        # Compute batch fidelity
        fidelities = self.quantum_fidelity(generated_states, target_states)
        
        # Loss is the deviation from target fidelity
        fidelity_loss = torch.mean((fidelities - self.target_fidelity) ** 2)
        
        return fidelity_loss
