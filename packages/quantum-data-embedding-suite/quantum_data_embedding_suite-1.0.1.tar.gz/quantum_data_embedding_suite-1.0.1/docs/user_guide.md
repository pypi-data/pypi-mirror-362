# User Guide

This guide provides comprehensive instructions for using the Quantum Data Embedding Suite.

## Table of Contents

1. [Installation](#installation)
2. [Basic Usage](#basic-usage)
3. [Embedding Types](#embedding-types)
4. [Quantum Kernels](#quantum-kernels)
5. [Quality Metrics](#quality-metrics)
6. [Backends](#backends)
7. [CLI Usage](#cli-usage)
8. [Advanced Features](#advanced-features)
9. [Best Practices](#best-practices)
10. [Troubleshooting](#troubleshooting)

## Installation

### Requirements

- Python 3.8+
- NumPy
- SciPy
- Scikit-learn
- Matplotlib
- Qiskit (for quantum simulation)
- PennyLane (optional, for additional backend support)

### Basic Installation

```bash
pip install quantum-data-embedding-suite
```

### Development Installation

```bash
git clone https://github.com/your-repo/quantum-data-embedding-suite
cd quantum-data-embedding-suite
pip install -e .
```

### Optional Dependencies

For PennyLane support:

```bash
pip install pennylane
```

For visualization enhancements:

```bash
pip install seaborn plotly
```

## Basic Usage

### Creating an Embedding Pipeline

The `QuantumEmbeddingPipeline` is the main interface for quantum data embedding:

```python
from quantum_data_embedding_suite import QuantumEmbeddingPipeline
import numpy as np

# Create sample data
X = np.random.randn(100, 4)

# Create pipeline
pipeline = QuantumEmbeddingPipeline(
    embedding_type="angle",
    n_qubits=4,
    backend="qiskit",
    shots=1024
)

# Compute quantum kernel
K = pipeline.fit_transform(X)
```

### Pipeline Parameters

- `embedding_type`: Type of quantum embedding ("angle", "amplitude", "iqp", "data_reuploading", "hamiltonian")
- `n_qubits`: Number of qubits in the quantum circuit
- `backend`: Quantum backend ("qiskit" or "pennylane")
- `shots`: Number of measurement shots (for noisy simulation)
- `normalize`: Whether to normalize input data
- `seed`: Random seed for reproducibility

## Embedding Types

### Angle Embedding

Encodes data as rotation angles in RY gates:

```python
from quantum_data_embedding_suite.embeddings import AngleEmbedding

embedding = AngleEmbedding(n_qubits=4)
circuit = embedding.embed(X[0])  # Embed single data point
```

**Use Cases**:

- Small datasets
- Real-valued features
- When interpretability is important

**Parameters**:

- `rotation_axis`: Rotation axis ('X', 'Y', 'Z')
- `entangling_layers`: Number of entangling layers

### Amplitude Embedding

Encodes data directly in quantum state amplitudes:

```python
from quantum_data_embedding_suite.embeddings import AmplitudeEmbedding

embedding = AmplitudeEmbedding(n_qubits=4)
circuit = embedding.embed(X[0])
```

**Use Cases**:

- High-dimensional data
- When preserving data relationships is crucial
- Normalized data vectors

**Limitations**:

- Requires data normalization
- Limited by 2^n_qubits dimensional vectors

### IQP Embedding

Uses Instantaneous Quantum Polynomial circuits:

```python
from quantum_data_embedding_suite.embeddings import IQPEmbedding

embedding = IQPEmbedding(n_qubits=4, depth=2)
circuit = embedding.embed(X[0])
```

**Use Cases**:

- Complex feature interactions
- When classical simulation is hard
- Theoretical quantum advantage scenarios

**Parameters**:

- `depth`: Circuit depth
- `connectivity`: Qubit connectivity pattern

### Data Re-uploading

Multiple encoding layers for increased expressivity:

```python
from quantum_data_embedding_suite.embeddings import DataReuploadingEmbedding

embedding = DataReuploadingEmbedding(
    n_qubits=4, 
    n_layers=3,
    rotation_gates=['RY', 'RZ']
)
circuit = embedding.embed(X[0])
```

**Use Cases**:

- Complex datasets
- When single encoding is insufficient
- Trainable quantum circuits

**Parameters**:

- `n_layers`: Number of encoding layers
- `rotation_gates`: Types of rotation gates
- `entangling_strategy`: How to create entanglement

### Hamiltonian Embedding

Physics-inspired embeddings using problem Hamiltonians:

```python
from quantum_data_embedding_suite.embeddings import HamiltonianEmbedding

embedding = HamiltonianEmbedding(
    n_qubits=4,
    hamiltonian_type="heisenberg",
    evolution_time=1.0
)
circuit = embedding.embed(X[0])
```

**Use Cases**:

- Physics-inspired problems
- Time evolution problems
- Custom Hamiltonian designs

## Quantum Kernels

### Fidelity Kernel

Computes state overlap between embedded data points:

```python
from quantum_data_embedding_suite.kernels import FidelityKernel

kernel = FidelityKernel(embedding, backend="qiskit")
K = kernel.compute_kernel(X)
```

### Projected Kernel

Uses measurement-based similarity:

```python
from quantum_data_embedding_suite.kernels import ProjectedKernel

kernel = ProjectedKernel(
    embedding, 
    measurement_basis="computational",
    n_measurements=100
)
K = kernel.compute_kernel(X)
```

### Trainable Kernel

Parameterized kernels with optimization:

```python
from quantum_data_embedding_suite.kernels import TrainableKernel

kernel = TrainableKernel(
    embedding,
    n_parameters=10,
    optimization_method="adam"
)

# Train kernel on data
kernel.fit(X, y)
K = kernel.compute_kernel(X)
```

## Quality Metrics

### Expressibility

Measures how uniformly embeddings cover Hilbert space:

```python
from quantum_data_embedding_suite.metrics import expressibility

expr_score = expressibility(
    embedding, 
    n_samples=1000,
    backend="qiskit"
)
print(f"Expressibility: {expr_score}")
```

Higher values indicate better coverage of state space.

### Trainability

Analyzes gradient magnitudes and barren plateaus:

```python
from quantum_data_embedding_suite.metrics import trainability

train_score = trainability(
    embedding,
    X,
    n_samples=100
)
print(f"Trainability: {train_score}")
```

Higher values indicate better gradient signal.

### Gradient Variance

Evaluates optimization landscape characteristics:

```python
from quantum_data_embedding_suite.metrics import gradient_variance

grad_var = gradient_variance(
    embedding,
    X,
    n_parameters=10
)
print(f"Gradient Variance: {grad_var}")
```

## Backends

### Qiskit Backend

Default quantum simulation backend:

```python
from quantum_data_embedding_suite.backends import QiskitBackend

backend = QiskitBackend(
    shots=1024,
    noise_model=None,  # Add noise for realistic simulation
    device="aer_simulator"
)
```

**Features**:

- Statevector and shot-based simulation
- Noise model support
- Real device execution
- Optimization transpilation

### PennyLane Backend

Alternative quantum ML framework:

```python
from quantum_data_embedding_suite.backends import PennyLaneBackend

backend = PennyLaneBackend(
    device="default.qubit",
    shots=1024
)
```

**Features**:

- Automatic differentiation
- Hybrid classical-quantum optimization
- Multiple device support
- JAX/TensorFlow integration

## CLI Usage

The package includes a command-line interface for rapid experimentation:

### Benchmark Command

Compare quantum vs classical performance:

```bash
qdes-cli benchmark --dataset iris --embedding angle --n-qubits 4
```

### Compare Command

Compare different embedding types:

```bash
qdes-cli compare --embeddings angle,iqp --dataset wine --output results.json
```

### Visualize Command

Generate visualization plots:

```bash
qdes-cli visualize --data data.csv --embedding angle --output plots/
```

### Experiment Command

Run custom experiments:

```bash
qdes-cli experiment --config experiment.yaml
```

## Advanced Features

### Custom Embeddings

Create custom embedding types:

```python
from quantum_data_embedding_suite.embeddings import BaseEmbedding

class CustomEmbedding(BaseEmbedding):
    def __init__(self, n_qubits, **kwargs):
        super().__init__(n_qubits)
        # Custom initialization
    
    def _build_circuit(self, data_point):
        # Implement custom embedding logic
        pass
```

### Batch Processing

Process large datasets efficiently:

```python
# Use batch processing for large datasets
pipeline = QuantumEmbeddingPipeline(
    embedding_type="angle",
    n_qubits=4,
    batch_size=100  # Process in batches
)

K = pipeline.fit_transform(large_dataset)
```

### Parallel Execution

Speed up computation with parallel processing:

```python
pipeline = QuantumEmbeddingPipeline(
    embedding_type="angle",
    n_qubits=4,
    n_jobs=4  # Use 4 parallel processes
)
```

## Best Practices

### Data Preprocessing

1: **Normalize your data**: Most embeddings work better with normalized features

```python
from sklearn.preprocessing import StandardScaler
X = StandardScaler().fit_transform(X)
```

2: **Handle missing values**: Ensure no NaN or infinite values

```python
from sklearn.impute import SimpleImputer
X = SimpleImputer().fit_transform(X)
```

3: **Feature selection**: Remove irrelevant features

```python
from sklearn.feature_selection import SelectKBest
X = SelectKBest(k=10).fit_transform(X, y)
```

### Choosing Embeddings

1. **Start simple**: Begin with angle embedding for initial experiments
2. **Consider data size**: Use amplitude embedding for high-dimensional data
3. **Think about structure**: Use IQP for complex feature interactions
4. **Scale gradually**: Start with fewer qubits and increase as needed

### Optimization

1. **Use appropriate shots**: Balance accuracy vs computation time
2. **Leverage caching**: Reuse computed kernels when possible
3. **Monitor metrics**: Track expressibility and trainability
4. **Profile performance**: Identify bottlenecks in your pipeline

### Debugging

1. **Check data shapes**: Ensure compatibility with embedding requirements
2. **Validate circuits**: Use circuit visualization tools
3. **Monitor convergence**: Track optimization progress
4. **Use logging**: Enable verbose output for debugging

## Troubleshooting

### Common Issues

#### Installation Problems

**Issue**: Package not found or import errors
**Solution**:

```bash
pip install --upgrade quantum-data-embedding-suite
python -c "import quantum_data_embedding_suite; print('Success!')"
```

#### Memory Issues

**Issue**: Out of memory errors with large datasets
**Solution**:

- Use batch processing
- Reduce number of qubits
- Use smaller shot counts
- Enable parallel processing with caution

#### Slow Performance

**Issue**: Computations taking too long
**Solution**:

- Reduce shots for initial experiments
- Use fewer qubits
- Enable caching
- Use optimized backends

#### Accuracy Issues

**Issue**: Poor quantum kernel performance
**Solution**:

- Increase shot count
- Try different embeddings
- Normalize input data
- Check for overfitting

### Getting Help

1. **Check documentation**: Most issues are covered in this guide
2. **Search issues**: Look for similar problems on GitHub
3. **Enable logging**: Use verbose output for debugging
4. **Minimal examples**: Create simple test cases
5. **Report bugs**: Open GitHub issues with reproducible examples

### Performance Optimization

#### Memory Management

```python
# For large datasets, use generators
def data_generator(X, batch_size=100):
    for i in range(0, len(X), batch_size):
        yield X[i:i+batch_size]

# Process in batches
for batch in data_generator(large_X):
    K_batch = pipeline.transform(batch)
```

#### Caching Results

```python
from functools import lru_cache

# Cache expensive computations
@lru_cache(maxsize=128)
def cached_kernel_computation(data_hash):
    return pipeline.transform(data)
```

#### Parallel Processing

```python
from joblib import Parallel, delayed

# Parallel kernel computation
def compute_kernel_row(i, X, pipeline):
    return pipeline.transform(X[[i]])

K_rows = Parallel(n_jobs=4)(
    delayed(compute_kernel_row)(i, X, pipeline) 
    for i in range(len(X))
)
```

This user guide provides a comprehensive overview of the Quantum Data Embedding Suite. For more specific examples and advanced usage patterns, refer to the tutorials and API documentation.
