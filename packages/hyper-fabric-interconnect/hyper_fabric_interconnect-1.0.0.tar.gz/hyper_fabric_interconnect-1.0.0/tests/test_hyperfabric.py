"""
Unit tests for HyperFabric Interconnect core functionality.
"""

import pytest
import asyncio
import time
from unittest.mock import Mock, patch

from hyperfabric import (
    HyperFabricProtocol,
    NodeSignature,
    HardwareType,
    FabricZone,
    ZoneType,
    IsolationLevel,
    PacketPriority,
    DataType,
    ZeroCopyBuffer,
    BufferManager,
    RoutingEngine,
    RoutingStrategy,
    TopologyManager,
)
from hyperfabric.exceptions import (
    HyperFabricError,
    NodeNotFoundError,
    RoutingError,
    BufferError,
    TopologyError,
)


class TestNodeSignature:
    """Test NodeSignature functionality."""
    
    def test_node_creation(self):
        """Test basic node creation."""
        node = NodeSignature(
            node_id="test-node-01",
            hardware_type=HardwareType.NVIDIA_H100,
            bandwidth_gbps=400,
            latency_ns=100,
        )
        
        assert node.node_id == "test-node-01"
        assert node.hardware_type == HardwareType.NVIDIA_H100
        assert node.bandwidth_gbps == 400
        assert node.latency_ns == 100
        assert node.is_active is True
        assert node.is_healthy is True
        assert node.memory_gb == 80.0  # Default for H100
    
    def test_node_validation(self):
        """Test node validation."""
        with pytest.raises(ValueError):
            NodeSignature(
                node_id="invalid",
                hardware_type=HardwareType.NVIDIA_H100,
                bandwidth_gbps=-1,  # Invalid
                latency_ns=100,
            )
    
    def test_quantum_capabilities(self):
        """Test quantum capability detection."""
        quantum_node = NodeSignature(
            node_id="qpu-01",
            hardware_type=HardwareType.QUANTUM_QPU,
            bandwidth_gbps=10,
            latency_ns=50,
            quantum_coherence_time_us=100.0,
        )
        
        regular_node = NodeSignature(
            node_id="gpu-01",
            hardware_type=HardwareType.NVIDIA_H100,
            bandwidth_gbps=400,
            latency_ns=100,
        )
        
        assert quantum_node.is_quantum_capable() is True
        assert regular_node.is_quantum_capable() is False
    
    def test_photonic_capabilities(self):
        """Test photonic capability detection."""
        photonic_node = NodeSignature(
            node_id="photonic-01",
            hardware_type=HardwareType.PHOTONIC_SWITCH,
            bandwidth_gbps=1000,
            latency_ns=10,
            photonic_channels=64,
        )
        
        assert photonic_node.is_photonic_capable() is True
    
    def test_neuromorphic_capabilities(self):
        """Test neuromorphic capability detection."""
        neuro_node = NodeSignature(
            node_id="neuro-01",
            hardware_type=HardwareType.NEUROMORPHIC_CHIP,
            bandwidth_gbps=50,
            latency_ns=200,
            neuromorphic_neurons=1000000,
        )
        
        assert neuro_node.is_neuromorphic_capable() is True
    
    def test_latency_estimation(self):
        """Test latency estimation between nodes."""
        node1 = NodeSignature(
            node_id="node1",
            hardware_type=HardwareType.NVIDIA_H100,
            bandwidth_gbps=400,
            latency_ns=100,
        )
        
        node2 = NodeSignature(
            node_id="node2",
            hardware_type=HardwareType.NVIDIA_A100,
            bandwidth_gbps=300,
            latency_ns=150,
        )
        
        estimated_latency = node1.estimate_latency_to(node2)
        assert estimated_latency > 0
        assert estimated_latency >= max(node1.latency_ns, node2.latency_ns)
    
    def test_throughput_calculation(self):
        """Test theoretical throughput calculation."""
        node = NodeSignature(
            node_id="test-node",
            hardware_type=HardwareType.NVIDIA_H100,
            bandwidth_gbps=400,
            latency_ns=100,
        )
        
        base_throughput = node.get_theoretical_throughput_gbps()
        assert base_throughput == 400.0
        
        # Test with load
        node.update_load(50.0)
        loaded_throughput = node.get_theoretical_throughput_gbps()
        assert loaded_throughput == 200.0  # 50% load reduction
    
    def test_serialization(self):
        """Test node serialization and deserialization."""
        node = NodeSignature(
            node_id="test-node",
            hardware_type=HardwareType.NVIDIA_H100,
            bandwidth_gbps=400,
            latency_ns=100,
        )
        
        # Test to_dict
        node_dict = node.to_dict()
        assert node_dict['node_id'] == "test-node"
        assert node_dict['hardware_type'] == "nvidia-h100"
        
        # Test from_dict
        restored_node = NodeSignature.from_dict(node_dict)
        assert restored_node.node_id == node.node_id
        assert restored_node.hardware_type == node.hardware_type


