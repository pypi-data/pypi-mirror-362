#!/usr/bin/env python3
"""
Setup script for Quantum Data Embedding Suite.

This package provides advanced classical-to-quantum data embedding techniques
for quantum machine learning applications.

Author: Krishna Bajpai
GitHub: https://github.com/krish567366/quantum-data-embedding-suite
Documentation: https://krish567366.github.io/quantum-data-embedding-suite
"""

import os
import sys
from pathlib import Path
from setuptools import setup, find_packages

# Ensure we're in the right directory
here = Path(__file__).parent.absolute()

# Read the README file
def read_readme():
    """Read the README.md file for long description."""
    readme_path = here / "README.md"
    if readme_path.exists():
        with open(readme_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

# Read requirements from requirements.txt if it exists
def read_requirements(filename):
    """Read requirements from a file."""
    req_path = here / filename
    if req_path.exists():
        with open(req_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return []

# Version information
def get_version():
    """Get version from __init__.py or use default."""
    init_path = here / "quantum_data_embedding_suite" / "__init__.py"
    if init_path.exists():
        with open(init_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("__version__"):
                    return line.split("=")[1].strip().strip('"').strip("'")
    return "0.1.0"

# Core dependencies
install_requires = [
    "qiskit>=0.45.0",
    "pennylane>=0.32.0", 
    "numpy>=1.21.0",
    "scipy>=1.7.0",
    "scikit-learn>=1.0.0",
    "matplotlib>=3.5.0",
    "seaborn>=0.11.0",
    "pandas>=1.3.0",
    "tqdm>=4.62.0",
    "pyyaml>=6.0",
    "click>=8.0.0",
    "jupyter>=1.0.0",
    "ipywidgets>=7.6.0",
    "plotly>=5.0.0",
    "scikit-optimize>=0.9.0",
    "quantummeta-license>=1.0.0",  # New dependency for license management
]

# Development dependencies
dev_requires = [
    "pytest>=6.0",
    "pytest-cov>=3.0",
    "black>=22.0",
    "flake8>=4.0",
    "mypy>=0.950",
    "pre-commit>=2.15",
]

# Documentation dependencies
docs_requires = [
    "mkdocs>=1.4.0",
    "mkdocs-material>=8.5.0",
    "mkdocstrings[python]>=0.19.0",
    "mkdocs-jupyter>=0.21.0",
    "mkdocs-gallery>=0.7.0",
]

# Cloud platform dependencies
aws_requires = ["amazon-braket-sdk>=1.50.0"]
ibm_requires = ["qiskit-ibm-runtime>=0.15.0"]
ionq_requires = ["cirq-ionq>=1.0.0"]

# All optional dependencies
all_requires = dev_requires + docs_requires + aws_requires + ibm_requires + ionq_requires

# Classifiers
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Science/Research",
    "Intended Audience :: Developers",
    "License :: Other/Proprietary License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3 :: Only",
    "Topic :: Scientific/Engineering",
    "Topic :: Scientific/Engineering :: Physics",
    "Topic :: Scientific/Engineering :: Artificial Intelligence",
    "Topic :: Software Development :: Libraries",
    "Topic :: Software Development :: Libraries :: Python Modules",
]

# Keywords
keywords = [
    "quantum",
    "quantum computing",
    "quantum machine learning",
    "qml",
    "data embedding",
    "quantum embedding",
    "quantum kernels",
    "qiskit",
    "pennylane",
    "variational quantum circuits",
    "vqc",
    "quantum neural networks",
    "qnn",
]

setup(
    # Package metadata
    name="quantum-data-embedding-suite",
    version=get_version(),
    author="Krishna Bajpai",
    author_email="bajpaikrishna715@gmail.com",
    description="Advanced classical-to-quantum data embedding techniques for quantum machine learning",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    license="MIT",
    
    # URLs
    url="https://github.com/krish567366/quantum-data-embedding-suite",
    project_urls={
        "Homepage": "https://github.com/krish567366/quantum-data-embedding-suite",
        "Documentation": "https://krish567366.github.io/quantum-data-embedding-suite",
        "Source Code": "https://github.com/krish567366/quantum-data-embedding-suite",
        "Bug Tracker": "https://github.com/krish567366/quantum-data-embedding-suite/issues",
        "Changelog": "https://krish567366.github.io/quantum-data-embedding-suite/changelog/",
        "Contributing": "https://krish567366.github.io/quantum-data-embedding-suite/contributing/",
    },
    
    # Package discovery
    packages=find_packages(include=["quantum_data_embedding_suite*"]),
    include_package_data=True,
    
    # Python version requirement
    python_requires=">=3.8",
    
    # Dependencies
    install_requires=install_requires,
    extras_require={
        "dev": dev_requires,
        "docs": docs_requires,
        "aws": aws_requires,
        "ibm": ibm_requires,
        "ionq": ionq_requires,
        "all": all_requires,
    },
    
    # Classification
    classifiers=classifiers,
    keywords=", ".join(keywords),
    
    # Entry points
    entry_points={
        "console_scripts": [
            "qdes-cli=quantum_data_embedding_suite.cli:main",
            "quantum-embedding=quantum_data_embedding_suite.cli:main",
        ],
    },
    
    # Package data
    package_data={
        "quantum_data_embedding_suite": [
            "*.yaml",
            "*.yml", 
            "*.json",
            "configs/*.yaml",
            "configs/*.yml",
            "configs/*.json",
        ],
    },
    
    # Data files
    data_files=[
        ("", ["README.md", "LICENSE"]),
    ],
    
    # Additional metadata
    zip_safe=False,
    
    # Setuptools options
    options={
        "build_py": {
            "compile": True,
            "optimize": 2,
        },
    },
)

# Post-installation message
if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 Quantum Data Embedding Suite Installation Complete!")
    print("="*60)
    print("📚 Documentation: https://krish567366.github.io/quantum-data-embedding-suite")
    print("🐙 GitHub: https://github.com/krish567366/quantum-data-embedding-suite")
    print("🔧 CLI Usage: qdes-cli --help")
    print("📦 Import: from quantum_data_embedding_suite import *")
    print("\n💡 Quick Start:")
    print("   from quantum_data_embedding_suite import EmbeddingPipeline")
    print("   pipeline = EmbeddingPipeline()")
    print("   pipeline.run(data)")
    print("="*60)
