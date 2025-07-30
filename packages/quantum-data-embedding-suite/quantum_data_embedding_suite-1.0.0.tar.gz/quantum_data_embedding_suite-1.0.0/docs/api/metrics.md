# Metrics API

This page documents the quantum embedding quality metrics and analysis functions.

## Core Metrics Functions

### expressibility

::: quantum_data_embedding_suite.metrics.expressibility
    options:
      show_source: true
      show_root_heading: true
      show_object_full_path: false

### trainability

::: quantum_data_embedding_suite.metrics.trainability
    options:
      show_source: true
      show_root_heading: true
      show_object_full_path: false

### gradient_variance

::: quantum_data_embedding_suite.metrics.gradient_variance
    options:
      show_source: true
      show_root_heading: true
      show_object_full_path: false

### effective_dimension

::: quantum_data_embedding_suite.metrics.effective_dimension
    options:
      show_source: true
      show_root_heading: true
      show_object_full_path: false

## Composite Metrics

### compute_all_metrics

::: quantum_data_embedding_suite.metrics.compute_all_metrics
    options:
      show_source: true
      show_root_heading: true
      show_object_full_path: false

### quantum_advantage_score

::: quantum_data_embedding_suite.metrics.quantum_advantage_score
    options:
      show_source: true
      show_root_heading: true
      show_object_full_path: false

## Kernel Metrics

### kernel_alignment

::: quantum_data_embedding_suite.metrics.kernel_alignment
    options:
      show_source: true
      show_root_heading: true
      show_object_full_path: false

### kernel_expressivity

::: quantum_data_embedding_suite.metrics.kernel_expressivity
    options:
      show_source: true
      show_root_heading: true
      show_object_full_path: false

### kernel_matrix_rank

::: quantum_data_embedding_suite.metrics.kernel_matrix_rank
    options:
      show_source: true
      show_root_heading: true
      show_object_full_path: false

### kernel_condition_number

::: quantum_data_embedding_suite.metrics.kernel_condition_number
    options:
      show_source: true
      show_root_heading: true
      show_object_full_path: false

## Advanced Metrics

### embedding_capacity

::: quantum_data_embedding_suite.metrics.embedding_capacity
    options:
      show_source: true
      show_root_heading: true
      show_object_full_path: false

### separability_measure

::: quantum_data_embedding_suite.metrics.separability_measure
    options:
      show_source: true
      show_root_heading: true
      show_object_full_path: false

## Usage Examples

### Basic Metrics Computation

```python
from quantum_data_embedding_suite.metrics import (
    expressibility, trainability, gradient_variance, effective_dimension
)
from quantum_data_embedding_suite.embeddings import AngleEmbedding
import numpy as np

# Create embedding and sample data
embedding = AngleEmbedding(n_qubits=4)
X = np.random.randn(100, 4)

# Compute individual metrics
expr_score = expressibility(
    embedding=embedding,
    n_samples=1000,
    random_seed=42
)

train_score = trainability(
    embedding=embedding,
    data=X,
    n_samples=100
)

grad_var = gradient_variance(
    embedding=embedding,
    data=X,
    n_samples=100
)

# For effective dimension, we need a kernel matrix
from quantum_data_embedding_suite.kernels import FidelityKernel
kernel = FidelityKernel(embedding=embedding)
kernel_matrix = kernel.compute_kernel_matrix(X[:20])  # Use subset for speed
eff_dim = effective_dimension(kernel_matrix=kernel_matrix)

print(f"Expressibility: {expr_score:.4f}")
print(f"Trainability: {train_score:.4f}")
print(f"Gradient Variance: {grad_var:.6f}")
print(f"Effective Dimension: {eff_dim:.1f}")
```

### Comprehensive Metrics Analysis

```python
from quantum_data_embedding_suite.metrics import compute_all_metrics

# Compute all metrics at once
all_metrics = compute_all_metrics(
    embedding=embedding,
    data=X,
    n_samples=500
)

print("Complete Metrics Report:")
print("=" * 40)
for metric_name, value in all_metrics.items():
    if isinstance(value, float):
        print(f"  {metric_name}: {value:.6f}")
    else:
        print(f"  {metric_name}: {value}")
```

### Embedding Comparison

