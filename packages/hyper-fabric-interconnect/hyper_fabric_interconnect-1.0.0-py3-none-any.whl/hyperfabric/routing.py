"""
Advanced routing engine with predictive optimization and ML-enhanced path selection.
Licensed software requiring valid activation.
"""

import asyncio
import time
import random
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, deque
import heapq

from .nodes import NodeSignature, HardwareType
from .exceptions import RoutingError, NodeNotFoundError
from .licensing import LicensedClass


class RoutingStrategy(Enum):
    """Available routing strategies."""
    SHORTEST_PATH = "shortest_path"
    LOWEST_LATENCY = "lowest_latency"
    HIGHEST_BANDWIDTH = "highest_bandwidth"
    LOAD_BALANCED = "load_balanced"
    QUANTUM_OPTIMIZED = "quantum_optimized"
    PREDICTIVE_ML = "predictive_ml"
    NEUROMORPHIC_INSPIRED = "neuromorphic_inspired"


class PacketPriority(Enum):
    """Packet priority levels."""
    ULTRA_HIGH = 0
    HIGH = 1
    NORMAL = 2
    LOW = 3
    BACKGROUND = 4


@dataclass
class RouteEntry:
    """Single route entry in the routing table."""
    destination: str
    next_hop: str
    cost: float
    latency_ns: int
    bandwidth_gbps: float
    hop_count: int
    last_updated: float = field(default_factory=time.time)
    reliability_score: float = 1.0
    quantum_entangled: bool = False
    
    def is_expired(self, max_age_seconds: float = 30.0) -> bool:
        """Check if route entry is expired."""
        return time.time() - self.last_updated > max_age_seconds


@dataclass
class Packet:
    """Network packet with hyperfabric-specific metadata."""
    packet_id: str
    source: str
    destination: str
    data_size_bytes: int
    priority: PacketPriority = PacketPriority.NORMAL
    timestamp: float = field(default_factory=time.time)
    ttl: int = 64
    quantum_flags: int = 0
    neuromorphic_weight: float = 1.0
    requires_quantum_path: bool = False
    latency_constraint_ns: Optional[int] = None
    bandwidth_requirement_gbps: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class TopologyGraph:
    """Network topology graph for route calculation."""
    
    def __init__(self):
        """Initialize empty topology graph."""
        self.nodes: Dict[str, NodeSignature] = {}
        self.edges: Dict[str, Dict[str, float]] = defaultdict(dict)
        self.latency_map: Dict[str, Dict[str, int]] = defaultdict(dict)
        self.bandwidth_map: Dict[str, Dict[str, float]] = defaultdict(dict)
        self._last_update = time.time()
    
    def add_node(self, node: NodeSignature) -> None:
        """Add a node to the topology."""
        self.nodes[node.node_id] = node
        self._last_update = time.time()
    
    def remove_node(self, node_id: str) -> None:
        """Remove a node from the topology."""
        if node_id in self.nodes:
            del self.nodes[node_id]
            # Remove all edges involving this node
            if node_id in self.edges:
                del self.edges[node_id]
            for neighbor_edges in self.edges.values():
                if node_id in neighbor_edges:
                    del neighbor_edges[node_id]
            self._last_update = time.time()
    
    def add_edge(self, node1: str, node2: str, cost: float = 1.0) -> None:
        """Add a bidirectional edge between two nodes."""
        if node1 not in self.nodes or node2 not in self.nodes:
            raise NodeNotFoundError(f"One or both nodes not found: {node1}, {node2}")
        
        self.edges[node1][node2] = cost
        self.edges[node2][node1] = cost
        
        # Calculate latency and bandwidth
        node1_sig = self.nodes[node1]
        node2_sig = self.nodes[node2]
        
        latency = node1_sig.estimate_latency_to(node2_sig)
        self.latency_map[node1][node2] = latency
        self.latency_map[node2][node1] = latency
        
        bandwidth = min(
            node1_sig.get_theoretical_throughput_gbps(),
            node2_sig.get_theoretical_throughput_gbps()
        )
        self.bandwidth_map[node1][node2] = bandwidth
        self.bandwidth_map[node2][node1] = bandwidth
        
        self._last_update = time.time()
    
    def get_neighbors(self, node_id: str) -> List[str]:
        """Get all neighbors of a node."""
        return list(self.edges.get(node_id, {}).keys())
    
    def get_edge_cost(self, node1: str, node2: str) -> Optional[float]:
        """Get the cost of an edge between two nodes."""
        return self.edges.get(node1, {}).get(node2)
    
    def get_edge_latency(self, node1: str, node2: str) -> Optional[int]:
        """Get the latency of an edge between two nodes."""
        return self.latency_map.get(node1, {}).get(node2)
    
    def get_edge_bandwidth(self, node1: str, node2: str) -> Optional[float]:
        """Get the bandwidth of an edge between two nodes."""
        return self.bandwidth_map.get(node1, {}).get(node2)


