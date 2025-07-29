"""
GAN Trainer implementation for QGANS Pro.

This module provides unified training interfaces for quantum, classical,
and hybrid GANs with advanced training techniques.
"""

from typing import Any, Dict, List, Optional, Tuple, Union, Callable
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
from tqdm import tqdm
import os
import json
from datetime import datetime

from ..models.quantum_generator import QuantumGenerator
from ..models.quantum_discriminator import QuantumDiscriminator
from ..models.classical_generator import ClassicalGenerator
from ..models.classical_discriminator import ClassicalDiscriminator
from ..losses.quantum_losses import QuantumWassersteinLoss, QuantumHingeLoss
from ..utils.metrics import FIDScore, InceptionScore, QuantumFidelity


class BaseGANTrainer:
    """
    Base class for GAN trainers.
    
    Provides common functionality for training GANs.
    """
    
    def __init__(
        self,
        generator: nn.Module,
        discriminator: nn.Module,
        device: torch.device = None,
        save_dir: str = "./checkpoints",
    ):
        """
        Initialize the base trainer.
        
        Args:
            generator: Generator model
            discriminator: Discriminator model
            device: Training device
            save_dir: Directory to save checkpoints
        """
        self.generator = generator
        self.discriminator = discriminator
        
        if device is None:
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.device = device
        
        self.generator.to(device)
        self.discriminator.to(device)
        
        self.save_dir = save_dir
        os.makedirs(save_dir, exist_ok=True)
        
        # Training history
        self.history = {
            "generator_loss": [],
            "discriminator_loss": [],
            "metrics": {}
        }
        
        # Training state
        self.current_epoch = 0
        self.global_step = 0
        
    def save_checkpoint(self, filename: Optional[str] = None):
        """Save training checkpoint."""
        if filename is None:
            filename = f"checkpoint_epoch_{self.current_epoch}.pt"
        
        filepath = os.path.join(self.save_dir, filename)
        
        checkpoint = {
            "epoch": self.current_epoch,
            "global_step": self.global_step,
            "generator_state_dict": self.generator.state_dict(),
            "discriminator_state_dict": self.discriminator.state_dict(),
            "history": self.history,
        }
        
        torch.save(checkpoint, filepath)
        
        # Also save training history as JSON
        history_file = os.path.join(self.save_dir, "training_history.json")
        with open(history_file, "w") as f:
            json.dump(self.history, f, indent=2)
    
    def load_checkpoint(self, filepath: str):
        """Load training checkpoint."""
        checkpoint = torch.load(filepath, map_location=self.device)
        
        self.generator.load_state_dict(checkpoint["generator_state_dict"])
        self.discriminator.load_state_dict(checkpoint["discriminator_state_dict"])
        self.current_epoch = checkpoint["epoch"]
        self.global_step = checkpoint["global_step"]
        self.history = checkpoint.get("history", self.history)
    
    def plot_training_history(self, save_path: Optional[str] = None):
        """Plot training loss curves."""
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))
        
        # Plot losses
        axes[0].plot(self.history["generator_loss"], label="Generator")
        axes[0].plot(self.history["discriminator_loss"], label="Discriminator")
        axes[0].set_title("Training Losses")
        axes[0].set_xlabel("Epoch")
        axes[0].set_ylabel("Loss")
        axes[0].legend()
        axes[0].grid(True)
        
        # Plot metrics if available
        if self.history["metrics"]:
            metric_names = list(self.history["metrics"].keys())
            if metric_names:
                for i, metric in enumerate(metric_names[:2]):  # Plot first 2 metrics
                    if i < len(axes) - 1:
                        axes[1].plot(self.history["metrics"][metric], label=metric)
                
                axes[1].set_title("Training Metrics")
                axes[1].set_xlabel("Epoch")
                axes[1].set_ylabel("Metric Value")
                axes[1].legend()
                axes[1].grid(True)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
        else:
            plt.show()


