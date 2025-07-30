# 💡 Usage Examples

Practical examples demonstrating HyperFabric Interconnect capabilities for real-world scenarios.

## Quick Start Examples

### Basic Setup

Set up a simple fabric with a few nodes:

```python
import asyncio
from hyperfabric import HyperFabricProtocol, NodeSignature, HardwareType

async def basic_fabric_setup():
    # Initialize protocol
    protocol = HyperFabricProtocol()
    
    # Register some nodes
    nodes = [
        NodeSignature("gpu-01", HardwareType.NVIDIA_H100, 400, 100),
        NodeSignature("gpu-02", HardwareType.NVIDIA_A100, 300, 150),
        NodeSignature("storage-01", HardwareType.STORAGE_ARRAY, 100, 500)
    ]
    
    for node in nodes:
        await protocol.register_node(node)
    
    # Test connectivity
    result = await protocol.ping("gpu-01", "storage-01")
    print(f"Ping latency: {result.latency_ms:.2f}ms")
    
    return protocol

# Run the setup
protocol = asyncio.run(basic_fabric_setup())
```

### Simple Data Transfer

Transfer data between nodes:

```python
async def simple_transfer_example():
    protocol = HyperFabricProtocol()
    
    # Register nodes
    await protocol.register_node(
        NodeSignature("source", HardwareType.CPU_SERVER, 10, 1000)
    )
    await protocol.register_node(
        NodeSignature("destination", HardwareType.STORAGE_ARRAY, 25, 2000)
    )
    
    # Prepare some data
    data_payload = b"Hello, HyperFabric!" * 1000  # 19KB
    
    # Transfer data
    result = await protocol.send_data(
        source="source",
        destination="destination",
        data=data_payload,
        compression_enabled=True
    )
    
    print(f"Transfer completed: {len(result)} bytes received")
    return result

asyncio.run(simple_transfer_example())
```

## AI/ML Examples

### Distributed Training Setup

Set up a distributed training environment:

```python
import asyncio
import numpy as np
from hyperfabric import (
    HyperFabricProtocol, NodeSignature, HardwareType, 
    DataType, PacketPriority, FabricZone, ZoneType, IsolationLevel
)

class DistributedTrainingCluster:
    def __init__(self, num_gpus=8):
        self.protocol = HyperFabricProtocol(enable_ml_routing=True)
        self.num_gpus = num_gpus
        self.parameter_server = None
        
    async def setup_cluster(self):
        """Set up the distributed training cluster."""
        
        # Create parameter server
        self.parameter_server = NodeSignature(
            node_id="param-server-01",
            hardware_type=HardwareType.CPU_SERVER,
            bandwidth_gbps=200,
            latency_ns=500,
            memory_gb=256,
            rack_position="rack-01-slot-01"
        )
        await self.protocol.register_node(self.parameter_server)
        
        # Create GPU workers
        gpu_nodes = []
        for i in range(self.num_gpus):
            gpu_node = NodeSignature(
                node_id=f"gpu-worker-{i:02d}",
                hardware_type=HardwareType.NVIDIA_H100,
                bandwidth_gbps=400,
                latency_ns=100,
                memory_gb=80,
                compute_units=16896,  # CUDA cores
                rack_position=f"rack-{i//4+1:02d}-slot-{i%4+1:02d}"
            )
            await self.protocol.register_node(gpu_node)
            gpu_nodes.append(gpu_node)
        
        # Create training zone
        training_zone = FabricZone(
            zone_id="distributed-training",
            zone_type=ZoneType.COMPUTE_CLUSTER,
            isolation_level=IsolationLevel.MEDIUM,
            max_nodes=self.num_gpus + 10,
            required_bandwidth_gbps=400.0,
            description="Distributed AI training cluster"
        )
        await self.protocol.create_zone(training_zone)
        
        print(f"✅ Cluster setup complete: {self.num_gpus} GPU workers + 1 parameter server")
        return gpu_nodes
    
    async def simulate_training_step(self, gpu_nodes, step=0):
        """Simulate one training step with gradient synchronization."""
        
        print(f"🔄 Training step {step + 1}")
        
        # Simulate forward pass (compute gradients on each GPU)
        gradients = {}
        for gpu_node in gpu_nodes:
            # Generate fake gradients (in practice, these come from actual training)
            gradient_data = np.random.randn(1000, 1000).astype(np.float32)
            gradients[gpu_node.node_id] = gradient_data
        
        # All-reduce operation: send gradients to parameter server
        gradient_tasks = []
        for node_id, gradient in gradients.items():
            task = self.protocol.send_data(
                source=node_id,
                destination="param-server-01",
                data=gradient.tobytes(),
                data_type=DataType.GRADIENT,
                priority=PacketPriority.HIGH,
                compression_enabled=True,
                metadata={"step": step, "worker_id": node_id}
            )
            gradient_tasks.append(task)
        
        # Wait for all gradients to reach parameter server
        start_time = asyncio.get_event_loop().time()
        received_gradients = await asyncio.gather(*gradient_tasks)
        gradient_sync_time = asyncio.get_event_loop().time() - start_time
        
        # Simulate parameter update on server
        await asyncio.sleep(0.01)  # 10ms for parameter update
        
        # Broadcast updated parameters back to all workers
        updated_params = np.random.randn(1000, 1000).astype(np.float32)
        broadcast_tasks = []
        
        for gpu_node in gpu_nodes:
            task = self.protocol.send_data(
                source="param-server-01",
                destination=gpu_node.node_id,
                data=updated_params.tobytes(),
                data_type=DataType.PARAMETER,
                priority=PacketPriority.HIGH,
                compression_enabled=True
            )
            broadcast_tasks.append(task)
        
        # Wait for parameter broadcast
        await asyncio.gather(*broadcast_tasks)
        broadcast_time = asyncio.get_event_loop().time() - start_time - gradient_sync_time
        
        total_time = gradient_sync_time + broadcast_time
        print(f"   Gradient sync: {gradient_sync_time*1000:.1f}ms")
        print(f"   Param broadcast: {broadcast_time*1000:.1f}ms")
        print(f"   Total communication: {total_time*1000:.1f}ms")
        
        return total_time

async def run_distributed_training():
    """Run a complete distributed training simulation."""
    
    cluster = DistributedTrainingCluster(num_gpus=8)
    gpu_nodes = await cluster.setup_cluster()
    
    print("🚀 Starting distributed training simulation...")
    
    # Run training for several steps
    total_comm_time = 0
    num_steps = 10
    
    for step in range(num_steps):
        step_time = await cluster.simulate_training_step(gpu_nodes, step)
        total_comm_time += step_time
        
        # Brief pause between steps
        await asyncio.sleep(0.1)
    
    avg_comm_time = total_comm_time / num_steps
    print(f"\n📊 Training Summary:")
    print(f"   Steps completed: {num_steps}")
    print(f"   Average communication time: {avg_comm_time*1000:.1f}ms/step")
    print(f"   Estimated speedup vs Ethernet: {50/avg_comm_time:.1f}x")

# Run the distributed training example
asyncio.run(run_distributed_training())
```

