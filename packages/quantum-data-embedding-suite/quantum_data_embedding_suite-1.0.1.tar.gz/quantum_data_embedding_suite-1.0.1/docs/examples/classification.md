# Classification Examples

This page demonstrates quantum data embedding applications for classification tasks.

## Binary Classification

### Basic Setup

```python
from quantum_data_embedding_suite.embeddings import AngleEmbedding
from quantum_data_embedding_suite.kernels import FidelityKernel
from sklearn.svm import SVC
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import numpy as np

# Generate sample classification data
X, y = make_classification(
    n_samples=200,
    n_features=4,
    n_redundant=0,
    n_informative=4,
    n_clusters_per_class=1,
    random_state=42
)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

print(f"Training set: {X_train.shape}")
print(f"Test set: {X_test.shape}")
print(f"Classes: {np.unique(y)}")
```

### Quantum Kernel Classification

```python
# Create quantum embedding
embedding = AngleEmbedding(n_qubits=4)

# Create quantum kernel
quantum_kernel = FidelityKernel(embedding=embedding)

# Compute kernel matrices
print("Computing training kernel matrix...")
K_train = quantum_kernel.compute_kernel_matrix(X_train)

print("Computing test kernel matrix...")
K_test = quantum_kernel.compute_kernel_matrix(X_test, X_train)

# Train SVM with precomputed kernel
svm_quantum = SVC(kernel='precomputed', C=1.0)
svm_quantum.fit(K_train, y_train)

# Make predictions
y_pred_quantum = svm_quantum.predict(K_test)

# Evaluate performance
accuracy_quantum = accuracy_score(y_test, y_pred_quantum)
print(f"\nQuantum Kernel SVM Accuracy: {accuracy_quantum:.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred_quantum))
```

### Classical Baseline Comparison

```python
# Train classical SVM for comparison
svm_classical = SVC(kernel='rbf', C=1.0, gamma='scale')
svm_classical.fit(X_train, y_train)

# Make predictions
y_pred_classical = svm_classical.predict(X_test)

# Evaluate performance
accuracy_classical = accuracy_score(y_test, y_pred_classical)
print(f"Classical RBF SVM Accuracy: {accuracy_classical:.4f}")

# Compare results
print(f"\nAccuracy Comparison:")
print(f"Quantum Kernel: {accuracy_quantum:.4f}")
print(f"Classical RBF:  {accuracy_classical:.4f}")
print(f"Improvement:    {accuracy_quantum - accuracy_classical:.4f}")
```

## Multi-class Classification

### Dataset Preparation

```python
from sklearn.datasets import make_classification
from sklearn.preprocessing import StandardScaler

# Generate multi-class data
X_multi, y_multi = make_classification(
    n_samples=300,
    n_features=6,
    n_classes=3,
    n_redundant=0,
    n_informative=6,
    n_clusters_per_class=1,
    random_state=42
)

# Standardize features
scaler = StandardScaler()
X_multi_scaled = scaler.fit_transform(X_multi)

# Split data
X_train_multi, X_test_multi, y_train_multi, y_test_multi = train_test_split(
    X_multi_scaled, y_multi, test_size=0.3, random_state=42, stratify=y_multi
)

print(f"Multi-class dataset: {X_multi_scaled.shape}")
print(f"Classes: {np.unique(y_multi)}")
print(f"Class distribution: {np.bincount(y_multi)}")
```

### Quantum Multi-class Classification

