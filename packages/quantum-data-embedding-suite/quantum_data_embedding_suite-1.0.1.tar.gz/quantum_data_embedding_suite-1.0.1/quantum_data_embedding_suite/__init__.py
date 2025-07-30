"""
Quantum Data Embedding Suite

A comprehensive package for advanced classical-to-quantum data embedding techniques
designed to maximize quantum advantage in machine learning applications.
"""

__version__ = "0.1.0"
__author__ = "Krishna Bajpai"
__email__ = "bajpaikrishna715@gmail.com"

# License validation on package import
from .licensing import check_license_status, get_machine_id, validate_license_strict

# Strict license check on import - will block if grace period expired
try:
    validate_license_strict()
except Exception as e:
    # If license validation fails completely, block the import
    print(str(e))
    raise

# Check license status for warnings
_license_status = check_license_status()
if _license_status["status"] != "valid":
    print(f"⚠️  Quantum Data Embedding Suite - License Notice: {_license_status['message']}")
    print(f"Machine ID: {_license_status['machine_id']}")

from .pipeline import QuantumEmbeddingPipeline
from .embeddings import (
    AngleEmbedding,
    AmplitudeEmbedding,
    IQPEmbedding,
    DataReuploadingEmbedding,
    HamiltonianEmbedding,
)
from .kernels import QuantumKernel, FidelityKernel, ProjectedKernel
from .metrics import (
    expressibility,
    trainability,
    gradient_variance,
    effective_dimension,
)
from .licensing import get_machine_id, check_license_status

__all__ = [
    "QuantumEmbeddingPipeline",
    "AngleEmbedding",
    "AmplitudeEmbedding", 
    "IQPEmbedding",
    "DataReuploadingEmbedding",
    "HamiltonianEmbedding",
    "QuantumKernel",
    "FidelityKernel",
    "ProjectedKernel",
    "expressibility",
    "trainability",
    "gradient_variance",
    "effective_dimension",
    "get_machine_id",
    "check_license_status",
]