### Real-Time Inference Pipeline

Create a real-time inference pipeline with edge computing:

```python
async def real_time_inference_pipeline():
    """Set up a real-time inference pipeline with edge nodes."""
    
    protocol = HyperFabricProtocol(
        enable_ml_routing=True,
        default_latency_constraint_ns=1_000_000  # 1ms max latency
    )
    
    # Central model server
    model_server = NodeSignature(
        node_id="model-server-central",
        hardware_type=HardwareType.NVIDIA_A100,
        bandwidth_gbps=400,
        latency_ns=200,
        memory_gb=40,
        physical_location="Data Center - Virginia"
    )
    await protocol.register_node(model_server)
    
    # Edge inference nodes
    edge_locations = [
        ("New York", 50),
        ("San Francisco", 75),
        ("Chicago", 45),
        ("Miami", 60)
    ]
    
    edge_nodes = []
    for city, latency_to_central in edge_locations:
        node = NodeSignature(
            node_id=f"edge-{city.lower().replace(' ', '-')}",
            hardware_type=HardwareType.NVIDIA_RTX4090,
            bandwidth_gbps=100,
            latency_ns=latency_to_central * 1000,  # Convert to ns
            memory_gb=24,
            physical_location=f"Edge - {city}"
        )
        await protocol.register_node(node)
        edge_nodes.append(node)
    
    print("🌐 Edge inference pipeline initialized")
    
    # Create inference zone
    inference_zone = FabricZone(
        zone_id="edge-inference",
        zone_type=ZoneType.INFERENCE_FARM,
        isolation_level=IsolationLevel.LOW,
        max_nodes=50,
        required_bandwidth_gbps=100.0,
        description="Real-time edge inference network"
    )
    await protocol.create_zone(inference_zone)
    
    # Simulate model deployment to edge nodes
    print("📦 Deploying models to edge nodes...")
    model_weights = np.random.randn(100, 100).astype(np.float32)  # Fake model
    
    deployment_tasks = []
    for edge_node in edge_nodes:
        task = protocol.send_data(
            source="model-server-central",
            destination=edge_node.node_id,
            data=model_weights.tobytes(),
            data_type=DataType.PARAMETER,
            priority=PacketPriority.HIGH,
            compression_enabled=True,
            latency_constraint_ns=10_000_000  # 10ms for model deployment
        )
        deployment_tasks.append(task)
    
    await asyncio.gather(*deployment_tasks)
    print("✅ Model deployment complete")
    
    # Simulate real-time inference requests
    print("⚡ Processing real-time inference requests...")
    
    for request_id in range(20):
        # Pick random edge node (simulating geographic routing)
        edge_node = np.random.choice(edge_nodes)
        
        # Generate fake input data
        input_data = np.random.randn(10, 100).astype(np.float32)
        
        # Send inference request
        start_time = asyncio.get_event_loop().time()
        
        result = await protocol.send_data(
            source="client",
            destination=edge_node.node_id,
            data=input_data.tobytes(),
            data_type=DataType.TENSOR,
            priority=PacketPriority.ULTRA_HIGH,
            latency_constraint_ns=1_000_000  # 1ms max
        )
        
        inference_time = (asyncio.get_event_loop().time() - start_time) * 1000
        
        print(f"   Request {request_id+1:2d}: {edge_node.node_id:20s} - {inference_time:.2f}ms")
        
        # Brief pause between requests
        await asyncio.sleep(0.05)

asyncio.run(real_time_inference_pipeline())
```

