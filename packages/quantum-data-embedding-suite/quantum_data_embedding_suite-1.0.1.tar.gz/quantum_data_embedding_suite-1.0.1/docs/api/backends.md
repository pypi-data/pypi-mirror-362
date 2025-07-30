# Backends API

This page documents the quantum computing backend implementations and utilities.

## Backend Base Classes

### BaseBackend

::: quantum_data_embedding_suite.backends.BaseBackend
    options:
      show_source: true
      show_root_heading: true
      show_object_full_path: false

## Qiskit Backend

### QiskitBackend

::: quantum_data_embedding_suite.backends.QiskitBackend
    options:
      show_source: true
      show_root_heading: true
      show_object_full_path: false

## PennyLane Backend

### PennyLaneBackend

::: quantum_data_embedding_suite.backends.PennyLaneBackend
    options:
      show_source: true
      show_root_heading: true
      show_object_full_path: false

## Backend Utilities

### get_available_backends

::: quantum_data_embedding_suite.backends.get_backend
    options:
      show_source: true
      show_root_heading: true
      show_object_full_path: false

### create_backend

::: quantum_data_embedding_suite.backends.BACKEND_REGISTRY
    options:
      show_source: true
      show_root_heading: true
      show_object_full_path: false

## Usage Examples

### Basic Backend Creation

```python
from quantum_data_embedding_suite.backends import (
    QiskitBackend, PennyLaneBackend, create_backend
)

# Create Qiskit backend
qiskit_backend = QiskitBackend(
    device_name="qasm_simulator",
    shots=1024,
    seed=42
)

# Create PennyLane backend
pennylane_backend = PennyLaneBackend(
    device_name="default.qubit",
    shots=1024,
    seed=42
)

# Create backend using factory function
backend = create_backend(
    backend_type="qiskit",
    device_name="aer_simulator",
    shots=2048
)

print(f"Backend type: {type(backend).__name__}")
print(f"Device: {backend.device_name}")
print(f"Shots: {backend.shots}")
```

### Backend Discovery and Selection

```python
from quantum_data_embedding_suite.backends import get_available_backends, backend_info

# Discover available backends
available = get_available_backends()

print("Available Backends:")
for backend_type, devices in available.items():
    print(f"\n{backend_type.upper()}:")
    for device in devices:
        info = backend_info(backend_type, device)
        print(f"  - {device}: {info.get('description', 'No description')}")
        
        # Show device capabilities
        if 'capabilities' in info:
            caps = info['capabilities']
            print(f"    Qubits: {caps.get('max_qubits', 'Unknown')}")
            print(f"    Noise: {'Yes' if caps.get('supports_noise') else 'No'}")
            print(f"    GPU: {'Yes' if caps.get('gpu_support') else 'No'}")

# Select optimal backend for task
def select_optimal_backend(n_qubits, require_noise=False, prefer_gpu=False):
    """Select the best available backend for given requirements"""
    
    available = get_available_backends()
    best_backend = None
    best_score = -1
    
    for backend_type, devices in available.items():
        for device in devices:
            info = backend_info(backend_type, device)
            caps = info.get('capabilities', {})
            
            # Check requirements
            if caps.get('max_qubits', 0) < n_qubits:
                continue
                
            if require_noise and not caps.get('supports_noise', False):
                continue
            
            # Calculate score
            score = 0
            score += caps.get('max_qubits', 0) * 0.1  # More qubits is better
            score += 10 if caps.get('supports_noise', False) else 0
            score += 5 if caps.get('gpu_support', False) and prefer_gpu else 0
            score += 3 if backend_type == 'qiskit' else 0  # Slight preference for Qiskit
            
            if score > best_score:
                best_score = score
                best_backend = (backend_type, device)
    
    return best_backend

# Find optimal backend
optimal = select_optimal_backend(n_qubits=6, require_noise=False, prefer_gpu=True)
if optimal:
    backend_type, device = optimal
    backend = create_backend(backend_type, device)
    print(f"\nSelected optimal backend: {backend_type}/{device}")
else:
    print("\nNo suitable backend found")
```

