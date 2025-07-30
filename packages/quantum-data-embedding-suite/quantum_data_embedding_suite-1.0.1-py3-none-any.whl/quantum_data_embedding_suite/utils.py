"""
Utility functions for quantum data embedding.
"""

import numpy as np
from typing import Tuple, Optional, Union
from sklearn.preprocessing import StandardScaler, MinMaxScaler


def validate_data(X: np.ndarray, n_qubits: int) -> np.ndarray:
    """
    Validate and preprocess data for quantum embedding.
    
    Parameters
    ----------
    X : array-like
        Input data
    n_qubits : int
        Number of qubits available
        
    Returns
    -------
    X : ndarray
        Validated and potentially reshaped data
    """
    X = np.asarray(X, dtype=np.float64)
    
    if X.ndim == 1:
        X = X.reshape(1, -1)
    elif X.ndim != 2:
        raise ValueError(f"Data must be 1D or 2D array, got {X.ndim}D")
    
    # Basic validation
    if np.any(~np.isfinite(X)):
        raise ValueError("Data contains NaN or infinite values")
    
    return X


def normalize_data(
    X: np.ndarray, 
    method: str = "minmax", 
    feature_range: Tuple[float, float] = (0, 2*np.pi)
) -> np.ndarray:
    """
    Normalize data for quantum embedding.
    
    Parameters
    ----------
    X : array-like
        Input data
    method : str, default='minmax'
        Normalization method ('minmax', 'standard', 'unit')
    feature_range : tuple, default=(0, 2*pi)
        Target range for minmax scaling
        
    Returns
    -------
    X_normalized : ndarray
        Normalized data
    """
    X = np.asarray(X, dtype=np.float64)
    
    if method == "minmax":
        scaler = MinMaxScaler(feature_range=feature_range)
        return scaler.fit_transform(X)
    elif method == "standard":
        scaler = StandardScaler()
        return scaler.fit_transform(X)
    elif method == "unit":
        # Normalize each sample to unit norm
        norms = np.linalg.norm(X, axis=1, keepdims=True)
        norms = np.where(norms == 0, 1, norms)  # Avoid division by zero
        return X / norms
    else:
        raise ValueError(f"Unknown normalization method: {method}")


def pad_features(X: np.ndarray, target_features: int) -> np.ndarray:
    """
    Pad features to match target dimension.
    
    Parameters
    ----------
    X : array-like
        Input data
    target_features : int
        Target number of features
        
    Returns
    -------
    X_padded : ndarray
        Data padded to target dimension
    """
    X = np.asarray(X)
    
    if X.shape[1] >= target_features:
        return X[:, :target_features]
    
    # Pad with zeros
    n_samples = X.shape[0]
    n_pad = target_features - X.shape[1]
    padding = np.zeros((n_samples, n_pad))
    
    return np.hstack([X, padding])


def reduce_features(
    X: np.ndarray, 
    target_features: int, 
    method: str = "pca"
) -> np.ndarray:
    """
    Reduce feature dimension using classical methods.
    
    Parameters
    ----------
    X : array-like
        Input data
    target_features : int
        Target number of features
    method : str, default='pca'
        Reduction method ('pca', 'truncate', 'average')
        
    Returns
    -------
    X_reduced : ndarray
        Data with reduced features
    """
    X = np.asarray(X)
    
    if X.shape[1] <= target_features:
        return X
    
    if method == "pca":
        from sklearn.decomposition import PCA
        pca = PCA(n_components=target_features)
        return pca.fit_transform(X)
    elif method == "truncate":
        return X[:, :target_features]
    elif method == "average":
        # Average neighboring features
        n_groups = target_features
        group_size = X.shape[1] // n_groups
        
        X_reduced = np.zeros((X.shape[0], n_groups))
        for i in range(n_groups):
            start_idx = i * group_size
            end_idx = (i + 1) * group_size if i < n_groups - 1 else X.shape[1]
            X_reduced[:, i] = np.mean(X[:, start_idx:end_idx], axis=1)
        
        return X_reduced
    else:
        raise ValueError(f"Unknown reduction method: {method}")


def generate_random_data(
    n_samples: int, 
    n_features: int, 
    data_type: str = "gaussian",
    seed: Optional[int] = None
) -> np.ndarray:
    """
    Generate random data for testing.
    
    Parameters
    ----------
    n_samples : int
        Number of samples
    n_features : int
        Number of features
    data_type : str, default='gaussian'
        Type of random data ('gaussian', 'uniform', 'sphere')
    seed : int, optional
        Random seed for reproducibility
        
    Returns
    -------
    X : ndarray
        Random data
    """
    if seed is not None:
        np.random.seed(seed)
    
    if data_type == "gaussian":
        return np.random.normal(0, 1, (n_samples, n_features))
    elif data_type == "uniform":
        return np.random.uniform(-1, 1, (n_samples, n_features))
    elif data_type == "sphere":
        # Points on unit hypersphere
        X = np.random.normal(0, 1, (n_samples, n_features))
        norms = np.linalg.norm(X, axis=1, keepdims=True)
        return X / norms
    else:
        raise ValueError(f"Unknown data type: {data_type}")