## Quantum Computing Examples

### Quantum Circuit Distribution

Distribute quantum circuits across multiple QPUs:

```python
async def quantum_circuit_distribution():
    """Distribute quantum computation across multiple QPUs."""
    
    protocol = HyperFabricProtocol(
        enable_quantum_optimization=True,
        enable_fault_tolerance=True
    )
    
    # Register quantum processing units
    qpu_specs = [
        ("ibm-qpu-01", 100, 1000),     # 100 qubits, 1000μs coherence
        ("google-qpu-01", 70, 500),    # 70 qubits, 500μs coherence  
        ("rigetti-qpu-01", 80, 200),   # 80 qubits, 200μs coherence
        ("ionq-qpu-01", 32, 10000),    # 32 qubits, 10000μs coherence (trapped ion)
    ]
    
    qpu_nodes = []
    for qpu_id, qubits, coherence_time in qpu_specs:
        node = NodeSignature(
            node_id=qpu_id,
            hardware_type=HardwareType.QUANTUM_QPU,
            bandwidth_gbps=10,
            latency_ns=50,
            compute_units=qubits,
            quantum_coherence_time_us=coherence_time,
            metadata={"quantum_volume": qubits * coherence_time}
        )
        await protocol.register_node(node)
        qpu_nodes.append(node)
    
    print(f"🔬 Registered {len(qpu_nodes)} quantum processing units")
    
    # Create quantum processing zone
    quantum_zone = FabricZone(
        zone_id="quantum-processing",
        zone_type=ZoneType.QUANTUM_REALM,
        isolation_level=IsolationLevel.QUANTUM_SECURE,
        max_nodes=20,
        required_bandwidth_gbps=50.0,
        quantum_coherence_required=True,
        description="Distributed quantum processing realm"
    )
    await protocol.create_zone(quantum_zone)
    
    # Simulate quantum circuit execution
    print("⚛️  Executing distributed quantum circuit...")
    
    # Create quantum circuit parts (simulated)
    circuit_parts = [
        {"qubits": list(range(0, 25)), "gates": ["H", "CNOT", "RZ"], "depth": 10},
        {"qubits": list(range(25, 50)), "gates": ["H", "CZ", "RY"], "depth": 8},
        {"qubits": list(range(50, 70)), "gates": ["X", "CNOT", "RX"], "depth": 12},
        {"qubits": list(range(70, 80)), "gates": ["Y", "CY", "RZ"], "depth": 6},
    ]
    
    # Execute circuit parts on different QPUs
    execution_tasks = []
    for i, (qpu_node, circuit_part) in enumerate(zip(qpu_nodes, circuit_parts)):
        # Serialize quantum circuit (in practice, use proper quantum circuit format)
        circuit_data = str(circuit_part).encode()
        
        task = protocol.send_data(
            source="quantum-controller",
            destination=qpu_node.node_id,
            data=circuit_data,
            data_type=DataType.QUANTUM_CIRCUIT,
            requires_quantum_entanglement=True,
            latency_constraint_ns=qpu_node.quantum_coherence_time_us * 100,  # 10% of coherence time
            metadata={"circuit_part": i, "expected_qubits": len(circuit_part["qubits"])}
        )
        execution_tasks.append((qpu_node.node_id, task))
    
    # Wait for quantum execution results
    results = []
    for qpu_id, task in execution_tasks:
        start_time = asyncio.get_event_loop().time()
        result = await task
        execution_time = (asyncio.get_event_loop().time() - start_time) * 1000000  # Convert to μs
        
        print(f"   {qpu_id:15s}: Completed in {execution_time:.1f}μs")
        results.append(result)
    
    # Simulate quantum state reconstruction
    print("🔮 Reconstructing final quantum state...")
    await asyncio.sleep(0.1)  # Simulate reconstruction time
    
    print("✅ Distributed quantum computation complete!")
    return results

asyncio.run(quantum_circuit_distribution())
```

