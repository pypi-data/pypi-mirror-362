# 📚 API Reference

Complete API documentation for HyperFabric Interconnect components.

## Core Protocol

### HyperFabricProtocol

The main orchestrator class for all fabric operations.

```python
class HyperFabricProtocol:
    """Ultra-low-latency, high-bandwidth interconnect protocol."""
    
    def __init__(
        self,
        enable_ml_routing: bool = False,
        enable_quantum_optimization: bool = False,
        enable_fault_tolerance: bool = True,
        default_latency_constraint_ns: Optional[int] = None,
        buffer_pool_size: int = 1000,
        max_packet_size: int = 65536
    ):
        """Initialize the HyperFabric protocol.
        
        Args:
            enable_ml_routing: Enable ML-based routing optimizations
            enable_quantum_optimization: Enable quantum-aware networking
            enable_fault_tolerance: Enable automatic fault recovery
            default_latency_constraint_ns: Default latency constraint in nanoseconds
            buffer_pool_size: Size of the zero-copy buffer pool
            max_packet_size: Maximum packet size in bytes
        """
```

#### Core Methods

##### register_node()

```python
async def register_node(self, node: NodeSignature) -> bool:
    """Register a new node in the fabric topology.
    
    Args:
        node: NodeSignature containing node specifications
        
    Returns:
        bool: True if registration successful, False otherwise
        
    Raises:
        DuplicateNodeError: If node ID already exists
        InvalidNodeError: If node specification is invalid
        
    Example:
        >>> node = NodeSignature(
        ...     node_id="gpu-cluster-01",
        ...     hardware_type=HardwareType.NVIDIA_H100,
        ...     bandwidth_gbps=400,
        ...     latency_ns=100
        ... )
        >>> success = await protocol.register_node(node)
    """
```

##### send_data()

```python
async def send_data(
    self,
    source: str,
    destination: str,
    data: Any,
    data_type: DataType = DataType.GENERIC,
    priority: PacketPriority = PacketPriority.MEDIUM,
    latency_constraint_ns: Optional[int] = None,
    requires_quantum_entanglement: bool = False,
    compression_enabled: bool = False,
    encryption_enabled: bool = False,
    metadata: Optional[Dict[str, Any]] = None
) -> Any:
    """Send data between nodes with optimized routing.
    
    Args:
        source: Source node ID
        destination: Destination node ID
        data: Data payload to transfer
        data_type: Type of data being transferred
        priority: Packet priority level
        latency_constraint_ns: Maximum acceptable latency in nanoseconds
        requires_quantum_entanglement: Whether quantum entanglement is required
        compression_enabled: Enable data compression
        encryption_enabled: Enable data encryption
        metadata: Additional metadata dictionary
        
    Returns:
        Any: Response data from destination node
        
    Raises:
        NodeNotFoundError: If source or destination node doesn't exist
        LatencyConstraintViolationError: If latency constraint cannot be met
        QuantumCoherenceError: If quantum operation fails
        
    Example:
        >>> result = await protocol.send_data(
        ...     source="gpu-01",
        ...     destination="storage-cluster",
        ...     data=model_weights,
        ...     data_type=DataType.PARAMETER,
        ...     priority=PacketPriority.HIGH,
        ...     latency_constraint_ns=1_000_000  # 1ms
        ... )
    """
```

##### ping()

```python
async def ping(
    self,
    source: str,
    destination: str,
    packet_size: int = 64,
    timeout_ms: int = 5000
) -> PingResult:
    """Test connectivity and measure latency between nodes.
    
    Args:
        source: Source node ID
        destination: Destination node ID  
        packet_size: Size of ping packet in bytes
        timeout_ms: Timeout in milliseconds
        
    Returns:
        PingResult: Contains latency, bandwidth, and path information
        
    Example:
        >>> result = await protocol.ping("gpu-01", "storage-01")
        >>> print(f"Latency: {result.latency_ns}ns")
    """
```

##### create_zone()