```python
from quantum_data_embedding_suite.embeddings import (
    AngleEmbedding, IQPEmbedding, AmplitudeEmbedding
)

# Create different embeddings
embeddings = {
    'angle': AngleEmbedding(n_qubits=4),
    'iqp': IQPEmbedding(n_qubits=4, depth=2),
    'amplitude': AmplitudeEmbedding(n_qubits=4)
}

# Compare metrics across embeddings
comparison_results = {}

for name, emb in embeddings.items():
    try:
        metrics = compute_all_metrics(
            embedding=emb,
            data=X[:50],  # Use smaller subset for speed
            n_samples=200
        )
        )
        
        comparison_results[name] = {
            'expressibility': metrics['expressibility'],
            'trainability': metrics['trainability'],
            'gradient_variance': metrics['gradient_variance']
        }
        
    except Exception as e:
        print(f"Error computing metrics for {name}: {e}")
        comparison_results[name] = None

# Display comparison
import pandas as pd
df = pd.DataFrame(comparison_results).T
print("\nEmbedding Comparison:")
print(df.round(4))

# Find best embedding for each metric
for metric in df.columns:
    best_embedding = df[metric].idxmax()
    best_value = df[metric].max()
    print(f"Best {metric}: {best_embedding} ({best_value:.4f})")
```

## Advanced Metrics Analysis

### Statistical Significance Testing

```python
from scipy import stats
import numpy as np

def compare_embeddings_statistically(embedding1, embedding2, X, n_trials=20):
    """Compare two embeddings with statistical significance testing"""
    
    # Collect metrics over multiple trials
    metrics1 = []
    metrics2 = []
    
    for trial in range(n_trials):
        # Add noise to data for each trial
        X_trial = X + np.random.normal(0, 0.01, X.shape)
        
        # Compute metrics
        expr1 = expressibility(embedding1, n_samples=500)
        expr2 = expressibility(embedding2, n_samples=500)
        
        metrics1.append(expr1)
        metrics2.append(expr2)
    
    metrics1 = np.array(metrics1)
    metrics2 = np.array(metrics2)
    
    # Perform statistical tests
    t_stat, p_value = stats.ttest_ind(metrics1, metrics2)
    mannwhitney_stat, mannwhitney_p = stats.mannwhitneyu(metrics1, metrics2)
    
    results = {
        'embedding1_mean': np.mean(metrics1),
        'embedding1_std': np.std(metrics1),
        'embedding2_mean': np.mean(metrics2),
        'embedding2_std': np.std(metrics2),
        't_test_p_value': p_value,
        'mann_whitney_p_value': mannwhitney_p,
        'significant_difference': p_value < 0.05
    }
    
    return results

# Compare embeddings statistically
angle_emb = AngleEmbedding(n_qubits=4)
iqp_emb = IQPEmbedding(n_qubits=4, depth=2)

stat_results = compare_embeddings_statistically(angle_emb, iqp_emb, X)

print("Statistical Comparison Results:")
for key, value in stat_results.items():
    print(f"{key}: {value}")
```

### Hyperparameter Sensitivity Analysis

```python
def analyze_hyperparameter_sensitivity(embedding_class, param_ranges, X, metric_func):
    """Analyze sensitivity of metrics to hyperparameter changes"""
    
    results = {}
    
    for param_name, param_values in param_ranges.items():
        param_results = []
        
        for param_value in param_values:
            try:
                # Create embedding with specific parameter
                kwargs = {param_name: param_value}
                embedding = embedding_class(n_qubits=4, **kwargs)
                
                # Compute metric
                metric_value = metric_func(embedding, X)
                param_results.append(metric_value)
                
            except Exception as e:
                print(f"Error with {param_name}={param_value}: {e}")
                param_results.append(np.nan)
        
        results[param_name] = {
            'values': param_values,
            'metrics': param_results,
            'sensitivity': np.std(param_results) if not np.all(np.isnan(param_results)) else 0
        }
    
    return results

# Analyze sensitivity for IQP embedding
param_ranges = {
    'depth': [1, 2, 3, 4],
    # Add other parameters as needed
}

def expr_metric(embedding, X):
    return expressibility(embedding, n_samples=500)

sensitivity_results = analyze_hyperparameter_sensitivity(
    IQPEmbedding, param_ranges, X, expr_metric
)

print("Hyperparameter Sensitivity Analysis:")
for param, results in sensitivity_results.items():
    print(f"{param}: sensitivity = {results['sensitivity']:.4f}")
```