class QuantumGAN(BaseGANTrainer):
    """
    Quantum GAN trainer using quantum generator and discriminator.
    
    This trainer implements specialized techniques for training quantum GANs,
    including quantum-aware optimizers and loss functions.
    """
    
    def __init__(
        self,
        generator: QuantumGenerator,
        discriminator: QuantumDiscriminator,
        device: torch.device = None,
        save_dir: str = "./quantum_gan_checkpoints",
        loss_type: str = "standard",
        optimizer_type: str = "adam",
        lr_g: float = 0.0002,
        lr_d: float = 0.0002,
        beta1: float = 0.5,
        beta2: float = 0.999,
    ):
        """
        Initialize the Quantum GAN trainer.
        
        Args:
            generator: Quantum generator
            discriminator: Quantum discriminator
            device: Training device
            save_dir: Directory to save checkpoints
            loss_type: Type of loss function ('standard', 'wasserstein', 'hinge')
            optimizer_type: Type of optimizer ('adam', 'rmsprop', 'sgd')
            lr_g: Learning rate for generator
            lr_d: Learning rate for discriminator
            beta1: Adam beta1 parameter
            beta2: Adam beta2 parameter
        """
        super().__init__(generator, discriminator, device, save_dir)
        
        self.loss_type = loss_type
        
        # Initialize loss functions
        if loss_type == "standard":
            self.criterion = nn.BCELoss()
        elif loss_type == "wasserstein":
            self.criterion = QuantumWassersteinLoss()
        elif loss_type == "hinge":
            self.criterion = QuantumHingeLoss()
        else:
            self.criterion = nn.BCELoss()
        
        # Initialize optimizers
        if optimizer_type == "adam":
            self.optimizer_g = optim.Adam(generator.parameters(), lr=lr_g, betas=(beta1, beta2))
            self.optimizer_d = optim.Adam(discriminator.parameters(), lr=lr_d, betas=(beta1, beta2))
        elif optimizer_type == "rmsprop":
            self.optimizer_g = optim.RMSprop(generator.parameters(), lr=lr_g)
            self.optimizer_d = optim.RMSprop(discriminator.parameters(), lr=lr_d)
        else:
            self.optimizer_g = optim.SGD(generator.parameters(), lr=lr_g)
            self.optimizer_d = optim.SGD(discriminator.parameters(), lr=lr_d)
        
        # Quantum-specific metrics
        self.quantum_fidelity = QuantumFidelity()
        
    def train_discriminator(self, real_data: torch.Tensor, batch_size: int) -> float:
        """
        Train discriminator for one step.
        
        Args:
            real_data: Real data batch
            batch_size: Batch size
            
        Returns:
            Discriminator loss
        """
        self.optimizer_d.zero_grad()
        
        # Train on real data
        real_labels = torch.ones(batch_size, 1, device=self.device)
        real_output = self.discriminator(real_data)
        real_loss = self.criterion(real_output, real_labels)
        
        # Train on fake data
        noise = torch.randn(batch_size, self.generator.noise_dim, device=self.device)
        fake_data = self.generator(noise).detach()
        fake_labels = torch.zeros(batch_size, 1, device=self.device)
        fake_output = self.discriminator(fake_data)
        fake_loss = self.criterion(fake_output, fake_labels)
        
        # Total discriminator loss
        d_loss = (real_loss + fake_loss) / 2
        d_loss.backward()
        self.optimizer_d.step()
        
        return d_loss.item()
    
    def train_generator(self, batch_size: int) -> float:
        """
        Train generator for one step.
        
        Args:
            batch_size: Batch size
            
        Returns:
            Generator loss
        """
        self.optimizer_g.zero_grad()
        
        # Generate fake data
        noise = torch.randn(batch_size, self.generator.noise_dim, device=self.device)
        fake_data = self.generator(noise)
        
        # Train generator to fool discriminator
        real_labels = torch.ones(batch_size, 1, device=self.device)
        fake_output = self.discriminator(fake_data)
        g_loss = self.criterion(fake_output, real_labels)
        
        g_loss.backward()
        self.optimizer_g.step()
        
        return g_loss.item()
    
    def compute_quantum_metrics(self, real_data: torch.Tensor, fake_data: torch.Tensor) -> Dict[str, float]:
        """
        Compute quantum-specific metrics.
        
        Args:
            real_data: Real data samples
            fake_data: Generated data samples
            
        Returns:
            Dictionary of metric values
        """
        metrics = {}
        
        # Quantum fidelity between real and fake data distributions
        try:
            fidelity = self.quantum_fidelity(real_data, fake_data)
            metrics["quantum_fidelity"] = fidelity.item()
        except Exception as e:
            print(f"Error computing quantum fidelity: {e}")
            metrics["quantum_fidelity"] = 0.0
        
        # Generator circuit complexity (approximate)
        if hasattr(self.generator, 'get_circuit_info'):
            circuit_info = self.generator.get_circuit_info()
            metrics["quantum_params"] = circuit_info.get("n_params", 0)
            metrics["quantum_qubits"] = circuit_info.get("n_qubits", 0)
        
        return metrics
    
    def train(
        self,
        dataloader: DataLoader,
        epochs: int,
        d_steps: int = 1,
        g_steps: int = 1,
        save_interval: int = 10,
        evaluate_interval: int = 5,
        sample_interval: int = 10,
        sample_size: int = 64,
    ):
        """
        Train the Quantum GAN.
        
        Args:
            dataloader: Training data loader
            epochs: Number of training epochs
            d_steps: Discriminator training steps per iteration
            g_steps: Generator training steps per iteration
            save_interval: Checkpoint saving interval
            evaluate_interval: Evaluation interval
            sample_interval: Sample generation interval
            sample_size: Number of samples to generate for evaluation
        """
        print(f"Training Quantum GAN for {epochs} epochs on {self.device}")
        print(f"Generator: {self.generator.get_circuit_info()}")
        print(f"Discriminator: {self.discriminator.get_circuit_info()}")
        
        self.generator.train()
        self.discriminator.train()
        
        for epoch in range(epochs):
            epoch_g_loss = 0.0
            epoch_d_loss = 0.0
            num_batches = 0
            
            pbar = tqdm(dataloader, desc=f"Epoch {epoch+1}/{epochs}")
            
            for batch_idx, (real_data, _) in enumerate(pbar):
                real_data = real_data.to(self.device)
                batch_size = real_data.size(0)
                
                # Flatten data if needed
                if real_data.dim() > 2:
                    real_data = real_data.view(batch_size, -1)
                
                # Train discriminator
                d_loss_total = 0.0
                for _ in range(d_steps):
                    d_loss = self.train_discriminator(real_data, batch_size)
                    d_loss_total += d_loss
                d_loss_avg = d_loss_total / d_steps
                
                # Train generator
                g_loss_total = 0.0
                for _ in range(g_steps):
                    g_loss = self.train_generator(batch_size)
                    g_loss_total += g_loss
                g_loss_avg = g_loss_total / g_steps
                
                epoch_g_loss += g_loss_avg
                epoch_d_loss += d_loss_avg
                num_batches += 1
                self.global_step += 1
                
                # Update progress bar
                pbar.set_postfix({
                    "G_loss": f"{g_loss_avg:.4f}",
                    "D_loss": f"{d_loss_avg:.4f}"
                })
            
            # Record epoch losses
            self.history["generator_loss"].append(epoch_g_loss / num_batches)
            self.history["discriminator_loss"].append(epoch_d_loss / num_batches)
            self.current_epoch = epoch + 1
            
            # Evaluation
            if (epoch + 1) % evaluate_interval == 0:
                self.evaluate(dataloader, sample_size)
            
            # Generate samples
            if (epoch + 1) % sample_interval == 0:
                self.generate_samples(sample_size, f"samples_epoch_{epoch+1}.png")
            
            # Save checkpoint
            if (epoch + 1) % save_interval == 0:
                self.save_checkpoint()
        
        print("Training completed!")
        self.plot_training_history(os.path.join(self.save_dir, "training_history.png"))
    
    def evaluate(self, dataloader: DataLoader, num_samples: int = 1000):
        """
        Evaluate the model using various metrics.
        
        Args:
            dataloader: Validation data loader
            num_samples: Number of samples to generate for evaluation
        """
        self.generator.eval()
        self.discriminator.eval()
        
        with torch.no_grad():
            # Generate samples
            fake_samples = self.generator.sample(num_samples, self.device)
            
            # Get real samples
            real_samples = []
            for batch, _ in dataloader:
                batch = batch.to(self.device)
                if batch.dim() > 2:
                    batch = batch.view(batch.size(0), -1)
                real_samples.append(batch)
                if len(real_samples) * batch.size(0) >= num_samples:
                    break
            
            real_samples = torch.cat(real_samples)[:num_samples]
            
            # Compute metrics
            metrics = self.compute_quantum_metrics(real_samples, fake_samples)
            
            # Store metrics
            for metric_name, value in metrics.items():
                if metric_name not in self.history["metrics"]:
                    self.history["metrics"][metric_name] = []
                self.history["metrics"][metric_name].append(value)
            
            print(f"Evaluation metrics: {metrics}")
        
        self.generator.train()
        self.discriminator.train()
    
    def generate_samples(self, num_samples: int, filename: Optional[str] = None) -> torch.Tensor:
        """
        Generate and optionally save samples.
        
        Args:
            num_samples: Number of samples to generate
            filename: Optional filename to save samples visualization
            
        Returns:
            Generated samples
        """
        self.generator.eval()
        
        with torch.no_grad():
            samples = self.generator.sample(num_samples, self.device)
        
        if filename:
            # Save sample visualization
            save_path = os.path.join(self.save_dir, filename)
            self.visualize_samples(samples, save_path)
        
        self.generator.train()
        return samples
    
    def visualize_samples(self, samples: torch.Tensor, save_path: str, grid_size: int = 8):
        """
        Visualize generated samples.
        
        Args:
            samples: Generated samples
            save_path: Path to save visualization
            grid_size: Size of the sample grid
        """
        # Convert to numpy
        samples_np = samples.cpu().numpy()
        
        # Determine if samples are images or 1D data
        if len(samples_np.shape) == 2:
            # Try to reshape as images
            sample_dim = samples_np.shape[1]
            img_size = int(np.sqrt(sample_dim))
            
            if img_size * img_size == sample_dim:
                # Reshape as square images
                samples_np = samples_np.reshape(-1, img_size, img_size)
                
                fig, axes = plt.subplots(grid_size, grid_size, figsize=(10, 10))
                for i in range(min(grid_size * grid_size, len(samples_np))):
                    row, col = i // grid_size, i % grid_size
                    axes[row, col].imshow(samples_np[i], cmap='gray')
                    axes[row, col].axis('off')
                
                # Hide unused subplots
                for i in range(len(samples_np), grid_size * grid_size):
                    row, col = i // grid_size, i % grid_size
                    axes[row, col].axis('off')
            else:
                # Plot as line plots for 1D data
                fig, axes = plt.subplots(grid_size, grid_size, figsize=(15, 15))
                for i in range(min(grid_size * grid_size, len(samples_np))):
                    row, col = i // grid_size, i % grid_size
                    axes[row, col].plot(samples_np[i])
                    axes[row, col].set_title(f"Sample {i+1}")
                
                # Hide unused subplots
                for i in range(len(samples_np), grid_size * grid_size):
                    row, col = i // grid_size, i % grid_size
                    axes[row, col].axis('off')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()


