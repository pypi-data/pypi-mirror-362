# Kernels API

This page documents the quantum kernel classes and functions.

## Base Classes

### BaseKernel

::: quantum_data_embedding_suite.kernels.BaseKernel
    options:
      show_source: true
      show_root_heading: true
      show_object_full_path: false

## Kernel Implementations

### FidelityKernel

::: quantum_data_embedding_suite.kernels.FidelityKernel
    options:
      show_source: true
      show_root_heading: true
      show_object_full_path: false

### ProjectedKernel

::: quantum_data_embedding_suite.kernels.ProjectedKernel
    options:
      show_source: true
      show_root_heading: true
      show_object_full_path: false

### TrainableKernel

::: quantum_data_embedding_suite.kernels.TrainableKernel
    options:
      show_source: true
      show_root_heading: true
      show_object_full_path: false

## Usage Examples

### Basic Kernel Creation

```python
from quantum_data_embedding_suite.kernels import FidelityKernel
from quantum_data_embedding_suite.embeddings import AngleEmbedding
import numpy as np

# Create embedding and kernel
embedding = AngleEmbedding(n_qubits=4)
kernel = FidelityKernel(embedding, backend="qiskit")

# Compute kernel matrix
X = np.random.randn(50, 4)
K = kernel.compute_kernel(X)

print(f"Kernel matrix shape: {K.shape}")
print(f"Kernel is symmetric: {np.allclose(K, K.T)}")
print(f"Diagonal elements (should be ~1): {np.diag(K)[:5]}")
```

### Kernel Comparison

```python
from quantum_data_embedding_suite.kernels import (
    FidelityKernel, ProjectedKernel, TrainableKernel
)
from sklearn.metrics.pairwise import rbf_kernel

# Create different quantum kernels
embedding = AngleEmbedding(n_qubits=4)
kernels = {
    'fidelity': FidelityKernel(embedding),
    'projected': ProjectedKernel(embedding, n_measurements=100),
    'trainable': TrainableKernel(embedding, n_parameters=20)
}

# Compare with classical kernel
X = np.random.randn(30, 4)
K_classical = rbf_kernel(X)

results = {}
for name, kernel in kernels.items():
    K_quantum = kernel.compute_kernel(X)
    
    # Compute kernel alignment with classical kernel
    alignment = np.sum(K_quantum * K_classical) / (
        np.linalg.norm(K_quantum) * np.linalg.norm(K_classical)
    )
    
    results[name] = {
        'trace': np.trace(K_quantum),
        'frobenius_norm': np.linalg.norm(K_quantum),
        'classical_alignment': alignment
    }

for name, metrics in results.items():
    print(f"{name.upper()} Kernel:")
    for metric, value in metrics.items():
        print(f"  {metric}: {value:.4f}")
    print()
```

### Custom Kernel Creation

```python
from quantum_data_embedding_suite.kernels import BaseKernel

class CustomKernel(BaseKernel):
    """Custom kernel implementation"""
    
    def __init__(self, embedding, alpha=1.0, beta=0.5):
        super().__init__(embedding)
        self.alpha = alpha
        self.beta = beta
    
    def _compute_element(self, x_i, x_j):
        """Compute kernel element K(x_i, x_j)"""
        # Create quantum circuits
        circuit_i = self.embedding.embed(x_i)
        circuit_j = self.embedding.embed(x_j)
        
        # Compute fidelity
        fidelity = self._compute_fidelity(circuit_i, circuit_j)
        
        # Apply custom transformation
        kernel_value = self.alpha * fidelity**self.beta
        
        return kernel_value
    
    def _compute_fidelity(self, circuit_i, circuit_j):
        """Compute fidelity between two circuits"""
        # Implement fidelity computation
        # This is a simplified version
        from quantum_data_embedding_suite.backends import QiskitBackend
        backend = QiskitBackend(device="statevector_simulator")
        
        state_i = backend.get_statevector(circuit_i)
        state_j = backend.get_statevector(circuit_j)
        
        fidelity = np.abs(np.vdot(state_i, state_j))**2
        return fidelity

# Use custom kernel
custom_kernel = CustomKernel(embedding, alpha=2.0, beta=0.8)
K_custom = custom_kernel.compute_kernel(X[:10])  # Small subset for testing
```

