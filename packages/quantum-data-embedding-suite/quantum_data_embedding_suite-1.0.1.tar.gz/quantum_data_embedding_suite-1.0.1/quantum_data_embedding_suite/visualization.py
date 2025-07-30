"""
Visualization utilities for quantum data embedding.
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional, Tuple, List, Any
import warnings
from .licensing import requires_license


@requires_license()
def plot_kernel_comparison(
    K_quantum: np.ndarray,
    K_classical: np.ndarray,
    output_file: Optional[str] = None,
    figsize: Tuple[int, int] = (12, 5)
) -> None:
    """
    Plot comparison between quantum and classical kernel matrices.
    
    Parameters
    ----------
    K_quantum : array-like
        Quantum kernel matrix
    K_classical : array-like
        Classical kernel matrix
    output_file : str, optional
        Path to save the plot
    figsize : tuple, default=(12, 5)
        Figure size (width, height)
    """
    fig, axes = plt.subplots(1, 3, figsize=figsize)
    
    # Plot quantum kernel
    im1 = axes[0].imshow(K_quantum, cmap='viridis', vmin=0, vmax=1)
    axes[0].set_title('Quantum Kernel')
    axes[0].set_xlabel('Sample Index')
    axes[0].set_ylabel('Sample Index')
    plt.colorbar(im1, ax=axes[0])
    
    # Plot classical kernel
    im2 = axes[1].imshow(K_classical, cmap='viridis', vmin=0, vmax=1)
    axes[1].set_title('Classical Kernel')
    axes[1].set_xlabel('Sample Index')
    axes[1].set_ylabel('Sample Index')
    plt.colorbar(im2, ax=axes[1])
    
    # Plot difference
    diff = K_quantum - K_classical
    im3 = axes[2].imshow(diff, cmap='RdBu', vmin=-1, vmax=1)
    axes[2].set_title('Difference (Q - C)')
    axes[2].set_xlabel('Sample Index')
    axes[2].set_ylabel('Sample Index')
    plt.colorbar(im3, ax=axes[2])
    
    plt.tight_layout()
    
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()


def plot_expressibility_analysis(
    embeddings: List[str],
    expressibility_scores: List[float],
    output_file: Optional[str] = None,
    figsize: Tuple[int, int] = (10, 6)
) -> None:
    """
    Plot expressibility analysis across different embeddings.
    
    Parameters
    ----------
    embeddings : list of str
        Embedding names
    expressibility_scores : list of float
        Expressibility scores for each embedding
    output_file : str, optional
        Path to save the plot
    figsize : tuple, default=(10, 6)
        Figure size (width, height)
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    colors = plt.cm.Set3(np.linspace(0, 1, len(embeddings)))
    bars = ax.bar(embeddings, expressibility_scores, color=colors)
    
    # Add value labels on bars
    for bar, score in zip(bars, expressibility_scores):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{score:.3f}', ha='center', va='bottom')
    
    ax.set_ylabel('Expressibility Score')
    ax.set_title('Expressibility Comparison Across Embeddings')
    ax.set_ylim(0, 1.1)
    
    # Add horizontal line at 0.5 for reference
    ax.axhline(y=0.5, color='gray', linestyle='--', alpha=0.7, label='Baseline')
    ax.legend()
    
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()


def plot_kernel_eigenspectrum(
    K: np.ndarray,
    title: str = "Kernel Eigenspectrum",
    output_file: Optional[str] = None,
    figsize: Tuple[int, int] = (8, 6)
) -> None:
    """
    Plot eigenspectrum of a kernel matrix.
    
    Parameters
    ----------
    K : array-like
        Kernel matrix
    title : str, default="Kernel Eigenspectrum"
        Plot title
    output_file : str, optional
        Path to save the plot
    figsize : tuple, default=(8, 6)
        Figure size (width, height)
    """
    # Compute eigenvalues
    eigenvals = np.linalg.eigvals(K)
    eigenvals = np.real(eigenvals)
    eigenvals = np.sort(eigenvals)[::-1]  # Sort in descending order
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
    
    # Plot eigenvalues
    ax1.plot(eigenvals, 'o-', markersize=4)
    ax1.set_xlabel('Eigenvalue Index')
    ax1.set_ylabel('Eigenvalue')
    ax1.set_title('Eigenvalues')
    ax1.grid(True, alpha=0.3)
    
    # Plot cumulative variance explained
    cumvar = np.cumsum(eigenvals) / np.sum(eigenvals)
    ax2.plot(cumvar, 'o-', markersize=4)
    ax2.axhline(y=0.95, color='red', linestyle='--', alpha=0.7, label='95% threshold')
    ax2.set_xlabel('Eigenvalue Index')
    ax2.set_ylabel('Cumulative Variance Explained')
    ax2.set_title('Cumulative Variance')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    plt.suptitle(title)
    plt.tight_layout()
    
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()