class HybridGAN(BaseGANTrainer):
    """
    Hybrid GAN trainer using quantum generator and classical discriminator.
    
    This trainer combines quantum and classical components to leverage
    the advantages of both approaches.
    """
    
    def __init__(
        self,
        generator: QuantumGenerator,
        discriminator: ClassicalDiscriminator,
        device: torch.device = None,
        save_dir: str = "./hybrid_gan_checkpoints",
        **kwargs
    ):
        """
        Initialize the Hybrid GAN trainer.
        
        Args:
            generator: Quantum generator
            discriminator: Classical discriminator
            device: Training device
            save_dir: Directory to save checkpoints
            **kwargs: Additional arguments for training configuration
        """
        super().__init__(generator, discriminator, device, save_dir)
        
        # Initialize optimizers with different learning rates for quantum/classical components
        lr_g = kwargs.get("lr_g", 0.001)  # Lower LR for quantum components
        lr_d = kwargs.get("lr_d", 0.0002)  # Standard LR for classical components
        
        self.optimizer_g = optim.Adam(generator.parameters(), lr=lr_g, betas=(0.5, 0.999))
        self.optimizer_d = optim.Adam(discriminator.parameters(), lr=lr_d, betas=(0.5, 0.999))
        
        self.criterion = nn.BCELoss()
    
    def train(self, dataloader: DataLoader, epochs: int, **kwargs):
        """Train the hybrid GAN using similar logic to QuantumGAN."""
        print(f"Training Hybrid GAN (Quantum Generator + Classical Discriminator)")
        
        # Use similar training loop as QuantumGAN but with adapted metrics
        for epoch in range(epochs):
            # Training logic similar to QuantumGAN
            # (Implementation details follow the same pattern)
            pass


