# Installation

This page provides detailed installation instructions for the Quantum Data Embedding Suite.

## Requirements

### System Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, or Linux
- **Memory**: At least 4GB RAM (8GB+ recommended for larger quantum circuits)
- **Disk Space**: ~500MB for the package and dependencies

### Python Dependencies

The package has the following core dependencies:

```pip
numpy>=1.21.0
scipy>=1.7.0
scikit-learn>=1.0.0
matplotlib>=3.5.0
seaborn>=0.11.0
pandas>=1.3.0
tqdm>=4.62.0
pyyaml>=6.0
click>=8.0.0
qiskit>=0.45.0
```

### Optional Dependencies

For enhanced functionality, you can install additional packages:

```pip
pennylane>=0.32.0          # Alternative quantum backend
amazon-braket-sdk>=1.50.0  # AWS Braket support
qiskit-ibm-runtime>=0.15.0 # IBM Quantum support
cirq-ionq>=1.0.0          # IonQ support
plotly>=5.0.0             # Interactive visualizations
jupyter>=1.0.0            # Notebook support
scikit-optimize>=0.9.0    # Bayesian optimization
```

## Installation Methods

### 1. Standard Installation (Recommended)

Install the latest stable version from PyPI:

```bash
pip install quantum-data-embedding-suite
```

This will install the package with all core dependencies.

### 2. Installation with Optional Dependencies

For full functionality including all backends and visualization tools:

```bash
pip install quantum-data-embedding-suite[all]
```

Or install specific optional dependencies:

```bash
# For AWS Braket support
pip install quantum-data-embedding-suite[aws]

# For IBM Quantum support  
pip install quantum-data-embedding-suite[ibm]

# For IonQ support
pip install quantum-data-embedding-suite[ionq]

# For documentation building
pip install quantum-data-embedding-suite[docs]

# For development
pip install quantum-data-embedding-suite[dev]
```

### 3. Development Installation

For contributors or users who want the latest features:

```bash
git clone https://github.com/krish567366/quantum-data-embedding-suite.git
cd quantum-data-embedding-suite
pip install -e ".[dev,docs]"
```

The `-e` flag installs the package in "editable" mode, so changes to the source code are immediately reflected.

### 4. Conda Installation

If you prefer using conda:

```bash
# Create a new environment (recommended)
conda create -n qdes python=3.9
conda activate qdes

# Install from conda-forge (when available)
conda install -c conda-forge quantum-data-embedding-suite

# Or install via pip in the conda environment
pip install quantum-data-embedding-suite
```

## Verification

After installation, verify that everything is working correctly:

```python
import quantum_data_embedding_suite as qdes
print(f"QDES version: {qdes.__version__}")

# Test basic functionality
from quantum_data_embedding_suite import QuantumEmbeddingPipeline
import numpy as np

# Create a simple test
X = np.random.randn(10, 4)
pipeline = QuantumEmbeddingPipeline(
    embedding_type="angle",
    n_qubits=4,
    backend="qiskit"
)

try:
    K = pipeline.fit_transform(X)
    print("✅ Installation successful!")
    print(f"Quantum kernel shape: {K.shape}")
except Exception as e:
    print(f"❌ Installation issue: {e}")
```

You can also use the CLI to verify installation:

```bash
qdes-cli --version
qdes-cli benchmark --dataset random --embedding angle --n-qubits 2
```

## Backend Setup

### Qiskit (Default)

Qiskit is included by default. For IBM Quantum device access:

1. Create an IBM Quantum account at [quantum-computing.ibm.com](https://quantum-computing.ibm.com)
2. Install IBM Quantum support:

   ```bash
   pip install qiskit-ibm-runtime
   ```

3. Save your credentials:

   ```python
   from qiskit_ibm_runtime import QiskitRuntimeService
   QiskitRuntimeService.save_account(channel="ibm_quantum", token="YOUR_TOKEN")
   ```

### PennyLane (Optional)

For PennyLane backend support:

```bash
pip install pennylane
```

Test PennyLane installation:

```python
import pennylane as qml
print(f"PennyLane version: {qml.__version__}")

# List available devices
print("Available devices:", qml.about())
```

### AWS Braket (Optional)

For AWS Braket support:

1. Install the SDK:

   ```bash
   pip install amazon-braket-sdk
   ```

2. Configure AWS credentials:

   ```bash
   aws configure
   ```

3. Test access:

   ```python
   from braket.aws import AwsDevice
   device = AwsDevice("arn:aws:braket:::device/qpu/ionq/ionQdevice")
   ```

## Troubleshooting

### Common Issues

#### Installation Failures

**Issue**: `pip install` fails with dependency conflicts
**Solution**: Use a fresh virtual environment:

```bash
python -m venv qdes_env
source qdes_env/bin/activate  # On Windows: qdes_env\Scripts\activate
pip install quantum-data-embedding-suite
```

**Issue**: Compilation errors during installation
**Solution**: Upgrade pip and setuptools:

```bash
pip install --upgrade pip setuptools wheel
pip install quantum-data-embedding-suite
```

#### Import Errors

**Issue**: `ModuleNotFoundError` when importing
**Solution**: Verify installation in the correct environment:

```bash
python -c "import sys; print(sys.path)"
pip list | grep quantum
```

**Issue**: Qiskit or PennyLane import errors
**Solution**: Install quantum backends separately:

```bash
pip install qiskit pennylane
```

#### Performance Issues

**Issue**: Slow quantum simulations
**Solution**:

- Reduce number of qubits for testing
- Use fewer shots initially
- Consider using GPU-accelerated simulators

#### Memory Issues

**Issue**: Out of memory errors
**Solution**:

- Use smaller datasets for initial testing
- Reduce batch sizes
- Monitor memory usage with `htop` or Task Manager

### Platform-Specific Notes

#### Windows

- Install Microsoft Visual C++ Build Tools if you encounter compilation errors
- Use Windows Subsystem for Linux (WSL) for better compatibility with quantum packages

#### macOS

- Install Xcode Command Line Tools: `xcode-select --install`
- For Apple Silicon Macs, some quantum packages may require Rosetta 2

#### Linux

- Install build dependencies:

  ```bash
  sudo apt-get update
  sudo apt-get install build-essential python3-dev
  ```

### Getting Help

If you encounter issues not covered here:

1. **Check the logs**: Look for detailed error messages
2. **Search existing issues**: Visit our [GitHub Issues](https://github.com/krish567366/quantum-data-embedding-suite/issues)
3. **Create a minimal example**: Isolate the problem to help with debugging
4. **Report the issue**: Include your environment details and error messages

## Next Steps

After successful installation:

1. **Read the [Quick Start Guide](quick_start.md)** for your first quantum embedding
2. **Explore the [User Guide](user_guide.md)** for detailed feature explanations
3. **Try the [Tutorials](tutorials/basic_workflow.md)** for hands-on learning
4. **Check out [Examples](examples/index.md)** for practical applications

## Environment Template

Here's a recommended `environment.yml` for conda users:

```yaml
name: qdes
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.9
  - numpy
  - scipy
  - scikit-learn
  - matplotlib
  - pandas
  - jupyter
  - pip
  - pip:
    - quantum-data-embedding-suite[all]
```

Save this as `environment.yml` and create the environment with:

```bash
conda env create -f environment.yml
conda activate qdes
```
