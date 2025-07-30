# Embeddings

This guide covers the different types of quantum embeddings available in the Quantum Data Embedding Suite.

## Overview

Quantum embeddings are the foundation of quantum machine learning. They encode classical data into quantum states, enabling quantum algorithms to process classical information. The choice of embedding significantly impacts the performance and quantum advantage potential of your machine learning model.

## Embedding Types

### Angle Embedding

Angle embedding encodes classical data as rotation angles in quantum gates, typically RY rotations.

#### How it Works

```python
from quantum_data_embedding_suite.embeddings import AngleEmbedding
import numpy as np

# Create angle embedding
embedding = AngleEmbedding(
    n_qubits=4,
    rotation_axis='Y',  # Can be 'X', 'Y', or 'Z'
    entangling_layers=1
)

# Embed a data point
data_point = np.array([0.1, 0.5, -0.3, 0.8])
circuit = embedding.embed(data_point)
```

#### Mathematical Representation

For a data point $\mathbf{x} = (x_1, x_2, ..., x_n)$, the angle embedding applies:

$$|\psi(\mathbf{x})\rangle = \prod_{i=1}^{n} R_Y(x_i) |0\rangle^{\otimes n}$$

Where $R_Y(\theta) = \exp(-i\theta\sigma_Y/2)$ is the Y-rotation gate.

#### Parameters

- **`n_qubits`**: Number of qubits (must match data dimensionality)
- **`rotation_axis`**: Rotation axis ('X', 'Y', 'Z')
- **`entangling_layers`**: Number of entangling layers between rotations
- **`entangling_gate`**: Type of entangling gate ('CNOT', 'CZ', 'CPHASE')

#### Use Cases

- **Small to medium datasets** (up to ~20 features)
- **Real-valued continuous features**
- **When interpretability is important**
- **Initial experiments and prototyping**

#### Advantages

- Simple and interpretable
- Low circuit depth
- Easy to implement on NISQ devices
- Good for debugging

#### Limitations

- Limited expressivity for complex data
- Requires feature scaling
- May not capture feature correlations well

### Amplitude Embedding

Amplitude embedding directly encodes data in the amplitudes of a quantum state.

#### How it Works

```python
from quantum_data_embedding_suite.embeddings import AmplitudeEmbedding

# Create amplitude embedding
embedding = AmplitudeEmbedding(
    n_qubits=4,
    normalize=True,  # Automatically normalize data
    padding_value=0.0
)

# Embed data point (must be normalized)
data_point = np.array([0.5, 0.3, 0.2, 0.1])  # Must sum to norm = 1
circuit = embedding.embed(data_point)
```

#### Mathematical Representation

For normalized data $\mathbf{x} = (x_1, x_2, ..., x_{2^n})$:

$$|\psi(\mathbf{x})\rangle = \sum_{i=1}^{2^n} x_i |i\rangle$$

#### Parameters

- **`n_qubits`**: Number of qubits (supports up to $2^n$ features)
- **`normalize`**: Whether to automatically normalize input data
- **`padding_value`**: Value to pad data if shorter than $2^n$
- **`truncate`**: Whether to truncate data if longer than $2^n$

#### Use Cases

- **High-dimensional data** (up to $2^n$ features)
- **Normalized data vectors** (probability distributions, images)
- **When preserving relative magnitudes is crucial**
- **Quantum advantage scenarios**

#### Advantages

- Exponential information density
- Preserves all data relationships
- Theoretically optimal for some algorithms
- Natural for probability distributions

#### Limitations

- Requires normalized data
- Exponential scaling with qubits
- Sensitive to noise
- Limited by available qubits

### IQP Embedding

Instantaneous Quantum Polynomial (IQP) circuits create complex feature interactions through diagonal unitaries.

#### How it Works

```python
from quantum_data_embedding_suite.embeddings import IQPEmbedding

# Create IQP embedding
embedding = IQPEmbedding(
    n_qubits=4,
    depth=2,
    connectivity='linear',  # or 'all-to-all', 'circular'
    hadamard_layers=True
)

# Embed data
data_point = np.array([0.1, 0.5, -0.3, 0.8])
circuit = embedding.embed(data_point)
```

#### Mathematical Representation

An IQP circuit with depth $d$ applies:

$$U_{IQP}(\mathbf{x}) = \prod_{l=1}^{d} H^{\otimes n} \exp\left(i\sum_{j,k} x_j x_k Z_j Z_k\right) H^{\otimes n}$$

#### Parameters

- **`n_qubits`**: Number of qubits
- **`depth`**: Circuit depth (number of IQP layers)
- **`connectivity`**: Qubit connectivity pattern
- **`hadamard_layers`**: Whether to include Hadamard layers
- **`interaction_strength`**: Scaling factor for interactions

#### Use Cases

- **Complex feature interactions**
- **Theoretical quantum advantage scenarios**
- **When classical simulation is hard**
- **Research applications**

#### Advantages

- Creates complex feature correlations
- Provable classical hardness
- Flexible connectivity patterns
- Quantum supremacy potential

#### Limitations

- High circuit depth
- Requires careful parameter tuning
- Sensitive to noise
- May be overparametrized

### Data Re-uploading Embedding

Multiple encoding layers with variational parameters for increased expressivity.

#### How it Works

```python
from quantum_data_embedding_suite.embeddings import DataReuploadingEmbedding

# Create data re-uploading embedding
embedding = DataReuploadingEmbedding(
    n_qubits=4,
    n_layers=3,
    rotation_gates=['RY', 'RZ'],
    entangling_strategy='linear',
    trainable=True
)

# Embed data with trainable parameters
data_point = np.array([0.1, 0.5, -0.3, 0.8])
circuit = embedding.embed(data_point)
```

#### Mathematical Representation

For $L$ layers:

$$U_{DR}(\mathbf{x}, \boldsymbol{\theta}) = \prod_{l=1}^{L} U_{ent}(\theta_l) U_{enc}(\mathbf{x})$$

Where $U_{enc}$ encodes data and $U_{ent}$ creates entanglement with trainable parameters.

#### Parameters

- **`n_qubits`**: Number of qubits
- **`n_layers`**: Number of encoding/entangling layers
- **`rotation_gates`**: Types of rotation gates to use
- **`entangling_strategy`**: How to create entanglement
- **`trainable`**: Whether parameters are trainable

#### Use Cases

- **Complex datasets** requiring high expressivity
- **Variational quantum algorithms**
- **When single encoding is insufficient**
- **Trainable quantum circuits**

#### Advantages

- High expressivity
- Trainable parameters
- Flexible architecture
- Can overcome barren plateaus

#### Limitations

- High parameter count
- Prone to overfitting
- Requires optimization
- Higher circuit depth

### Hamiltonian Embedding

Physics-inspired embeddings using problem-specific Hamiltonians.

#### How it Works

```python
from quantum_data_embedding_suite.embeddings import HamiltonianEmbedding

# Create Hamiltonian embedding
embedding = HamiltonianEmbedding(
    n_qubits=4,
    hamiltonian_type='heisenberg',
    evolution_time=1.0,
    trotter_steps=10
)

# Embed data through Hamiltonian evolution
data_point = np.array([0.1, 0.5, -0.3, 0.8])
circuit = embedding.embed(data_point)
```

#### Mathematical Representation

Data-dependent Hamiltonian evolution:

$$U_H(\mathbf{x}, t) = \exp(-i H(\mathbf{x}) t)$$

Where $H(\mathbf{x})$ is a data-dependent Hamiltonian.

#### Built-in Hamiltonians

- **Heisenberg**: $H = \sum_i J_i(\mathbf{x}) \sigma_i^x \sigma_{i+1}^x + \sigma_i^y \sigma_{i+1}^y + \sigma_i^z \sigma_{i+1}^z$
- **Ising**: $H = \sum_i h_i(\mathbf{x}) \sigma_i^z + \sum_{i,j} J_{ij}(\mathbf{x}) \sigma_i^z \sigma_j^z$
- **Custom**: User-defined Hamiltonian

#### Parameters

- **`n_qubits`**: Number of qubits
- **`hamiltonian_type`**: Type of Hamiltonian
- **`evolution_time`**: Total evolution time
- **`trotter_steps`**: Number of Trotter steps
- **`coupling_map`**: Qubit coupling topology

#### Use Cases

- **Physics-inspired problems**
- **Time evolution simulations**
- **Problem-specific encodings**
- **Research applications**

