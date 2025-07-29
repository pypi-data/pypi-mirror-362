"""
Classical Discriminator implementation for QGANS Pro.

This module provides classical GAN discriminators for baseline comparison
with quantum-enhanced versions.
"""

from typing import Dict, List, Optional, Tuple
import torch
import torch.nn as nn


class ClassicalDiscriminator(nn.Module):
    """
    Classical Discriminator using Multi-Layer Perceptrons.
    
    This is a standard classical GAN discriminator used as a baseline
    for comparison with quantum discriminators.
    """
    
    def __init__(
        self,
        input_dim: int = 784,
        hidden_dims: Optional[List[int]] = None,
        activation: str = "leaky_relu",
        use_batch_norm: bool = False,
        dropout_rate: float = 0.3,
        use_spectral_norm: bool = False,
    ):
        """
        Initialize the Classical Discriminator.
        
        Args:
            input_dim: Dimension of input data
            hidden_dims: List of hidden layer dimensions
            activation: Activation function ('relu', 'leaky_relu', 'gelu')
            use_batch_norm: Whether to use batch normalization
            dropout_rate: Dropout rate (0.0 = no dropout)
            use_spectral_norm: Whether to use spectral normalization
        """
        super().__init__()
        
        self.input_dim = input_dim
        
        if hidden_dims is None:
            # Default architecture
            hidden_dims = [1024, 512, 256]
        
        # Choose activation function
        if activation == "relu":
            act_fn = nn.ReLU()
        elif activation == "leaky_relu":
            act_fn = nn.LeakyReLU(0.2)
        elif activation == "gelu":
            act_fn = nn.GELU()
        else:
            act_fn = nn.LeakyReLU(0.2)
        
        # Build network layers
        layers = []
        current_dim = input_dim
        
        for i, hidden_dim in enumerate(hidden_dims):
            # Linear layer
            linear = nn.Linear(current_dim, hidden_dim)
            
            # Apply spectral normalization if requested
            if use_spectral_norm:
                linear = nn.utils.spectral_norm(linear)
            
            layers.append(linear)
            
            # Batch normalization (usually not used in discriminator)
            if use_batch_norm and i > 0:  # Skip BN on first layer
                layers.append(nn.BatchNorm1d(hidden_dim))
            
            # Activation
            layers.append(act_fn)
            
            # Dropout
            if dropout_rate > 0.0:
                layers.append(nn.Dropout(dropout_rate))
            
            current_dim = hidden_dim
        
        # Output layer (single neuron for binary classification)
        output_linear = nn.Linear(current_dim, 1)
        if use_spectral_norm:
            output_linear = nn.utils.spectral_norm(output_linear)
        
        layers.append(output_linear)
        layers.append(nn.Sigmoid())
        
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
    
    def forward(self, data: torch.Tensor) -> torch.Tensor:
        """
        Forward pass through the discriminator.
        
        Args:
            data: Input data [batch_size, input_dim]
            
        Returns:
            Classification probabilities [batch_size, 1]
        """
        # Flatten input if needed
        if data.dim() > 2:
            data = data.view(data.size(0), -1)
        
        return self.network(data)
    
    def get_model_info(self) -> Dict:
        """
        Get information about the model.
        
        Returns:
            Dictionary with model information
        """
        total_params = sum(p.numel() for p in self.parameters())
        trainable_params = sum(p.numel() for p in self.parameters() if p.requires_grad)
        
        return {
            "model_type": "ClassicalDiscriminator",
            "input_dim": self.input_dim,
            "total_parameters": total_params,
            "trainable_parameters": trainable_params,
            "network_depth": len([m for m in self.network if isinstance(m, nn.Linear)]),
        }


class ConvolutionalDiscriminator(nn.Module):
    """
    Convolutional Discriminator for image data.
    
    This discriminator uses convolutional layers to process images,
    similar to DCGAN architecture.
    """
    
    def __init__(
        self,
        input_channels: int = 1,
        input_size: int = 28,
        base_channels: int = 64,
        use_batch_norm: bool = False,
        dropout_rate: float = 0.3,
        use_spectral_norm: bool = True,
    ):
        """
        Initialize the Convolutional Discriminator.
        
        Args:
            input_channels: Number of input channels (1 for grayscale, 3 for RGB)
            input_size: Size of input images (assumes square images)
            base_channels: Base number of channels
            use_batch_norm: Whether to use batch normalization
            dropout_rate: Dropout rate
            use_spectral_norm: Whether to use spectral normalization
        """
        super().__init__()
        
        self.input_channels = input_channels
        self.input_size = input_size
        
        # Calculate number of downsampling layers
        n_downsample = 0
        size = input_size
        while size > 4:
            size //= 2
            n_downsample += 1
        
        # Convolutional layers
        layers = []
        in_channels = input_channels
        
        for i in range(n_downsample):
            out_channels = base_channels * (2 ** i)
            
            # Convolutional layer
            conv = nn.Conv2d(in_channels, out_channels, 4, 2, 1)
            if use_spectral_norm:
                conv = nn.utils.spectral_norm(conv)
            layers.append(conv)
            
            # Batch normalization (skip on first layer)
            if use_batch_norm and i > 0:
                layers.append(nn.BatchNorm2d(out_channels))
            
            # Activation
            layers.append(nn.LeakyReLU(0.2, inplace=True))
            
            # Dropout
            if dropout_rate > 0.0:
                layers.append(nn.Dropout2d(dropout_rate))
            
            in_channels = out_channels
        
        self.conv_layers = nn.Sequential(*layers)
        
        # Calculate the size after convolutions
        final_size = input_size
        for _ in range(n_downsample):
            final_size = (final_size - 4 + 2) // 2 + 1
        
        # Final fully connected layer
        self.fc_input_dim = in_channels * final_size * final_size
        fc = nn.Linear(self.fc_input_dim, 1)
        if use_spectral_norm:
            fc = nn.utils.spectral_norm(fc)
        
        self.fc = nn.Sequential(
            fc,
            nn.Sigmoid()
        )
        
        # Initialize weights
        self.apply(self._init_weights)
    
    def _init_weights(self, module):
        """Initialize network weights."""
        if isinstance(module, (nn.Linear, nn.Conv2d)):
            nn.init.normal_(module.weight, 0.0, 0.02)
            if module.bias is not None:
                nn.init.zeros_(module.bias)
        elif isinstance(module, nn.BatchNorm2d):
            nn.init.ones_(module.weight)
            nn.init.zeros_(module.bias)
    
    def forward(self, data: torch.Tensor) -> torch.Tensor:
        """
        Forward pass through the discriminator.
        
        Args:
            data: Input images [batch_size, channels, height, width]
            
        Returns:
            Classification probabilities [batch_size, 1]
        """
        # Apply convolutional layers
        x = self.conv_layers(data)
        
        # Flatten for fully connected layer
        x = x.view(x.size(0), -1)
        
        # Final classification
        x = self.fc(x)
        
        return x
    
    def get_model_info(self) -> Dict:
        """
        Get information about the model.
        
        Returns:
            Dictionary with model information
        """
        total_params = sum(p.numel() for p in self.parameters())
        trainable_params = sum(p.numel() for p in self.parameters() if p.requires_grad)
        
        return {
            "model_type": "ConvolutionalDiscriminator",
            "input_channels": self.input_channels,
            "input_size": self.input_size,
            "total_parameters": total_params,
            "trainable_parameters": trainable_params,
        }


