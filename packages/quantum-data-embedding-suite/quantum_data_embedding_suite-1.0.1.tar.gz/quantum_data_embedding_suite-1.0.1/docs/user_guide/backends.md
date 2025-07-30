# Backends

This guide covers the quantum computing backends available in the Quantum Data Embedding Suite.

## Overview

Backends provide the interface between your quantum embeddings and actual quantum computation. The Quantum Data Embedding Suite supports multiple backends to ensure flexibility and compatibility with different quantum computing platforms.

## Available Backends

### Qiskit Backend

The default backend using IBM's Qiskit framework.

#### Basic Usage

```python
from quantum_data_embedding_suite.backends import QiskitBackend

# Create Qiskit backend
backend = QiskitBackend(
    device="aer_simulator",
    shots=1024,
    optimization_level=1
)

# Use with embedding
from quantum_data_embedding_suite import QuantumEmbeddingPipeline

pipeline = QuantumEmbeddingPipeline(
    embedding_type="angle",
    n_qubits=4,
    backend=backend
)
```

#### Simulator Options

**Statevector Simulator**

```python
backend = QiskitBackend(
    device="statevector_simulator",
    shots=None,  # Exact computation
    precision="double"
)
```

**Noisy Simulator**

```python
from qiskit.providers.aer.noise import NoiseModel

# Create noise model
noise_model = NoiseModel.from_backend(ibm_backend)

backend = QiskitBackend(
    device="aer_simulator",
    shots=1024,
    noise_model=noise_model
)
```

**GPU Simulator**

```python
backend = QiskitBackend(
    device="aer_simulator_gpu",
    shots=1024,
    gpu=True,
    max_memory_mb=8192
)
```

#### Real Hardware

**IBM Quantum Devices**

```python
from qiskit import IBMQ

# Load IBM Quantum account
IBMQ.load_account()
provider = IBMQ.get_provider(hub='ibm-q')

# Select device
device = provider.get_backend('ibmq_qasm_simulator')

backend = QiskitBackend(
    device=device,
    shots=1024,
    optimization_level=3  # Maximum optimization for real hardware
)
```

#### Configuration Options

```python
backend = QiskitBackend(
    device="aer_simulator",
    shots=1024,
    optimization_level=2,
    seed_simulator=42,
    memory=True,  # Return individual shot results
    max_credits=10,  # For IBM Quantum devices
    coupling_map=None,  # Custom coupling map
    basis_gates=None,  # Custom gate set
    initial_layout=None,  # Custom qubit mapping
    layout_method="trivial",  # Layout optimization
    routing_method="stochastic",  # Routing optimization
    translation_method="translator",  # Gate translation
    scheduling_method=None,  # Instruction scheduling
    instruction_durations=None,  # Gate durations
    dt=None,  # System time unit
    approximation_degree=1.0  # Approximation level for synthesis
)
```

### PennyLane Backend

Alternative backend using Xanadu's PennyLane framework.

#### Basic Usage

```python
from quantum_data_embedding_suite.backends import PennyLaneBackend

# Create PennyLane backend
backend = PennyLaneBackend(
    device="default.qubit",
    shots=1024,
    wires=4
)

# Use with embedding
pipeline = QuantumEmbeddingPipeline(
    embedding_type="amplitude",
    n_qubits=4,
    backend=backend
)
```

#### Device Options

**Default Simulator**

```python
backend = PennyLaneBackend(
    device="default.qubit",
    shots=None,  # Exact computation
    analytic=True
)
```

**Lightning Simulator**

```python
backend = PennyLaneBackend(
    device="lightning.qubit",
    shots=1024,
    c_dtype=np.complex128
)
```

**Cirq Integration**

```python
backend = PennyLaneBackend(
    device="cirq.simulator",
    shots=1024,
    wires=4
)
```

**Hardware Providers**

```python
# AWS Braket
backend = PennyLaneBackend(
    device="braket.aws.qubit",
    device_arn="arn:aws:braket::device/qpu/ionq/ionQdevice",
    shots=1000,
    wires=4
)

# IonQ
backend = PennyLaneBackend(
    device="ionq.qpu",
    token="your_ionq_token",
    shots=1024,
    wires=4
)
```