## Advanced Usage

### Trainable Kernels

```python
from quantum_data_embedding_suite.kernels import TrainableKernel
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split

# Create trainable kernel
trainable_kernel = TrainableKernel(
    embedding=embedding,
    n_parameters=15,
    optimization_method="adam",
    learning_rate=0.01
)

# Prepare data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# Train the kernel
print("Training kernel...")
trainable_kernel.fit(
    X_train, y_train, 
    epochs=50,
    validation_split=0.2,
    verbose=True
)

# Use trained kernel for classification
K_train = trainable_kernel.compute_kernel(X_train)
K_test = trainable_kernel.compute_kernel(X_test, X_train)

svm = SVC(kernel='precomputed')
svm.fit(K_train, y_train)

train_accuracy = svm.score(K_train, y_train)
test_accuracy = svm.score(K_test, y_test)

print(f"Training accuracy: {train_accuracy:.4f}")
print(f"Test accuracy: {test_accuracy:.4f}")
```

### Kernel Optimization

```python
from quantum_data_embedding_suite.optimization import optimize_kernel

# Define objective function
def objective_function(kernel, X, y):
    """Objective function for kernel optimization"""
    K = kernel.compute_kernel(X)
    
    # Use cross-validation accuracy as objective
    from sklearn.model_selection import cross_val_score
    svm = SVC(kernel='precomputed')
    scores = cross_val_score(svm, K, y, cv=5)
    
    return scores.mean()

# Optimize kernel parameters
best_kernel = optimize_kernel(
    kernel_class=TrainableKernel,
    embedding=embedding,
    X_train=X_train,
    y_train=y_train,
    objective_function=objective_function,
    n_trials=50,
    optimization_method="bayesian"
)

print("Optimal kernel parameters found")
```

### Batch Kernel Computation

```python
def compute_kernel_batch(kernel, X, batch_size=100):
    """Compute kernel matrix in batches to manage memory"""
    n_samples = len(X)
    K = np.zeros((n_samples, n_samples))
    
    for i in range(0, n_samples, batch_size):
        for j in range(0, n_samples, batch_size):
            i_end = min(i + batch_size, n_samples)
            j_end = min(j + batch_size, n_samples)
            
            X_batch_i = X[i:i_end]
            X_batch_j = X[j:j_end]
            
            K_batch = kernel.compute_kernel(X_batch_i, X_batch_j)
            K[i:i_end, j:j_end] = K_batch
            
            print(f"Computed batch ({i}:{i_end}, {j}:{j_end})")
    
    return K

# Use batch computation for large datasets
large_X = np.random.randn(1000, 4)
K_large = compute_kernel_batch(kernel, large_X, batch_size=200)
```

## Kernel Analysis

### Kernel Properties

```python
def analyze_kernel_properties(K):
    """Analyze properties of a kernel matrix"""
    n = K.shape[0]
    
    # Basic properties
    is_symmetric = np.allclose(K, K.T)
    is_psd = np.all(np.linalg.eigvals(K) >= -1e-10)
    
    # Eigenvalue analysis
    eigenvals = np.linalg.eigvals(K)
    eigenvals = np.real(eigenvals[eigenvals.argsort()[::-1]])
    
    # Effective rank
    eigenval_sum = np.sum(eigenvals)
    normalized_eigenvals = eigenvals / eigenval_sum
    effective_rank = 1.0 / np.sum(normalized_eigenvals**2)
    
    # Condition number
    condition_number = eigenvals[0] / eigenvals[-1] if eigenvals[-1] > 1e-12 else np.inf
    
    # Kernel alignment with identity
    identity_alignment = np.trace(K) / np.linalg.norm(K) / np.sqrt(n)
    
    return {
        'is_symmetric': is_symmetric,
        'is_positive_semidefinite': is_psd,
        'rank': np.linalg.matrix_rank(K),
        'effective_rank': effective_rank,
        'condition_number': condition_number,
        'trace': np.trace(K),
        'frobenius_norm': np.linalg.norm(K),
        'largest_eigenvalue': eigenvals[0],
        'smallest_eigenvalue': eigenvals[-1],
        'identity_alignment': identity_alignment,
        'eigenvalue_decay': eigenvals[:min(10, len(eigenvals))]
    }

# Analyze kernel
K = kernel.compute_kernel(X[:50])
properties = analyze_kernel_properties(K)

print("Kernel Properties:")
for prop, value in properties.items():
    if isinstance(value, np.ndarray):
        print(f"{prop}: {value}")
    elif isinstance(value, float):
        print(f"{prop}: {value:.6f}")
    else:
        print(f"{prop}: {value}")
```

