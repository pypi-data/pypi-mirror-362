"""
Node definitions and hardware signatures for HyperFabric Interconnect.
"""

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any
from uuid import uuid4


class HardwareType(Enum):
    """Supported hardware types in the fabric."""
    NVIDIA_H100 = "nvidia-h100"
    NVIDIA_A100 = "nvidia-a100"
    NVIDIA_V100 = "nvidia-v100"
    AMD_MI300X = "amd-mi300x"
    INTEL_GAUDI2 = "intel-gaudi2"
    QUANTUM_QPU = "quantum-qpu"
    CPU_CLUSTER = "cpu-cluster"
    FPGA_FABRIC = "fpga-fabric"
    PHOTONIC_SWITCH = "photonic-switch"
    NEUROMORPHIC_CHIP = "neuromorphic-chip"


@dataclass
class NodeSignature:
    """
    Hardware signature and capabilities of a fabric node.
    
    This represents the complete hardware profile including performance
    characteristics, connectivity options, and quantum-aware capabilities.
    """
    node_id: str
    hardware_type: HardwareType
    bandwidth_gbps: float
    latency_ns: int
    memory_gb: Optional[float] = None
    compute_units: Optional[int] = None
    quantum_coherence_time_us: Optional[float] = None
    photonic_channels: Optional[int] = None
    neuromorphic_neurons: Optional[int] = None
    
    # Auto-generated fields
    uuid: str = field(default_factory=lambda: str(uuid4()))
    registration_time: float = field(default_factory=time.time)
    last_heartbeat: float = field(default_factory=time.time)
    
    # Status tracking
    is_active: bool = True
    is_healthy: bool = True
    load_percentage: float = 0.0
    temperature_c: Optional[float] = None
    
    # Connectivity
    physical_location: Optional[str] = None
    rack_position: Optional[str] = None
    switch_port: Optional[str] = None
    
    # Custom metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate node signature after initialization."""
        if self.bandwidth_gbps <= 0:
            raise ValueError("Bandwidth must be positive")
        if self.latency_ns < 0:
            raise ValueError("Latency cannot be negative")
        
        # Set default memory based on hardware type
        if self.memory_gb is None:
            self.memory_gb = self._get_default_memory()
        
        # Set default compute units
        if self.compute_units is None:
            self.compute_units = self._get_default_compute_units()
    
    def _get_default_memory(self) -> float:
        """Get default memory based on hardware type."""
        memory_map = {
            HardwareType.NVIDIA_H100: 80.0,
            HardwareType.NVIDIA_A100: 80.0,
            HardwareType.NVIDIA_V100: 32.0,
            HardwareType.AMD_MI300X: 192.0,
            HardwareType.INTEL_GAUDI2: 96.0,
            HardwareType.QUANTUM_QPU: 0.001,  # Quantum memory in GB equivalent
            HardwareType.CPU_CLUSTER: 1024.0,
            HardwareType.FPGA_FABRIC: 64.0,
            HardwareType.PHOTONIC_SWITCH: 0.0,
            HardwareType.NEUROMORPHIC_CHIP: 8.0,
        }
        return memory_map.get(self.hardware_type, 32.0)
    
    def _get_default_compute_units(self) -> int:
        """Get default compute units based on hardware type."""
        compute_map = {
            HardwareType.NVIDIA_H100: 16896,  # CUDA cores
            HardwareType.NVIDIA_A100: 6912,
            HardwareType.NVIDIA_V100: 5120,
            HardwareType.AMD_MI300X: 19456,
            HardwareType.INTEL_GAUDI2: 2048,
            HardwareType.QUANTUM_QPU: 1000,  # Qubits
            HardwareType.CPU_CLUSTER: 128,   # CPU cores
            HardwareType.FPGA_FABRIC: 1000000,  # Logic elements
            HardwareType.PHOTONIC_SWITCH: 0,
            HardwareType.NEUROMORPHIC_CHIP: 1000000,  # Neurons
        }
        return compute_map.get(self.hardware_type, 1)
    
    def update_heartbeat(self) -> None:
        """Update the last heartbeat timestamp."""
        self.last_heartbeat = time.time()
    
    def update_load(self, load_percentage: float) -> None:
        """Update the current load percentage."""
        if 0 <= load_percentage <= 100:
            self.load_percentage = load_percentage
        else:
            raise ValueError("Load percentage must be between 0 and 100")
    
    def is_quantum_capable(self) -> bool:
        """Check if this node has quantum capabilities."""
        return (
            self.hardware_type == HardwareType.QUANTUM_QPU
            or self.quantum_coherence_time_us is not None
        )
    
    def is_photonic_capable(self) -> bool:
        """Check if this node has photonic capabilities."""
        return (
            self.hardware_type == HardwareType.PHOTONIC_SWITCH
            or self.photonic_channels is not None
        )
    
    def is_neuromorphic_capable(self) -> bool:
        """Check if this node has neuromorphic capabilities."""
        return (
            self.hardware_type == HardwareType.NEUROMORPHIC_CHIP
            or self.neuromorphic_neurons is not None
        )
    
    def get_theoretical_throughput_gbps(self) -> float:
        """Calculate theoretical maximum throughput."""
        base_throughput = self.bandwidth_gbps
        
        # Apply hardware-specific multipliers
        if self.hardware_type == HardwareType.PHOTONIC_SWITCH:
            base_throughput *= 10  # Photonic advantage
        elif self.is_quantum_capable():
            base_throughput *= 5   # Quantum parallelism
        elif self.is_neuromorphic_capable():
            base_throughput *= 3   # Neuromorphic efficiency
        
        # Apply load factor
        load_factor = 1.0 - (self.load_percentage / 100.0)
        return base_throughput * load_factor
    
    def estimate_latency_to(self, other_node: "NodeSignature") -> float:
        """Estimate latency to another node in nanoseconds."""
        base_latency = max(self.latency_ns, other_node.latency_ns)
        
        # Add network hop latency (simplified model)
        network_latency = 1000  # 1 microsecond base network latency
        
        # Hardware-specific optimizations
        if self.is_photonic_capable() and other_node.is_photonic_capable():
            network_latency *= 0.1  # Photonic speed-of-light advantage
        elif self.is_quantum_capable() and other_node.is_quantum_capable():
            network_latency *= 0.5  # Quantum entanglement advantage
        
        return base_latency + network_latency
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert node signature to dictionary."""
        return {
            "node_id": self.node_id,
            "hardware_type": self.hardware_type.value,
            "bandwidth_gbps": self.bandwidth_gbps,
            "latency_ns": self.latency_ns,
            "memory_gb": self.memory_gb,
            "compute_units": self.compute_units,
            "quantum_coherence_time_us": self.quantum_coherence_time_us,
            "photonic_channels": self.photonic_channels,
            "neuromorphic_neurons": self.neuromorphic_neurons,
            "uuid": self.uuid,
            "registration_time": self.registration_time,
            "last_heartbeat": self.last_heartbeat,
            "is_active": self.is_active,
            "is_healthy": self.is_healthy,
            "load_percentage": self.load_percentage,
            "temperature_c": self.temperature_c,
            "physical_location": self.physical_location,
            "rack_position": self.rack_position,
            "switch_port": self.switch_port,
            "metadata": self.metadata,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "NodeSignature":
        """Create node signature from dictionary."""
        # Convert string hardware type back to enum
        if isinstance(data.get("hardware_type"), str):
            data["hardware_type"] = HardwareType(data["hardware_type"])
        
        return cls(**data)