class TestZeroCopyBuffer:
    """Test ZeroCopyBuffer functionality."""
    
    def test_buffer_creation(self):
        """Test buffer creation."""
        buffer = ZeroCopyBuffer(1024)
        assert buffer.size_bytes == 1024
        assert buffer.buffer_id is not None
    
    def test_buffer_write_read(self):
        """Test buffer write and read operations."""
        buffer = ZeroCopyBuffer(1024)
        test_data = b"Hello, HyperFabric!"
        
        # Write data
        bytes_written = buffer.write(test_data)
        assert bytes_written == len(test_data)
        
        # Read data
        read_data = buffer.read(len(test_data))
        assert bytes(read_data) == test_data
    
    def test_buffer_overflow(self):
        """Test buffer overflow protection."""
        buffer = ZeroCopyBuffer(10)
        large_data = b"This data is too large for the buffer"
        
        with pytest.raises(BufferError):
            buffer.write(large_data)
    
    def test_buffer_copy(self):
        """Test zero-copy buffer copying."""
        source_buffer = ZeroCopyBuffer(1024)
        dest_buffer = ZeroCopyBuffer(1024)
        
        test_data = b"Copy test data"
        source_buffer.write(test_data)
        
        bytes_copied = source_buffer.copy_to(dest_buffer)
        assert bytes_copied == len(test_data)
        
        read_data = dest_buffer.read(len(test_data))
        assert bytes(read_data) == test_data
    
    def test_buffer_view(self):
        """Test memory view functionality."""
        buffer = ZeroCopyBuffer(1024)
        test_data = b"View test data"
        buffer.write(test_data)
        
        view = buffer.get_view(0, len(test_data))
        assert bytes(view) == test_data
    
    def test_buffer_compression(self):
        """Test buffer compression simulation."""
        buffer = ZeroCopyBuffer(1024)
        test_data = b"A" * 100  # Repetitive data for better compression
        buffer.write(test_data)
        
        compression_ratio = buffer.compress()
        assert compression_ratio > 1.0  # Should achieve some compression