def compute_pairwise_distances(X: np.ndarray) -> np.ndarray:
    """
    Compute pairwise Euclidean distances.
    
    Parameters
    ----------
    X : array-like
        Input data
        
    Returns
    -------
    distances : ndarray
        Pairwise distance matrix
    """
    from sklearn.metrics.pairwise import euclidean_distances
    return euclidean_distances(X)


def compute_data_statistics(X: np.ndarray) -> dict:
    """
    Compute basic statistics of the data.
    
    Parameters
    ----------
    X : array-like
        Input data
        
    Returns
    -------
    stats : dict
        Dictionary containing data statistics
    """
    X = np.asarray(X)
    
    stats = {
        'shape': X.shape,
        'mean': np.mean(X, axis=0),
        'std': np.std(X, axis=0),
        'min': np.min(X, axis=0),
        'max': np.max(X, axis=0),
        'median': np.median(X, axis=0),
        'range': np.ptp(X, axis=0),  # peak-to-peak (max - min)
    }
    
    # Global statistics
    stats.update({
        'global_mean': np.mean(X),
        'global_std': np.std(X),
        'global_min': np.min(X),
        'global_max': np.max(X),
        'condition_number': np.linalg.cond(X @ X.T) if X.shape[0] <= X.shape[1] else np.linalg.cond(X.T @ X),
    })
    
    return stats


def estimate_optimal_qubits(X: np.ndarray, embedding_type: str = "angle") -> int:
    """
    Estimate optimal number of qubits for data.
    
    Parameters
    ----------
    X : array-like
        Input data
    embedding_type : str, default='angle'
        Type of embedding
        
    Returns
    -------
    n_qubits : int
        Recommended number of qubits
    """
    X = np.asarray(X)
    n_features = X.shape[1]
    
    if embedding_type == "angle":
        # For angle embedding, typically 1 feature per qubit
        return min(n_features, 10)  # Cap at 10 qubits for practicality
    elif embedding_type == "amplitude":
        # For amplitude embedding, need 2^n_qubits >= n_features
        return max(1, int(np.ceil(np.log2(n_features))))
    elif embedding_type in ["iqp", "data_reuploading"]:
        # These can be more flexible
        return min(max(2, n_features // 2), 8)
    else:
        # Default heuristic
        return min(max(2, n_features), 6)


def check_quantum_advantage_potential(X: np.ndarray, y: np.ndarray = None) -> dict:
    """
    Assess potential for quantum advantage on given data.
    
    Parameters
    ----------
    X : array-like
        Input features
    y : array-like, optional
        Target labels
        
    Returns
    -------
    assessment : dict
        Dictionary containing quantum advantage potential assessment
    """
    X = np.asarray(X)
    n_samples, n_features = X.shape
    
    assessment = {
        'data_size': 'small' if n_samples < 100 else 'medium' if n_samples < 1000 else 'large',
        'feature_dimension': 'low' if n_features < 5 else 'medium' if n_features < 20 else 'high',
        'recommended_qubits': estimate_optimal_qubits(X),
    }
    
    # Assess data complexity
    try:
        from sklearn.decomposition import PCA
        pca = PCA()
        pca.fit(X)
        
        # Intrinsic dimensionality
        explained_var_ratio = pca.explained_variance_ratio_
        intrinsic_dim = np.sum(np.cumsum(explained_var_ratio) < 0.95) + 1
        assessment['intrinsic_dimension'] = intrinsic_dim
        
        # Data spread
        assessment['data_spread'] = 'concentrated' if np.sum(explained_var_ratio[:2]) > 0.9 else 'distributed'
        
    except Exception:
        assessment['intrinsic_dimension'] = n_features
        assessment['data_spread'] = 'unknown'
    
    # If labels are provided, assess separability
    if y is not None:
        y = np.asarray(y)
        n_classes = len(np.unique(y))
        assessment['n_classes'] = n_classes
        assessment['classification_complexity'] = 'binary' if n_classes == 2 else 'multiclass'
        
        # Simple separability check
        try:
            from sklearn.linear_model import LogisticRegression
            from sklearn.model_selection import cross_val_score
            
            lr = LogisticRegression(max_iter=1000)
            scores = cross_val_score(lr, X, y, cv=min(5, n_samples // 10))
            linear_accuracy = np.mean(scores)
            
            assessment['linear_separability'] = 'high' if linear_accuracy > 0.9 else 'medium' if linear_accuracy > 0.7 else 'low'
            assessment['quantum_advantage_potential'] = 'high' if linear_accuracy < 0.8 else 'medium' if linear_accuracy < 0.9 else 'low'
            
        except Exception:
            assessment['linear_separability'] = 'unknown'
            assessment['quantum_advantage_potential'] = 'unknown'
    
    return assessment
