# Basic Workflow Tutorial

This tutorial walks you through the fundamental workflow of using the Quantum Data Embedding Suite, from data preparation to quantum kernel computation and evaluation.

## Learning Objectives

By the end of this tutorial, you will:

- Understand the basic quantum data embedding workflow
- Know how to prepare data for quantum embeddings
- Be able to compute and analyze quantum kernels
- Understand embedding quality metrics
- Know how to compare quantum and classical approaches

## Prerequisites

- Basic understanding of machine learning concepts
- Familiarity with Python and NumPy
- Optional: Basic quantum computing knowledge

## Setup

First, ensure you have the package installed and import the necessary modules:

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris, make_classification
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report

# Import quantum embedding components
from quantum_data_embedding_suite import QuantumEmbeddingPipeline
from quantum_data_embedding_suite.visualization import plot_kernel_matrix, plot_embedding_comparison
from quantum_data_embedding_suite.metrics import expressibility, trainability

# Set random seed for reproducibility
np.random.seed(42)
```

## Step 1: Data Preparation

Let's start with a simple dataset to understand the workflow:

```python
# Load the Iris dataset
X, y = load_iris(return_X_y=True)
print(f"Dataset shape: {X.shape}")
print(f"Features: {X.shape[1]}, Samples: {X.shape[0]}")
print(f"Classes: {np.unique(y)}")

# Split the data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# Normalize the data (important for quantum embeddings)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f"Training set shape: {X_train_scaled.shape}")
print(f"Test set shape: {X_test_scaled.shape}")
```

**Key Points:**

- Always normalize your data for quantum embeddings
- Quantum circuits work best with data in a reasonable range
- Use proper train/test splits to avoid overfitting

## Step 2: Creating Your First Quantum Embedding

Let's create a simple quantum embedding pipeline:

```python
# Create a quantum embedding pipeline
pipeline = QuantumEmbeddingPipeline(
    embedding_type="angle",     # Start with angle embedding (simple and reliable)
    n_qubits=4,                # Use 4 qubits (suitable for 4-dimensional data)
    backend="qiskit",          # Use Qiskit backend
    shots=1024,                # Number of measurement shots
    random_state=42            # For reproducibility
)

print("Pipeline created successfully!")
print(f"Embedding type: {pipeline.get_embedding_info()['embedding_type']}")
print(f"Number of qubits: {pipeline.get_embedding_info()['n_qubits']}")
```

**Understanding the Parameters:**

- `embedding_type="angle"`: Encodes data as rotation angles in quantum gates
- `n_qubits=4`: We use 4 qubits for our 4-dimensional Iris data
- `shots=1024`: Higher shots = more accurate but slower computation
- `backend="qiskit"`: Uses IBM's Qiskit quantum simulator

## Step 3: Computing Quantum Kernels

Now let's compute quantum kernels for our data:

```python
# Fit the pipeline and compute the training kernel
print("Computing quantum kernels...")
K_train = pipeline.fit_transform(X_train_scaled)

# Compute test kernel (how test samples relate to training samples)
K_test = pipeline.transform(X_test_scaled)

print(f"Training kernel shape: {K_train.shape}")  # (n_train, n_train)
print(f"Test kernel shape: {K_test.shape}")      # (n_test, n_train)
print(f"Kernel value range: [{K_train.min():.3f}, {K_train.max():.3f}]")
```

**Understanding Kernel Shapes:**

- Training kernel: `(n_train, n_train)` - symmetric matrix
- Test kernel: `(n_test, n_train)` - rectangular matrix
- Kernel values represent similarity between quantum states

## Step 4: Visualizing Quantum Kernels

Let's visualize the computed kernels to understand their structure:

```python
# Plot the training kernel matrix
plt.figure(figsize=(12, 5))

# Training kernel
plt.subplot(1, 2, 1)
im1 = plt.imshow(K_train, cmap='viridis', aspect='auto')
plt.colorbar(im1, label='Kernel Value')
plt.title('Quantum Kernel Matrix (Training)')
plt.xlabel('Sample Index')
plt.ylabel('Sample Index')

# Test kernel
plt.subplot(1, 2, 2)
im2 = plt.imshow(K_test, cmap='viridis', aspect='auto')
plt.colorbar(im2, label='Kernel Value')
plt.title('Quantum Kernel Matrix (Test)')
plt.xlabel('Training Sample Index')
plt.ylabel('Test Sample Index')

plt.tight_layout()
plt.show()