class TestBufferManager:
    """Test BufferManager functionality."""
    
    def test_buffer_allocation(self):
        """Test buffer allocation."""
        manager = BufferManager()
        buffer = manager.allocate_buffer(1024)
        
        assert buffer.size_bytes == 1024
        assert buffer is not None
    
    def test_buffer_deallocation(self):
        """Test buffer deallocation."""
        manager = BufferManager()
        buffer = manager.allocate_buffer(1024)
        
        # Should not raise an exception
        manager.deallocate_buffer(buffer)
    
    def test_buffer_pool_usage(self):
        """Test buffer pool functionality."""
        manager = BufferManager()
        
        # Allocate multiple buffers of the same size
        buffers = []
        for _ in range(5):
            buffer = manager.allocate_buffer(1024 * 1024)  # 1MB
            buffers.append(buffer)
        
        # Deallocate them
        for buffer in buffers:
            manager.deallocate_buffer(buffer)
        
        # Allocate again - should reuse from pool
        new_buffer = manager.allocate_buffer(1024 * 1024)
        assert new_buffer is not None
    
    @pytest.mark.asyncio
    async def test_async_transfer(self):
        """Test asynchronous buffer transfer."""
        manager = BufferManager()
        source = manager.allocate_buffer(1024)
        dest = manager.allocate_buffer(1024)
        
        test_data = b"Async transfer test"
        source.write(test_data)
        
        bytes_transferred = await manager.transfer_data(source, dest, len(test_data))
        assert bytes_transferred == len(test_data)
        
        read_data = dest.read(len(test_data))
        assert bytes(read_data) == test_data


class TestFabricZone:
    """Test FabricZone functionality."""
    
    def test_zone_creation(self):
        """Test zone creation."""
        zone = FabricZone(
            zone_id="test-zone",
            zone_type=ZoneType.COMPUTE_CLUSTER,
            isolation_level=IsolationLevel.MEDIUM,
            max_nodes=100,
        )
        
        assert zone.zone_id == "test-zone"
        assert zone.zone_type == ZoneType.COMPUTE_CLUSTER
        assert zone.max_nodes == 100
        assert zone.is_active is True
    
    def test_zone_node_management(self):
        """Test adding and removing nodes from zones."""
        zone = FabricZone(
            zone_id="test-zone",
            zone_type=ZoneType.COMPUTE_CLUSTER,
            isolation_level=IsolationLevel.MEDIUM,
            max_nodes=2,
        )
        
        # Add nodes
        assert zone.add_node("node1") is True
        assert zone.add_node("node2") is True
        assert zone.add_node("node3") is False  # Should fail - at capacity
        
        assert zone.get_node_count() == 2
        assert zone.is_full() is True
        
        # Remove node
        assert zone.remove_node("node1") is True
        assert zone.get_node_count() == 1
        assert zone.is_full() is False
    
    def test_zone_serialization(self):
        """Test zone serialization."""
        zone = FabricZone(
            zone_id="test-zone",
            zone_type=ZoneType.COMPUTE_CLUSTER,
            isolation_level=IsolationLevel.MEDIUM,
        )
        zone.add_node("node1")
        
        # Test to_dict
        zone_dict = zone.to_dict()
        assert zone_dict['zone_id'] == "test-zone"
        assert zone_dict['zone_type'] == "compute_cluster"
        
        # Test from_dict
        restored_zone = FabricZone.from_dict(zone_dict)
        assert restored_zone.zone_id == zone.zone_id
        assert restored_zone.zone_type == zone.zone_type
        assert restored_zone.has_node("node1")


