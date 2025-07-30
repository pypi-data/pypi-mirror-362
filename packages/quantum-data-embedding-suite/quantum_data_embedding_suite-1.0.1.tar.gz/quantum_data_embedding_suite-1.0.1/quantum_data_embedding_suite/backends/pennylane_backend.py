"""
PennyLane backend implementation.
"""

from typing import Any, Dict, List, Optional
import numpy as np
from .base import BaseBackend


class PennyLaneBackend(BaseBackend):
    """
    PennyLane backend for quantum circuit execution.
    
    Supports various PennyLane devices including simulators and hardware.
    
    Parameters
    ----------
    device : str, optional
        PennyLane device name (e.g., 'default.qubit', 'qiskit.aer', 'cirq.simulator')
    shots : int, default=1024
        Number of measurement shots
    **kwargs
        Additional PennyLane-specific parameters
    """
    
    def __init__(
        self, 
        device: Optional[str] = None, 
        shots: int = 1024,
        **kwargs
    ):
        super().__init__(device=device, shots=shots, **kwargs)
        self._device = None
        self._qnode_cache = {}
        
        # Default device
        if device is None:
            self.device = "default.qubit"
    
    @property
    def name(self) -> str:
        """Get the backend name."""
        return "pennylane"
    
    def initialize(self) -> None:
        """Initialize the PennyLane backend."""
        try:
            import pennylane as qml
        except ImportError:
            raise ImportError("PennyLane is required for PennyLaneBackend")
        
        # Create PennyLane device
        n_qubits = self.params.get('n_qubits', 10)  # Default number of qubits
        
        device_kwargs = {
            'wires': n_qubits,
            'shots': self.shots if self.shots > 0 else None,
        }
        
        # Add device-specific parameters
        if self.device.startswith('qiskit'):
            device_kwargs.update({
                'backend': self.params.get('qiskit_backend', 'qasm_simulator'),
            })
        elif self.device.startswith('cirq'):
            # Cirq-specific parameters
            pass
        elif self.device == 'lightning.qubit':
            # Lightning-specific parameters
            device_kwargs['batch_obs'] = self.params.get('batch_obs', False)
        
        self._device = qml.device(self.device, **device_kwargs)
    
    def execute_circuit(
        self, 
        circuit: Any, 
        shots: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Execute a quantum circuit using PennyLane.
        
        Parameters
        ----------
        circuit : callable
            PennyLane quantum function
        shots : int, optional
            Number of shots (overrides default if provided)
            
        Returns
        -------
        result : dict
            Execution results containing probabilities, samples, etc.
        """
        self.ensure_initialized()
        
        import pennylane as qml
        
        # Create QNode for execution
        @qml.qnode(self._device)
        def qnode():
            circuit()
            return qml.probs(wires=range(self._device.num_wires))
        
        # Execute and get probabilities
        probs = qnode()
        
        # Convert to numpy array
        probs = np.array(probs)
        
        # Generate sample counts if shots are specified
        output = {'probabilities': probs}
        
        if shots is not None and shots > 0:
            # Sample from probability distribution
            n_states = len(probs)
            states = np.arange(n_states)
            samples = np.random.choice(states, size=shots, p=probs)
            
            # Count occurrences
            unique, counts = np.unique(samples, return_counts=True)
            counts_dict = {}
            for state, count in zip(unique, counts):
                # Convert to binary string
                binary = format(state, f'0{self._device.num_wires}b')
                counts_dict[binary] = int(count)
            
            output['counts'] = counts_dict
            output['samples'] = samples
        
        return output
    
    def get_statevector(self, circuit: Any) -> np.ndarray:
        """
        Get the statevector from a quantum circuit.
        
        Parameters
        ----------
        circuit : callable
            PennyLane quantum function
            
        Returns
        -------
        statevector : ndarray
            Complex amplitudes of the quantum state
        """
        self.ensure_initialized()
        
        import pennylane as qml
        
        # Create a statevector device if current device doesn't support it
        if hasattr(self._device, 'analytic') and self._device.analytic:
            device = self._device
        else:
            # Create temporary statevector device
            device = qml.device('default.qubit', wires=self._device.num_wires)
        
        @qml.qnode(device)
        def qnode():
            circuit()
            return qml.state()
        
        statevector = qnode()
        return np.array(statevector)
    
    def compute_expectation(
        self, 
        circuit: Any, 
        observable: Any
    ) -> float:
        """
        Compute expectation value of an observable.
        
        Parameters
        ----------
        circuit : callable
            PennyLane quantum function
        observable : pennylane.Hamiltonian or pennylane.operation.Observable
            PennyLane observable
            
        Returns
        -------
        expectation : float
            Expectation value
        """
        self.ensure_initialized()
        
        import pennylane as qml
        
        @qml.qnode(self._device)
        def qnode():
            circuit()
            return qml.expval(observable)
        
        expectation = qnode()
        return float(expectation)
    
    def create_observable(self, pauli_string: str, qubits: List[int]) -> Any:
        """
        Create a PennyLane observable from a Pauli string.
        
        Parameters
        ----------
        pauli_string : str
            Pauli string (e.g., 'XYZ', 'ZZI')
        qubits : list of int
            Qubits to apply the observable to
            
        Returns
        -------
        observable : pennylane.Hamiltonian
            PennyLane observable object
        """
        try:
            import pennylane as qml
        except ImportError:
            raise ImportError("PennyLane is required for observables")
        
        # Map Pauli characters to PennyLane operators
        pauli_map = {
            'I': qml.Identity,
            'X': qml.PauliX,
            'Y': qml.PauliY,
            'Z': qml.PauliZ,
        }
        
        # Build tensor product of Pauli operators
        if len(pauli_string) == 1:
            # Single Pauli operator
            return pauli_map[pauli_string](wires=qubits[0])
        else:
            # Tensor product of multiple Pauli operators
            ops = []
            for i, pauli in enumerate(pauli_string):
                if i < len(qubits) and pauli != 'I':
                    ops.append(pauli_map[pauli](wires=qubits[i]))
            
            if len(ops) == 0:
                # All identity operators
                return qml.Identity(wires=qubits[0])
            elif len(ops) == 1:
                return ops[0]
            else:
                # Tensor product
                result = ops[0]
                for op in ops[1:]:
                    result = result @ op
                return result
    
    def sample_circuit(self, circuit: Any, shots: int) -> np.ndarray:
        """
        Sample from a quantum circuit.
        
        Parameters
        ----------
        circuit : callable
            PennyLane quantum function
        shots : int
            Number of samples
            
        Returns
        -------
        samples : ndarray
            Array of measurement samples
        """
        self.ensure_initialized()
        
        import pennylane as qml
        
        # Create sampling device
        sample_device = qml.device(
            self.device, 
            wires=self._device.num_wires, 
            shots=shots
        )
        
        @qml.qnode(sample_device)
        def qnode():
            circuit()
            return qml.sample(wires=range(self._device.num_wires))
        
        samples = qnode()
        return np.array(samples)
    
    def get_device_properties(self) -> Dict[str, Any]:
        """
        Get properties of the current device.
        
        Returns
        -------
        properties : dict
            Device properties and capabilities
        """
        self.ensure_initialized()
        
        props = {
            "name": self.device,
            "type": "simulator" if "default" in self.device else "hardware",
            "n_qubits": self._device.num_wires,
            "shots_supported": hasattr(self._device, 'shots'),
            "analytic_supported": getattr(self._device, 'analytic', False),
        }
        
        if hasattr(self._device, 'capabilities'):
            caps = self._device.capabilities()
            props.update({
                "operations": caps.get('operations', []),
                "observables": caps.get('observables', []),
                "supports_finite_shots": caps.get('supports_finite_shots', True),
                "supports_tensor_observables": caps.get('supports_tensor_observables', True),
            })
        
        return props
    
    def create_qnode(self, circuit: Any, interface: str = "numpy") -> Any:
        """
        Create a PennyLane QNode.
        
        Parameters
        ----------
        circuit : callable
            PennyLane quantum function
        interface : str, default='numpy'
            Differentiation interface
            
        Returns
        -------
        qnode : pennylane.QNode
            PennyLane QNode object
        """
        self.ensure_initialized()
        
        import pennylane as qml
        
        return qml.QNode(circuit, self._device, interface=interface)
