"""
Quantum kernel implementations.
"""

from .base import BaseKernel
from .fidelity import FidelityKernel
from .projected import ProjectedKernel
from .trainable import TrainableKernel

# Main quantum kernel class
QuantumKernel = FidelityKernel  # Default to fidelity kernel

__all__ = [
    "BaseKernel",
    "QuantumKernel", 
    "FidelityKernel",
    "ProjectedKernel",
    "TrainableKernel",
]
