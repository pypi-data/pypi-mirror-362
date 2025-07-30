"""
Visualization utilities for QGANS Pro.

This module provides functions for visualizing generated samples,
training progress, and quantum circuits.
"""

from typing import Any, Dict, List, Optional, Tuple, Union
import numpy as np
import torch
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import Normalize
import seaborn as sns

try:
    from sklearn.manifold import TSNE
    from sklearn.decomposition import PCA
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


def plot_generated_samples(
    samples: torch.Tensor,
    title: str = "Generated Samples",
    save_path: Optional[str] = None,
    grid_size: int = 8,
    figsize: Tuple[int, int] = (12, 12),
    cmap: str = "gray",
) -> None:
    """
    Plot generated samples in a grid.
    
    Args:
        samples: Generated samples tensor
        title: Plot title
        save_path: Path to save the plot
        grid_size: Size of the sample grid
        figsize: Figure size
        cmap: Colormap for images
    """
    # Convert to numpy
    if isinstance(samples, torch.Tensor):
        samples = samples.detach().cpu().numpy()
    
    # Determine sample type and dimensions
    n_samples = len(samples)
    sample_shape = samples.shape[1:]
    
    # Create figure
    fig, axes = plt.subplots(grid_size, grid_size, figsize=figsize)
    fig.suptitle(title, fontsize=16)
    
    # Plot samples
    for i in range(min(grid_size * grid_size, n_samples)):
        row, col = i // grid_size, i % grid_size
        sample = samples[i]
        
        if len(sample_shape) == 1:
            # 1D data - plot as line
            if grid_size == 1:
                axes.plot(sample)
                axes.set_title(f"Sample {i+1}")
            else:
                axes[row, col].plot(sample)
                axes[row, col].set_title(f"Sample {i+1}")
                axes[row, col].grid(True, alpha=0.3)
                
        elif len(sample_shape) == 2:
            # 2D data - plot as heatmap/image
            if grid_size == 1:
                im = axes.imshow(sample, cmap=cmap)
                axes.set_title(f"Sample {i+1}")
                axes.axis('off')
            else:
                im = axes[row, col].imshow(sample, cmap=cmap)
                axes[row, col].set_title(f"Sample {i+1}")
                axes[row, col].axis('off')
                
        elif len(sample_shape) == 3:
            # 3D data (e.g., RGB images) - plot as image
            # Handle different channel orders
            if sample_shape[0] in [1, 3]:  # CHW format
                sample = np.transpose(sample, (1, 2, 0))
            
            if sample_shape[-1] == 1:  # Single channel
                sample = sample.squeeze(-1)
                cmap_use = cmap
            else:  # Multi-channel
                sample = np.clip(sample, 0, 1)
                cmap_use = None
            
            if grid_size == 1:
                axes.imshow(sample, cmap=cmap_use)
                axes.set_title(f"Sample {i+1}")
                axes.axis('off')
            else:
                axes[row, col].imshow(sample, cmap=cmap_use)
                axes[row, col].set_title(f"Sample {i+1}")
                axes[row, col].axis('off')
    
    # Hide unused subplots
    for i in range(n_samples, grid_size * grid_size):
        row, col = i // grid_size, i % grid_size
        if grid_size > 1:
            axes[row, col].axis('off')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()


