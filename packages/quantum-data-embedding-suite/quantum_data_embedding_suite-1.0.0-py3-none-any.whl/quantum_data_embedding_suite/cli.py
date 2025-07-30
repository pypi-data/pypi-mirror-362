"""
Command-line interface for quantum data embedding suite.
"""

import click
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Optional, List

from . import QuantumEmbeddingPipeline
from .utils import generate_random_data
from .visualization import plot_kernel_comparison, plot_expressibility_analysis
from .licensing import validate_license_for_class, check_license_status, get_machine_id


@click.group()
@click.version_option()
def main():
    """Quantum Data Embedding Suite CLI for rapid experimentation."""
    # Check license status on CLI startup
    status = check_license_status()
    if status["status"] != "valid":
        click.echo(f"⚠️  License Status: {status['message']}", err=True)
        click.echo(f"Machine ID: {status['machine_id']}", err=True)


@main.command()
def license_info():
    """Display license information and machine ID."""
    status = check_license_status()
    click.echo(f"License Status: {status['status']}")
    click.echo(f"Machine ID: {status['machine_id']}")
    if status["status"] != "valid":
        click.echo(f"Error: {status.get('error', 'Unknown error')}")
        click.echo("Contact bajpaikrishna715@gmail.com for license assistance")


@main.command()
@click.option('--dataset', 
              type=click.Choice(['iris', 'wine', 'breast_cancer', 'random']),
              default='iris',
              help='Dataset to use for benchmarking')
@click.option('--embedding',
              type=click.Choice(['angle', 'amplitude', 'iqp', 'data_reuploading', 'hamiltonian']),
              default='angle',
              help='Quantum embedding type')
@click.option('--n-qubits', type=int, default=4, help='Number of qubits')
@click.option('--backend', 
              type=click.Choice(['qiskit', 'pennylane']),
              default='qiskit',
              help='Quantum backend')
@click.option('--shots', type=int, default=1024, help='Number of measurement shots')
@click.option('--output', type=str, help='Output file for results')
@click.option('--verbose', is_flag=True, help='Verbose output')
def benchmark(dataset: str, embedding: str, n_qubits: int, backend: str, 
              shots: int, output: Optional[str], verbose: bool):
    """Run benchmark on sample data."""
    
    if verbose:
        click.echo(f"Running benchmark with:")
        click.echo(f"  Dataset: {dataset}")
        click.echo(f"  Embedding: {embedding}")
        click.echo(f"  Qubits: {n_qubits}")
        click.echo(f"  Backend: {backend}")
        click.echo(f"  Shots: {shots}")
    
    # Load dataset
    X, y = _load_dataset(dataset, verbose=verbose)
    
    # Limit data size for quick benchmarking
    if len(X) > 50:
        idx = np.random.choice(len(X), 50, replace=False)
        X, y = X[idx], y[idx]
    
    # Create pipeline
    try:
        pipeline = QuantumEmbeddingPipeline(
            embedding_type=embedding,
            n_qubits=n_qubits,
            backend=backend,
            shots=shots
        )
        
        if verbose:
            click.echo("Fitting embedding pipeline...")
        
        # Fit and transform
        K_quantum = pipeline.fit_transform(X)
        
        if verbose:
            click.echo("Computing embedding metrics...")
        
        # Evaluate embedding
        metrics = pipeline.evaluate_embedding(X)
        
        # Results
        results = {
            'dataset': dataset,
            'embedding': embedding,
            'n_qubits': n_qubits,
            'backend': backend,
            'shots': shots,
            'data_shape': X.shape,
            'kernel_shape': K_quantum.shape,
            **metrics
        }
        
        # Display results
        click.echo("\n=== Benchmark Results ===")
        for key, value in results.items():
            if isinstance(value, float):
                click.echo(f"{key}: {value:.4f}")
            else:
                click.echo(f"{key}: {value}")
        
        # Save results if requested
        if output:
            _save_results(results, output, verbose=verbose)
            
    except Exception as e:
        click.echo(f"Error during benchmarking: {e}", err=True)
        if verbose:
            import traceback
            click.echo(traceback.format_exc(), err=True)


@main.command()
@click.option('--embeddings', type=str, 
              default='angle,amplitude,iqp',
              help='Comma-separated list of embeddings to compare')