### Kernel Visualization

```python
import matplotlib.pyplot as plt
import seaborn as sns

def visualize_kernel(K, labels=None, title="Kernel Matrix"):
    """Visualize kernel matrix"""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Kernel matrix heatmap
    sns.heatmap(K, ax=axes[0,0], cmap='viridis', cbar=True)
    axes[0,0].set_title(f"{title} - Heatmap")
    
    # Eigenvalue spectrum
    eigenvals = np.linalg.eigvals(K)
    eigenvals = np.real(eigenvals[eigenvals.argsort()[::-1]])
    axes[0,1].plot(eigenvals, 'o-')
    axes[0,1].set_title("Eigenvalue Spectrum")
    axes[0,1].set_xlabel("Index")
    axes[0,1].set_ylabel("Eigenvalue")
    axes[0,1].set_yscale('log')
    
    # Kernel values distribution
    K_upper = K[np.triu_indices_from(K, k=1)]
    axes[1,0].hist(K_upper, bins=30, alpha=0.7)
    axes[1,0].set_title("Off-diagonal Elements Distribution")
    axes[1,0].set_xlabel("Kernel Value")
    axes[1,0].set_ylabel("Frequency")
    
    # Diagonal elements
    diag_elements = np.diag(K)
    axes[1,1].hist(diag_elements, bins=20, alpha=0.7)
    axes[1,1].set_title("Diagonal Elements Distribution")
    axes[1,1].set_xlabel("Kernel Value")
    axes[1,1].set_ylabel("Frequency")
    
    plt.tight_layout()
    plt.show()

# Visualize kernel
visualize_kernel(K, title="Quantum Fidelity Kernel")
```

## Performance Optimization

### Parallel Kernel Computation

```python
from multiprocessing import Pool
import functools

def compute_kernel_parallel(kernel, X, n_jobs=4):
    """Compute kernel matrix using parallel processing"""
    n_samples = len(X)
    
    def compute_row(i):
        """Compute one row of the kernel matrix"""
        row = np.zeros(n_samples)
        for j in range(n_samples):
            if j <= i:  # Exploit symmetry
                row[j] = kernel._compute_element(X[i], X[j])
        return i, row
    
    # Compute upper triangle in parallel
    with Pool(n_jobs) as pool:
        results = pool.map(compute_row, range(n_samples))
    
    # Construct full matrix
    K = np.zeros((n_samples, n_samples))
    for i, row in results:
        K[i, :] = row
        
    # Fill lower triangle using symmetry
    K = K + K.T - np.diag(np.diag(K))
    
    return K

# Use parallel computation
K_parallel = compute_kernel_parallel(kernel, X[:20], n_jobs=2)
```

### Approximate Kernels