def plot_embedding_landscape(
    X: np.ndarray,
    y: Optional[np.ndarray] = None,
    embedding_type: str = "Unknown",
    output_file: Optional[str] = None,
    figsize: Tuple[int, int] = (10, 8)
) -> None:
    """
    Plot 2D visualization of the embedding landscape.
    
    Parameters
    ----------
    X : array-like
        Data points (will be reduced to 2D if necessary)
    y : array-like, optional
        Labels for coloring
    embedding_type : str, default="Unknown"
        Type of embedding for plot title
    output_file : str, optional
        Path to save the plot
    figsize : tuple, default=(10, 8)
        Figure size (width, height)
    """
    # Reduce to 2D if necessary
    if X.shape[1] > 2:
        try:
            from sklearn.decomposition import PCA
            pca = PCA(n_components=2)
            X_2d = pca.fit_transform(X)
            variance_explained = pca.explained_variance_ratio_
            subtitle = f"PCA projection (explains {np.sum(variance_explained):.1%} variance)"
        except ImportError:
            # Fallback: just take first two dimensions
            X_2d = X[:, :2]
            subtitle = "First two dimensions"
    else:
        X_2d = X
        subtitle = "Original 2D data"
    
    fig, ax = plt.subplots(figsize=figsize)
    
    if y is not None:
        scatter = ax.scatter(X_2d[:, 0], X_2d[:, 1], c=y, cmap='tab10', s=50, alpha=0.7)
        plt.colorbar(scatter, ax=ax, label='Class')
    else:
        ax.scatter(X_2d[:, 0], X_2d[:, 1], s=50, alpha=0.7)
    
    ax.set_xlabel('Component 1')
    ax.set_ylabel('Component 2')
    ax.set_title(f'{embedding_type} Embedding Landscape\n{subtitle}')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()


def plot_gradient_analysis(
    gradients: np.ndarray,
    parameter_names: Optional[List[str]] = None,
    output_file: Optional[str] = None,
    figsize: Tuple[int, int] = (12, 5)
) -> None:
    """
    Plot gradient analysis for trainability assessment.
    
    Parameters
    ----------
    gradients : array-like
        Gradient values (can be 1D or 2D)
    parameter_names : list of str, optional
        Names of parameters
    output_file : str, optional
        Path to save the plot
    figsize : tuple, default=(12, 5)
        Figure size (width, height)
    """
    if gradients.ndim == 1:
        gradients = gradients.reshape(-1, 1)
    
    fig, axes = plt.subplots(1, 2, figsize=figsize)
    
    # Plot gradient magnitudes
    grad_magnitudes = np.linalg.norm(gradients, axis=1)
    axes[0].hist(grad_magnitudes, bins=30, alpha=0.7, edgecolor='black')
    axes[0].set_xlabel('Gradient Magnitude')
    axes[0].set_ylabel('Frequency')
    axes[0].set_title('Gradient Magnitude Distribution')
    axes[0].grid(True, alpha=0.3)
    
    # Plot gradient variance per parameter
    if gradients.shape[1] > 1:
        grad_vars = np.var(gradients, axis=0)
        x_pos = range(len(grad_vars))
        axes[1].bar(x_pos, grad_vars)
        axes[1].set_xlabel('Parameter Index')
        axes[1].set_ylabel('Gradient Variance')
        axes[1].set_title('Gradient Variance per Parameter')
        
        if parameter_names:
            axes[1].set_xticks(x_pos)
            axes[1].set_xticklabels(parameter_names, rotation=45, ha='right')
    else:
        # Single parameter case
        axes[1].plot(gradients[:, 0], 'o-', markersize=3)
        axes[1].set_xlabel('Sample')
        axes[1].set_ylabel('Gradient Value')
        axes[1].set_title('Gradient Evolution')
        axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()


