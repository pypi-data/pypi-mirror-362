# Quick Start

Get up and running with the Quantum Data Embedding Suite in minutes.

## Basic Example

Here's a complete example showing how to create and use a quantum embedding:

```python
import numpy as np
from quantum_data_embedding_suite import QuantumEmbeddingPipeline
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler

# 1. Load and prepare data
X, y = load_iris(return_X_y=True)
X = StandardScaler().fit_transform(X)

# 2. Create quantum embedding pipeline
pipeline = QuantumEmbeddingPipeline(
    embedding_type="angle",  # Type of quantum embedding
    n_qubits=4,             # Number of qubits
    backend="qiskit",       # Quantum backend
    shots=1024              # Number of measurements
)

# 3. Compute quantum kernel matrix
K_quantum = pipeline.fit_transform(X)
print(f"Quantum kernel shape: {K_quantum.shape}")

# 4. Evaluate embedding quality
metrics = pipeline.evaluate_embedding(X)
print(f"Expressibility: {metrics['expressibility']:.3f}")
print(f"Trainability: {metrics['trainability']:.3f}")
```

## Understanding the Output

The quantum kernel matrix `K_quantum` contains similarity values between all pairs of data points as measured in the quantum feature space. Higher values indicate more similar data points.

The metrics provide insight into embedding quality:

- **Expressibility**: How well the embedding covers the quantum state space (0-1, higher is better)
- **Trainability**: How suitable the embedding is for optimization (higher is better)

## Comparing Different Embeddings

```python
import matplotlib.pyplot as plt
from quantum_data_embedding_suite.visualization import plot_kernel_comparison

# Test different embedding types
embedding_types = ["angle", "amplitude", "iqp"]
results = {}

for emb_type in embedding_types:
    pipeline = QuantumEmbeddingPipeline(
        embedding_type=emb_type,
        n_qubits=4,
        backend="qiskit"
    )
    
    # Use subset for faster computation
    X_small = X[:20]
    K = pipeline.fit_transform(X_small)
    metrics = pipeline.evaluate_embedding(X_small)
    
    results[emb_type] = {
        'kernel': K,
        'expressibility': metrics['expressibility'],
        'trainability': metrics['trainability']
    }

# Compare results
for emb_type, result in results.items():
    print(f"{emb_type.upper()} Embedding:")
    print(f"  Expressibility: {result['expressibility']:.3f}")
    print(f"  Trainability: {result['trainability']:.3f}")
    print()
```

## Using the Command Line Interface

The package includes a CLI for rapid experimentation:

```bash
# Quick benchmark on Iris dataset
qdes-cli benchmark --dataset iris --embedding angle --n-qubits 4

# Compare multiple embeddings
qdes-cli compare --embeddings angle,iqp,amplitude --dataset wine

# Visualize quantum kernel
qdes-cli visualize --embedding angle --dataset iris --output kernel_plot.png
```

## Machine Learning with Quantum Kernels

Integrate quantum kernels with scikit-learn:

```python
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# Create quantum kernel
pipeline = QuantumEmbeddingPipeline(
    embedding_type="angle",
    n_qubits=4,
    backend="qiskit"
)

# Compute kernel matrices
K_train = pipeline.fit_transform(X_train)
K_test = pipeline.transform(X_test)

# Train SVM with precomputed quantum kernel
svm = SVC(kernel='precomputed')
svm.fit(K_train, y_train)

# Make predictions
y_pred = svm.predict(K_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Quantum SVM accuracy: {accuracy:.3f}")
```

## Working with Real Quantum Devices

To run on actual quantum hardware:

```python
# IBM Quantum device
from quantum_data_embedding_suite.backends import QiskitBackend

backend = QiskitBackend(
    device="ibmq_qasm_simulator",  # or actual device name
    shots=1024
)

pipeline = QuantumEmbeddingPipeline(
    embedding_type="angle",
    n_qubits=4,
    backend=backend
)

# Note: Use smaller datasets for real devices due to queue times
X_small = X[:10]
K = pipeline.fit_transform(X_small)
```

