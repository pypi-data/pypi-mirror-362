"""
Data re-uploading embedding implementation.
"""

from typing import Any, List
import numpy as np
from .base import BaseEmbedding


class DataReuploadingEmbedding(BaseEmbedding):
    """
    Data re-uploading embedding repeatedly encodes the same data across multiple layers.
    
    This technique allows quantum circuits to achieve universal approximation
    properties by encoding data multiple times with trainable parameters
    interspersed between encoding layers.
    
    Parameters
    ----------
    n_qubits : int
        Number of qubits in the circuit
    backend : object
        Backend instance for quantum circuit execution
    depth : int, default=3
        Number of re-uploading layers
    trainable_params : bool, default=True
        Whether to include trainable parameters between layers
    rotation_gates : list, default=['RX', 'RY', 'RZ']
        Types of rotation gates to use
    entangling : str, default='linear'
        Entangling pattern between layers
    
    Examples
    --------
    >>> from quantum_data_embedding_suite.backends import QiskitBackend
    >>> backend = QiskitBackend()
    >>> embedding = DataReuploadingEmbedding(n_qubits=4, backend=backend, depth=3)
    >>> circuit = embedding.create_circuit([0.1, 0.2, 0.3, 0.4])
    """
    
    def __init__(
        self,
        n_qubits: int,
        backend: Any,
        depth: int = 3,
        trainable_params: bool = True,
        rotation_gates: List[str] = None,
        entangling: str = "linear",
        **kwargs
    ):
        super().__init__(n_qubits, backend, **kwargs)
        
        if rotation_gates is None:
            rotation_gates = ["RX", "RY", "RZ"]
            
        for gate in rotation_gates:
            if gate not in ["RX", "RY", "RZ"]:
                raise ValueError(f"Invalid rotation gate: {gate}")
                
        if entangling not in ["linear", "circular", "full", "none"]:
            raise ValueError(f"Invalid entangling pattern: {entangling}")
            
        self._depth = depth
        self.trainable_params = trainable_params
        self.rotation_gates = rotation_gates
        self.entangling = entangling
        
        # Calculate number of parameters
        gates_per_qubit_per_layer = len(rotation_gates)
        if trainable_params:
            # Trainable params + data params
            self._n_parameters = (
                depth * n_qubits * gates_per_qubit_per_layer * 2
            )
        else:
            # Only data parameters
            self._n_parameters = 0
            
        # Initialize trainable parameters randomly
        if trainable_params:
            self.theta = np.random.uniform(
                0, 2 * np.pi, 
                size=(depth, n_qubits, gates_per_qubit_per_layer)
            )
        else:
            self.theta = None
    
    def get_feature_dimension(self) -> int:
        """
        Get the expected number of input features.
        
        For data re-uploading, the same features are used in each layer.
        
        Returns
        -------
        n_features : int
            Number of features (same as number of qubits)
        """
        return self.n_qubits
    
    def create_circuit(self, x: np.ndarray) -> Any:
        """
        Create data re-uploading circuit for a data point.
        
        Parameters
        ----------
        x : array-like of shape (n_features,)
            Classical data point to embed
            
        Returns
        -------
        circuit : quantum circuit object
            Backend-specific quantum circuit with data re-uploading
        """
        x = self.validate_input(x)
        
        if self.backend.name == "qiskit":
            return self._create_qiskit_circuit(x)
        elif self.backend.name == "pennylane":
            return self._create_pennylane_circuit(x)
        else:
            raise ValueError(f"Unsupported backend: {self.backend.name}")
    
    def _create_qiskit_circuit(self, x: np.ndarray) -> Any:
        """Create Qiskit circuit for data re-uploading."""
        from qiskit import QuantumCircuit
        
        circuit = QuantumCircuit(self.n_qubits)
        
        for layer in range(self._depth):
            # Data encoding layer
            for i in range(self.n_qubits):
                for g, gate_type in enumerate(self.rotation_gates):
                    angle = x[i]  # Same data re-uploaded
                    
                    # Add trainable parameter if enabled
                    if self.trainable_params:
                        angle += self.theta[layer, i, g]
                    
                    if gate_type == "RX":
                        circuit.rx(angle, i)
                    elif gate_type == "RY":
                        circuit.ry(angle, i)
                    elif gate_type == "RZ":
                        circuit.rz(angle, i)
            
            # Entangling layer (except last layer)
            if layer < self._depth - 1:
                self._add_entangling_gates_qiskit(circuit)
                
        return circuit
    
    def _create_pennylane_circuit(self, x: np.ndarray) -> Any:
        """Create PennyLane circuit for data re-uploading."""
        import pennylane as qml
        
        def circuit():
            for layer in range(self._depth):
                # Data encoding layer
                for i in range(self.n_qubits):
                    for g, gate_type in enumerate(self.rotation_gates):
                        angle = x[i]  # Same data re-uploaded
                        
                        # Add trainable parameter if enabled
                        if self.trainable_params:
                            angle += self.theta[layer, i, g]
                        
                        if gate_type == "RX":
                            qml.RX(angle, wires=i)
                        elif gate_type == "RY":
                            qml.RY(angle, wires=i)
                        elif gate_type == "RZ":
                            qml.RZ(angle, wires=i)
                
                # Entangling layer (except last layer)
                if layer < self._depth - 1:
                    self._add_entangling_gates_pennylane()
                    
        return circuit
    
    def _add_entangling_gates_qiskit(self, circuit: Any) -> None:
        """Add entangling gates to Qiskit circuit."""
        if self.entangling == "linear":
            for i in range(self.n_qubits - 1):
                circuit.cx(i, i + 1)
        elif self.entangling == "circular":
            for i in range(self.n_qubits - 1):
                circuit.cx(i, i + 1)
            if self.n_qubits > 2:
                circuit.cx(self.n_qubits - 1, 0)
        elif self.entangling == "full":
            for i in range(self.n_qubits):
                for j in range(i + 1, self.n_qubits):
                    circuit.cx(i, j)
    
    def _add_entangling_gates_pennylane(self) -> None:
        """Add entangling gates to PennyLane circuit."""
        import pennylane as qml
        
        if self.entangling == "linear":
            for i in range(self.n_qubits - 1):
                qml.CNOT(wires=[i, i + 1])
        elif self.entangling == "circular":
            for i in range(self.n_qubits - 1):
                qml.CNOT(wires=[i, i + 1])
            if self.n_qubits > 2:
                qml.CNOT(wires=[self.n_qubits - 1, 0])
        elif self.entangling == "full":
            for i in range(self.n_qubits):
                for j in range(i + 1, self.n_qubits):
                    qml.CNOT(wires=[i, j])
    
    def update_parameters(self, new_theta: np.ndarray) -> None:
        """
        Update trainable parameters.
        
        Parameters
        ----------
        new_theta : array-like
            New parameter values
        """
        if not self.trainable_params:
            raise ValueError("No trainable parameters to update")
            
        expected_shape = (self._depth, self.n_qubits, len(self.rotation_gates))
        new_theta = np.asarray(new_theta).reshape(expected_shape)
        self.theta = new_theta
    
    def get_parameters(self) -> np.ndarray:
        """
        Get current trainable parameters.
        
        Returns
        -------
        theta : ndarray
            Current parameter values
        """
        if not self.trainable_params:
            return np.array([])
        return self.theta.copy()
    
    def fit(self, X: np.ndarray) -> "DataReuploadingEmbedding":
        """
        Fit the embedding to training data.
        
        For data re-uploading, this can optionally optimize the trainable
        parameters using the training data.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training data
            
        Returns
        -------
        self : DataReuploadingEmbedding
            Returns self for method chaining
        """
        # Basic implementation: just store the data statistics
        # In a more advanced version, you could optimize the trainable
        # parameters using the training data
        
        X = np.asarray(X)
        self.data_mean_ = np.mean(X, axis=0)
        self.data_std_ = np.std(X, axis=0)
        
        return self
