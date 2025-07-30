# Quantum Kernels

This guide covers quantum kernel methods available in the Quantum Data Embedding Suite.

## Overview

Quantum kernels are similarity measures computed using quantum circuits. They form the foundation of quantum machine learning algorithms, particularly quantum support vector machines (QSVMs). A quantum kernel measures similarity between data points by comparing their quantum state representations.

## What is a Quantum Kernel?

A quantum kernel $K(x_i, x_j)$ computes the similarity between two data points $x_i$ and $x_j$ by:

1. Encoding both points into quantum states: $|\psi(x_i)\rangle$ and $|\psi(x_j)\rangle$
2. Computing their overlap: $K(x_i, x_j) = |\langle\psi(x_i)|\psi(x_j)\rangle|^2$

This quantum approach can capture complex data relationships that classical kernels might miss.

## Kernel Types

### Fidelity Kernel

The fidelity kernel computes the state overlap between quantum embeddings.

#### Implementation

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
```

#### Mathematical Foundation

For quantum states $|\psi(x_i)\rangle$ and $|\psi(x_j)\rangle$:

$$K_{fidelity}(x_i, x_j) = |\langle\psi(x_i)|\psi(x_j)\rangle|^2$$

#### Configuration Options

```python
kernel = FidelityKernel(
    embedding=embedding,
    backend="qiskit",
    shots=1024,  # Number of shots for noisy simulation
    cache_circuits=True,  # Cache quantum circuits
    parallel=True  # Parallel computation
)
```

#### When to Use

- **Standard quantum ML applications**
- **When you need theoretical guarantees**
- **Comparing different embeddings**
- **Proof-of-concept experiments**

#### Advantages

- Theoretically well-understood
- Direct state comparison
- Works with any embedding
- Provides quantum advantage potential

#### Limitations

- Can be expensive to compute
- Sensitive to noise
- May require many measurements
- Limited by quantum hardware constraints

### Projected Kernel

The projected kernel uses measurement outcomes instead of full state information.

#### Implementation

```python
from quantum_data_embedding_suite.kernels import ProjectedKernel

kernel = ProjectedKernel(
    embedding=embedding,
    measurement_basis="computational",  # or "random_pauli"
    n_measurements=100,
    measurement_strategy="adaptive"
)

K = kernel.compute_kernel(X)
```

#### Mathematical Foundation

Using measurement outcomes $m_i$ and $m_j$:

$$K_{projected}(x_i, x_j) = \sum_k w_k \langle m_i^{(k)} | m_j^{(k)} \rangle$$

Where $w_k$ are measurement weights and $m^{(k)}$ are measurement outcomes.

#### Measurement Strategies

**Computational Basis**

```python
kernel = ProjectedKernel(
    embedding=embedding,
    measurement_basis="computational",
    n_measurements=1000
)
```

**Random Pauli Measurements**

```python
kernel = ProjectedKernel(
    embedding=embedding,
    measurement_basis="random_pauli",
    n_measurements=100,
    pauli_weight=2  # Average number of non-identity Paulis
)
```

**Adaptive Measurements**

```python
kernel = ProjectedKernel(
    embedding=embedding,
    measurement_strategy="adaptive",
    n_measurements=50,
    adaptation_rate=0.1
)
```

#### When to Use

- **NISQ device compatibility**
- **When full state access is unavailable**
- **Reduced measurement requirements**
- **Hardware-efficient implementations**

#### Advantages

- NISQ-friendly
- Fewer measurement requirements
- Can work with partial information
- Naturally handles noise

#### Limitations

- Approximation of true kernel
- Requires careful measurement design
- May lose some quantum information
- Performance depends on measurement choice

### Trainable Kernel

Trainable kernels have parameters that can be optimized for specific tasks.

#### Implementation

```python
from quantum_data_embedding_suite.kernels import TrainableKernel

kernel = TrainableKernel(
    embedding=embedding,
    n_parameters=20,
    parameter_bounds=(-np.pi, np.pi),
    optimization_method="adam",
    learning_rate=0.01
)

# Train the kernel
kernel.fit(X_train, y_train, epochs=100)