### Temporal Metrics Evolution

```python
class MetricsTracker:
    """Track metrics evolution during training/optimization"""
    
    def __init__(self):
        self.history = {
            'expressibility': [],
            'trainability': [],
            'gradient_variance': [],
            'iteration': []
        }
    
    def record_metrics(self, embedding, X, iteration):
        """Record metrics at current iteration"""
        try:
            expr = expressibility(embedding, n_samples=200)  # Reduced for speed
            train = trainability(embedding, data=X[:20])  # Small subset
            grad_var = gradient_variance(embedding, data=X[:20], n_samples=50)
            
            self.history['expressibility'].append(expr)
            self.history['trainability'].append(train)
            self.history['gradient_variance'].append(grad_var)
            self.history['iteration'].append(iteration)
            
        except Exception as e:
            print(f"Error recording metrics at iteration {iteration}: {e}")
    
    def plot_evolution(self):
        """Plot metrics evolution"""
        import matplotlib.pyplot as plt
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 8))
        axes = axes.ravel()
        
        metrics = ['expressibility', 'trainability', 'gradient_variance']
        
        for i, metric in enumerate(metrics):
            axes[i].plot(self.history['iteration'], self.history[metric], 'o-')
            axes[i].set_title(f'{metric.capitalize()} Evolution')
            axes[i].set_xlabel('Iteration')
            axes[i].set_ylabel(metric.replace('_', ' ').title())
            axes[i].grid(True)
        
        # Summary plot
        normalized_metrics = {}
        for metric in metrics:
            values = np.array(self.history[metric])
            if np.std(values) > 0:
                normalized_metrics[metric] = (values - np.mean(values)) / np.std(values)
            else:
                normalized_metrics[metric] = values
        
        for metric in metrics:
            axes[3].plot(self.history['iteration'], normalized_metrics[metric], 
                        'o-', label=metric)
        
        axes[3].set_title('Normalized Metrics Evolution')
        axes[3].set_xlabel('Iteration')
        axes[3].set_ylabel('Normalized Value')
        axes[3].legend()
        axes[3].grid(True)
        
        plt.tight_layout()
        plt.show()
    
    def get_summary_statistics(self):
        """Get summary statistics of metrics evolution"""
        summary = {}
        
        for metric in ['expressibility', 'trainability', 'gradient_variance']:
            values = np.array(self.history[metric])
            if len(values) > 0:
                summary[metric] = {
                    'initial': values[0],
                    'final': values[-1],
                    'mean': np.mean(values),
                    'std': np.std(values),
                    'min': np.min(values),
                    'max': np.max(values),
                    'trend': 'increasing' if values[-1] > values[0] else 'decreasing'
                }
        
        return summary

# Example usage during optimization
tracker = MetricsTracker()

# Simulate optimization process
embedding = AngleEmbedding(n_qubits=4)
for iteration in range(10):
    # Simulate parameter updates
    # embedding.update_parameters(...)
    
    # Record metrics
    tracker.record_metrics(embedding, X, iteration)

# Analyze evolution
summary = tracker.get_summary_statistics()
print("Metrics Evolution Summary:")
for metric, stats in summary.items():
    print(f"\n{metric.upper()}:")
    for stat_name, value in stats.items():
        if isinstance(value, float):
            print(f"  {stat_name}: {value:.6f}")
        else:
            print(f"  {stat_name}: {value}")
```

## Kernel-Specific Metrics

### Kernel Quality Assessment

