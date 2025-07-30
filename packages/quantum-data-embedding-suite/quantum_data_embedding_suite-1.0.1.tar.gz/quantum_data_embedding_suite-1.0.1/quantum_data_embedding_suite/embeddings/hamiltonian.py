"""
Hamiltonian-based embedding implementation.
"""

from typing import Any, Dict, List, Union
import numpy as np
from .base import BaseEmbedding


class HamiltonianEmbedding(BaseEmbedding):
    """
    Hamiltonian embedding encodes data through time evolution under a data-dependent Hamiltonian.
    
    This physics-inspired approach uses the Hamiltonian H = Σ x_i * H_i where x_i are the
    classical features and H_i are Pauli operators. The quantum state is evolved using
    exp(-i * H * t) where t is an evolution time parameter.
    
    Parameters
    ----------
    n_qubits : int
        Number of qubits in the circuit
    backend : object
        Backend instance for quantum circuit execution
    hamiltonian_type : str, default='pauli_x'
        Type of Hamiltonian ('pauli_x', 'pauli_y', 'pauli_z', 'ising', 'custom')
    evolution_time : float, default=1.0
        Time parameter for Hamiltonian evolution
    trotter_steps : int, default=1
        Number of Trotter steps for time evolution approximation
    initial_state : str, default='zero'
        Initial quantum state ('zero', 'plus', 'random')
    
    Examples
    --------
    >>> from quantum_data_embedding_suite.backends import QiskitBackend
    >>> backend = QiskitBackend()
    >>> embedding = HamiltonianEmbedding(n_qubits=4, backend=backend, hamiltonian_type='ising')
    >>> circuit = embedding.create_circuit([0.1, 0.2, 0.3, 0.4])
    """
    
    def __init__(
        self,
        n_qubits: int,
        backend: Any,
        hamiltonian_type: str = "pauli_x",
        evolution_time: float = 1.0,
        trotter_steps: int = 1,
        initial_state: str = "zero",
        custom_operators: List[str] = None,
        **kwargs
    ):
        super().__init__(n_qubits, backend, **kwargs)
        
        valid_types = ["pauli_x", "pauli_y", "pauli_z", "ising", "heisenberg", "custom"]
        if hamiltonian_type not in valid_types:
            raise ValueError(f"Invalid hamiltonian_type: {hamiltonian_type}")
            
        if initial_state not in ["zero", "plus", "random"]:
            raise ValueError(f"Invalid initial_state: {initial_state}")
            
        self.hamiltonian_type = hamiltonian_type
        self.evolution_time = evolution_time
        self.trotter_steps = trotter_steps
        self.initial_state = initial_state
        self.custom_operators = custom_operators or []
        
        # Determine circuit depth based on Trotter steps
        self._depth = trotter_steps
        self._n_parameters = 1  # Evolution time parameter
        
        # Generate Hamiltonian operators
        self.operators = self._generate_operators()
        
    def get_feature_dimension(self) -> int:
        """
        Get the expected number of input features.
        
        Returns
        -------
        n_features : int
            Number of features (equal to number of Hamiltonian terms)
        """
        return len(self.operators)
    
    def _generate_operators(self) -> List[Dict[str, Any]]:
        """Generate the Hamiltonian operators based on the type."""
        operators = []
        
        if self.hamiltonian_type == "pauli_x":
            # Single-qubit X operators: H = Σ x_i * X_i
            for i in range(self.n_qubits):
                operators.append({"type": "X", "qubits": [i]})
                
        elif self.hamiltonian_type == "pauli_y":
            # Single-qubit Y operators: H = Σ x_i * Y_i
            for i in range(self.n_qubits):
                operators.append({"type": "Y", "qubits": [i]})
                
        elif self.hamiltonian_type == "pauli_z":
            # Single-qubit Z operators: H = Σ x_i * Z_i
            for i in range(self.n_qubits):
                operators.append({"type": "Z", "qubits": [i]})
                
        elif self.hamiltonian_type == "ising":
            # Ising model: H = Σ x_i * Z_i + Σ x_{i,j} * Z_i * Z_j
            # Single-qubit terms
            for i in range(self.n_qubits):
                operators.append({"type": "Z", "qubits": [i]})
            # Two-qubit terms (nearest neighbor)
            for i in range(self.n_qubits - 1):
                operators.append({"type": "ZZ", "qubits": [i, i + 1]})
                
        elif self.hamiltonian_type == "heisenberg":
            # Heisenberg model: H = Σ (X_i*X_{i+1} + Y_i*Y_{i+1} + Z_i*Z_{i+1})
            for i in range(self.n_qubits - 1):
                operators.append({"type": "XX", "qubits": [i, i + 1]})
                operators.append({"type": "YY", "qubits": [i, i + 1]})
                operators.append({"type": "ZZ", "qubits": [i, i + 1]})
                
        elif self.hamiltonian_type == "custom":
            # Custom operators specified by user
            for op_str in self.custom_operators:
                operators.append(self._parse_operator_string(op_str))
                
        return operators
    
    def _parse_operator_string(self, op_str: str) -> Dict[str, Any]:
        """Parse operator string like 'X0', 'Z1Z2', etc."""
        # Simple parser for operator strings
        # Format: 'X0', 'Y1', 'Z2', 'X0Y1', 'Z1Z2', etc.
        qubits = []
        op_type = ""
        
        i = 0
        while i < len(op_str):
            if op_str[i] in "XYZ":
                op_type += op_str[i]
                i += 1
                # Extract qubit number
                qubit_str = ""
                while i < len(op_str) and op_str[i].isdigit():
                    qubit_str += op_str[i]
                    i += 1
                qubits.append(int(qubit_str))
            else:
                i += 1
                
        return {"type": op_type, "qubits": qubits}
    
    def create_circuit(self, x: np.ndarray) -> Any:
        """
        Create Hamiltonian evolution circuit for a data point.
        
        Parameters
        ----------
        x : array-like of shape (n_features,)
            Classical data point (Hamiltonian coefficients)
            
        Returns
        -------
        circuit : quantum circuit object
            Backend-specific quantum circuit with Hamiltonian evolution
        """
        x = self.validate_input(x)
        
        if self.backend.name == "qiskit":
            return self._create_qiskit_circuit(x)
        elif self.backend.name == "pennylane":
            return self._create_pennylane_circuit(x)
        else:
            raise ValueError(f"Unsupported backend: {self.backend.name}")
    
    def _create_qiskit_circuit(self, x: np.ndarray) -> Any:
        """Create Qiskit circuit for Hamiltonian evolution."""
        from qiskit import QuantumCircuit
        
        circuit = QuantumCircuit(self.n_qubits)
        
        # Prepare initial state
        self._prepare_initial_state_qiskit(circuit)
        
        # Trotter evolution
        dt = self.evolution_time / self.trotter_steps
        
        for step in range(self.trotter_steps):
            for i, operator in enumerate(self.operators):
                if i < len(x):
                    self._apply_operator_evolution_qiskit(
                        circuit, operator, x[i] * dt
                    )
                    
        return circuit
    
    def _create_pennylane_circuit(self, x: np.ndarray) -> Any:
        """Create PennyLane circuit for Hamiltonian evolution."""
        import pennylane as qml
        
        def circuit():
            # Prepare initial state
            self._prepare_initial_state_pennylane()
            
            # Trotter evolution
            dt = self.evolution_time / self.trotter_steps
            
            for step in range(self.trotter_steps):
                for i, operator in enumerate(self.operators):
                    if i < len(x):
                        self._apply_operator_evolution_pennylane(
                            operator, x[i] * dt
                        )
                        
        return circuit
    
    def _prepare_initial_state_qiskit(self, circuit: Any) -> None:
        """Prepare the initial quantum state."""
        if self.initial_state == "plus":
            for i in range(self.n_qubits):
                circuit.h(i)
        elif self.initial_state == "random":
            # Simple random state preparation
            angles = np.random.uniform(0, 2*np.pi, self.n_qubits)
            for i, angle in enumerate(angles):
                circuit.ry(angle, i)
        # 'zero' state requires no preparation
    
    def _prepare_initial_state_pennylane(self) -> None:
        """Prepare the initial quantum state."""
        import pennylane as qml
        
        if self.initial_state == "plus":
            for i in range(self.n_qubits):
                qml.Hadamard(wires=i)
        elif self.initial_state == "random":
            # Simple random state preparation
            angles = np.random.uniform(0, 2*np.pi, self.n_qubits)
            for i, angle in enumerate(angles):
                qml.RY(angle, wires=i)
        # 'zero' state requires no preparation
    
    def _apply_operator_evolution_qiskit(
        self, 
        circuit: Any, 
        operator: Dict[str, Any], 
        angle: float
    ) -> None:
        """Apply evolution under a single operator term."""
        op_type = operator["type"]
        qubits = operator["qubits"]
        
        if op_type == "X":
            circuit.rx(2 * angle, qubits[0])
        elif op_type == "Y":
            circuit.ry(2 * angle, qubits[0])
        elif op_type == "Z":
            circuit.rz(2 * angle, qubits[0])
        elif op_type == "ZZ":
            # ZZ evolution: exp(-i*angle*ZZ) = CNOT-RZ-CNOT
            circuit.cx(qubits[0], qubits[1])
            circuit.rz(2 * angle, qubits[1])
            circuit.cx(qubits[0], qubits[1])
        elif op_type == "XX":
            # XX evolution
            circuit.h(qubits[0])
            circuit.h(qubits[1])
            circuit.cx(qubits[0], qubits[1])
            circuit.rz(2 * angle, qubits[1])
            circuit.cx(qubits[0], qubits[1])
            circuit.h(qubits[0])
            circuit.h(qubits[1])
        elif op_type == "YY":
            # YY evolution
            circuit.rx(np.pi/2, qubits[0])
            circuit.rx(np.pi/2, qubits[1])
            circuit.cx(qubits[0], qubits[1])
            circuit.rz(2 * angle, qubits[1])
            circuit.cx(qubits[0], qubits[1])
            circuit.rx(-np.pi/2, qubits[0])
            circuit.rx(-np.pi/2, qubits[1])
    
    def _apply_operator_evolution_pennylane(
        self, 
        operator: Dict[str, Any], 
        angle: float
    ) -> None:
        """Apply evolution under a single operator term."""
        import pennylane as qml
        
        op_type = operator["type"]
        qubits = operator["qubits"]
        
        if op_type == "X":
            qml.RX(2 * angle, wires=qubits[0])
        elif op_type == "Y":
            qml.RY(2 * angle, wires=qubits[0])
        elif op_type == "Z":
            qml.RZ(2 * angle, wires=qubits[0])
        elif op_type == "ZZ":
            qml.IsingZZ(2 * angle, wires=qubits)
        elif op_type in ["XX", "YY"]:
            # Use built-in evolution gates if available
            if hasattr(qml, f"Ising{op_type}"):
                getattr(qml, f"Ising{op_type}")(2 * angle, wires=qubits)
            else:
                # Fallback to manual decomposition
                self._manual_two_qubit_evolution_pennylane(op_type, angle, qubits)
    
    def _manual_two_qubit_evolution_pennylane(
        self, 
        op_type: str, 
        angle: float, 
        qubits: List[int]
    ) -> None:
        """Manual decomposition for two-qubit evolutions."""
        import pennylane as qml
        
        if op_type == "XX":
            qml.Hadamard(wires=qubits[0])
            qml.Hadamard(wires=qubits[1])
            qml.IsingZZ(2 * angle, wires=qubits)
            qml.Hadamard(wires=qubits[0])
            qml.Hadamard(wires=qubits[1])
        elif op_type == "YY":
            qml.RX(np.pi/2, wires=qubits[0])
            qml.RX(np.pi/2, wires=qubits[1])
            qml.IsingZZ(2 * angle, wires=qubits)
            qml.RX(-np.pi/2, wires=qubits[0])
            qml.RX(-np.pi/2, wires=qubits[1])
