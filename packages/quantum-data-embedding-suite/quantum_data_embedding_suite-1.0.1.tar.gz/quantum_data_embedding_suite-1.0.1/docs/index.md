# Quantum Data Embedding Suite

[![PyPI - Version](https://img.shields.io/pypi/v/quantum-data-embedding-suite?color=purple&label=PyPI&logo=pypi)](https://pypi.org/project/quantum-data-embedding-suite/)
[![PyPI Downloads](https://static.pepy.tech/badge/quantum-data-embedding-suite)](https://pepy.tech/projects/quantum-data-embedding-suite)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blacksvg)](https://www.python.org/downloads/)
[![License: Commercial](https://img.shields.io/badge/license-commercial-blueviolet?logo=briefcase)](https://krish567366.github.io/license-server/)
[![Docs](https://img.shields.io/badge/docs-online-blue?logo=readthedocs)](https://krish567366.github.io/quantum-data-embedding-suite/)

Welcome to the **Quantum Data Embedding Suite** - a comprehensive Python package for advanced classical-to-quantum data embedding techniques designed to maximize quantum advantage in machine learning applications.

## 🎯 What is Quantum Data Embedding?

Quantum data embedding is the process of encoding classical data into quantum states, enabling quantum algorithms to process classical information. The choice of embedding significantly impacts the performance of quantum machine learning algorithms, determining:

- **Expressibility**: How well the embedding can represent diverse quantum states
- **Trainability**: How effectively gradients can be computed for optimization
- **Quantum Advantage**: The potential for quantum speedup over classical methods

## ✨ Key Features

### Embedding Types

- **Angle Embedding**: Encode data as rotation angles in quantum gates
- **Amplitude Embedding**: Encode data directly in quantum state amplitudes  
- **IQP Embedding**: Instantaneous Quantum Polynomial circuits for data encoding
- **Data Re-uploading**: Multiple encoding layers for increased expressivity
- **Hamiltonian Embedding**: Physics-inspired encodings using problem Hamiltonians

### Quantum Kernels

- **Fidelity Kernels**: State overlap-based similarity measures
- **Projected Kernels**: Measurement-based kernel computation
- **Trainable Kernels**: Parameterized kernels with gradient-based optimization

### Quality Metrics

- **Expressibility**: Measure how uniformly embeddings cover Hilbert space
- **Trainability**: Analyze gradient magnitudes and barren plateau susceptibility
- **Gradient Variance**: Evaluate optimization landscape characteristics

### Advanced Features

- **Multi-Backend Support**: Seamless integration with Qiskit and PennyLane
- **Real QPU Support**: Execute on actual quantum hardware
- **Dimensionality Reduction**: Quantum PCA and SVD implementations
- **Benchmarking Tools**: Systematic classical vs quantum performance comparison
- **Interactive CLI**: Rapid experimentation with `qdes-cli` command-line interface
- **Extensible Design**: Plugin architecture for custom embeddings and metrics

## 🚀 Quick Start

```python
from quantum_data_embedding_suite import QuantumEmbeddingPipeline
from sklearn.datasets import load_iris
import numpy as np

# Load sample data
X, y = load_iris(return_X_y=True)
X = X[:50, :2]  # Use subset for demo

# Create quantum embedding pipeline
pipeline = QuantumEmbeddingPipeline(
    embedding_type="angle",
    n_qubits=4,
    backend="qiskit"
)

# Compute quantum kernel matrix
quantum_kernel = pipeline.fit_transform(X)

# Evaluate embedding quality
metrics = pipeline.evaluate_embedding(X)
print(f"Expressibility: {metrics['expressibility']:.3f}")
print(f"Trainability: {metrics['trainability']:.3f}")
```

## 📊 Why Quantum Embeddings Matter

Quantum embeddings can provide exponential advantages in certain machine learning tasks by:

- **Exploiting Quantum Superposition**: Representing data in superposition states
- **Leveraging Entanglement**: Creating complex correlations between features
- **Accessing Larger Feature Spaces**: Exponentially large Hilbert spaces
- **Enabling Quantum Kernels**: Computing kernels that are hard to evaluate classically

## 🔬 Research Applications

This package supports research in:

- **Quantum Machine Learning**: Developing quantum advantage in ML tasks
- **Quantum Feature Maps**: Designing expressive quantum embeddings
- **Barren Plateau Analysis**: Understanding trainability in quantum circuits
- **Quantum Kernel Methods**: Exploring quantum-enhanced kernel machines
- **NISQ Algorithms**: Practical quantum computing applications

## 🛠️ Installation

```bash
pip install quantum-data-embedding-suite
```

For development:

```bash
git clone https://github.com/krish567366/quantum-data-embedding-suite.git
cd quantum-data-embedding-suite
pip install -e ".[dev,docs]"
```

## 📚 Documentation Structure

- **[Getting Started](installation.md)**: Installation and basic setup
- **[User Guide](user_guide/embeddings.md)**: Detailed explanations of all components
- **[Tutorials](examples/basic_workflow.ipynb)**: Step-by-step Jupyter notebooks
- **[API Reference](api/pipeline.md)**: Complete API documentation
- **[Examples](examples/index.md)**: Gallery of practical examples

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](contributing.md) for details on:

- Submitting bug reports and feature requests
- Contributing code and documentation
- Adding new embedding types or metrics
- Improving performance and compatibility

## 📄 Citation

If you use this package in your research, please cite:

```bibtex
@software{quantum_data_embedding_suite,
  title={Quantum Data Embedding Suite: Advanced Classical-to-Quantum Data Embedding for QML},
  author={Krishna Bajpai},
  year={2025},
  url={https://github.com/krish567366/quantum-data-embedding-suite}
}
```

## 📞 Support

- **Documentation**: [Full Documentation](https://krish567366.github.io/quantum-data-embedding-suite)
- **Issues**: [GitHub Issues](https://github.com/krish567366/quantum-data-embedding-suite/issues)
- **Discussions**: [GitHub Discussions](https://github.com/krish567366/quantum-data-embedding-suite/discussions)
- **Email**: bajpaikrishna715@gmail.com

---

**Author**: Krishna Bajpai  
**License**: MIT  
**Version**: 0.1.0