```python
from quantum_data_embedding_suite.kernels import FidelityKernel
from quantum_data_embedding_suite.metrics import kernel_alignment, kernel_expressivity

def assess_kernel_quality(kernel, X, y=None):
    """Comprehensive kernel quality assessment"""
    
    # Compute kernel matrix
    K = kernel.compute_kernel(X)
    
    # Basic kernel properties
    from quantum_data_embedding_suite.api.kernels import analyze_kernel_properties
    properties = analyze_kernel_properties(K)
    
    # Kernel-specific metrics
    expressivity = kernel_expressivity(kernel, X, method='entropy')
    
    # Compare with classical kernels
    from sklearn.metrics.pairwise import rbf_kernel, polynomial_kernel, linear_kernel
    
    classical_kernels = {
        'rbf': rbf_kernel(X),
        'polynomial': polynomial_kernel(X),
        'linear': linear_kernel(X)
    }
    
    alignments = {}
    for name, K_classical in classical_kernels.items():
        alignment = kernel_alignment(K, K_classical)
        alignments[f'{name}_alignment'] = alignment
    
    # Combine results
    quality_report = {
        'properties': properties,
        'expressivity': expressivity,
        'classical_alignments': alignments
    }
    
    # Add classification performance if labels available
    if y is not None:
        from sklearn.svm import SVC
        from sklearn.model_selection import cross_val_score
        
        svm = SVC(kernel='precomputed')
        cv_scores = cross_val_score(svm, K, y, cv=5)
        
        quality_report['classification_performance'] = {
            'cv_mean': np.mean(cv_scores),
            'cv_std': np.std(cv_scores),
            'cv_scores': cv_scores
        }
    
    return quality_report

# Assess kernel quality
kernel = FidelityKernel(embedding)
quality_report = assess_kernel_quality(kernel, X[:50], y[:50] if 'y' in locals() else None)

print("Kernel Quality Assessment:")
for category, metrics in quality_report.items():
    print(f"\n{category.upper()}:")
    if isinstance(metrics, dict):
        for metric_name, value in metrics.items():
            if isinstance(value, (int, float)):
                print(f"  {metric_name}: {value:.6f}")
            else:
                print(f"  {metric_name}: {value}")
    else:
        print(f"  {metrics}")
```

## Metrics Visualization

### Comprehensive Metrics Dashboard

