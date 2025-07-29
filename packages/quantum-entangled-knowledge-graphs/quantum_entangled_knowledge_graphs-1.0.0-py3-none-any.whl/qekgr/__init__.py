"""
Quantum Entangled Knowledge Graphs (QE-KGR)

A revolutionary Python library that applies quantum mechanics principles 
to knowledge graph representation and reasoning.

Author: Krishna Bajpai
Contact: bajpaikrishna715@gmail.com
GitHub: https://github.com/krish567366/quantum-entangled-knowledge-graphs
"""

__version__ = "1.0.0"
__author__ = "Krishna Bajpai"
__email__ = "bajpaikrishna715@gmail.com"

# Core imports for easy access
from qekgr.graphs.entangled_graph import EntangledGraph
from qekgr.reasoning.quantum_inference import QuantumInference
from qekgr.query.entangled_query_engine import EntangledQueryEngine

__all__ = [
    "EntangledGraph",
    "QuantumInference", 
    "EntangledQueryEngine",
]
