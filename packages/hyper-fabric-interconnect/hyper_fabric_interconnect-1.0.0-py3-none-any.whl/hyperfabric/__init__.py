"""
HyperFabric Interconnect: Breakthrough protocol architecture for ultra-low-latency, 
high-bandwidth interconnects powering AI superclusters and quantum simulation networks.

Licensed software - Valid license required for operation.
Contact: bajpaikrishna715@gmail.com
"""

__version__ = "0.1.0"
__author__ = "Krishna Bajpai"
__email__ = "bajpaikrishna715@gmail.com"
__license__ = "Commercial - Licensed Software"

# Import licensing system FIRST
from .licensing import validate_package_license, get_machine_info, LicenseError

# Validate package license on import
_license_valid = validate_package_license()

if not _license_valid:
    machine_info = get_machine_info()
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                    HYPERFABRIC IMPORT NOTICE                  ║
╠══════════════════════════════════════════════════════════════╣
║ This is licensed software requiring activation.               ║
║                                                              ║
║ Machine ID: {machine_info['machine_id']}                              ║
║ Contact: {machine_info['contact_email']}                    ║
║                                                              ║
║ Functionality will be restricted until licensed.             ║
╚══════════════════════════════════════════════════════════════╝
""")

from .protocol import HyperFabricProtocol
from .nodes import NodeSignature, HardwareType
from .routing import RoutingEngine, RoutingStrategy
from .buffers import ZeroCopyBuffer, BufferManager
from .topology import TopologyManager, FabricZone
from .exceptions import (
    HyperFabricError,
    NodeNotFoundError,
    RoutingError,
    BufferError,
    TopologyError,
)

try:
    from ._version import version as __version__
except ImportError:
    __version__ = "0.1.0"

__all__ = [
    "HyperFabricProtocol",
    "NodeSignature",
    "HardwareType",
    "RoutingEngine",
    "RoutingStrategy",
    "ZeroCopyBuffer",
    "BufferManager",
    "TopologyManager",
    "FabricZone",
    "HyperFabricError",
    "NodeNotFoundError",
    "RoutingError",
    "BufferError",
    "TopologyError",
    "LicenseError",
    "get_machine_info",
    "__version__",
]