```python
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D

def create_metrics_dashboard(embeddings_dict, X, save_path=None):
    """Create comprehensive metrics visualization dashboard"""
    
    # Collect metrics for all embeddings
    all_metrics = {}
    for name, embedding in embeddings_dict.items():
        try:
            metrics = compute_all_metrics(embedding, X[:30])  # Small subset for speed
            all_metrics[name] = metrics['core']
        except Exception as e:
            print(f"Error computing metrics for {name}: {e}")
            continue
    
    if not all_metrics:
        print("No metrics computed successfully")
        return
    
    # Create dashboard
    fig = plt.figure(figsize=(16, 12))
    
    # 1. Metrics comparison bar plot
    ax1 = plt.subplot(3, 3, 1)
    metrics_df = pd.DataFrame(all_metrics).T
    metrics_df.plot(kind='bar', ax=ax1)
    ax1.set_title('Metrics Comparison')
    ax1.set_ylabel('Metric Value')
    ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # 2. Expressibility vs Trainability scatter
    ax2 = plt.subplot(3, 3, 2)
    expr_vals = [metrics['expressibility'] for metrics in all_metrics.values()]
    train_vals = [metrics['trainability'] for metrics in all_metrics.values()]
    names = list(all_metrics.keys())
    
    scatter = ax2.scatter(expr_vals, train_vals, s=100, alpha=0.7)
    for i, name in enumerate(names):
        ax2.annotate(name, (expr_vals[i], train_vals[i]), 
                    xytext=(5, 5), textcoords='offset points')
    ax2.set_xlabel('Expressibility')
    ax2.set_ylabel('Trainability')
    ax2.set_title('Expressibility vs Trainability')
    ax2.grid(True, alpha=0.3)
    
    # 3. Radar chart
    ax3 = plt.subplot(3, 3, 3, projection='polar')
    
    metric_names = list(metrics_df.columns)
    angles = np.linspace(0, 2 * np.pi, len(metric_names), endpoint=False)
    angles = np.concatenate((angles, [angles[0]]))
    
    for name in names:
        values = metrics_df.loc[name].values
        values = np.concatenate((values, [values[0]]))
        ax3.plot(angles, values, 'o-', linewidth=2, label=name)
        ax3.fill(angles, values, alpha=0.25)
    
    ax3.set_xticks(angles[:-1])
    ax3.set_xticklabels(metric_names)
    ax3.set_title('Metrics Radar Chart')
    ax3.legend(bbox_to_anchor=(1.3, 1.1))
    
    # 4. Metrics correlation heatmap
    ax4 = plt.subplot(3, 3, 4)
    correlation_matrix = metrics_df.corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', 
                center=0, ax=ax4)
    ax4.set_title('Metrics Correlation')
    
    # 5. Individual metric distributions
    ax5 = plt.subplot(3, 3, 5)
    for metric in metric_names:
        ax5.hist(metrics_df[metric], alpha=0.5, label=metric, bins=10)
    ax5.set_xlabel('Metric Value')
    ax5.set_ylabel('Frequency')
    ax5.set_title('Metric Distributions')
    ax5.legend()
    
    # 6. Embedding ranking
    ax6 = plt.subplot(3, 3, 6)
    
    # Simple ranking based on average normalized metrics
    normalized_metrics = metrics_df.apply(lambda x: (x - x.min()) / (x.max() - x.min()) if x.max() > x.min() else x)
    rankings = normalized_metrics.mean(axis=1).sort_values(ascending=False)
    
    bars = ax6.bar(range(len(rankings)), rankings.values)
    ax6.set_xticks(range(len(rankings)))
    ax6.set_xticklabels(rankings.index, rotation=45)
    ax6.set_ylabel('Average Normalized Score')
    ax6.set_title('Embedding Rankings')
    
    # Color bars by rank
    colors = plt.cm.RdYlGn(np.linspace(0.3, 1, len(bars)))
    for bar, color in zip(bars, colors):
        bar.set_color(color)
    
    # 7-9. Individual embedding analysis
    for i, (name, embedding) in enumerate(list(embeddings_dict.items())[:3]):
        ax = plt.subplot(3, 3, 7 + i)
        
        # Create sample circuit for visualization
        sample_data = X[0] if len(X) > 0 else np.random.randn(4)
        circuit = embedding.embed(sample_data)
        
        # Plot circuit depth over different data points
        depths = []
        for j in range(min(20, len(X))):
            circ = embedding.embed(X[j])
            depths.append(circ.depth())
        
        ax.plot(depths, 'o-')
        ax.set_xlabel('Data Point Index')
        ax.set_ylabel('Circuit Depth')
        ax.set_title(f'{name} - Circuit Depth Variation')
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()
    
    return fig

# Create dashboard
embeddings_for_dashboard = {
    'Angle': AngleEmbedding(n_qubits=4),
    'IQP': IQPEmbedding(n_qubits=4, depth=2),
    'Amplitude': AmplitudeEmbedding(n_qubits=4)
}

dashboard_fig = create_metrics_dashboard(embeddings_for_dashboard, X)
```

## Performance Optimization

### Efficient Metrics Computation

```python
class MetricsCache:
    """Cache for expensive metrics computations"""
    
    def __init__(self, max_size=100):
        self.cache = {}
        self.max_size = max_size
        self.access_count = {}
    
    def _get_key(self, embedding, X, metric_name, **kwargs):
        """Generate cache key"""
        import hashlib
        
        # Create key from embedding type, data hash, and parameters
        embedding_str = f"{type(embedding).__name__}_{embedding.n_qubits}"
        data_hash = hashlib.md5(X.tobytes()).hexdigest()[:8]
        params_str = "_".join([f"{k}_{v}" for k, v in sorted(kwargs.items())])
        
        return f"{embedding_str}_{data_hash}_{metric_name}_{params_str}"
    
    def get(self, embedding, X, metric_name, **kwargs):
        """Get cached result"""
        key = self._get_key(embedding, X, metric_name, **kwargs)
        
        if key in self.cache:
            self.access_count[key] = self.access_count.get(key, 0) + 1
            return self.cache[key]
        
        return None
    
    def set(self, embedding, X, metric_name, result, **kwargs):
        """Cache result"""
        key = self._get_key(embedding, X, metric_name, **kwargs)
        
        # Remove least accessed item if cache is full
        if len(self.cache) >= self.max_size:
            least_accessed = min(self.access_count.items(), key=lambda x: x[1])
            del self.cache[least_accessed[0]]
            del self.access_count[least_accessed[0]]
        
        self.cache[key] = result
        self.access_count[key] = 1

# Global cache instance
_metrics_cache = MetricsCache()

def cached_expressibility(embedding, X=None, n_samples=1000, **kwargs):
    """Cached version of expressibility computation"""
    
    # Check cache
    cached_result = _metrics_cache.get(embedding, X or np.array([]), 
                                     'expressibility', 
                                     n_samples=n_samples, **kwargs)
    if cached_result is not None:
        return cached_result
    
    # Compute if not cached
    result = expressibility(embedding, n_samples=n_samples, **kwargs)
    
    # Cache result
    _metrics_cache.set(embedding, X or np.array([]), 
                      'expressibility', result, 
                      n_samples=n_samples, **kwargs)
    
    return result

# Use cached function
expr_score = cached_expressibility(embedding, n_samples=1000)
```