def plot_training_curves(
    history: Dict[str, List],
    title: str = "Training Progress",
    save_path: Optional[str] = None,
    figsize: Tuple[int, int] = (15, 5),
) -> None:
    """
    Plot training loss and metrics curves.
    
    Args:
        history: Training history dictionary
        title: Plot title
        save_path: Path to save the plot
        figsize: Figure size
    """
    # Determine number of subplots needed
    n_plots = 1  # Always have loss plot
    
    # Check for metrics
    metrics = history.get("metrics", {})
    if metrics:
        n_plots += len(metrics)
    
    # Create subplots
    fig, axes = plt.subplots(1, min(n_plots, 3), figsize=figsize)
    if n_plots == 1:
        axes = [axes]
    
    # Plot losses
    ax_idx = 0
    if "generator_loss" in history and "discriminator_loss" in history:
        axes[ax_idx].plot(history["generator_loss"], label="Generator", color='blue', alpha=0.8)
        axes[ax_idx].plot(history["discriminator_loss"], label="Discriminator", color='red', alpha=0.8)
        axes[ax_idx].set_title("Training Losses")
        axes[ax_idx].set_xlabel("Epoch")
        axes[ax_idx].set_ylabel("Loss")
        axes[ax_idx].legend()
        axes[ax_idx].grid(True, alpha=0.3)
        ax_idx += 1
    
    # Plot metrics
    for i, (metric_name, values) in enumerate(metrics.items()):
        if ax_idx >= len(axes):
            break
            
        axes[ax_idx].plot(values, label=metric_name, alpha=0.8)
        axes[ax_idx].set_title(f"{metric_name.replace('_', ' ').title()}")
        axes[ax_idx].set_xlabel("Epoch")
        axes[ax_idx].set_ylabel("Value")
        axes[ax_idx].legend()
        axes[ax_idx].grid(True, alpha=0.3)
        ax_idx += 1
    
    # Hide unused subplots
    for i in range(ax_idx, len(axes)):
        axes[i].axis('off')
    
    plt.suptitle(title, fontsize=16)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()