```python
# Create embedding for multi-class problem
embedding_multi = AngleEmbedding(n_qubits=6)
quantum_kernel_multi = FidelityKernel(embedding=embedding_multi)

# Compute kernel matrices
K_train_multi = quantum_kernel_multi.compute_kernel_matrix(X_train_multi)
K_test_multi = quantum_kernel_multi.compute_kernel_matrix(X_test_multi, X_train_multi)

# Train multi-class SVM
svm_quantum_multi = SVC(
    kernel='precomputed',
    C=1.0,
    decision_function_shape='ovr'  # One-vs-rest
)
svm_quantum_multi.fit(K_train_multi, y_train_multi)

# Make predictions
y_pred_quantum_multi = svm_quantum_multi.predict(K_test_multi)

# Evaluate performance
accuracy_quantum_multi = accuracy_score(y_test_multi, y_pred_quantum_multi)
print(f"Quantum Multi-class Accuracy: {accuracy_quantum_multi:.4f}")
print("\nConfusion Matrix:")

from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

cm = confusion_matrix(y_test_multi, y_pred_quantum_multi)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.title('Quantum Kernel Multi-class Confusion Matrix')
plt.show()
```

## Feature Importance Analysis

### Quantum Feature Importance

```python
def quantum_feature_importance(embedding, X, y, n_trials=10):
    """Compute quantum feature importance via permutation"""
    
    # Baseline performance
    kernel = FidelityKernel(embedding=embedding)
    K = kernel.compute_kernel_matrix(X)
    
    svm = SVC(kernel='precomputed')
    svm.fit(K, y)
    baseline_score = svm.score(K, y)
    
    importances = []
    
    for feature_idx in range(X.shape[1]):
        feature_scores = []
        
        for trial in range(n_trials):
            # Permute feature
            X_permuted = X.copy()
            np.random.shuffle(X_permuted[:, feature_idx])
            
            # Compute permuted kernel
            K_permuted = kernel.compute_kernel_matrix(X_permuted)
            
            # Train and score
            svm_permuted = SVC(kernel='precomputed')
            svm_permuted.fit(K_permuted, y)
            permuted_score = svm_permuted.score(K_permuted, y)
            
            # Importance is drop in performance
            importance = baseline_score - permuted_score
            feature_scores.append(importance)
        
        # Average importance across trials
        mean_importance = np.mean(feature_scores)
        importances.append(mean_importance)
    
    return np.array(importances)

# Compute feature importance
feature_importance = quantum_feature_importance(
    embedding, X_train, y_train, n_trials=5
)

# Plot feature importance
plt.figure(figsize=(10, 6))
feature_names = [f'Feature {i}' for i in range(len(feature_importance))]
plt.bar(feature_names, feature_importance)
plt.xlabel('Features')
plt.ylabel('Importance Score')
plt.title('Quantum Feature Importance')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.show()

print("Feature Importance Scores:")
for i, importance in enumerate(feature_importance):
    print(f"Feature {i}: {importance:.4f}")
```

## Advanced Classification Techniques

### Ensemble Methods with Quantum Kernels

