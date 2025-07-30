"""
Quantum embedding implementations for classical data.
"""

from .base import BaseEmbedding
from .angle import AngleEmbedding
from .amplitude import AmplitudeEmbedding
from .iqp import IQPEmbedding
from .data_reuploading import DataReuploadingEmbedding
from .hamiltonian import HamiltonianEmbedding

# Registry of available embeddings
EMBEDDING_REGISTRY = {
    "angle": AngleEmbedding,
    "amplitude": AmplitudeEmbedding,
    "iqp": IQPEmbedding,
    "data_reuploading": DataReuploadingEmbedding,
    "hamiltonian": HamiltonianEmbedding,
}

__all__ = [
    "BaseEmbedding",
    "AngleEmbedding",
    "AmplitudeEmbedding",
    "IQPEmbedding", 
    "DataReuploadingEmbedding",
    "HamiltonianEmbedding",
    "EMBEDDING_REGISTRY",
]