def plot_data_distribution(
    real_data: torch.Tensor,
    generated_data: torch.Tensor,
    title: str = "Data Distribution Comparison",
    save_path: Optional[str] = None,
    figsize: Tuple[int, int] = (12, 8),
    max_features: int = 6,
) -> None:
    """
    Compare distributions of real and generated data.
    
    Args:
        real_data: Real data samples
        generated_data: Generated data samples
        title: Plot title
        save_path: Path to save the plot
        figsize: Figure size
        max_features: Maximum number of features to plot
    """
    # Convert to numpy
    if isinstance(real_data, torch.Tensor):
        real_data = real_data.detach().cpu().numpy()
    if isinstance(generated_data, torch.Tensor):
        generated_data = generated_data.detach().cpu().numpy()
    
    # Flatten data if multi-dimensional
    if real_data.ndim > 2:
        real_data = real_data.reshape(real_data.shape[0], -1)
    if generated_data.ndim > 2:
        generated_data = generated_data.reshape(generated_data.shape[0], -1)
    
    n_features = min(real_data.shape[1], max_features)
    
    # Create subplots
    n_cols = min(3, n_features)
    n_rows = (n_features + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
    if n_features == 1:
        axes = [axes]
    elif n_rows == 1:
        axes = axes.reshape(1, -1)
    
    # Plot feature distributions
    for i in range(n_features):
        row, col = i // n_cols, i % n_cols
        ax = axes[row, col] if n_rows > 1 else axes[col]
        
        # Plot histograms
        ax.hist(real_data[:, i], bins=50, alpha=0.7, label='Real', density=True, color='blue')
        ax.hist(generated_data[:, i], bins=50, alpha=0.7, label='Generated', density=True, color='red')
        
        ax.set_title(f"Feature {i+1}")
        ax.set_xlabel("Value")
        ax.set_ylabel("Density")
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    # Hide unused subplots
    for i in range(n_features, n_rows * n_cols):
        row, col = i // n_cols, i % n_cols
        if n_rows > 1:
            axes[row, col].axis('off')
        else:
            axes[col].axis('off')
    
    plt.suptitle(title, fontsize=16)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()


def plot_latent_space(
    real_data: torch.Tensor,
    generated_data: torch.Tensor,
    method: str = "tsne",
    title: str = "Latent Space Visualization",
    save_path: Optional[str] = None,
    figsize: Tuple[int, int] = (10, 8),
    max_samples: int = 2000,
) -> None:
    """
    Visualize data in 2D latent space using dimensionality reduction.
    
    Args:
        real_data: Real data samples
        generated_data: Generated data samples
        method: Dimensionality reduction method ('tsne', 'pca')
        title: Plot title
        save_path: Path to save the plot
        figsize: Figure size
        max_samples: Maximum samples to use for visualization
    """
    if not SKLEARN_AVAILABLE:
        print("Warning: scikit-learn not available. Skipping latent space visualization.")
        return
    
    # Convert to numpy
    if isinstance(real_data, torch.Tensor):
        real_data = real_data.detach().cpu().numpy()
    if isinstance(generated_data, torch.Tensor):
        generated_data = generated_data.detach().cpu().numpy()
    
    # Flatten data
    if real_data.ndim > 2:
        real_data = real_data.reshape(real_data.shape[0], -1)
    if generated_data.ndim > 2:
        generated_data = generated_data.reshape(generated_data.shape[0], -1)
    
    # Subsample if too many samples
    if len(real_data) > max_samples:
        idx = np.random.choice(len(real_data), max_samples, replace=False)
        real_data = real_data[idx]
    
    if len(generated_data) > max_samples:
        idx = np.random.choice(len(generated_data), max_samples, replace=False)
        generated_data = generated_data[idx]
    
    # Combine data
    combined_data = np.vstack([real_data, generated_data])
    labels = np.hstack([np.zeros(len(real_data)), np.ones(len(generated_data))])
    
    # Apply dimensionality reduction
    if method.lower() == "tsne":
        reducer = TSNE(n_components=2, random_state=42, perplexity=min(30, len(combined_data)//4))
    elif method.lower() == "pca":
        reducer = PCA(n_components=2)
    else:
        raise ValueError(f"Unknown method: {method}")
    
    reduced_data = reducer.fit_transform(combined_data)
    
    # Split back
    real_reduced = reduced_data[labels == 0]
    gen_reduced = reduced_data[labels == 1]
    
    # Create plot
    plt.figure(figsize=figsize)
    
    plt.scatter(real_reduced[:, 0], real_reduced[:, 1], 
               alpha=0.6, label='Real', s=20, c='blue')
    plt.scatter(gen_reduced[:, 0], gen_reduced[:, 1], 
               alpha=0.6, label='Generated', s=20, c='red')
    
    plt.title(f"{title} ({method.upper()})")
    plt.xlabel(f"{method.upper()} Component 1")
    plt.ylabel(f"{method.upper()} Component 2")
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()


def plot_quantum_circuit_parameters(
    parameters: torch.Tensor,
    title: str = "Quantum Circuit Parameters",
    save_path: Optional[str] = None,
    figsize: Tuple[int, int] = (12, 6),
) -> None:
    """
    Visualize quantum circuit parameters.
    
    Args:
        parameters: Quantum circuit parameters
        title: Plot title
        save_path: Path to save the plot
        figsize: Figure size
    """
    if isinstance(parameters, torch.Tensor):
        parameters = parameters.detach().cpu().numpy()
    
    fig, axes = plt.subplots(1, 2, figsize=figsize)
    
    # Parameter distribution
    axes[0].hist(parameters, bins=50, alpha=0.7, edgecolor='black')
    axes[0].set_title("Parameter Distribution")
    axes[0].set_xlabel("Parameter Value")
    axes[0].set_ylabel("Frequency")
    axes[0].grid(True, alpha=0.3)
    
    # Parameter evolution (if parameters represent time series)
    axes[1].plot(parameters, alpha=0.8)
    axes[1].set_title("Parameter Values")
    axes[1].set_xlabel("Parameter Index")
    axes[1].set_ylabel("Value")
    axes[1].grid(True, alpha=0.3)
    
    plt.suptitle(title, fontsize=16)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()


def visualize_quantum_circuit(
    circuit: Any,
    title: str = "Quantum Circuit",
    save_path: Optional[str] = None,
    figsize: Tuple[int, int] = (12, 8),
) -> None:
    """
    Visualize quantum circuit structure.
    
    Args:
        circuit: Quantum circuit object
        title: Plot title
        save_path: Path to save the plot
        figsize: Figure size
    """
    try:
        # Try different circuit visualization methods
        if hasattr(circuit, 'draw'):
            # Qiskit circuit
            try:
                fig = circuit.draw(output='mpl', style='iqp')
                if save_path:
                    fig.savefig(save_path, dpi=300, bbox_inches='tight')
                    plt.close(fig)
                else:
                    plt.show()
                return
            except Exception as e:
                print(f"Qiskit visualization failed: {e}")
        
        # Fallback: create a simple text representation
        plt.figure(figsize=figsize)
        plt.text(0.5, 0.5, f"Quantum Circuit\n{str(circuit)}", 
                ha='center', va='center', fontsize=12,
                bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"))
        plt.title(title)
        plt.axis('off')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
        else:
            plt.show()
            
    except Exception as e:
        print(f"Circuit visualization failed: {e}")


def plot_metric_comparison(
    metrics_dict: Dict[str, Dict[str, float]],
    title: str = "Model Comparison",
    save_path: Optional[str] = None,
    figsize: Tuple[int, int] = (12, 8),
) -> None:
    """
    Plot comparison of metrics across different models.
    
    Args:
        metrics_dict: Dictionary mapping model names to metric dictionaries
        title: Plot title
        save_path: Path to save the plot
        figsize: Figure size
    """
    # Extract metric names
    all_metrics = set()
    for model_metrics in metrics_dict.values():
        all_metrics.update(model_metrics.keys())
    
    metric_names = sorted(list(all_metrics))
    model_names = list(metrics_dict.keys())
    
    # Prepare data for plotting
    n_metrics = len(metric_names)
    n_models = len(model_names)
    
    # Create bar plot
    x = np.arange(n_metrics)
    width = 0.8 / n_models
    
    plt.figure(figsize=figsize)
    
    for i, model_name in enumerate(model_names):
        values = []
        for metric_name in metric_names:
            value = metrics_dict[model_name].get(metric_name, 0)
            values.append(value)
        
        plt.bar(x + i * width, values, width, label=model_name, alpha=0.8)
    
    plt.xlabel('Metrics')
    plt.ylabel('Value')
    plt.title(title)
    plt.xticks(x + width * (n_models - 1) / 2, metric_names, rotation=45, ha='right')
    plt.legend()
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()


def create_animation(
    sample_history: List[torch.Tensor],
    title: str = "GAN Training Progress",
    save_path: Optional[str] = None,
    interval: int = 200,
    grid_size: int = 8,
) -> None:
    """
    Create animation showing GAN training progress.
    
    Args:
        sample_history: List of sample tensors from different epochs
        title: Animation title
        save_path: Path to save animation (as GIF)
        interval: Interval between frames in milliseconds
        grid_size: Size of sample grid
    """
    try:
        from matplotlib.animation import FuncAnimation, PillowWriter
        
        fig, ax = plt.subplots(figsize=(10, 10))
        
        def update_frame(frame_idx):
            ax.clear()
            samples = sample_history[frame_idx]
            
            # Plot samples
            if isinstance(samples, torch.Tensor):
                samples = samples.detach().cpu().numpy()
            
            # Create grid of samples
            n_samples = min(grid_size * grid_size, len(samples))
            
            if samples.ndim > 2:
                # Image data
                sample_shape = samples.shape[1:]
                if len(sample_shape) == 2 or (len(sample_shape) == 3 and sample_shape[0] in [1, 3]):
                    # Create image grid
                    grid_img = np.zeros((grid_size * sample_shape[-2], grid_size * sample_shape[-1]))
                    
                    for i in range(n_samples):
                        row, col = i // grid_size, i % grid_size
                        sample = samples[i]
                        
                        if len(sample_shape) == 3 and sample_shape[0] == 1:
                            sample = sample[0]
                        elif len(sample_shape) == 3 and sample_shape[0] == 3:
                            sample = np.transpose(sample, (1, 2, 0)).mean(axis=2)
                        
                        y_start, y_end = row * sample_shape[-2], (row + 1) * sample_shape[-2]
                        x_start, x_end = col * sample_shape[-1], (col + 1) * sample_shape[-1]
                        grid_img[y_start:y_end, x_start:x_end] = sample
                    
                    ax.imshow(grid_img, cmap='gray')
                    ax.axis('off')
            
            ax.set_title(f"{title} - Epoch {frame_idx + 1}")
        
        # Create animation
        anim = FuncAnimation(fig, update_frame, frames=len(sample_history), 
                           interval=interval, repeat=True)
        
        if save_path:
            writer = PillowWriter(fps=1000//interval)
            anim.save(save_path, writer=writer)
            plt.close()
        else:
            plt.show()
            
    except ImportError:
        print("Animation requires matplotlib.animation. Saving individual frames instead.")
        
        # Save individual frames
        for i, samples in enumerate(sample_history):
            frame_path = save_path.replace('.gif', f'_frame_{i:03d}.png') if save_path else None
            plot_generated_samples(samples, f"{title} - Epoch {i+1}", frame_path, grid_size)