### Advanced Configuration

```python
# Advanced Qiskit configuration
from qiskit import IBMQ
from qiskit.providers.aer.noise import NoiseModel
from qiskit.providers.aer.noise.errors import pauli_error, depolarizing_error

# Configure with noise model
def create_noisy_qiskit_backend():
    """Create Qiskit backend with realistic noise"""
    
    # Create noise model
    noise_model = NoiseModel()
    
    # Add depolarizing error to gates
    error_1q = depolarizing_error(0.001, 1)  # 0.1% error rate
    error_2q = depolarizing_error(0.01, 2)   # 1% error rate
    
    noise_model.add_all_qubit_quantum_error(error_1q, ['u1', 'u2', 'u3'])
    noise_model.add_all_qubit_quantum_error(error_2q, ['cx'])
    
    # Add measurement error
    from qiskit.providers.aer.noise.errors import ReadoutError
    readout_error = ReadoutError([[0.98, 0.02], [0.03, 0.97]])
    noise_model.add_all_qubit_readout_error(readout_error)
    
    # Create backend with noise
    backend = QiskitBackend(
        device_name="aer_simulator",
        shots=2048,
        noise_model=noise_model,
        basis_gates=noise_model.basis_gates,
        coupling_map=None
    )
    
    return backend

noisy_backend = create_noisy_qiskit_backend()

# Advanced PennyLane configuration
import pennylane as qml

def create_advanced_pennylane_backend():
    """Create PennyLane backend with advanced features"""
    
    # Create device with custom configuration
    device = qml.device(
        'default.qubit',
        wires=8,
        shots=1024,
        analytic=False,  # Use sampling
        seed=42
    )
    
    backend = PennyLaneBackend(
        device=device,
        differentiable=True,
        interface='autograd'
    )
    
    return backend

advanced_pennylane = create_advanced_pennylane_backend()
```

### Backend Performance Benchmarking

```python
import time
import numpy as np
from quantum_data_embedding_suite.embeddings import AngleEmbedding

def benchmark_backend(backend, embedding, X, n_trials=10):
    """Benchmark backend performance"""
    
    times = []
    
    for trial in range(n_trials):
        start_time = time.time()
        
        try:
            # Execute embedding on multiple data points
            for x in X[:5]:  # Test with 5 data points
                circuit = embedding.embed(x)
                backend.execute(circuit)
            
            end_time = time.time()
            times.append(end_time - start_time)
            
        except Exception as e:
            print(f"Error in trial {trial}: {e}")
            continue
    
    if not times:
        return None
    
    results = {
        'mean_time': np.mean(times),
        'std_time': np.std(times),
        'min_time': np.min(times),
        'max_time': np.max(times),
        'n_successful_trials': len(times),
        'throughput': len(X[:5]) / np.mean(times)  # circuits per second
    }
    
    return results

# Benchmark different backends
embedding = AngleEmbedding(n_qubits=4)
X = np.random.randn(10, 4)

backends_to_test = {
    'qiskit_simulator': QiskitBackend("qasm_simulator", shots=1024),
    'pennylane_default': PennyLaneBackend("default.qubit", shots=1024)
}

benchmark_results = {}

print("Backend Benchmarking Results:")
print("=" * 50)

for name, backend in backends_to_test.items():
    print(f"\nTesting {name}...")
    
    results = benchmark_backend(backend, embedding, X)
    
    if results:
        benchmark_results[name] = results
        
        print(f"  Mean execution time: {results['mean_time']:.4f}s")
        print(f"  Std deviation: {results['std_time']:.4f}s")
        print(f"  Throughput: {results['throughput']:.2f} circuits/s")
        print(f"  Successful trials: {results['n_successful_trials']}/10")
    else:
        print(f"  Benchmark failed for {name}")

# Find fastest backend
if benchmark_results:
    fastest = min(benchmark_results.items(), key=lambda x: x[1]['mean_time'])
    print(f"\nFastest backend: {fastest[0]} ({fastest[1]['mean_time']:.4f}s)")
```

## Hardware Integration

### Real Quantum Hardware Access