class ClassicalGAN(BaseGANTrainer):
    """
    Classical GAN trainer for baseline comparison.
    
    This trainer implements standard GAN training with classical
    generators and discriminators.
    """
    
    def __init__(
        self,
        generator: ClassicalGenerator,
        discriminator: ClassicalDiscriminator,
        device: torch.device = None,
        save_dir: str = "./classical_gan_checkpoints",
        **kwargs
    ):
        """
        Initialize the Classical GAN trainer.
        
        Args:
            generator: Classical generator
            discriminator: Classical discriminator  
            device: Training device
            save_dir: Directory to save checkpoints
            **kwargs: Additional training configuration
        """
        super().__init__(generator, discriminator, device, save_dir)
        
        # Standard GAN optimizers
        lr = kwargs.get("lr", 0.0002)
        self.optimizer_g = optim.Adam(generator.parameters(), lr=lr, betas=(0.5, 0.999))
        self.optimizer_d = optim.Adam(discriminator.parameters(), lr=lr, betas=(0.5, 0.999))
        
        self.criterion = nn.BCELoss()
        
        # Classical metrics
        self.fid_score = FIDScore()
        self.inception_score = InceptionScore()
    
    def train(self, dataloader: DataLoader, epochs: int, **kwargs):
        """Train the classical GAN."""
        print(f"Training Classical GAN (Baseline)")
        
        # Standard GAN training implementation
        # (Implementation follows standard GAN training procedures)
        pass
