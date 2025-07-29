"""
Test suite for Quantum Entangled Knowledge Graphs (QE-KGR).

This module contains comprehensive tests for all core functionality.
"""

import unittest
import numpy as np
from qekgr import EntangledGraph, QuantumInference, EntangledQueryEngine
from qekgr.graphs.entangled_graph import QuantumNode, EntangledEdge


class TestEntangledGraph(unittest.TestCase):
    """Test cases for EntangledGraph class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.graph = EntangledGraph(hilbert_dim=4)
        
    def test_graph_initialization(self):
        """Test graph initialization."""
        self.assertEqual(self.graph.hilbert_dim, 4)
        self.assertEqual(len(self.graph.nodes), 0)
        self.assertEqual(len(self.graph.edges), 0)
        
    def test_add_quantum_node(self):
        """Test adding quantum nodes."""
        node = self.graph.add_quantum_node("test_node", state="test_state")
        
        self.assertIsInstance(node, QuantumNode)
        self.assertEqual(node.node_id, "test_node")
        self.assertEqual(len(node.state_vector), 4)
        self.assertAlmostEqual(np.linalg.norm(node.state_vector), 1.0)
        
    def test_add_entangled_edge(self):
        """Test adding entangled edges."""
        # Add nodes first
        node1 = self.graph.add_quantum_node("node1")
        node2 = self.graph.add_quantum_node("node2")
        
        # Add edge
        edge = self.graph.add_entangled_edge(
            node1, node2,
            relations=["relation1", "relation2"],
            amplitudes=[0.8, 0.6]
        )
        
        self.assertIsInstance(edge, EntangledEdge)
        self.assertEqual(edge.source_id, "node1")
        self.assertEqual(edge.target_id, "node2")
        self.assertEqual(len(edge.relations), 2)
        self.assertAlmostEqual(edge.entanglement_strength, 1.0, places=5)
        
    def test_quantum_state_overlap(self):
        """Test quantum state overlap calculation."""
        node1 = self.graph.add_quantum_node("node1")
        node2 = self.graph.add_quantum_node("node2") 
        
        overlap = self.graph.get_quantum_state_overlap("node1", "node2")
        self.assertIsInstance(overlap, complex)
        self.assertLessEqual(abs(overlap), 1.0)
        
    def test_entanglement_entropy(self):
        """Test entanglement entropy calculation."""
        node = self.graph.add_quantum_node("test_node")
        entropy = self.graph.get_entanglement_entropy("test_node")
        
        self.assertIsInstance(entropy, float)
        self.assertGreaterEqual(entropy, 0.0)
        
    def test_quantum_state_evolution(self):
        """Test quantum state evolution."""
        node = self.graph.add_quantum_node("test_node")
        initial_state = node.state_vector.copy()
        
        # Create simple Hamiltonian
        H = np.random.hermitian(4)
        
        # Evolve state
        self.graph.evolve_quantum_state("test_node", H, 0.1)
        evolved_state = self.graph.nodes["test_node"].state_vector
        
        # Check normalization is preserved
        self.assertAlmostEqual(np.linalg.norm(evolved_state), 1.0)
        
        # Check state has changed (unless time is 0)
        self.assertFalse(np.allclose(initial_state, evolved_state))


class TestQuantumInference(unittest.TestCase):
    """Test cases for QuantumInference class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.graph = EntangledGraph(hilbert_dim=4)
        
        # Add test nodes
        self.graph.add_quantum_node("Alice", metadata={"field": "physics"})
        self.graph.add_quantum_node("Bob", metadata={"field": "computer_science"})
        self.graph.add_quantum_node("Charlie", metadata={"field": "mathematics"})
        
        # Add edges
        self.graph.add_entangled_edge("Alice", "Bob", 
                                     relations=["collaborates"], 
                                     amplitudes=[0.8])
        self.graph.add_entangled_edge("Bob", "Charlie",
                                     relations=["mentors"],
                                     amplitudes=[0.7])
        
        self.inference = QuantumInference(self.graph)
        
    def test_quantum_walk(self):
        """Test quantum walk functionality."""
        walk_result = self.inference.quantum_walk(
            start_node="Alice",
            steps=5
        )
        
        self.assertEqual(walk_result.path[0], "Alice")
        self.assertEqual(len(walk_result.path), 6)  # start + 5 steps
        self.assertEqual(len(walk_result.amplitudes), 6)
        self.assertIsInstance(walk_result.final_state, np.ndarray)
        
    def test_grover_search(self):
        """Test Grover-like search."""
        # Search for physics researchers
        results = self.inference.grover_search(
            target_condition={"field": "physics"},
            max_iterations=5
        )
        
        self.assertIn("Alice", results)
        self.assertIsInstance(results, list)
        
    def test_interference_link_prediction(self):
        """Test interference-based link prediction."""
        predictions = self.inference.interference_link_prediction(
            source_node="Alice",
            num_predictions=2
        )
        
        self.assertIsInstance(predictions, list)
        self.assertLessEqual(len(predictions), 2)
        
        if predictions:
            pred = predictions[0]
            self.assertEqual(pred.source_node, "Alice")
            self.assertIsInstance(pred.quantum_score, float)
            self.assertGreaterEqual(pred.quantum_score, 0.0)
            self.assertLessEqual(pred.quantum_score, 1.0)
    
    def test_subgraph_discovery(self):
        """Test entangled subgraph discovery."""
        discovery = self.inference.discover_entangled_subgraph(
            seed_nodes=["Alice"],
            expansion_steps=2,
            min_entanglement=0.1
        )
        
        self.assertIn("Alice", discovery.nodes)
        self.assertIsInstance(discovery.entanglement_density, float)
        self.assertIsInstance(discovery.coherence_measure, float)
        self.assertIsInstance(discovery.discovery_confidence, float)


