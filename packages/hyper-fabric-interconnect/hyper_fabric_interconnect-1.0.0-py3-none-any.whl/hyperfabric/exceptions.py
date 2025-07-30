"""
Custom exceptions for HyperFabric Interconnect.
"""


class HyperFabricError(Exception):
    """Base exception for all HyperFabric errors."""
    pass


class NodeNotFoundError(HyperFabricError):
    """Raised when a node is not found in the fabric."""
    pass


class RoutingError(HyperFabricError):
    """Raised when routing operations fail."""
    pass


class BufferError(HyperFabricError):
    """Raised when buffer operations fail."""
    pass


class TopologyError(HyperFabricError):
    """Raised when topology operations fail."""
    pass


class LatencyViolationError(HyperFabricError):
    """Raised when latency requirements cannot be met."""
    pass


class BandwidthExceededError(HyperFabricError):
    """Raised when bandwidth limits are exceeded."""
    pass


class FaultToleranceError(HyperFabricError):
    """Raised when fault tolerance mechanisms fail."""
    pass
