"""
Command Line Interface for Quantum Entangled Knowledge Graphs (QE-KGR).

This module provides a command-line interface for interacting with quantum
entangled graphs, running queries, and generating visualizations.
"""

import argparse
import sys
import json
from typing import Dict, Any, List
import numpy as np

from qekgr import EntangledGraph, QuantumInference, EntangledQueryEngine
from qekgr.utils.visualization import QuantumGraphVisualizer


def create_sample_graph() -> EntangledGraph:
    """Create a sample quantum entangled graph for demonstration."""
    graph = EntangledGraph(hilbert_dim=4)
    
    # Add some sample nodes
    alice = graph.add_quantum_node("Alice", state="researcher", 
                                  metadata={"field": "quantum_physics", "institution": "MIT"})
    bob = graph.add_quantum_node("Bob", state="professor",
                                metadata={"field": "computer_science", "institution": "Stanford"})
    charlie = graph.add_quantum_node("Charlie", state="student",
                                    metadata={"field": "quantum_computing", "institution": "Caltech"})
    diana = graph.add_quantum_node("Diana", state="scientist",
                                  metadata={"field": "artificial_intelligence", "institution": "MIT"})
    
    # Add entangled edges
    graph.add_entangled_edge(alice, bob, 
                           relations=["collaborates", "co-authors"],
                           amplitudes=[0.8, 0.6])
    graph.add_entangled_edge(bob, charlie,
                           relations=["mentors", "supervises"],
                           amplitudes=[0.9, 0.7])
    graph.add_entangled_edge(alice, diana,
                           relations=["collaborates", "same_institution"],
                           amplitudes=[0.7, 0.8])
    graph.add_entangled_edge(charlie, diana,
                           relations=["studies_with", "discusses"],
                           amplitudes=[0.6, 0.5])
    
    return graph


def cmd_create_graph(args) -> None:
    """Create a new quantum entangled graph."""
    print("Creating new quantum entangled graph...")
    
    graph = EntangledGraph(hilbert_dim=args.hilbert_dim)
    print(f"Created graph with Hilbert dimension: {args.hilbert_dim}")
    
    # Save graph if output specified
    if args.output:
        # In a full implementation, we'd serialize the graph
        print(f"Graph would be saved to: {args.output}")
    
    print(f"Graph created: {graph}")


def cmd_add_node(args) -> None:
    """Add a quantum node to the graph."""
    print(f"Adding quantum node: {args.node_id}")
    
    # In a full implementation, we'd load an existing graph
    graph = create_sample_graph()
    
    metadata = {}
    if args.metadata:
        try:
            metadata = json.loads(args.metadata)
        except json.JSONDecodeError:
            print("Error: Invalid JSON in metadata")
            return
    
    node = graph.add_quantum_node(args.node_id, state=args.state, metadata=metadata)
    print(f"Added node: {node.node_id}")


def cmd_query(args) -> None:
    """Run a quantum query on the graph."""
    print(f"Processing quantum query: {args.query}")
    
    # Create sample graph for demonstration
    graph = create_sample_graph()
    query_engine = EntangledQueryEngine(graph)
    
    # Process query
    results = query_engine.query(args.query, max_results=args.max_results)
    
    print(f"\nQuery Results ({len(results)} found):")
    print("-" * 50)
    
    for i, result in enumerate(results, 1):
        print(f"\nResult {i}:")
        print(f"  Confidence: {result.confidence_score:.3f}")
        print(f"  Answer Nodes: {', '.join(result.answer_nodes) if result.answer_nodes else 'None'}")
        print(f"  Reasoning Path: {' -> '.join(result.reasoning_path) if result.reasoning_path else 'None'}")
        
        if args.explain and i == 1:  # Explain top result
            explanation = query_engine.explain_reasoning(result)
            print(f"\nExplanation for top result:")
            print(f"  Quantum Effects: {explanation.get('quantum_effects', {})}")
            print(f"  Confidence Breakdown: {explanation.get('confidence_breakdown', {})}")


def cmd_walk(args) -> None:
    """Perform quantum walk on the graph."""
    print(f"Starting quantum walk from node: {args.start_node}")
    
    # Create sample graph
    graph = create_sample_graph()
    inference_engine = QuantumInference(graph)
    
    # Check if start node exists
    if args.start_node not in graph.nodes:
        print(f"Error: Node '{args.start_node}' not found in graph")
        print(f"Available nodes: {', '.join(graph.get_all_nodes())}")
        return
    
    # Perform quantum walk
    walk_result = inference_engine.quantum_walk(
        start_node=args.start_node,
        steps=args.steps,
        bias_relations=args.bias_relations.split(',') if args.bias_relations else None
    )
    
    print(f"\nQuantum Walk Results:")
    print("-" * 30)
    print(f"Path: {' -> '.join(walk_result.path)}")
    print(f"Steps: {len(walk_result.path) - 1}")
    print(f"Final Amplitude: {walk_result.amplitudes[-1]:.3f}")
    print(f"Average Entanglement: {np.mean(walk_result.entanglement_trace):.3f}")


