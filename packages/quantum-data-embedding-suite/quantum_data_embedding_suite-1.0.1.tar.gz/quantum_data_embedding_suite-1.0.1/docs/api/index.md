# API Reference

This section provides detailed documentation for all classes and functions in the Quantum Data Embedding Suite.

## Core Components

### [Pipeline](pipeline.md)

The main `QuantumEmbeddingPipeline` class that provides the unified interface for quantum embeddings.

### [Embeddings](embeddings.md)

Quantum embedding implementations including angle, amplitude, IQP, and data re-uploading embeddings.

### [Backends](backends.md)

Quantum backend implementations supporting Qiskit and PennyLane.

### [Kernels](kernels.md)

Quantum kernel computation methods including fidelity and projected kernels.

### [Metrics](metrics.md)

Embedding quality assessment functions for expressibility, trainability, and gradient analysis.

### [Utilities](utils.md)

Data processing and validation utilities.

## Quick Reference

### Main Classes

- **`QuantumEmbeddingPipeline`** - Primary interface for quantum embeddings
- **`BaseEmbedding`** - Abstract base class for embeddings
- **`BaseBackend`** - Abstract base class for quantum backends
- **`BaseKernel`** - Abstract base class for quantum kernels

### Key Functions

- **`expressibility()`** - Compute embedding expressibility
- **`trainability()`** - Compute embedding trainability  
- **`validate_data()`** - Validate input data format
- **`plot_kernel_matrix()`** - Visualize quantum kernel matrices

### Supported Embedding Types

- `"angle"` - Angle embedding
- `"amplitude"` - Amplitude embedding
- `"iqp"` - Instantaneous Quantum Polynomial embedding
- `"data_reuploading"` - Data re-uploading embedding
- `"hamiltonian"` - Hamiltonian evolution embedding

### Supported Backends

- `"qiskit"` - IBM Qiskit backend (default)
- `"pennylane"` - Xanadu PennyLane backend

## Usage Patterns

### Basic Usage

```python
from quantum_data_embedding_suite import QuantumEmbeddingPipeline

# Create pipeline
pipeline = QuantumEmbeddingPipeline(
    embedding_type="angle",
    n_qubits=4,
    backend="qiskit"
)

# Fit and transform data
K = pipeline.fit_transform(X)
```

### Advanced Configuration

```python
from quantum_data_embedding_suite.backends import QiskitBackend
from quantum_data_embedding_suite.embeddings import AngleEmbedding

# Custom backend
backend = QiskitBackend(device="aer_simulator", shots=2048)

# Custom embedding
embedding = AngleEmbedding(n_qubits=4, depth=2)

# Pipeline with custom components
pipeline = QuantumEmbeddingPipeline(
    embedding=embedding,
    backend=backend
)
```

### Error Handling

All classes provide comprehensive error handling with descriptive messages:

```python
try:
    pipeline = QuantumEmbeddingPipeline(
        embedding_type="invalid_type",
        n_qubits=4
    )
except ValueError as e:
    print(f"Configuration error: {e}")

try:
    K = pipeline.fit_transform(invalid_data)
except ValueError as e:
    print(f"Data validation error: {e}")
```

## Type Annotations

The package uses comprehensive type annotations for better IDE support and error checking:

```python
from typing import Optional, Union, Dict, Any
import numpy as np
from numpy.typing import NDArray

def compute_kernel(
    X: NDArray[np.floating],
    Y: Optional[NDArray[np.floating]] = None,
    normalize: bool = True
) -> NDArray[np.floating]:
    """Type-annotated function example."""
    pass
```

## Performance Considerations

### Memory Usage

- Kernel matrices scale as O(n²) in memory
- Use batch processing for large datasets
- Consider data compression for storage

### Computational Complexity

- Quantum simulations scale exponentially with qubit count
- Shot noise affects kernel quality
- Backend choice impacts performance

### Optimization Tips

- Cache kernel matrices when possible
- Use appropriate shot counts for your precision needs
- Consider classical preprocessing for dimensionality reduction

## Extension Points

The package is designed for extensibility:

### Custom Embeddings

```python
from quantum_data_embedding_suite.embeddings import BaseEmbedding

class MyCustomEmbedding(BaseEmbedding):
    def create_circuit(self, x: np.ndarray) -> Any:
        # Implement your embedding logic
        pass
```

### Custom Backends

```python
from quantum_data_embedding_suite.backends import BaseBackend

class MyCustomBackend(BaseBackend):
    def execute_circuit(self, circuit: Any, shots: int) -> Dict[str, int]:
        # Implement your backend logic
        pass
```

### Custom Kernels

```python
from quantum_data_embedding_suite.kernels import BaseKernel

class MyCustomKernel(BaseKernel):
    def _compute_element(self, x_i: np.ndarray, x_j: np.ndarray) -> float:
        # Implement your kernel computation
        pass
```

## Version Compatibility

- **Python**: 3.8+
- **NumPy**: 1.20+
- **Scikit-learn**: 1.0+
- **Qiskit**: 0.39+ (optional)
- **PennyLane**: 0.28+ (optional)
