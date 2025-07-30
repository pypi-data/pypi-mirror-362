"""
IQP (Instantaneous Quantum Polynomial) embedding implementation.
"""

from typing import Any, List
import numpy as np
from .base import BaseEmbedding


class IQPEmbedding(BaseEmbedding):
    """
    IQP embedding uses diagonal unitaries to create expressive quantum feature maps.
    
    IQP circuits consist of layers of Hadamard gates followed by diagonal gates
    with multi-qubit interactions. These circuits are known to be hard to simulate
    classically while remaining shallow, making them excellent for NISQ devices.
    
    Parameters
    ----------
    n_qubits : int
        Number of qubits in the circuit
    backend : object
        Backend instance for quantum circuit execution
    depth : int, default=3
        Number of IQP layers
    interaction_pattern : str, default='all'
        Pattern of qubit interactions ('all', 'linear', 'circular')
    
    Examples
    --------
    >>> from quantum_data_embedding_suite.backends import QiskitBackend
    >>> backend = QiskitBackend()
    >>> embedding = IQPEmbedding(n_qubits=4, backend=backend, depth=3)
    >>> circuit = embedding.create_circuit([0.1, 0.2, 0.3, 0.4, 0.5, 0.6])
    """
    
    def __init__(
        self,
        n_qubits: int,
        backend: Any,
        depth: int = 3,
        interaction_pattern: str = "all",
        **kwargs
    ):
        super().__init__(n_qubits, backend, **kwargs)
        
        if interaction_pattern not in ["all", "linear", "circular"]:
            raise ValueError(f"Invalid interaction pattern: {interaction_pattern}")
            
        self._depth = depth
        self.interaction_pattern = interaction_pattern
        self._n_parameters = 0  # Data-dependent, no trainable parameters
        
        # Generate interaction pairs based on pattern
        self.interaction_pairs = self._generate_interaction_pairs()
        
    def get_feature_dimension(self) -> int:
        """
        Get the expected number of input features.
        
        IQP embedding uses features for both single-qubit rotations and 
        multi-qubit interactions.
        
        Returns
        -------
        n_features : int
            Number of features needed
        """
        # Features for single-qubit gates + features for interaction pairs
        single_qubit_features = self.n_qubits * self._depth
        interaction_features = len(self.interaction_pairs) * self._depth
        return single_qubit_features + interaction_features
    
    def _generate_interaction_pairs(self) -> List[tuple]:
        """Generate qubit interaction pairs based on the pattern."""
        pairs = []
        
        if self.interaction_pattern == "all":
            # All pairs of qubits
            for i in range(self.n_qubits):
                for j in range(i + 1, self.n_qubits):
                    pairs.append((i, j))
        elif self.interaction_pattern == "linear":
            # Adjacent pairs only
            for i in range(self.n_qubits - 1):
                pairs.append((i, i + 1))
        elif self.interaction_pattern == "circular":
            # Adjacent pairs + wrap around
            for i in range(self.n_qubits - 1):
                pairs.append((i, i + 1))
            if self.n_qubits > 2:
                pairs.append((self.n_qubits - 1, 0))
                
        return pairs
    
    def create_circuit(self, x: np.ndarray) -> Any:
        """
        Create IQP embedding circuit for a data point.
        
        Parameters
        ----------
        x : array-like of shape (n_features,)
            Classical data point to embed
            
        Returns
        -------
        circuit : quantum circuit object
            Backend-specific quantum circuit with IQP encoding
        """
        x = self.validate_input(x)
        
        if self.backend.name == "qiskit":
            return self._create_qiskit_circuit(x)
        elif self.backend.name == "pennylane":
            return self._create_pennylane_circuit(x)
        else:
            raise ValueError(f"Unsupported backend: {self.backend.name}")
    
    def _create_qiskit_circuit(self, x: np.ndarray) -> Any:
        """Create Qiskit circuit for IQP embedding."""
        from qiskit import QuantumCircuit
        
        circuit = QuantumCircuit(self.n_qubits)
        
        # Initial Hadamard layer
        for i in range(self.n_qubits):
            circuit.h(i)
        
        # IQP layers
        feature_idx = 0
        for layer in range(self._depth):
            # Single-qubit Z rotations
            for i in range(self.n_qubits):
                circuit.rz(x[feature_idx], i)
                feature_idx += 1
            
            # Multi-qubit interactions (ZZ gates)
            for i, j in self.interaction_pairs:
                # ZZ interaction using CNOT-RZ-CNOT
                circuit.cx(i, j)
                circuit.rz(x[feature_idx], j)
                circuit.cx(i, j)
                feature_idx += 1
            
            # Hadamard layer (except last layer)
            if layer < self._depth - 1:
                for i in range(self.n_qubits):
                    circuit.h(i)
                    
        return circuit
    
    def _create_pennylane_circuit(self, x: np.ndarray) -> Any:
        """Create PennyLane circuit for IQP embedding."""
        import pennylane as qml
        
        def circuit():
            # Initial Hadamard layer
            for i in range(self.n_qubits):
                qml.Hadamard(wires=i)
            
            # IQP layers
            feature_idx = 0
            for layer in range(self._depth):
                # Single-qubit Z rotations
                for i in range(self.n_qubits):
                    qml.RZ(x[feature_idx], wires=i)
                    feature_idx += 1
                
                # Multi-qubit interactions (ZZ gates)
                for i, j in self.interaction_pairs:
                    # Use IsingZZ gate if available, otherwise decompose
                    try:
                        qml.IsingZZ(x[feature_idx], wires=[i, j])
                    except:
                        # Decomposition: ZZ = CNOT-RZ-CNOT
                        qml.CNOT(wires=[i, j])
                        qml.RZ(x[feature_idx], wires=j)
                        qml.CNOT(wires=[i, j])
                    feature_idx += 1
                
                # Hadamard layer (except last layer)
                if layer < self._depth - 1:
                    for i in range(self.n_qubits):
                        qml.Hadamard(wires=i)
                        
        return circuit
    
    def get_expressibility_bounds(self) -> tuple:
        """
        Get theoretical expressibility bounds for IQP circuits.
        
        Returns
        -------
        bounds : tuple
            (lower_bound, upper_bound) for expressibility
        """
        # IQP circuits have known expressibility properties
        # This is based on theoretical analysis of IQP expressiveness
        n_states = 2 ** self.n_qubits
        
        # Lower bound: uniform distribution
        lower_bound = 0.0
        
        # Upper bound: depends on circuit depth and connectivity
        max_expressibility = 1.0 - 1.0 / n_states
        
        # Scaling with depth (heuristic)
        depth_factor = min(1.0, self._depth / self.n_qubits)
        
        # Scaling with connectivity
        max_pairs = self.n_qubits * (self.n_qubits - 1) // 2
        connectivity_factor = len(self.interaction_pairs) / max_pairs
        
        upper_bound = max_expressibility * depth_factor * connectivity_factor
        
        return (lower_bound, upper_bound)
