# Basic Examples

This page provides simple, self-contained examples to get you started with quantum data embedding.

## Example 1: Basic Quantum Kernel

Let's start with a simple example using the Iris dataset:

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from quantum_data_embedding_suite import QuantumEmbeddingPipeline

# Load and prepare data
X, y = load_iris(return_X_y=True)
X = StandardScaler().fit_transform(X)

# Create quantum embedding
pipeline = QuantumEmbeddingPipeline(
    embedding_type="angle",
    n_qubits=4,
    backend="qiskit",
    shots=1024
)

# Compute quantum kernel
K_quantum = pipeline.fit_transform(X)

# Visualize kernel matrix
plt.figure(figsize=(10, 8))
plt.imshow(K_quantum, cmap='viridis')
plt.colorbar(label='Kernel Value')
plt.title('Quantum Kernel Matrix - Iris Dataset')
plt.xlabel('Sample Index')
plt.ylabel('Sample Index')
plt.show()

print(f"Kernel matrix shape: {K_quantum.shape}")
print(f"Kernel values range: [{K_quantum.min():.3f}, {K_quantum.max():.3f}]")
```

## Example 2: Comparing Classical and Quantum Kernels

```python
from sklearn.metrics.pairwise import rbf_kernel
from quantum_data_embedding_suite.visualization import plot_kernel_comparison

# Generate sample data
np.random.seed(42)
X = np.random.randn(20, 4)

# Compute classical RBF kernel
K_classical = rbf_kernel(X, gamma=1.0)

# Compute quantum kernel
pipeline = QuantumEmbeddingPipeline(
    embedding_type="angle",
    n_qubits=4,
    backend="qiskit"
)
K_quantum = pipeline.fit_transform(X)

# Compare visually
plot_kernel_comparison(K_quantum, K_classical, "kernel_comparison.png")

# Compare numerically
correlation = np.corrcoef(K_quantum.flatten(), K_classical.flatten())[0, 1]
print(f"Correlation between quantum and classical kernels: {correlation:.3f}")
```

## Example 3: Classification with Quantum SVM

```python
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

# Load wine dataset
from sklearn.datasets import load_wine
X, y = load_wine(return_X_y=True)
X = StandardScaler().fit_transform(X)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# Create quantum embedding pipeline
pipeline = QuantumEmbeddingPipeline(
    embedding_type="angle",
    n_qubits=6,  # More qubits for wine dataset
    backend="qiskit"
)

# Compute quantum kernels
print("Computing quantum kernels...")
K_train = pipeline.fit_transform(X_train)
K_test = pipeline.transform(X_test)

# Train quantum SVM
quantum_svm = SVC(kernel='precomputed', C=1.0)
quantum_svm.fit(K_train, y_train)

# Make predictions
y_pred_quantum = quantum_svm.predict(K_test)
quantum_accuracy = accuracy_score(y_test, y_pred_quantum)

# Compare with classical SVM
classical_svm = SVC(kernel='rbf', C=1.0, gamma='scale')
classical_svm.fit(X_train, y_train)
y_pred_classical = classical_svm.predict(X_test)
classical_accuracy = accuracy_score(y_test, y_pred_classical)

print(f"Quantum SVM accuracy: {quantum_accuracy:.3f}")
print(f"Classical SVM accuracy: {classical_accuracy:.3f}")
print(f"Improvement: {quantum_accuracy - classical_accuracy:.3f}")

print("\nQuantum SVM Classification Report:")
print(classification_report(y_test, y_pred_quantum))
```

## Example 4: Embedding Quality Analysis

```python
from quantum_data_embedding_suite.metrics import expressibility, trainability

# Generate test data
X = np.random.randn(50, 4)

# Test different embeddings
embeddings = ["angle", "amplitude", "iqp"]
results = {}

for emb_type in embeddings:
    print(f"Analyzing {emb_type} embedding...")
    
    pipeline = QuantumEmbeddingPipeline(
        embedding_type=emb_type,
        n_qubits=4,
        backend="qiskit"
    )
    
    # Compute metrics
    metrics = pipeline.evaluate_embedding(X[:30])  # Use subset for speed
    
    results[emb_type] = metrics
    print(f"  Expressibility: {metrics['expressibility']:.3f}")
    print(f"  Trainability: {metrics['trainability']:.3f}")