```python
from qiskit import IBMQ
from qiskit.providers.ibmq import least_busy

def setup_ibm_hardware_backend(hub=None, group=None, project=None):
    """Setup connection to IBM Quantum hardware"""
    
    try:
        # Load account (assumes IBMQ account is saved)
        IBMQ.load_account()
        
        # Get provider
        if hub and group and project:
            provider = IBMQ.get_provider(hub=hub, group=group, project=project)
        else:
            provider = IBMQ.get_provider()
        
        # Get available backends
        backends = provider.backends(
            filters=lambda x: x.configuration().n_qubits >= 5 and 
                             not x.configuration().simulator and 
                             x.status().operational
        )
        
        if not backends:
            print("No operational quantum hardware available")
            return None
        
        # Select least busy backend
        least_busy_backend = least_busy(backends)
        
        # Create our backend wrapper
        hardware_backend = QiskitHardware(
            provider=provider,
            backend_name=least_busy_backend.name(),
            shots=1024,
            optimization_level=2
        )
        
        print(f"Connected to {least_busy_backend.name()}")
        print(f"Qubits: {least_busy_backend.configuration().n_qubits}")
        print(f"Queue length: {least_busy_backend.status().pending_jobs}")
        
        return hardware_backend
        
    except Exception as e:
        print(f"Failed to setup IBM hardware backend: {e}")
        return None

# Setup hardware backend
hardware_backend = setup_ibm_hardware_backend()

if hardware_backend:
    # Execute on real quantum hardware
    embedding = AngleEmbedding(n_qubits=4)
    test_data = np.array([0.1, 0.2, 0.3, 0.4])
    
    circuit = embedding.embed(test_data)
    result = hardware_backend.execute(circuit)
    
    print(f"Hardware execution result: {result}")
```

### Error Mitigation

```python
from qiskit.ignis.mitigation.measurement import complete_meas_cal, CompleteMeasFitter

def create_error_mitigated_backend(base_backend):
    """Create backend with measurement error mitigation"""
    
    class ErrorMitigatedBackend:
        def __init__(self, base_backend):
            self.base_backend = base_backend
            self.calibration_fitter = None
            self._setup_calibration()
        
        def _setup_calibration(self):
            """Setup measurement error calibration"""
            try:
                # Create calibration circuits
                n_qubits = 5  # Assume 5 qubits for calibration
                qubits = list(range(n_qubits))
                
                cal_circuits, state_labels = complete_meas_cal(
                    qubit_list=qubits,
                    circlabel='cal'
                )
                
                # Execute calibration circuits
                cal_results = []
                for circuit in cal_circuits:
                    result = self.base_backend.execute(circuit)
                    cal_results.append(result)
                
                # Create fitter
                self.calibration_fitter = CompleteMeasFitter(
                    cal_results, state_labels, circlabel='cal'
                )
                
                print("Measurement error calibration complete")
                
            except Exception as e:
                print(f"Calibration failed: {e}")
                self.calibration_fitter = None
        
        def execute(self, circuit):
            """Execute circuit with error mitigation"""
            # Execute original circuit
            raw_result = self.base_backend.execute(circuit)
            
            # Apply error mitigation if calibration available
            if self.calibration_fitter:
                try:
                    mitigated_result = self.calibration_fitter.filter.apply(raw_result)
                    return mitigated_result
                except Exception as e:
                    print(f"Error mitigation failed: {e}")
                    return raw_result
            
            return raw_result
        
        def __getattr__(self, name):
            """Delegate other attributes to base backend"""
            return getattr(self.base_backend, name)
    
    return ErrorMitigatedBackend(base_backend)

# Create error-mitigated backend
if hardware_backend:
    mitigated_backend = create_error_mitigated_backend(hardware_backend)
```

## Backend Comparison and Analysis

### Feature Comparison Matrix