```python
from sklearn.ensemble import VotingClassifier
from quantum_data_embedding_suite.embeddings import IQPEmbedding, AmplitudeEmbedding

def create_quantum_ensemble(X_train, y_train):
    """Create ensemble of quantum kernel classifiers"""
    
    # Different embeddings
    embeddings = [
        ('angle', AngleEmbedding(n_qubits=4)),
        ('iqp', IQPEmbedding(n_qubits=4, depth=2)),
        ('amplitude', AmplitudeEmbedding(n_qubits=4))
    ]
    
    classifiers = []
    
    for name, embedding in embeddings:
        # Create kernel and compute kernel matrix
        kernel = FidelityKernel(embedding=embedding)
        K = kernel.compute_kernel_matrix(X_train)
        
        # Create SVM
        svm = SVC(kernel='precomputed', probability=True)
        svm.fit(K, y_train)
        
        # Wrap for ensemble (store kernel for prediction)
        classifier_with_kernel = QuantumKernelClassifier(embedding, svm)
        classifiers.append((name, classifier_with_kernel))
    
    # Create voting ensemble
    ensemble = VotingClassifier(
        estimators=classifiers,
        voting='soft'  # Use probability voting
    )
    
    return ensemble

class QuantumKernelClassifier:
    """Wrapper for quantum kernel classifier"""
    
    def __init__(self, embedding, trained_svm):
        self.embedding = embedding
        self.svm = trained_svm
        self.kernel = FidelityKernel(embedding=embedding)
        self.training_data = None
    
    def fit(self, X, y):
        """Store training data for kernel computation"""
        self.training_data = X
        return self
    
    def predict(self, X):
        """Predict using quantum kernel"""
        if self.training_data is None:
            raise ValueError("Classifier not fitted")
        
        K_test = self.kernel.compute_kernel_matrix(X, self.training_data)
        return self.svm.predict(K_test)
    
    def predict_proba(self, X):
        """Predict probabilities using quantum kernel"""
        if self.training_data is None:
            raise ValueError("Classifier not fitted")
        
        K_test = self.kernel.compute_kernel_matrix(X, self.training_data)
        return self.svm.predict_proba(K_test)

# Create and evaluate ensemble
ensemble = create_quantum_ensemble(X_train, y_train)
ensemble.fit(X_train, y_train)  # Store training data

y_pred_ensemble = ensemble.predict(X_test)
accuracy_ensemble = accuracy_score(y_test, y_pred_ensemble)

print(f"Quantum Ensemble Accuracy: {accuracy_ensemble:.4f}")
```

### Cross-Validation with Quantum Kernels

```python
from sklearn.model_selection import cross_val_score, StratifiedKFold

def quantum_cross_validation(embedding, X, y, cv_folds=5):
    """Perform cross-validation with quantum kernels"""
    
    kfold = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=42)
    scores = []
    
    for fold, (train_idx, val_idx) in enumerate(kfold.split(X, y)):
        print(f"Processing fold {fold + 1}/{cv_folds}...")
        
        X_train_fold = X[train_idx]
        X_val_fold = X[val_idx]
        y_train_fold = y[train_idx]
        y_val_fold = y[val_idx]
        
        # Compute kernel matrices
        kernel = FidelityKernel(embedding=embedding)
        K_train_fold = kernel.compute_kernel_matrix(X_train_fold)
        K_val_fold = kernel.compute_kernel_matrix(X_val_fold, X_train_fold)
        
        # Train and evaluate
        svm = SVC(kernel='precomputed')
        svm.fit(K_train_fold, y_train_fold)
        
        score = svm.score(K_val_fold, y_val_fold)
        scores.append(score)
    
    return np.array(scores)

# Perform cross-validation
cv_scores = quantum_cross_validation(embedding, X_train, y_train, cv_folds=5)

print(f"Cross-validation scores: {cv_scores}")
print(f"Mean CV accuracy: {np.mean(cv_scores):.4f} ± {np.std(cv_scores):.4f}")
```

## Real-World Dataset Examples

### Iris Dataset

```python
from sklearn.datasets import load_iris

# Load Iris dataset
iris = load_iris()
X_iris, y_iris = iris.data, iris.target

# Use only 2 classes for binary classification
binary_mask = y_iris != 2
X_iris_binary = X_iris[binary_mask]
y_iris_binary = y_iris[binary_mask]

# Split data
X_train_iris, X_test_iris, y_train_iris, y_test_iris = train_test_split(
    X_iris_binary, y_iris_binary, test_size=0.3, random_state=42
)

# Scale features
scaler_iris = StandardScaler()
X_train_iris_scaled = scaler_iris.fit_transform(X_train_iris)
X_test_iris_scaled = scaler_iris.transform(X_test_iris)

# Quantum classification
embedding_iris = AngleEmbedding(n_qubits=4)
kernel_iris = FidelityKernel(embedding=embedding_iris)

K_train_iris = kernel_iris.compute_kernel_matrix(X_train_iris_scaled)
K_test_iris = kernel_iris.compute_kernel_matrix(X_test_iris_scaled, X_train_iris_scaled)

svm_iris = SVC(kernel='precomputed')
svm_iris.fit(K_train_iris, y_train_iris)

accuracy_iris = svm_iris.score(K_test_iris, y_test_iris)
print(f"Iris Dataset - Quantum Kernel Accuracy: {accuracy_iris:.4f}")
```

