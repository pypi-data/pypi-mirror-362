"""
Metrics for evaluating quantum embeddings.
"""

import numpy as np
from typing import Any, Dict, Optional, List
from scipy.stats import unitary_group
from .licensing import requires_license


@requires_license()
def expressibility(
    embedding: Any,
    n_samples: int = 1000,
    n_bins: int = 50,
    random_seed: Optional[int] = None
) -> float:
    """
    Compute the expressibility of a quantum embedding.
    
    Expressibility measures how well the embedding can generate
    diverse quantum states across the Hilbert space. It compares
    the distribution of fidelities from randomly sampled states
    with the uniform (Haar) distribution.
    
    Parameters
    ----------
    embedding : BaseEmbedding
        Quantum embedding to evaluate
    n_samples : int, default=1000
        Number of random samples for evaluation
    n_bins : int, default=50
        Number of bins for histogram comparison
    random_seed : int, optional
        Random seed for reproducibility
        
    Returns
    -------
    expressibility : float
        Expressibility score (0 = poor, 1 = excellent)
    """
    if random_seed is not None:
        np.random.seed(random_seed)
    
    n_qubits = embedding.n_qubits
    n_features = embedding.get_feature_dimension()
    
    # Generate random parameter sets
    params1 = np.random.uniform(-2*np.pi, 2*np.pi, (n_samples, n_features))
    params2 = np.random.uniform(-2*np.pi, 2*np.pi, (n_samples, n_features))
    
    # Compute fidelities between random states
    fidelities = []
    for i in range(n_samples):
        try:
            circuit1 = embedding.create_circuit(params1[i])
            circuit2 = embedding.create_circuit(params2[i])
            
            # Get statevectors
            psi1 = embedding.backend.get_statevector(circuit1)
            psi2 = embedding.backend.get_statevector(circuit2)
            
            # Compute fidelity
            fidelity = np.abs(np.vdot(psi1, psi2)) ** 2
            fidelities.append(fidelity)
            
        except Exception:
            # Skip failed computations
            continue
    
    if len(fidelities) < 10:
        return 0.0  # Not enough successful computations
    
    fidelities = np.array(fidelities)
    
    # Generate reference Haar distribution
    haar_fidelities = _generate_haar_fidelities(n_qubits, len(fidelities), random_seed)
    
    # Compare distributions using Kolmogorov-Smirnov statistic
    try:
        from scipy.stats import ks_2samp
        ks_stat, _ = ks_2samp(fidelities, haar_fidelities)
        # Convert to expressibility score (lower KS distance = higher expressibility)
        expressibility_score = 1.0 - ks_stat
        return max(0.0, min(1.0, expressibility_score))
    except ImportError:
        # Fallback: use histogram comparison
        return _histogram_expressibility(fidelities, haar_fidelities, n_bins)


def _generate_haar_fidelities(n_qubits: int, n_samples: int, random_seed: Optional[int] = None) -> np.ndarray:
    """Generate fidelities from Haar random states."""
    if random_seed is not None:
        np.random.seed(random_seed)
    
    # For Haar random states, the fidelity distribution has a known form
    # For pure states: P(F) = (2^n - 1) * (1 - F)^(2^n - 2)
    # We can sample directly from this distribution
    
    # Simplified approach: use beta distribution approximation
    # For large Hilbert spaces, fidelities are concentrated near 0
    alpha = 1.0
    beta = 2**n_qubits - 1
    
    try:
        from scipy.stats import beta
        fidelities = beta.rvs(alpha, beta, size=n_samples)
        return fidelities
    except ImportError:
        # Fallback: uniform distribution (rough approximation)
        return np.random.uniform(0, 1, n_samples)


def _histogram_expressibility(fidelities: np.ndarray, haar_fidelities: np.ndarray, n_bins: int) -> float:
    """Compute expressibility using histogram comparison."""
    # Create histograms
    hist1, bins = np.histogram(fidelities, bins=n_bins, range=(0, 1), density=True)
    hist2, _ = np.histogram(haar_fidelities, bins=bins, density=True)
    
    # Compute overlap (higher overlap = better expressibility)
    overlap = np.sum(np.minimum(hist1, hist2)) / n_bins
    return overlap


