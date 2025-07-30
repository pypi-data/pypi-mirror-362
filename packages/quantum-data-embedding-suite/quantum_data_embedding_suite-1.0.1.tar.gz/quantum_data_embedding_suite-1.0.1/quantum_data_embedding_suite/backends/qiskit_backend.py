"""
Qiskit backend implementation.
"""

from typing import Any, Dict, List, Optional
import numpy as np
from .base import BaseBackend


class QiskitBackend(BaseBackend):
    """
    Qiskit backend for quantum circuit execution.
    
    Supports various Qiskit simulators and real quantum devices.
    
    Parameters
    ----------
    device : str, optional
        Qiskit device name (e.g., 'qasm_simulator', 'statevector_simulator', 'ibmq_qasm_simulator')
    shots : int, default=1024
        Number of measurement shots
    optimization_level : int, default=1
        Qiskit transpiler optimization level (0-3)
    **kwargs
        Additional Qiskit-specific parameters
    """
    
    def __init__(
        self, 
        device: Optional[str] = None, 
        shots: int = 1024,
        optimization_level: int = 1,
        **kwargs
    ):
        super().__init__(device=device, shots=shots, **kwargs)
        self.optimization_level = optimization_level
        self._backend = None
        self._provider = None
        
        # Default device
        if device is None:
            self.device = "qasm_simulator"
    
    @property
    def name(self) -> str:
        """Get the backend name."""
        return "qiskit"
    
    def initialize(self) -> None:
        """Initialize the Qiskit backend."""
        try:
            import qiskit
            from qiskit import Aer
            from qiskit.providers.aer import AerSimulator
        except ImportError:
            raise ImportError("Qiskit is required for QiskitBackend")
        
        # Handle different device types
        if self.device in ["qasm_simulator", "statevector_simulator", "unitary_simulator"]:
            # Use Aer simulators
            self._backend = Aer.get_backend(self.device)
        elif self.device.startswith("aer_"):
            # AerSimulator with specific method
            method = self.device.replace("aer_", "")
            self._backend = AerSimulator(method=method)
        elif self.device.startswith("ibmq_") or self.device.startswith("ibm_"):
            # IBM Quantum device
            self._initialize_ibm_backend()
        else:
            # Try to find the device in available backends
            try:
                self._backend = Aer.get_backend(self.device)
            except Exception:
                # Fallback to default simulator
                print(f"Warning: Device '{self.device}' not found, using qasm_simulator")
                self._backend = Aer.get_backend("qasm_simulator")
                self.device = "qasm_simulator"
    
    def _initialize_ibm_backend(self) -> None:
        """Initialize IBM Quantum backend."""
        try:
            from qiskit_ibm_runtime import QiskitRuntimeService
            
            service = QiskitRuntimeService()
            self._backend = service.backend(self.device)
            self._provider = service
        except ImportError:
            raise ImportError("qiskit-ibm-runtime is required for IBM Quantum devices")
        except Exception as e:
            raise RuntimeError(f"Failed to initialize IBM backend: {e}")
    
    def execute_circuit(
        self, 
        circuit: Any, 
        shots: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Execute a quantum circuit using Qiskit.
        
        Parameters
        ----------
        circuit : QuantumCircuit
            Qiskit quantum circuit
        shots : int, optional
            Number of shots (overrides default if provided)
            
        Returns
        -------
        result : dict
            Execution results containing counts, probabilities, etc.
        """
        self.ensure_initialized()
        
        from qiskit import transpile, execute
        
        # Use provided shots or default
        exec_shots = shots if shots is not None else self.shots
        
        # Add measurements if not present (for sampling-based backends)
        if not hasattr(circuit, 'cregs') or len(circuit.cregs) == 0:
            from qiskit import ClassicalRegister
            if self.device != "statevector_simulator":
                circuit.add_register(ClassicalRegister(circuit.num_qubits))
                circuit.measure_all()
        
        # Transpile circuit
        transpiled = transpile(
            circuit, 
            backend=self._backend,
            optimization_level=self.optimization_level
        )
        
        # Execute circuit
        job = execute(transpiled, self._backend, shots=exec_shots)
        result = job.result()
        
        # Extract results
        output = {}
        
        if hasattr(result, 'get_counts'):
            try:
                counts = result.get_counts()
                output['counts'] = counts
                
                # Convert to probabilities
                total_shots = sum(counts.values())
                probs = {state: count/total_shots for state, count in counts.items()}
                output['probabilities'] = probs
            except:
                pass
        
        if hasattr(result, 'get_statevector'):
            try:
                statevector = result.get_statevector()
                output['statevector'] = np.array(statevector.data)
            except:
                pass
        
        return output
    
    def get_statevector(self, circuit: Any) -> np.ndarray:
        """
        Get the statevector from a quantum circuit.
        
        Parameters
        ----------
        circuit : QuantumCircuit
            Qiskit quantum circuit
            
        Returns
        -------
        statevector : ndarray
            Complex amplitudes of the quantum state
        """
        self.ensure_initialized()
        
        from qiskit import Aer, transpile, execute
        
        # Use statevector simulator
        sv_backend = Aer.get_backend('statevector_simulator')
        
        # Remove any measurements
        circuit_copy = circuit.copy()
        circuit_copy.remove_final_measurements(inplace=True)
        
        # Transpile and execute
        transpiled = transpile(circuit_copy, backend=sv_backend)
        job = execute(transpiled, sv_backend)
        result = job.result()
        
        # Get statevector
        statevector = result.get_statevector()
        return np.array(statevector.data)
    
    def compute_expectation(
        self, 
        circuit: Any, 
        observable: Any
    ) -> float:
        """
        Compute expectation value of an observable.
        
        Parameters
        ----------
        circuit : QuantumCircuit
            Qiskit quantum circuit
        observable : SparsePauliOp or similar
            Qiskit observable
            
        Returns
        -------
        expectation : float
            Expectation value
        """
        self.ensure_initialized()
        
        # Get statevector
        psi = self.get_statevector(circuit)
        
        # Compute expectation value ⟨ψ|O|ψ⟩
        if hasattr(observable, 'to_matrix'):
            obs_matrix = observable.to_matrix()
        else:
            obs_matrix = observable
        
        expectation = np.real(np.conj(psi) @ obs_matrix @ psi)
        return float(expectation)
    
    def create_observable(self, pauli_string: str, qubits: List[int]) -> Any:
        """
        Create a Qiskit observable from a Pauli string.
        
        Parameters
        ----------
        pauli_string : str
            Pauli string (e.g., 'XYZ', 'ZZI')
        qubits : list of int
            Qubits to apply the observable to
            
        Returns
        -------
        observable : SparsePauliOp
            Qiskit observable object
        """
        try:
            from qiskit.quantum_info import SparsePauliOp
        except ImportError:
            raise ImportError("qiskit.quantum_info is required for observables")
        
        # Create Pauli string for specific qubits
        n_qubits = max(qubits) + 1 if qubits else len(pauli_string)
        full_pauli = ['I'] * n_qubits
        
        for i, pauli in enumerate(pauli_string):
            if i < len(qubits):
                full_pauli[qubits[i]] = pauli
        
        pauli_str = ''.join(full_pauli)
        return SparsePauliOp.from_list([(pauli_str, 1.0)])
    
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
            "type": "simulator" if "simulator" in self.device else "hardware",
            "shots_supported": True,
            "statevector_supported": "statevector" in self.device,
        }
        
        if hasattr(self._backend, 'configuration'):
            config = self._backend.configuration()
            props.update({
                "n_qubits": getattr(config, 'n_qubits', None),
                "coupling_map": getattr(config, 'coupling_map', None),
                "basis_gates": getattr(config, 'basis_gates', None),
            })
        
        return props