# Use trained kernel
K = kernel.compute_kernel(X_test)
```

#### Architecture

Trainable kernels add parameterized layers:

```python
# Configure trainable layers
kernel = TrainableKernel(
    embedding=embedding,
    trainable_layers=[
        {"type": "rotation", "gates": ["RY", "RZ"]},
        {"type": "entangling", "pattern": "linear"},
        {"type": "rotation", "gates": ["RX"]}
    ]
)
```

#### Optimization Methods

**Gradient-based Optimization**

```python
kernel = TrainableKernel(
    embedding=embedding,
    optimization_method="adam",
    learning_rate=0.01,
    gradient_method="parameter_shift"
)
```

**Evolutionary Strategies**

```python
kernel = TrainableKernel(
    embedding=embedding,
    optimization_method="evolutionary",
    population_size=50,
    mutation_rate=0.1
)
```

**Bayesian Optimization**

```python
kernel = TrainableKernel(
    embedding=embedding,
    optimization_method="bayesian",
    acquisition_function="expected_improvement",
    n_initial_points=20
)
```

#### Training Strategies

**Supervised Training**

```python
# Train to maximize classification accuracy
kernel.fit(
    X_train, y_train,
    objective="classification_accuracy",
    validation_split=0.2
)
```

**Unsupervised Training**

```python
# Train to maximize kernel alignment
kernel.fit(
    X_train,
    objective="kernel_alignment",
    target_kernel=classical_kernel
)
```

**Regularized Training**

```python
# Train with regularization
kernel.fit(
    X_train, y_train,
    objective="classification_accuracy",
    regularization=0.01,
    regularization_type="l2"
)
```

#### When to Use

- **Task-specific optimization**
- **When standard kernels underperform**
- **Transfer learning scenarios**
- **Research into quantum advantage**

#### Advantages

- Adaptive to specific problems
- Can learn optimal representations
- Potential for improved performance
- Flexible architecture

#### Limitations

- Requires optimization
- Risk of overfitting
- Higher computational cost
- May need careful regularization

## Kernel Computation

### Computing Kernel Matrices

#### Full Kernel Matrix

```python
# Compute full kernel matrix
K = kernel.compute_kernel(X)
print(f"Kernel shape: {K.shape}")
print(f"Kernel is symmetric: {np.allclose(K, K.T)}")
```

#### Kernel Between Different Sets

```python
# Compute kernel between training and test sets
K_train_test = kernel.compute_kernel(X_train, X_test)
print(f"Cross-kernel shape: {K_train_test.shape}")
```

#### Kernel Diagonal

```python
# Compute only diagonal elements (faster)
K_diag = kernel.compute_diagonal(X)
print(f"Diagonal shape: {K_diag.shape}")
```

### Performance Optimization

#### Batch Processing

```python
# Process large datasets in batches
kernel = FidelityKernel(
    embedding=embedding,
    batch_size=100,  # Process 100 samples at a time
    n_jobs=4  # Use 4 parallel processes
)

K = kernel.compute_kernel(large_X)
```

#### Caching

```python
# Enable caching for repeated computations
kernel = FidelityKernel(
    embedding=embedding,
    cache_circuits=True,
    cache_size=1000  # Cache up to 1000 circuits
)
```

#### Approximate Computation

```python
# Use approximation for speed
kernel = FidelityKernel(
    embedding=embedding,
    approximation="random_sampling",
    n_samples=100  # Use 100 random samples
)
```

## Kernel Analysis

### Kernel Properties

#### Spectrum Analysis

```python
from quantum_data_embedding_suite.analysis import analyze_kernel_spectrum

# Analyze kernel eigenvalues
spectrum_info = analyze_kernel_spectrum(K)
print(f"Effective rank: {spectrum_info['effective_rank']}")
print(f"Condition number: {spectrum_info['condition_number']}")
```

#### Kernel Alignment

```python
from quantum_data_embedding_suite.metrics import kernel_alignment

# Compare quantum and classical kernels
alignment = kernel_alignment(K_quantum, K_classical)
print(f"Kernel alignment: {alignment:.3f}")
```

#### Expressivity Metrics

```python
from quantum_data_embedding_suite.metrics import kernel_expressivity

# Measure kernel expressivity
expressivity = kernel_expressivity(
    kernel=kernel,
    X=X,
    n_samples=1000
)
print(f"Kernel expressivity: {expressivity:.3f}")
```

### Visualization

#### Kernel Matrix Heatmap

```python
from quantum_data_embedding_suite.visualization import plot_kernel_matrix

# Visualize kernel matrix
plot_kernel_matrix(
    K, 
    labels=y,
    title="Quantum Kernel Matrix",
    save_path="kernel_heatmap.png"
)
```

#### Kernel Eigenspectrum

```python
from quantum_data_embedding_suite.visualization import plot_kernel_spectrum

# Plot eigenvalue distribution
plot_kernel_spectrum(
    K,
    n_eigenvalues=50,
    title="Kernel Eigenspectrum"
)
```

#### Kernel PCA

```python
from quantum_data_embedding_suite.visualization import plot_kernel_pca

# Visualize data in kernel space
plot_kernel_pca(
    K, 
    labels=y,
    n_components=2,
    title="Kernel PCA Visualization"
)
```

## Advanced Usage

### Custom Kernels

#### Creating Custom Kernel Classes

```python
from quantum_data_embedding_suite.kernels import BaseKernel

class CustomKernel(BaseKernel):
    def __init__(self, embedding, custom_param=1.0):
        super().__init__(embedding)
        self.custom_param = custom_param
    
    def _compute_element(self, x_i, x_j):
        """Compute kernel element K(x_i, x_j)"""
        # Custom kernel computation logic
        circuit_i = self.embedding.embed(x_i)
        circuit_j = self.embedding.embed(x_j)
        
        # Custom similarity computation
        similarity = self._custom_similarity(circuit_i, circuit_j)
        return similarity * self.custom_param