@click.option('--dataset',
              type=click.Choice(['iris', 'wine', 'breast_cancer', 'random']),
              default='iris',
              help='Dataset to use')
@click.option('--n-qubits', type=int, default=4, help='Number of qubits')
@click.option('--backend',
              type=click.Choice(['qiskit', 'pennylane']),
              default='qiskit',
              help='Quantum backend')
@click.option('--output', type=str, help='Output file for comparison report')
@click.option('--verbose', is_flag=True, help='Verbose output')
def compare(embeddings: str, dataset: str, n_qubits: int, backend: str,
            output: Optional[str], verbose: bool):
    """Generate embedding comparison report."""
    
    embedding_list = [e.strip() for e in embeddings.split(',')]
    
    if verbose:
        click.echo(f"Comparing embeddings: {embedding_list}")
        click.echo(f"Dataset: {dataset}")
    
    # Load dataset
    X, y = _load_dataset(dataset, verbose=verbose)
    
    # Limit data size
    if len(X) > 30:
        idx = np.random.choice(len(X), 30, replace=False)
        X, y = X[idx], y[idx]
    
    results = []
    
    for embedding in embedding_list:
        if verbose:
            click.echo(f"\nEvaluating {embedding} embedding...")
        
        try:
            pipeline = QuantumEmbeddingPipeline(
                embedding_type=embedding,
                n_qubits=n_qubits,
                backend=backend
            )
            
            # Fit and evaluate
            K = pipeline.fit_transform(X)
            metrics = pipeline.evaluate_embedding(X)
            
            result = {
                'embedding': embedding,
                'kernel_trace': np.trace(K),
                'kernel_mean': np.mean(K[~np.eye(len(K), dtype=bool)]),
                'kernel_std': np.std(K[~np.eye(len(K), dtype=bool)]),
                **metrics
            }
            
            results.append(result)
            
            if verbose:
                click.echo(f"  Expressibility: {metrics.get('expressibility', 'N/A')}")
                click.echo(f"  Trainability: {metrics.get('trainability', 'N/A')}")
                
        except Exception as e:
            click.echo(f"Error with {embedding}: {e}", err=True)
            continue
    
    # Display comparison
    if results:
        click.echo("\n=== Embedding Comparison ===")
        df = pd.DataFrame(results)
        click.echo(df.to_string(index=False, float_format='%.4f'))
        
        # Save results
        if output:
            df.to_csv(output, index=False)
            click.echo(f"\nResults saved to {output}")
    else:
        click.echo("No successful embeddings to compare.")


@main.command()
@click.option('--embedding',
              type=click.Choice(['angle', 'amplitude', 'iqp', 'data_reuploading', 'hamiltonian']),
              default='angle',
              help='Quantum embedding type')
@click.option('--data', type=str, help='Path to CSV data file')
@click.option('--dataset',
              type=click.Choice(['iris', 'wine', 'breast_cancer', 'random']),
              help='Built-in dataset (used if --data not provided)')
@click.option('--n-qubits', type=int, default=4, help='Number of qubits')
@click.option('--backend',
              type=click.Choice(['qiskit', 'pennylane']),
              default='qiskit',
              help='Quantum backend')
@click.option('--output', type=str, default='kernel_plot.png', 
              help='Output file for plot')
@click.option('--verbose', is_flag=True, help='Verbose output')
def visualize(embedding: str, data: Optional[str], dataset: Optional[str],
              n_qubits: int, backend: str, output: str, verbose: bool):
    """Visualize quantum kernel."""
    
    # Load data
    if data:
        if verbose:
            click.echo(f"Loading data from {data}")
        try:
            df = pd.read_csv(data)
            X = df.values
            y = None
        except Exception as e:
            click.echo(f"Error loading data: {e}", err=True)
            return
    else:
        dataset = dataset or 'iris'
        X, y = _load_dataset(dataset, verbose=verbose)
    
    # Limit data size for visualization
    if len(X) > 20:
        idx = np.random.choice(len(X), 20, replace=False)
        X = X[idx]
        if y is not None:
            y = y[idx]
    
    if verbose:
        click.echo(f"Creating {embedding} embedding with {n_qubits} qubits...")
    
    try:
        # Create pipeline
        pipeline = QuantumEmbeddingPipeline(
            embedding_type=embedding,
            n_qubits=n_qubits,
            backend=backend
        )
        
        # Compute quantum kernel
        K_quantum = pipeline.fit_transform(X)
        
        # Compute classical kernel for comparison
        from sklearn.metrics.pairwise import rbf_kernel
        K_classical = rbf_kernel(X)
        
        # Create visualization
        if verbose:
            click.echo("Generating visualization...")
        
        try:
            plot_kernel_comparison(K_quantum, K_classical, output)
            click.echo(f"Visualization saved to {output}")
        except ImportError:
            # Fallback: save kernel matrices as CSV
            output_base = Path(output).stem
            np.savetxt(f"{output_base}_quantum.csv", K_quantum, delimiter=',')
            np.savetxt(f"{output_base}_classical.csv", K_classical, delimiter=',')
            click.echo(f"Kernel matrices saved as CSV files")
            
    except Exception as e:
        click.echo(f"Error during visualization: {e}", err=True)
        if verbose:
            import traceback
            click.echo(traceback.format_exc(), err=True)