```python
def compare_backend_features():
    """Compare features across different backends"""
    
    backends = [
        ('qiskit', 'qasm_simulator'),
        ('qiskit', 'statevector_simulator'),
        ('pennylane', 'default.qubit'),
        ('pennylane', 'default.mixed'),
    ]
    
    features = [
        'max_qubits', 'supports_noise', 'gpu_support', 'differentiable',
        'supports_measurements', 'supports_conditional', 'parallelizable'
    ]
    
    comparison_matrix = []
    
    for backend_type, device in backends:
        try:
            info = backend_info(backend_type, device)
            caps = info.get('capabilities', {})
            
            row = [f"{backend_type}/{device}"]
            for feature in features:
                value = caps.get(feature, 'Unknown')
                if isinstance(value, bool):
                    value = '✓' if value else '✗'
                row.append(str(value))
            
            comparison_matrix.append(row)
            
        except Exception as e:
            print(f"Error getting info for {backend_type}/{device}: {e}")
            continue
    
    # Create DataFrame for easy viewing
    import pandas as pd
    
    columns = ['Backend'] + features
    df = pd.DataFrame(comparison_matrix, columns=columns)
    
    return df

# Generate comparison
comparison_df = compare_backend_features()
print("Backend Feature Comparison:")
print(comparison_df.to_string(index=False))
```

### Backend Recommendations

```python
def recommend_backend(use_case, requirements=None):
    """Recommend optimal backend for specific use case"""
    
    if requirements is None:
        requirements = {}
    
    recommendations = {
        'development': {
            'primary': ('qiskit', 'qasm_simulator'),
            'alternative': ('pennylane', 'default.qubit'),
            'reason': 'Fast execution, good debugging tools'
        },
        
        'research': {
            'primary': ('qiskit', 'statevector_simulator'),
            'alternative': ('pennylane', 'default.qubit'),
            'reason': 'Exact results, noise-free environment'
        },
        
        'machine_learning': {
            'primary': ('pennylane', 'default.qubit'),
            'alternative': ('qiskit', 'qasm_simulator'),
            'reason': 'Automatic differentiation, ML integration'
        },
        
        'noise_modeling': {
            'primary': ('qiskit', 'aer_simulator'),
            'alternative': ('pennylane', 'default.mixed'),
            'reason': 'Advanced noise models, realistic simulation'
        },
        
        'production': {
            'primary': ('qiskit', 'ibmq_hardware'),
            'alternative': ('qiskit', 'aer_simulator'),
            'reason': 'Real quantum hardware access'
        },
        
        'large_scale': {
            'primary': ('qiskit', 'aer_simulator_gpu'),
            'alternative': ('pennylane', 'lightning.gpu'),
            'reason': 'GPU acceleration, high qubit count'
        }
    }
    
    if use_case not in recommendations:
        return {
            'recommendation': 'No specific recommendation',
            'suggested_backends': [('qiskit', 'qasm_simulator'), ('pennylane', 'default.qubit')],
            'reason': 'General-purpose backends suitable for most tasks'
        }
    
    rec = recommendations[use_case]
    
    # Check if recommended backends are available
    available = get_available_backends()
    
    primary_available = (rec['primary'][0] in available and 
                        rec['primary'][1] in available[rec['primary'][0]])
    
    alt_available = (rec['alternative'][0] in available and 
                    rec['alternative'][1] in available[rec['alternative'][0]])
    
    final_rec = {
        'use_case': use_case,
        'primary_recommendation': rec['primary'] if primary_available else None,
        'alternative_recommendation': rec['alternative'] if alt_available else None,
        'reason': rec['reason'],
        'requirements_met': True  # Could add requirement checking logic
    }
    
    return final_rec

# Get recommendations for different use cases
use_cases = ['development', 'research', 'machine_learning', 'production']

print("Backend Recommendations:")
print("=" * 50)

for use_case in use_cases:
    rec = recommend_backend(use_case)
    print(f"\n{use_case.upper()}:")
    
    if rec['primary_recommendation']:
        backend_type, device = rec['primary_recommendation']
        print(f"  Primary: {backend_type}/{device}")
    
    if rec['alternative_recommendation']:
        backend_type, device = rec['alternative_recommendation']
        print(f"  Alternative: {backend_type}/{device}")
    
    print(f"  Reason: {rec['reason']}")
```

