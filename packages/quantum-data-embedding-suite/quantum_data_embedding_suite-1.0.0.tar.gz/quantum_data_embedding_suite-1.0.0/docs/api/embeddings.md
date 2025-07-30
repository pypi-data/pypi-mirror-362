# Embeddings API

This page documents the quantum embedding classes and functions.

## Base Classes

### BaseEmbedding

::: quantum_data_embedding_suite.embeddings.BaseEmbedding
    options:
      show_source: true
      show_root_heading: true
      show_object_full_path: false

## Embedding Implementations

### AngleEmbedding

::: quantum_data_embedding_suite.embeddings.AngleEmbedding
    options:
      show_source: true
      show_root_heading: true
      show_object_full_path: false

### AmplitudeEmbedding

::: quantum_data_embedding_suite.embeddings.AmplitudeEmbedding
    options:
      show_source: true
      show_root_heading: true
      show_object_full_path: false

### IQPEmbedding

::: quantum_data_embedding_suite.embeddings.IQPEmbedding
    options:
      show_source: true
      show_root_heading: true
      show_object_full_path: false

### DataReuploadingEmbedding

::: quantum_data_embedding_suite.embeddings.DataReuploadingEmbedding
    options:
      show_source: true
      show_root_heading: true
      show_object_full_path: false

### HamiltonianEmbedding

::: quantum_data_embedding_suite.embeddings.HamiltonianEmbedding
    options:
      show_source: true
      show_root_heading: true
      show_object_full_path: false

## Usage Examples

### Basic Embedding Creation

```python
from quantum_data_embedding_suite.embeddings import AngleEmbedding
import numpy as np

# Create an angle embedding
embedding = AngleEmbedding(
    n_qubits=4,
    rotation_axis='Y',
    entangling_layers=1
)

# Embed a data point
data_point = np.array([0.1, 0.5, -0.3, 0.8])
circuit = embedding.embed(data_point)

# Get embedding information
info = embedding.get_info()
print(f"Circuit depth: {info['depth']}")
print(f"Number of parameters: {info['n_parameters']}")
```

### Custom Embedding Creation

```python
from quantum_data_embedding_suite.embeddings import BaseEmbedding
from qiskit import QuantumCircuit

class CustomEmbedding(BaseEmbedding):
    def __init__(self, n_qubits, custom_param=1.0):
        super().__init__(n_qubits)
        self.custom_param = custom_param
    
    def _build_circuit(self, data_point):
        circuit = QuantumCircuit(self.n_qubits)
        
        # Custom embedding logic
        for i, x in enumerate(data_point):
            circuit.ry(x * self.custom_param, i)
            
        # Add entanglement
        for i in range(self.n_qubits - 1):
            circuit.cnot(i, i + 1)
            
        return circuit
    
    def get_info(self):
        info = super().get_info()
        info['custom_param'] = self.custom_param
        return info

# Use custom embedding
custom_embedding = CustomEmbedding(n_qubits=4, custom_param=2.0)
circuit = custom_embedding.embed(data_point)
```

### Embedding Comparison

```python
from quantum_data_embedding_suite.embeddings import (
    AngleEmbedding, AmplitudeEmbedding, IQPEmbedding
)

# Create different embeddings
embeddings = {
    'angle': AngleEmbedding(n_qubits=4),
    'amplitude': AmplitudeEmbedding(n_qubits=4),
    'iqp': IQPEmbedding(n_qubits=4, depth=2)
}

# Compare circuit properties
data_point = np.random.randn(4)

for name, embedding in embeddings.items():
    circuit = embedding.embed(data_point)
    info = embedding.get_info()
    
    print(f"{name.upper()} Embedding:")
    print(f"  Circuit depth: {circuit.depth()}")
    print(f"  Gate count: {circuit.size()}")
    print(f"  Parameters: {info.get('n_parameters', 0)}")
    print()
```

## Advanced Usage

### Parameterized Embeddings