### Quantum Error Correction Network

Implement a quantum error correction network:

```python
async def quantum_error_correction_network():
    """Simulate quantum error correction across distributed QPUs."""
    
    protocol = HyperFabricProtocol(enable_quantum_optimization=True)
    
    # Create logical qubit blocks (each containing multiple physical qubits)
    logical_qubits = []
    for i in range(5):  # 5 logical qubits
        node = NodeSignature(
            node_id=f"logical-qubit-{i}",
            hardware_type=HardwareType.QUANTUM_QPU,
            bandwidth_gbps=20,
            latency_ns=25,  # Ultra-low latency for error correction
            compute_units=200,  # 200 physical qubits per logical qubit
            quantum_coherence_time_us=50.0,
            metadata={"logical_qubit_id": i, "error_correction_code": "surface_code"}
        )
        await protocol.register_node(node)
        logical_qubits.append(node)
    
    # Central error correction processor
    error_processor = NodeSignature(
        node_id="error-correction-processor",
        hardware_type=HardwareType.CPU_SERVER,
        bandwidth_gbps=100,
        latency_ns=10,
        memory_gb=64,
        metadata={"purpose": "quantum_error_correction"}
    )
    await protocol.register_node(error_processor)
    
    print("🛡️  Quantum error correction network initialized")
    
    # Simulate error correction cycle
    print("🔄 Running error correction cycles...")
    
    for cycle in range(10):
        cycle_start = asyncio.get_event_loop().time()
        
        # Step 1: Measure syndromes from all logical qubits
        syndrome_tasks = []
        for logical_qubit in logical_qubits:
            # Generate fake syndrome data
            syndrome_data = np.random.randint(0, 2, 100)  # 100 syndrome bits
            
            task = protocol.send_data(
                source=logical_qubit.node_id,
                destination="error-correction-processor",
                data=syndrome_data.tobytes(),
                data_type=DataType.QUANTUM_STATE,
                priority=PacketPriority.ULTRA_HIGH,
                latency_constraint_ns=10_000,  # 10 microseconds max
                requires_quantum_entanglement=False  # Syndrome data is classical
            )
            syndrome_tasks.append(task)
        
        # Wait for all syndrome measurements
        syndrome_results = await asyncio.gather(*syndrome_tasks)
        syndrome_time = (asyncio.get_event_loop().time() - cycle_start) * 1000000
        
        # Step 2: Process error correction (simulate classical processing)
        processing_start = asyncio.get_event_loop().time()
        await asyncio.sleep(0.005)  # 5ms processing time
        processing_time = (asyncio.get_event_loop().time() - processing_start) * 1000000
        
        # Step 3: Send correction operations back to logical qubits
        correction_tasks = []
        for i, logical_qubit in enumerate(logical_qubits):
            # Generate fake correction operations
            corrections = np.random.choice(['I', 'X', 'Y', 'Z'], 50)  # 50 corrections
            
            task = protocol.send_data(
                source="error-correction-processor",
                destination=logical_qubit.node_id,
                data=corrections.tobytes(),
                data_type=DataType.QUANTUM_STATE,
                priority=PacketPriority.ULTRA_HIGH,
                latency_constraint_ns=5_000,  # 5 microseconds max
                requires_quantum_entanglement=True  # Corrections affect quantum state
            )
            correction_tasks.append(task)
        
        # Wait for all corrections to be applied
        await asyncio.gather(*correction_tasks)
        correction_time = (asyncio.get_event_loop().time() - processing_start - 0.005) * 1000000
        
        total_cycle_time = (asyncio.get_event_loop().time() - cycle_start) * 1000000
        
        print(f"   Cycle {cycle+1:2d}: "
              f"Syndrome {syndrome_time:5.1f}μs | "
              f"Process {processing_time:5.1f}μs | "
              f"Correct {correction_time:5.1f}μs | "
              f"Total {total_cycle_time:6.1f}μs")
        
        # Error correction cycles run every 100μs
        await asyncio.sleep(0.0001)
    
    print("✅ Quantum error correction cycles completed successfully")

asyncio.run(quantum_error_correction_network())
```

## High-Performance Computing Examples

### Supercomputing Cluster

Set up a large-scale supercomputing cluster:

```python
async def supercomputing_cluster_example():
    """Create a large-scale supercomputing cluster with HyperFabric."""
    
    protocol = HyperFabricProtocol(
        enable_ml_routing=True,
        enable_fault_tolerance=True,
        buffer_pool_size=10000  # Large buffer pool for HPC workloads
    )
    
    print("🖥️  Initializing supercomputing cluster...")
    
    # Create compute nodes (simulate 1000-node cluster)
    compute_nodes = []
    for rack in range(10):  # 10 racks
        for node in range(100):  # 100 nodes per rack
            node_id = f"compute-r{rack:02d}n{node:02d}"
            
            compute_node = NodeSignature(
                node_id=node_id,
                hardware_type=HardwareType.CPU_SERVER,
                bandwidth_gbps=200,
                latency_ns=500,
                memory_gb=512,
                compute_units=128,  # 128 CPU cores
                power_watts=800,
                rack_position=f"rack-{rack:02d}-node-{node:02d}",
                metadata={"node_type": "compute", "rack": rack, "position": node}
            )
            
            await protocol.register_node(compute_node)
            compute_nodes.append(compute_node)
            
            # Print progress every 100 nodes
            if (rack * 100 + node + 1) % 100 == 0:
                print(f"   Registered {rack * 100 + node + 1}/1000 compute nodes...")
    
    # Create storage nodes
    storage_nodes = []
    for i in range(20):  # 20 storage nodes
        storage_node = NodeSignature(
            node_id=f"storage-{i:02d}",
            hardware_type=HardwareType.STORAGE_ARRAY,
            bandwidth_gbps=400,
            latency_ns=2000,
            memory_gb=1024,
            metadata={"storage_capacity_tb": 1000, "storage_type": "parallel_filesystem"}
        )
        await protocol.register_node(storage_node)
        storage_nodes.append(storage_node)
    
    # Create management nodes
    management_node = NodeSignature(
        node_id="management-01",
        hardware_type=HardwareType.CPU_SERVER,
        bandwidth_gbps=100,
        latency_ns=1000,
        memory_gb=256,
        metadata={"node_type": "management", "services": ["scheduler", "monitoring"]}
    )
    await protocol.register_node(management_node)
    
    print(f"✅ Cluster initialized: {len(compute_nodes)} compute + {len(storage_nodes)} storage + 1 management")
    
    # Create HPC zones
    zones = [
        FabricZone(
            zone_id="hpc-compute",
            zone_type=ZoneType.COMPUTE_CLUSTER,
            isolation_level=IsolationLevel.MEDIUM,
            max_nodes=1200,
            required_bandwidth_gbps=200.0,
            description="High-performance computing cluster"
        ),
        FabricZone(
            zone_id="hpc-storage",
            zone_type=ZoneType.STORAGE_TIER,
            isolation_level=IsolationLevel.LOW,
            max_nodes=50,
            required_bandwidth_gbps=400.0,
            description="High-performance storage tier"
        )
    ]
    
    for zone in zones:
        await protocol.create_zone(zone)
    
    # Simulate parallel job execution
    print("🚀 Executing parallel computational job...")
    
    # Select subset of nodes for the job (simulate job allocation)
    job_nodes = compute_nodes[:256]  # Use 256 nodes for this job
    
    # Phase 1: Data distribution from storage to compute nodes
    print("   Phase 1: Distributing input data...")
    
    input_data = np.random.randn(1000, 1000).astype(np.float64)  # 8MB per node
    distribution_tasks = []
    
    for compute_node in job_nodes:
        task = protocol.send_data(
            source="storage-00",
            destination=compute_node.node_id,
            data=input_data.tobytes(),
            data_type=DataType.TENSOR,
            priority=PacketPriority.HIGH,
            compression_enabled=True
        )
        distribution_tasks.append(task)
    
    distribution_start = asyncio.get_event_loop().time()
    await asyncio.gather(*distribution_tasks)
    distribution_time = asyncio.get_event_loop().time() - distribution_start
    
    print(f"      Data distribution: {distribution_time:.2f}s "
          f"({len(job_nodes) * 8 / distribution_time:.1f} MB/s aggregate)")
    
    # Phase 2: Simulation of computation (nodes working independently)
    print("   Phase 2: Parallel computation...")
    computation_start = asyncio.get_event_loop().time()
    await asyncio.sleep(2.0)  # Simulate 2 seconds of computation
    computation_time = asyncio.get_event_loop().time() - computation_start
    
    # Phase 3: Results collection
    print("   Phase 3: Collecting results...")
    
    collection_tasks = []
    for compute_node in job_nodes:
        # Generate fake results
        result_data = np.random.randn(100, 100).astype(np.float64)  # 80KB per node
        
        task = protocol.send_data(
            source=compute_node.node_id,
            destination="storage-01",
            data=result_data.tobytes(),
            data_type=DataType.TENSOR,
            priority=PacketPriority.MEDIUM,
            compression_enabled=True
        )
        collection_tasks.append(task)
    
    collection_start = asyncio.get_event_loop().time()
    await asyncio.gather(*collection_tasks)
    collection_time = asyncio.get_event_loop().time() - collection_start
    
    total_job_time = distribution_time + computation_time + collection_time
    
    print(f"      Results collection: {collection_time:.2f}s")
    print(f"\n📊 Job Summary:")
    print(f"   Nodes used: {len(job_nodes)}")
    print(f"   Total job time: {total_job_time:.2f}s")
    print(f"   Communication overhead: {(distribution_time + collection_time)/total_job_time*100:.1f}%")
    print(f"   Effective computation time: {computation_time:.2f}s ({computation_time/total_job_time*100:.1f}%)")

asyncio.run(supercomputing_cluster_example())
```