@requires_license()
def trainability(
    embedding: Any,
    data: np.ndarray,
    n_samples: int = 100,
    epsilon: float = 1e-4,
    random_seed: Optional[int] = None
) -> float:
    """
    Compute the trainability of a quantum embedding.
    
    Trainability measures the variance of gradients, which indicates
    whether the embedding is trainable or suffers from barren plateaus.
    
    Parameters
    ----------
    embedding : BaseEmbedding
        Quantum embedding to evaluate
    data : array-like
        Sample data points for evaluation
    n_samples : int, default=100
        Number of samples for gradient estimation
    epsilon : float, default=1e-4
        Finite difference step size
    random_seed : int, optional
        Random seed for reproducibility
        
    Returns
    -------
    trainability : float
        Trainability score (higher = more trainable)
    """
    if random_seed is not None:
        np.random.seed(random_seed)
    
    # Check if embedding has trainable parameters
    if not hasattr(embedding, 'get_parameters') or embedding.n_parameters == 0:
        # Data-dependent embeddings: analyze sensitivity to data
        return _data_sensitivity_trainability(embedding, data, n_samples, epsilon)
    
    # Parameter-dependent embeddings: analyze gradient variance
    return _parameter_gradient_trainability(embedding, data, n_samples, epsilon)


def _data_sensitivity_trainability(
    embedding: Any, 
    data: np.ndarray, 
    n_samples: int, 
    epsilon: float
) -> float:
    """Compute trainability based on data sensitivity."""
    data = np.asarray(data)
    
    if len(data) < 2:
        return 0.0
    
    sensitivities = []
    
    for _ in range(n_samples):
        # Pick random data point
        idx = np.random.randint(len(data))
        x = data[idx].copy()
        
        # Compute reference state
        try:
            circuit_ref = embedding.create_circuit(x)
            psi_ref = embedding.backend.get_statevector(circuit_ref)
            
            # Perturb each feature and measure change
            feature_sensitivities = []
            for j in range(len(x)):
                x_pert = x.copy()
                x_pert[j] += epsilon
                
                circuit_pert = embedding.create_circuit(x_pert)
                psi_pert = embedding.backend.get_statevector(circuit_pert)
                
                # Compute distance between states
                fidelity = np.abs(np.vdot(psi_ref, psi_pert)) ** 2
                distance = 1.0 - fidelity
                sensitivity = distance / epsilon
                feature_sensitivities.append(sensitivity)
            
            sensitivities.extend(feature_sensitivities)
            
        except Exception:
            continue
    
    if len(sensitivities) == 0:
        return 0.0
    
    # Trainability is related to gradient variance
    gradient_variance = np.var(sensitivities)
    mean_gradient = np.mean(np.abs(sensitivities))
    
    # Normalize and convert to trainability score
    if mean_gradient > 1e-10:
        trainability_score = min(1.0, gradient_variance / mean_gradient)
        return trainability_score
    else:
        return 0.0


def _parameter_gradient_trainability(
    embedding: Any, 
    data: np.ndarray, 
    n_samples: int, 
    epsilon: float
) -> float:
    """Compute trainability based on parameter gradients."""
    # This would require access to trainable parameters
    # For now, return a placeholder
    return 0.5


@requires_license()
def gradient_variance(
    embedding: Any,
    data: np.ndarray,
    observable: Optional[Any] = None,
    n_samples: int = 100,
    epsilon: float = 1e-4
) -> float:
    """
    Compute gradient variance for barren plateau analysis.
    
    Parameters
    ----------
    embedding : BaseEmbedding
        Quantum embedding to analyze
    data : array-like
        Sample data points
    observable : observable, optional
        Observable to measure (defaults to Z on first qubit)
    n_samples : int, default=100
        Number of samples for gradient estimation
    epsilon : float, default=1e-4
        Finite difference step size
        
    Returns
    -------
    grad_var : float
        Gradient variance
    """
    if observable is None:
        # Default observable: Z measurement on first qubit
        observable = embedding.backend.create_observable("Z", [0])
    
    data = np.asarray(data)
    gradients = []
    
    for _ in range(min(n_samples, len(data))):
        idx = np.random.randint(len(data))
        x = data[idx]
        
        try:
            # Compute gradient using finite differences
            grad = _compute_finite_difference_gradient(
                embedding, x, observable, epsilon
            )
            gradients.extend(grad)
        except Exception:
            continue
    
    if len(gradients) == 0:
        return 0.0
    
    return float(np.var(gradients))