#### Automatic Differentiation

```python
# Enable automatic differentiation
backend = PennyLaneBackend(
    device="default.qubit",
    diff_method="backprop",  # or "parameter-shift", "finite-diff"
    gradient_kwargs={"h": 1e-7}
)

# Use with trainable embeddings
from quantum_data_embedding_suite.embeddings import DataReuploadingEmbedding

embedding = DataReuploadingEmbedding(
    n_qubits=4,
    n_layers=3,
    trainable=True
)

pipeline = QuantumEmbeddingPipeline(
    embedding=embedding,
    backend=backend
)
```

## Backend Comparison

### Feature Matrix

| Feature | Qiskit | PennyLane |
|---------|--------|-----------|
| Simulators | ✅ Comprehensive | ✅ Good coverage |
| Real Hardware | ✅ IBM Quantum | ✅ Multiple providers |
| Noise Models | ✅ Advanced | ✅ Basic |
| Optimization | ✅ Advanced | ✅ Basic |
| Auto-diff | ❌ Limited | ✅ Native |
| GPU Support | ✅ Native | ✅ Via plugins |
| Hybrid Algorithms | ✅ Good | ✅ Excellent |

### Performance Comparison

```python
import time
import numpy as np

def benchmark_backends():
    X = np.random.randn(100, 4)
    
    backends = {
        "qiskit_statevector": QiskitBackend(device="statevector_simulator"),
        "qiskit_aer": QiskitBackend(device="aer_simulator", shots=1024),
        "pennylane_default": PennyLaneBackend(device="default.qubit"),
        "pennylane_lightning": PennyLaneBackend(device="lightning.qubit")
    }
    
    results = {}
    
    for name, backend in backends.items():
        pipeline = QuantumEmbeddingPipeline(
            embedding_type="angle",
            n_qubits=4,
            backend=backend
        )
        
        start_time = time.time()
        K = pipeline.fit_transform(X[:20])  # Small subset for timing
        end_time = time.time()
        
        results[name] = {
            "time": end_time - start_time,
            "accuracy": np.trace(K) / len(K)  # Rough accuracy measure
        }
    
    return results

# Run benchmark
benchmark_results = benchmark_backends()
```

## Custom Backends

### Creating Custom Backend

```python
from quantum_data_embedding_suite.backends import BaseBackend

class CustomBackend(BaseBackend):
    def __init__(self, custom_param=1.0):
        super().__init__()
        self.custom_param = custom_param
        
    def execute_circuit(self, circuit, shots=None):
        """Execute quantum circuit and return results"""
        # Implement custom execution logic
        # This is where you'd interface with your quantum computing platform
        
        # Example: Convert to your platform's circuit format
        custom_circuit = self._convert_circuit(circuit)
        
        # Execute on your platform
        results = your_platform.execute(custom_circuit, shots=shots)
        
        # Convert results to standard format
        return self._convert_results(results)
    
    def get_statevector(self, circuit):
        """Get exact statevector (for simulators)"""
        # Implement statevector computation
        pass
    
    def get_fidelity(self, circuit1, circuit2):
        """Compute fidelity between two circuits"""
        # Implement fidelity computation
        pass
    
    def _convert_circuit(self, circuit):
        """Convert from standard format to backend format"""
        # Implement circuit conversion
        pass
    
    def _convert_results(self, results):
        """Convert results to standard format"""
        # Implement result conversion
        pass
```

### Backend Plugin System

```python
# Register custom backend
from quantum_data_embedding_suite.backends import register_backend

@register_backend("my_custom_backend")
class MyCustomBackend(BaseBackend):
    def __init__(self, **kwargs):
        super().__init__()
        # Custom initialization
    
    def execute_circuit(self, circuit, shots=None):
        # Custom implementation
        pass

# Use registered backend
pipeline = QuantumEmbeddingPipeline(
    embedding_type="angle",
    n_qubits=4,
    backend="my_custom_backend"
)
```

## Backend Configuration

### Configuration Files

Create backend configuration files for easy setup:

```yaml
# backends.yaml
qiskit:
  default:
    device: "aer_simulator"
    shots: 1024
    optimization_level: 1
    
  hardware:
    device: "ibmq_qasm_simulator"
    shots: 8192
    optimization_level: 3
    
  gpu:
    device: "aer_simulator_gpu"
    shots: 1024
    gpu: true

pennylane:
  default:
    device: "default.qubit"
    shots: 1024
    
  lightning:
    device: "lightning.qubit"
    shots: 1024
```

```python
# Load configuration
from quantum_data_embedding_suite.config import load_backend_config

config = load_backend_config("backends.yaml")
backend = config.create_backend("qiskit.hardware")
```

### Environment Variables

```bash
# Set default backend
export QDES_DEFAULT_BACKEND=qiskit
export QDES_DEFAULT_SHOTS=1024

# IBM Quantum credentials
export IBMQ_TOKEN=your_token_here
export IBMQ_URL=https://auth.quantum-computing.ibm.com/api

# AWS Braket credentials
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_DEFAULT_REGION=us-east-1
```

## Hardware-Specific Considerations

### IBM Quantum

#### Device Selection

```python
from qiskit import IBMQ
from quantum_data_embedding_suite.utils import select_best_device

# Automatically select best available device
IBMQ.load_account()
provider = IBMQ.get_provider()

best_device = select_best_device(
    provider=provider,
    n_qubits=4,
    criteria=["queue_length", "gate_error", "readout_error"]
)

backend = QiskitBackend(device=best_device, shots=1024)
```

#### Calibration Data

```python
# Use device calibration data
device = provider.get_backend('ibmq_5_yorktown')
properties = device.properties()

# Configure backend with calibration
backend = QiskitBackend(
    device=device,
    shots=1024,
    use_calibration=True,
    properties=properties
)
```

#### Error Mitigation

```python
from qiskit.ignis.mitigation import CompleteMeasFitter

# Measurement error mitigation
backend = QiskitBackend(
    device=device,
    shots=1024,
    measurement_error_mitigation=True,
    mitigation_method="complete"
)
```

### AWS Braket

```python
# Configure AWS Braket backend
import boto3

backend = PennyLaneBackend(
    device="braket.aws.qubit",
    device_arn="arn:aws:braket::device/qpu/ionq/ionQdevice",
    shots=1000,
    aws_session=boto3.Session(),
    poll_timeout_seconds=86400
)
```

### IonQ

```python
# Configure IonQ backend
backend = PennyLaneBackend(
    device="ionq.qpu",
    token="your_ionq_token",
    shots=1024,
    wires=4,
    target="qpu"  # or "simulator"
)
```

## Optimization and Performance

### Circuit Optimization

```python
# Enable circuit optimization
backend = QiskitBackend(
    device="aer_simulator",
    shots=1024,
    optimization_level=3,  # Maximum optimization
    optimization_passes=[
        "RemoveRedundantGates",
        "CommutativeCancellation",
        "OptimizeSwapBeforeNativeGates"
    ]
)
```

### Parallel Execution

```python
# Enable parallel execution
backend = QiskitBackend(
    device="aer_simulator",
    shots=1024,
    max_parallel_threads=4,
    max_parallel_experiments=10
)
```

### Memory Management

```python
# Configure memory usage
backend = QiskitBackend(
    device="aer_simulator",
    shots=1024,
    max_memory_mb=8192,
    memory_mapping=True
)
```

### Batch Processing

```python
# Efficient batch processing
class BatchBackend:
    def __init__(self, base_backend, batch_size=100):
        self.base_backend = base_backend
        self.batch_size = batch_size
    
    def execute_batch(self, circuits):
        results = []
        for i in range(0, len(circuits), self.batch_size):
            batch = circuits[i:i+self.batch_size]
            batch_results = self.base_backend.execute_circuits(batch)
            results.extend(batch_results)
        return results
```

## Error Handling and Debugging

### Error Handling

```python
from quantum_data_embedding_suite.backends import BackendError

try:
    backend = QiskitBackend(device="nonexistent_device")
    result = backend.execute_circuit(circuit)
except BackendError as e:
    print(f"Backend error: {e}")
    # Fallback to simulator
    backend = QiskitBackend(device="aer_simulator")
```

