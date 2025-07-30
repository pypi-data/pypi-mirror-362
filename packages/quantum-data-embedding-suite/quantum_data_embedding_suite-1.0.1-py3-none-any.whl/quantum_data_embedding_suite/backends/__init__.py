"""
Backend implementations for different quantum computing frameworks.
"""

from .base import BaseBackend
from .qiskit_backend import QiskitBackend
from .pennylane_backend import PennyLaneBackend

# Registry of available backends
BACKEND_REGISTRY = {
    "qiskit": QiskitBackend,
    "pennylane": PennyLaneBackend,
}


def get_backend(backend: str, device: str = None, shots: int = 1024, **kwargs) -> BaseBackend:
    """
    Factory function to create backend instances.
    
    Parameters
    ----------
    backend : str
        Backend name ('qiskit', 'pennylane')
    device : str, optional
        Specific device/simulator to use
    shots : int, default=1024
        Number of measurement shots
    **kwargs
        Additional backend-specific parameters
        
    Returns
    -------
    backend_instance : BaseBackend
        Initialized backend instance
    """
    if backend not in BACKEND_REGISTRY:
        raise ValueError(f"Unknown backend: {backend}. Available: {list(BACKEND_REGISTRY.keys())}")
    
    backend_class = BACKEND_REGISTRY[backend]
    return backend_class(device=device, shots=shots, **kwargs)


__all__ = [
    "BaseBackend",
    "QiskitBackend", 
    "PennyLaneBackend",
    "get_backend",
    "BACKEND_REGISTRY",
]
