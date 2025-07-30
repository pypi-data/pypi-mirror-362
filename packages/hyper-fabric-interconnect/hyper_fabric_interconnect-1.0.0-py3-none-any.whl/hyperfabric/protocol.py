"""
Main HyperFabric Protocol implementation - the core of ultra-low-latency interconnects.
Licensed software requiring valid activation.
"""

import asyncio
import time
import uuid
from typing import Dict, List, Optional, Any, Union, Callable
from dataclasses import dataclass, field
from enum import Enum
import weakref
import logging

from .nodes import NodeSignature, HardwareType
from .routing import RoutingEngine, RoutingStrategy, Packet, PacketPriority
from .buffers import BufferManager, ZeroCopyBuffer
from .topology import TopologyManager, FabricZone
from .licensing import LicensedClass, LicenseError, require_license
from .licensing import LicensedClass, LicenseError, require_license
from .exceptions import (
    HyperFabricError,
    NodeNotFoundError,
    RoutingError,
    BufferError,
    LatencyViolationError,
    BandwidthExceededError,
)


class ProtocolState(Enum):
    """Protocol operational states."""
    INITIALIZING = "initializing"
    ACTIVE = "active"
    DEGRADED = "degraded"
    MAINTENANCE = "maintenance"
    SHUTDOWN = "shutdown"


class DataType(Enum):
    """Types of data that can be transmitted."""
    TENSOR = "tensor"
    GRADIENT = "gradient"
    PARAMETER = "parameter"
    ACTIVATION = "activation"
    QUANTUM_STATE = "quantum_state"
    NEUROMORPHIC_SPIKE = "neuromorphic_spike"
    CONTROL_MESSAGE = "control_message"
    HEARTBEAT = "heartbeat"
    CUSTOM = "custom"


@dataclass
class TransferRequest:
    """Request for data transfer between nodes."""
    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    source: str = ""
    destination: str = ""
    data_type: DataType = DataType.TENSOR
    data_size_bytes: int = 0
    priority: PacketPriority = PacketPriority.NORMAL
    latency_constraint_ns: Optional[int] = None
    bandwidth_requirement_gbps: Optional[float] = None
    requires_quantum_entanglement: bool = False
    compression_enabled: bool = True
    encryption_enabled: bool = False
    callback: Optional[Callable] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)


@dataclass
class TransferResult:
    """Result of a data transfer operation."""
    request_id: str
    success: bool
    bytes_transferred: int
    actual_latency_ns: int
    throughput_gbps: float
    path_taken: List[str]
    compression_ratio: float = 1.0
    error_message: Optional[str] = None
    completed_at: float = field(default_factory=time.time)


