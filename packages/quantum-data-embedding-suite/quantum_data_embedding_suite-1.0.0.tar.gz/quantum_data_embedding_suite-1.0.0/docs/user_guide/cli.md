# CLI Usage

This guide covers the command-line interface (CLI) tools provided by the Quantum Data Embedding Suite.

## Overview

The `qdes-cli` command-line interface provides rapid access to common quantum embedding tasks without writing Python code. It's designed for quick experimentation, benchmarking, and automated workflows.

## Installation

The CLI is automatically installed with the package:

```bash
pip install quantum-data-embedding-suite
```

Verify installation:

```bash
qdes-cli --version
qdes-cli --help
```

## Basic Usage

### Command Structure

```bash
qdes-cli [GLOBAL_OPTIONS] COMMAND [COMMAND_OPTIONS]
```

### Global Options

- `--verbose, -v`: Enable verbose output
- `--quiet, -q`: Suppress output except errors
- `--config CONFIG_FILE`: Use custom configuration file
- `--backend BACKEND`: Default backend (qiskit, pennylane)
- `--help`: Show help message

## Commands

### benchmark

Compare quantum embeddings against classical baselines.

#### Basic Usage

```bash
# Benchmark angle embedding on Iris dataset
qdes-cli benchmark --dataset iris --embedding angle --n-qubits 4

# Multiple embeddings comparison
qdes-cli benchmark --dataset wine --embeddings angle,iqp,amplitude --n-qubits 4

# Custom dataset
qdes-cli benchmark --data mydata.csv --target-column class --embedding angle
```

#### Parameters

- `--dataset DATASET`: Built-in dataset name (iris, wine, breast_cancer, digits)
- `--data DATA_FILE`: Path to custom CSV file
- `--target-column COLUMN`: Target column name for custom data
- `--embedding EMBEDDING`: Embedding type (angle, amplitude, iqp, data_reuploading, hamiltonian)
- `--embeddings LIST`: Multiple embeddings (comma-separated)
- `--n-qubits N`: Number of qubits
- `--shots N`: Number of shots for quantum simulation
- `--backend BACKEND`: Quantum backend
- `--classical-methods LIST`: Classical methods to compare against
- `--cv-folds N`: Number of cross-validation folds
- `--output FILE`: Output file for results
- `--plot`: Generate comparison plots
- `--seed N`: Random seed for reproducibility

#### Examples

```bash
# Comprehensive benchmark with plots
qdes-cli benchmark \
    --dataset iris \
    --embeddings angle,iqp,amplitude \
    --n-qubits 4 \
    --shots 1024 \
    --classical-methods rbf_svm,linear_svm,random_forest \
    --cv-folds 5 \
    --output benchmark_results.json \
    --plot \
    --seed 42

# Quick benchmark
qdes-cli benchmark --dataset wine --embedding angle --n-qubits 3

# Custom data benchmark
qdes-cli benchmark \
    --data dataset.csv \
    --target-column target \
    --embedding iqp \
    --n-qubits 4 \
    --output results.json
```

#### Output

```json
{
  "dataset": "iris",
  "results": {
    "angle_embedding": {
      "accuracy": 0.953,
      "precision": 0.951,
      "recall": 0.953,
      "f1_score": 0.951,
      "std_error": 0.021
    },
    "classical_rbf_svm": {
      "accuracy": 0.967,
      "precision": 0.968,
      "recall": 0.967,
      "f1_score": 0.967,
      "std_error": 0.018
    }
  },
  "quantum_advantage": -0.014,
  "execution_time": 45.2
}
```

### compare

Compare different embedding types and hyperparameters.

#### Basic Usage

```bash
# Compare embeddings
qdes-cli compare --embeddings angle,iqp --dataset iris --n-qubits 4

# Compare qubit counts
qdes-cli compare --embedding angle --n-qubits-range 2,3,4,5 --dataset wine

# Parameter sweep
qdes-cli compare \
    --embedding iqp \
    --dataset iris \
    --param-grid "depth=[1,2,3],n_qubits=[3,4,5]"
```

#### Parameters