```python
from quantum_data_embedding_suite.embeddings import DataReuploadingEmbedding

# Create trainable embedding
embedding = DataReuploadingEmbedding(
    n_qubits=4,
    n_layers=3,
    rotation_gates=['RY', 'RZ'],
    trainable=True
)

# Set parameters
parameters = np.random.randn(embedding.n_parameters)
embedding.set_parameters(parameters)

# Get current parameters
current_params = embedding.get_parameters()
print(f"Number of parameters: {len(current_params)}")
```

### Embedding Optimization

```python
from quantum_data_embedding_suite.optimization import optimize_embedding_parameters

# Optimize embedding parameters
best_params = optimize_embedding_parameters(
    embedding=embedding,
    X_train=X_train,
    y_train=y_train,
    objective='classification_accuracy',
    n_trials=100
)

# Apply optimized parameters
embedding.set_parameters(best_params)
```

### Batch Processing

```python
# Process multiple data points
data_points = np.random.randn(100, 4)

# Method 1: Loop through data points
circuits = []
for data_point in data_points:
    circuit = embedding.embed(data_point)
    circuits.append(circuit)

# Method 2: Use batch method (if available)
if hasattr(embedding, 'embed_batch'):
    circuits = embedding.embed_batch(data_points)
```

## Integration with Backends

### Using Different Backends

```python
from quantum_data_embedding_suite.backends import QiskitBackend, PennyLaneBackend

# Qiskit backend
qiskit_backend = QiskitBackend(device='aer_simulator')
circuit = embedding.embed(data_point)
result = qiskit_backend.execute_circuit(circuit)

# PennyLane backend
pennylane_backend = PennyLaneBackend(device='default.qubit')
# Convert circuit for PennyLane
pennylane_circuit = pennylane_backend.convert_circuit(circuit)
```

### Hardware Compatibility

```python
# Check hardware compatibility
from quantum_data_embedding_suite.utils import check_hardware_compatibility

compatibility = check_hardware_compatibility(
    embedding=embedding,
    hardware_specs={
        'n_qubits': 127,
        'connectivity': 'heavy_hex',
        'gate_fidelity': 0.999
    }
)

print(f"Compatibility score: {compatibility['score']}")
if compatibility['compatible']:
    print("Embedding is compatible with the hardware")
else:
    print(f"Issues: {compatibility['issues']}")
```

## Error Handling

### Common Error Patterns

```python
from quantum_data_embedding_suite.embeddings import AngleEmbedding
from quantum_data_embedding_suite.exceptions import EmbeddingError

try:
    # Create embedding
    embedding = AngleEmbedding(n_qubits=4)
    
    # This will raise an error if data dimension doesn't match
    wrong_size_data = np.array([1, 2, 3])  # Only 3 features, need 4
    circuit = embedding.embed(wrong_size_data)
    
except EmbeddingError as e:
    print(f"Embedding error: {e}")
    
    # Handle by padding or truncating data
    if len(wrong_size_data) < embedding.n_qubits:
        # Pad with zeros
        padded_data = np.pad(wrong_size_data, 
                           (0, embedding.n_qubits - len(wrong_size_data)))
        circuit = embedding.embed(padded_data)
    else:
        # Truncate
        truncated_data = wrong_size_data[:embedding.n_qubits]
        circuit = embedding.embed(truncated_data)
```

### Validation and Debugging

```python
# Validate embedding before use
def validate_embedding(embedding, data_sample):
    """Validate embedding with sample data"""
    try:
        # Test embedding
        circuit = embedding.embed(data_sample)
        
        # Check circuit properties
        if circuit.depth() > 100:
            print("Warning: Circuit depth is very high")
            
        if circuit.size() > 1000:
            print("Warning: Circuit has many gates")
            
        # Test with backend
        from quantum_data_embedding_suite.backends import QiskitBackend
        backend = QiskitBackend(device='statevector_simulator')
        result = backend.execute_circuit(circuit)
        
        print("Embedding validation successful")
        return True
        
    except Exception as e:
        print(f"Embedding validation failed: {e}")
        return False

# Use validation
data_sample = np.random.randn(4)
is_valid = validate_embedding(embedding, data_sample)
```