class TestTopologyManager:
    """Test TopologyManager functionality."""
    
    def test_node_registration(self):
        """Test node registration."""
        manager = TopologyManager()
        node = NodeSignature(
            node_id="test-node",
            hardware_type=HardwareType.NVIDIA_H100,
            bandwidth_gbps=400,
            latency_ns=100,
        )
        
        manager.register_node(node)
        assert "test-node" in manager.nodes
        assert manager.nodes["test-node"] == node
    
    def test_node_unregistration(self):
        """Test node unregistration."""
        manager = TopologyManager()
        node = NodeSignature(
            node_id="test-node",
            hardware_type=HardwareType.NVIDIA_H100,
            bandwidth_gbps=400,
            latency_ns=100,
        )
        
        manager.register_node(node)
        manager.unregister_node("test-node")
        assert "test-node" not in manager.nodes
    
    def test_zone_management(self):
        """Test zone creation and management."""
        manager = TopologyManager()
        zone = FabricZone(
            zone_id="test-zone",
            zone_type=ZoneType.COMPUTE_CLUSTER,
            isolation_level=IsolationLevel.MEDIUM,
        )
        
        manager.create_zone(zone)
        assert "test-zone" in manager.zones
        
        # Test adding node to zone
        node = NodeSignature(
            node_id="test-node",
            hardware_type=HardwareType.NVIDIA_H100,
            bandwidth_gbps=400,
            latency_ns=100,
        )
        manager.register_node(node)
        
        success = manager.add_node_to_zone("test-node", "test-zone")
        assert success is True
        assert manager.zones["test-zone"].has_node("test-node")
    
    def test_connection_management(self):
        """Test connection management."""
        manager = TopologyManager()
        
        # Create and register nodes
        node1 = NodeSignature("node1", HardwareType.NVIDIA_H100, 400, 100)
        node2 = NodeSignature("node2", HardwareType.NVIDIA_A100, 300, 150)
        
        manager.register_node(node1)
        manager.register_node(node2)
        
        # Add connection
        manager.add_connection("node1", "node2")
        assert manager.graph.has_edge("node1", "node2")
        
        # Remove connection
        manager.remove_connection("node1", "node2")
        assert not manager.graph.has_edge("node1", "node2")
    
    def test_shortest_path(self):
        """Test shortest path calculation."""
        manager = TopologyManager()
        
        # Create a simple topology
        nodes = [
            NodeSignature("node1", HardwareType.NVIDIA_H100, 400, 100),
            NodeSignature("node2", HardwareType.NVIDIA_A100, 300, 150),
            NodeSignature("node3", HardwareType.NVIDIA_V100, 200, 200),
        ]
        
        for node in nodes:
            manager.register_node(node)
        
        # Create connections: node1 -> node2 -> node3
        manager.add_connection("node1", "node2")
        manager.add_connection("node2", "node3")
        
        path = manager.find_shortest_path("node1", "node3")
        assert path == ["node1", "node2", "node3"]
    
    @pytest.mark.asyncio
    async def test_topology_optimization(self):
        """Test topology optimization."""
        manager = TopologyManager()
        
        # Create nodes
        for i in range(5):
            node = NodeSignature(
                f"node{i}",
                HardwareType.NVIDIA_H100,
                400,
                100,
            )
            manager.register_node(node)
        
        # Run optimization
        result = await manager.optimize_topology()
        assert "optimizations_applied" in result
        assert "recommendations" in result
        assert "metrics_before" in result
        assert "metrics_after" in result
    
    @pytest.mark.asyncio
    async def test_node_failure_handling(self):
        """Test node failure handling."""
        manager = TopologyManager()
        
        node = NodeSignature("test-node", HardwareType.NVIDIA_H100, 400, 100)
        manager.register_node(node)
        
        # Simulate node failure
        recovery_result = await manager.handle_node_failure("test-node")
        assert recovery_result["failed_node"] == "test-node"
        assert not manager.nodes["test-node"].is_healthy
        assert not manager.nodes["test-node"].is_active
    
    def test_topology_export_import(self):
        """Test topology export and import."""
        manager = TopologyManager()
        
        # Create a simple topology
        node = NodeSignature("test-node", HardwareType.NVIDIA_H100, 400, 100)
        manager.register_node(node)
        
        # Export
        exported_data = manager.export_topology("json")
        assert exported_data is not None
        assert "nodes" in exported_data
        
        # Clear and import
        manager.nodes.clear()
        manager.import_topology(exported_data, "json")
        assert "test-node" in manager.nodes