```python
async def create_zone(self, zone: FabricZone) -> bool:
    """Create a new fabric zone for logical network segmentation.
    
    Args:
        zone: FabricZone configuration
        
    Returns:
        bool: True if zone created successfully
        
    Raises:
        DuplicateZoneError: If zone ID already exists
        InsufficientResourcesError: If not enough resources available
    """
```

##### get_topology_info()

```python
async def get_topology_info(self) -> TopologyInfo:
    """Get current fabric topology information.
    
    Returns:
        TopologyInfo: Complete topology state including nodes, links, and zones
    """
```

##### start_background_services()

```python
async def start_background_services(self) -> None:
    """Start background monitoring and optimization services.
    
    Services started:
    - Topology monitoring
    - Performance optimization  
    - Fault detection
    - Load balancing
    """
```

##### stop_background_services()

```python
async def stop_background_services(self) -> None:
    """Stop all background services gracefully."""
```

## Data Models

### NodeSignature

```python
@dataclass
class NodeSignature:
    """Comprehensive node specification for fabric registration."""
    
    node_id: str
    hardware_type: HardwareType
    bandwidth_gbps: float
    latency_ns: int
    memory_gb: Optional[float] = None
    compute_units: Optional[int] = None
    power_watts: Optional[float] = None
    rack_position: Optional[str] = None
    physical_location: Optional[str] = None
    quantum_coherence_time_us: Optional[float] = None
    neuromorphic_neurons: Optional[int] = None
    photonic_channels: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        """Validate node specification after initialization."""
        if self.bandwidth_gbps <= 0:
            raise ValueError("Bandwidth must be positive")
        if self.latency_ns < 0:
            raise ValueError("Latency cannot be negative")
        if self.hardware_type == HardwareType.QUANTUM_QPU and not self.quantum_coherence_time_us:
            raise ValueError("Quantum QPU requires coherence time specification")
```

### HardwareType

```python
class HardwareType(Enum):
    """Supported hardware types for fabric nodes."""
    
    # GPU Accelerators
    NVIDIA_H100 = "nvidia_h100"
    NVIDIA_A100 = "nvidia_a100"
    NVIDIA_RTX4090 = "nvidia_rtx4090"
    AMD_MI300X = "amd_mi300x"
    AMD_MI250X = "amd_mi250x"
    INTEL_GAUDI2 = "intel_gaudi2"
    
    # Quantum Processing Units
    QUANTUM_QPU = "quantum_qpu"
    QUANTUM_ANNEALER = "quantum_annealer"
    
    # Neuromorphic Chips
    NEUROMORPHIC_CHIP = "neuromorphic_chip"
    INTEL_LOIHI = "intel_loihi"
    
    # Photonic Components
    PHOTONIC_SWITCH = "photonic_switch"
    OPTICAL_INTERCONNECT = "optical_interconnect"
    
    # Traditional Computing
    CPU_SERVER = "cpu_server"
    STORAGE_ARRAY = "storage_array"
    NETWORK_SWITCH = "network_switch"
    
    # Custom Hardware
    CUSTOM = "custom"
```

### DataType

```python
class DataType(Enum):
    """Types of data that can be transferred through the fabric."""
    
    # AI/ML Data Types
    TENSOR = "tensor"
    PARAMETER = "parameter"
    GRADIENT = "gradient"
    ACTIVATION = "activation"
    EMBEDDING = "embedding"
    
    # Quantum Data Types
    QUANTUM_STATE = "quantum_state"
    QUANTUM_CIRCUIT = "quantum_circuit"
    
    # Neuromorphic Data Types
    NEUROMORPHIC_SPIKE = "neuromorphic_spike"
    SPIKE_TRAIN = "spike_train"
    
    # Control and Metadata
    CONTROL_MESSAGE = "control_message"
    METADATA = "metadata"
    HEARTBEAT = "heartbeat"
    
    # Generic Data
    GENERIC = "generic"
    BINARY = "binary"
    JSON = "json"
```