- `--embeddings LIST`: Embeddings to compare
- `--n-qubits-range LIST`: Range of qubit counts
- `--param-grid GRID`: Parameter grid for hyperparameter search
- `--metric METRIC`: Comparison metric (accuracy, f1_score, expressibility)
- `--optimization METHOD`: Hyperparameter optimization method
- `--n-trials N`: Number of optimization trials
- `--timeout SECONDS`: Maximum time per trial

#### Examples

```bash
# Systematic comparison
qdes-cli compare \
    --embeddings angle,iqp,amplitude \
    --dataset breast_cancer \
    --n-qubits-range 3,4,5,6 \
    --metric accuracy \
    --cv-folds 5 \
    --output comparison.json

# Hyperparameter optimization
qdes-cli compare \
    --embedding data_reuploading \
    --dataset wine \
    --param-grid "n_layers=[2,3,4],n_qubits=[4,5,6]" \
    --optimization bayesian \
    --n-trials 50 \
    --timeout 3600
```

### visualize

Generate visualizations for quantum embeddings and kernels.

#### Basic Usage

```bash
# Visualize kernel matrix
qdes-cli visualize kernel --data data.csv --embedding angle --n-qubits 4

# Embedding quality metrics
qdes-cli visualize metrics --data data.csv --embedding iqp --n-qubits 4

# Parameter space exploration
qdes-cli visualize parameter-space \
    --embedding angle \
    --dataset iris \
    --param n_qubits \
    --range 2,8
```

#### Visualization Types

**Kernel Visualization**

```bash
qdes-cli visualize kernel \
    --data data.csv \
    --embedding angle \
    --n-qubits 4 \
    --output kernel_plots/ \
    --format png
```

**Metrics Dashboard**

```bash
qdes-cli visualize metrics \
    --data data.csv \
    --embeddings angle,iqp \
    --metrics expressibility,trainability \
    --output metrics_dashboard.html
```

**Parameter Exploration**

```bash
qdes-cli visualize parameter-space \
    --embedding iqp \
    --dataset wine \
    --param depth \
    --range 1,5 \
    --metric expressibility
```

**Eigenspectrum Analysis**

```bash
qdes-cli visualize eigenspectrum \
    --data data.csv \
    --embedding amplitude \
    --n-qubits 4 \
    --n-eigenvalues 20
```

#### Parameters

- `--data DATA_FILE`: Input data file
- `--embedding EMBEDDING`: Embedding type
- `--embeddings LIST`: Multiple embeddings
- `--metrics LIST`: Metrics to visualize
- `--output DIR`: Output directory
- `--format FORMAT`: Output format (png, pdf, svg, html)
- `--interactive`: Generate interactive plots
- `--theme THEME`: Plot theme (default, dark, minimal)

### experiment

Run custom experiments with configuration files.

#### Basic Usage

```bash
# Run experiment from config
qdes-cli experiment --config experiment.yaml

# Override config parameters
qdes-cli experiment --config experiment.yaml --override "n_qubits=6,shots=2048"
```

#### Configuration File Format

```yaml
# experiment.yaml
name: "Quantum vs Classical Comparison"
description: "Compare quantum embeddings with classical methods"

dataset:
  name: "iris"
  # Or use custom data:
  # file: "data.csv"
  # target_column: "class"
  
preprocessing:
  normalize: true
  feature_selection: "top_k"
  k_features: 4

embeddings:
  - type: "angle"
    n_qubits: 4
    parameters:
      rotation_axis: "Y"
      entangling_layers: 1
      
  - type: "iqp"
    n_qubits: 4
    parameters:
      depth: 2
      connectivity: "linear"

quantum:
  backend: "qiskit"
  shots: 1024
  noise_model: null

evaluation:
  method: "cross_validation"
  cv_folds: 5
  metrics: ["accuracy", "precision", "recall", "f1_score"]
  
classical_baselines:
  - "rbf_svm"
  - "linear_svm"
  - "random_forest"

output:
  directory: "results/"
  format: "json"
  plots: true
  verbose: true
```

#### Advanced Configuration