@main.command()
@click.option('--config', type=str, help='Path to YAML configuration file')
@click.option('--output', type=str, default='experiment_results.json',
              help='Output file for results')
@click.option('--verbose', is_flag=True, help='Verbose output')
def experiment(config: Optional[str], output: str, verbose: bool):
    """Run custom experiment from configuration file."""
    
    if not config:
        click.echo("Configuration file is required for custom experiments.", err=True)
        return
    
    if verbose:
        click.echo(f"Loading experiment configuration from {config}")
    
    try:
        import yaml
        with open(config, 'r') as f:
            exp_config = yaml.safe_load(f)
    except Exception as e:
        click.echo(f"Error loading configuration: {e}", err=True)
        return
    
    # Run experiment based on configuration
    try:
        results = _run_custom_experiment(exp_config, verbose=verbose)
        
        # Save results
        import json
        with open(output, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        click.echo(f"Experiment results saved to {output}")
        
    except Exception as e:
        click.echo(f"Error during experiment: {e}", err=True)
        if verbose:
            import traceback
            click.echo(traceback.format_exc(), err=True)


def _load_dataset(dataset: str, verbose: bool = False):
    """Load dataset for benchmarking."""
    
    if dataset == 'random':
        if verbose:
            click.echo("Generating random dataset...")
        X = generate_random_data(100, 4, 'gaussian', seed=42)
        y = np.random.randint(0, 2, 100)
        return X, y
    
    try:
        from sklearn.datasets import load_iris, load_wine, load_breast_cancer
        
        if dataset == 'iris':
            data = load_iris()
        elif dataset == 'wine':
            data = load_wine()
        elif dataset == 'breast_cancer':
            data = load_breast_cancer()
        else:
            raise ValueError(f"Unknown dataset: {dataset}")
        
        X, y = data.data, data.target
        
        # Normalize features
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        X = scaler.fit_transform(X)
        
        if verbose:
            click.echo(f"Loaded {dataset} dataset: {X.shape[0]} samples, {X.shape[1]} features")
        
        return X, y
        
    except ImportError:
        if verbose:
            click.echo("Scikit-learn not available, using random data")
        X = generate_random_data(100, 4, 'gaussian', seed=42)
        y = np.random.randint(0, 3, 100)
        return X, y


def _save_results(results: dict, output: str, verbose: bool = False):
    """Save results to file."""
    
    try:
        if output.endswith('.json'):
            import json
            with open(output, 'w') as f:
                json.dump(results, f, indent=2, default=str)
        elif output.endswith('.csv'):
            df = pd.DataFrame([results])
            df.to_csv(output, index=False)
        else:
            # Default to JSON
            import json
            with open(output + '.json', 'w') as f:
                json.dump(results, f, indent=2, default=str)
        
        if verbose:
            click.echo(f"Results saved to {output}")
            
    except Exception as e:
        click.echo(f"Error saving results: {e}", err=True)


def _run_custom_experiment(config: dict, verbose: bool = False):
    """Run custom experiment from configuration."""
    
    # This is a placeholder for custom experiment functionality
    # In a full implementation, this would parse the YAML config
    # and run complex multi-embedding experiments
    
    results = {
        'experiment_type': 'custom',
        'config': config,
        'status': 'completed',
        'message': 'Custom experiments require full implementation'
    }
    
    if verbose:
        click.echo("Custom experiment functionality is a placeholder")
    
    return results


if __name__ == '__main__':
    main()