## Performance Considerations

### Memory Usage

```python
# Monitor memory usage for large embeddings
import psutil
import gc

def monitor_memory_usage(embedding, data_points):
    """Monitor memory usage during embedding"""
    process = psutil.Process()
    initial_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    circuits = []
    for i, data_point in enumerate(data_points):
        circuit = embedding.embed(data_point)
        circuits.append(circuit)
        
        if i % 100 == 0:
            current_memory = process.memory_info().rss / 1024 / 1024
            print(f"Processed {i} points, Memory: {current_memory:.1f} MB")
            
            # Clean up if memory usage is too high
            if current_memory > initial_memory + 1000:  # 1GB increase
                gc.collect()
                
    return circuits
```

### Caching

```python
from functools import lru_cache
import hashlib

class CachedEmbedding:
    """Wrapper for caching embedding results"""
    
    def __init__(self, embedding, cache_size=128):
        self.embedding = embedding
        self.cache_size = cache_size
        
    @lru_cache(maxsize=None)
    def _cached_embed(self, data_hash):
        """Cache embedding results by data hash"""
        # This is a simplified version - in practice, you'd need
        # to store the actual data and retrieve it for embedding
        pass
    
    def embed(self, data_point):
        # Create hash of data point
        data_hash = hashlib.md5(data_point.tobytes()).hexdigest()
        
        # Check cache or compute
        if hasattr(self, '_cache') and data_hash in self._cache:
            return self._cache[data_hash]
        
        circuit = self.embedding.embed(data_point)
        
        # Store in cache
        if not hasattr(self, '_cache'):
            self._cache = {}
        if len(self._cache) < self.cache_size:
            self._cache[data_hash] = circuit
            
        return circuit

# Use cached embedding
cached_embedding = CachedEmbedding(embedding, cache_size=256)
```

## Best Practices

### Embedding Selection Guidelines

```python
def select_embedding(data_characteristics):
    """Select appropriate embedding based on data characteristics"""
    
    n_samples, n_features = data_characteristics['shape']
    data_type = data_characteristics['type']  # 'continuous', 'binary', 'categorical'
    
    # Guidelines for embedding selection
    if n_features <= 4:
        return AngleEmbedding(n_qubits=n_features)
    elif n_features <= 16 and data_type == 'continuous':
        return AmplitudeEmbedding(n_qubits=int(np.ceil(np.log2(n_features))))
    elif data_characteristics.get('complex_interactions', False):
        n_qubits = min(6, int(np.ceil(np.log2(n_features))))
        return IQPEmbedding(n_qubits=n_qubits, depth=2)
    else:
        # Default to angle embedding with feature selection
        n_qubits = min(8, n_features)
        return AngleEmbedding(n_qubits=n_qubits)

# Example usage
data_chars = {
    'shape': (1000, 10),
    'type': 'continuous',
    'complex_interactions': True
}

recommended_embedding = select_embedding(data_chars)
```

### Parameter Initialization

```python
def initialize_embedding_parameters(embedding, method='random'):
    """Initialize embedding parameters using different strategies"""
    
    if not hasattr(embedding, 'set_parameters'):
        return  # Not a parameterized embedding
    
    n_params = embedding.n_parameters
    
    if method == 'random':
        # Random initialization
        params = np.random.uniform(-np.pi, np.pi, n_params)
    elif method == 'xavier':
        # Xavier initialization
        fan_in = n_params
        limit = np.sqrt(6.0 / fan_in)
        params = np.random.uniform(-limit, limit, n_params)
    elif method == 'zeros':
        # Zero initialization
        params = np.zeros(n_params)
    elif method == 'small_random':
        # Small random values
        params = np.random.normal(0, 0.1, n_params)
    
    embedding.set_parameters(params)
    return params

# Initialize parameters
params = initialize_embedding_parameters(embedding, method='xavier')
```

## Further Reading

- [Embedding User Guide](../user_guide/embeddings.md)
- [Kernel API](kernels.md)
- [Backend API](backends.md)
- [Optimization Tutorial](../tutorials/optimization.ipynb)