# Analyze kernel properties
print("\nKernel Analysis:")
print(f"Training kernel diagonal mean: {np.mean(np.diag(K_train)):.3f}")
print(f"Training kernel off-diagonal mean: {np.mean(K_train - np.diag(np.diag(K_train))):.3f}")
print(f"Kernel matrix condition number: {np.linalg.cond(K_train):.2e}")
```

**What to Look For:**

- Diagonal values should be close to 1 (self-similarity)
- Block structure might indicate class separability
- Condition number indicates numerical stability

## Step 5: Embedding Quality Assessment

Let's evaluate the quality of our quantum embedding:

```python
# Compute embedding quality metrics
print("Evaluating embedding quality...")
metrics = pipeline.evaluate_embedding(X_train_scaled)

print("\nEmbedding Quality Metrics:")
for metric_name, value in metrics.items():
    print(f"{metric_name.capitalize()}: {value:.4f}")

# What do these metrics mean?
print("\nMetric Interpretation:")
print("• Expressibility (0-1): How well the embedding explores the Hilbert space")
print("  - Higher values indicate more expressive embeddings")
print("• Trainability (0-1): How sensitive the embedding is to parameter changes")
print("  - Moderate values (0.1-0.5) are typically good")
print("• Gradient Variance: Variability in parameter gradients")
print("  - Lower values might indicate barren plateaus")
```

## Step 6: Quantum vs Classical Comparison

Let's compare our quantum kernel with classical approaches:

```python
# Compute classical kernels for comparison
from sklearn.metrics.pairwise import rbf_kernel, polynomial_kernel, linear_kernel

# Classical kernels
K_rbf = rbf_kernel(X_train_scaled, gamma='scale')
K_poly = polynomial_kernel(X_train_scaled, degree=2)
K_linear = linear_kernel(X_train_scaled)

# Compare kernel matrices visually
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

kernels = [
    (K_train, "Quantum (Angle)"),
    (K_rbf, "Classical (RBF)"),
    (K_poly, "Classical (Polynomial)"),
    (K_linear, "Classical (Linear)")
]