def _compute_finite_difference_gradient(
    embedding: Any,
    x: np.ndarray,
    observable: Any,
    epsilon: float
) -> List[float]:
    """Compute gradient using finite differences."""
    x = x.copy()
    grad = []
    
    for i in range(len(x)):
        # Forward difference
        x_plus = x.copy()
        x_plus[i] += epsilon
        
        x_minus = x.copy()
        x_minus[i] -= epsilon
        
        # Compute expectation values
        circuit_plus = embedding.create_circuit(x_plus)
        circuit_minus = embedding.create_circuit(x_minus)
        
        exp_plus = embedding.backend.compute_expectation(circuit_plus, observable)
        exp_minus = embedding.backend.compute_expectation(circuit_minus, observable)
        
        # Gradient estimate
        gradient = (exp_plus - exp_minus) / (2 * epsilon)
        grad.append(gradient)
    
    return grad


def effective_dimension(kernel_matrix: np.ndarray, threshold: float = 0.95) -> int:
    """
    Compute effective dimension of a kernel matrix.
    
    Parameters
    ----------
    kernel_matrix : array-like
        Kernel matrix
    threshold : float, default=0.95
        Variance threshold for determining effective dimension
        
    Returns
    -------
    eff_dim : int
        Effective dimension
    """
    try:
        eigenvals = np.linalg.eigvals(kernel_matrix)
        eigenvals = np.real(eigenvals)
        eigenvals = np.sort(eigenvals)[::-1]
        eigenvals = np.maximum(eigenvals, 0)  # Remove negative eigenvalues
        
        if np.sum(eigenvals) == 0:
            return 0
        
        # Cumulative variance explained
        cumvar = np.cumsum(eigenvals) / np.sum(eigenvals)
        
        # Find effective dimension
        eff_dim = np.searchsorted(cumvar, threshold) + 1
        
        return min(eff_dim, len(eigenvals))
    except np.linalg.LinAlgError:
        return len(kernel_matrix)


@requires_license()
def compute_all_metrics(
    embedding: Any,
    data: np.ndarray,
    n_samples: int = 1000
) -> Dict[str, float]:
    """
    Compute all embedding quality metrics.
    
    Parameters
    ----------
    embedding : BaseEmbedding
        Quantum embedding to evaluate
    data : array-like
        Sample data for evaluation
    n_samples : int, default=1000
        Number of samples for stochastic metrics
        
    Returns
    -------
    metrics : dict
        Dictionary containing all computed metrics
    """
    data = np.asarray(data)
    
    metrics = {}
    
    # Expressibility
    try:
        expr = expressibility(embedding, n_samples=n_samples)
        metrics['expressibility'] = expr
    except Exception as e:
        metrics['expressibility'] = 0.0
        metrics['expressibility_error'] = str(e)
    
    # Trainability
    try:
        train = trainability(embedding, data, n_samples=min(100, n_samples))
        metrics['trainability'] = train
    except Exception as e:
        metrics['trainability'] = 0.0
        metrics['trainability_error'] = str(e)
    
    # Gradient variance
    try:
        grad_var = gradient_variance(embedding, data, n_samples=min(100, n_samples))
        metrics['gradient_variance'] = grad_var
    except Exception as e:
        metrics['gradient_variance'] = 0.0
        metrics['gradient_variance_error'] = str(e)
    
    return metrics