class RoutingTable:
    """Advanced routing table with multiple metrics."""
    
    def __init__(self, max_entries: int = 10000):
        """Initialize routing table."""
        self.max_entries = max_entries
        self.routes: Dict[str, Dict[str, RouteEntry]] = defaultdict(dict)
        self._access_counts: Dict[Tuple[str, str], int] = defaultdict(int)
    
    def add_route(self, source: str, destination: str, route: RouteEntry) -> None:
        """Add a route to the table."""
        self.routes[source][destination] = route
        self._cleanup_if_needed()
    
    def get_route(self, source: str, destination: str) -> Optional[RouteEntry]:
        """Get a route from the table."""
        route = self.routes.get(source, {}).get(destination)
        if route and not route.is_expired():
            self._access_counts[(source, destination)] += 1
            return route
        elif route:
            # Remove expired route
            del self.routes[source][destination]
        return None
    
    def remove_route(self, source: str, destination: str) -> None:
        """Remove a route from the table."""
        if source in self.routes and destination in self.routes[source]:
            del self.routes[source][destination]
            self._access_counts.pop((source, destination), None)
    
    def _cleanup_if_needed(self) -> None:
        """Clean up table if it exceeds maximum size."""
        total_routes = sum(len(routes) for routes in self.routes.values())
        if total_routes > self.max_entries:
            self._cleanup_lru_routes()
    
    def _cleanup_lru_routes(self) -> None:
        """Remove least recently used routes."""
        # Sort by access count (ascending) and remove 10% of routes
        sorted_routes = sorted(self._access_counts.items(), key=lambda x: x[1])
        routes_to_remove = int(len(sorted_routes) * 0.1)
        
        for (source, destination), _ in sorted_routes[:routes_to_remove]:
            self.remove_route(source, destination)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get routing table statistics."""
        total_routes = sum(len(routes) for routes in self.routes.values())
        expired_count = 0
        
        for source_routes in self.routes.values():
            for route in source_routes.values():
                if route.is_expired():
                    expired_count += 1
        
        return {
            "total_routes": total_routes,
            "expired_routes": expired_count,
            "sources": len(self.routes),
            "max_entries": self.max_entries,
            "utilization": total_routes / self.max_entries,
        }


class MLRoutePredictor:
    """Machine learning-based route prediction (simplified implementation)."""
    
    def __init__(self):
        """Initialize the ML predictor."""
        self.route_history: List[Tuple[str, str, float, float]] = []
        self.congestion_patterns: Dict[str, List[float]] = defaultdict(list)
        self.latency_patterns: Dict[Tuple[str, str], List[float]] = defaultdict(list)
    
    def record_route_performance(
        self,
        source: str,
        destination: str,
        latency_ns: float,
        bandwidth_used_gbps: float
    ) -> None:
        """Record route performance for learning."""
        self.route_history.append((source, destination, latency_ns, bandwidth_used_gbps))
        self.latency_patterns[(source, destination)].append(latency_ns)
        
        # Keep only recent history
        if len(self.route_history) > 10000:
            self.route_history = self.route_history[-5000:]
    
    def predict_latency(self, source: str, destination: str) -> Optional[float]:
        """Predict latency for a route based on historical data."""
        pattern = self.latency_patterns.get((source, destination), [])
        if len(pattern) < 3:
            return None
        
        # Simple moving average with recent bias
        recent_samples = pattern[-10:]
        weights = [i + 1 for i in range(len(recent_samples))]
        weighted_avg = sum(l * w for l, w in zip(recent_samples, weights)) / sum(weights)
        return weighted_avg
    
    def predict_congestion(self, node_id: str) -> float:
        """Predict congestion level for a node."""
        congestion_data = self.congestion_patterns.get(node_id, [])
        if not congestion_data:
            return 0.5  # Default moderate congestion
        
        # Return average of recent congestion levels
        recent_data = congestion_data[-20:]
        return sum(recent_data) / len(recent_data)
    
    def suggest_alternative_routes(
        self,
        source: str,
        destination: str,
        topology: TopologyGraph
    ) -> List[Tuple[List[str], float]]:
        """Suggest alternative routes with predicted performance."""
        # This is a simplified implementation
        # Real ML would use more sophisticated algorithms
        alternatives = []
        
        # Find some alternative paths through different intermediate nodes
        for intermediate in topology.nodes:
            if intermediate != source and intermediate != destination:
                if (topology.get_edge_cost(source, intermediate) is not None and
                    topology.get_edge_cost(intermediate, destination) is not None):
                    
                    path = [source, intermediate, destination]
                    predicted_latency = self._estimate_path_latency(path, topology)
                    alternatives.append((path, predicted_latency))
        
        # Sort by predicted performance
        alternatives.sort(key=lambda x: x[1])
        return alternatives[:3]  # Return top 3 alternatives
    
    def _estimate_path_latency(self, path: List[str], topology: TopologyGraph) -> float:
        """Estimate total path latency."""
        total_latency = 0.0
        for i in range(len(path) - 1):
            edge_latency = topology.get_edge_latency(path[i], path[i + 1])
            if edge_latency:
                total_latency += edge_latency
            
            # Add predicted congestion delay
            congestion = self.predict_congestion(path[i])
            total_latency += congestion * 1000  # Convert to nanoseconds
        
        return total_latency


class RoutingEngine(LicensedClass):
    """
    Advanced routing engine with multiple algorithms and ML optimization.
    
    Supports various routing strategies including quantum-optimized paths,
    neuromorphic-inspired routing, and predictive ML-based optimization.
    """
    
    def __init__(self):
        """Initialize the routing engine."""
        # STRICT LICENSE VALIDATION - NO BYPASS
        super().__init__(required_features=["core"])
        
        self.topology = TopologyGraph()
        self.routing_table = RoutingTable()
        self.ml_predictor = MLRoutePredictor()
        self.packet_queue: Dict[PacketPriority, deque] = {
            priority: deque() for priority in PacketPriority
        }
        self._stats = {
            "packets_routed": 0,
            "route_cache_hits": 0,
            "route_cache_misses": 0,
            "average_latency_ns": 0.0,
            "quantum_routes": 0,
            "ml_predictions": 0,
        }
    
    def register_node(self, node: NodeSignature) -> None:
        """Register a node in the routing topology."""
        self.topology.add_node(node)
        
        # Auto-discover connections based on hardware compatibility
        self._auto_discover_connections(node)
    
    def unregister_node(self, node_id: str) -> None:
        """Unregister a node from the routing topology."""
        self.topology.remove_node(node_id)
    
    def _auto_discover_connections(self, new_node: NodeSignature) -> None:
        """Automatically discover connections for a new node."""
        for existing_node in self.topology.nodes.values():
            if existing_node.node_id != new_node.node_id:
                # Check if nodes are compatible for direct connection
                if self._are_nodes_compatible(new_node, existing_node):
                    cost = self._calculate_connection_cost(new_node, existing_node)
                    self.topology.add_edge(new_node.node_id, existing_node.node_id, cost)
    
    def _are_nodes_compatible(self, node1: NodeSignature, node2: NodeSignature) -> bool:
        """Check if two nodes can be directly connected."""
        # Quantum nodes can connect to other quantum nodes with higher priority
        if node1.is_quantum_capable() and node2.is_quantum_capable():
            return True
        
        # Photonic nodes have high connectivity
        if node1.is_photonic_capable() or node2.is_photonic_capable():
            return True
        
        # GPU clusters can connect to each other
        gpu_types = {HardwareType.NVIDIA_H100, HardwareType.NVIDIA_A100, 
                    HardwareType.NVIDIA_V100, HardwareType.AMD_MI300X}
        if node1.hardware_type in gpu_types and node2.hardware_type in gpu_types:
            return True
        
        # Neuromorphic chips can connect to any other node
        if node1.is_neuromorphic_capable() or node2.is_neuromorphic_capable():
            return True
        
        # Default compatibility based on proximity (simplified)
        return random.random() > 0.3  # 70% chance of connection
    
    def _calculate_connection_cost(self, node1: NodeSignature, node2: NodeSignature) -> float:
        """Calculate the cost of connecting two nodes."""
        base_cost = 1.0
        
        # Lower cost for high-bandwidth connections
        min_bandwidth = min(node1.bandwidth_gbps, node2.bandwidth_gbps)
        bandwidth_factor = 1.0 / (1.0 + min_bandwidth / 100.0)
        
        # Lower cost for low-latency connections
        avg_latency = (node1.latency_ns + node2.latency_ns) / 2
        latency_factor = avg_latency / 1000.0  # Normalize to microseconds
        
        # Special bonuses for advanced hardware
        quantum_bonus = 0.5 if (node1.is_quantum_capable() and node2.is_quantum_capable()) else 1.0
        photonic_bonus = 0.3 if (node1.is_photonic_capable() or node2.is_photonic_capable()) else 1.0
        
        return base_cost * bandwidth_factor * latency_factor * quantum_bonus * photonic_bonus
    
    async def route_packet(self, packet: Packet, strategy: RoutingStrategy = RoutingStrategy.PREDICTIVE_ML) -> List[str]:
        """
        Route a packet through the network using the specified strategy.
        
        Args:
            packet: Packet to route
            strategy: Routing strategy to use
            
        Returns:
            List of node IDs representing the path
        """
        # STRICT LICENSE VALIDATION - NO BYPASS
        required_features = ["core"]
        if strategy in [RoutingStrategy.QUANTUM_OPTIMIZED, RoutingStrategy.PREDICTIVE_ML, RoutingStrategy.NEUROMORPHIC_INSPIRED]:
            required_features.append("professional")
        
        self._validate_license(required_features)
        
        if packet.source not in self.topology.nodes:
            raise NodeNotFoundError(f"Source node not found: {packet.source}")
        if packet.destination not in self.topology.nodes:
            raise NodeNotFoundError(f"Destination node not found: {packet.destination}")
        
        # Check routing table cache first
        cached_route = self.routing_table.get_route(packet.source, packet.destination)
        if cached_route and self._is_route_suitable(cached_route, packet):
            self._stats["route_cache_hits"] += 1
            return self._reconstruct_path_from_route(cached_route)
        
        self._stats["route_cache_misses"] += 1
        
        # Calculate new route based on strategy
        path = await self._calculate_route(packet, strategy)
        
        # Cache the route
        if path and len(path) > 1:
            route_entry = self._create_route_entry(path, packet)
            self.routing_table.add_route(packet.source, packet.destination, route_entry)
        
        self._stats["packets_routed"] += 1
        return path
    
    def _is_route_suitable(self, route: RouteEntry, packet: Packet) -> bool:
        """Check if a cached route is suitable for the packet requirements."""
        if packet.latency_constraint_ns and route.latency_ns > packet.latency_constraint_ns:
            return False
        if packet.bandwidth_requirement_gbps and route.bandwidth_gbps < packet.bandwidth_requirement_gbps:
            return False
        if packet.requires_quantum_path and not route.quantum_entangled:
            return False
        return True
    
    async def _calculate_route(self, packet: Packet, strategy: RoutingStrategy) -> List[str]:
        """Calculate route based on the specified strategy."""
        if strategy == RoutingStrategy.SHORTEST_PATH:
            return self._dijkstra_shortest_path(packet.source, packet.destination)
        elif strategy == RoutingStrategy.LOWEST_LATENCY:
            return self._lowest_latency_path(packet.source, packet.destination)
        elif strategy == RoutingStrategy.HIGHEST_BANDWIDTH:
            return self._highest_bandwidth_path(packet.source, packet.destination)
        elif strategy == RoutingStrategy.LOAD_BALANCED:
            return await self._load_balanced_path(packet.source, packet.destination)
        elif strategy == RoutingStrategy.QUANTUM_OPTIMIZED:
            return self._quantum_optimized_path(packet.source, packet.destination)
        elif strategy == RoutingStrategy.PREDICTIVE_ML:
            return await self._ml_optimized_path(packet)
        elif strategy == RoutingStrategy.NEUROMORPHIC_INSPIRED:
            return self._neuromorphic_path(packet)
        else:
            return self._dijkstra_shortest_path(packet.source, packet.destination)
    
    def _dijkstra_shortest_path(self, source: str, destination: str) -> List[str]:
        """Calculate shortest path using Dijkstra's algorithm."""
        distances = {node: float('inf') for node in self.topology.nodes}
        distances[source] = 0
        previous = {}
        unvisited = [(0, source)]
        
        while unvisited:
            current_distance, current = heapq.heappop(unvisited)
            
            if current == destination:
                break
            
            if current_distance > distances[current]:
                continue
            
            for neighbor in self.topology.get_neighbors(current):
                edge_cost = self.topology.get_edge_cost(current, neighbor)
                if edge_cost is None:
                    continue
                
                distance = current_distance + edge_cost
                
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current
                    heapq.heappush(unvisited, (distance, neighbor))
        
        # Reconstruct path
        path = []
        current = destination
        while current is not None:
            path.append(current)
            current = previous.get(current)
        
        return list(reversed(path)) if path[-1] == source else []
    
    def _lowest_latency_path(self, source: str, destination: str) -> List[str]:
        """Calculate path with lowest total latency."""
        distances = {node: float('inf') for node in self.topology.nodes}
        distances[source] = 0
        previous = {}
        unvisited = [(0, source)]
        
        while unvisited:
            current_latency, current = heapq.heappop(unvisited)
            
            if current == destination:
                break
            
            if current_latency > distances[current]:
                continue
            
            for neighbor in self.topology.get_neighbors(current):
                edge_latency = self.topology.get_edge_latency(current, neighbor)
                if edge_latency is None:
                    continue
                
                total_latency = current_latency + edge_latency
                
                if total_latency < distances[neighbor]:
                    distances[neighbor] = total_latency
                    previous[neighbor] = current
                    heapq.heappush(unvisited, (total_latency, neighbor))
        
        # Reconstruct path
        path = []
        current = destination
        while current is not None:
            path.append(current)
            current = previous.get(current)
        
        return list(reversed(path)) if path[-1] == source else []
    
    def _highest_bandwidth_path(self, source: str, destination: str) -> List[str]:
        """Calculate path with highest minimum bandwidth."""
        # Use modified Dijkstra with bandwidth as the metric (maximizing minimum)
        bandwidths = {node: 0 for node in self.topology.nodes}
        bandwidths[source] = float('inf')
        previous = {}
        unvisited = [(-float('inf'), source)]  # Negative for max-heap behavior
        
        while unvisited:
            current_bandwidth, current = heapq.heappop(unvisited)
            current_bandwidth = -current_bandwidth
            
            if current == destination:
                break
            
            if current_bandwidth < bandwidths[current]:
                continue
            
            for neighbor in self.topology.get_neighbors(current):
                edge_bandwidth = self.topology.get_edge_bandwidth(current, neighbor)
                if edge_bandwidth is None:
                    continue
                
                # Minimum bandwidth along the path
                path_bandwidth = min(current_bandwidth, edge_bandwidth)
                
                if path_bandwidth > bandwidths[neighbor]:
                    bandwidths[neighbor] = path_bandwidth
                    previous[neighbor] = current
                    heapq.heappush(unvisited, (-path_bandwidth, neighbor))
        
        # Reconstruct path
        path = []
        current = destination
        while current is not None:
            path.append(current)
            current = previous.get(current)
        
        return list(reversed(path)) if path[-1] == source else []
    
    async def _load_balanced_path(self, source: str, destination: str) -> List[str]:
        """Calculate load-balanced path considering node utilization."""
        # Get current load for all nodes
        node_loads = {}
        for node_id, node in self.topology.nodes.items():
            node_loads[node_id] = node.load_percentage / 100.0
        
        # Modified Dijkstra considering load
        distances = {node: float('inf') for node in self.topology.nodes}
        distances[source] = 0
        previous = {}
        unvisited = [(0, source)]
        
        while unvisited:
            current_cost, current = heapq.heappop(unvisited)
            
            if current == destination:
                break
            
            if current_cost > distances[current]:
                continue
            
            for neighbor in self.topology.get_neighbors(current):
                edge_cost = self.topology.get_edge_cost(current, neighbor)
                if edge_cost is None:
                    continue
                
                # Factor in load - higher load increases cost
                load_factor = 1 + node_loads.get(neighbor, 0) * 2
                total_cost = current_cost + edge_cost * load_factor
                
                if total_cost < distances[neighbor]:
                    distances[neighbor] = total_cost
                    previous[neighbor] = current
                    heapq.heappush(unvisited, (total_cost, neighbor))
        
        # Reconstruct path
        path = []
        current = destination
        while current is not None:
            path.append(current)
            current = previous.get(current)
        
        return list(reversed(path)) if path[-1] == source else []
    
    def _quantum_optimized_path(self, source: str, destination: str) -> List[str]:
        """Calculate quantum-optimized path prioritizing quantum-capable nodes."""
        # STRICT LICENSE VALIDATION - NO BYPASS
        self._validate_license(["professional"])
        
        # Prefer paths through quantum-capable nodes
        distances = {node: float('inf') for node in self.topology.nodes}
        distances[source] = 0
        previous = {}
        unvisited = [(0, source)]
        
        while unvisited:
            current_cost, current = heapq.heappop(unvisited)
            
            if current == destination:
                break
            
            if current_cost > distances[current]:
                continue
            
            for neighbor in self.topology.get_neighbors(current):
                edge_cost = self.topology.get_edge_cost(current, neighbor)
                if edge_cost is None:
                    continue
                
                # Quantum bonus
                neighbor_node = self.topology.nodes[neighbor]
                quantum_bonus = 0.5 if neighbor_node.is_quantum_capable() else 1.0
                
                total_cost = current_cost + edge_cost * quantum_bonus
                
                if total_cost < distances[neighbor]:
                    distances[neighbor] = total_cost
                    previous[neighbor] = current
                    heapq.heappush(unvisited, (total_cost, neighbor))
        
        # Reconstruct path
        path = []
        current = destination
        while current is not None:
            path.append(current)
            current = previous.get(current)
        
        return list(reversed(path)) if path[-1] == source else []
    
    async def _ml_optimized_path(self, packet: Packet) -> List[str]:
        """Use ML prediction to optimize routing."""
        # STRICT LICENSE VALIDATION - NO BYPASS
        self._validate_license(["professional"])
        
        self._stats["ml_predictions"] += 1
        
        # Get ML-suggested alternatives
        alternatives = self.ml_predictor.suggest_alternative_routes(
            packet.source, packet.destination, self.topology
        )
        
        if not alternatives:
            # Fall back to shortest path
            return self._dijkstra_shortest_path(packet.source, packet.destination)
        
        # Select best alternative based on packet requirements
        best_path = alternatives[0][0]  # Default to first alternative
        
        for path, predicted_latency in alternatives:
            if packet.latency_constraint_ns:
                if predicted_latency <= packet.latency_constraint_ns:
                    best_path = path
                    break
            else:
                # Choose path with best predicted performance
                best_path = path
                break
        
        return best_path
    
    def _neuromorphic_path(self, packet: Packet) -> List[str]:
        """Neuromorphic-inspired routing using adaptive weights."""
        # STRICT LICENSE VALIDATION - NO BYPASS
        self._validate_license(["professional"])
        
        # Implement simple adaptive routing inspired by neural networks
        # Each edge has a "synaptic weight" that adapts based on success
        
        # For now, implement as a variant of shortest path with random exploration
        if random.random() < 0.1:  # 10% exploration
            return self._random_walk_path(packet.source, packet.destination)
        else:
            return self._dijkstra_shortest_path(packet.source, packet.destination)
    
    def _random_walk_path(self, source: str, destination: str, max_hops: int = 10) -> List[str]:
        """Perform random walk routing (for exploration)."""
        path = [source]
        current = source
        visited = {source}
        
        for _ in range(max_hops):
            if current == destination:
                break
            
            neighbors = [n for n in self.topology.get_neighbors(current) if n not in visited]
            if not neighbors:
                # Dead end, try backtracking
                if len(path) > 1:
                    path.pop()
                    current = path[-1]
                    visited.discard(current)
                continue
            
            # Choose next hop (prefer destination if available)
            if destination in neighbors:
                next_hop = destination
            else:
                next_hop = random.choice(neighbors)
            
            path.append(next_hop)
            current = next_hop
            visited.add(current)
        
        return path if path[-1] == destination else []
    
    def _create_route_entry(self, path: List[str], packet: Packet) -> RouteEntry:
        """Create a route entry from a calculated path."""
        if len(path) < 2:
            raise RoutingError("Invalid path for route entry")
        
        total_latency = 0
        min_bandwidth = float('inf')
        total_cost = 0.0
        quantum_entangled = True
        
        for i in range(len(path) - 1):
            current = path[i]
            next_hop = path[i + 1]
            
            edge_cost = self.topology.get_edge_cost(current, next_hop)
            edge_latency = self.topology.get_edge_latency(current, next_hop)
            edge_bandwidth = self.topology.get_edge_bandwidth(current, next_hop)
            
            if edge_cost is not None:
                total_cost += edge_cost
            if edge_latency is not None:
                total_latency += edge_latency
            if edge_bandwidth is not None:
                min_bandwidth = min(min_bandwidth, edge_bandwidth)
            
            # Check if both nodes are quantum-capable
            current_node = self.topology.nodes[current]
            next_node = self.topology.nodes[next_hop]
            if not (current_node.is_quantum_capable() and next_node.is_quantum_capable()):
                quantum_entangled = False
        
        return RouteEntry(
            destination=packet.destination,
            next_hop=path[1],
            cost=total_cost,
            latency_ns=int(total_latency),
            bandwidth_gbps=min_bandwidth if min_bandwidth != float('inf') else 0.0,
            hop_count=len(path) - 1,
            quantum_entangled=quantum_entangled,
        )
    
    def _reconstruct_path_from_route(self, route: RouteEntry) -> List[str]:
        """Reconstruct full path from route entry (simplified)."""
        # This is a simplified implementation
        # In practice, you'd need to trace the full path
        return [route.destination]  # Placeholder
    
    def add_packet_to_queue(self, packet: Packet) -> None:
        """Add packet to the appropriate priority queue."""
        self.packet_queue[packet.priority].append(packet)
    
    async def process_packet_queue(self) -> None:
        """Process packets from queues in priority order."""
        for priority in PacketPriority:
            queue = self.packet_queue[priority]
            if queue:
                packet = queue.popleft()
                try:
                    path = await self.route_packet(packet)
                    # Process the packet (placeholder)
                    await self._forward_packet(packet, path)
                except Exception as e:
                    # Handle routing errors
                    print(f"Failed to route packet {packet.packet_id}: {e}")
    
    async def _forward_packet(self, packet: Packet, path: List[str]) -> None:
        """Forward packet along the calculated path."""
        # This is a placeholder for actual packet forwarding
        # In a real implementation, this would handle the actual data transfer
        
        # Record performance for ML learning
        if len(path) > 1:
            estimated_latency = sum(
                self.topology.get_edge_latency(path[i], path[i + 1]) or 0
                for i in range(len(path) - 1)
            )
            self.ml_predictor.record_route_performance(
                packet.source,
                packet.destination,
                estimated_latency,
                packet.data_size_bytes / (1024**3)  # Convert to GB
            )
        
        # Simulate forwarding delay
        await asyncio.sleep(0.001)  # 1ms simulation delay
    
    def get_topology_stats(self) -> Dict[str, Any]:
        """Get comprehensive topology statistics."""
        quantum_nodes = sum(1 for node in self.topology.nodes.values() if node.is_quantum_capable())
        photonic_nodes = sum(1 for node in self.topology.nodes.values() if node.is_photonic_capable())
        neuromorphic_nodes = sum(1 for node in self.topology.nodes.values() if node.is_neuromorphic_capable())
        
        total_edges = sum(len(edges) for edges in self.topology.edges.values()) // 2
        
        return {
            "total_nodes": len(self.topology.nodes),
            "quantum_nodes": quantum_nodes,
            "photonic_nodes": photonic_nodes,
            "neuromorphic_nodes": neuromorphic_nodes,
            "total_edges": total_edges,
            "topology_last_updated": self.topology._last_update,
            "routing_stats": self._stats.copy(),
            "routing_table_stats": self.routing_table.get_stats(),
        }
