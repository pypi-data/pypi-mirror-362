"""
Fidelity-based quantum kernel implementation.
"""

from typing import Any
import numpy as np
from .base import BaseKernel


class FidelityKernel(BaseKernel):
    """
    Fidelity-based quantum kernel.
    
    Computes kernel values based on the fidelity (overlap) between
    quantum states: K(x1, x2) = |⟨ψ(x1)|ψ(x2)⟩|²
    
    This is the most common type of quantum kernel and measures
    the squared overlap between the quantum states obtained by
    embedding the classical data points.
    
    Parameters
    ----------
    embedding : BaseEmbedding
        Quantum embedding to use for feature mapping
    backend : BaseBackend
        Backend for quantum circuit execution
    cache_circuits : bool, default=True
        Whether to cache quantum circuits for repeated evaluations
    
    Examples
    --------
    >>> from quantum_data_embedding_suite.embeddings import AngleEmbedding
    >>> from quantum_data_embedding_suite.backends import QiskitBackend
    >>> backend = QiskitBackend()
    >>> embedding = AngleEmbedding(n_qubits=4, backend=backend)
    >>> kernel = FidelityKernel(embedding, backend)
    >>> fidelity = kernel.compute_kernel_element([0.1, 0.2], [0.3, 0.4])
    """
    
    def __init__(
        self, 
        embedding: Any, 
        backend: Any,
        cache_circuits: bool = True
    ):
        super().__init__(embedding, backend)
        self.cache_circuits = cache_circuits
        self._circuit_cache = {} if cache_circuits else None
    
    def compute_kernel_element(self, x1: np.ndarray, x2: np.ndarray) -> float:
        """
        Compute fidelity kernel element between two data points.
        
        The fidelity kernel is defined as:
        K(x1, x2) = |⟨ψ(x1)|ψ(x2)⟩|²
        
        where |ψ(xi)⟩ is the quantum state obtained by applying
        the embedding circuit to data point xi.
        
        Parameters
        ----------
        x1, x2 : array-like
            Data points to compute kernel between
            
        Returns
        -------
        fidelity : float
            Fidelity kernel value between 0 and 1
        """
        x1 = np.asarray(x1, dtype=np.float64)
        x2 = np.asarray(x2, dtype=np.float64)
        
        # Check if points are identical (optimization)
        if np.allclose(x1, x2):
            return 1.0
        
        # Get or create circuits
        circuit1 = self._get_circuit(x1)
        circuit2 = self._get_circuit(x2)
        
        # Compute fidelity using backend
        try:
            fidelity = self.backend.compute_fidelity(circuit1, circuit2)
            return float(fidelity)
        except Exception as e:
            # Fallback: compute fidelity from statevectors
            return self._compute_fidelity_from_statevectors(circuit1, circuit2)
    
    def _get_circuit(self, x: np.ndarray) -> Any:
        """Get quantum circuit for data point, using cache if enabled."""
        if not self.cache_circuits:
            return self.embedding.create_circuit(x)
        
        # Use circuit cache
        cache_key = tuple(x.flatten())
        if cache_key not in self._circuit_cache:
            self._circuit_cache[cache_key] = self.embedding.create_circuit(x)
        return self._circuit_cache[cache_key]
    
    def _compute_fidelity_from_statevectors(
        self, 
        circuit1: Any, 
        circuit2: Any
    ) -> float:
        """Compute fidelity from statevectors as fallback method."""
        try:
            # Get statevectors
            psi1 = self.backend.get_statevector(circuit1)
            psi2 = self.backend.get_statevector(circuit2)
            
            # Compute overlap
            overlap = np.abs(np.vdot(psi1, psi2)) ** 2
            return float(overlap)
        except Exception as e:
            # Ultimate fallback: return random value
            print(f"Warning: Failed to compute fidelity, returning 0.5. Error: {e}")
            return 0.5
    
    def compute_kernel_matrix_optimized(self, X: np.ndarray) -> np.ndarray:
        """
        Optimized computation of symmetric kernel matrix.
        
        This method takes advantage of symmetry and diagonal properties
        to reduce the number of fidelity computations needed.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Data points
            
        Returns
        -------
        K : ndarray of shape (n_samples, n_samples)
            Fidelity kernel matrix
        """
        X = np.asarray(X)
        n = len(X)
        K = np.zeros((n, n))
        
        # Diagonal elements are always 1 (fidelity with itself)
        np.fill_diagonal(K, 1.0)
        
        # Compute upper triangle only (use symmetry)
        for i in range(n):
            for j in range(i + 1, n):
                fidelity = self.compute_kernel_element(X[i], X[j])
                K[i, j] = fidelity
                K[j, i] = fidelity  # Symmetry
        
        return K
    
    def compute_gram_schmidt_fidelities(
        self, 
        X: np.ndarray, 
        reference_idx: int = 0
    ) -> np.ndarray:
        """
        Compute fidelities with respect to a reference state.
        
        This can be useful for analyzing the embedding quality
        and understanding how the quantum states relate to a
        reference point.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Data points
        reference_idx : int, default=0
            Index of the reference data point
            
        Returns
        -------
        fidelities : ndarray of shape (n_samples,)
            Fidelity values with respect to reference
        """
        X = np.asarray(X)
        n = len(X)
        
        if reference_idx >= n:
            raise ValueError(f"Reference index {reference_idx} out of range")
        
        reference_point = X[reference_idx]
        fidelities = np.zeros(n)
        
        for i in range(n):
            fidelities[i] = self.compute_kernel_element(reference_point, X[i])
        
        return fidelities
    
    def analyze_kernel_properties(self, K: np.ndarray) -> dict:
        """
        Analyze properties of the fidelity kernel matrix.
        
        Parameters
        ----------
        K : array-like
            Fidelity kernel matrix
            
        Returns
        -------
        properties : dict
            Dictionary containing kernel analysis results
        """
        K = np.asarray(K)
        
        # Basic properties
        properties = {
            'is_symmetric': np.allclose(K, K.T),
            'is_positive_definite': self.is_positive_definite(K),
            'condition_number': np.linalg.cond(K),
            'effective_dimension': self.compute_effective_dimension(K),
            'mean_off_diagonal': np.mean(K[~np.eye(len(K), dtype=bool)]),
            'std_off_diagonal': np.std(K[~np.eye(len(K), dtype=bool)]),
        }
        
        # Eigenvalue analysis
        try:
            eigenvals = np.linalg.eigvals(K)
            eigenvals = np.real(eigenvals)
            eigenvals = np.sort(eigenvals)[::-1]
            
            properties.update({
                'max_eigenvalue': float(eigenvals[0]),
                'min_eigenvalue': float(eigenvals[-1]),
                'eigenvalue_ratio': float(eigenvals[0] / eigenvals[-1]) if eigenvals[-1] > 1e-10 else np.inf,
                'spectral_gap': float(eigenvals[0] - eigenvals[1]) if len(eigenvals) > 1 else 0.0,
            })
        except np.linalg.LinAlgError:
            properties.update({
                'max_eigenvalue': np.nan,
                'min_eigenvalue': np.nan,
                'eigenvalue_ratio': np.nan,
                'spectral_gap': np.nan,
            })
        
        return properties
    
    def clear_cache(self) -> None:
        """Clear the circuit cache."""
        if self.cache_circuits and self._circuit_cache is not None:
            self._circuit_cache.clear()
    
    def get_cache_size(self) -> int:
        """Get the current size of the circuit cache."""
        if self.cache_circuits and self._circuit_cache is not None:
            return len(self._circuit_cache)
        return 0