## Choosing the Right Embedding

### Decision Matrix

| Dataset Characteristics | Recommended Embedding | Reason |
|------------------------|----------------------|---------|
| Small, continuous features | Angle | Simple and effective |
| High-dimensional, normalized | Amplitude | Information efficient |
| Complex feature interactions | IQP | Captures correlations |
| Requires high expressivity | Data Re-uploading | Trainable parameters |
| Physics-inspired | Hamiltonian | Domain knowledge |

### Performance Considerations

#### Circuit Depth

```python
# Compare circuit depths
embeddings = {
    'angle': AngleEmbedding(n_qubits=4),
    'amplitude': AmplitudeEmbedding(n_qubits=4),
    'iqp': IQPEmbedding(n_qubits=4, depth=2),
    'data_reuploading': DataReuploadingEmbedding(n_qubits=4, n_layers=3)
}

for name, embedding in embeddings.items():
    circuit = embedding.embed(np.random.randn(4))
    print(f"{name}: depth = {circuit.depth()}")
```

#### Gate Count

Monitor the total number of gates for NISQ device compatibility:

```python
def analyze_embedding(embedding, data_point):
    circuit = embedding.embed(data_point)
    return {
        'depth': circuit.depth(),
        'size': circuit.size(),
        'n_gates': circuit.count_ops()
    }
```

## Advanced Usage

### Custom Embeddings

Create custom embedding classes:

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
            
        return circuit
```

### Hybrid Embeddings

Combine multiple embedding types:

```python
class HybridEmbedding(BaseEmbedding):
    def __init__(self, n_qubits):
        super().__init__(n_qubits)
        self.angle_embedding = AngleEmbedding(n_qubits // 2)
        self.amplitude_embedding = AmplitudeEmbedding(n_qubits // 2)
    
    def _build_circuit(self, data_point):
        # Split data between embeddings
        mid = len(data_point) // 2
        
        # Apply different embeddings to different qubits
        circuit1 = self.angle_embedding.embed(data_point[:mid])
        circuit2 = self.amplitude_embedding.embed(data_point[mid:])
        
        # Combine circuits
        return combine_circuits(circuit1, circuit2)
```

### Embedding Optimization

Optimize embedding parameters for your specific problem:

```python
from quantum_data_embedding_suite.optimization import optimize_embedding

# Optimize embedding parameters
best_params = optimize_embedding(
    embedding_type="data_reuploading",
    X_train=X_train,
    y_train=y_train,
    metric="expressibility",
    n_trials=100
)

# Create optimized embedding
optimized_embedding = DataReuploadingEmbedding(**best_params)
```

## Best Practices

### Data Preprocessing

1. **Normalize features** for angle embeddings
2. **Scale to [0, 2π]** for optimal angle encoding
3. **Normalize vectors** for amplitude embedding
4. **Handle missing values** before embedding

### Circuit Design

1. **Start simple** with angle embedding
2. **Gradually increase complexity** as needed
3. **Monitor circuit depth** for NISQ compatibility
4. **Use entanglement strategically**

### Performance Monitoring

```python
from quantum_data_embedding_suite.metrics import embedding_metrics

# Monitor embedding quality
metrics = embedding_metrics(
    embedding=embedding,
    X=X_train,
    metrics=['expressibility', 'trainability', 'effective_dimension']
)

print(f"Expressibility: {metrics['expressibility']:.3f}")
print(f"Trainability: {metrics['trainability']:.3f}")
```

### Troubleshooting

#### Common Issues

1. **NaN values**: Check data normalization
2. **Poor performance**: Try different embedding types
3. **High circuit depth**: Reduce complexity or use simpler embedding
4. **Memory errors**: Use batch processing or fewer qubits

#### Debugging Tools

```python
# Visualize embedding circuit
from quantum_data_embedding_suite.utils import visualize_circuit

circuit = embedding.embed(data_point)
visualize_circuit(circuit)

# Check embedding properties
embedding.analyze(verbose=True)
```

## Further Reading

- [Quantum Kernel Methods](kernels.md)
- [Embedding Metrics](metrics.md)
- [Optimization Strategies](../tutorials/optimization.ipynb)
- [Real QPU Usage](../tutorials/real_qpu.ipynb)