### Wine Dataset

```python
from sklearn.datasets import load_wine

# Load Wine dataset
wine = load_wine()
X_wine, y_wine = wine.data, wine.target

# Use subset of features
feature_indices = [0, 1, 6, 9]  # Select 4 most important features
X_wine_subset = X_wine[:, feature_indices]

# Split and scale
X_train_wine, X_test_wine, y_train_wine, y_test_wine = train_test_split(
    X_wine_subset, y_wine, test_size=0.3, random_state=42, stratify=y_wine
)

scaler_wine = StandardScaler()
X_train_wine_scaled = scaler_wine.fit_transform(X_train_wine)
X_test_wine_scaled = scaler_wine.transform(X_test_wine)

# Quantum multi-class classification
embedding_wine = AngleEmbedding(n_qubits=4)
kernel_wine = FidelityKernel(embedding=embedding_wine)

K_train_wine = kernel_wine.compute_kernel_matrix(X_train_wine_scaled)
K_test_wine = kernel_wine.compute_kernel_matrix(X_test_wine_scaled, X_train_wine_scaled)

svm_wine = SVC(kernel='precomputed', decision_function_shape='ovr')
svm_wine.fit(K_train_wine, y_train_wine)

accuracy_wine = svm_wine.score(K_test_wine, y_test_wine)
print(f"Wine Dataset - Quantum Kernel Accuracy: {accuracy_wine:.4f}")

# Detailed evaluation
y_pred_wine = svm_wine.predict(K_test_wine)
print("\nWine Classification Report:")
print(classification_report(y_test_wine, y_pred_wine, target_names=wine.target_names))
```

## Hyperparameter Optimization for Classification

### Grid Search with Quantum Kernels

```python
from sklearn.model_selection import ParameterGrid

def quantum_grid_search(X_train, y_train, X_val, y_val):
    """Grid search for quantum kernel hyperparameters"""
    
    # Define parameter grid
    param_grid = {
        'n_qubits': [3, 4, 5],
        'embedding_type': ['angle', 'iqp'],
        'svm_C': [0.1, 1.0, 10.0]
    }
    
    best_score = 0
    best_params = None
    results = []
    
    for params in ParameterGrid(param_grid):
        print(f"Testing parameters: {params}")
        
        # Create embedding
        if params['embedding_type'] == 'angle':
            embedding = AngleEmbedding(n_qubits=params['n_qubits'])
        elif params['embedding_type'] == 'iqp':
            embedding = IQPEmbedding(n_qubits=params['n_qubits'], depth=2)
        
        # Compute kernels
        kernel = FidelityKernel(embedding=embedding)
        K_train = kernel.compute_kernel_matrix(X_train)
        K_val = kernel.compute_kernel_matrix(X_val, X_train)
        
        # Train SVM
        svm = SVC(kernel='precomputed', C=params['svm_C'])
        svm.fit(K_train, y_train)
        
        # Evaluate
        score = svm.score(K_val, y_val)
        results.append({**params, 'score': score})
        
        if score > best_score:
            best_score = score
            best_params = params
    
    return best_params, best_score, results

# Perform grid search
best_params, best_score, all_results = quantum_grid_search(
    X_train, y_train, X_test, y_test
)

print(f"\nBest parameters: {best_params}")
print(f"Best validation score: {best_score:.4f}")

# Plot results
import pandas as pd

df_results = pd.DataFrame(all_results)
print("\nAll Results:")
print(df_results.sort_values('score', ascending=False))
```

This comprehensive classification guide demonstrates how to effectively use quantum data embeddings for various classification tasks, from basic binary classification to advanced ensemble methods and hyperparameter optimization.
