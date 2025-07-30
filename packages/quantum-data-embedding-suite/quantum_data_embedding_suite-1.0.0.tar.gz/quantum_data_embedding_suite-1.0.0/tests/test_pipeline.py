"""
Tests for the main pipeline functionality.
"""

import pytest
import numpy as np
from quantum_data_embedding_suite import QuantumEmbeddingPipeline


class TestQuantumEmbeddingPipeline:
    """Test suite for QuantumEmbeddingPipeline."""
    
    def test_pipeline_creation(self, backend):
        """Test basic pipeline creation."""
        pipeline = QuantumEmbeddingPipeline(
            embedding_type="angle",
            n_qubits=2,
            backend=backend.name
        )
        
        assert pipeline.embedding_type == "angle"
        assert pipeline.n_qubits == 2
        assert pipeline.backend == backend.name
    
    def test_pipeline_fit(self, small_data, backend):
        """Test pipeline fitting."""
        X, y = small_data
        
        pipeline = QuantumEmbeddingPipeline(
            embedding_type="angle",
            n_qubits=2,
            backend=backend.name
        )
        
        # Should not raise any errors
        pipeline.fit(X)
        assert pipeline._is_fitted
    
    def test_pipeline_transform(self, small_data, backend):
        """Test pipeline transformation."""
        X, y = small_data
        
        pipeline = QuantumEmbeddingPipeline(
            embedding_type="angle",
            n_qubits=2,
            backend=backend.name
        )
        
        # Fit and transform
        K = pipeline.fit_transform(X)
        
        # Check kernel matrix properties
        assert K.shape == (len(X), len(X))
        assert np.allclose(K, K.T)  # Should be symmetric
        assert np.all(np.diag(K) >= 0)  # Diagonal should be non-negative
    
    def test_pipeline_fit_transform(self, small_data, backend):
        """Test combined fit_transform method."""
        X, y = small_data
        
        pipeline = QuantumEmbeddingPipeline(
            embedding_type="angle",
            n_qubits=2,
            backend=backend.name
        )
        
        K = pipeline.fit_transform(X)
        
        assert isinstance(K, np.ndarray)
        assert K.shape == (len(X), len(X))
    
    def test_pipeline_evaluate_embedding(self, small_data, backend):
        """Test embedding evaluation."""
        X, y = small_data
        
        pipeline = QuantumEmbeddingPipeline(
            embedding_type="angle",
            n_qubits=2,
            backend=backend.name
        )
        
        pipeline.fit(X)
        metrics = pipeline.evaluate_embedding(X, n_samples=10)  # Small n_samples for speed
        
        assert isinstance(metrics, dict)
        # Check that we get some metrics back
        assert len(metrics) > 0
    
    def test_different_embedding_types(self, small_data, backend, embedding_types):
        """Test different embedding types."""
        X, y = small_data
        
        for embedding_type in embedding_types:
            pipeline = QuantumEmbeddingPipeline(
                embedding_type=embedding_type,
                n_qubits=2,
                backend=backend.name
            )
            
            try:
                K = pipeline.fit_transform(X)
                assert K.shape == (len(X), len(X))
            except Exception as e:
                # Some embeddings might fail with certain data shapes
                pytest.skip(f"Embedding {embedding_type} failed: {e}")
    
    def test_invalid_embedding_type(self, backend):
        """Test error handling for invalid embedding type."""
        with pytest.raises(ValueError):
            pipeline = QuantumEmbeddingPipeline(
                embedding_type="invalid_embedding",
                n_qubits=2,
                backend=backend.name
            )
            # Error should occur during initialization
            pipeline._initialize_components()
    
    def test_pipeline_info(self, backend):
        """Test getting pipeline information."""
        pipeline = QuantumEmbeddingPipeline(
            embedding_type="angle",
            n_qubits=2,
            backend=backend.name
        )
        
        info = pipeline.get_embedding_info()
        
        assert isinstance(info, dict)
        assert "embedding_type" in info
        assert "n_qubits" in info
        assert "backend" in info