```yaml
# advanced_experiment.yaml
name: "Large Scale Quantum Embedding Study"

datasets:
  - name: "iris"
  - name: "wine"
  - file: "custom_data.csv"
    target_column: "label"

embeddings:
  angle:
    n_qubits: [3, 4, 5]
    rotation_axis: ["X", "Y", "Z"]
    
  iqp:
    n_qubits: [4, 5, 6]
    depth: [1, 2, 3]
    connectivity: ["linear", "all_to_all"]

optimization:
  method: "grid_search"  # or "random_search", "bayesian"
  n_trials: 100
  timeout: 7200  # 2 hours
  
parallel:
  n_jobs: 4
  backend_parallel: true

hardware:
  test_real_devices: true
  devices: ["ibmq_qasm_simulator", "ibmq_manila"]
  
output:
  database: "results.sqlite"
  plots_format: "pdf"
  generate_report: true
```

#### Examples

```bash
# Simple experiment
qdes-cli experiment --config simple_experiment.yaml

# Override parameters
qdes-cli experiment \
    --config experiment.yaml \
    --override "quantum.shots=2048,evaluation.cv_folds=10"

# Parallel execution
qdes-cli experiment \
    --config large_experiment.yaml \
    --parallel 8 \
    --timeout 3600
```

## Advanced Features

### Configuration Files

Create default configuration files:

```bash
# Generate default config
qdes-cli config init

# Show current config
qdes-cli config show

# Set global defaults
qdes-cli config set backend qiskit
qdes-cli config set shots 1024
```

### Batch Processing

Process multiple datasets or configurations:

```bash
# Batch benchmark
qdes-cli batch benchmark \
    --configs experiments/*.yaml \
    --output results/ \
    --parallel 4

# Batch comparison
qdes-cli batch compare \
    --datasets data/*.csv \
    --embeddings angle,iqp \
    --output comparisons/
```

### Plugin System

Extend functionality with plugins:

```bash
# List available plugins
qdes-cli plugins list

# Install plugin
qdes-cli plugins install qdes-optimization

# Use plugin command
qdes-cli optimization tune --embedding angle --dataset iris
```

## Integration with Scripts

### Shell Scripts

```bash
#!/bin/bash
# benchmark_all.sh

datasets=("iris" "wine" "breast_cancer")
embeddings=("angle" "iqp" "amplitude")

for dataset in "${datasets[@]}"; do
    for embedding in "${embeddings[@]}"; do
        echo "Benchmarking $embedding on $dataset"
        qdes-cli benchmark \
            --dataset "$dataset" \
            --embedding "$embedding" \
            --n-qubits 4 \
            --output "results/${dataset}_${embedding}.json"
    done
done
```

### Python Integration

```python
import subprocess
import json

def run_benchmark(dataset, embedding, n_qubits):
    """Run CLI benchmark from Python"""
    cmd = [
        "qdes-cli", "benchmark",
        "--dataset", dataset,
        "--embedding", embedding,
        "--n-qubits", str(n_qubits),
        "--output", "temp_results.json"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        with open("temp_results.json", "r") as f:
            return json.load(f)
    else:
        raise RuntimeError(f"CLI command failed: {result.stderr}")

# Use in Python
results = run_benchmark("iris", "angle", 4)
print(f"Accuracy: {results['results']['angle_embedding']['accuracy']}")
```

### Jupyter Integration

```python
# In Jupyter notebook
!qdes-cli benchmark --dataset iris --embedding angle --n-qubits 4 --plot

# Load results
import json
with open("benchmark_results.json", "r") as f:
    results = json.load(f)
    
# Display results
import pandas as pd
df = pd.DataFrame(results['results']).T
display(df)
```

## Output Formats

### JSON Output

```json
{
  "metadata": {
    "timestamp": "2024-01-15T10:30:00Z",
    "version": "1.0.0",
    "command": "benchmark",
    "parameters": {...}
  },
  "results": {
    "quantum_results": {...},
    "classical_results": {...},
    "comparison": {...}
  },
  "metrics": {
    "execution_time": 120.5,
    "memory_usage": "2.1 GB",
    "quantum_advantage": 0.05
  }
}
```

### CSV Output

```bash
# Generate CSV output
qdes-cli benchmark \
    --dataset iris \
    --embeddings angle,iqp \
    --output results.csv \
    --format csv
```

