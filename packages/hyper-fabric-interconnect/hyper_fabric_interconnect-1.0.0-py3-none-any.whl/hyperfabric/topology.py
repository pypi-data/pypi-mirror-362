"""
Topology management and fabric zone orchestration.
Licensed software requiring valid activation.
"""

import asyncio
import time
import json
from typing import Dict, List, Optional, Set, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import networkx as nx
from collections import defaultdict

from .nodes import NodeSignature, HardwareType
from .exceptions import TopologyError, NodeNotFoundError
from .licensing import LicensedClass


class ZoneType(Enum):
    """Types of fabric zones."""
    COMPUTE_CLUSTER = "compute_cluster"
    STORAGE_FABRIC = "storage_fabric"
    QUANTUM_REALM = "quantum_realm"
    PHOTONIC_BACKBONE = "photonic_backbone"
    NEUROMORPHIC_MESH = "neuromorphic_mesh"
    EDGE_SWARM = "edge_swarm"
    HYBRID_DOMAIN = "hybrid_domain"


class IsolationLevel(Enum):
    """Isolation levels for fabric zones."""
    NONE = 0
    SOFT = 1
    MEDIUM = 2
    HARD = 3
    QUANTUM_SECURE = 4


@dataclass
class FabricZone:
    """
    A logical grouping of nodes with specific characteristics and policies.
    
    Fabric zones provide scalable isolation and specialized handling for
    different types of workloads (AI, quantum, HPC, etc.).
    """
    zone_id: str
    zone_type: ZoneType
    isolation_level: IsolationLevel
    nodes: Set[str] = field(default_factory=set)
    created_at: float = field(default_factory=time.time)
    
    # Zone policies
    max_nodes: Optional[int] = None
    min_latency_ns: Optional[int] = None
    max_latency_ns: Optional[int] = None
    required_bandwidth_gbps: Optional[float] = None
    quantum_coherence_required: bool = False
    photonic_priority: bool = False
    neuromorphic_optimization: bool = False
    
    # Zone state
    is_active: bool = True
    load_balancing_enabled: bool = True
    auto_scaling_enabled: bool = False
    fault_tolerance_level: int = 1
    
    # Metadata
    description: str = ""
    tags: Set[str] = field(default_factory=set)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate zone configuration."""
        if self.max_nodes is not None and self.max_nodes <= 0:
            raise ValueError("max_nodes must be positive")
        if len(self.nodes) > (self.max_nodes or float('inf')):
            raise ValueError("Initial nodes exceed max_nodes limit")
    
    def add_node(self, node_id: str) -> bool:
        """Add a node to the zone."""
        if self.max_nodes and len(self.nodes) >= self.max_nodes:
            return False
        
        self.nodes.add(node_id)
        return True
    
    def remove_node(self, node_id: str) -> bool:
        """Remove a node from the zone."""
        if node_id in self.nodes:
            self.nodes.remove(node_id)
            return True
        return False
    
    def has_node(self, node_id: str) -> bool:
        """Check if a node belongs to this zone."""
        return node_id in self.nodes
    
    def get_node_count(self) -> int:
        """Get the number of nodes in the zone."""
        return len(self.nodes)
    
    def is_full(self) -> bool:
        """Check if the zone is at capacity."""
        return self.max_nodes is not None and len(self.nodes) >= self.max_nodes
    
    def get_utilization(self) -> float:
        """Get zone utilization as a percentage."""
        if self.max_nodes is None:
            return 0.0
        return (len(self.nodes) / self.max_nodes) * 100.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert zone to dictionary."""
        return {
            "zone_id": self.zone_id,
            "zone_type": self.zone_type.value,
            "isolation_level": self.isolation_level.value,
            "nodes": list(self.nodes),
            "created_at": self.created_at,
            "max_nodes": self.max_nodes,
            "min_latency_ns": self.min_latency_ns,
            "max_latency_ns": self.max_latency_ns,
            "required_bandwidth_gbps": self.required_bandwidth_gbps,
            "quantum_coherence_required": self.quantum_coherence_required,
            "photonic_priority": self.photonic_priority,
            "neuromorphic_optimization": self.neuromorphic_optimization,
            "is_active": self.is_active,
            "load_balancing_enabled": self.load_balancing_enabled,
            "auto_scaling_enabled": self.auto_scaling_enabled,
            "fault_tolerance_level": self.fault_tolerance_level,
            "description": self.description,
            "tags": list(self.tags),
            "metadata": self.metadata,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FabricZone":
        """Create zone from dictionary."""
        # Convert enum values
        if isinstance(data.get("zone_type"), str):
            data["zone_type"] = ZoneType(data["zone_type"])
        if isinstance(data.get("isolation_level"), int):
            data["isolation_level"] = IsolationLevel(data["isolation_level"])
        
        # Convert sets
        if isinstance(data.get("nodes"), list):
            data["nodes"] = set(data["nodes"])
        if isinstance(data.get("tags"), list):
            data["tags"] = set(data["tags"])
        
        return cls(**data)


class TopologyManager(LicensedClass):
    """
    Advanced topology manager with fabric zones, auto-discovery, and optimization.
    
    Manages the overall network topology including zone orchestration,
    fault tolerance, and performance optimization.
    """
    
    def __init__(self):
        """Initialize the topology manager."""
        # STRICT LICENSE VALIDATION - NO BYPASS
        super().__init__(required_features=["core"])
        
        self.nodes: Dict[str, NodeSignature] = {}
        self.zones: Dict[str, FabricZone] = {}
        self.node_to_zones: Dict[str, Set[str]] = defaultdict(set)
        
        # Network graph for advanced analysis
        self.graph = nx.Graph()
        
        # Topology state
        self._last_optimization = time.time()
        self._auto_discovery_enabled = True
        self._fault_tolerance_enabled = True
        
        # Statistics and monitoring
        self._stats = {
            "total_nodes": 0,
            "total_zones": 0,
            "total_connections": 0,
            "last_topology_change": time.time(),
            "optimization_runs": 0,
            "fault_recoveries": 0,
        }
        
        # Create default zones
        self._create_default_zones()
    
    def _create_default_zones(self) -> None:
        """Create default fabric zones for common use cases."""
        default_zones = [
            FabricZone(
                zone_id="ai-supercluster",
                zone_type=ZoneType.COMPUTE_CLUSTER,
                isolation_level=IsolationLevel.MEDIUM,
                max_nodes=1000,
                required_bandwidth_gbps=400.0,
                description="High-performance AI/ML compute cluster"
            ),
            FabricZone(
                zone_id="quantum-realm",
                zone_type=ZoneType.QUANTUM_REALM,
                isolation_level=IsolationLevel.QUANTUM_SECURE,
                max_nodes=100,
                quantum_coherence_required=True,
                description="Quantum processing units with entanglement support"
            ),
            FabricZone(
                zone_id="photonic-backbone",
                zone_type=ZoneType.PHOTONIC_BACKBONE,
                isolation_level=IsolationLevel.SOFT,
                photonic_priority=True,
                description="Ultra-high-speed photonic interconnect backbone"
            ),
            FabricZone(
                zone_id="neuromorphic-mesh",
                zone_type=ZoneType.NEUROMORPHIC_MESH,
                isolation_level=IsolationLevel.MEDIUM,
                neuromorphic_optimization=True,
                description="Neuromorphic computing mesh network"
            ),
        ]
        
        for zone in default_zones:
            self.zones[zone.zone_id] = zone
            self._stats["total_zones"] += 1
    
    def register_node(self, node: NodeSignature, auto_assign_zone: bool = True) -> None:
        """
        Register a node in the topology.
        
        Args:
            node: Node signature to register
            auto_assign_zone: Whether to automatically assign the node to appropriate zones
        """
        if node.node_id in self.nodes:
            raise TopologyError(f"Node {node.node_id} is already registered")
        
        self.nodes[node.node_id] = node
        self.graph.add_node(node.node_id, **node.to_dict())
        
        if auto_assign_zone:
            self._auto_assign_zones(node)
        
        self._stats["total_nodes"] += 1
        self._stats["last_topology_change"] = time.time()
        
        # Trigger auto-discovery of connections
        if self._auto_discovery_enabled:
            self._discover_connections(node)
    
    def unregister_node(self, node_id: str) -> None:
        """Unregister a node from the topology."""
        if node_id not in self.nodes:
            raise NodeNotFoundError(f"Node {node_id} not found")
        
        # Remove from all zones
        for zone_id in self.node_to_zones[node_id].copy():
            self.remove_node_from_zone(node_id, zone_id)
        
        # Remove from graph
        if self.graph.has_node(node_id):
            self.graph.remove_node(node_id)
        
        # Remove from nodes
        del self.nodes[node_id]
        del self.node_to_zones[node_id]
        
        self._stats["total_nodes"] -= 1
        self._stats["last_topology_change"] = time.time()
    
    def _auto_assign_zones(self, node: NodeSignature) -> None:
        """Automatically assign a node to appropriate zones."""
        # AI/ML compute nodes
        gpu_types = {HardwareType.NVIDIA_H100, HardwareType.NVIDIA_A100, 
                    HardwareType.NVIDIA_V100, HardwareType.AMD_MI300X, HardwareType.INTEL_GAUDI2}
        if node.hardware_type in gpu_types:
            self.add_node_to_zone(node.node_id, "ai-supercluster")
        
        # Quantum nodes
        if node.is_quantum_capable():
            self.add_node_to_zone(node.node_id, "quantum-realm")
        
        # Photonic nodes
        if node.is_photonic_capable():
            self.add_node_to_zone(node.node_id, "photonic-backbone")
        
        # Neuromorphic nodes
        if node.is_neuromorphic_capable():
            self.add_node_to_zone(node.node_id, "neuromorphic-mesh")
    
    def _discover_connections(self, new_node: NodeSignature) -> None:
        """Discover and establish connections for a new node."""
        for existing_node in self.nodes.values():
            if existing_node.node_id != new_node.node_id:
                if self._should_connect_nodes(new_node, existing_node):
                    self.add_connection(new_node.node_id, existing_node.node_id)
    
    def _should_connect_nodes(self, node1: NodeSignature, node2: NodeSignature) -> bool:
        """Determine if two nodes should be connected."""
        # Check if nodes are in the same zone
        node1_zones = self.node_to_zones[node1.node_id]
        node2_zones = self.node_to_zones[node2.node_id]
        
        # Direct connection if in same zone
        if node1_zones & node2_zones:
            return True
        
        # Photonic nodes can connect across zones
        if node1.is_photonic_capable() or node2.is_photonic_capable():
            return True
        
        # High-performance nodes with compatible bandwidth
        if (node1.bandwidth_gbps >= 100 and node2.bandwidth_gbps >= 100 and
            abs(node1.bandwidth_gbps - node2.bandwidth_gbps) / max(node1.bandwidth_gbps, node2.bandwidth_gbps) < 0.5):
            return True
        
        # Quantum entanglement possibilities
        if node1.is_quantum_capable() and node2.is_quantum_capable():
            return True
        
        return False
    
    def add_connection(self, node1_id: str, node2_id: str, weight: Optional[float] = None) -> None:
        """Add a connection between two nodes."""
        if node1_id not in self.nodes or node2_id not in self.nodes:
            raise NodeNotFoundError("One or both nodes not found")
        
        node1 = self.nodes[node1_id]
        node2 = self.nodes[node2_id]
        
        if weight is None:
            weight = self._calculate_connection_weight(node1, node2)
        
        self.graph.add_edge(node1_id, node2_id, weight=weight)
        self._stats["total_connections"] += 1
        self._stats["last_topology_change"] = time.time()
    
    def _calculate_connection_weight(self, node1: NodeSignature, node2: NodeSignature) -> float:
        """Calculate the weight of a connection between two nodes."""
        # Base weight
        base_weight = 1.0
        
        # Latency factor
        avg_latency = (node1.latency_ns + node2.latency_ns) / 2
        latency_factor = avg_latency / 1000.0  # Normalize to microseconds
        
        # Bandwidth factor (higher bandwidth = lower weight)
        min_bandwidth = min(node1.bandwidth_gbps, node2.bandwidth_gbps)
        bandwidth_factor = 100.0 / (min_bandwidth + 1.0)
        
        # Special bonuses
        quantum_bonus = 0.5 if (node1.is_quantum_capable() and node2.is_quantum_capable()) else 1.0
        photonic_bonus = 0.3 if (node1.is_photonic_capable() or node2.is_photonic_capable()) else 1.0
        neuromorphic_bonus = 0.7 if (node1.is_neuromorphic_capable() or node2.is_neuromorphic_capable()) else 1.0
        
        return base_weight * latency_factor * bandwidth_factor * quantum_bonus * photonic_bonus * neuromorphic_bonus
    
    def remove_connection(self, node1_id: str, node2_id: str) -> None:
        """Remove a connection between two nodes."""
        if self.graph.has_edge(node1_id, node2_id):
            self.graph.remove_edge(node1_id, node2_id)
            self._stats["total_connections"] -= 1
            self._stats["last_topology_change"] = time.time()
    
    def create_zone(self, zone: FabricZone) -> None:
        """Create a new fabric zone."""
        # STRICT LICENSE VALIDATION - NO BYPASS
        required_features = ["core"]
        if zone.zone_type in [ZoneType.QUANTUM_REALM, ZoneType.NEUROMORPHIC_MESH]:
            required_features.append("professional")
        elif zone.zone_type in [ZoneType.HYBRID_DOMAIN] or zone.isolation_level == IsolationLevel.QUANTUM_SECURE:
            required_features.append("enterprise")
        
        self._validate_license(required_features)
        
        if zone.zone_id in self.zones:
            raise TopologyError(f"Zone {zone.zone_id} already exists")
        
        self.zones[zone.zone_id] = zone
        self._stats["total_zones"] += 1
    
    def delete_zone(self, zone_id: str) -> None:
        """Delete a fabric zone."""
        if zone_id not in self.zones:
            raise TopologyError(f"Zone {zone_id} not found")
        
        zone = self.zones[zone_id]
        
        # Remove all nodes from the zone
        for node_id in zone.nodes.copy():
            self.remove_node_from_zone(node_id, zone_id)
        
        del self.zones[zone_id]
        self._stats["total_zones"] -= 1
    
    def add_node_to_zone(self, node_id: str, zone_id: str) -> bool:
        """Add a node to a zone."""
        if node_id not in self.nodes:
            raise NodeNotFoundError(f"Node {node_id} not found")
        if zone_id not in self.zones:
            raise TopologyError(f"Zone {zone_id} not found")
        
        zone = self.zones[zone_id]
        if zone.add_node(node_id):
            self.node_to_zones[node_id].add(zone_id)
            return True
        return False
    
    def remove_node_from_zone(self, node_id: str, zone_id: str) -> bool:
        """Remove a node from a zone."""
        if zone_id not in self.zones:
            return False
        
        zone = self.zones[zone_id]
        if zone.remove_node(node_id):
            self.node_to_zones[node_id].discard(zone_id)
            return True
        return False
    
    def get_node_zones(self, node_id: str) -> Set[str]:
        """Get all zones that a node belongs to."""
        return self.node_to_zones[node_id].copy()
    
    def get_zone_nodes(self, zone_id: str) -> Set[str]:
        """Get all nodes in a zone."""
        if zone_id not in self.zones:
            raise TopologyError(f"Zone {zone_id} not found")
        return self.zones[zone_id].nodes.copy()
    
    def find_shortest_path(self, source: str, destination: str) -> Optional[List[str]]:
        """Find the shortest path between two nodes."""
        try:
            return nx.shortest_path(self.graph, source, destination, weight='weight')
        except nx.NetworkXNoPath:
            return None
    
    def find_all_paths(self, source: str, destination: str, max_length: int = 10) -> List[List[str]]:
        """Find all paths between two nodes up to a maximum length."""
        try:
            return list(nx.all_simple_paths(self.graph, source, destination, cutoff=max_length))
        except nx.NetworkXNoPath:
            return []
    
    def calculate_network_diameter(self) -> Optional[int]:
        """Calculate the network diameter (longest shortest path)."""
        if not self.graph.nodes():
            return None
        
        try:
            return nx.diameter(self.graph)
        except nx.NetworkXError:
            # Graph is not connected
            return None
    
    def get_clustering_coefficient(self) -> float:
        """Get the average clustering coefficient of the network."""
        if not self.graph.nodes():
            return 0.0
        return nx.average_clustering(self.graph)
    
    def detect_communities(self) -> List[Set[str]]:
        """Detect communities in the network using modularity optimization."""
        try:
            import networkx.algorithms.community as nx_comm
            communities = nx_comm.greedy_modularity_communities(self.graph)
            return [set(community) for community in communities]
        except ImportError:
            # Fallback to simple connected components
            return [set(component) for component in nx.connected_components(self.graph)]
    
    def analyze_node_centrality(self) -> Dict[str, Dict[str, float]]:
        """Analyze various centrality measures for all nodes."""
        if not self.graph.nodes():
            return {}
        
        try:
            centrality_measures = {
                'degree': nx.degree_centrality(self.graph),
                'betweenness': nx.betweenness_centrality(self.graph),
                'closeness': nx.closeness_centrality(self.graph),
                'eigenvector': nx.eigenvector_centrality(self.graph, max_iter=1000),
            }
            
            # Transpose to get per-node results
            node_centrality = {}
            for node in self.graph.nodes():
                node_centrality[node] = {
                    measure: values[node]
                    for measure, values in centrality_measures.items()
                }
            
            return node_centrality
        except (nx.NetworkXError, nx.PowerIterationFailedConvergence):
            return {}
    
    async def optimize_topology(self) -> Dict[str, Any]:
        """
        Optimize the network topology for performance.
        
        Returns:
            Optimization results and recommendations
        """
        optimization_start = time.time()
        results = {
            "optimizations_applied": [],
            "recommendations": [],
            "metrics_before": self._get_topology_metrics(),
            "metrics_after": {},
            "optimization_time_ms": 0.0,
        }
        
        # Remove redundant connections
        redundant_removed = self._remove_redundant_connections()
        if redundant_removed > 0:
            results["optimizations_applied"].append(f"Removed {redundant_removed} redundant connections")
        
        # Add missing critical connections
        critical_added = self._add_critical_connections()
        if critical_added > 0:
            results["optimizations_applied"].append(f"Added {critical_added} critical connections")
        
        # Optimize zone assignments
        zone_optimizations = await self._optimize_zone_assignments()
        if zone_optimizations:
            results["optimizations_applied"].extend(zone_optimizations)
        
        # Generate recommendations
        recommendations = self._generate_optimization_recommendations()
        results["recommendations"] = recommendations
        
        # Final metrics
        results["metrics_after"] = self._get_topology_metrics()
        results["optimization_time_ms"] = (time.time() - optimization_start) * 1000
        
        self._stats["optimization_runs"] += 1
        self._last_optimization = time.time()
        
        return results
    
    def _remove_redundant_connections(self) -> int:
        """Remove redundant connections that don't improve connectivity."""
        removed_count = 0
        edges_to_remove = []
        
        for edge in self.graph.edges():
            node1, node2 = edge
            # Temporarily remove edge
            self.graph.remove_edge(node1, node2)
            
            # Check if nodes are still connected through alternative paths
            try:
                alternative_path = nx.shortest_path(self.graph, node1, node2)
                if len(alternative_path) <= 3:  # If there's a short alternative path
                    edges_to_remove.append(edge)
                    removed_count += 1
            except nx.NetworkXNoPath:
                # No alternative path, keep the edge
                pass
            
            # Restore edge for now
            self.graph.add_edge(node1, node2)
        
        # Actually remove the redundant edges
        for edge in edges_to_remove:
            self.graph.remove_edge(edge[0], edge[1])
        
        return removed_count
    
    def _add_critical_connections(self) -> int:
        """Add connections to improve network resilience and performance."""
        added_count = 0
        
        # Identify nodes with low connectivity
        degree_centrality = nx.degree_centrality(self.graph)
        low_connectivity_nodes = [
            node for node, centrality in degree_centrality.items()
            if centrality < 0.1  # Less than 10% connectivity
        ]
        
        # Connect low-connectivity nodes to high-centrality nodes
        betweenness_centrality = nx.betweenness_centrality(self.graph)
        high_centrality_nodes = sorted(
            betweenness_centrality.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]  # Top 5 most central nodes
        
        for low_node in low_connectivity_nodes:
            for high_node, _ in high_centrality_nodes:
                if (low_node != high_node and 
                    not self.graph.has_edge(low_node, high_node) and
                    self._should_connect_nodes(self.nodes[low_node], self.nodes[high_node])):
                    
                    self.add_connection(low_node, high_node)
                    added_count += 1
                    break  # Only add one connection per low-connectivity node
        
        return added_count
    
    async def _optimize_zone_assignments(self) -> List[str]:
        """Optimize node assignments to zones."""
        optimizations = []
        
        # Move nodes to more appropriate zones based on their characteristics
        for node_id, node in self.nodes.items():
            current_zones = self.get_node_zones(node_id)
            recommended_zones = self._get_recommended_zones_for_node(node)
            
            # Add to recommended zones if not already present
            for zone_id in recommended_zones:
                if zone_id not in current_zones and zone_id in self.zones:
                    if self.add_node_to_zone(node_id, zone_id):
                        optimizations.append(f"Added {node_id} to zone {zone_id}")
            
            # Remove from inappropriate zones
            for zone_id in current_zones:
                if zone_id not in recommended_zones:
                    zone = self.zones[zone_id]
                    if not self._node_fits_zone_requirements(node, zone):
                        self.remove_node_from_zone(node_id, zone_id)
                        optimizations.append(f"Removed {node_id} from zone {zone_id}")
        
        return optimizations
    
    def _get_recommended_zones_for_node(self, node: NodeSignature) -> Set[str]:
        """Get recommended zones for a node based on its characteristics."""
        recommended = set()
        
        # GPU nodes should be in compute clusters
        gpu_types = {HardwareType.NVIDIA_H100, HardwareType.NVIDIA_A100, 
                    HardwareType.NVIDIA_V100, HardwareType.AMD_MI300X, HardwareType.INTEL_GAUDI2}
        if node.hardware_type in gpu_types:
            recommended.add("ai-supercluster")
        
        # Quantum nodes
        if node.is_quantum_capable():
            recommended.add("quantum-realm")
        
        # Photonic nodes
        if node.is_photonic_capable():
            recommended.add("photonic-backbone")
        
        # Neuromorphic nodes
        if node.is_neuromorphic_capable():
            recommended.add("neuromorphic-mesh")
        
        return recommended
    
    def _node_fits_zone_requirements(self, node: NodeSignature, zone: FabricZone) -> bool:
        """Check if a node meets zone requirements."""
        # Check bandwidth requirements
        if zone.required_bandwidth_gbps and node.bandwidth_gbps < zone.required_bandwidth_gbps:
            return False
        
        # Check latency constraints
        if zone.max_latency_ns and node.latency_ns > zone.max_latency_ns:
            return False
        
        # Check quantum requirements
        if zone.quantum_coherence_required and not node.is_quantum_capable():
            return False
        
        return True
    
    def _generate_optimization_recommendations(self) -> List[str]:
        """Generate optimization recommendations."""
        recommendations = []
        
        # Check network connectivity
        if not nx.is_connected(self.graph):
            recommendations.append("Network is not fully connected - consider adding more inter-zone links")
        
        # Check zone utilization
        for zone_id, zone in self.zones.items():
            utilization = zone.get_utilization()
            if utilization > 90:
                recommendations.append(f"Zone {zone_id} is {utilization:.1f}% full - consider expanding capacity")
            elif utilization < 10 and zone.get_node_count() > 0:
                recommendations.append(f"Zone {zone_id} is underutilized ({utilization:.1f}%) - consider consolidation")
        
        # Check for isolated nodes
        isolated_nodes = list(nx.isolates(self.graph))
        if isolated_nodes:
            recommendations.append(f"Found {len(isolated_nodes)} isolated nodes: {isolated_nodes}")
        
        # Check network diameter
        diameter = self.calculate_network_diameter()
        if diameter and diameter > 6:
            recommendations.append(f"Network diameter is {diameter} - consider adding express links")
        
        return recommendations
    
    def _get_topology_metrics(self) -> Dict[str, Any]:
        """Get comprehensive topology metrics."""
        metrics = {
            "node_count": len(self.nodes),
            "edge_count": self.graph.number_of_edges(),
            "zone_count": len(self.zones),
            "average_degree": 0.0,
            "clustering_coefficient": 0.0,
            "diameter": None,
            "is_connected": False,
        }
        
        if self.graph.nodes():
            metrics["average_degree"] = sum(dict(self.graph.degree()).values()) / len(self.graph.nodes())
            metrics["clustering_coefficient"] = self.get_clustering_coefficient()
            metrics["diameter"] = self.calculate_network_diameter()
            metrics["is_connected"] = nx.is_connected(self.graph)
        
        return metrics
    
    async def handle_node_failure(self, node_id: str) -> Dict[str, Any]:
        """
        Handle node failure with automatic recovery.
        
        Args:
            node_id: ID of the failed node
            
        Returns:
            Recovery actions taken
        """
        if node_id not in self.nodes:
            raise NodeNotFoundError(f"Node {node_id} not found")
        
        recovery_actions = {
            "failed_node": node_id,
            "actions_taken": [],
            "alternative_routes": [],
            "affected_zones": [],
        }
        
        # Mark node as unhealthy
        self.nodes[node_id].is_healthy = False
        self.nodes[node_id].is_active = False
        
        # Find affected zones
        affected_zones = self.get_node_zones(node_id)
        recovery_actions["affected_zones"] = list(affected_zones)
        
        # Remove node connections temporarily
        neighbors = list(self.graph.neighbors(node_id))
        self.graph.remove_node(node_id)
        recovery_actions["actions_taken"].append(f"Isolated failed node {node_id}")
        
        # Find alternative routes for each affected neighbor
        for neighbor in neighbors:
            for other_neighbor in neighbors:
                if neighbor != other_neighbor:
                    try:
                        alt_path = nx.shortest_path(self.graph, neighbor, other_neighbor)
                        recovery_actions["alternative_routes"].append({
                            "from": neighbor,
                            "to": other_neighbor,
                            "path": alt_path
                        })
                    except nx.NetworkXNoPath:
                        # No alternative path available
                        pass
        
        # Re-add node to graph but keep it marked as failed
        self.graph.add_node(node_id, **self.nodes[node_id].to_dict())
        
        self._stats["fault_recoveries"] += 1
        
        return recovery_actions
    
    async def recover_node(self, node_id: str) -> None:
        """Recover a previously failed node."""
        if node_id not in self.nodes:
            raise NodeNotFoundError(f"Node {node_id} not found")
        
        # Mark node as healthy
        node = self.nodes[node_id]
        node.is_healthy = True
        node.is_active = True
        node.update_heartbeat()
        
        # Re-establish connections
        self._discover_connections(node)
    
    def export_topology(self, format: str = "json") -> str:
        """
        Export topology to various formats.
        
        Args:
            format: Export format ("json", "gml", "graphml")
            
        Returns:
            Serialized topology data
        """
        if format == "json":
            return self._export_json()
        elif format == "gml":
            return self._export_gml()
        elif format == "graphml":
            return self._export_graphml()
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    def _export_json(self) -> str:
        """Export topology as JSON."""
        data = {
            "nodes": {node_id: node.to_dict() for node_id, node in self.nodes.items()},
            "zones": {zone_id: zone.to_dict() for zone_id, zone in self.zones.items()},
            "edges": [
                {
                    "source": u,
                    "target": v,
                    "weight": data.get("weight", 1.0)
                }
                for u, v, data in self.graph.edges(data=True)
            ],
            "metadata": {
                "exported_at": time.time(),
                "stats": self._stats.copy(),
            }
        }
        return json.dumps(data, indent=2)
    
    def _export_gml(self) -> str:
        """Export topology as GML format."""
        import io
        output = io.StringIO()
        nx.write_gml(self.graph, output)
        return output.getvalue()
    
    def _export_graphml(self) -> str:
        """Export topology as GraphML format."""
        import io
        output = io.StringIO()
        nx.write_graphml(self.graph, output)
        return output.getvalue()
    
    def import_topology(self, data: str, format: str = "json") -> None:
        """
        Import topology from serialized data.
        
        Args:
            data: Serialized topology data
            format: Import format ("json", "gml", "graphml")
        """
        if format == "json":
            self._import_json(data)
        elif format == "gml":
            self._import_gml(data)
        elif format == "graphml":
            self._import_graphml(data)
        else:
            raise ValueError(f"Unsupported import format: {format}")
    
    def _import_json(self, data: str) -> None:
        """Import topology from JSON."""
        topology_data = json.loads(data)
        
        # Clear existing topology
        self.nodes.clear()
        self.zones.clear()
        self.node_to_zones.clear()
        self.graph.clear()
        
        # Import nodes
        for node_id, node_data in topology_data.get("nodes", {}).items():
            node = NodeSignature.from_dict(node_data)
            self.nodes[node_id] = node
            self.graph.add_node(node_id, **node_data)
        
        # Import zones
        for zone_id, zone_data in topology_data.get("zones", {}).items():
            zone = FabricZone.from_dict(zone_data)
            self.zones[zone_id] = zone
            
            # Rebuild node-to-zone mapping
            for node_id in zone.nodes:
                self.node_to_zones[node_id].add(zone_id)
        
        # Import edges
        for edge_data in topology_data.get("edges", []):
            self.graph.add_edge(
                edge_data["source"],
                edge_data["target"],
                weight=edge_data.get("weight", 1.0)
            )
        
        # Update stats
        if "metadata" in topology_data and "stats" in topology_data["metadata"]:
            self._stats.update(topology_data["metadata"]["stats"])
    
    def _import_gml(self, data: str) -> None:
        """Import topology from GML format."""
        import io
        input_stream = io.StringIO(data)
        self.graph = nx.read_gml(input_stream)
    
    def _import_graphml(self, data: str) -> None:
        """Import topology from GraphML format."""
        import io
        input_stream = io.StringIO(data)
        self.graph = nx.read_graphml(input_stream)
    
    def get_comprehensive_stats(self) -> Dict[str, Any]:
        """Get comprehensive topology statistics."""
        stats = self._stats.copy()
        
        # Add topology metrics
        stats.update(self._get_topology_metrics())
        
        # Add zone statistics
        zone_stats = {}
        for zone_id, zone in self.zones.items():
            zone_stats[zone_id] = {
                "node_count": zone.get_node_count(),
                "utilization": zone.get_utilization(),
                "is_active": zone.is_active,
                "zone_type": zone.zone_type.value,
                "isolation_level": zone.isolation_level.value,
            }
        stats["zones"] = zone_stats
        
        # Add hardware distribution
        hardware_distribution = defaultdict(int)
        for node in self.nodes.values():
            hardware_distribution[node.hardware_type.value] += 1
        stats["hardware_distribution"] = dict(hardware_distribution)
        
        # Add centrality analysis
        centrality_analysis = self.analyze_node_centrality()
        if centrality_analysis:
            # Get top 5 most central nodes for each measure
            top_central_nodes = {}
            for measure in ['degree', 'betweenness', 'closeness', 'eigenvector']:
                if centrality_analysis:
                    sorted_nodes = sorted(
                        centrality_analysis.items(),
                        key=lambda x: x[1].get(measure, 0),
                        reverse=True
                    )
                    top_central_nodes[measure] = [
                        {"node": node, "score": data[measure]}
                        for node, data in sorted_nodes[:5]
                    ]
            stats["centrality_leaders"] = top_central_nodes
        
        return stats