class WassersteinDiscriminator(nn.Module):
    """
    Wasserstein Discriminator (Critic) for WGAN.
    
    This discriminator doesn't use sigmoid activation and is designed
    for Wasserstein GAN training.
    """
    
    def __init__(
        self,
        input_dim: int = 784,
        hidden_dims: Optional[List[int]] = None,
        activation: str = "leaky_relu",
        use_batch_norm: bool = False,
        dropout_rate: float = 0.0,
        use_spectral_norm: bool = True,
        gradient_penalty: bool = True,
    ):
        """
        Initialize the Wasserstein Discriminator.
        
        Args:
            input_dim: Dimension of input data
            hidden_dims: List of hidden layer dimensions
            activation: Activation function
            use_batch_norm: Whether to use batch normalization
            dropout_rate: Dropout rate
            use_spectral_norm: Whether to use spectral normalization
            gradient_penalty: Whether to use gradient penalty (instead of weight clipping)
        """
        super().__init__()
        
        self.input_dim = input_dim
        self.gradient_penalty = gradient_penalty
        
        if hidden_dims is None:
            hidden_dims = [512, 256, 128]
        
        # Choose activation function
        if activation == "relu":
            act_fn = nn.ReLU()
        elif activation == "leaky_relu":
            act_fn = nn.LeakyReLU(0.2)
        elif activation == "gelu":
            act_fn = nn.GELU()
        else:
            act_fn = nn.LeakyReLU(0.2)
        
        # Build network layers
        layers = []
        current_dim = input_dim
        
        for i, hidden_dim in enumerate(hidden_dims):
            # Linear layer
            linear = nn.Linear(current_dim, hidden_dim)
            
            # Apply spectral normalization if requested
            if use_spectral_norm:
                linear = nn.utils.spectral_norm(linear)
            
            layers.append(linear)
            
            # Batch normalization
            if use_batch_norm:
                layers.append(nn.BatchNorm1d(hidden_dim))
            
            # Activation
            layers.append(act_fn)
            
            # Dropout
            if dropout_rate > 0.0:
                layers.append(nn.Dropout(dropout_rate))
            
            current_dim = hidden_dim
        
        # Output layer (no sigmoid for Wasserstein)
        output_linear = nn.Linear(current_dim, 1)
        if use_spectral_norm:
            output_linear = nn.utils.spectral_norm(output_linear)
        
        layers.append(output_linear)
        
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
    
    def forward(self, data: torch.Tensor) -> torch.Tensor:
        """
        Forward pass through the critic.
        
        Args:
            data: Input data [batch_size, input_dim]
            
        Returns:
            Critic scores [batch_size, 1] (no sigmoid)
        """
        # Flatten input if needed
        if data.dim() > 2:
            data = data.view(data.size(0), -1)
        
        return self.network(data)
    
    def clip_weights(self, clip_value: float = 0.01):
        """
        Clip weights for Wasserstein GAN (if not using gradient penalty).
        
        Args:
            clip_value: Clipping value
        """
        if not self.gradient_penalty:
            for p in self.parameters():
                p.data.clamp_(-clip_value, clip_value)
    
    def get_model_info(self) -> Dict:
        """
        Get information about the model.
        
        Returns:
            Dictionary with model information
        """
        total_params = sum(p.numel() for p in self.parameters())
        trainable_params = sum(p.numel() for p in self.parameters() if p.requires_grad)
        
        return {
            "model_type": "WassersteinDiscriminator",
            "input_dim": self.input_dim,
            "gradient_penalty": self.gradient_penalty,
            "total_parameters": total_params,
            "trainable_parameters": trainable_params,
            "network_depth": len([m for m in self.network if isinstance(m, nn.Linear)]),
        }