## Edge Computing Examples

### IoT Sensor Network

Create an edge computing network for IoT sensors:

```python
async def iot_edge_network():
    """Set up edge computing network for IoT sensor data processing."""
    
    protocol = HyperFabricProtocol(
        enable_ml_routing=True,
        default_latency_constraint_ns=100_000_000  # 100ms for IoT applications
    )
    
    print("🌐 Setting up IoT edge computing network...")
    
    # Central cloud processing
    cloud_node = NodeSignature(
        node_id="cloud-datacenter",
        hardware_type=HardwareType.NVIDIA_A100,
        bandwidth_gbps=1000,
        latency_ns=50000,  # 50ms to cloud
        memory_gb=1000,
        physical_location="AWS us-east-1"
    )
    await protocol.register_node(cloud_node)
    
    # Regional edge servers
    edge_regions = [
        ("edge-west-coast", "San Francisco", 5000),
        ("edge-east-coast", "New York", 8000),
        ("edge-midwest", "Chicago", 12000),
        ("edge-south", "Atlanta", 10000)
    ]
    
    edge_servers = []
    for edge_id, location, latency_to_cloud in edge_regions:
        edge_server = NodeSignature(
            node_id=edge_id,
            hardware_type=HardwareType.NVIDIA_RTX4090,
            bandwidth_gbps=100,
            latency_ns=latency_to_cloud,
            memory_gb=64,
            physical_location=location,
            metadata={"server_type": "edge", "region": location}
        )
        await protocol.register_node(edge_server)
        edge_servers.append(edge_server)
    
    # IoT gateway nodes
    iot_gateways = []
    for region_idx, (edge_id, location, _) in enumerate(edge_regions):
        for gateway_idx in range(10):  # 10 gateways per region
            gateway_id = f"iot-gateway-{location.lower().replace(' ', '')}-{gateway_idx:02d}"
            
            gateway = NodeSignature(
                node_id=gateway_id,
                hardware_type=HardwareType.CPU_SERVER,
                bandwidth_gbps=10,
                latency_ns=1000,  # 1ms to edge server
                memory_gb=8,
                metadata={
                    "gateway_type": "iot",
                    "region": location,
                    "edge_server": edge_id,
                    "sensor_capacity": 1000
                }
            )
            await protocol.register_node(gateway)
            iot_gateways.append(gateway)
    
    print(f"✅ Network topology: 1 cloud + {len(edge_servers)} edge + {len(iot_gateways)} gateways")
    
    # Create edge computing zones
    edge_zone = FabricZone(
        zone_id="iot-edge-processing",
        zone_type=ZoneType.EDGE_NETWORK,
        isolation_level=IsolationLevel.LOW,
        max_nodes=100,
        required_bandwidth_gbps=10.0,
        description="IoT edge processing network"
    )
    await protocol.create_zone(edge_zone)
    
    # Simulate IoT data processing pipeline
    print("📡 Simulating IoT data processing...")
    
    # Deploy ML models to edge servers
    print("   Deploying ML models to edge servers...")
    model_data = np.random.randn(50, 50).astype(np.float32)  # Lightweight edge model
    
    model_deployment_tasks = []
    for edge_server in edge_servers:
        task = protocol.send_data(
            source="cloud-datacenter",
            destination=edge_server.node_id,
            data=model_data.tobytes(),
            data_type=DataType.PARAMETER,
            priority=PacketPriority.MEDIUM,
            compression_enabled=True
        )
        model_deployment_tasks.append(task)
    
    await asyncio.gather(*model_deployment_tasks)
    
    # Simulate sensor data flow
    print("   Processing real-time sensor data...")
    
    for batch in range(5):  # Process 5 batches of sensor data
        print(f"      Batch {batch + 1}/5:")
        
        batch_tasks = []
        
        # Each gateway processes sensor data from its region
        for gateway in iot_gateways:
            # Generate fake sensor data (temperature, humidity, pressure, etc.)
            sensor_data = {
                'timestamp': asyncio.get_event_loop().time(),
                'sensors': np.random.randn(100, 5),  # 100 sensors, 5 measurements each
                'gateway_id': gateway.node_id
            }
            
            # Find corresponding edge server for this gateway
            region = gateway.metadata['region']
            edge_server_id = gateway.metadata['edge_server']
            
            # Send raw sensor data to edge server for processing
            task = protocol.send_data(
                source=gateway.node_id,
                destination=edge_server_id,
                data=str(sensor_data).encode(),
                data_type=DataType.TENSOR,
                priority=PacketPriority.HIGH,
                latency_constraint_ns=50_000_000,  # 50ms max
                compression_enabled=True
            )
            batch_tasks.append((gateway.node_id, edge_server_id, task))
        
        # Process all sensor data in parallel
        batch_start = asyncio.get_event_loop().time()
        
        processed_results = []
        for gateway_id, edge_id, task in batch_tasks:
            result = await task
            processed_results.append((gateway_id, edge_id, result))
        
        batch_time = asyncio.get_event_loop().time() - batch_start
        
        # Aggregate and send significant results to cloud
        aggregated_data = f"Batch {batch + 1} aggregated results from {len(processed_results)} gateways"
        
        cloud_tasks = []
        for edge_server in edge_servers:
            task = protocol.send_data(
                source=edge_server.node_id,
                destination="cloud-datacenter",
                data=aggregated_data.encode(),
                data_type=DataType.METADATA,
                priority=PacketPriority.LOW,  # Non-critical cloud sync
                compression_enabled=True
            )
            cloud_tasks.append(task)
        
        await asyncio.gather(*cloud_tasks)
        
        print(f"         Processed {len(batch_tasks)} gateways in {batch_time*1000:.1f}ms")
        
        # Brief pause between batches
        await asyncio.sleep(1.0)
    
    print("✅ IoT edge processing simulation completed")

asyncio.run(iot_edge_network())
```

