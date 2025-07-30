"""
Core pipeline for quantum data embedding and evaluation.
"""

from typing import Any, Dict, List, Optional, Union, Tuple
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_array

from .embeddings import EMBEDDING_REGISTRY
from .kernels import QuantumKernel
from .metrics import compute_all_metrics
from .backends import get_backend
from .utils import validate_data, normalize_data
from .licensing import validate_license_for_class

class QuantumEmbeddingPipeline(BaseEstimator, TransformerMixin):
    """
    Main pipeline for quantum data embedding and evaluation.
    
    This class provides a unified interface for:
    - Classical data preprocessing
    - Quantum feature embedding
    - Kernel computation
    - Embedding quality assessment
    
    Parameters
    ----------
    embedding_type : str
        Type of quantum embedding ('angle', 'amplitude', 'iqp', 'data_reuploading', 'hamiltonian')
    n_qubits : int
        Number of qubits in the quantum circuit
    backend : str, default='qiskit'
        Backend framework ('qiskit', 'pennylane')
    device : str, optional
        Specific quantum device/simulator
    shots : int, default=1024
        Number of measurement shots
    normalize : bool, default=True
        Whether to normalize input data
    embedding_params : dict, optional
        Additional parameters for the embedding
    """
    
    def __init__(
        self,
        embedding_type: str,
        n_qubits: int,
        backend: str = "qiskit",
        device: Optional[str] = None,
        shots: int = 1024,
        normalize: bool = True,
        embedding_params: Optional[Dict[str, Any]] = None,
    ):
        # License validation at class instantiation
        validate_license_for_class(self.__class__)
        
        self.embedding_type = embedding_type
        self.n_qubits = n_qubits
        self.backend = backend
        self.device = device
        self.shots = shots
        self.normalize = normalize
        self.embedding_params = embedding_params or {}
        
        # Initialize components
        self._embedding = None
        self._kernel = None
        self._backend_instance = None
        self._is_fitted = False
        
    def _initialize_components(self) -> None:
        """Initialize embedding, kernel, and backend components."""
        # Get backend instance
        self._backend_instance = get_backend(
            backend=self.backend,
            device=self.device,
            shots=self.shots
        )
        
        # Get embedding class and initialize
        if self.embedding_type not in EMBEDDING_REGISTRY:
            raise ValueError(f"Unknown embedding type: {self.embedding_type}")
            
        embedding_class = EMBEDDING_REGISTRY[self.embedding_type]
        self._embedding = embedding_class(
            n_qubits=self.n_qubits,
            backend=self._backend_instance,
            **self.embedding_params
        )
        
        # Initialize quantum kernel
        self._kernel = QuantumKernel(
            embedding=self._embedding,
            backend=self._backend_instance
        )
    
    def fit(self, X: np.ndarray, y: Optional[np.ndarray] = None) -> "QuantumEmbeddingPipeline":
        """
        Fit the quantum embedding pipeline.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training data
        y : array-like of shape (n_samples,), optional
            Target values (ignored)
            
        Returns
        -------
        self : QuantumEmbeddingPipeline
            Returns self for method chaining
        """
        X = check_array(X, dtype=np.float64)
        X = validate_data(X, self.n_qubits)
        
        if self.normalize:
            X = normalize_data(X)
            
        # Initialize components if not already done
        if self._embedding is None:
            self._initialize_components()
            
        # Fit embedding (if it has fit method)
        if hasattr(self._embedding, 'fit'):
            self._embedding.fit(X)
            
        self._is_fitted = True
        return self
    
    def transform(self, X: np.ndarray) -> np.ndarray:
        """
        Transform data using quantum kernel computation.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Data to transform
            
        Returns
        -------
        K : ndarray of shape (n_samples, n_samples)
            Quantum kernel matrix
        """
        if not self._is_fitted:
            raise ValueError("Pipeline must be fitted before transform")
            
        X = check_array(X, dtype=np.float64)
        X = validate_data(X, self.n_qubits)
        
        if self.normalize:
            X = normalize_data(X)
            
        # Compute quantum kernel matrix
        return self._kernel.compute_kernel_matrix(X)
    
    def fit_transform(self, X: np.ndarray, y: Optional[np.ndarray] = None) -> np.ndarray:
        """
        Fit the pipeline and transform the data.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training data
        y : array-like of shape (n_samples,), optional
            Target values (ignored)
            
        Returns
        -------
        K : ndarray of shape (n_samples, n_samples)
            Quantum kernel matrix
        """
        return self.fit(X, y).transform(X)
    
    def evaluate_embedding(
        self, 
        X: np.ndarray, 
        n_samples: int = 1000
    ) -> Dict[str, float]:
        """
        Evaluate the quality of the quantum embedding.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Data to evaluate
        n_samples : int, default=1000
            Number of random samples for expressibility computation
            
        Returns
        -------
        metrics : dict
            Dictionary containing embedding quality metrics:
            - expressibility: Measure of state space coverage
            - trainability: Gradient variance analysis
            - effective_dimension: Effective quantum dimension
        """
        if not self._is_fitted:
            raise ValueError("Pipeline must be fitted before evaluation")
            
        X = check_array(X, dtype=np.float64)
        X = validate_data(X, self.n_qubits)
        
        if self.normalize:
            X = normalize_data(X)
            
        return compute_all_metrics(
            embedding=self._embedding,
            data=X,
            n_samples=n_samples
        )
    
    def get_circuit(self, x: np.ndarray) -> Any:
        """
        Get the quantum circuit for a single data point.
        
        Parameters
        ----------
        x : array-like of shape (n_features,)
            Single data point
            
        Returns
        -------
        circuit : quantum circuit object
            Backend-specific quantum circuit
        """
        if not self._is_fitted:
            raise ValueError("Pipeline must be fitted before getting circuit")
            
        x = np.asarray(x, dtype=np.float64)
        if x.ndim != 1:
            raise ValueError("Input must be a 1D array")
            
        x = validate_data(x.reshape(1, -1), self.n_qubits)[0]
        
        if self.normalize:
            x = normalize_data(x.reshape(1, -1))[0]
            
        return self._embedding.create_circuit(x)
    
    def compute_kernel_element(self, x1: np.ndarray, x2: np.ndarray) -> float:
        """
        Compute a single kernel element between two data points.
        
        Parameters
        ----------
        x1, x2 : array-like of shape (n_features,)
            Data points to compute kernel between
            
        Returns
        -------
        kernel_value : float
            Quantum kernel value between x1 and x2
        """
        if not self._is_fitted:
            raise ValueError("Pipeline must be fitted before computing kernel")
            
        x1 = np.asarray(x1, dtype=np.float64)
        x2 = np.asarray(x2, dtype=np.float64)
        
        if x1.ndim != 1 or x2.ndim != 1:
            raise ValueError("Inputs must be 1D arrays")
            
        # Validate and normalize data
        x1 = validate_data(x1.reshape(1, -1), self.n_qubits)[0]
        x2 = validate_data(x2.reshape(1, -1), self.n_qubits)[0]
        
        if self.normalize:
            x1 = normalize_data(x1.reshape(1, -1))[0]
            x2 = normalize_data(x2.reshape(1, -1))[0]
            
        return self._kernel.compute_kernel_element(x1, x2)
    
    def get_embedding_info(self) -> Dict[str, Any]:
        """
        Get information about the current embedding configuration.
        
        Returns
        -------
        info : dict
            Dictionary containing embedding information
        """
        info = {
            "embedding_type": self.embedding_type,
            "n_qubits": self.n_qubits,
            "backend": self.backend,
            "device": self.device,
            "shots": self.shots,
            "normalize": self.normalize,
            "embedding_params": self.embedding_params,
            "is_fitted": self._is_fitted,
        }
        
        if self._embedding is not None:
            info["circuit_depth"] = getattr(self._embedding, 'depth', None)
            info["n_parameters"] = getattr(self._embedding, 'n_parameters', None)
            
        return info
