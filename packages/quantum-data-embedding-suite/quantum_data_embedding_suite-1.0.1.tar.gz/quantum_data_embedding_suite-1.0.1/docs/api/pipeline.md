# Pipeline API

The `QuantumEmbeddingPipeline` class is the main interface for creating and using quantum data embeddings.

## Class: QuantumEmbeddingPipeline

The primary class for quantum data embedding operations.

### Constructor

```python
QuantumEmbeddingPipeline(
    embedding_type: str = "angle",
    n_qubits: int = 4,
    backend: Union[str, BaseBackend] = "qiskit",
    shots: int = 1024,
    random_state: Optional[int] = None,
    cache_embeddings: bool = True,
    embedding: Optional[BaseEmbedding] = None,
    kernel: Optional[BaseKernel] = None,
    **kwargs
)
```

#### Parameters

- **embedding_type** (`str`, default="angle"): Type of quantum embedding to use.
  - Supported values: `"angle"`, `"amplitude"`, `"iqp"`, `"data_reuploading"`, `"hamiltonian"`
  
- **n_qubits** (`int`, default=4): Number of qubits in the quantum circuit.
  - Must be positive integer
  - Should be ≥ log₂(data dimension) for efficiency
  
- **backend** (`str` or `BaseBackend`, default="qiskit"): Quantum backend to use.
  - String values: `"qiskit"`, `"pennylane"`
  - Or custom backend instance
  
- **shots** (`int`, default=1024): Number of measurement shots.
  - Higher values → more accurate but slower
  - Typical range: 512-8192
  
- **random_state** (`int`, optional): Random seed for reproducibility.

- **cache_embeddings** (`bool`, default=True): Whether to cache computed embeddings.

- **embedding** (`BaseEmbedding`, optional): Custom embedding instance.
  - Overrides `embedding_type` if provided
  
- **kernel** (`BaseKernel`, optional): Custom kernel instance.
  - Uses fidelity kernel by default

- **kwargs**: Additional parameters passed to embedding/backend constructors.

#### Raises

- **ValueError**: If invalid parameters are provided
- **ImportError**: If required backend dependencies are missing

### Methods

#### fit(X, y=None)

Fit the quantum embedding to training data.

```python
def fit(self, X: ArrayLike, y: ArrayLike = None) -> "QuantumEmbeddingPipeline"
```

**Parameters:**

- **X** (`array-like`): Training data of shape (n_samples, n_features)
- **y** (`array-like`, optional): Target values (ignored, present for API compatibility)

**Returns:**

- **self**: The fitted pipeline instance

**Raises:**

- **ValueError**: If X has invalid shape or contains invalid values

#### transform(X)

Transform data using the fitted quantum embedding.

```python
def transform(self, X: ArrayLike) -> np.ndarray
```

**Parameters:**

- **X** (`array-like`): Data to transform of shape (n_samples, n_features)

**Returns:**

- **K** (`np.ndarray`): Quantum kernel matrix of shape (n_samples, n_train_samples)

**Raises:**

- **ValueError**: If pipeline not fitted or X has invalid shape
- **RuntimeError**: If quantum computation fails

#### fit_transform(X, y=None)

Fit the embedding and transform the data in one step.

```python
def fit_transform(self, X: ArrayLike, y: ArrayLike = None) -> np.ndarray
```

**Parameters:**

- **X** (`array-like`): Training data of shape (n_samples, n_features)
- **y** (`array-like`, optional): Target values (ignored)

**Returns:**

- **K** (`np.ndarray`): Quantum kernel matrix of shape (n_samples, n_samples)

#### evaluate_embedding(X, metrics=None)

Evaluate the quality of the quantum embedding.

```python
def evaluate_embedding(
    self, 
    X: ArrayLike, 
    metrics: Optional[List[str]] = None
) -> Dict[str, float]
```

**Parameters:**

- **X** (`array-like`): Data to evaluate on
- **metrics** (`list`, optional): List of metrics to compute.
  - Available: `["expressibility", "trainability", "gradient_variance"]`
  - Default: computes all metrics

**Returns:**

- **results** (`dict`): Dictionary mapping metric names to values

#### get_embedding_info()

Get information about the current embedding configuration.

```python
def get_embedding_info() -> Dict[str, Any]
```

**Returns:**

- **info** (`dict`): Configuration information including:
  - `embedding_type`: Type of embedding
  - `n_qubits`: Number of qubits
  - `backend_name`: Backend name
  - `shots`: Number of shots
  - `embedding_params`: Embedding-specific parameters

#### compute_quantum_advantage(X_train, X_test=None, classical_kernel="rbf")

Assess potential quantum advantage over classical methods.

```python
def compute_quantum_advantage(
    self,
    X_train: ArrayLike,
    X_test: ArrayLike = None,
    classical_kernel: str = "rbf"
) -> Dict[str, Any]
```

**Parameters:**

- **X_train** (`array-like`): Training data
- **X_test** (`array-like`, optional): Test data (uses X_train if None)
- **classical_kernel** (`str`): Classical kernel to compare against

**Returns:**