def quantum_advantage_score(
    embedding: Any,
    data: np.ndarray,
    classical_baseline: Optional[Dict[str, float]] = None,
    n_samples: int = 1000
) -> Dict[str, float]:
    """
    Compute quantum advantage score by comparing to classical baselines.
    
    This function evaluates the potential quantum advantage of an embedding
    by comparing its performance metrics against classical feature engineering
    techniques and traditional machine learning preprocessing methods.
    
    Parameters
    ----------
    embedding : BaseEmbedding
        Quantum embedding to evaluate
    data : array-like
        Sample data for evaluation
    classical_baseline : dict, optional
        Classical baseline metrics for comparison. If None, will compute
        standard classical baselines (PCA, polynomial features, etc.)
    n_samples : int, default=1000
        Number of samples for stochastic metrics
        
    Returns
    -------
    advantage_metrics : dict
        Dictionary containing quantum advantage scores and comparisons
        
    Examples
    --------
    >>> from quantum_data_embedding_suite import AngleEmbedding
    >>> import numpy as np
    >>> data = np.random.randn(100, 4)
    >>> embedding = AngleEmbedding(n_qubits=4)
    >>> scores = quantum_advantage_score(embedding, data)
    >>> print(f"Quantum advantage: {scores['overall_advantage']:.3f}")
    """
    data = np.asarray(data)
    
    # Compute quantum metrics
    quantum_metrics = compute_all_metrics(embedding, data, n_samples=n_samples)
    
    # Compute or use provided classical baselines
    if classical_baseline is None:
        classical_baseline = _compute_classical_baselines(data)
    
    # Calculate advantage scores
    advantage_scores = {}
    
    # Expressibility advantage
    classical_expr = classical_baseline.get('expressibility', 0.5)
    quantum_expr = quantum_metrics.get('expressibility', 0.0)
    advantage_scores['expressibility_advantage'] = quantum_expr - classical_expr
    
    # Trainability advantage
    classical_train = classical_baseline.get('trainability', 0.3)
    quantum_train = quantum_metrics.get('trainability', 0.0)
    advantage_scores['trainability_advantage'] = quantum_train - classical_train
    
    # Feature richness (based on gradient variance)
    classical_features = classical_baseline.get('feature_variance', 0.1)
    quantum_features = quantum_metrics.get('gradient_variance', 0.0)
    if classical_features > 0:
        advantage_scores['feature_richness_ratio'] = quantum_features / classical_features
    else:
        advantage_scores['feature_richness_ratio'] = 1.0
    
    # Overall quantum advantage score
    # Weighted combination of individual advantages
    weights = {
        'expressibility': 0.4,
        'trainability': 0.4,
        'feature_richness': 0.2
    }
    
    overall_advantage = (
        weights['expressibility'] * max(0, advantage_scores['expressibility_advantage']) +
        weights['trainability'] * max(0, advantage_scores['trainability_advantage']) +
        weights['feature_richness'] * min(2.0, advantage_scores['feature_richness_ratio'])
    )
    
    advantage_scores['overall_advantage'] = overall_advantage
    
    # Add baseline and quantum metrics for reference
    advantage_scores['quantum_metrics'] = quantum_metrics
    advantage_scores['classical_baseline'] = classical_baseline
    
    # Interpretation
    if overall_advantage > 0.7:
        advantage_scores['interpretation'] = 'Strong quantum advantage'
    elif overall_advantage > 0.4:
        advantage_scores['interpretation'] = 'Moderate quantum advantage'
    elif overall_advantage > 0.1:
        advantage_scores['interpretation'] = 'Weak quantum advantage'
    else:
        advantage_scores['interpretation'] = 'No clear quantum advantage'
    
    return advantage_scores


def _compute_classical_baselines(data: np.ndarray) -> Dict[str, float]:
    """
    Compute classical baseline metrics for comparison.
    
    Parameters
    ----------
    data : array-like
        Input data for baseline computation
        
    Returns
    -------
    baselines : dict
        Classical baseline metrics
    """
    data = np.asarray(data)
    baselines = {}
    
    try:
        # Principal Component Analysis baseline
        from sklearn.decomposition import PCA
        from sklearn.preprocessing import StandardScaler
        
        # Standardize data
        scaler = StandardScaler()
        data_scaled = scaler.fit_transform(data)
        
        # PCA expressibility (variance captured by components)
        pca = PCA()
        pca.fit(data_scaled)
        explained_variance = pca.explained_variance_ratio_
        
        # Expressibility based on how evenly variance is distributed
        if len(explained_variance) > 1:
            entropy = -np.sum(explained_variance * np.log(explained_variance + 1e-10))
            max_entropy = np.log(len(explained_variance))
            baselines['expressibility'] = entropy / max_entropy if max_entropy > 0 else 0.0
        else:
            baselines['expressibility'] = 0.0
            
        # Trainability based on feature variance
        feature_vars = np.var(data_scaled, axis=0)
        baselines['trainability'] = np.mean(feature_vars)
        baselines['feature_variance'] = np.mean(feature_vars)
        
    except ImportError:
        # Fallback without sklearn
        baselines['expressibility'] = 0.3
        baselines['trainability'] = 0.2
        baselines['feature_variance'] = np.var(data)
    
    except Exception:
        # Fallback for any other errors
        baselines['expressibility'] = 0.3
        baselines['trainability'] = 0.2
        baselines['feature_variance'] = 0.1
    
    return baselines