### Debugging Tools

```python
# Enable verbose logging
import logging
logging.basicConfig(level=logging.DEBUG)

backend = QiskitBackend(
    device="aer_simulator",
    shots=1024,
    verbose=True,
    log_level="DEBUG"
)

# Circuit inspection
circuit = embedding.embed(data_point)
print(f"Circuit depth: {circuit.depth()}")
print(f"Circuit gates: {circuit.count_ops()}")

# Backend diagnostics
diagnostics = backend.diagnose()
print(f"Backend status: {diagnostics['status']}")
print(f"Available memory: {diagnostics['memory_mb']} MB")
```

### Performance Monitoring

```python
from quantum_data_embedding_suite.monitoring import BackendMonitor

# Monitor backend performance
monitor = BackendMonitor(backend)

with monitor:
    result = backend.execute_circuit(circuit)

print(f"Execution time: {monitor.execution_time:.3f}s")
print(f"Memory usage: {monitor.peak_memory_mb:.1f} MB")
print(f"Queue time: {monitor.queue_time:.3f}s")
```

## Best Practices

### Backend Selection

1. **Start with simulators** for development and testing
2. **Use GPU simulators** for large-scale experiments
3. **Choose hardware** based on your specific requirements
4. **Consider queue times** for real devices

### Performance Optimization

1. **Enable circuit optimization** for real hardware
2. **Use appropriate shot counts** (1024 for development, more for production)
3. **Batch operations** when possible
4. **Cache results** for repeated computations

### Error Mitigation

1. **Use error mitigation** on real hardware
2. **Monitor device calibration** data
3. **Implement fallback** strategies
4. **Validate results** with simulators

### Resource Management

1. **Monitor queue usage** on shared devices
2. **Optimize circuit depth** for NISQ devices
3. **Use appropriate memory** settings
4. **Clean up resources** after use

## Troubleshooting

### Common Issues

#### Connection Problems

**Issue**: Cannot connect to quantum device
**Solutions**:

- Check internet connection
- Verify API tokens
- Check device availability
- Use simulator as fallback

#### Performance Issues

**Issue**: Slow execution times
**Solutions**:

- Use GPU simulators
- Enable parallel execution
- Reduce circuit complexity
- Use approximate methods

#### Memory Errors

**Issue**: Out of memory errors
**Solutions**:

- Reduce number of qubits
- Use statevector simulator only when necessary
- Increase system memory
- Use batch processing

#### Accuracy Issues

**Issue**: Unexpected results
**Solutions**:

- Increase shot count
- Check circuit implementation
- Verify device calibration
- Compare with simulator results

### Getting Help

1. **Check device status** pages
2. **Review provider documentation**
3. **Test with simulators** first
4. **Contact provider support** for hardware issues
5. **Report bugs** to package maintainers

## Migration Guide

### From Qiskit to PennyLane

```python
# Qiskit version
qiskit_backend = QiskitBackend(device="aer_simulator", shots=1024)

# Equivalent PennyLane version
pennylane_backend = PennyLaneBackend(device="default.qubit", shots=1024)

# Update pipeline
pipeline = QuantumEmbeddingPipeline(
    embedding_type="angle",
    n_qubits=4,
    backend=pennylane_backend  # Changed backend
)
```

### Backend Abstraction

```python
def create_backend(backend_type, **kwargs):
    """Factory function for creating backends"""
    if backend_type == "qiskit":
        return QiskitBackend(**kwargs)
    elif backend_type == "pennylane":
        return PennyLaneBackend(**kwargs)
    else:
        raise ValueError(f"Unknown backend type: {backend_type}")

# Use abstraction
backend = create_backend("qiskit", device="aer_simulator", shots=1024)
```

## Further Reading

- [Quantum Embeddings](embeddings.md)
- [Real QPU Tutorial](../tutorials/real_qpu.ipynb)
- [Hardware Optimization](../examples/hardware_optimization.md)
- [Provider Documentation Links](../resources/providers.md)
