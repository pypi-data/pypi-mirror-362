"""
Amplitude embedding implementation.
"""

from typing import Any
import numpy as np
from .base import BaseEmbedding


class AmplitudeEmbedding(BaseEmbedding):
    """
    Amplitude embedding encodes classical data into quantum state amplitudes.
    
    Classical data is directly encoded as the amplitudes of a quantum state.
    This provides an exponential advantage in data density but requires
    normalization and specific data sizes (powers of 2).
    
    Parameters
    ----------
    n_qubits : int
        Number of qubits in the circuit
    backend : object
        Backend instance for quantum circuit execution
    normalize : bool, default=True
        Whether to normalize the input data to unit norm
    padding : str, default='zero'
        How to handle data that doesn't fit 2^n_qubits ('zero', 'repeat', 'truncate')
    
    Examples
    --------
    >>> from quantum_data_embedding_suite.backends import QiskitBackend
    >>> backend = QiskitBackend()
    >>> embedding = AmplitudeEmbedding(n_qubits=3, backend=backend)
    >>> circuit = embedding.create_circuit([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8])
    """
    
    def __init__(
        self,
        n_qubits: int,
        backend: Any,
        normalize: bool = True,
        padding: str = "zero",
        **kwargs
    ):
        super().__init__(n_qubits, backend, **kwargs)
        
        if padding not in ["zero", "repeat", "truncate"]:
            raise ValueError(f"Invalid padding method: {padding}")
            
        self.normalize = normalize
        self.padding = padding
        self._depth = 1  # Amplitude encoding is typically single layer
        self._n_parameters = 0  # Data-dependent, no trainable parameters
        
    def get_feature_dimension(self) -> int:
        """
        Get the expected number of input features.
        
        For amplitude embedding, the number of features should be 2^n_qubits
        for optimal encoding, but can be flexible with padding.
        
        Returns
        -------
        n_features : int
            Maximum number of features (2^n_qubits)
        """
        return 2 ** self.n_qubits
    
    def create_circuit(self, x: np.ndarray) -> Any:
        """
        Create amplitude embedding circuit for a data point.
        
        Parameters
        ----------
        x : array-like of shape (n_features,)
            Classical data point to embed as amplitudes
            
        Returns
        -------
        circuit : quantum circuit object
            Backend-specific quantum circuit with amplitude encoding
        """
        # Validate and prepare amplitudes
        amplitudes = self._prepare_amplitudes(x)
        
        if self.backend.name == "qiskit":
            return self._create_qiskit_circuit(amplitudes)
        elif self.backend.name == "pennylane":
            return self._create_pennylane_circuit(amplitudes)
        else:
            raise ValueError(f"Unsupported backend: {self.backend.name}")
    
    def _prepare_amplitudes(self, x: np.ndarray) -> np.ndarray:
        """
        Prepare amplitudes from input data.
        
        Parameters
        ----------
        x : array-like
            Input data
            
        Returns
        -------
        amplitudes : ndarray
            Normalized amplitudes for quantum state
        """
        x = np.asarray(x, dtype=np.float64)
        target_size = 2 ** self.n_qubits
        
        # Handle size mismatch
        if len(x) > target_size:
            if self.padding == "truncate":
                x = x[:target_size]
            else:
                raise ValueError(
                    f"Input size {len(x)} exceeds maximum {target_size} for {self.n_qubits} qubits"
                )
        elif len(x) < target_size:
            if self.padding == "zero":
                padded = np.zeros(target_size)
                padded[:len(x)] = x
                x = padded
            elif self.padding == "repeat":
                # Repeat the pattern to fill the space
                repeats = target_size // len(x)
                remainder = target_size % len(x)
                x = np.concatenate([np.tile(x, repeats), x[:remainder]])
            else:
                raise ValueError(f"Unknown padding method: {self.padding}")
        
        # Normalize to unit norm if requested
        if self.normalize:
            norm = np.linalg.norm(x)
            if norm > 1e-10:  # Avoid division by zero
                x = x / norm
            else:
                # Handle zero vector case
                x = np.zeros_like(x)
                x[0] = 1.0  # Set to |0...0⟩ state
                
        return x
    
    def _create_qiskit_circuit(self, amplitudes: np.ndarray) -> Any:
        """Create Qiskit circuit for amplitude embedding."""
        from qiskit import QuantumCircuit
        
        circuit = QuantumCircuit(self.n_qubits)
        
        # Use Qiskit's built-in amplitude embedding if available
        try:
            from qiskit.circuit.library import Initialize
            circuit.append(Initialize(amplitudes), circuit.qubits)
        except ImportError:
            # Fallback: manual amplitude embedding (simplified)
            # This is a basic implementation - in practice, you'd want
            # a more sophisticated state preparation routine
            self._manual_amplitude_embedding_qiskit(circuit, amplitudes)
            
        return circuit
    
    def _create_pennylane_circuit(self, amplitudes: np.ndarray) -> Any:
        """Create PennyLane circuit for amplitude embedding."""
        import pennylane as qml
        
        def circuit():
            # Use PennyLane's amplitude embedding
            qml.AmplitudeEmbedding(
                features=amplitudes,
                wires=range(self.n_qubits),
                normalize=False  # Already normalized in _prepare_amplitudes
            )
            
        return circuit
    
    def _manual_amplitude_embedding_qiskit(
        self, 
        circuit: Any, 
        amplitudes: np.ndarray
    ) -> None:
        """
        Manual implementation of amplitude embedding for Qiskit.
        
        This is a simplified version. In practice, you'd use more sophisticated
        state preparation algorithms like those in Qiskit's Initialize class.
        """
        # This is a placeholder for manual amplitude embedding
        # In practice, you would implement a proper state preparation algorithm
        # For now, we'll just apply some rotations based on the amplitudes
        
        # Simple approach: use the amplitudes to determine rotation angles
        for i, amp in enumerate(amplitudes[:self.n_qubits]):
            if amp != 0:
                angle = 2 * np.arcsin(abs(amp))
                circuit.ry(angle, i)
    
    def validate_input(self, x: np.ndarray) -> np.ndarray:
        """
        Validate input for amplitude embedding.
        
        Parameters
        ----------
        x : array-like
            Input data
            
        Returns
        -------
        x : ndarray
            Validated input data
        """
        x = np.asarray(x, dtype=np.float64)
        
        if x.ndim != 1:
            raise ValueError(f"Input must be 1D array, got {x.ndim}D")
        
        max_features = 2 ** self.n_qubits
        if len(x) > max_features and self.padding == "truncate":
            return x  # Will be truncated in _prepare_amplitudes
        elif len(x) > max_features:
            raise ValueError(
                f"Input size {len(x)} too large for {self.n_qubits} qubits "
                f"(max {max_features}). Use padding='truncate' or reduce input size."
            )
            
        return x