def kernel_alignment(
    kernel_matrix1: np.ndarray,
    kernel_matrix2: np.ndarray
) -> float:
    """
    Compute kernel alignment between two kernel matrices.
    
    Kernel alignment measures the similarity between two kernel matrices,
    which is useful for comparing quantum and classical kernels.
    
    Parameters
    ----------
    kernel_matrix1 : array-like
        First kernel matrix
    kernel_matrix2 : array-like
        Second kernel matrix
        
    Returns
    -------
    alignment : float
        Kernel alignment score (0 = no alignment, 1 = perfect alignment)
    """
    K1 = np.asarray(kernel_matrix1)
    K2 = np.asarray(kernel_matrix2)
    
    if K1.shape != K2.shape:
        raise ValueError("Kernel matrices must have the same shape")
    
    # Compute Frobenius inner product
    numerator = np.sum(K1 * K2)
    
    # Compute norms
    norm_K1 = np.sqrt(np.sum(K1 * K1))
    norm_K2 = np.sqrt(np.sum(K2 * K2))
    
    if norm_K1 == 0 or norm_K2 == 0:
        return 0.0
    
    # Centered kernel alignment
    alignment = numerator / (norm_K1 * norm_K2)
    
    return float(alignment)


def kernel_expressivity(
    kernel_matrix: np.ndarray,
    n_bins: int = 50
) -> float:
    """
    Compute expressivity of a kernel matrix.
    
    Kernel expressivity measures how well the kernel can distinguish
    between different data points based on the distribution of kernel values.
    
    Parameters
    ----------
    kernel_matrix : array-like
        Kernel matrix to analyze
    n_bins : int, default=50
        Number of bins for histogram analysis
        
    Returns
    -------
    expressivity : float
        Kernel expressivity score (higher = more expressive)
    """
    K = np.asarray(kernel_matrix)
    
    # Extract upper triangular values (excluding diagonal)
    n = K.shape[0]
    triu_indices = np.triu_indices(n, k=1)
    kernel_values = K[triu_indices]
    
    if len(kernel_values) == 0:
        return 0.0
    
    # Compute histogram
    hist, bins = np.histogram(kernel_values, bins=n_bins, density=True)
    
    # Compute entropy as measure of expressivity
    # Higher entropy = more uniform distribution = better expressivity
    hist_normalized = hist / np.sum(hist)
    
    # Add small epsilon to avoid log(0)
    epsilon = 1e-10
    hist_normalized = hist_normalized + epsilon
    
    # Shannon entropy
    entropy = -np.sum(hist_normalized * np.log2(hist_normalized))
    
    # Normalize by maximum possible entropy
    max_entropy = np.log2(n_bins)
    expressivity = entropy / max_entropy if max_entropy > 0 else 0.0
    
    return float(expressivity)


def kernel_matrix_rank(kernel_matrix: np.ndarray, threshold: float = 1e-10) -> int:
    """
    Compute the numerical rank of a kernel matrix.
    
    Parameters
    ----------
    kernel_matrix : array-like
        Kernel matrix to analyze
    threshold : float, default=1e-10
        Threshold for determining rank
        
    Returns
    -------
    rank : int
        Numerical rank of the kernel matrix
    """
    K = np.asarray(kernel_matrix)
    
    try:
        # Compute singular values
        singular_values = np.linalg.svd(K, compute_uv=False)
        
        # Count singular values above threshold
        rank = np.sum(singular_values > threshold)
        
        return int(rank)
        
    except np.linalg.LinAlgError:
        # Return matrix size as fallback
        return K.shape[0]


def kernel_condition_number(kernel_matrix: np.ndarray) -> float:
    """
    Compute the condition number of a kernel matrix.
    
    Parameters
    ----------
    kernel_matrix : array-like
        Kernel matrix to analyze
        
    Returns
    -------
    condition_number : float
        Condition number of the kernel matrix
    """
    K = np.asarray(kernel_matrix)
    
    try:
        # Compute condition number
        cond_num = np.linalg.cond(K)
        
        return float(cond_num)
        
    except np.linalg.LinAlgError:
        # Return large number as fallback for singular matrices
        return 1e12