### Parallel Metrics Computation

```python
from multiprocessing import Pool
import functools

def compute_metrics_parallel(embeddings_list, X, n_jobs=4):
    """Compute metrics for multiple embeddings in parallel"""
    
    def compute_single_embedding_metrics(embedding):
        """Compute metrics for a single embedding"""
        try:
            return {
                'embedding': type(embedding).__name__,
                'expressibility': expressibility(embedding, n_samples=500),
                'trainability': trainability(embedding, X[:20]),
                'effective_dimension': effective_dimension(embedding, X[:20])
            }
        except Exception as e:
            return {
                'embedding': type(embedding).__name__,
                'error': str(e)
            }
    
    # Compute in parallel
    with Pool(n_jobs) as pool:
        results = pool.map(compute_single_embedding_metrics, embeddings_list)
    
    return results

# Use parallel computation
embeddings_list = [
    AngleEmbedding(n_qubits=4),
    IQPEmbedding(n_qubits=4, depth=2),
    AmplitudeEmbedding(n_qubits=4)
]

parallel_results = compute_metrics_parallel(embeddings_list, X, n_jobs=2)

print("Parallel Metrics Results:")
for result in parallel_results:
    print(f"  {result}")
```

## Best Practices

### Metrics Interpretation Guidelines

```python
def interpret_metrics(metrics, context=None):
    """Provide interpretation guidelines for metrics"""
    
    interpretations = {}
    
    # Expressibility interpretation
    expr = metrics.get('expressibility', 0)
    if expr > 0.8:
        interpretations['expressibility'] = "Excellent - covers state space uniformly"
    elif expr > 0.6:
        interpretations['expressibility'] = "Good - adequate state space coverage"
    elif expr > 0.4:
        interpretations['expressibility'] = "Fair - limited state space coverage"
    else:
        interpretations['expressibility'] = "Poor - very limited state space coverage"
    
    # Trainability interpretation
    train = metrics.get('trainability', 0)
    if train > 0.01:
        interpretations['trainability'] = "Good - strong gradient signals"
    elif train > 0.001:
        interpretations['trainability'] = "Moderate - weak but usable gradients"
    else:
        interpretations['trainability'] = "Poor - potential barren plateau"
    
    # Effective dimension interpretation
    eff_dim = metrics.get('effective_dimension', 0)
    data_dim = context.get('data_dimension', 0) if context else 0
    
    if data_dim > 0:
        if eff_dim > data_dim * 0.8:
            interpretations['effective_dimension'] = "High - preserves most data information"
        elif eff_dim > data_dim * 0.5:
            interpretations['effective_dimension'] = "Moderate - reasonable compression"
        else:
            interpretations['effective_dimension'] = "Low - significant information loss"
    
    return interpretations

# Example usage
sample_metrics = {
    'expressibility': 0.75,
    'trainability': 0.005,
    'effective_dimension': 3.2
}

context_info = {'data_dimension': 4}
interpretations = interpret_metrics(sample_metrics, context_info)

print("Metrics Interpretations:")
for metric, interpretation in interpretations.items():
    print(f"  {metric}: {interpretation}")
```

## Further Reading

- [Metrics User Guide](../user_guide/metrics.md)
- [Embedding API](embeddings.md)
- [Kernel API](kernels.md)
- [Optimization Tutorial](../tutorials/optimization.ipynb)