## Custom Backend Development

### Creating Custom Backends

```python
from quantum_data_embedding_suite.backends.base import BaseBackend

class CustomQuantumBackend(BaseBackend):
    """Example custom quantum backend implementation"""
    
    def __init__(self, custom_param=None, **kwargs):
        super().__init__(**kwargs)
        self.custom_param = custom_param
        self._setup_custom_features()
    
    def _setup_custom_features(self):
        """Setup custom backend features"""
        self.custom_features = {
            'special_gates': True,
            'advanced_optimization': True,
            'custom_metrics': True
        }
        print(f"Custom backend initialized with param: {self.custom_param}")
    
    def execute(self, circuit, **kwargs):
        """Execute quantum circuit with custom processing"""
        
        # Pre-processing
        optimized_circuit = self._optimize_circuit(circuit)
        
        # Execute (this would interface with actual quantum hardware/simulator)
        result = self._execute_circuit(optimized_circuit, **kwargs)
        
        # Post-processing
        processed_result = self._post_process_result(result)
        
        return processed_result
    
    def _optimize_circuit(self, circuit):
        """Apply custom circuit optimizations"""
        # Implement custom optimization logic
        print(f"Applying custom optimization to circuit with {circuit.depth()} depth")
        
        # Placeholder optimization
        return circuit
    
    def _execute_circuit(self, circuit, **kwargs):
        """Execute the circuit (placeholder implementation)"""
        # This would interface with actual quantum execution
        # For demonstration, return mock results
        
        n_qubits = circuit.num_qubits
        shots = kwargs.get('shots', self.shots)
        
        # Generate mock measurement results
        import random
        results = {}
        
        for _ in range(shots):
            # Generate random bit string
            bitstring = ''.join([str(random.randint(0, 1)) for _ in range(n_qubits)])
            results[bitstring] = results.get(bitstring, 0) + 1
        
        return results
    
    def _post_process_result(self, result):
        """Apply custom post-processing to results"""
        # Implement custom result processing
        print("Applying custom post-processing")
        
        # Example: Add metadata
        processed = {
            'counts': result,
            'metadata': {
                'backend_type': 'custom',
                'custom_param': self.custom_param,
                'post_processed': True
            }
        }
        
        return processed
    
    def get_backend_info(self):
        """Return backend information"""
        info = super().get_backend_info()
        info.update({
            'custom_features': self.custom_features,
            'custom_param': self.custom_param
        })
        return info

# Use custom backend
custom_backend = CustomQuantumBackend(
    custom_param="special_mode",
    shots=2048,
    seed=42
)

# Test custom backend
embedding = AngleEmbedding(n_qubits=3)
test_data = np.array([0.1, 0.2, 0.3])

circuit = embedding.embed(test_data)
result = custom_backend.execute(circuit)

print("\nCustom Backend Result:")
print(f"Counts: {result['counts']}")
print(f"Metadata: {result['metadata']}")
```

### Backend Plugin System

```python
class BackendRegistry:
    """Registry for custom backends"""
    
    _backends = {}
    
    @classmethod
    def register(cls, name, backend_class):
        """Register a custom backend"""
        cls._backends[name] = backend_class
        print(f"Registered backend: {name}")
    
    @classmethod
    def get_backend(cls, name, **kwargs):
        """Get registered backend instance"""
        if name not in cls._backends:
            raise ValueError(f"Backend '{name}' not registered")
        
        backend_class = cls._backends[name]
        return backend_class(**kwargs)
    
    @classmethod
    def list_backends(cls):
        """List all registered backends"""
        return list(cls._backends.keys())

# Register custom backend
BackendRegistry.register('custom', CustomQuantumBackend)

# Use registered backend
registered_backend = BackendRegistry.get_backend('custom', custom_param="registry_test")

print(f"Available backends: {BackendRegistry.list_backends()}")
```

## Further Reading

- [Backends User Guide](../user_guide/backends.md)
- [Hardware Integration Tutorial](../tutorials/hardware_integration.ipynb)
- [Performance Optimization Guide](../examples/optimization.md)