```python
class ApproximateKernel:
    """Approximate kernel using random sampling"""
    
    def __init__(self, base_kernel, n_samples=100):
        self.base_kernel = base_kernel
        self.n_samples = n_samples
    
    def compute_kernel(self, X, Y=None):
        """Compute approximate kernel using random sampling"""
        if Y is None:
            Y = X
            
        n_x, n_y = len(X), len(Y)
        
        # Sample random pairs for approximation
        n_total_pairs = n_x * n_y
        n_sample_pairs = min(self.n_samples, n_total_pairs)
        
        # Generate random indices
        i_indices = np.random.randint(0, n_x, n_sample_pairs)
        j_indices = np.random.randint(0, n_y, n_sample_pairs)
        
        # Compute sampled kernel values
        K_approx = np.zeros((n_x, n_y))
        sample_count = np.zeros((n_x, n_y))
        
        for i, j in zip(i_indices, j_indices):
            k_val = self.base_kernel._compute_element(X[i], Y[j])
            K_approx[i, j] += k_val
            sample_count[i, j] += 1
        
        # Average multiple samples
        K_approx = np.divide(K_approx, sample_count, 
                           out=np.zeros_like(K_approx), 
                           where=sample_count!=0)
        
        # Fill missing values with mean
        mean_val = np.mean(K_approx[K_approx > 0])
        K_approx[sample_count == 0] = mean_val
        
        return K_approx

# Use approximate kernel
approx_kernel = ApproximateKernel(kernel, n_samples=500)
K_approx = approx_kernel.compute_kernel(X[:100])
```

## Integration with Machine Learning

### Scikit-learn Integration

```python
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline

class QuantumKernelTransformer(BaseEstimator, TransformerMixin):
    """Scikit-learn transformer for quantum kernels"""
    
    def __init__(self, quantum_kernel):
        self.quantum_kernel = quantum_kernel
        
    def fit(self, X, y=None):
        """Fit the transformer"""
        self.X_train_ = X.copy()
        return self
    
    def transform(self, X):
        """Transform data to kernel space"""
        if not hasattr(self, 'X_train_'):
            raise ValueError("Transformer not fitted")
            
        # Compute kernel between X and training data
        K = self.quantum_kernel.compute_kernel(X, self.X_train_)
        return K
    
    def fit_transform(self, X, y=None):
        """Fit and transform"""
        self.fit(X, y)
        # For training data, compute full kernel matrix
        K = self.quantum_kernel.compute_kernel(X)
        return K

# Use in scikit-learn pipeline
pipeline = Pipeline([
    ('quantum_kernel', QuantumKernelTransformer(kernel)),
    ('svm', SVC(kernel='precomputed'))
])

# Train pipeline
pipeline.fit(X_train, y_train)

# Predict
predictions = pipeline.predict(X_test)
```

### Custom Kernel for SVM

```python
def create_sklearn_kernel(quantum_kernel):
    """Create sklearn-compatible kernel function"""
    
    def sklearn_kernel(X, Y=None):
        """Kernel function for sklearn"""
        if Y is None:
            # Training phase - compute full kernel matrix
            return quantum_kernel.compute_kernel(X)
        else:
            # Prediction phase - compute cross-kernel
            return quantum_kernel.compute_kernel(X, Y)
    
    return sklearn_kernel

# Use with sklearn SVM
from sklearn.svm import SVC

sklearn_kernel_func = create_sklearn_kernel(kernel)
svm = SVC(kernel=sklearn_kernel_func)

# Note: This approach has limitations with sklearn's kernel caching
# It's better to use precomputed kernels for quantum kernels
```

## Error Handling and Debugging

### Kernel Validation

```python
def validate_kernel(K, tolerance=1e-10):
    """Validate kernel matrix properties"""
    errors = []
    warnings = []
    
    # Check if matrix is square
    if K.shape[0] != K.shape[1]:
        errors.append("Kernel matrix is not square")
        return errors, warnings
    
    n = K.shape[0]
    
    # Check symmetry
    if not np.allclose(K, K.T, atol=tolerance):
        errors.append("Kernel matrix is not symmetric")
    
    # Check positive semidefiniteness
    eigenvals = np.linalg.eigvals(K)
    min_eigenval = np.min(np.real(eigenvals))
    if min_eigenval < -tolerance:
        errors.append(f"Kernel matrix is not PSD (min eigenvalue: {min_eigenval})")
    
    # Check diagonal elements
    diag_elements = np.diag(K)
    if np.any(diag_elements < 0):
        warnings.append("Some diagonal elements are negative")
    
    if np.any(diag_elements > 1 + tolerance):
        warnings.append("Some diagonal elements are > 1 (unusual for normalized kernels)")
    
    # Check for NaN or Inf values
    if np.any(np.isnan(K)):
        errors.append("Kernel matrix contains NaN values")
    
    if np.any(np.isinf(K)):
        errors.append("Kernel matrix contains infinite values")
    
    # Check condition number
    condition_num = np.linalg.cond(K)
    if condition_num > 1e12:
        warnings.append(f"Kernel matrix is ill-conditioned (cond={condition_num:.2e})")
    
    return errors, warnings

# Validate kernel matrix
errors, warnings = validate_kernel(K)

if errors:
    print("Kernel validation errors:")
    for error in errors:
        print(f"  - {error}")

if warnings:
    print("Kernel validation warnings:")
    for warning in warnings:
        print(f"  - {warning}")

if not errors and not warnings:
    print("Kernel matrix is valid")
```