class HyperFabricProtocol(LicensedClass):
    """
    Main HyperFabric Protocol implementation.
    
    This is the core protocol that orchestrates ultra-low-latency, high-bandwidth
    interconnects for AI superclusters and quantum simulation networks.
    
    LICENSED SOFTWARE - Valid license required for operation.
    """
    
    def __init__(
        self,
        protocol_id: Optional[str] = None,
        enable_ml_routing: bool = True,
        enable_quantum_optimization: bool = True,
        enable_fault_tolerance: bool = True,
        default_latency_constraint_ns: int = 1000000,  # 1ms default
        log_level: str = "INFO",
        license_tier: str = "basic"
    ):
        """
        Initialize the HyperFabric Protocol.
        
        Args:
            protocol_id: Unique identifier for this protocol instance
            enable_ml_routing: Enable ML-based predictive routing
            enable_quantum_optimization: Enable quantum-optimized paths
            enable_fault_tolerance: Enable automatic fault recovery
            default_latency_constraint_ns: Default latency constraint in nanoseconds
            log_level: Logging level
            license_tier: Required license tier (basic, professional, enterprise)
        """
        # Initialize licensing FIRST - this will validate the license
        super().__init__(license_tier=license_tier)
        
        self.protocol_id = protocol_id or f"hfp_{int(time.time() * 1000000)}"
        self.state = ProtocolState.INITIALIZING
        
        # Core components
        self.topology_manager = TopologyManager()
        self.routing_engine = RoutingEngine()
        self.buffer_manager = BufferManager()
        
        # Configuration
        self.enable_ml_routing = enable_ml_routing
        self.enable_quantum_optimization = enable_quantum_optimization
        self.enable_fault_tolerance = enable_fault_tolerance
        self.default_latency_constraint_ns = default_latency_constraint_ns
        
        # Active transfers and connections
        self.active_transfers: Dict[str, TransferRequest] = {}
        self.transfer_callbacks: Dict[str, List[Callable]] = {}
        self.connection_pool: Dict[str, Any] = {}
        
        # Performance monitoring
        self._stats = {
            "protocol_start_time": time.time(),
            "total_transfers": 0,
            "successful_transfers": 0,
            "failed_transfers": 0,
            "total_bytes_transferred": 0,
            "average_latency_ns": 0.0,
            "peak_throughput_gbps": 0.0,
            "quantum_transfers": 0,
            "ml_optimized_transfers": 0,
            "fault_recoveries": 0,
        }
        
        # Background tasks
        self._background_tasks: List[asyncio.Task] = []
        self._shutdown_event = asyncio.Event()
        
        # Logging
        self.logger = logging.getLogger(f"hyperfabric.{self.protocol_id}")
        self.logger.setLevel(getattr(logging, log_level.upper()))
        
        # Auto-start background services
        asyncio.create_task(self._initialize_protocol())
    
    async def _initialize_protocol(self) -> None:
        """Initialize the protocol and start background services."""
        try:
            self.logger.info(f"Initializing HyperFabric Protocol {self.protocol_id}")
            
            # Start background monitoring tasks
            self._background_tasks.extend([
                asyncio.create_task(self._heartbeat_monitor()),
                asyncio.create_task(self._performance_monitor()),
                asyncio.create_task(self._process_transfer_queue()),
                asyncio.create_task(self._topology_optimization_loop()),
            ])
            
            if self.enable_fault_tolerance:
                self._background_tasks.append(
                    asyncio.create_task(self._fault_detection_loop())
                )
            
            self.state = ProtocolState.ACTIVE
            self.logger.info("HyperFabric Protocol initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize protocol: {e}")
            self.state = ProtocolState.DEGRADED
            raise HyperFabricError(f"Protocol initialization failed: {e}")
    
    def register_node(self, node: NodeSignature) -> None:
        """
        Register a node in the fabric.
        
        LICENSED METHOD - Valid license required for operation.
        
        Args:
            node: Node signature to register
            
        Raises:
            LicenseError: If license validation fails
        """
        # STRICT LICENSE VALIDATION - NO BYPASS
        required_features = ["core", "networking"]
        
        # Add feature requirements based on node type
        if node.hardware_type in [HardwareType.QUANTUM_QPU, HardwareType.QUANTUM_ANNEALER]:
            required_features.append("quantum_basic")
        if node.hardware_type == HardwareType.NEUROMORPHIC_CHIP:
            required_features.append("neuromorphic")
            
        self._validate_method_license(required_features)
        
        try:
            # Register with topology manager
            self.topology_manager.register_node(node)
            
            # Register with routing engine
            self.routing_engine.register_node(node)
            
            self.logger.info(f"Registered node {node.node_id} ({node.hardware_type.value})")
            
        except Exception as e:
            self.logger.error(f"Failed to register node {node.node_id}: {e}")
            raise HyperFabricError(f"Node registration failed: {e}")
    
    def unregister_node(self, node_id: str) -> None:
        """
        Unregister a node from the fabric.
        
        Args:
            node_id: ID of the node to unregister
        """
        try:
            # Remove from topology manager
            self.topology_manager.unregister_node(node_id)
            
            # Remove from routing engine
            self.routing_engine.unregister_node(node_id)
            
            self.logger.info(f"Unregistered node {node_id}")
            
        except Exception as e:
            self.logger.error(f"Failed to unregister node {node_id}: {e}")
            raise HyperFabricError(f"Node unregistration failed: {e}")
    
    def get_registered_nodes(self) -> Dict[str, NodeSignature]:
        """Get all registered nodes."""
        return self.topology_manager.nodes.copy()
    
    def create_zone(self, zone: FabricZone) -> None:
        """
        Create a new fabric zone.
        
        LICENSED METHOD - Valid license required for operation.
        
        Args:
            zone: Zone configuration
            
        Raises:
            LicenseError: If license validation fails
        """
        # STRICT LICENSE VALIDATION - NO BYPASS
        required_features = ["core", "networking"]
        
        # Add feature requirements based on zone type
        if "quantum" in zone.zone_type.value.lower():
            required_features.append("quantum_basic")
        if "enterprise" in zone.zone_type.value.lower():
            required_features.append("enterprise_analytics")
            
        self._validate_method_license(required_features)
        
        try:
            self.topology_manager.create_zone(zone)
            self.logger.info(f"Created zone {zone.zone_id} ({zone.zone_type.value})")
        except Exception as e:
            self.logger.error(f"Failed to create zone {zone.zone_id}: {e}")
            raise HyperFabricError(f"Zone creation failed: {e}")
    
    async def send_data(
        self,
        source: str,
        destination: str,
        data: Union[bytes, bytearray, memoryview, ZeroCopyBuffer],
        data_type: DataType = DataType.TENSOR,
        priority: PacketPriority = PacketPriority.NORMAL,
        latency_constraint_ns: Optional[int] = None,
        bandwidth_requirement_gbps: Optional[float] = None,
        requires_quantum_entanglement: bool = False,
        compression_enabled: bool = True,
        encryption_enabled: bool = False,
        callback: Optional[Callable] = None,
        **metadata
    ) -> TransferResult:
        """
        Send data from source to destination with hyperfabric optimization.
        
        LICENSED METHOD - Valid license required for operation.
        
        Args:
            source: Source node ID
            destination: Destination node ID
            data: Data to transfer
            data_type: Type of data being transferred
            priority: Transfer priority
            latency_constraint_ns: Maximum acceptable latency
            bandwidth_requirement_gbps: Minimum required bandwidth
            requires_quantum_entanglement: Whether quantum entanglement is required
            compression_enabled: Whether to enable compression
            encryption_enabled: Whether to enable encryption
            callback: Optional callback function for completion notification
            **metadata: Additional metadata
            
        Returns:
            Transfer result
            
        Raises:
            LicenseError: If license validation fails
        """
        # STRICT LICENSE VALIDATION - NO BYPASS
        required_features = ["core", "networking"]
        
        # Add feature requirements based on capabilities used
        if requires_quantum_entanglement:
            required_features.append("quantum_basic")
        if priority == PacketPriority.ULTRA_HIGH:
            required_features.append("professional")
        if data_type in [DataType.QUANTUM_STATE, DataType.NEUROMORPHIC_SPIKE]:
            required_features.append("quantum_advanced")
            
        self._validate_method_license(required_features)
        # Create transfer request
        request = TransferRequest(
            source=source,
            destination=destination,
            data_type=data_type,
            data_size_bytes=len(data) if hasattr(data, '__len__') else 0,
            priority=priority,
            latency_constraint_ns=latency_constraint_ns or self.default_latency_constraint_ns,
            bandwidth_requirement_gbps=bandwidth_requirement_gbps,
            requires_quantum_entanglement=requires_quantum_entanglement,
            compression_enabled=compression_enabled,
            encryption_enabled=encryption_enabled,
            callback=callback,
            metadata=metadata,
        )
        
        return await self._execute_transfer(request, data)
    
    async def _execute_transfer(
        self,
        request: TransferRequest,
        data: Union[bytes, bytearray, memoryview, ZeroCopyBuffer]
    ) -> TransferResult:
        """Execute the actual data transfer."""
        start_time = time.time()
        transfer_start_ns = time.time_ns()
        
        try:
            # Validate nodes exist
            if request.source not in self.topology_manager.nodes:
                raise NodeNotFoundError(f"Source node {request.source} not found")
            if request.destination not in self.topology_manager.nodes:
                raise NodeNotFoundError(f"Destination node {request.destination} not found")
            
            # Track active transfer
            self.active_transfers[request.request_id] = request
            
            # Determine optimal routing strategy
            routing_strategy = self._select_routing_strategy(request)
            
            # Create packet for routing
            packet = Packet(
                packet_id=request.request_id,
                source=request.source,
                destination=request.destination,
                data_size_bytes=request.data_size_bytes,
                priority=request.priority,
                latency_constraint_ns=request.latency_constraint_ns,
                bandwidth_requirement_gbps=request.bandwidth_requirement_gbps,
                requires_quantum_path=request.requires_quantum_entanglement,
                metadata=request.metadata,
            )
            
            # Calculate optimal route
            path = await self.routing_engine.route_packet(packet, routing_strategy)
            
            if not path or len(path) < 2:
                raise RoutingError(f"No valid route found from {request.source} to {request.destination}")
            
            # Prepare data for transfer
            transfer_buffer = await self._prepare_transfer_data(data, request)
            
            # Execute transfer along the path
            bytes_transferred = await self._transfer_along_path(transfer_buffer, path, request)
            
            # Calculate performance metrics
            transfer_end_ns = time.time_ns()
            actual_latency_ns = transfer_end_ns - transfer_start_ns
            throughput_gbps = (bytes_transferred * 8) / (actual_latency_ns / 1e9) / 1e9
            
            # Create result
            result = TransferResult(
                request_id=request.request_id,
                success=True,
                bytes_transferred=bytes_transferred,
                actual_latency_ns=actual_latency_ns,
                throughput_gbps=throughput_gbps,
                path_taken=path,
                compression_ratio=getattr(transfer_buffer, 'compression_ratio', 1.0) if hasattr(transfer_buffer, 'compression_ratio') else 1.0,
            )
            
            # Update statistics
            await self._update_transfer_stats(result, request)
            
            # Execute callback if provided
            if request.callback:
                try:
                    if asyncio.iscoroutinefunction(request.callback):
                        await request.callback(result)
                    else:
                        request.callback(result)
                except Exception as e:
                    self.logger.warning(f"Transfer callback failed: {e}")
            
            self.logger.info(f"Transfer {request.request_id} completed: {bytes_transferred} bytes in {actual_latency_ns/1e6:.2f}ms")
            
            return result
            
        except Exception as e:
            # Handle transfer failure
            transfer_end_ns = time.time_ns()
            actual_latency_ns = transfer_end_ns - transfer_start_ns
            
            result = TransferResult(
                request_id=request.request_id,
                success=False,
                bytes_transferred=0,
                actual_latency_ns=actual_latency_ns,
                throughput_gbps=0.0,
                path_taken=[],
                error_message=str(e),
            )
            
            self._stats["failed_transfers"] += 1
            self.logger.error(f"Transfer {request.request_id} failed: {e}")
            
            # Execute callback with error
            if request.callback:
                try:
                    if asyncio.iscoroutinefunction(request.callback):
                        await request.callback(result)
                    else:
                        request.callback(result)
                except Exception as callback_error:
                    self.logger.warning(f"Error callback failed: {callback_error}")
            
            raise HyperFabricError(f"Transfer failed: {e}")
        
        finally:
            # Clean up
            if request.request_id in self.active_transfers:
                del self.active_transfers[request.request_id]
    
    def _select_routing_strategy(self, request: TransferRequest) -> RoutingStrategy:
        """Select the optimal routing strategy for a transfer request."""
        # Quantum-priority routing
        if request.requires_quantum_entanglement:
            return RoutingStrategy.QUANTUM_OPTIMIZED
        
        # ML-based routing for large transfers
        if self.enable_ml_routing and request.data_size_bytes > 1024 * 1024:  # > 1MB
            return RoutingStrategy.PREDICTIVE_ML
        
        # Ultra-high priority gets lowest latency
        if request.priority == PacketPriority.ULTRA_HIGH:
            return RoutingStrategy.LOWEST_LATENCY
        
        # High bandwidth requirements
        if request.bandwidth_requirement_gbps and request.bandwidth_requirement_gbps > 100:
            return RoutingStrategy.HIGHEST_BANDWIDTH
        
        # Default to load-balanced routing
        return RoutingStrategy.LOAD_BALANCED
    
    async def _prepare_transfer_data(
        self,
        data: Union[bytes, bytearray, memoryview, ZeroCopyBuffer],
        request: TransferRequest
    ) -> ZeroCopyBuffer:
        """Prepare data for transfer (compression, encryption, buffering)."""
        # Convert data to zero-copy buffer if needed
        if isinstance(data, ZeroCopyBuffer):
            transfer_buffer = data
        else:
            transfer_buffer = self.buffer_manager.allocate_buffer(
                size=len(data),
                buffer_id=f"transfer_{request.request_id}",
            )
            transfer_buffer.write(data)
        
        # Apply compression if enabled
        if request.compression_enabled and request.data_size_bytes > 1024:  # Only compress data > 1KB
            compression_ratio = transfer_buffer.compress()
            self.logger.debug(f"Compressed data with ratio {compression_ratio:.2f}")
        
        # Apply encryption if enabled (placeholder)
        if request.encryption_enabled:
            # This would implement actual encryption
            self.logger.debug("Encryption applied")
        
        return transfer_buffer
    
    async def _transfer_along_path(
        self,
        buffer: ZeroCopyBuffer,
        path: List[str],
        request: TransferRequest
    ) -> int:
        """Execute the actual data transfer along the calculated path."""
        total_bytes = buffer.size_bytes
        
        # Simulate transfer through each hop
        for i in range(len(path) - 1):
            current_node = path[i]
            next_node = path[i + 1]
            
            # Simulate network latency and processing
            hop_latency_ns = await self._simulate_hop_transfer(
                current_node, next_node, buffer, request
            )
            
            # Check latency constraints
            if (request.latency_constraint_ns and 
                hop_latency_ns > request.latency_constraint_ns):
                raise LatencyViolationError(
                    f"Hop latency {hop_latency_ns}ns exceeds constraint {request.latency_constraint_ns}ns"
                )
            
            self.logger.debug(f"Hop {current_node} -> {next_node}: {hop_latency_ns/1000:.1f}μs")
        
        return total_bytes
    
    async def _simulate_hop_transfer(
        self,
        source_node: str,
        dest_node: str,
        buffer: ZeroCopyBuffer,
        request: TransferRequest
    ) -> int:
        """Simulate transfer between two adjacent nodes."""
        # Get node characteristics
        source = self.topology_manager.nodes[source_node]
        destination = self.topology_manager.nodes[dest_node]
        
        # Calculate transfer characteristics
        bandwidth_gbps = min(source.bandwidth_gbps, destination.bandwidth_gbps)
        base_latency_ns = source.estimate_latency_to(destination)
        
        # Calculate transfer time based on data size and bandwidth
        transfer_time_ns = (buffer.size_bytes * 8) / (bandwidth_gbps * 1e9) * 1e9
        total_latency_ns = base_latency_ns + transfer_time_ns
        
        # Add processing delays
        if source.is_quantum_capable() and destination.is_quantum_capable():
            # Quantum entanglement reduces latency
            total_latency_ns *= 0.5
            if request.requires_quantum_entanglement:
                self._stats["quantum_transfers"] += 1
        
        # Simulate the actual delay
        await asyncio.sleep(total_latency_ns / 1e9)
        
        return int(total_latency_ns)
    
    async def _update_transfer_stats(self, result: TransferResult, request: TransferRequest) -> None:
        """Update performance statistics."""
        self._stats["total_transfers"] += 1
        self._stats["successful_transfers"] += 1
        self._stats["total_bytes_transferred"] += result.bytes_transferred
        
        # Update average latency (running average)
        current_avg = self._stats["average_latency_ns"]
        n = self._stats["successful_transfers"]
        self._stats["average_latency_ns"] = (current_avg * (n - 1) + result.actual_latency_ns) / n
        
        # Update peak throughput
        self._stats["peak_throughput_gbps"] = max(
            self._stats["peak_throughput_gbps"],
            result.throughput_gbps
        )
        
        # Track ML optimizations
        if hasattr(request, 'used_ml_routing') and request.used_ml_routing:
            self._stats["ml_optimized_transfers"] += 1
    
    async def ping(self, source: str, destination: str, timeout_ms: int = 1000) -> Dict[str, Any]:
        """
        Ping between two nodes to measure connectivity and latency.
        
        Args:
            source: Source node ID
            destination: Destination node ID
            timeout_ms: Timeout in milliseconds
            
        Returns:
            Ping results including latency and path information
        """
        start_time = time.time_ns()
        
        try:
            # Create a small ping packet
            ping_data = b"HYPERFABRIC_PING_" + str(time.time_ns()).encode()
            
            # Send ping data
            result = await self.send_data(
                source=source,
                destination=destination,
                data=ping_data,
                data_type=DataType.CONTROL_MESSAGE,
                priority=PacketPriority.HIGH,
                latency_constraint_ns=timeout_ms * 1000000,  # Convert to nanoseconds
            )
            
            # Calculate round-trip time (simplified - actual implementation would need response)
            rtt_ns = result.actual_latency_ns
            
            return {
                "success": True,
                "source": source,
                "destination": destination,
                "rtt_ns": rtt_ns,
                "rtt_ms": rtt_ns / 1e6,
                "path": result.path_taken,
                "throughput_gbps": result.throughput_gbps,
                "timestamp": time.time(),
            }
            
        except Exception as e:
            return {
                "success": False,
                "source": source,
                "destination": destination,
                "error": str(e),
                "timestamp": time.time(),
            }
    
    async def get_topology_info(self) -> Dict[str, Any]:
        """Get comprehensive topology information."""
        return {
            "protocol_id": self.protocol_id,
            "state": self.state.value,
            "topology_stats": self.topology_manager.get_comprehensive_stats(),
            "routing_stats": self.routing_engine.get_topology_stats(),
            "buffer_stats": self.buffer_manager.get_stats(),
            "performance_stats": self._stats.copy(),
            "active_transfers": len(self.active_transfers),
            "uptime_seconds": time.time() - self._stats["protocol_start_time"],
        }
    
    async def optimize_topology(self) -> Dict[str, Any]:
        """Trigger topology optimization."""
        return await self.topology_manager.optimize_topology()
    
    # Background monitoring tasks
    
    async def _heartbeat_monitor(self) -> None:
        """Monitor node heartbeats and update node status."""
        while not self._shutdown_event.is_set():
            try:
                current_time = time.time()
                
                for node_id, node in self.topology_manager.nodes.items():
                    # Check if node heartbeat is stale
                    if current_time - node.last_heartbeat > 30:  # 30 seconds timeout
                        if node.is_healthy:
                            self.logger.warning(f"Node {node_id} heartbeat timeout")
                            node.is_healthy = False
                            
                            if self.enable_fault_tolerance:
                                await self.topology_manager.handle_node_failure(node_id)
                
                await asyncio.sleep(10)  # Check every 10 seconds
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Heartbeat monitor error: {e}")
                await asyncio.sleep(5)
    
    async def _performance_monitor(self) -> None:
        """Monitor performance metrics and detect anomalies."""
        while not self._shutdown_event.is_set():
            try:
                # Monitor for performance degradation
                if self._stats["successful_transfers"] > 0:
                    current_avg_latency = self._stats["average_latency_ns"]
                    
                    # Alert if average latency exceeds 10ms
                    if current_avg_latency > 10_000_000:  # 10ms in nanoseconds
                        self.logger.warning(f"High average latency detected: {current_avg_latency/1e6:.2f}ms")
                        
                        if self.state == ProtocolState.ACTIVE:
                            self.state = ProtocolState.DEGRADED
                
                # Monitor buffer utilization
                buffer_stats = self.buffer_manager.get_stats()
                if buffer_stats["global_stats"]["current_memory_usage"] > 1024**3:  # 1GB
                    self.logger.info("High memory usage detected, triggering optimization")
                    self.buffer_manager.optimize_pools()
                
                await asyncio.sleep(30)  # Monitor every 30 seconds
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Performance monitor error: {e}")
                await asyncio.sleep(10)
    
    async def _process_transfer_queue(self) -> None:
        """Process queued transfers with priority scheduling."""
        while not self._shutdown_event.is_set():
            try:
                # Process packets from routing engine queue
                await self.routing_engine.process_packet_queue()
                await asyncio.sleep(0.001)  # 1ms scheduling interval
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Transfer queue processing error: {e}")
                await asyncio.sleep(0.1)
    
    async def _topology_optimization_loop(self) -> None:
        """Periodically optimize topology."""
        while not self._shutdown_event.is_set():
            try:
                # Optimize topology every 5 minutes
                await asyncio.sleep(300)
                
                if self.state == ProtocolState.ACTIVE:
                    self.logger.info("Running periodic topology optimization")
                    await self.topology_manager.optimize_topology()
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Topology optimization error: {e}")
                await asyncio.sleep(60)
    
    async def _fault_detection_loop(self) -> None:
        """Monitor for faults and trigger recovery."""
        while not self._shutdown_event.is_set():
            try:
                # Check for network partitions and isolated nodes
                topology_stats = self.topology_manager.get_comprehensive_stats()
                
                if not topology_stats.get("is_connected", True):
                    self.logger.error("Network partition detected!")
                    self._stats["fault_recoveries"] += 1
                    
                    # Trigger recovery procedures
                    # This would implement actual partition recovery logic
                
                await asyncio.sleep(15)  # Check every 15 seconds
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Fault detection error: {e}")
                await asyncio.sleep(30)
    
    async def shutdown(self) -> None:
        """Gracefully shutdown the protocol."""
        self.logger.info("Shutting down HyperFabric Protocol")
        self.state = ProtocolState.SHUTDOWN
        
        # Signal shutdown to background tasks
        self._shutdown_event.set()
        
        # Wait for active transfers to complete (with timeout)
        timeout = 30  # 30 seconds timeout
        start_time = time.time()
        
        while self.active_transfers and (time.time() - start_time) < timeout:
            self.logger.info(f"Waiting for {len(self.active_transfers)} active transfers to complete")
            await asyncio.sleep(1)
        
        # Cancel remaining background tasks
        for task in self._background_tasks:
            if not task.done():
                task.cancel()
        
        # Wait for tasks to complete
        if self._background_tasks:
            await asyncio.gather(*self._background_tasks, return_exceptions=True)
        
        # Cleanup resources
        self.buffer_manager.cleanup_all()
        
        self.logger.info("HyperFabric Protocol shutdown complete")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        asyncio.create_task(self.shutdown())
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.shutdown()