class TestRoutingEngine:
    """Test RoutingEngine functionality."""
    
    def test_node_registration(self):
        """Test node registration in routing engine."""
        engine = RoutingEngine()
        node = NodeSignature("test-node", HardwareType.NVIDIA_H100, 400, 100)
        
        engine.register_node(node)
        assert "test-node" in engine.topology.nodes
    
    @pytest.mark.asyncio
    async def test_packet_routing(self):
        """Test packet routing."""
        engine = RoutingEngine()
        
        # Create nodes
        node1 = NodeSignature("node1", HardwareType.NVIDIA_H100, 400, 100)
        node2 = NodeSignature("node2", HardwareType.NVIDIA_A100, 300, 150)
        
        engine.register_node(node1)
        engine.register_node(node2)
        
        # Create packet
        from hyperfabric.routing import Packet
        packet = Packet(
            packet_id="test-packet",
            source="node1",
            destination="node2",
            data_size_bytes=1024,
        )
        
        # Route packet
        path = await engine.route_packet(packet)
        assert len(path) >= 2
        assert path[0] == "node1"
        assert path[-1] == "node2"
    
    def test_routing_strategies(self):
        """Test different routing strategies."""
        engine = RoutingEngine()
        
        # Create nodes
        nodes = [
            NodeSignature("node1", HardwareType.NVIDIA_H100, 400, 100),
            NodeSignature("node2", HardwareType.NVIDIA_A100, 300, 150),
            NodeSignature("node3", HardwareType.PHOTONIC_SWITCH, 1000, 10),
        ]
        
        for node in nodes:
            engine.register_node(node)
        
        # Test shortest path
        path = engine._dijkstra_shortest_path("node1", "node3")
        assert path is not None
        
        # Test lowest latency path
        path = engine._lowest_latency_path("node1", "node3")
        assert path is not None
        
        # Test highest bandwidth path
        path = engine._highest_bandwidth_path("node1", "node3")
        assert path is not None


@pytest.mark.asyncio
class TestHyperFabricProtocol:
    """Test HyperFabricProtocol functionality."""
    
    async def test_protocol_initialization(self):
        """Test protocol initialization."""
        protocol = HyperFabricProtocol()
        
        # Wait for initialization
        await asyncio.sleep(0.1)
        
        assert protocol.protocol_id is not None
        assert protocol.topology_manager is not None
        assert protocol.routing_engine is not None
        assert protocol.buffer_manager is not None
        
        await protocol.shutdown()
    
    async def test_node_registration(self):
        """Test node registration through protocol."""
        protocol = HyperFabricProtocol()
        await asyncio.sleep(0.1)  # Wait for initialization
        
        node = NodeSignature("test-node", HardwareType.NVIDIA_H100, 400, 100)
        protocol.register_node(node)
        
        registered_nodes = protocol.get_registered_nodes()
        assert "test-node" in registered_nodes
        
        await protocol.shutdown()
    
    async def test_data_transfer(self):
        """Test data transfer functionality."""
        protocol = HyperFabricProtocol()
        await asyncio.sleep(0.1)  # Wait for initialization
        
        # Create nodes
        node1 = NodeSignature("source", HardwareType.NVIDIA_H100, 400, 100)
        node2 = NodeSignature("dest", HardwareType.NVIDIA_A100, 300, 150)
        
        protocol.register_node(node1)
        protocol.register_node(node2)
        
        # Wait for auto-discovery
        await asyncio.sleep(0.1)
        
        # Test data transfer
        test_data = b"Hello, HyperFabric!"
        
        result = await protocol.send_data(
            source="source",
            destination="dest",
            data=test_data,
            data_type=DataType.TENSOR,
            priority=PacketPriority.HIGH,
        )
        
        assert result.success is True
        assert result.bytes_transferred == len(test_data)
        assert result.actual_latency_ns > 0
        assert len(result.path_taken) >= 2
        
        await protocol.shutdown()
    
    async def test_ping_functionality(self):
        """Test ping functionality."""
        protocol = HyperFabricProtocol()
        await asyncio.sleep(0.1)  # Wait for initialization
        
        # Create nodes
        node1 = NodeSignature("source", HardwareType.NVIDIA_H100, 400, 100)
        node2 = NodeSignature("dest", HardwareType.NVIDIA_A100, 300, 150)
        
        protocol.register_node(node1)
        protocol.register_node(node2)
        
        # Wait for auto-discovery
        await asyncio.sleep(0.1)
        
        # Test ping
        ping_result = await protocol.ping("source", "dest")
        
        assert ping_result["success"] is True
        assert ping_result["source"] == "source"
        assert ping_result["destination"] == "dest"
        assert ping_result["rtt_ns"] > 0
        
        await protocol.shutdown()
    
    async def test_zone_creation(self):
        """Test zone creation through protocol."""
        protocol = HyperFabricProtocol()
        await asyncio.sleep(0.1)  # Wait for initialization
        
        zone = FabricZone(
            zone_id="test-zone",
            zone_type=ZoneType.COMPUTE_CLUSTER,
            isolation_level=IsolationLevel.MEDIUM,
        )
        
        protocol.create_zone(zone)
        assert "test-zone" in protocol.topology_manager.zones
        
        await protocol.shutdown()
    
    async def test_topology_info(self):
        """Test topology information retrieval."""
        protocol = HyperFabricProtocol()
        await asyncio.sleep(0.1)  # Wait for initialization
        
        # Add a node
        node = NodeSignature("test-node", HardwareType.NVIDIA_H100, 400, 100)
        protocol.register_node(node)
        
        # Get topology info
        topo_info = await protocol.get_topology_info()
        
        assert "protocol_id" in topo_info
        assert "state" in topo_info
        assert "topology_stats" in topo_info
        assert "performance_stats" in topo_info
        
        await protocol.shutdown()
    
    async def test_error_handling(self):
        """Test error handling in protocol operations."""
        protocol = HyperFabricProtocol()
        await asyncio.sleep(0.1)  # Wait for initialization
        
        # Test transfer to non-existent node
        with pytest.raises(HyperFabricError):
            await protocol.send_data(
                source="non-existent",
                destination="also-non-existent",
                data=b"test",
            )
        
        await protocol.shutdown()