## Custom Embeddings

Create your own embedding:

```python
from quantum_data_embedding_suite.embeddings import BaseEmbedding

class CustomEmbedding(BaseEmbedding):
    def __init__(self, n_qubits, backend, **kwargs):
        super().__init__(n_qubits, backend, **kwargs)
    
    def get_feature_dimension(self):
        return self.n_qubits
    
    def create_circuit(self, x):
        if self.backend.name == "qiskit":
            from qiskit import QuantumCircuit
            circuit = QuantumCircuit(self.n_qubits)
            
            # Custom encoding logic
            for i, val in enumerate(x):
                circuit.ry(val * np.pi, i)
                if i > 0:
                    circuit.cx(i-1, i)
            
            return circuit

# Use custom embedding
custom_embedding = CustomEmbedding(n_qubits=4, backend=pipeline.backend)
pipeline._embedding = custom_embedding
K_custom = pipeline.transform(X[:10])
```

## Performance Tips

### For Large Datasets

```python
# Use batch processing
pipeline = QuantumEmbeddingPipeline(
    embedding_type="angle",
    n_qubits=4,
    backend="qiskit",
    batch_size=50  # Process in batches
)

# Or use parallel processing
pipeline = QuantumEmbeddingPipeline(
    embedding_type="angle",
    n_qubits=4,
    backend="qiskit",
    n_jobs=4  # Use 4 parallel processes
)
```

### For Quick Prototyping

```python
# Reduce shots for faster computation
pipeline = QuantumEmbeddingPipeline(
    embedding_type="angle",
    n_qubits=4,
    backend="qiskit",
    shots=100  # Fewer shots = faster but less accurate
)

# Use fewer qubits
pipeline = QuantumEmbeddingPipeline(
    embedding_type="angle",
    n_qubits=2,  # Smaller circuits = faster simulation
    backend="qiskit"
)
```

## Common Patterns

### Data Preprocessing Pipeline

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, PCA

# Classical preprocessing
preprocessor = Pipeline([
    ('scaler', StandardScaler()),
    ('pca', PCA(n_components=4))
])

X_processed = preprocessor.fit_transform(X)

# Quantum embedding
quantum_pipeline = QuantumEmbeddingPipeline(
    embedding_type="angle",
    n_qubits=4,
    backend="qiskit"
)

K = quantum_pipeline.fit_transform(X_processed)
```

### Hyperparameter Tuning

```python
from sklearn.model_selection import GridSearchCV

# Define parameter grid
param_grid = {
    'embedding_type': ['angle', 'iqp'],
    'n_qubits': [3, 4, 5],
    'shots': [512, 1024]
}

# Note: This is pseudocode - actual implementation would require
# a custom estimator that wraps QuantumEmbeddingPipeline
```

## Error Handling

```python
try:
    pipeline = QuantumEmbeddingPipeline(
        embedding_type="angle",
        n_qubits=4,
        backend="qiskit"
    )
    K = pipeline.fit_transform(X)
    
except Exception as e:
    print(f"Error: {e}")
    # Fallback to classical kernel
    from sklearn.metrics.pairwise import rbf_kernel
    K = rbf_kernel(X)
```

## Next Steps

Now that you've seen the basics, explore more advanced topics:

- **[User Guide](user_guide.md)**: Detailed documentation of all features
- **[Tutorials](tutorials/basic_workflow.md)**: Step-by-step learning materials  
- **[Examples](examples/index.md)**: Real-world applications
- **[API Reference](api/pipeline.md)**: Complete API documentation

## Getting Help

If you encounter issues:

1. Check the [troubleshooting section](installation.md#troubleshooting) in the installation guide
2. Search [GitHub Issues](https://github.com/krish567366/quantum-data-embedding-suite/issues)
3. Join the [GitHub Discussions](https://github.com/krish567366/quantum-data-embedding-suite/discussions)
4. Email the author: bajpaikrishna715@gmail.com