class TestEntangledQueryEngine(unittest.TestCase):
    """Test cases for EntangledQueryEngine class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.graph = EntangledGraph(hilbert_dim=4)
        
        # Create test knowledge graph
        self.graph.add_quantum_node("Alice", state="researcher",
                                   metadata={"field": "quantum_physics"})
        self.graph.add_quantum_node("Bob", state="professor", 
                                   metadata={"field": "computer_science"})
        
        self.graph.add_entangled_edge("Alice", "Bob",
                                     relations=["collaborates", "co_authors"],
                                     amplitudes=[0.8, 0.6])
        
        self.query_engine = EntangledQueryEngine(self.graph)
        
    def test_simple_query(self):
        """Test basic query functionality."""
        results = self.query_engine.query("Who collaborates with Alice?")
        
        self.assertIsInstance(results, list)
        self.assertGreaterEqual(len(results), 0)
        
        if results:
            result = results[0]
            self.assertIsInstance(result.confidence_score, float)
            self.assertGreaterEqual(result.confidence_score, 0.0)
            self.assertLessEqual(result.confidence_score, 1.0)
            
    def test_query_with_context(self):
        """Test query with quantum context."""
        context_vector = np.random.randn(64) + 1j * np.random.randn(64)
        context_vector = context_vector / np.linalg.norm(context_vector)
        
        results = self.query_engine.query_with_quantum_context(
            "Find quantum researchers",
            context_vector
        )
        
        self.assertIsInstance(results, list)
        
    def test_query_chain(self):
        """Test chained queries with context transfer."""
        query_chain = [
            "Who works on quantum physics?",
            "Who might they collaborate with?"
        ]
        
        results = self.query_engine.chain_queries(query_chain)
        
        self.assertEqual(len(results), 2)
        for result in results:
            self.assertIsInstance(result.confidence_score, float)
            
    def test_concept_discovery(self):
        """Test related concept discovery."""
        discovery = self.query_engine.discover_related_concepts(
            seed_concept="quantum",
            max_hops=2
        )
        
        self.assertIsInstance(discovery.nodes, set)
        self.assertIsInstance(discovery.discovery_confidence, float)
        
    def test_reasoning_explanation(self):
        """Test reasoning explanation functionality."""
        results = self.query_engine.query("Find researchers")
        
        if results:
            explanation = self.query_engine.explain_reasoning(results[0])
            
            self.assertIn("quantum_effects", explanation)
            self.assertIn("confidence_breakdown", explanation)
            self.assertIn("reasoning_steps", explanation)


class TestQuantumNode(unittest.TestCase):
    """Test cases for QuantumNode class."""
    
    def test_node_initialization(self):
        """Test quantum node initialization."""
        node = QuantumNode(node_id="test", metadata={"key": "value"})
        
        self.assertEqual(node.node_id, "test")
        self.assertEqual(node.hilbert_dim, 2)  # Default dimension
        self.assertAlmostEqual(np.linalg.norm(node.state_vector), 1.0)
        
    def test_entropy_calculation(self):
        """Test entropy calculation for quantum nodes."""
        node = QuantumNode(node_id="test")
        entropy = node.measure_entropy()
        
        self.assertIsInstance(entropy, float)
        self.assertGreaterEqual(entropy, 0.0)


class TestEntangledEdge(unittest.TestCase):
    """Test cases for EntangledEdge class."""
    
    def test_edge_initialization(self):
        """Test entangled edge initialization."""
        edge = EntangledEdge(
            source_id="A",
            target_id="B", 
            relations=["rel1", "rel2"],
            amplitudes=[0.8, 0.6]
        )
        
        self.assertEqual(edge.source_id, "A")
        self.assertEqual(edge.target_id, "B")
        self.assertEqual(len(edge.relations), 2)
        
        # Check amplitude normalization
        total_prob = sum(abs(amp)**2 for amp in edge.amplitudes)
        self.assertAlmostEqual(total_prob, 1.0, places=5)
        
    def test_entanglement_strength(self):
        """Test entanglement strength calculation."""
        edge = EntangledEdge(
            source_id="A",
            target_id="B",
            relations=["rel1"],
            amplitudes=[0.8]
        )
        
        strength = edge.entanglement_strength
        self.assertIsInstance(strength, float)
        self.assertGreaterEqual(strength, 0.0)
        self.assertLessEqual(strength, 1.0)
        
    def test_relation_collapse(self):
        """Test quantum measurement collapse of relations."""
        edge = EntangledEdge(
            source_id="A",
            target_id="B",
            relations=["rel1", "rel2"],
            amplitudes=[0.8, 0.6]
        )
        
        collapsed_relation = edge.collapse_relation()
        self.assertIn(collapsed_relation, edge.relations)


class TestIntegration(unittest.TestCase):
    """Integration tests for complete workflows."""
    
    def test_complete_workflow(self):
        """Test complete QE-KGR workflow."""
        # Create graph
        graph = EntangledGraph(hilbert_dim=4)
        
        # Add nodes and edges
        graph.add_quantum_node("Researcher1", metadata={"field": "AI"})
        graph.add_quantum_node("Researcher2", metadata={"field": "Quantum"})
        graph.add_entangled_edge("Researcher1", "Researcher2",
                                relations=["collaborates"],
                                amplitudes=[0.8])
        
        # Run inference
        inference = QuantumInference(graph)
        walk = inference.quantum_walk("Researcher1", steps=3)
        
        # Run queries
        query_engine = EntangledQueryEngine(graph)
        results = query_engine.query("Find AI researchers")
        
        # Basic assertions
        self.assertIsNotNone(walk)
        self.assertIsInstance(results, list)
        
    def test_error_handling(self):
        """Test error handling in various scenarios."""
        graph = EntangledGraph()
        
        # Test node not found
        with self.assertRaises(ValueError):
            graph.get_entanglement_entropy("nonexistent_node")
            
        # Test edge between non-existent nodes
        with self.assertRaises(ValueError):
            graph.add_entangled_edge("A", "B", ["rel"], [1.0])
            
        # Test inference with empty graph
        inference = QuantumInference(graph)
        with self.assertRaises(ValueError):
            inference.quantum_walk("nonexistent", steps=5)


if __name__ == "__main__":
    unittest.main()