class TestIntegration:
    """Integration tests for the complete system."""
    
    @pytest.mark.asyncio
    async def test_full_workflow(self):
        """Test a complete workflow from setup to data transfer."""
        protocol = HyperFabricProtocol()
        await asyncio.sleep(0.1)  # Wait for initialization
        
        try:
            # 1. Create diverse nodes
            nodes = [
                NodeSignature("gpu-01", HardwareType.NVIDIA_H100, 400, 100),
                NodeSignature("gpu-02", HardwareType.NVIDIA_A100, 300, 150),
                NodeSignature("qpu-01", HardwareType.QUANTUM_QPU, 10, 50, quantum_coherence_time_us=100),
                NodeSignature("photonic-01", HardwareType.PHOTONIC_SWITCH, 1000, 10, photonic_channels=64),
            ]
            
            # 2. Register nodes
            for node in nodes:
                protocol.register_node(node)
            
            # 3. Create custom zone
            custom_zone = FabricZone(
                zone_id="ai-cluster",
                zone_type=ZoneType.COMPUTE_CLUSTER,
                isolation_level=IsolationLevel.MEDIUM,
                max_nodes=10,
            )
            protocol.create_zone(custom_zone)
            
            # 4. Wait for auto-discovery
            await asyncio.sleep(0.2)
            
            # 5. Test various transfers
            test_cases = [
                ("gpu-01", "gpu-02", DataType.TENSOR, PacketPriority.HIGH),
                ("gpu-01", "qpu-01", DataType.QUANTUM_STATE, PacketPriority.ULTRA_HIGH),
                ("photonic-01", "gpu-01", DataType.PARAMETER, PacketPriority.NORMAL),
            ]
            
            for source, dest, data_type, priority in test_cases:
                test_data = b"Integration test data" + str(time.time()).encode()
                
                result = await protocol.send_data(
                    source=source,
                    destination=dest,
                    data=test_data,
                    data_type=data_type,
                    priority=priority,
                )
                
                assert result.success is True
                assert result.bytes_transferred == len(test_data)
            
            # 6. Test ping between all pairs
            for i, source_node in enumerate(nodes):
                for j, dest_node in enumerate(nodes):
                    if i != j:
                        ping_result = await protocol.ping(source_node.node_id, dest_node.node_id)
                        assert ping_result["success"] is True
            
            # 7. Get comprehensive stats
            topo_info = await protocol.get_topology_info()
            assert topo_info["performance_stats"]["total_transfers"] > 0
            assert topo_info["performance_stats"]["successful_transfers"] > 0
            
            # 8. Test topology optimization
            optimization_result = await protocol.optimize_topology()
            assert "optimizations_applied" in optimization_result
            
        finally:
            await protocol.shutdown()
    
    @pytest.mark.asyncio
    async def test_fault_tolerance(self):
        """Test fault tolerance and recovery mechanisms."""
        protocol = HyperFabricProtocol(enable_fault_tolerance=True)
        await asyncio.sleep(0.1)  # Wait for initialization
        
        try:
            # Create nodes
            nodes = [
                NodeSignature("primary", HardwareType.NVIDIA_H100, 400, 100),
                NodeSignature("backup", HardwareType.NVIDIA_A100, 300, 150),
                NodeSignature("target", HardwareType.NVIDIA_V100, 200, 200),
            ]
            
            for node in nodes:
                protocol.register_node(node)
            
            await asyncio.sleep(0.1)
            
            # Simulate node failure
            recovery_result = await protocol.topology_manager.handle_node_failure("primary")
            assert recovery_result["failed_node"] == "primary"
            
            # Test that communication still works through backup paths
            test_data = b"Fault tolerance test"
            result = await protocol.send_data(
                source="backup",
                destination="target",
                data=test_data,
            )
            
            assert result.success is True
            
            # Test node recovery
            await protocol.topology_manager.recover_node("primary")
            assert protocol.topology_manager.nodes["primary"].is_healthy is True
            
        finally:
            await protocol.shutdown()
    
    @pytest.mark.asyncio
    async def test_performance_characteristics(self):
        """Test performance characteristics and benchmarks."""
        protocol = HyperFabricProtocol()
        await asyncio.sleep(0.1)  # Wait for initialization
        
        try:
            # Create high-performance nodes
            source = NodeSignature("hpc-source", HardwareType.NVIDIA_H100, 400, 100)
            dest = NodeSignature("hpc-dest", HardwareType.NVIDIA_H100, 400, 100)
            
            protocol.register_node(source)
            protocol.register_node(dest)
            
            await asyncio.sleep(0.1)
            
            # Test various data sizes
            data_sizes = [1024, 64*1024, 1024*1024, 16*1024*1024]  # 1KB to 16MB
            
            for size in data_sizes:
                test_data = b"X" * size
                start_time = time.time()
                
                result = await protocol.send_data(
                    source="hpc-source",
                    destination="hpc-dest",
                    data=test_data,
                    priority=PacketPriority.ULTRA_HIGH,
                )
                
                end_time = time.time()
                
                assert result.success is True
                assert result.bytes_transferred == size
                
                # Check performance metrics
                throughput_mbps = (size * 8) / (result.actual_latency_ns / 1e9) / 1e6
                print(f"Size: {size:,} bytes, Latency: {result.actual_latency_ns/1e6:.2f}ms, Throughput: {throughput_mbps:.1f} Mbps")
                
                # For larger transfers, expect higher throughput
                if size >= 1024*1024:  # 1MB+
                    assert throughput_mbps > 100  # Should achieve > 100 Mbps
        
        finally:
            await protocol.shutdown()


if __name__ == "__main__":
    # Run with: python -m pytest tests/test_hyperfabric.py -v
    pytest.main([__file__, "-v"])
