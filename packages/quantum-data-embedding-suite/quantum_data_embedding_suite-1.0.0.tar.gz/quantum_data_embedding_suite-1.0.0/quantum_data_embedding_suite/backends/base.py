"""
Base class for quantum backends.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
import numpy as np
from ..licensing import validate_license_for_class


class BaseBackend(ABC):
    """
    Abstract base class for quantum computing backends.
    
    All backend implementations should inherit from this class and implement
    the required abstract methods.
    
    Parameters
    ----------
    device : str, optional
        Specific device/simulator to use
    shots : int, default=1024
        Number of measurement shots
    """
    
    def __init__(self, device: Optional[str] = None, shots: int = 1024, **kwargs):
        # License validation for all backend classes
        validate_license_for_class(self.__class__)
        
        self.device = device
        self.shots = shots
        self.params = kwargs
        self._initialized = False
        
    @property
    @abstractmethod
    def name(self) -> str:
        """Get the backend name."""
        pass
    
    @abstractmethod
    def initialize(self) -> None:
        """Initialize the backend."""
        pass
    
    @abstractmethod
    def execute_circuit(self, circuit: Any, shots: Optional[int] = None) -> Dict[str, Any]:
        """
        Execute a quantum circuit.
        
        Parameters
        ----------
        circuit : quantum circuit object
            Backend-specific quantum circuit
        shots : int, optional
            Number of shots (overrides default if provided)
            
        Returns
        -------
        result : dict
            Execution results containing counts, probabilities, etc.
        """
        pass
    
    @abstractmethod
    def get_statevector(self, circuit: Any) -> np.ndarray:
        """
        Get the statevector from a quantum circuit.
        
        Parameters
        ----------
        circuit : quantum circuit object
            Backend-specific quantum circuit
            
        Returns
        -------
        statevector : ndarray
            Complex amplitudes of the quantum state
        """
        pass
    
    @abstractmethod
    def compute_expectation(
        self, 
        circuit: Any, 
        observable: Any
    ) -> float:
        """
        Compute expectation value of an observable.
        
        Parameters
        ----------
        circuit : quantum circuit object
            Backend-specific quantum circuit
        observable : observable object
            Backend-specific observable
            
        Returns
        -------
        expectation : float
            Expectation value
        """
        pass
    
    @abstractmethod
    def create_observable(self, pauli_string: str, qubits: List[int]) -> Any:
        """
        Create an observable from a Pauli string.
        
        Parameters
        ----------
        pauli_string : str
            Pauli string (e.g., 'XYZ', 'ZZI')
        qubits : list of int
            Qubits to apply the observable to
            
        Returns
        -------
        observable : backend-specific observable object
        """
        pass
    
    def ensure_initialized(self) -> None:
        """Ensure the backend is initialized."""
        if not self._initialized:
            self.initialize()
            self._initialized = True
    
    def compute_fidelity(self, circuit1: Any, circuit2: Any) -> float:
        """
        Compute fidelity between two quantum circuits.
        
        Parameters
        ----------
        circuit1, circuit2 : quantum circuit objects
            Backend-specific quantum circuits
            
        Returns
        -------
        fidelity : float
            Fidelity between the two circuits
        """
        self.ensure_initialized()
        
        # Get statevectors
        psi1 = self.get_statevector(circuit1)
        psi2 = self.get_statevector(circuit2)
        
        # Compute fidelity |⟨ψ1|ψ2⟩|²
        overlap = np.abs(np.vdot(psi1, psi2)) ** 2
        return float(overlap)
    
    def compute_trace_distance(self, circuit1: Any, circuit2: Any) -> float:
        """
        Compute trace distance between two quantum circuits.
        
        Parameters
        ----------
        circuit1, circuit2 : quantum circuit objects
            Backend-specific quantum circuits
            
        Returns
        -------
        trace_distance : float
            Trace distance between the two circuits
        """
        fidelity = self.compute_fidelity(circuit1, circuit2)
        return 1.0 - fidelity
    
    def get_info(self) -> Dict[str, Any]:
        """
        Get information about the backend.
        
        Returns
        -------
        info : dict
            Dictionary containing backend information
        """
        return {
            "name": self.name,
            "device": self.device,
            "shots": self.shots,
            "initialized": self._initialized,
            "params": self.params,
        }