# Plot comparison
import matplotlib.pyplot as plt

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Expressibility comparison
expr_values = [results[emb]['expressibility'] for emb in embeddings]
ax1.bar(embeddings, expr_values, color=['blue', 'green', 'red'])
ax1.set_ylabel('Expressibility')
ax1.set_title('Expressibility Comparison')
ax1.set_ylim(0, 1)

# Trainability comparison
train_values = [results[emb]['trainability'] for emb in embeddings]
ax2.bar(embeddings, train_values, color=['blue', 'green', 'red'])
ax2.set_ylabel('Trainability')
ax2.set_title('Trainability Comparison')

plt.tight_layout()
plt.show()
```

## Example 5: CLI Usage Examples

Here are some practical CLI commands you can run:

```bash
# Basic benchmark on random data
qdes-cli benchmark --dataset random --embedding angle --n-qubits 4 --verbose

# Compare multiple embeddings on Iris dataset
qdes-cli compare --embeddings angle,iqp,amplitude --dataset iris --output comparison.csv

# Visualize quantum kernel for wine dataset
qdes-cli visualize --embedding angle --dataset wine --n-qubits 4 --output wine_kernel.png

# Custom data file (CSV format)
qdes-cli benchmark --data my_data.csv --embedding iqp --n-qubits 3
```

## Example 6: Custom Backend Configuration

```python
from quantum_data_embedding_suite.backends import QiskitBackend

# Custom backend with specific settings
backend = QiskitBackend(
    device="aer_simulator",
    shots=2048,
    optimization_level=2
)

pipeline = QuantumEmbeddingPipeline(
    embedding_type="angle",
    n_qubits=4,
    backend=backend
)

# For PennyLane backend
from quantum_data_embedding_suite.backends import PennyLaneBackend

pennylane_backend = PennyLaneBackend(
    device="default.qubit",
    shots=1024
)

pipeline_pl = QuantumEmbeddingPipeline(
    embedding_type="angle",
    n_qubits=4,
    backend=pennylane_backend
)
```

## Example 7: Batch Processing for Large Datasets

```python
# For large datasets, use batch processing
def process_large_dataset(X, batch_size=100):
    pipeline = QuantumEmbeddingPipeline(
        embedding_type="angle",
        n_qubits=4,
        backend="qiskit"
    )
    
    n_samples = len(X)
    n_batches = (n_samples + batch_size - 1) // batch_size
    
    kernel_blocks = []
    
    for i in range(n_batches):
        start_idx = i * batch_size
        end_idx = min((i + 1) * batch_size, n_samples)
        
        X_batch = X[start_idx:end_idx]
        print(f"Processing batch {i+1}/{n_batches} (samples {start_idx}-{end_idx})")
        
        if i == 0:
            # Fit on first batch
            K_batch = pipeline.fit_transform(X_batch)
        else:
            # Transform subsequent batches
            K_batch = pipeline.transform(X_batch)
        
        kernel_blocks.append(K_batch)
    
    # Combine results (this is simplified - in practice you'd need to
    # handle the full kernel matrix construction carefully)
    return kernel_blocks

# Example usage
large_X = np.random.randn(500, 4)
kernel_blocks = process_large_dataset(large_X, batch_size=50)
print(f"Processed {len(kernel_blocks)} batches")
```

## Example 8: Error Handling and Robustness

```python
def robust_quantum_embedding(X, fallback_to_classical=True):
    """
    Robust quantum embedding with fallback options.
    """
    try:
        # Try quantum embedding
        pipeline = QuantumEmbeddingPipeline(
            embedding_type="angle",
            n_qubits=min(4, X.shape[1]),  # Adaptive qubit count
            backend="qiskit",
            shots=1024
        )
        
        K = pipeline.fit_transform(X)
        print("✅ Quantum embedding successful")
        return K, "quantum"
        
    except Exception as e:
        print(f"❌ Quantum embedding failed: {e}")
        
        if fallback_to_classical:
            print("🔄 Falling back to classical RBF kernel")
            from sklearn.metrics.pairwise import rbf_kernel
            K = rbf_kernel(X, gamma='scale')
            return K, "classical"
        else:
            raise