def plot_kernel_alignment_heatmap(
    alignments: np.ndarray,
    embedding_names: List[str],
    output_file: Optional[str] = None,
    figsize: Tuple[int, int] = (8, 6)
) -> None:
    """
    Plot kernel alignment heatmap between different embeddings.
    
    Parameters
    ----------
    alignments : array-like
        Kernel alignment matrix
    embedding_names : list of str
        Names of embeddings
    output_file : str, optional
        Path to save the plot
    figsize : tuple, default=(8, 6)
        Figure size (width, height)
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Create heatmap
    im = ax.imshow(alignments, cmap='viridis', vmin=0, vmax=1)
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Kernel Alignment', rotation=270, labelpad=20)
    
    # Set ticks and labels
    ax.set_xticks(range(len(embedding_names)))
    ax.set_yticks(range(len(embedding_names)))
    ax.set_xticklabels(embedding_names, rotation=45, ha='right')
    ax.set_yticklabels(embedding_names)
    
    # Add text annotations
    for i in range(len(embedding_names)):
        for j in range(len(embedding_names)):
            text = ax.text(j, i, f'{alignments[i, j]:.3f}',
                          ha="center", va="center", color="white" if alignments[i, j] < 0.5 else "black")
    
    ax.set_title('Kernel Alignment Between Embeddings')
    plt.tight_layout()
    
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()


@requires_license(features=["pro"])
def create_embedding_dashboard(
    results: dict,
    output_file: Optional[str] = None,
    figsize: Tuple[int, int] = (16, 12)
) -> None:
    """
    Create a comprehensive dashboard for embedding analysis.
    
    Parameters
    ----------
    results : dict
        Dictionary containing analysis results
    output_file : str, optional
        Path to save the plot
    figsize : tuple, default=(16, 12)
        Figure size (width, height)
    """
    fig = plt.figure(figsize=figsize)
    
    # Create subplot grid
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    # Plot 1: Kernel matrix
    if 'kernel_matrix' in results:
        ax1 = fig.add_subplot(gs[0, 0])
        im = ax1.imshow(results['kernel_matrix'], cmap='viridis')
        ax1.set_title('Quantum Kernel Matrix')
        plt.colorbar(im, ax=ax1, fraction=0.046, pad=0.04)
    
    # Plot 2: Eigenspectrum
    if 'eigenvalues' in results:
        ax2 = fig.add_subplot(gs[0, 1])
        eigenvals = results['eigenvalues']
        ax2.plot(eigenvals, 'o-', markersize=4)
        ax2.set_title('Kernel Eigenspectrum')
        ax2.set_xlabel('Index')
        ax2.set_ylabel('Eigenvalue')
        ax2.grid(True, alpha=0.3)
    
    # Plot 3: Metrics comparison
    if 'metrics' in results:
        ax3 = fig.add_subplot(gs[0, 2])
        metrics = results['metrics']
        metric_names = list(metrics.keys())
        metric_values = list(metrics.values())
        
        bars = ax3.bar(range(len(metric_names)), metric_values)
        ax3.set_title('Embedding Metrics')
        ax3.set_xticks(range(len(metric_names)))
        ax3.set_xticklabels(metric_names, rotation=45, ha='right')
        ax3.set_ylabel('Score')
    
    # Add more plots as needed...
    
    plt.suptitle('Quantum Embedding Analysis Dashboard', fontsize=16)
    
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()


# Interactive plotting functions (requires plotly)
def create_interactive_kernel_plot(K: np.ndarray, labels: Optional[np.ndarray] = None) -> Any:
    """
    Create interactive kernel matrix plot using Plotly.
    
    Parameters
    ----------
    K : array-like
        Kernel matrix
    labels : array-like, optional
        Sample labels
        
    Returns
    -------
    fig : plotly figure
        Interactive plot figure
    """
    try:
        import plotly.graph_objects as go
        import plotly.express as px
        
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=K,
            colorscale='Viridis',
            showscale=True,
            hovertemplate='Sample %{x} vs Sample %{y}<br>Kernel Value: %{z:.3f}<extra></extra>'
        ))
        
        fig.update_layout(
            title='Interactive Quantum Kernel Matrix',
            xaxis_title='Sample Index',
            yaxis_title='Sample Index',
            width=600,
            height=600
        )
        
        return fig
        
    except ImportError:
        warnings.warn("Plotly not available, returning None")
        return None
