"""
Tests for quantum embeddings.
"""

import pytest
import numpy as np
from quantum_data_embedding_suite.embeddings import (
    AngleEmbedding, AmplitudeEmbedding, IQPEmbedding
)


class TestAngleEmbedding:
    """Test suite for AngleEmbedding."""
    
    def test_angle_embedding_creation(self, backend, n_qubits):
        """Test angle embedding creation."""
        embedding = AngleEmbedding(n_qubits=n_qubits, backend=backend)
        
        assert embedding.n_qubits == n_qubits
        assert embedding.rotation == "Y"  # default
        assert embedding.entangling == "linear"  # default
    
    def test_angle_embedding_feature_dimension(self, backend, n_qubits):
        """Test feature dimension calculation."""
        embedding = AngleEmbedding(n_qubits=n_qubits, backend=backend)
        
        expected_features = n_qubits  # Default depth=1, rotation="Y"
        assert embedding.get_feature_dimension() == expected_features
    
    def test_angle_embedding_circuit_creation(self, backend):
        """Test circuit creation."""
        embedding = AngleEmbedding(n_qubits=2, backend=backend)
        x = np.array([0.1, 0.2])
        
        circuit = embedding.create_circuit(x)
        assert circuit is not None
    
    def test_angle_embedding_input_validation(self, backend):
        """Test input validation."""
        embedding = AngleEmbedding(n_qubits=2, backend=backend)
        
        # Wrong number of features
        with pytest.raises(ValueError):
            x = np.array([0.1, 0.2, 0.3])  # 3 features for 2 qubits
            embedding.validate_input(x)
        
        # Wrong dimensions
        with pytest.raises(ValueError):
            x = np.array([[0.1, 0.2], [0.3, 0.4]])  # 2D array
            embedding.validate_input(x)


class TestAmplitudeEmbedding:
    """Test suite for AmplitudeEmbedding."""
    
    def test_amplitude_embedding_creation(self, backend, n_qubits):
        """Test amplitude embedding creation."""
        embedding = AmplitudeEmbedding(n_qubits=n_qubits, backend=backend)
        
        assert embedding.n_qubits == n_qubits
        assert embedding.normalize == True  # default
    
    def test_amplitude_embedding_feature_dimension(self, backend):
        """Test feature dimension calculation."""
        embedding = AmplitudeEmbedding(n_qubits=2, backend=backend)
        
        expected_features = 2**2  # 2^n_qubits
        assert embedding.get_feature_dimension() == expected_features
    
    def test_amplitude_embedding_prepare_amplitudes(self, backend):
        """Test amplitude preparation."""
        embedding = AmplitudeEmbedding(n_qubits=2, backend=backend)
        
        # Test with exact size
        x = np.array([0.5, 0.5, 0.5, 0.5])
        amplitudes = embedding._prepare_amplitudes(x)
        
        assert len(amplitudes) == 4
        assert np.allclose(np.linalg.norm(amplitudes), 1.0)  # Should be normalized
    
    def test_amplitude_embedding_padding(self, backend):
        """Test padding functionality."""
        embedding = AmplitudeEmbedding(n_qubits=2, backend=backend, padding="zero")
        
        # Test with smaller input
        x = np.array([0.5, 0.5])  # Only 2 elements, need 4
        amplitudes = embedding._prepare_amplitudes(x)
        
        assert len(amplitudes) == 4
        assert amplitudes[0] == 0.5 / np.linalg.norm([0.5, 0.5, 0, 0])
        assert amplitudes[1] == 0.5 / np.linalg.norm([0.5, 0.5, 0, 0])
        assert amplitudes[2] == 0.0
        assert amplitudes[3] == 0.0


class TestIQPEmbedding:
    """Test suite for IQPEmbedding."""
    
    def test_iqp_embedding_creation(self, backend, n_qubits):
        """Test IQP embedding creation."""
        embedding = IQPEmbedding(n_qubits=n_qubits, backend=backend)
        
        assert embedding.n_qubits == n_qubits
        assert embedding._depth == 3  # default
        assert embedding.interaction_pattern == "all"  # default
    
    def test_iqp_embedding_interaction_pairs(self, backend):
        """Test interaction pair generation."""
        embedding = IQPEmbedding(n_qubits=3, backend=backend, interaction_pattern="linear")
        
        expected_pairs = [(0, 1), (1, 2)]
        assert embedding.interaction_pairs == expected_pairs
    
    def test_iqp_embedding_feature_dimension(self, backend):
        """Test feature dimension calculation."""
        embedding = IQPEmbedding(n_qubits=2, backend=backend, depth=2, interaction_pattern="all")
        
        # Should be: (n_qubits * depth) + (n_pairs * depth)
        # For 2 qubits: 2*2 + 1*2 = 6
        expected_features = 2 * 2 + 1 * 2  # single_qubit + interaction features
        assert embedding.get_feature_dimension() == expected_features