- **analysis** (`dict`): Quantum advantage analysis including:
  - `quantum_kernel`: Quantum kernel matrix
  - `classical_kernel`: Classical kernel matrix
  - `correlation`: Correlation between kernels
  - `spectral_analysis`: Eigenvalue comparison
  - `advantage_score`: Estimated advantage score

### Properties

#### is_fitted

Check if the pipeline has been fitted.

```python
@property
def is_fitted(self) -> bool
```

**Returns:**

- **fitted** (`bool`): True if pipeline is fitted

#### n_features_in_

Number of features seen during fitting.

```python
@property
def n_features_in_(self) -> int
```

**Returns:**

- **n_features** (`int`): Number of input features

#### backend_name

Name of the quantum backend being used.

```python
@property
def backend_name(self) -> str
```

**Returns:**

- **name** (`str`): Backend name

### Class Methods

#### supported_embeddings()

Get list of supported embedding types.

```python
@classmethod
def supported_embeddings(cls) -> List[str]
```

**Returns:**

- **embeddings** (`list`): List of supported embedding type strings

#### supported_backends()

Get list of supported backend types.

```python
@classmethod
def supported_backends(cls) -> List[str]
```

**Returns:**

- **backends** (`list`): List of supported backend type strings

## Usage Examples

### Basic Usage

```python
from quantum_data_embedding_suite import QuantumEmbeddingPipeline
import numpy as np

# Create sample data
X = np.random.randn(50, 4)

# Create and fit pipeline
pipeline = QuantumEmbeddingPipeline(
    embedding_type="angle",
    n_qubits=4,
    backend="qiskit",
    shots=1024
)

# Compute quantum kernel
K = pipeline.fit_transform(X)
print(f"Kernel shape: {K.shape}")  # (50, 50)
```

### Advanced Configuration

```python
from quantum_data_embedding_suite.backends import QiskitBackend
from quantum_data_embedding_suite.embeddings import IQPEmbedding

# Custom backend with specific settings
backend = QiskitBackend(
    device="aer_simulator",
    shots=2048,
    optimization_level=2
)

# Custom embedding with parameters
embedding = IQPEmbedding(
    n_qubits=4,
    depth=3,
    entanglement="circular"
)

# Pipeline with custom components
pipeline = QuantumEmbeddingPipeline(
    embedding=embedding,
    backend=backend
)

K = pipeline.fit_transform(X)
```

### Evaluation and Analysis

```python
# Evaluate embedding quality
metrics = pipeline.evaluate_embedding(X)
print(f"Expressibility: {metrics['expressibility']:.3f}")
print(f"Trainability: {metrics['trainability']:.3f}")

# Assess quantum advantage
advantage = pipeline.compute_quantum_advantage(X)
print(f"Quantum-classical correlation: {advantage['correlation']:.3f}")
print(f"Advantage score: {advantage['advantage_score']:.3f}")

# Get configuration info
info = pipeline.get_embedding_info()
print(f"Backend: {info['backend_name']}")
print(f"Embedding: {info['embedding_type']}")
```

### Batch Processing

```python
# For large datasets, process in batches
def process_large_dataset(X, batch_size=100):
    pipeline = QuantumEmbeddingPipeline(
        embedding_type="angle",
        n_qubits=4
    )
    
    # Fit on first batch
    X_first = X[:batch_size]
    pipeline.fit(X_first)
    
    # Process all data in batches
    kernels = []
    for i in range(0, len(X), batch_size):
        X_batch = X[i:i+batch_size]
        K_batch = pipeline.transform(X_batch)
        kernels.append(K_batch)
    
    return kernels

# Usage
large_X = np.random.randn(1000, 4)
kernel_blocks = process_large_dataset(large_X)
```

### Error Handling

```python
try:
    pipeline = QuantumEmbeddingPipeline(
        embedding_type="invalid_type"
    )
except ValueError as e:
    print(f"Invalid embedding type: {e}")

try:
    # Try to transform before fitting
    K = pipeline.transform(X)
except ValueError as e:
    print(f"Pipeline not fitted: {e}")

try:
    # Invalid data shape
    X_invalid = np.random.randn(10)  # 1D array
    K = pipeline.fit_transform(X_invalid)
except ValueError as e:
    print(f"Invalid data shape: {e}")
```

## Scikit-learn Compatibility

The `QuantumEmbeddingPipeline` implements the scikit-learn transformer interface:

```python
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC

# Use in scikit-learn pipelines
quantum_transformer = QuantumEmbeddingPipeline(
    embedding_type="angle",
    n_qubits=4
)

# Create preprocessing pipeline
pipeline = Pipeline([
    ('quantum', quantum_transformer),
    ('svm', SVC(kernel='precomputed'))
])

# Fit and predict
pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)
```

## Performance Considerations

### Memory Usage

- Kernel matrices require O(n²) memory
- Use batch processing for large datasets
- Enable caching for repeated computations

### Computational Cost

- Quantum simulation scales exponentially with qubits
- More shots improve accuracy but increase runtime
- Backend choice affects performance significantly

### Optimization Tips

1. Start with small qubit counts (3-5) for testing
2. Use appropriate shot counts for your precision needs
3. Cache embeddings when processing similar datasets
4. Consider classical preprocessing for dimension reduction
