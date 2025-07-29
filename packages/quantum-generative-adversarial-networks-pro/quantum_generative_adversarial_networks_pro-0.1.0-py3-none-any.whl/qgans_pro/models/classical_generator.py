"""
Classical Generator implementation for QGANS Pro.

This module provides classical GAN generators for baseline comparison
with quantum-enhanced versions.
"""

from typing import Dict, List, Optional, Tuple
import torch
import torch.nn as nn


class ClassicalGenerator(nn.Module):
    """
    Classical Generator using Multi-Layer Perceptrons.
    
    This is a standard classical GAN generator used as a baseline
    for comparison with quantum generators.
    """
    
    def __init__(
        self,
        noise_dim: int = 100,
        output_dim: int = 784,
        hidden_dims: Optional[List[int]] = None,
        activation: str = "relu",
        output_activation: str = "tanh",
        use_batch_norm: bool = True,
        dropout_rate: float = 0.0,
    ):
        """
        Initialize the Classical Generator.
        
        Args:
            noise_dim: Dimension of input noise vector
            output_dim: Dimension of generated data
            hidden_dims: List of hidden layer dimensions
            activation: Activation function ('relu', 'leaky_relu', 'gelu')
            output_activation: Output activation ('tanh', 'sigmoid', 'none')
            use_batch_norm: Whether to use batch normalization
            dropout_rate: Dropout rate (0.0 = no dropout)
        """
        super().__init__()
        
        self.noise_dim = noise_dim
        self.output_dim = output_dim
        
        if hidden_dims is None:
            # Default architecture
            hidden_dims = [256, 512, 1024]
        
        # Choose activation function
        if activation == "relu":
            act_fn = nn.ReLU()
        elif activation == "leaky_relu":
            act_fn = nn.LeakyReLU(0.2)
        elif activation == "gelu":
            act_fn = nn.GELU()
        else:
            act_fn = nn.ReLU()
        
        # Build network layers
        layers = []
        input_dim = noise_dim
        
        for i, hidden_dim in enumerate(hidden_dims):
            # Linear layer
            layers.append(nn.Linear(input_dim, hidden_dim))
            
            # Batch normalization
            if use_batch_norm:
                layers.append(nn.BatchNorm1d(hidden_dim))
            
            # Activation
            layers.append(act_fn)
            
            # Dropout
            if dropout_rate > 0.0:
                layers.append(nn.Dropout(dropout_rate))
            
            input_dim = hidden_dim
        
        # Output layer
        layers.append(nn.Linear(input_dim, output_dim))
        
        # Output activation
        if output_activation == "tanh":
            layers.append(nn.Tanh())
        elif output_activation == "sigmoid":
            layers.append(nn.Sigmoid())
        # 'none' means no output activation
        
        self.network = nn.Sequential(*layers)
        
        # Initialize weights
        self.apply(self._init_weights)
    
    def _init_weights(self, module):
        """Initialize network weights."""
        if isinstance(module, nn.Linear):
            nn.init.xavier_uniform_(module.weight)
            if module.bias is not None:
                nn.init.zeros_(module.bias)
        elif isinstance(module, nn.BatchNorm1d):
            nn.init.ones_(module.weight)
            nn.init.zeros_(module.bias)
    
    def forward(self, noise: torch.Tensor) -> torch.Tensor:
        """
        Forward pass through the generator.
        
        Args:
            noise: Random noise input [batch_size, noise_dim]
            
        Returns:
            Generated data [batch_size, output_dim]
        """
        return self.network(noise)
    
    def sample(self, batch_size: int, device: Optional[torch.device] = None) -> torch.Tensor:
        """
        Sample synthetic data from the generator.
        
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
    
    def get_model_info(self) -> Dict:
        """
        Get information about the model.
        
        Returns:
            Dictionary with model information
        """
        total_params = sum(p.numel() for p in self.parameters())
        trainable_params = sum(p.numel() for p in self.parameters() if p.requires_grad)
        
        return {
            "model_type": "ClassicalGenerator",
            "noise_dim": self.noise_dim,
            "output_dim": self.output_dim,
            "total_parameters": total_params,
            "trainable_parameters": trainable_params,
            "network_depth": len([m for m in self.network if isinstance(m, nn.Linear)]),
        }


class ConvolutionalGenerator(nn.Module):
    """
    Convolutional Generator for image data.
    
    This generator uses transposed convolutions to generate images,
    similar to DCGAN architecture.
    """
    
    def __init__(
        self,
        noise_dim: int = 100,
        output_channels: int = 1,
        output_size: int = 28,
        base_channels: int = 64,
        use_batch_norm: bool = True,
    ):
        """
        Initialize the Convolutional Generator.
        
        Args:
            noise_dim: Dimension of input noise
            output_channels: Number of output channels (1 for grayscale, 3 for RGB)
            output_size: Size of output images (assumes square images)
            base_channels: Base number of channels
            use_batch_norm: Whether to use batch normalization
        """
        super().__init__()
        
        self.noise_dim = noise_dim
        self.output_channels = output_channels
        self.output_size = output_size
        
        # Calculate initial size for transposed convolutions
        # We'll start with 4x4 and upsample
        self.init_size = 4
        
        # Calculate channel multipliers
        n_upsample = 0
        size = self.init_size
        while size < output_size:
            size *= 2
            n_upsample += 1
        
        # Fully connected layer to create initial feature map
        self.fc = nn.Linear(noise_dim, base_channels * 8 * self.init_size * self.init_size)
        
        # Transposed convolutional layers
        layers = []
        in_channels = base_channels * 8
        
        for i in range(n_upsample):
            out_channels = in_channels // 2 if i < n_upsample - 1 else output_channels
            
            if i < n_upsample - 1:
                # Intermediate layers
                layers.extend([
                    nn.ConvTranspose2d(in_channels, out_channels, 4, 2, 1),
                    nn.BatchNorm2d(out_channels) if use_batch_norm else nn.Identity(),
                    nn.ReLU(inplace=True)
                ])
            else:
                # Final layer
                layers.extend([
                    nn.ConvTranspose2d(in_channels, out_channels, 4, 2, 1),
                    nn.Tanh()
                ])
            
            in_channels = out_channels
        
        self.conv_layers = nn.Sequential(*layers)
        
        # Initialize weights
        self.apply(self._init_weights)
    
    def _init_weights(self, module):
        """Initialize network weights."""
        if isinstance(module, (nn.Linear, nn.ConvTranspose2d)):
            nn.init.normal_(module.weight, 0.0, 0.02)
            if module.bias is not None:
                nn.init.zeros_(module.bias)
        elif isinstance(module, nn.BatchNorm2d):
            nn.init.ones_(module.weight)
            nn.init.zeros_(module.bias)
    
    def forward(self, noise: torch.Tensor) -> torch.Tensor:
        """
        Forward pass through the generator.
        
        Args:
            noise: Random noise input [batch_size, noise_dim]
            
        Returns:
            Generated images [batch_size, channels, height, width]
        """
        batch_size = noise.size(0)
        
        # Transform noise to initial feature map
        x = self.fc(noise)
        x = x.view(batch_size, -1, self.init_size, self.init_size)
        
        # Apply transposed convolutions
        x = self.conv_layers(x)
        
        # Crop to exact output size if needed
        if x.size(-1) != self.output_size:
            x = x[:, :, :self.output_size, :self.output_size]
        
        return x
    
    def sample(self, batch_size: int, device: Optional[torch.device] = None) -> torch.Tensor:
        """
        Sample synthetic images from the generator.
        
        Args:
            batch_size: Number of samples to generate
            device: Device to generate samples on
            
        Returns:
            Generated images [batch_size, channels, height, width]
        """
        if device is None:
            device = next(self.parameters()).device
        
        # Sample random noise
        noise = torch.randn(batch_size, self.noise_dim, device=device)
        
        # Generate images
        with torch.no_grad():
            generated = self.forward(noise)
        
        return generated
    
    def get_model_info(self) -> Dict:
        """
        Get information about the model.
        
        Returns:
            Dictionary with model information
        """
        total_params = sum(p.numel() for p in self.parameters())
        trainable_params = sum(p.numel() for p in self.parameters() if p.requires_grad)
        
        return {
            "model_type": "ConvolutionalGenerator",
            "noise_dim": self.noise_dim,
            "output_channels": self.output_channels,
            "output_size": self.output_size,
            "total_parameters": total_params,
            "trainable_parameters": trainable_params,
        }
