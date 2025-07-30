# 🖥️ CLI Reference

Complete command-line interface reference for HyperFabric Interconnect management.

## Installation

The CLI is automatically installed with the package:

```bash
pip install hyper-fabric-interconnect
```

After installation, the `hfabric` command will be available globally.

## Global Options

All commands support these global options:

```bash
hfabric [OPTIONS] COMMAND [ARGS]...
```

**Global Options:**

- `--verbose, -v`: Enable verbose output
- `--quiet, -q`: Suppress non-error output  
- `--config FILE`: Specify configuration file path
- `--help`: Show help message and exit

## Commands Overview

| Command | Description |
|---------|-------------|
| [`ping`](#hfabric-ping) | Test connectivity between fabric nodes |
| [`topo`](#hfabric-topo) | Display fabric topology information |
| [`diagnose`](#hfabric-diagnose) | Run comprehensive fabric diagnostics |
| [`transfer`](#hfabric-transfer) | Perform data transfer operations |
| [`nodes`](#hfabric-nodes) | Manage fabric nodes |
| [`zones`](#hfabric-zones) | Manage fabric zones |
| [`monitor`](#hfabric-monitor) | Real-time fabric monitoring |
| [`config`](#hfabric-config) | Configuration management |
| [`license`](#hfabric-license) | License information and machine ID |

---

## hfabric ping

Test connectivity and measure performance between fabric nodes.

### Syntax

```bash
hfabric ping [OPTIONS] SOURCE DESTINATION
```

### Arguments

- `SOURCE`: Source node ID
- `DESTINATION`: Destination node ID

### Options

- `--count, -c INTEGER`: Number of ping packets to send (default: 4)
- `--size, -s INTEGER`: Packet size in bytes (default: 64)
- `--timeout, -t INTEGER`: Timeout in milliseconds (default: 5000)
- `--interval, -i FLOAT`: Interval between pings in seconds (default: 1.0)
- `--quantum`: Enable quantum-optimized ping
- `--detailed`: Show detailed routing information
- `--json`: Output results in JSON format

### Examples

**Basic connectivity test:**

```bash
hfabric ping gpu-cluster-01 storage-array-01
```

**High-frequency latency measurement:**

```bash
hfabric ping --count 100 --interval 0.1 gpu-01 gpu-02
```

**Quantum-optimized ping:**

```bash
hfabric ping --quantum qpu-ibm-01 qpu-google-01
```

**Large packet test:**

```bash
hfabric ping --size 1500 --count 10 edge-server-nyc edge-server-sfo
```

### Output

```
PING from gpu-cluster-01 to storage-array-01
64 bytes from storage-array-01: time=0.123ms path=[gpu-cluster-01, switch-01, storage-array-01]
64 bytes from storage-array-01: time=0.119ms path=[gpu-cluster-01, switch-01, storage-array-01]
64 bytes from storage-array-01: time=0.125ms path=[gpu-cluster-01, switch-01, storage-array-01]
64 bytes from storage-array-01: time=0.121ms path=[gpu-cluster-01, switch-01, storage-array-01]

--- storage-array-01 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss
min/avg/max/stddev = 0.119/0.122/0.125/0.002 ms
```

---

## hfabric topo

Display and analyze fabric topology information.

### Syntax

```bash
hfabric topo [OPTIONS] [COMMAND]
```

### Subcommands

#### show

Display topology overview:

```bash
hfabric topo show [OPTIONS]
```

**Options:**

- `--format FORMAT`: Output format (table, json, yaml, graph) (default: table)
- `--filter TYPE`: Filter by node type (gpu, quantum, neuromorphic, storage)
- `--zone ZONE_ID`: Show only nodes in specified zone
- `--detailed`: Include detailed node specifications

#### analyze

Analyze topology for bottlenecks:

```bash

hfabric topo analyze [OPTIONS]
```

**Options:**

- `--threshold FLOAT`: Bottleneck severity threshold (0.0-1.0) (default: 0.7)
- `--recommendations`: Include optimization recommendations

#### path

Show routing path between nodes:

```bash
hfabric topo path [OPTIONS] SOURCE DESTINATION
```

**Options:**

- `--algorithm ALGO`: Routing algorithm (shortest, fastest, balanced) (default: optimal)
- `--constraints`: Show latency and bandwidth constraints

### Examples

**Basic topology overview:**

```bash
hfabric topo show
```

**Detailed GPU nodes only:**

```bash
hfabric topo show --filter gpu --detailed
```

**Topology as visual graph:**

```bash
hfabric topo show --format graph
```

**Analyze bottlenecks:**

```bash
hfabric topo analyze --recommendations
```

**Show optimal path:**

```bash
hfabric topo path gpu-01 storage-01 --constraints
```

### Output Examples

**Table format:**
```
┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┓
┃ Node ID           ┃ Hardware Type     ┃ Bandwidth     ┃ Latency     ┃ Zone              ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━┩
│ gpu-cluster-01    │ NVIDIA_H100       │ 400.0 Gbps   │ 100 ns     │ ai-training       │
│ qpu-ibm-01        │ QUANTUM_QPU       │ 10.0 Gbps    │ 50 ns      │ quantum-realm     │
│ neuromorphic-01   │ NEUROMORPHIC_CHIP │ 50.0 Gbps    │ 80 ns      │ edge-processing   │
└───────────────────┴───────────────────┴───────────────┴─────────────┴───────────────────┘
```

---

## hfabric diagnose

Run comprehensive diagnostics on the fabric infrastructure.

### Syntax

```bash
hfabric diagnose [OPTIONS] [TARGET]
```

### Arguments

- `TARGET`: Specific node, zone, or 'all' for full fabric (default: all)

### Options

- `--tests TESTS`: Comma-separated list of test types
  - `connectivity`: Node connectivity tests
  - `performance`: Bandwidth and latency tests
  - `quantum`: Quantum coherence and fidelity tests
  - `security`: Security and encryption tests
  - `all`: Run all test types (default)
- `--concurrency INTEGER`: Number of concurrent test threads (default: 10)
- `--duration INTEGER`: Test duration in seconds (default: 30)
- `--output FILE`: Save detailed results to file
- `--format FORMAT`: Output format (table, json, report) (default: table)

### Examples

**Full fabric diagnostics:**

```bash
hfabric diagnose
```

**Specific node performance test:**

```bash
hfabric diagnose gpu-cluster-01 --tests performance --duration 60
```

**Quantum zone diagnostics:**

```bash
hfabric diagnose quantum-realm --tests quantum,connectivity
```

**High-concurrency stress test:**

```bash
hfabric diagnose --concurrency 50 --duration 300 --output stress-test.json
```

### Output

```
🔍 HyperFabric Diagnostics Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Overall Health: ✅ EXCELLENT (98.7%)

🔗 Connectivity Tests
  ✅ All nodes reachable: 42/42 nodes
  ✅ Inter-zone connectivity: 100% success rate
  ⚠️  High latency path detected: gpu-01 → storage-remote (15ms)

⚡ Performance Tests  
  ✅ Bandwidth utilization: 87.3% average
  ✅ Latency targets met: 95.2% of paths < 1ms
  ✅ Zero packet loss on critical paths

🔬 Quantum Tests
  ✅ Quantum coherence: 99.9% fidelity maintained
  ✅ Entanglement preservation: 8/8 QPU pairs
  ⚠️  Coherence time degradation on qpu-03: 85μs (target: 100μs)

🔒 Security Tests
  ✅ Encryption operational: All secure zones
  ✅ Quantum key distribution: Active on 4 channels
  ✅ No unauthorized access attempts detected

📋 Recommendations:
  • Optimize routing for gpu-01 → storage-remote path
  • Schedule maintenance for qpu-03 coherence optimization
  • Consider adding redundant links in ai-training zone
```

---

## hfabric transfer

Perform data transfer operations between fabric nodes.

### Syntax

```bash
hfabric transfer [OPTIONS] SOURCE DESTINATION
```

### Arguments

- `SOURCE`: Source node ID or file path
- `DESTINATION`: Destination node ID or file path

### Options

- `--data-type TYPE`: Data type (tensor, parameter, quantum_state, generic) (default: generic)
- `--priority PRIORITY`: Transfer priority (ultra_high, high, medium, low, bulk) (default: medium)
- `--size SIZE`: Transfer size (supports K, M, G, T suffixes)
- `--compression`: Enable data compression
- `--encryption`: Enable data encryption
- `--verify`: Verify transfer integrity
- `--latency-constraint TIME`: Maximum latency constraint (e.g., 1ms, 500us, 100ns)
- `--bandwidth-min BANDWIDTH`: Minimum bandwidth requirement
- `--quantum-entangled`: Require quantum entanglement preservation
- `--progress`: Show transfer progress
- `--benchmark`: Run transfer benchmark

### Examples

**Simple data transfer:**
```bash
hfabric transfer gpu-01 storage-01 --size 1GB --progress
```

**High-priority AI model transfer:**
```bash
hfabric transfer model-server gpu-cluster-01 \
  --data-type parameter \
  --priority high \
  --compression \
  --verify
```

**Quantum state transfer:**
```bash
hfabric transfer qpu-01 qpu-02 \
  --data-type quantum_state \
  --quantum-entangled \
  --latency-constraint 100us
```

**Bulk data migration:**
```bash
hfabric transfer old-storage new-storage \
  --size 10TB \
  --priority bulk \
  --compression \
  --benchmark
```

### Output

```
🚀 Data Transfer Operation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Source: gpu-01
Destination: storage-01
Data Type: parameter
Size: 1.00 GB
Priority: high

🛣️  Route: gpu-01 → switch-spine-01 → storage-01
⚡ Estimated Time: 2.1 seconds
📊 Bandwidth: 400.0 Gbps

Progress: ████████████████████████████████████████ 100% │ 1.00 GB │ 1.95s

✅ Transfer completed successfully
📈 Performance Metrics:
  • Actual time: 1.95s (7% faster than estimated)
  • Average bandwidth: 415.3 Gbps (103.8% utilization)
  • Peak bandwidth: 425.7 Gbps
  • Latency: 125ns average
  • Zero packet loss
  • Compression ratio: 2.3:1
```

---

## hfabric nodes

Manage fabric nodes (registration, removal, status).

### Syntax

```bash
hfabric nodes [OPTIONS] COMMAND [ARGS]...
```

### Subcommands

#### list

List all registered nodes:

```bash
hfabric nodes list [OPTIONS]
```

**Options:**

- `--filter TYPE`: Filter by hardware type
- `--zone ZONE_ID`: Filter by zone
- `--status STATUS`: Filter by status (online, offline, degraded)
- `--format FORMAT`: Output format (table, json, yaml)

#### register

Register a new node:

```bash
hfabric nodes register [OPTIONS] NODE_ID
```

**Options:**

- `--hardware-type TYPE`: Hardware type (required)
- `--bandwidth BANDWIDTH`: Bandwidth capacity in Gbps (required)
- `--latency LATENCY`: Base latency in nanoseconds (required)
- `--memory MEMORY`: Memory capacity in GB
- `--location LOCATION`: Physical location
- `--zone ZONE_ID`: Assign to zone
- `--quantum-coherence TIME`: Quantum coherence time in microseconds
- `--config FILE`: Load configuration from file

#### remove

Remove a node:

```bash
hfabric nodes remove [OPTIONS] NODE_ID
```

**Options:**

- `--force`: Force removal even if node is active
- `--migrate-data`: Migrate data before removal

#### status

Show detailed node status:

```bash
hfabric nodes status [OPTIONS] NODE_ID
```

**Options:**

- `--metrics`: Include performance metrics
- `--history`: Show historical performance data

### Examples

**List all nodes:**

```bash
hfabric nodes list
```

**List quantum nodes only:**

```bash
hfabric nodes list --filter quantum_qpu
```

**Register new GPU node:**

```bash
hfabric nodes register gpu-new-01 \
  --hardware-type nvidia_h100 \
  --bandwidth 400 \
  --latency 100 \
  --memory 80 \
  --location "Rack-15-Slot-3"
```

**Register quantum node:**

```bash
hfabric nodes register qpu-new-01 \
  --hardware-type quantum_qpu \
  --bandwidth 10 \
  --latency 50 \
  --quantum-coherence 150 \
  --zone quantum-realm
```

**Remove node safely:**.

```bash
hfabric nodes remove old-gpu-01 --migrate-data
```

**Detailed node status:**

```bash
hfabric nodes status gpu-cluster-01 --metrics --history
```

---

## hfabric zones

Manage fabric zones for network segmentation and optimization.

### Syntax

```bash
hfabric zones [OPTIONS] COMMAND [ARGS]...
```

### Subcommands

#### list

List all zones:

```bash
hfabric zones list [OPTIONS]
```

#### create

Create a new zone:

```bash
hfabric zones create [OPTIONS] ZONE_ID
```

**Options:**

- `--type TYPE`: Zone type (compute_cluster, inference_farm, quantum_realm, etc.)
- `--isolation LEVEL`: Isolation level (none, low, medium, high, quantum_secure)
- `--max-nodes INTEGER`: Maximum nodes in zone
- `--bandwidth BANDWIDTH`: Required bandwidth in Gbps
- `--description TEXT`: Zone description

#### delete

Delete a zone:

```bash
hfabric zones delete [OPTIONS] ZONE_ID
```

#### assign

Assign node to zone:

```bash
hfabric zones assign [OPTIONS] ZONE_ID NODE_ID
```

#### remove

Remove node from zone:

```bash
hfabric zones remove [OPTIONS] ZONE_ID NODE_ID
```

### Examples

**Create AI training zone:**

```bash
hfabric zones create ai-training-cluster \
  --type compute_cluster \
  --isolation medium \
  --max-nodes 1000 \
  --bandwidth 400 \
  --description "Large-scale AI training cluster"
```

**Create quantum processing zone:**

```bash
hfabric zones create quantum-lab \
  --type quantum_realm \
  --isolation quantum_secure \
  --max-nodes 20 \
  --bandwidth 50
```

**Assign node to zone:**

```bash
hfabric zones assign ai-training-cluster gpu-cluster-01
```

---

## hfabric monitor

Real-time monitoring of fabric performance and health.

### Syntax

```bash
hfabric monitor [OPTIONS] [TARGET]
```

### Arguments

- `TARGET`: Specific node, zone, or 'all' for full fabric (default: all)

### Options

- `--refresh SECONDS`: Refresh interval in seconds (default: 1)
- `--metrics METRICS`: Comma-separated metrics to display
  - `latency`: Inter-node latency
  - `bandwidth`: Bandwidth utilization
  - `throughput`: Data throughput
  - `quantum`: Quantum coherence metrics
  - `errors`: Error rates
  - `all`: All available metrics (default)
- `--threshold FLOAT`: Alert threshold for anomalies
- `--export FILE`: Export metrics to file
- `--dashboard`: Launch web dashboard

### Examples

**Real-time fabric monitoring:**
```bash
hfabric monitor
```

**Monitor specific zone:**
```bash
hfabric monitor quantum-realm --refresh 0.5
```

**Monitor bandwidth only:**
```bash
hfabric monitor --metrics bandwidth,throughput
```

**Launch web dashboard:**
```bash
hfabric monitor --dashboard
```

### Output

```
🌐 HyperFabric Real-Time Monitor                                     [2024-01-15 14:23:45]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Overall Status: ✅ HEALTHY
🔗 Active Connections: 1,247
⚡ Total Throughput: 2.3 TB/s
🔬 Quantum Coherence: 99.7%

┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┓
┃ Node              ┃ Latency      ┃ Bandwidth    ┃ Throughput   ┃ Status            ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━┩
│ gpu-cluster-01    │ 0.12ms ▲ 5% │ 387.2 Gbps  │ 1.2 TB/s ▲   │ ✅ Excellent     │
│ qpu-ibm-01        │ 0.05ms ▼ 2% │ 9.8 Gbps    │ 45.3 GB/s    │ ✅ Optimal       │
│ storage-tier-01   │ 0.31ms       │ 156.7 Gbps  │ 891.2 GB/s   │ ⚠️  High Load    │
│ edge-server-nyc   │ 2.15ms ▲12% │ 45.2 Gbps   │ 123.4 GB/s   │ ⚠️  Degraded     │
└───────────────────┴──────────────┴──────────────┴──────────────┴───────────────────┘

🚨 Alerts:
  • High latency detected: edge-server-nyc (2.15ms > 1ms threshold)
  • Storage tier approaching capacity: 87.3% utilization

Press 'q' to quit, 'r' to refresh, 'd' for detailed view
```

---

## hfabric config

Configuration management for fabric settings.

### Syntax

```bash
hfabric config [OPTIONS] COMMAND [ARGS]...
```

### Subcommands

#### show

Display current configuration:

```bash
hfabric config show [OPTIONS]
```

#### set

Set configuration value:

```bash
hfabric config set [OPTIONS] KEY VALUE
```

#### get
Get configuration value:
```bash
hfabric config get [OPTIONS] KEY
```

#### reset
Reset configuration to defaults:
```bash
hfabric config reset [OPTIONS]
```

#### export
Export configuration to file:
```bash
hfabric config export [OPTIONS] FILE
```

#### import
Import configuration from file:
```bash
hfabric config import [OPTIONS] FILE
```

### Configuration Keys

| Key | Description | Default |
|-----|-------------|---------|
| `fabric.default_latency_constraint_ns` | Default latency constraint | `1000000` |
| `fabric.enable_ml_routing` | Enable ML-based routing | `false` |
| `fabric.enable_quantum_optimization` | Enable quantum optimizations | `false` |
| `fabric.buffer_pool_size` | Buffer pool size | `1000` |
| `fabric.max_packet_size` | Maximum packet size | `65536` |
| `routing.algorithm` | Default routing algorithm | `optimal` |
| `monitoring.refresh_interval_s` | Monitoring refresh interval | `1` |
| `quantum.coherence_threshold_us` | Quantum coherence threshold | `10.0` |
| `security.encryption_enabled` | Enable encryption by default | `false` |

### Examples

**Show all configuration:**
```bash
hfabric config show
```

**Enable ML routing:**
```bash
hfabric config set fabric.enable_ml_routing true
```

**Set default latency constraint:**
```bash
hfabric config set fabric.default_latency_constraint_ns 500000
```

**Export configuration:**
```bash
hfabric config export production-config.yaml
```

**Reset to defaults:**
```bash
hfabric config reset --confirm
```

---

## Environment Variables

The CLI respects these environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `HFABRIC_CONFIG_FILE` | Default configuration file | `~/.hfabric/config.yaml` |
| `HFABRIC_LOG_LEVEL` | Logging level | `INFO` |
| `HFABRIC_ENDPOINT` | Fabric endpoint URL | `localhost:8080` |
| `HFABRIC_API_KEY` | API authentication key | None |
| `HFABRIC_TIMEOUT` | Default operation timeout | `30s` |

## Configuration File

Default configuration file location: `~/.hfabric/config.yaml`

Example configuration:

```yaml
fabric:
  default_latency_constraint_ns: 1000000
  enable_ml_routing: false
  enable_quantum_optimization: false
  buffer_pool_size: 1000
  max_packet_size: 65536

routing:
  algorithm: optimal
  load_balancing: true
  fault_tolerance: true

monitoring:
  refresh_interval_s: 1
  enable_alerts: true
  alert_threshold: 0.8

quantum:
  coherence_threshold_us: 10.0
  enable_entanglement: true
  error_correction: true

security:
  encryption_enabled: false
  quantum_key_distribution: false
  
logging:
  level: INFO
  file: ~/.hfabric/logs/hfabric.log
  max_size_mb: 100
```

## Exit Codes

| Code | Description |
|------|-------------|
| 0 | Success |
| 1 | General error |
| 2 | Invalid arguments |
| 3 | Connection error |
| 4 | Authentication error |
| 5 | Permission denied |
| 10 | Node not found |
| 11 | Route not found |
| 12 | Latency constraint violation |
| 20 | Quantum error |
| 21 | Coherence lost |
| 30 | Buffer error |
| 40 | Configuration error |

This comprehensive CLI reference enables complete management of HyperFabric Interconnect infrastructure through the command line interface.
