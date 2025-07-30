# Contributing Guide

Thank you for your interest in contributing to the Quantum Data Embedding Suite! This guide will help you get started with contributing to the project.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Guidelines](#contributing-guidelines)
- [Code Standards](#code-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Submitting Changes](#submitting-changes)
- [Community](#community)

## Getting Started

### Ways to Contribute

We welcome contributions in many forms:

- **Bug Reports**: Help us identify and fix issues
- **Feature Requests**: Suggest new functionality
- **Code Contributions**: Implement new features or fix bugs
- **Documentation**: Improve docs, examples, and tutorials
- **Testing**: Add test cases and improve coverage
- **Examples**: Create new use case demonstrations
- **Performance**: Optimize algorithms and implementations

### Before You Start

1. Check existing [issues](https://github.com/your-repo/quantum-data-embedding-suite/issues) to avoid duplicates
2. Read through this contributing guide
3. Review the [Code of Conduct](CODE_OF_CONDUCT.md)
4. Join our [community discussions](https://github.com/your-repo/quantum-data-embedding-suite/discussions)

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- Virtual environment manager (venv, conda, or poetry)

### Environment Setup

1. **Fork and Clone the Repository**

   ```bash
   git clone https://github.com/krish567366/quantum-data-embedding-suite.git
   cd quantum-data-embedding-suite
   ```

2. **Create Virtual Environment**

   ```bash
   # Using venv
   python -m venv quantum_env
   source quantum_env/bin/activate  # On Windows: quantum_env\Scripts\activate
   
   # Using conda
   conda create -n quantum_env python=3.8
   conda activate quantum_env
   ```

3. **Install Development Dependencies**

   ```bash
   # Install package in development mode
   pip install -e .
   
   # Install development dependencies
   pip install -e ".[dev,test,docs]"
   ```

4. **Install Pre-commit Hooks**

   ```bash
   pre-commit install
   ```

5. **Verify Installation**

   ```bash
   python -c "import quantum_data_embedding_suite; print('Installation successful!')"
   pytest tests/ -v
   ```

### Development Tools

We use the following tools for development:

- **Code Formatting**: Black, isort
- **Linting**: flake8, pylint
- **Type Checking**: mypy
- **Testing**: pytest, pytest-cov
- **Documentation**: MkDocs, mkdocs-material
- **Pre-commit**: Automated code quality checks

## Contributing Guidelines

### Issue Guidelines

**Bug Reports**

- Use the bug report template
- Include minimal reproducible example
- Specify Python version, OS, and package versions
- Include error messages and stack traces

**Feature Requests**

- Use the feature request template
- Describe the use case and motivation
- Provide example usage if possible
- Consider implementation complexity

### Code Contribution Workflow

1. **Create Issue**: Discuss major changes in an issue first
2. **Fork Repository**: Create your own fork
3. **Create Branch**: Use descriptive branch names
4. **Make Changes**: Follow code standards
5. **Add Tests**: Ensure good test coverage
6. **Update Docs**: Update relevant documentation
7. **Submit PR**: Create pull request with clear description

### Branch Naming

Use descriptive branch names:

- `feature/add-quantum-embedding`
- `bugfix/fix-kernel-computation`
- `docs/improve-installation-guide`
- `refactor/simplify-backend-interface`

## Code Standards

### Python Style Guide

We follow PEP 8 with some modifications:

```python
# Line length: 88 characters (Black default)
# Imports: isort configuration
# Docstrings: Google style

def example_function(param1: str, param2: int = 10) -> Dict[str, Any]:
    """
    Example function demonstrating our coding standards.
    
    Args:
        param1: Description of first parameter.
        param2: Description of second parameter with default value.
        
    Returns:
        Dictionary containing results.
        
    Raises:
        ValueError: If param1 is empty.
        
    Example:
        >>> result = example_function("hello", 20)
        >>> print(result['status'])
        'success'
    """
    if not param1:
        raise ValueError("param1 cannot be empty")
    
    return {"status": "success", "value": param1 * param2}
```

### Code Quality Checks

Run these checks before submitting:

```bash
# Format code
black quantum_data_embedding_suite/ tests/
isort quantum_data_embedding_suite/ tests/

# Lint code
flake8 quantum_data_embedding_suite/ tests/
pylint quantum_data_embedding_suite/

# Type checking
mypy quantum_data_embedding_suite/

# Run all pre-commit hooks
pre-commit run --all-files
```

### Architecture Guidelines

**Modularity**

- Keep classes focused and single-purpose
- Use composition over inheritance where appropriate
- Implement proper interfaces and abstractions

**Error Handling**

- Use specific exception types
- Provide helpful error messages
- Include context in error messages

**Performance**

- Profile code for bottlenecks
- Use appropriate data structures
- Consider memory usage for large datasets

**Documentation**

- Write clear docstrings for all public APIs
- Include examples in docstrings
- Keep documentation up to date

## Testing

### Test Structure

```bash
tests/
├── unit/                    # Unit tests
│   ├── test_pipeline.py
│   ├── test_embeddings.py
│   └── test_backends.py
├── integration/             # Integration tests
│   ├── test_workflows.py
│   └── test_examples.py
├── performance/             # Performance tests
│   └── test_benchmarks.py
└── fixtures/                # Test data and fixtures
    └── sample_data.py
```

### Writing Tests

**Unit Tests**

```python
import pytest
import numpy as np
from quantum_data_embedding_suite import QuantumEmbeddingPipeline

class TestQuantumEmbeddingPipeline:
    """Test cases for QuantumEmbeddingPipeline."""
    
    def test_init_valid_parameters(self):
        """Test pipeline initialization with valid parameters."""
        pipeline = QuantumEmbeddingPipeline(
            embedding_type="angle",
            n_qubits=4,
            backend="qiskit"
        )
        assert pipeline.embedding_type == "angle"
        assert pipeline.n_qubits == 4
    
    def test_init_invalid_embedding_type(self):
        """Test pipeline initialization with invalid embedding type."""
        with pytest.raises(ValueError, match="Invalid embedding type"):
            QuantumEmbeddingPipeline(embedding_type="invalid")
    
    @pytest.mark.parametrize("n_qubits", [1, 2, 3, 4, 5])
    def test_different_qubit_counts(self, n_qubits):
        """Test pipeline with different qubit counts."""
        pipeline = QuantumEmbeddingPipeline(n_qubits=n_qubits)
        assert pipeline.n_qubits == n_qubits
```

**Integration Tests**

```python
def test_full_workflow():
    """Test complete workflow from data to predictions."""
    # Generate sample data
    X = np.random.randn(50, 4)
    y = np.random.randint(0, 2, 50)
    
    # Create pipeline
    pipeline = QuantumEmbeddingPipeline(
        embedding_type="angle",
        n_qubits=4
    )
    
    # Compute kernel
    K = pipeline.fit_transform(X)
    
    # Validate results
    assert K.shape == (50, 50)
    assert np.allclose(K, K.T)  # Symmetry
    assert np.all(np.diag(K) >= 0.8)  # Self-similarity
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=quantum_data_embedding_suite --cov-report=html

# Run specific test file
pytest tests/unit/test_pipeline.py

# Run with specific markers
pytest -m "not slow"

# Run in parallel
pytest -n auto
```

### Test Data

Use fixtures for consistent test data:

```python
@pytest.fixture
def sample_data():
    """Generate sample data for testing."""
    np.random.seed(42)
    X = np.random.randn(30, 4)
    y = np.random.randint(0, 3, 30)
    return X, y

@pytest.fixture
def quantum_pipeline():
    """Create quantum pipeline for testing."""
    return QuantumEmbeddingPipeline(
        embedding_type="angle",
        n_qubits=4,
        backend="qiskit",
        shots=1024,
        random_state=42
    )
```

## Documentation

### Documentation Structure

```bash
docs/
├── index.md                 # Main landing page
├── installation.md          # Installation instructions
├── quick_start.md          # Quick start guide
├── user_guide.md           # Comprehensive user guide
├── api/                    # API reference
├── tutorials/              # Step-by-step tutorials
├── examples/               # Example gallery
└── contributing.md         # This file
```

### Writing Documentation

**API Documentation**

- Use Google-style docstrings
- Include parameter types and descriptions
- Provide usage examples
- Document exceptions

**Tutorials**

- Start with learning objectives
- Provide complete, runnable examples
- Explain concepts clearly
- Include troubleshooting tips

**Examples**

- Focus on specific use cases
- Include data preparation steps
- Show expected outputs
- Provide interpretation of results

### Building Documentation

```bash
# Install documentation dependencies
pip install -e ".[docs]"

# Build documentation
mkdocs build

# Serve documentation locally
mkdocs serve

# Deploy to GitHub Pages
mkdocs gh-deploy
```

## Submitting Changes

### Pull Request Process

1. **Update Documentation**: Ensure docs are updated
2. **Add Tests**: Include tests for new functionality
3. **Update Changelog**: Add entry to CHANGELOG.md
4. **Run Checks**: Ensure all CI checks pass
5. **Create PR**: Use the pull request template

### Pull Request Template

```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that breaks existing functionality)
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] Manual testing performed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Changelog updated
```

### Review Process

1. **Automated Checks**: CI/CD pipeline runs automatically
2. **Code Review**: Maintainers review code and provide feedback
3. **Iteration**: Address feedback and update PR
4. **Approval**: At least one maintainer approval required
5. **Merge**: Maintainer merges the PR

## Community

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and discussions
- **Pull Requests**: Code review and collaboration

### Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please read our [Code of Conduct](CODE_OF_CONDUCT.md) and help us maintain a positive community.

### Getting Help

- **Documentation**: Check the docs first
- **Search Issues**: Look for similar problems
- **Ask Questions**: Use GitHub Discussions
- **Stack Overflow**: Tag questions with `quantum-embedding`

### Recognition

Contributors are recognized in:

- CONTRIBUTORS.md file
- Release notes
- Documentation acknowledgments

## Release Process

### Version Numbering

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

1. Update version numbers
2. Update CHANGELOG.md
3. Create release branch
4. Run full test suite
5. Build and test documentation
6. Create GitHub release
7. Upload to PyPI
8. Announce release

## Advanced Topics

### Performance Optimization

- Profile code using `cProfile` and `memory_profiler`
- Use `numpy` operations for vectorization
- Consider `numba` for computational bottlenecks
- Implement caching for expensive operations

### Adding New Embedding Types

1. Inherit from `BaseEmbedding`
2. Implement required methods
3. Add to factory in `__init__.py`
4. Write comprehensive tests
5. Add documentation and examples

### Backend Development

1. Inherit from `BaseBackend`
2. Implement quantum circuit execution
3. Handle device-specific optimizations
4. Add error handling and validation
5. Write integration tests

## Thank You

Thank you for contributing to the Quantum Data Embedding Suite! Your contributions help advance quantum machine learning research and make these tools accessible to the broader community.
