"""
Angle embedding implementation.
"""

from typing import Any
import numpy as np
from .base import BaseEmbedding


class AngleEmbedding(BaseEmbedding):
    """
    Angle embedding encodes classical data as rotation angles in quantum circuits.
    
    Features are encoded as parameters to rotation gates (RX, RY, RZ).
    This is one of the most common and straightforward embedding methods.
    
    Parameters
    ----------
    n_qubits : int
        Number of qubits in the circuit
    backend : object
        Backend instance for quantum circuit execution
    rotation : str, default='Y'
        Type of rotation gate ('X', 'Y', 'Z', or 'XYZ' for all)
    entangling : str, default='linear'
        Entangling pattern ('linear', 'circular', 'full', 'none')
    depth : int, default=1
        Number of encoding layers
    
    Examples
    --------
    >>> from quantum_data_embedding_suite.backends import QiskitBackend
    >>> backend = QiskitBackend()
    >>> embedding = AngleEmbedding(n_qubits=4, backend=backend)
    >>> circuit = embedding.create_circuit([0.1, 0.2, 0.3, 0.4])
    """
    
    def __init__(
        self,
        n_qubits: int,
        backend: Any,
        rotation: str = "Y",
        entangling: str = "linear",
        depth: int = 1,
        **kwargs
    ):
        super().__init__(n_qubits, backend, **kwargs)
        
        if rotation not in ["X", "Y", "Z", "XYZ"]:
            raise ValueError(f"Invalid rotation type: {rotation}")
            
        if entangling not in ["linear", "circular", "full", "none"]:
            raise ValueError(f"Invalid entangling pattern: {entangling}")
            
        self.rotation = rotation
        self.entangling = entangling
        self._depth = depth
        self._n_parameters = 0  # Data-dependent, no trainable parameters
        
    def get_feature_dimension(self) -> int:
        """
        Get the expected number of input features.
        
        For angle embedding, each qubit can encode one feature per layer.
        
        Returns
        -------
        n_features : int
            Number of features (n_qubits * depth)
        """
        if self.rotation == "XYZ":
            return self.n_qubits * 3 * self._depth
        else:
            return self.n_qubits * self._depth
    
    def create_circuit(self, x: np.ndarray) -> Any:
        """
        Create angle embedding circuit for a data point.
        
        Parameters
        ----------
        x : array-like of shape (n_features,)
            Classical data point to embed
            
        Returns
        -------
        circuit : quantum circuit object
            Backend-specific quantum circuit with angle encoding
        """
        x = self.validate_input(x)
        
        if self.backend.name == "qiskit":
            return self._create_qiskit_circuit(x)
        elif self.backend.name == "pennylane":
            return self._create_pennylane_circuit(x)
        else:
            raise ValueError(f"Unsupported backend: {self.backend.name}")
    
    def _create_qiskit_circuit(self, x: np.ndarray) -> Any:
        """Create Qiskit circuit for angle embedding."""
        from qiskit import QuantumCircuit
        
        circuit = QuantumCircuit(self.n_qubits)
        
        # Apply encoding layers
        for layer in range(self._depth):
            # Rotation gates
            if self.rotation == "XYZ":
                for i in range(self.n_qubits):
                    idx_base = layer * self.n_qubits * 3 + i * 3
                    circuit.rx(x[idx_base], i)
                    circuit.ry(x[idx_base + 1], i) 
                    circuit.rz(x[idx_base + 2], i)
            else:
                for i in range(self.n_qubits):
                    idx = layer * self.n_qubits + i
                    if self.rotation == "X":
                        circuit.rx(x[idx], i)
                    elif self.rotation == "Y":
                        circuit.ry(x[idx], i)
                    elif self.rotation == "Z":
                        circuit.rz(x[idx], i)
            
            # Entangling gates (except last layer)
            if layer < self._depth - 1 or self._depth == 1:
                self._add_entangling_gates_qiskit(circuit)
                
        return circuit
    
    def _create_pennylane_circuit(self, x: np.ndarray) -> Any:
        """Create PennyLane circuit for angle embedding."""
        import pennylane as qml
        
        def circuit():
            # Apply encoding layers
            for layer in range(self._depth):
                # Rotation gates
                if self.rotation == "XYZ":
                    for i in range(self.n_qubits):
                        idx_base = layer * self.n_qubits * 3 + i * 3
                        qml.RX(x[idx_base], wires=i)
                        qml.RY(x[idx_base + 1], wires=i)
                        qml.RZ(x[idx_base + 2], wires=i)
                else:
                    for i in range(self.n_qubits):
                        idx = layer * self.n_qubits + i
                        if self.rotation == "X":
                            qml.RX(x[idx], wires=i)
                        elif self.rotation == "Y":
                            qml.RY(x[idx], wires=i)
                        elif self.rotation == "Z":
                            qml.RZ(x[idx], wires=i)
                
                # Entangling gates (except last layer)
                if layer < self._depth - 1 or self._depth == 1:
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
        # 'none' case: no entangling gates
    
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
        # 'none' case: no entangling gates