### Debugging Tools

```python
def debug_kernel_computation(kernel, X, verbose=True):
    """Debug kernel computation step by step"""
    if verbose:
        print(f"Debugging kernel: {type(kernel).__name__}")
        print(f"Embedding: {type(kernel.embedding).__name__}")
        print(f"Data shape: {X.shape}")
    
    # Test single element computation
    try:
        if len(X) >= 2:
            k_val = kernel._compute_element(X[0], X[1])
            if verbose:
                print(f"Sample kernel value K(x_0, x_1): {k_val}")
        
        # Test diagonal element
        k_diag = kernel._compute_element(X[0], X[0])
        if verbose:
            print(f"Diagonal element K(x_0, x_0): {k_diag}")
            
        # Test small kernel matrix
        if len(X) >= 3:
            K_small = kernel.compute_kernel(X[:3])
            if verbose:
                print(f"Small kernel matrix (3x3):")
                print(K_small)
                
            # Validate small matrix
            errors, warnings = validate_kernel(K_small)
            if errors:
                print(f"Errors in small kernel: {errors}")
            if warnings:
                print(f"Warnings in small kernel: {warnings}")
                
    except Exception as e:
        print(f"Error during kernel computation: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

# Debug kernel
debug_success = debug_kernel_computation(kernel, X)
```

## Best Practices

### Kernel Selection Guidelines

```python
def recommend_kernel(data_characteristics, problem_type):
    """Recommend kernel based on data and problem characteristics"""
    
    n_samples, n_features = data_characteristics['n_samples'], data_characteristics['n_features']
    noise_level = data_characteristics.get('noise_level', 'medium')
    computational_budget = data_characteristics.get('computational_budget', 'medium')
    
    recommendations = []
    
    # Data size considerations
    if n_samples < 100:
        recommendations.append("Consider FidelityKernel for small datasets")
    elif n_samples > 1000:
        recommendations.append("Consider ProjectedKernel or approximate methods for large datasets")
    
    # Noise considerations
    if noise_level == 'high':
        recommendations.append("ProjectedKernel may be more robust to noise")
    else:
        recommendations.append("FidelityKernel provides better accuracy for low-noise data")
    
    # Computational budget
    if computational_budget == 'low':
        recommendations.append("Use ProjectedKernel with fewer measurements")
    elif computational_budget == 'high':
        recommendations.append("Consider TrainableKernel for optimal performance")
    
    # Problem type
    if problem_type == 'classification':
        recommendations.append("All kernel types suitable for classification")
    elif problem_type == 'regression':
        recommendations.append("FidelityKernel often works well for regression")
    
    return recommendations

# Get recommendations
data_chars = {
    'n_samples': 500,
    'n_features': 8,
    'noise_level': 'medium',
    'computational_budget': 'high'
}

recommendations = recommend_kernel(data_chars, 'classification')
print("Kernel recommendations:")
for rec in recommendations:
    print(f"  - {rec}")
```

## Further Reading

- [Kernel User Guide](../user_guide/kernels.md)
- [Embedding API](embeddings.md)
- [Backend API](backends.md)
- [Machine Learning Examples](../examples/classification.md)