for i, (K, title) in enumerate(kernels):
    ax = axes[i // 2, i % 2]
    im = ax.imshow(K, cmap='viridis', aspect='auto')
    ax.set_title(title)
    ax.set_xlabel('Sample Index')
    ax.set_ylabel('Sample Index')
    plt.colorbar(im, ax=ax)

plt.tight_layout()
plt.show()

# Quantitative comparison
print("\nKernel Comparison:")
print(f"Quantum - RBF correlation: {np.corrcoef(K_train.flatten(), K_rbf.flatten())[0,1]:.3f}")
print(f"Quantum - Polynomial correlation: {np.corrcoef(K_train.flatten(), K_poly.flatten())[0,1]:.3f}")
print(f"Quantum - Linear correlation: {np.corrcoef(K_train.flatten(), K_linear.flatten())[0,1]:.3f}")
```

## Step 7: Machine Learning with Quantum Kernels

Now let's use our quantum kernels for classification:

```python
# Train SVM with quantum kernel
print("Training Quantum SVM...")
quantum_svm = SVC(kernel='precomputed', C=1.0)
quantum_svm.fit(K_train, y_train)

# Make predictions
y_pred_quantum = quantum_svm.predict(K_test)
quantum_accuracy = accuracy_score(y_test, y_pred_quantum)

# Compare with classical SVM
print("Training Classical SVM...")
classical_svm = SVC(kernel='rbf', C=1.0, gamma='scale')
classical_svm.fit(X_train_scaled, y_train)
y_pred_classical = classical_svm.predict(X_test_scaled)
classical_accuracy = accuracy_score(y_test, y_pred_classical)

# Results
print(f"\nClassification Results:")
print(f"Quantum SVM Accuracy: {quantum_accuracy:.3f}")
print(f"Classical SVM Accuracy: {classical_accuracy:.3f}")
print(f"Difference: {quantum_accuracy - classical_accuracy:.3f}")

# Detailed classification report for quantum SVM
print(f"\nQuantum SVM Classification Report:")
print(classification_report(y_test, y_pred_quantum, 
                          target_names=['Setosa', 'Versicolor', 'Virginica']))
```

## Step 8: Exploring Different Embeddings

Let's try different quantum embeddings to see how they perform:

```python
# Test different embedding types
embedding_types = ["angle", "amplitude", "iqp"]
results = {}

for emb_type in embedding_types:
    print(f"\nTesting {emb_type} embedding...")
    
    try:
        # Create pipeline with different embedding
        pipeline_test = QuantumEmbeddingPipeline(
            embedding_type=emb_type,
            n_qubits=4,
            backend="qiskit",
            shots=1024,
            random_state=42
        )
        
        # Compute kernels
        K_train_test = pipeline_test.fit_transform(X_train_scaled)
        K_test_test = pipeline_test.transform(X_test_scaled)
        
        # Train and evaluate
        svm_test = SVC(kernel='precomputed', C=1.0)
        svm_test.fit(K_train_test, y_train)
        y_pred_test = svm_test.predict(K_test_test)
        accuracy_test = accuracy_score(y_test, y_pred_test)
        
        # Evaluate embedding quality
        metrics_test = pipeline_test.evaluate_embedding(X_train_scaled[:30])  # Use subset for speed
        
        results[emb_type] = {
            'accuracy': accuracy_test,
            'expressibility': metrics_test['expressibility'],
            'trainability': metrics_test['trainability']
        }
        
        print(f"  Accuracy: {accuracy_test:.3f}")
        print(f"  Expressibility: {metrics_test['expressibility']:.3f}")
        print(f"  Trainability: {metrics_test['trainability']:.3f}")
        
    except Exception as e:
        print(f"  Error with {emb_type}: {e}")
        continue

# Visualize comparison
if results:
    embeddings = list(results.keys())
    accuracies = [results[emb]['accuracy'] for emb in embeddings]
    expressibilities = [results[emb]['expressibility'] for emb in embeddings]
    trainabilities = [results[emb]['trainability'] for emb in embeddings]
    
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
    
    # Accuracy comparison
    ax1.bar(embeddings, accuracies, color=['blue', 'green', 'red'])
    ax1.set_ylabel('Accuracy')
    ax1.set_title('Classification Accuracy')
    ax1.set_ylim(0, 1)
    
    # Expressibility comparison
    ax2.bar(embeddings, expressibilities, color=['blue', 'green', 'red'])
    ax2.set_ylabel('Expressibility')
    ax2.set_title('Expressibility')
    ax2.set_ylim(0, 1)
    
    # Trainability comparison
    ax3.bar(embeddings, trainabilities, color=['blue', 'green', 'red'])
    ax3.set_ylabel('Trainability')
    ax3.set_title('Trainability')
    
    plt.tight_layout()
    plt.show()
```

## Step 9: Parameter Sensitivity Analysis

Let's explore how different parameters affect performance:

```python
# Test different numbers of qubits
print("Analyzing qubit count sensitivity...")
qubit_counts = [3, 4, 5, 6]
qubit_results = []

for n_qubits in qubit_counts:
    try:
        pipeline_qubits = QuantumEmbeddingPipeline(
            embedding_type="angle",
            n_qubits=n_qubits,
            backend="qiskit",
            shots=1024,
            random_state=42
        )
        
        # Use subset for speed
        X_subset = X_train_scaled[:30]
        y_subset = y_train[:30]
        
        K_subset = pipeline_qubits.fit_transform(X_subset)
        metrics_subset = pipeline_qubits.evaluate_embedding(X_subset)
        
        qubit_results.append({
            'n_qubits': n_qubits,
            'expressibility': metrics_subset['expressibility'],
            'trainability': metrics_subset['trainability']
        })
        
        print(f"  {n_qubits} qubits - Expr: {metrics_subset['expressibility']:.3f}, "
              f"Train: {metrics_subset['trainability']:.3f}")
        
    except Exception as e:
        print(f"  Error with {n_qubits} qubits: {e}")

# Visualize qubit sensitivity
if qubit_results:
    n_qubits_list = [r['n_qubits'] for r in qubit_results]
    expr_list = [r['expressibility'] for r in qubit_results]
    train_list = [r['trainability'] for r in qubit_results]
    
    plt.figure(figsize=(10, 5))
    
    plt.subplot(1, 2, 1)
    plt.plot(n_qubits_list, expr_list, 'bo-', label='Expressibility')
    plt.xlabel('Number of Qubits')
    plt.ylabel('Expressibility')
    plt.title('Expressibility vs Qubit Count')
    plt.grid(True)
    
    plt.subplot(1, 2, 2)
    plt.plot(n_qubits_list, train_list, 'ro-', label='Trainability')
    plt.xlabel('Number of Qubits')
    plt.ylabel('Trainability')
    plt.title('Trainability vs Qubit Count')
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()
```

## Step 10: Best Practices and Tips

Here are some key takeaways and best practices:

```python
# Demonstration of best practices
def quantum_embedding_best_practices():
    """
    Demonstrates best practices for quantum data embedding.
    """
    
    print("Best Practices for Quantum Data Embedding:")
    print("=" * 50)
    
    # 1. Data preprocessing
    print("\n1. Data Preprocessing:")
    print("   ✓ Always normalize your data")
    print("   ✓ Handle missing values appropriately")
    print("   ✓ Consider dimensionality reduction for high-dimensional data")
    
    # 2. Parameter selection
    print("\n2. Parameter Selection:")
    print("   ✓ Start with n_qubits ≥ log₂(n_features)")
    print("   ✓ Use 1024-2048 shots for good accuracy")
    print("   ✓ Begin with simple embeddings (angle) before trying complex ones")
    
    # 3. Evaluation
    print("\n3. Evaluation:")
    print("   ✓ Always evaluate embedding quality metrics")
    print("   ✓ Compare with classical baselines")
    print("   ✓ Use proper cross-validation")
    
    # 4. Performance optimization
    print("\n4. Performance Optimization:")
    print("   ✓ Cache embeddings when possible")
    print("   ✓ Use batch processing for large datasets")
    print("   ✓ Consider classical preprocessing")
    
    # 5. Debugging
    print("\n5. Debugging:")
    print("   ✓ Check kernel matrix properties (symmetry, positive definiteness)")
    print("   ✓ Monitor for barren plateaus (low gradient variance)")
    print("   ✓ Visualize kernels to understand behavior")

quantum_embedding_best_practices()

# Example of proper error handling
def robust_quantum_pipeline(X, y, embedding_type="angle"):
    """
    Example of robust quantum pipeline with error handling.
    """
    try:
        # Validate data
        if X.ndim != 2:
            raise ValueError("X must be 2D array")
        if len(X) != len(y):
            raise ValueError("X and y must have same length")
        
        # Choose appropriate number of qubits
        n_features = X.shape[1]
        n_qubits = max(3, min(6, n_features))  # Reasonable range
        
        # Create pipeline with error handling
        pipeline = QuantumEmbeddingPipeline(
            embedding_type=embedding_type,
            n_qubits=n_qubits,
            backend="qiskit",
            shots=1024,
            random_state=42
        )
        
        # Compute kernels
        K = pipeline.fit_transform(X)
        
        # Validate kernel
        if not np.allclose(K, K.T, atol=1e-10):
            print("Warning: Kernel matrix is not symmetric")
        
        eigenvals = np.linalg.eigvals(K)
        if np.any(eigenvals < -1e-10):
            print("Warning: Kernel matrix is not positive semidefinite")
        
        return pipeline, K
        
    except Exception as e:
        print(f"Error in quantum pipeline: {e}")
        return None, None

# Test robust pipeline
pipeline_robust, K_robust = robust_quantum_pipeline(X_train_scaled, y_train)
if K_robust is not None:
    print("Robust pipeline executed successfully!")
```

## Summary

In this tutorial, you learned:

1. **Data Preparation**: How to properly prepare and normalize data for quantum embeddings
2. **Pipeline Creation**: How to create and configure quantum embedding pipelines
3. **Kernel Computation**: How to compute and interpret quantum kernels
4. **Quality Assessment**: How to evaluate embedding quality using expressibility and trainability
5. **Comparison**: How to compare quantum and classical approaches
6. **Machine Learning**: How to use quantum kernels for classification
7. **Parameter Exploration**: How to systematically test different configurations
8. **Best Practices**: Key guidelines for successful quantum data embedding

## Next Steps

- Try the [Advanced Workflow Tutorial](advanced_workflow.md) for more complex scenarios
- Explore [Real-world Applications](../examples/classification.md) with larger datasets
- Learn about [Custom Embeddings](../examples/custom_embeddings.md)
- Read about [Performance Optimization](../examples/performance.md) techniques

## Troubleshooting

**Common Issues:**

1. **Import Errors**: Ensure all dependencies are installed
2. **Memory Issues**: Use batch processing for large datasets
3. **Slow Computation**: Reduce shots or qubit count for testing
4. **Poor Performance**: Check data normalization and parameter selection
5. **Numerical Issues**: Monitor kernel matrix properties

**Getting Help:**

- Check the [FAQ](../faq.md) for common questions
- Review the [API Documentation](../api/index.md) for detailed references
- See [Examples](../examples/index.md) for more use cases
