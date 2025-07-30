"""
Projected quantum kernel implementation.
"""

from typing import Any, Optional
import numpy as np
from .base import BaseKernel


class ProjectedKernel(BaseKernel):
    """
    Projected quantum kernel that measures specific observables.
    
    Instead of computing full state fidelity, this kernel computes
    expectation values of specific observables on the quantum states,
    providing a different notion of similarity.
    
    Parameters
    ----------
    embedding : BaseEmbedding
        Quantum embedding to use for feature mapping
    backend : BaseBackend
        Backend for quantum circuit execution
    observable : str or object, default='Z'
        Observable to measure ('Z', 'X', 'Y', or custom observable)
    qubits : list of int, optional
        Qubits to measure (defaults to all qubits)
    """
    
    def __init__(
        self, 
        embedding: Any, 
        backend: Any,
        observable: str = "Z",
        qubits: Optional[list] = None
    ):
        super().__init__(embedding, backend)
        self.observable_str = observable
        self.qubits = qubits or list(range(embedding.n_qubits))
        
        # Create observable
        self.observable = self._create_observable()
    
    def _create_observable(self) -> Any:
        """Create the observable object."""
        if isinstance(self.observable_str, str):
            # Create Pauli observable
            pauli_string = self.observable_str * len(self.qubits)
            return self.backend.create_observable(pauli_string, self.qubits)
        else:
            # Use provided observable
            return self.observable_str
    
    def compute_kernel_element(self, x1: np.ndarray, x2: np.ndarray) -> float:
        """
        Compute projected kernel element between two data points.
        
        The projected kernel is defined as:
        K(x1, x2) = ⟨ψ(x1)|O|ψ(x1)⟩ * ⟨ψ(x2)|O|ψ(x2)⟩
        
        where O is the observable and |ψ(xi)⟩ are the embedded states.
        
        Parameters
        ----------
        x1, x2 : array-like
            Data points to compute kernel between
            
        Returns
        -------
        kernel_value : float
            Projected kernel value
        """
        x1 = np.asarray(x1, dtype=np.float64)
        x2 = np.asarray(x2, dtype=np.float64)
        
        # Create circuits
        circuit1 = self.embedding.create_circuit(x1)
        circuit2 = self.embedding.create_circuit(x2)
        
        # Compute expectation values
        exp1 = self.backend.compute_expectation(circuit1, self.observable)
        exp2 = self.backend.compute_expectation(circuit2, self.observable)
        
        # Kernel is product of expectation values
        return float(exp1 * exp2)