### PacketPriority

```python
class PacketPriority(Enum):
    """Packet priority levels for QoS routing."""
    
    ULTRA_HIGH = 0    # Real-time critical (autonomous vehicles, quantum)
    HIGH = 1          # Low-latency applications (AI inference)
    MEDIUM = 2        # Standard applications (training, file transfer)
    LOW = 3           # Background tasks (data synchronization)
    BULK = 4          # Large transfers (model distribution)
```

## Routing Engine

### RoutingEngine

```python
class RoutingEngine:
    """Advanced routing engine with multiple optimization strategies."""
    
    def __init__(
        self,
        enable_ml_optimization: bool = False,
        enable_quantum_optimization: bool = False,
        enable_neuromorphic_routing: bool = False
    ):
        """Initialize routing engine with optimization features."""
```

#### Routing Methods

##### find_optimal_path()

```python
async def find_optimal_path(
    self,
    source: str,
    destination: str,
    data_type: DataType,
    latency_constraint_ns: Optional[int] = None,
    bandwidth_requirement_gbps: Optional[float] = None
) -> List[str]:
    """Find optimal routing path between nodes.
    
    Args:
        source: Source node ID
        destination: Destination node ID
        data_type: Type of data being routed
        latency_constraint_ns: Maximum acceptable latency
        bandwidth_requirement_gbps: Minimum required bandwidth
        
    Returns:
        List[str]: Ordered list of node IDs forming the optimal path
        
    Raises:
        NoRouteFoundError: If no valid route exists
        LatencyConstraintViolationError: If latency constraint cannot be met
    """
```

##### update_link_metrics()

```python
async def update_link_metrics(
    self,
    source: str,
    destination: str,
    latency_ns: int,
    bandwidth_utilized_gbps: float,
    packet_loss_rate: float = 0.0
) -> None:
    """Update real-time link performance metrics.
    
    Args:
        source: Source node ID
        destination: Destination node ID
        latency_ns: Measured latency in nanoseconds
        bandwidth_utilized_gbps: Current bandwidth utilization
        packet_loss_rate: Packet loss rate (0.0 to 1.0)
    """
```

## Buffer Management

### ZeroCopyBuffer

```python
class ZeroCopyBuffer:
    """High-performance zero-copy buffer for ultra-low latency transfers."""
    
    def __init__(
        self,
        size: int,
        enable_compression: bool = False,
        enable_encryption: bool = False
    ):
        """Initialize zero-copy buffer.
        
        Args:
            size: Buffer size in bytes
            enable_compression: Enable LZ4 compression
            enable_encryption: Enable AES encryption
        """
```

#### Buffer Methods

##### write_data()

```python
async def write_data(
    self,
    data: bytes,
    offset: int = 0,
    compress: bool = False
) -> int:
    """Write data to buffer with zero-copy semantics.
    
    Args:
        data: Data to write
        offset: Offset in buffer
        compress: Apply compression
        
    Returns:
        int: Number of bytes written
        
    Raises:
        BufferOverflowError: If data exceeds buffer capacity
    """
```

##### read_data()

```python
async def read_data(
    self,
    size: int,
    offset: int = 0,
    decompress: bool = False
) -> bytes:
    """Read data from buffer with zero-copy semantics.
    
    Args:
        size: Number of bytes to read
        offset: Offset in buffer  
        decompress: Apply decompression
        
    Returns:
        bytes: Data read from buffer
        
    Raises:
        BufferUnderflowError: If not enough data available
    """
```

### BufferManager

```python
class BufferManager:
    """Manages pool of zero-copy buffers for optimal memory utilization."""
    
    def __init__(self, pool_size: int = 1000, buffer_size: int = 65536):
        """Initialize buffer manager with specified pool size."""
```

## Topology Management

### TopologyManager

```python
class TopologyManager:
    """Manages fabric topology and network graph operations."""
    
    def __init__(self, enable_auto_optimization: bool = True):
        """Initialize topology manager."""
```

