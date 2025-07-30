"""
Test script to verify licensing integration.
"""

try:
    # Import the package to trigger license check
    import quantum_data_embedding_suite as qdes
    
    print("✅ Package imported successfully")
    print(f"Machine ID: {qdes.get_machine_id()}")
    
    # Try to create a pipeline (this should trigger license validation)
    try:
        pipeline = qdes.QuantumEmbeddingPipeline(
            embedding_type="angle",
            n_qubits=4
        )
        print("✅ Pipeline created successfully")
    except Exception as e:
        print(f"❌ Pipeline creation failed: {e}")
    
    # Check license status
    status = qdes.check_license_status()
    print(f"License Status: {status}")
    
except Exception as e:
    print(f"❌ Package import failed: {e}")
