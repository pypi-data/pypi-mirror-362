"""
Base class for quantum embeddings.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Union
import numpy as np
from ..licensing import validate_license_for_class


class BaseEmbedding(ABC):
    """
    Abstract base class for quantum data embeddings.
    
    All embedding implementations should inherit from this class and implement
    the required abstract methods.
    
    Parameters
    ----------
    n_qubits : int
        Number of qubits in the embedding circuit
    backend : object
        Backend instance for quantum circuit execution
    """
    
    def __init__(self, n_qubits: int, backend: Any, **kwargs):
        # License validation for all embedding classes
        validate_license_for_class(self.__class__)
        
        self.n_qubits = n_qubits
        self.backend = backend
        self.params = kwargs
        self._circuit_cache = {}
        
    @abstractmethod
    def create_circuit(self, x: np.ndarray) -> Any:
        """
        Create a quantum circuit for embedding a single data point.
        
        Parameters
        ----------
        x : array-like of shape (n_features,)
            Classical data point to embed
            
        Returns
        -------
        circuit : quantum circuit object
            Backend-specific quantum circuit
        """
        pass
    
    @abstractmethod
    def get_feature_dimension(self) -> int:
        """
        Get the expected dimension of input features.
        
        Returns
        -------
        n_features : int
            Number of classical features this embedding expects
        """
        pass
    
    @property
    def depth(self) -> int:
        """
        Get the depth of the embedding circuit.
        
        Returns
        -------
        depth : int
            Circuit depth (number of layers)
        """
        return getattr(self, '_depth', 1)
    
    @property
    def n_parameters(self) -> int:
        """
        Get the number of trainable parameters in the embedding.
        
        Returns
        -------
        n_params : int
            Number of trainable parameters
        """
        return getattr(self, '_n_parameters', 0)
    
    def fit(self, X: np.ndarray) -> "BaseEmbedding":
        """
        Fit the embedding to training data (if needed).
        
        Some embeddings may need to fit parameters based on the data distribution.
        Default implementation does nothing.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training data
            
        Returns
        -------
        self : BaseEmbedding
            Returns self for method chaining
        """
        return self
    
    def validate_input(self, x: np.ndarray) -> np.ndarray:
        """
        Validate and preprocess input data.
        
        Parameters
        ----------
        x : array-like
            Input data point
            
        Returns
        -------
        x : ndarray
            Validated and preprocessed data
        """
        x = np.asarray(x, dtype=np.float64)
        
        if x.ndim != 1:
            raise ValueError(f"Input must be 1D array, got {x.ndim}D")
            
        expected_features = self.get_feature_dimension()
        if len(x) != expected_features:
            raise ValueError(
                f"Expected {expected_features} features, got {len(x)}"
            )
            
        return x
    
    def get_circuit_hash(self, x: np.ndarray) -> str:
        """
        Generate a hash for circuit caching.
        
        Parameters
        ----------
        x : array-like
            Input data point
            
        Returns
        -------
        hash_str : str
            Hash string for the circuit
        """
        return str(hash(tuple(x.flatten())))
    
    def create_circuit_cached(self, x: np.ndarray) -> Any:
        """
        Create circuit with caching support.
        
        Parameters
        ----------
        x : array-like
            Input data point
            
        Returns
        -------
        circuit : quantum circuit object
            Backend-specific quantum circuit
        """
        x = self.validate_input(x)
        circuit_hash = self.get_circuit_hash(x)
        
        if circuit_hash not in self._circuit_cache:
            self._circuit_cache[circuit_hash] = self.create_circuit(x)
            
        return self._circuit_cache[circuit_hash]
    
    def clear_cache(self) -> None:
        """Clear the circuit cache."""
        self._circuit_cache.clear()
    
    def get_info(self) -> Dict[str, Any]:
        """
        Get information about the embedding.
        
        Returns
        -------
        info : dict
            Dictionary containing embedding information
        """
        return {
            "name": self.__class__.__name__,
            "n_qubits": self.n_qubits,
            "n_features": self.get_feature_dimension(),
            "depth": self.depth,
            "n_parameters": self.n_parameters,
            "backend": str(self.backend),
            "params": self.params,
        }