def cmd_discover(args) -> None:
    """Discover entangled subgraphs."""
    print(f"Discovering entangled subgraphs from seeds: {args.seed_nodes}")
    
    # Create sample graph
    graph = create_sample_graph()
    inference_engine = QuantumInference(graph)
    
    # Parse seed nodes
    seed_nodes = [node.strip() for node in args.seed_nodes.split(',')]
    
    # Check if seed nodes exist
    missing_nodes = [node for node in seed_nodes if node not in graph.nodes]
    if missing_nodes:
        print(f"Error: Nodes not found: {', '.join(missing_nodes)}")
        print(f"Available nodes: {', '.join(graph.get_all_nodes())}")
        return
    
    # Discover subgraph
    discovery = inference_engine.discover_entangled_subgraph(
        seed_nodes=seed_nodes,
        expansion_steps=args.expansion_steps,
        min_entanglement=args.min_entanglement
    )
    
    print(f"\nSubgraph Discovery Results:")
    print("-" * 35)
    print(f"Discovered Nodes: {', '.join(discovery.nodes)}")
    print(f"Discovered Edges: {len(discovery.edges)}")
    print(f"Entanglement Density: {discovery.entanglement_density:.3f}")
    print(f"Coherence Measure: {discovery.coherence_measure:.3f}")
    print(f"Discovery Confidence: {discovery.discovery_confidence:.3f}")


def cmd_visualize(args) -> None:
    """Generate visualization of the quantum graph."""
    print(f"Generating {args.type} visualization...")
    
    # Create sample graph
    graph = create_sample_graph()
    visualizer = QuantumGraphVisualizer(graph)
    
    try:
        if args.type == "2d":
            fig = visualizer.visualize_graph_2d()
        elif args.type == "3d":
            fig = visualizer.visualize_graph_3d()
        elif args.type == "heatmap":
            fig = visualizer.visualize_entanglement_heatmap()
        elif args.type == "states":
            fig = visualizer.visualize_quantum_states()
        elif args.type == "dashboard":
            fig = visualizer.create_interactive_dashboard()
        else:
            print(f"Error: Unknown visualization type: {args.type}")
            return
        
        if args.output:
            fig.write_html(args.output)
            print(f"Visualization saved to: {args.output}")
        else:
            fig.show()
            
    except ImportError as e:
        print(f"Error: Missing visualization dependencies: {e}")
        print("Install with: pip install quantum-entangled-knowledge-graphs[visualization]")


def cmd_info(args) -> None:
    """Display information about the graph."""
    print("Quantum Entangled Knowledge Graph Information")
    print("=" * 50)
    
    # Create sample graph
    graph = create_sample_graph()
    
    print(f"Nodes: {len(graph.nodes)}")
    print(f"Edges: {len(graph.edges)}")
    print(f"Hilbert Dimension: {graph.hilbert_dim}")
    
    print(f"\nNode Details:")
    for node_id, node in graph.nodes.items():
        entropy = graph.get_entanglement_entropy(node_id)
        neighbors = len(graph.get_neighbors(node_id))
        print(f"  {node_id}: entropy={entropy:.3f}, degree={neighbors}")
    
    print(f"\nEdge Details:")
    for (source, target), edge in graph.edges.items():
        print(f"  {source} -> {target}: strength={edge.entanglement_strength:.3f}, relations={edge.relations}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Quantum Entangled Knowledge Graphs (QE-KGR) CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  qekgr info                              # Show graph information
  qekgr query "Who collaborates with Alice?"  # Run quantum query
  qekgr walk Alice --steps 5              # Quantum walk from Alice
  qekgr discover Alice,Bob --expansion-steps 2  # Discover subgraph
  qekgr visualize 2d --output graph.html  # Generate 2D visualization
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Create graph command
    create_parser = subparsers.add_parser('create', help='Create new quantum graph')
    create_parser.add_argument('--hilbert-dim', type=int, default=2,
                              help='Hilbert space dimension (default: 2)')
    create_parser.add_argument('--output', type=str,
                              help='Output file for the graph')
    create_parser.set_defaults(func=cmd_create_graph)
    
    # Add node command
    node_parser = subparsers.add_parser('add-node', help='Add quantum node')
    node_parser.add_argument('node_id', help='Node identifier')
    node_parser.add_argument('--state', type=str, help='Initial quantum state')
    node_parser.add_argument('--metadata', type=str, help='Node metadata (JSON format)')
    node_parser.set_defaults(func=cmd_add_node)
    
    # Query command
    query_parser = subparsers.add_parser('query', help='Run quantum query')
    query_parser.add_argument('query', help='Natural language query')
    query_parser.add_argument('--max-results', type=int, default=5,
                             help='Maximum number of results (default: 5)')
    query_parser.add_argument('--explain', action='store_true',
                             help='Explain reasoning for top result')
    query_parser.set_defaults(func=cmd_query)
    
    # Quantum walk command
    walk_parser = subparsers.add_parser('walk', help='Perform quantum walk')
    walk_parser.add_argument('start_node', help='Starting node for walk')
    walk_parser.add_argument('--steps', type=int, default=10,
                            help='Number of walk steps (default: 10)')
    walk_parser.add_argument('--bias-relations', type=str,
                            help='Comma-separated list of relations to bias towards')
    walk_parser.set_defaults(func=cmd_walk)
    
    # Discover command
    discover_parser = subparsers.add_parser('discover', help='Discover entangled subgraphs')
    discover_parser.add_argument('seed_nodes', help='Comma-separated seed nodes')
    discover_parser.add_argument('--expansion-steps', type=int, default=3,
                                help='Number of expansion steps (default: 3)')
    discover_parser.add_argument('--min-entanglement', type=float, default=0.3,
                                help='Minimum entanglement threshold (default: 0.3)')
    discover_parser.set_defaults(func=cmd_discover)
    
    # Visualize command
    viz_parser = subparsers.add_parser('visualize', help='Generate visualizations')
    viz_parser.add_argument('type', choices=['2d', '3d', 'heatmap', 'states', 'dashboard'],
                           help='Visualization type')
    viz_parser.add_argument('--output', type=str,
                           help='Output HTML file')
    viz_parser.set_defaults(func=cmd_visualize)
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Display graph information')
    info_parser.set_defaults(func=cmd_info)
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        args.func(args)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