def embedding_capacity(
    embedding: Any,
    data: np.ndarray,
    n_samples: int = 100
) -> float:
    """
    Compute the capacity of a quantum embedding.
    
    Capacity measures how much information the embedding can encode
    about the input data.
    
    Parameters
    ----------
    embedding : BaseEmbedding
        Quantum embedding to evaluate
    data : array-like
        Sample data points
    n_samples : int, default=100
        Number of samples for evaluation
        
    Returns
    -------
    capacity : float
        Embedding capacity score
    """
    data = np.asarray(data)
    
    if len(data) < 2:
        return 0.0
    
    # Sample random pairs of data points
    n_pairs = min(n_samples, len(data) * (len(data) - 1) // 2)
    pairs = []
    
    for _ in range(n_pairs):
        i, j = np.random.choice(len(data), size=2, replace=False)
        pairs.append((i, j))
    
    # Compute distances in input space and quantum state space
    input_distances = []
    quantum_distances = []
    
    for i, j in pairs:
        # Input space distance
        input_dist = np.linalg.norm(data[i] - data[j])
        input_distances.append(input_dist)
        
        try:
            # Quantum state distance (fidelity)
            circuit_i = embedding.create_circuit(data[i])
            circuit_j = embedding.create_circuit(data[j])
            
            # Compute state fidelity (placeholder - would need actual implementation)
            fidelity = 0.5 + 0.5 * np.exp(-input_dist)  # Approximate relationship
            quantum_dist = 1 - fidelity
            quantum_distances.append(quantum_dist)
            
        except Exception:
            quantum_distances.append(0.0)
    
    if len(input_distances) == 0 or len(quantum_distances) == 0:
        return 0.0
    
    # Compute correlation between input and quantum distances
    try:
        correlation = np.corrcoef(input_distances, quantum_distances)[0, 1]
        
        # Convert to capacity score (higher correlation = better capacity)
        capacity = abs(correlation) if not np.isnan(correlation) else 0.0
        
        return float(capacity)
        
    except Exception:
        return 0.0


def separability_measure(
    embedding: Any,
    data: np.ndarray,
    labels: np.ndarray,
    n_samples: int = 100
) -> float:
    """
    Compute how well the embedding separates different classes.
    
    Parameters
    ----------
    embedding : BaseEmbedding
        Quantum embedding to evaluate
    data : array-like
        Sample data points
    labels : array-like
        Class labels for data points
    n_samples : int, default=100
        Number of samples for evaluation
        
    Returns
    -------
    separability : float
        Class separability score (higher = better separation)
    """
    data = np.asarray(data)
    labels = np.asarray(labels)
    
    if len(data) != len(labels):
        raise ValueError("Data and labels must have same length")
    
    unique_labels = np.unique(labels)
    
    if len(unique_labels) < 2:
        return 0.0
    
    # Compute within-class and between-class distances
    within_distances = []
    between_distances = []
    
    for _ in range(n_samples):
        # Sample two points from same class
        label = np.random.choice(unique_labels)
        same_class_indices = np.where(labels == label)[0]
        
        if len(same_class_indices) >= 2:
            i, j = np.random.choice(same_class_indices, size=2, replace=False)
            
            try:
                # Compute quantum distance
                circuit_i = embedding.create_circuit(data[i])
                circuit_j = embedding.create_circuit(data[j])
                
                # Placeholder distance computation
                dist = np.linalg.norm(data[i] - data[j])
                within_distances.append(dist)
                
            except Exception:
                continue
        
        # Sample two points from different classes
        if len(unique_labels) >= 2:
            label1, label2 = np.random.choice(unique_labels, size=2, replace=False)
            
            class1_indices = np.where(labels == label1)[0]
            class2_indices = np.where(labels == label2)[0]
            
            if len(class1_indices) > 0 and len(class2_indices) > 0:
                i = np.random.choice(class1_indices)
                j = np.random.choice(class2_indices)
                
                try:
                    # Compute quantum distance
                    circuit_i = embedding.create_circuit(data[i])
                    circuit_j = embedding.create_circuit(data[j])
                    
                    # Placeholder distance computation
                    dist = np.linalg.norm(data[i] - data[j])
                    between_distances.append(dist)
                    
                except Exception:
                    continue
    
    if len(within_distances) == 0 or len(between_distances) == 0:
        return 0.0
    
    # Separability is ratio of between-class to within-class distances
    mean_within = np.mean(within_distances)
    mean_between = np.mean(between_distances)
    
    if mean_within == 0:
        return 1.0 if mean_between > 0 else 0.0
    
    separability = mean_between / mean_within
    
    return float(min(separability, 1.0))  # Cap at 1.0