# Example usage
X = np.random.randn(30, 6)
K, method = robust_quantum_embedding(X)
print(f"Used {method} method, kernel shape: {K.shape}")
```

## Example 9: Hyperparameter Exploration

```python
def explore_hyperparameters(X, y):
    """
    Explore different hyperparameter combinations.
    """
    results = []
    
    # Parameter combinations to test
    embedding_types = ["angle", "iqp"]
    qubit_counts = [3, 4, 5]
    shot_counts = [512, 1024, 2048]
    
    for emb_type in embedding_types:
        for n_qubits in qubit_counts:
            for shots in shot_counts:
                print(f"Testing: {emb_type}, {n_qubits} qubits, {shots} shots")
                
                try:
                    pipeline = QuantumEmbeddingPipeline(
                        embedding_type=emb_type,
                        n_qubits=n_qubits,
                        backend="qiskit",
                        shots=shots
                    )
                    
                    # Use small subset for speed
                    X_small = X[:20]
                    y_small = y[:20]
                    
                    K = pipeline.fit_transform(X_small)
                    metrics = pipeline.evaluate_embedding(X_small)
                    
                    results.append({
                        'embedding': emb_type,
                        'n_qubits': n_qubits,
                        'shots': shots,
                        'expressibility': metrics['expressibility'],
                        'trainability': metrics['trainability']
                    })
                    
                except Exception as e:
                    print(f"  Failed: {e}")
                    continue
    
    return results

# Run exploration
X, y = load_iris(return_X_y=True)
X = StandardScaler().fit_transform(X)

results = explore_hyperparameters(X, y)

# Analyze results
import pandas as pd
df = pd.DataFrame(results)
print("\nBest configurations by expressibility:")
print(df.nlargest(3, 'expressibility')[['embedding', 'n_qubits', 'shots', 'expressibility']])

print("\nBest configurations by trainability:")
print(df.nlargest(3, 'trainability')[['embedding', 'n_qubits', 'shots', 'trainability']])
```

## Example 10: Saving and Loading Results

```python
import pickle
import json

def save_quantum_results(pipeline, K, metrics, filename_base):
    """
    Save quantum embedding results for later use.
    """
    # Save kernel matrix
    np.save(f"{filename_base}_kernel.npy", K)
    
    # Save metrics
    with open(f"{filename_base}_metrics.json", 'w') as f:
        json.dump(metrics, f, indent=2)
    
    # Save pipeline configuration
    config = pipeline.get_embedding_info()
    with open(f"{filename_base}_config.json", 'w') as f:
        json.dump(config, f, indent=2, default=str)
    
    print(f"Results saved with base name: {filename_base}")

def load_quantum_results(filename_base):
    """
    Load previously saved quantum embedding results.
    """
    # Load kernel matrix
    K = np.load(f"{filename_base}_kernel.npy")
    
    # Load metrics
    with open(f"{filename_base}_metrics.json", 'r') as f:
        metrics = json.load(f)
    
    # Load configuration
    with open(f"{filename_base}_config.json", 'r') as f:
        config = json.load(f)
    
    return K, metrics, config

# Example usage
X = np.random.randn(50, 4)

pipeline = QuantumEmbeddingPipeline(
    embedding_type="angle",
    n_qubits=4,
    backend="qiskit"
)

K = pipeline.fit_transform(X)
metrics = pipeline.evaluate_embedding(X)

# Save results
save_quantum_results(pipeline, K, metrics, "my_experiment")

# Load results later
K_loaded, metrics_loaded, config_loaded = load_quantum_results("my_experiment")
print(f"Loaded kernel shape: {K_loaded.shape}")
print(f"Loaded expressibility: {metrics_loaded['expressibility']:.3f}")
```

These examples provide a solid foundation for using the Quantum Data Embedding Suite. Each example builds on previous concepts while introducing new features and best practices.

## Next Steps

- Explore the [User Guide](user_guide.md) for detailed feature explanations
- Try the [Interactive Tutorials](tutorials/basic_workflow.md) for hands-on learning
- Check out [Advanced Examples](examples/index.md) for real-world applications
- Read the [API Reference](api/pipeline.md) for complete documentation