```

#### Composite Kernels

```python
class CompositeKernel(BaseKernel):
    def __init__(self, kernels, weights=None):
        self.kernels = kernels
        self.weights = weights or [1.0] * len(kernels)
    
    def compute_kernel(self, X, Y=None):
        """Combine multiple kernels"""
        K_combined = np.zeros((len(X), len(Y or X)))
        
        for kernel, weight in zip(self.kernels, self.weights):
            K_i = kernel.compute_kernel(X, Y)
            K_combined += weight * K_i
            
        return K_combined / sum(self.weights)
```

### Kernel Selection

#### Automatic Kernel Selection

```python
from quantum_data_embedding_suite.selection import select_best_kernel

# Automatically select best kernel
best_kernel = select_best_kernel(
    X_train, y_train,
    kernel_types=["fidelity", "projected", "trainable"],
    embedding_types=["angle", "iqp"],
    cv_folds=5,
    metric="accuracy"
)
```

#### Cross-Validation

```python
from sklearn.model_selection import cross_val_score
from sklearn.svm import SVC

# Evaluate kernel with cross-validation
K = kernel.compute_kernel(X)
svm = SVC(kernel='precomputed')
scores = cross_val_score(svm, K, y, cv=5)
print(f"CV Accuracy: {scores.mean():.3f} ± {scores.std():.3f}")
```

### Hybrid Quantum-Classical Kernels

#### Concatenated Features

```python
class HybridKernel(BaseKernel):
    def __init__(self, quantum_kernel, classical_kernel, weight=0.5):
        self.quantum_kernel = quantum_kernel
        self.classical_kernel = classical_kernel
        self.weight = weight
    
    def compute_kernel(self, X, Y=None):
        K_quantum = self.quantum_kernel.compute_kernel(X, Y)
        K_classical = self.classical_kernel.compute_kernel(X, Y)
        
        return self.weight * K_quantum + (1 - self.weight) * K_classical
```

#### Feature Space Combination

```python
def create_hybrid_features(X, quantum_kernel):
    """Combine classical and quantum features"""
    # Classical features
    classical_features = X
    
    # Quantum kernel features (kernel PCA)
    K = quantum_kernel.compute_kernel(X)
    eigenvals, eigenvecs = np.linalg.eigh(K)
    quantum_features = eigenvecs[:, -10:]  # Top 10 components
    
    # Combine features
    return np.hstack([classical_features, quantum_features])
```

## Best Practices

### Kernel Design

1. **Start simple**: Begin with fidelity kernels
2. **Match embedding**: Choose kernel appropriate for your embedding
3. **Consider hardware**: Use projected kernels for NISQ devices
4. **Monitor performance**: Track kernel quality metrics

### Optimization

1. **Batch processing**: Use batches for large datasets
2. **Caching**: Enable circuit caching for repeated computations
3. **Parallel execution**: Use multiple cores when available
4. **Approximation**: Consider approximate methods for speed

### Validation

1. **Cross-validation**: Always validate kernel performance
2. **Baseline comparison**: Compare against classical kernels
3. **Ablation studies**: Test different kernel components
4. **Hardware testing**: Validate on real quantum devices

### Troubleshooting

#### Common Issues

1. **Numerical instability**: Check for negative eigenvalues
2. **Poor performance**: Try different embeddings or kernel types
3. **Memory issues**: Use batch processing or approximation
4. **Slow computation**: Enable caching and parallelization

#### Debugging Tools

```python
# Kernel diagnostics
from quantum_data_embedding_suite.diagnostics import diagnose_kernel

diagnosis = diagnose_kernel(kernel, X, y)
print(diagnosis.summary())
```

## Integration with Machine Learning

### Scikit-learn Integration

```python
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from quantum_data_embedding_suite.sklearn import QuantumKernelTransformer

# Create pipeline with quantum kernel
pipeline = Pipeline([
    ('quantum_kernel', QuantumKernelTransformer(kernel)),
    ('svm', SVC(kernel='precomputed'))
])

# Train and evaluate
pipeline.fit(X_train, y_train)
accuracy = pipeline.score(X_test, y_test)
```

### Custom Estimators

```python
from sklearn.base import BaseEstimator, ClassifierMixin

class QuantumSVM(BaseEstimator, ClassifierMixin):
    def __init__(self, quantum_kernel, C=1.0):
        self.quantum_kernel = quantum_kernel
        self.C = C
    
    def fit(self, X, y):
        K = self.quantum_kernel.compute_kernel(X)
        self.svm_ = SVC(kernel='precomputed', C=self.C)
        self.svm_.fit(K, y)
        return self
    
    def predict(self, X):
        K = self.quantum_kernel.compute_kernel(X, self.X_train_)
        return self.svm_.predict(K)
```

## Further Reading

- [Quantum Embeddings](embeddings.md)
- [Kernel Metrics](metrics.md)
- [Optimization Tutorial](../tutorials/optimization.ipynb)
- [Real QPU Examples](../tutorials/real_qpu.ipynb)