#### Topology Methods

##### add_node()

```python
async def add_node(self, node: NodeSignature) -> bool:
    """Add node to topology graph.
    
    Args:
        node: Node specification
        
    Returns:
        bool: True if node added successfully
    """
```

##### remove_node()

```python
async def remove_node(self, node_id: str) -> bool:
    """Remove node from topology graph.
    
    Args:
        node_id: ID of node to remove
        
    Returns:
        bool: True if node removed successfully
    """
```

##### find_shortest_path()

```python
def find_shortest_path(
    self,
    source: str,
    destination: str,
    weight_metric: str = "latency"
) -> List[str]:
    """Find shortest path using specified metric.
    
    Args:
        source: Source node ID
        destination: Destination node ID
        weight_metric: Metric for path optimization ("latency", "bandwidth", "hops")
        
    Returns:
        List[str]: Shortest path as list of node IDs
    """
```

##### analyze_bottlenecks()

```python
async def analyze_bottlenecks(self) -> List[BottleneckInfo]:
    """Analyze topology for performance bottlenecks.
    
    Returns:
        List[BottleneckInfo]: Identified bottlenecks with recommendations
    """
```

### FabricZone

```python
@dataclass
class FabricZone:
    """Logical network zone for traffic isolation and optimization."""
    
    zone_id: str
    zone_type: ZoneType
    isolation_level: IsolationLevel
    max_nodes: int
    required_bandwidth_gbps: float
    description: Optional[str] = None
    quantum_coherence_required: bool = False
    neuromorphic_optimization: bool = False
    
    def __post_init__(self):
        """Validate zone configuration."""
        if self.max_nodes <= 0:
            raise ValueError("Max nodes must be positive")
        if self.required_bandwidth_gbps <= 0:
            raise ValueError("Required bandwidth must be positive")
```

### ZoneType

```python
class ZoneType(Enum):
    """Types of fabric zones for different workload patterns."""
    
    COMPUTE_CLUSTER = "compute_cluster"       # AI training clusters
    INFERENCE_FARM = "inference_farm"         # Real-time inference
    STORAGE_TIER = "storage_tier"             # Data storage systems
    QUANTUM_REALM = "quantum_realm"           # Quantum processing
    NEUROMORPHIC_NET = "neuromorphic_net"     # Neuromorphic computing
    EDGE_NETWORK = "edge_network"             # Edge computing nodes
    CONTROL_PLANE = "control_plane"           # Management and monitoring
```

### IsolationLevel

```python
class IsolationLevel(Enum):
    """Network isolation levels for security and performance."""
    
    NONE = "none"                    # No isolation
    LOW = "low"                      # Basic traffic shaping
    MEDIUM = "medium"                # VLAN-level isolation
    HIGH = "high"                    # Strong network segmentation
    QUANTUM_SECURE = "quantum_secure" # Quantum-level security
```

## Exception Hierarchy

### Core Exceptions

```python
class HyperFabricError(Exception):
    """Base exception for all HyperFabric errors."""
    pass

class NodeError(HyperFabricError):
    """Base class for node-related errors."""
    pass

class DuplicateNodeError(NodeError):
    """Raised when attempting to register a duplicate node."""
    pass

class NodeNotFoundError(NodeError):
    """Raised when specified node doesn't exist."""
    pass

class InvalidNodeError(NodeError):
    """Raised when node specification is invalid."""
    pass

class RoutingError(HyperFabricError):
    """Base class for routing-related errors."""
    pass

class NoRouteFoundError(RoutingError):
    """Raised when no valid route exists between nodes."""
    pass

class LatencyConstraintViolationError(RoutingError):
    """Raised when latency constraint cannot be satisfied."""
    pass

class QuantumError(HyperFabricError):
    """Base class for quantum-related errors."""
    pass

class QuantumCoherenceError(QuantumError):
    """Raised when quantum coherence is lost."""
    pass

class BufferError(HyperFabricError):
    """Base class for buffer-related errors."""
    pass

class BufferOverflowError(BufferError):
    """Raised when buffer capacity is exceeded."""
    pass

class BufferUnderflowError(BufferError):
    """Raised when insufficient data in buffer."""
    pass
```