## Performance Monitoring Examples

### Real-Time Fabric Monitoring

Monitor fabric performance in real-time:

```python
async def fabric_monitoring_example():
    """Comprehensive fabric monitoring and performance analysis."""
    
    protocol = HyperFabricProtocol(enable_ml_routing=True)
    
    # Set up a monitoring infrastructure
    print("📊 Setting up fabric monitoring infrastructure...")
    
    # Create diverse node types for comprehensive monitoring
    test_nodes = [
        NodeSignature("gpu-powerhouse", HardwareType.NVIDIA_H100, 400, 80),
        NodeSignature("quantum-lab", HardwareType.QUANTUM_QPU, 10, 30, quantum_coherence_time_us=200),
        NodeSignature("storage-massive", HardwareType.STORAGE_ARRAY, 200, 1000),
        NodeSignature("neuromorphic-brain", HardwareType.NEUROMORPHIC_CHIP, 50, 60, neuromorphic_neurons=1000000),
        NodeSignature("edge-processor", HardwareType.CPU_SERVER, 25, 5000),
    ]
    
    for node in test_nodes:
        await protocol.register_node(node)
    
    print(f"✅ Monitoring setup: {len(test_nodes)} nodes registered")
    
    # Performance monitoring loop
    print("🔄 Starting real-time performance monitoring...")
    
    monitoring_duration = 30  # Monitor for 30 seconds
    sample_interval = 2  # Sample every 2 seconds
    samples = monitoring_duration // sample_interval
    
    performance_history = []
    
    for sample in range(samples):
        sample_start = asyncio.get_event_loop().time()
        
        print(f"\n📈 Sample {sample + 1}/{samples} - {asyncio.get_event_loop().time():.1f}s")
        
        # Test connectivity between all node pairs
        connectivity_results = []
        ping_tasks = []
        
        for i, source_node in enumerate(test_nodes):
            for j, dest_node in enumerate(test_nodes):
                if i != j:  # Don't ping self
                    task = protocol.ping(
                        source=source_node.node_id,
                        destination=dest_node.node_id,
                        packet_size=1024  # 1KB ping packets
                    )
                    ping_tasks.append((source_node.node_id, dest_node.node_id, task))
        
        # Execute all pings in parallel
        for source, dest, task in ping_tasks:
            try:
                result = await task
                connectivity_results.append({
                    'source': source,
                    'destination': dest,
                    'latency_ms': result.latency_ms,
                    'bandwidth_gbps': result.bandwidth_gbps,
                    'success': result.success
                })
            except Exception as e:
                connectivity_results.append({
                    'source': source,
                    'destination': dest,
                    'latency_ms': float('inf'),
                    'bandwidth_gbps': 0,
                    'success': False,
                    'error': str(e)
                })
        
        # Analyze connectivity results
        successful_pings = [r for r in connectivity_results if r['success']]
        failed_pings = [r for r in connectivity_results if not r['success']]
        
        if successful_pings:
            avg_latency = np.mean([r['latency_ms'] for r in successful_pings])
            min_latency = np.min([r['latency_ms'] for r in successful_pings])
            max_latency = np.max([r['latency_ms'] for r in successful_pings])
            avg_bandwidth = np.mean([r['bandwidth_gbps'] for r in successful_pings])
            
            print(f"   Connectivity: {len(successful_pings)}/{len(connectivity_results)} successful")
            print(f"   Latency: {min_latency:.3f}ms - {avg_latency:.3f}ms - {max_latency:.3f}ms (min/avg/max)")
            print(f"   Bandwidth: {avg_bandwidth:.1f} Gbps average")
            
            if failed_pings:
                print(f"   ⚠️  {len(failed_pings)} failed connections detected")
        
        # Simulate data transfers for throughput testing
        transfer_tasks = []
        transfer_sizes = [1024, 10240, 102400]  # 1KB, 10KB, 100KB
        
        for size in transfer_sizes:
            test_data = np.random.bytes(size)
            
            task = protocol.send_data(
                source="gpu-powerhouse",
                destination="storage-massive",
                data=test_data,
                data_type=DataType.GENERIC,
                priority=PacketPriority.MEDIUM
            )
            transfer_tasks.append((size, task))
        
        # Measure transfer performance
        transfer_results = []
        for size, task in transfer_tasks:
            transfer_start = asyncio.get_event_loop().time()
            try:
                result = await task
                transfer_time = asyncio.get_event_loop().time() - transfer_start
                throughput_mbps = (size * 8) / (transfer_time * 1_000_000)  # Mbps
                
                transfer_results.append({
                    'size_bytes': size,
                    'time_ms': transfer_time * 1000,
                    'throughput_mbps': throughput_mbps
                })
                
                print(f"   Transfer {size:6d}B: {transfer_time*1000:5.1f}ms ({throughput_mbps:6.1f} Mbps)")
                
            except Exception as e:
                print(f"   Transfer {size:6d}B: FAILED - {e}")
        
        # Store sample data
        sample_data = {
            'timestamp': sample_start,
            'connectivity': connectivity_results,
            'transfers': transfer_results,
            'successful_connections': len(successful_pings),
            'total_connections': len(connectivity_results),
            'avg_latency_ms': avg_latency if successful_pings else None,
            'avg_bandwidth_gbps': avg_bandwidth if successful_pings else None
        }
        performance_history.append(sample_data)
        
        # Wait for next sample
        elapsed = asyncio.get_event_loop().time() - sample_start
        sleep_time = max(0, sample_interval - elapsed)
        if sleep_time > 0:
            await asyncio.sleep(sleep_time)
    
    # Generate monitoring report
    print(f"\n📋 Fabric Performance Report ({monitoring_duration}s monitoring)")
    print("=" * 60)
    
    # Connectivity analysis
    total_tests = sum(len(sample['connectivity']) for sample in performance_history)
    successful_tests = sum(sample['successful_connections'] for sample in performance_history)
    success_rate = (successful_tests / total_tests) * 100 if total_tests > 0 else 0
    
    print(f"📡 Connectivity Analysis:")
    print(f"   Total connection tests: {total_tests}")
    print(f"   Successful connections: {successful_tests}")
    print(f"   Success rate: {success_rate:.1f}%")
    
    # Latency trends
    latencies = [s['avg_latency_ms'] for s in performance_history if s['avg_latency_ms'] is not None]
    if latencies:
        print(f"\n⚡ Latency Trends:")
        print(f"   Average latency: {np.mean(latencies):.3f}ms")
        print(f"   Latency range: {np.min(latencies):.3f}ms - {np.max(latencies):.3f}ms")
        print(f"   Latency std dev: {np.std(latencies):.3f}ms")
    
    # Bandwidth trends
    bandwidths = [s['avg_bandwidth_gbps'] for s in performance_history if s['avg_bandwidth_gbps'] is not None]
    if bandwidths:
        print(f"\n🚀 Bandwidth Trends:")
        print(f"   Average bandwidth: {np.mean(bandwidths):.1f} Gbps")
        print(f"   Bandwidth range: {np.min(bandwidths):.1f} - {np.max(bandwidths):.1f} Gbps")
        print(f"   Bandwidth utilization: {np.mean(bandwidths)/400*100:.1f}% of peak capacity")
    
    print("\n✅ Fabric monitoring completed successfully")
    
    return performance_history

# Run the monitoring example
monitoring_data = asyncio.run(fabric_monitoring_example())
```

These comprehensive examples demonstrate the full capabilities of HyperFabric Interconnect across diverse computing scenarios, from basic setups to advanced distributed systems, quantum computing, and real-time monitoring applications.