### HTML Reports

```bash
# Generate HTML report
qdes-cli experiment \
    --config experiment.yaml \
    --output report.html \
    --format html
```

## Performance Optimization

### Parallel Execution

```bash
# Enable parallel processing
qdes-cli benchmark \
    --dataset large_dataset.csv \
    --embeddings angle,iqp,amplitude \
    --parallel 8 \
    --batch-size 100
```

### Caching

```bash
# Enable caching
qdes-cli --cache-dir ~/.qdes_cache benchmark \
    --dataset iris \
    --embedding angle \
    --n-qubits 4
```

### Memory Management

```bash
# Limit memory usage
qdes-cli benchmark \
    --dataset large_dataset.csv \
    --embedding amplitude \
    --memory-limit 8GB \
    --batch-size 50
```

## Troubleshooting

### Common Issues

#### Command Not Found

```bash
# Check installation
pip list | grep quantum-data-embedding-suite

# Reinstall if necessary
pip install --upgrade quantum-data-embedding-suite
```

#### Permission Errors

```bash
# Use user installation
pip install --user quantum-data-embedding-suite

# Or create virtual environment
python -m venv qdes-env
source qdes-env/bin/activate
pip install quantum-data-embedding-suite
```

#### Memory Issues

```bash
# Reduce batch size
qdes-cli benchmark --dataset large.csv --batch-size 10

# Use approximate methods
qdes-cli benchmark --dataset large.csv --approximate --n-samples 1000
```

### Debugging

```bash
# Enable verbose output
qdes-cli --verbose benchmark --dataset iris --embedding angle

# Debug mode
qdes-cli --debug benchmark --dataset iris --embedding angle

# Log to file
qdes-cli benchmark --dataset iris --embedding angle --log debug.log
```

### Getting Help

```bash
# General help
qdes-cli --help

# Command-specific help
qdes-cli benchmark --help
qdes-cli compare --help
qdes-cli visualize --help
qdes-cli experiment --help

# Show examples
qdes-cli examples
qdes-cli examples benchmark
```

## Best Practices

### Reproducibility

1. **Always set random seeds**

```bash
qdes-cli benchmark --dataset iris --embedding angle --seed 42
```

2. **Use configuration files** for complex experiments
3. **Version control** your configuration files
4. **Document parameters** in output files

### Performance

1. **Start small** with fewer qubits and samples
2. **Use appropriate shot counts** (1024 for development, more for production)
3. **Enable caching** for repeated experiments
4. **Use parallel execution** for multiple comparisons

### Organization

1. **Create structured output directories**

```bash
qdes-cli benchmark --output results/$(date +%Y%m%d)/
```

2. **Use descriptive filenames**
3. **Keep configuration files organized**
4. **Document your experiments**

## Examples and Templates

### Quick Start Templates

```bash
# Classification benchmark
qdes-cli benchmark \
    --dataset iris \
    --embedding angle \
    --n-qubits 4 \
    --output quick_benchmark.json

# Embedding comparison
qdes-cli compare \
    --embeddings angle,iqp,amplitude \
    --dataset wine \
    --n-qubits 4 \
    --output embedding_comparison.json

# Visualization
qdes-cli visualize metrics \
    --data data.csv \
    --embedding angle \
    --n-qubits 4 \
    --output plots/
```

### Production Templates

```yaml
# production_config.yaml
name: "Production Quantum ML Pipeline"
dataset:
  file: "production_data.csv"
  target_column: "target"
  
preprocessing:
  normalize: true
  feature_selection: "variance_threshold"
  
embeddings:
  - type: "angle"
    n_qubits: 6
    optimization: true
    
quantum:
  backend: "qiskit"
  shots: 8192
  noise_model: "ibmq_manila"
  
evaluation:
  method: "train_test_split"
  test_size: 0.2
  stratify: true
  
output:
  directory: "production_results/"
  database: "results.db"
  monitoring: true
```

## Further Reading

- [Configuration Guide](../configuration.md)
- [API Reference](../api/cli.md)
- [Automation Examples](../examples/automation.md)
- [Integration Patterns](../examples/integration.md)
