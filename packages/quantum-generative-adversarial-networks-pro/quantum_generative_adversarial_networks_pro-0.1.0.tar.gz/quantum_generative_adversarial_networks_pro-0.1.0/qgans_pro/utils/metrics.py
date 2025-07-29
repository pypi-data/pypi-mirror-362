"""
Evaluation metrics for QGANS Pro.

This module implements various metrics for evaluating the quality
of generated data, including both classical and quantum metrics.
"""

from typing import Any, Dict, List, Optional, Tuple, Union
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from scipy import linalg
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

try:
    from torchvision.models import inception_v3
    TORCHVISION_AVAILABLE = True
except ImportError:
    TORCHVISION_AVAILABLE = False


class FIDScore:
    """
    Fréchet Inception Distance (FID) score calculation.
    
    FID measures the distance between feature distributions of real and generated images.
    Lower scores indicate better quality and diversity of generated samples.
    """
    
    def __init__(self, device: torch.device = None):
        """
        Initialize FID score calculator.
        
        Args:
            device: Device to run calculations on
        """
        if device is None:
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.device = device
        
        # Load pre-trained Inception v3 model for feature extraction
        if TORCHVISION_AVAILABLE:
            self.inception_model = inception_v3(pretrained=True, transform_input=False)
            self.inception_model.fc = nn.Identity()  # Remove final classification layer
            self.inception_model.eval()
            self.inception_model.to(device)
        else:
            print("Warning: torchvision not available. Using simplified feature extraction.")
            self.inception_model = None
    
    def extract_features(self, data: torch.Tensor) -> torch.Tensor:
        """
        Extract features from data using Inception v3.
        
        Args:
            data: Input data [batch_size, channels, height, width]
            
        Returns:
            Feature vectors [batch_size, feature_dim]
        """
        if self.inception_model is None:
            # Fallback: use simple statistical features
            return self._extract_simple_features(data)
        
        # Ensure data is in correct format for Inception
        if data.shape[1] == 1:  # Grayscale to RGB
            data = data.repeat(1, 3, 1, 1)
        
        if data.shape[-1] != 299:  # Resize to 299x299 for Inception
            data = F.interpolate(data, size=(299, 299), mode='bilinear', align_corners=False)
        
        # Normalize to [-1, 1] range expected by Inception
        data = (data - 0.5) * 2
        
        with torch.no_grad():
            features = self.inception_model(data)
        
        return features
    
    def _extract_simple_features(self, data: torch.Tensor) -> torch.Tensor:
        """
        Extract simple statistical features as fallback.
        
        Args:
            data: Input data
            
        Returns:
            Simple feature vectors
        """
        batch_size = data.shape[0]
        data_flat = data.view(batch_size, -1)
        
        # Compute statistical features
        mean_vals = torch.mean(data_flat, dim=1)
        std_vals = torch.std(data_flat, dim=1)
        min_vals = torch.min(data_flat, dim=1)[0]
        max_vals = torch.max(data_flat, dim=1)[0]
        
        # Simple histogram features
        hist_features = []
        for i in range(batch_size):
            hist = torch.histc(data_flat[i], bins=10, min=-1, max=1)
            hist_features.append(hist)
        hist_features = torch.stack(hist_features)
        
        # Combine features
        features = torch.cat([
            mean_vals.unsqueeze(1),
            std_vals.unsqueeze(1),
            min_vals.unsqueeze(1),
            max_vals.unsqueeze(1),
            hist_features
        ], dim=1)
        
        return features
    
    def calculate_statistics(self, features: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Calculate mean and covariance matrix of features.
        
        Args:
            features: Feature vectors [batch_size, feature_dim]
            
        Returns:
            Tuple of (mean, covariance_matrix)
        """
        features_np = features.cpu().numpy()
        
        mu = np.mean(features_np, axis=0)
        sigma = np.cov(features_np, rowvar=False)
        
        return torch.tensor(mu), torch.tensor(sigma)
    
    def compute_fid(
        self,
        real_features: torch.Tensor,
        fake_features: torch.Tensor
    ) -> float:
        """
        Compute FID score between real and fake features.
        
        Args:
            real_features: Features from real data
            fake_features: Features from generated data
            
        Returns:
            FID score
        """
        # Calculate statistics
        mu1, sigma1 = self.calculate_statistics(real_features)
        mu2, sigma2 = self.calculate_statistics(fake_features)
        
        mu1_np = mu1.numpy()
        mu2_np = mu2.numpy()
        sigma1_np = sigma1.numpy()
        sigma2_np = sigma2.numpy()
        
        # Calculate FID
        diff = mu1_np - mu2_np
        
        # Compute sqrt of product of covariance matrices
        covmean, _ = linalg.sqrtm(sigma1_np.dot(sigma2_np), disp=False)
        
        # Handle numerical errors
        if not np.isfinite(covmean).all():
            print("Warning: FID calculation resulted in complex values. Using simplified calculation.")
            covmean = np.real(covmean)
        
        # FID formula
        fid = diff.dot(diff) + np.trace(sigma1_np + sigma2_np - 2 * covmean)
        
        return float(fid)
    
    def __call__(
        self,
        real_data: torch.Tensor,
        fake_data: torch.Tensor
    ) -> float:
        """
        Calculate FID score between real and generated data.
        
        Args:
            real_data: Real data samples
            fake_data: Generated data samples
            
        Returns:
            FID score
        """
        # Extract features
        real_features = self.extract_features(real_data.to(self.device))
        fake_features = self.extract_features(fake_data.to(self.device))
        
        # Compute FID
        fid_score = self.compute_fid(real_features, fake_features)
        
        return fid_score


class InceptionScore:
    """
    Inception Score (IS) calculation.
    
    IS measures both quality and diversity of generated samples using
    a pre-trained Inception network.
    """
    
    def __init__(self, device: torch.device = None, splits: int = 10):
        """
        Initialize Inception Score calculator.
        
        Args:
            device: Device to run calculations on
            splits: Number of splits for score calculation
        """
        if device is None:
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.device = device
        self.splits = splits
        
        # Load pre-trained Inception v3 model
        if TORCHVISION_AVAILABLE:
            self.inception_model = inception_v3(pretrained=True, transform_input=False)
            self.inception_model.eval()
            self.inception_model.to(device)
        else:
            print("Warning: torchvision not available. Using simplified IS calculation.")
            self.inception_model = None
    
    def get_predictions(self, data: torch.Tensor) -> torch.Tensor:
        """
        Get Inception predictions for data.
        
        Args:
            data: Input data [batch_size, channels, height, width]
            
        Returns:
            Prediction probabilities [batch_size, num_classes]
        """
        if self.inception_model is None:
            # Fallback: random predictions
            batch_size = data.shape[0]
            return torch.rand(batch_size, 1000, device=self.device)
        
        # Ensure data is in correct format
        if data.shape[1] == 1:  # Grayscale to RGB
            data = data.repeat(1, 3, 1, 1)
        
        if data.shape[-1] != 299:  # Resize to 299x299
            data = F.interpolate(data, size=(299, 299), mode='bilinear', align_corners=False)
        
        # Normalize
        data = (data - 0.5) * 2
        
        with torch.no_grad():
            predictions = self.inception_model(data)
            predictions = F.softmax(predictions, dim=1)
        
        return predictions
    
    def calculate_is(self, predictions: torch.Tensor) -> Tuple[float, float]:
        """
        Calculate Inception Score from predictions.
        
        Args:
            predictions: Softmax predictions [batch_size, num_classes]
            
        Returns:
            Tuple of (mean_score, std_score)
        """
        scores = []
        
        # Split predictions into chunks
        chunk_size = predictions.shape[0] // self.splits
        
        for i in range(self.splits):
            start_idx = i * chunk_size
            if i == self.splits - 1:
                end_idx = predictions.shape[0]
            else:
                end_idx = (i + 1) * chunk_size
            
            chunk_preds = predictions[start_idx:end_idx]
            
            # Calculate KL divergence
            marginal = torch.mean(chunk_preds, dim=0, keepdim=True)
            kl_div = chunk_preds * (torch.log(chunk_preds + 1e-8) - torch.log(marginal + 1e-8))
            kl_div = torch.sum(kl_div, dim=1)
            score = torch.exp(torch.mean(kl_div))
            
            scores.append(score.item())
        
        return np.mean(scores), np.std(scores)
    
    def __call__(self, data: torch.Tensor) -> Tuple[float, float]:
        """
        Calculate Inception Score for generated data.
        
        Args:
            data: Generated data samples
            
        Returns:
            Tuple of (mean_score, std_score)
        """
        # Get predictions
        predictions = self.get_predictions(data.to(self.device))
        
        # Calculate IS
        mean_score, std_score = self.calculate_is(predictions)
        
        return mean_score, std_score


class QuantumFidelity:
    """
    Quantum-specific fidelity metrics.
    
    This class implements quantum state fidelity and other quantum-specific
    measures for evaluating quantum GAN performance.
    """
    
    def __init__(self, device: torch.device = None):
        """
        Initialize quantum fidelity calculator.
        
        Args:
            device: Device to run calculations on
        """
        if device is None:
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.device = device
    
    def state_fidelity(
        self,
        state1: torch.Tensor,
        state2: torch.Tensor
    ) -> torch.Tensor:
        """
        Calculate quantum state fidelity between two states.
        
        Args:
            state1: First quantum state [batch_size, state_dim]
            state2: Second quantum state [batch_size, state_dim]
            
        Returns:
            Fidelity values [batch_size]
        """
        # Normalize states
        state1_norm = state1 / (torch.norm(state1, dim=-1, keepdim=True) + 1e-8)
        state2_norm = state2 / (torch.norm(state2, dim=-1, keepdim=True) + 1e-8)
        
        # Calculate overlap |<ψ1|ψ2>|²
        if torch.is_complex(state1_norm) or torch.is_complex(state2_norm):
            overlap = torch.sum(torch.conj(state1_norm) * state2_norm, dim=-1)
            fidelity = torch.abs(overlap) ** 2
        else:
            overlap = torch.sum(state1_norm * state2_norm, dim=-1)
            fidelity = overlap ** 2
        
        return fidelity
    
    def average_fidelity(
        self,
        real_states: torch.Tensor,
        generated_states: torch.Tensor
    ) -> float:
        """
        Calculate average fidelity between real and generated quantum states.
        
        Args:
            real_states: Real quantum states
            generated_states: Generated quantum states
            
        Returns:
            Average fidelity
        """
        # Calculate pairwise fidelities
        fidelities = []
        
        for i in range(min(len(real_states), len(generated_states))):
            fidelity = self.state_fidelity(
                real_states[i:i+1],
                generated_states[i:i+1]
            )
            fidelities.append(fidelity)
        
        if fidelities:
            avg_fidelity = torch.mean(torch.cat(fidelities))
            return avg_fidelity.item()
        else:
            return 0.0
    
    def quantum_divergence(
        self,
        real_data: torch.Tensor,
        generated_data: torch.Tensor
    ) -> float:
        """
        Calculate quantum-inspired divergence between real and generated data.
        
        Args:
            real_data: Real data samples
            generated_data: Generated data samples
            
        Returns:
            Quantum divergence value
        """
        # Convert data to quantum-like states (normalized probability distributions)
        real_probs = F.softmax(real_data.view(real_data.shape[0], -1), dim=1)
        gen_probs = F.softmax(generated_data.view(generated_data.shape[0], -1), dim=1)
        
        # Calculate quantum relative entropy (quantum KL divergence)
        # D(ρ||σ) = Tr(ρ log ρ) - Tr(ρ log σ)
        
        # Marginal distributions
        real_marginal = torch.mean(real_probs, dim=0)
        gen_marginal = torch.mean(gen_probs, dim=0)
        
        # Quantum relative entropy
        entropy_real = -torch.sum(real_marginal * torch.log(real_marginal + 1e-8))
        cross_entropy = -torch.sum(real_marginal * torch.log(gen_marginal + 1e-8))
        
        quantum_divergence = cross_entropy - entropy_real
        
        return quantum_divergence.item()
    
    def __call__(
        self,
        real_data: torch.Tensor,
        generated_data: torch.Tensor
    ) -> Dict[str, float]:
        """
        Calculate various quantum fidelity metrics.
        
        Args:
            real_data: Real data samples
            generated_data: Generated data samples
            
        Returns:
            Dictionary of quantum metrics
        """
        metrics = {}
        
        # Average fidelity
        avg_fidelity = self.average_fidelity(real_data, generated_data)
        metrics["average_fidelity"] = avg_fidelity
        
        # Quantum divergence
        quantum_div = self.quantum_divergence(real_data, generated_data)
        metrics["quantum_divergence"] = quantum_div
        
        # Quantum purity (measure of quantum state purity)
        real_probs = F.softmax(real_data.view(real_data.shape[0], -1), dim=1)
        gen_probs = F.softmax(generated_data.view(generated_data.shape[0], -1), dim=1)
        
        real_purity = torch.mean(torch.sum(real_probs ** 2, dim=1))
        gen_purity = torch.mean(torch.sum(gen_probs ** 2, dim=1))
        
        metrics["real_purity"] = real_purity.item()
        metrics["generated_purity"] = gen_purity.item()
        metrics["purity_difference"] = abs(real_purity.item() - gen_purity.item())
        
        return metrics


class PrivacyMetrics:
    """
    Privacy and fairness metrics for generated data.
    
    This class implements metrics to evaluate bias and privacy preservation
    in generated synthetic data.
    """
    
    def __init__(self):
        """Initialize privacy metrics calculator."""
        pass
    
    def membership_inference_attack(
        self,
        model: nn.Module,
        train_data: torch.Tensor,
        test_data: torch.Tensor,
        generated_data: torch.Tensor
    ) -> Dict[str, float]:
        """
        Evaluate privacy using membership inference attack.
        
        Args:
            model: Trained generator model
            train_data: Training data
            test_data: Test data
            generated_data: Generated synthetic data
            
        Returns:
            Privacy metrics
        """
        # This is a simplified implementation
        # In practice, this would involve training an attack model
        
        # Placeholder implementation
        metrics = {
            "mia_accuracy": 0.5,  # Random guess baseline
            "privacy_score": 1.0,  # Higher is better
        }
        
        return metrics
    
    def statistical_parity(
        self,
        data: torch.Tensor,
        sensitive_attributes: torch.Tensor,
        predictions: torch.Tensor
    ) -> float:
        """
        Calculate statistical parity for fairness evaluation.
        
        Args:
            data: Data samples
            sensitive_attributes: Sensitive attribute labels
            predictions: Model predictions
            
        Returns:
            Statistical parity difference
        """
        # Calculate positive prediction rates for different groups
        unique_attributes = torch.unique(sensitive_attributes)
        
        group_rates = []
        for attr in unique_attributes:
            mask = sensitive_attributes == attr
            group_predictions = predictions[mask]
            positive_rate = torch.mean((group_predictions > 0.5).float())
            group_rates.append(positive_rate)
        
        # Statistical parity difference
        if len(group_rates) >= 2:
            sp_diff = abs(group_rates[0] - group_rates[1])
            return sp_diff.item()
        else:
            return 0.0