## Result Classes

### PingResult

```python
@dataclass
class PingResult:
    """Result of a ping operation between two nodes."""
    
    source: str
    destination: str
    latency_ns: int
    bandwidth_gbps: float
    path: List[str]
    packet_loss_rate: float
    timestamp: float
    success: bool
    
    @property
    def latency_ms(self) -> float:
        """Get latency in milliseconds."""
        return self.latency_ns / 1_000_000
    
    @property
    def latency_us(self) -> float:
        """Get latency in microseconds."""
        return self.latency_ns / 1_000
```

### TopologyInfo

```python
@dataclass  
class TopologyInfo:
    """Complete fabric topology information."""
    
    total_nodes: int
    total_links: int
    zones: List[FabricZone]
    bottlenecks: List[BottleneckInfo]
    performance_metrics: Dict[str, float]
    quantum_enabled_nodes: int
    neuromorphic_nodes: int
    timestamp: float
```

### BottleneckInfo

```python
@dataclass
class BottleneckInfo:
    """Information about network bottlenecks."""
    
    location: str
    bottleneck_type: str
    severity: float  # 0.0 to 1.0
    current_utilization: float
    recommended_action: str
    affected_paths: List[List[str]]
```

## Utility Functions

### Performance Monitoring

```python
async def measure_network_performance(
    protocol: HyperFabricProtocol,
    duration_seconds: int = 60
) -> Dict[str, float]:
    """Measure comprehensive network performance metrics.
    
    Args:
        protocol: HyperFabric protocol instance
        duration_seconds: Measurement duration
        
    Returns:
        Dict containing performance metrics
    """
```

### Configuration Management

```python
def load_fabric_config(config_file: str) -> Dict[str, Any]:
    """Load fabric configuration from YAML file.
    
    Args:
        config_file: Path to configuration file
        
    Returns:
        Dict containing configuration parameters
    """

def save_fabric_config(
    config: Dict[str, Any],
    config_file: str
) -> None:
    """Save fabric configuration to YAML file.
    
    Args:
        config: Configuration dictionary
        config_file: Output file path
    """
```

### Hardware Detection

```python
def detect_hardware_capabilities() -> List[NodeSignature]:
    """Auto-detect available hardware and generate node signatures.
    
    Returns:
        List of detected node signatures
    """

def validate_hardware_compatibility(
    node: NodeSignature
) -> bool:
    """Validate hardware compatibility with fabric requirements.
    
    Args:
        node: Node signature to validate
        
    Returns:
        bool: True if compatible, False otherwise
    """
```

## Constants

```python
# Performance Thresholds
MAX_LATENCY_QUANTUM_NS = 100_000      # 100 microseconds for quantum ops
MAX_LATENCY_AI_INFERENCE_NS = 1_000_000  # 1ms for AI inference
MAX_LATENCY_TRAINING_NS = 10_000_000   # 10ms for training workloads

# Buffer Sizes
DEFAULT_BUFFER_SIZE = 65536           # 64KB default buffer
LARGE_BUFFER_SIZE = 1048576          # 1MB for large transfers
QUANTUM_BUFFER_SIZE = 4096           # 4KB for quantum states

# Bandwidth Limits
MIN_BANDWIDTH_GBPS = 1.0             # Minimum supported bandwidth
MAX_BANDWIDTH_GBPS = 1000.0          # Maximum theoretical bandwidth

# Quantum Parameters
QUANTUM_COHERENCE_THRESHOLD_US = 10.0  # Minimum coherence time
MAX_QUANTUM_ENTANGLED_NODES = 100     # Maximum entangled nodes
```

This comprehensive API reference provides complete documentation for all HyperFabric Interconnect components, enabling developers to build advanced networking applications for AI and quantum computing workloads.
