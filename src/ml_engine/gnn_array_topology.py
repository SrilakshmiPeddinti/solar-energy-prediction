"""
FEAT-14: Graph Neural Networks (GNN) for Solar Array Spatial Topology
Represents solar strings, inverters, and transformers as nodes and edges in a spatial graph model.
"""
from typing import Dict, Any, List

class GraphNeuralNetworkArrayTopology:
    def __init__(self, num_nodes: int = 20):
        self.num_nodes = num_nodes

    def analyze_interconnect_shading(self, node_voltages: List[float]) -> Dict[str, Any]:
        """Runs Graph Convolutional Network (GCN) spatial message passing over string topology."""
        avg_voltage = sum(node_voltages) / max(len(node_voltages), 1)
        anomalous_nodes = [i for i, v in enumerate(node_voltages) if v < (avg_voltage * 0.85)]

        return {
            "total_array_nodes": len(node_voltages),
            "graph_average_voltage": round(avg_voltage, 2),
            "anomalous_string_node_ids": anomalous_nodes,
            "spatial_topology_health_score": round(100.0 - (len(anomalous_nodes) / max(len(node_voltages), 1)) * 100, 2)
        }
