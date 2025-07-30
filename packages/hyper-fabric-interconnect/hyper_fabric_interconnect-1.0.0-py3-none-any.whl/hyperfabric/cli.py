"""
HyperFabric Interconnect CLI tool for diagnostics and management.
Licensed software requiring valid activation.
"""

import asyncio
import json
import time
import sys
from typing import Dict, Any, Optional
import click
from rich.console import Console
from rich.table import Table
from rich.tree import Tree
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax

from hyperfabric import (
    HyperFabricProtocol,
    NodeSignature,
    HardwareType,
    FabricZone,
    ZoneType,
    IsolationLevel,
    PacketPriority,
    DataType,
    LicenseError,
    get_machine_info,
)
from hyperfabric.licensing import LicenseValidator

console = Console()


def validate_cli_license():
    """Validate license for CLI usage."""
    try:
        validator = LicenseValidator()
        validator.validate_license(["core"])
        return True
    except LicenseError as e:
        machine_info = get_machine_info()
        console.print(f"""
[red]╔══════════════════════════════════════════════════════════════╗[/red]
[red]║                    HYPERFABRIC CLI ACCESS DENIED              ║[/red]
[red]╠══════════════════════════════════════════════════════════════╣[/red]
[red]║ Valid license required for CLI operations.                    ║[/red]
[red]║                                                              ║[/red]
[red]║ Machine ID: {machine_info['machine_id']}                              ║[/red]
[red]║ Contact: {machine_info['contact_email']}                    ║[/red]
[red]║                                                              ║[/red]
[red]║ Include your Machine ID when requesting license activation.   ║[/red]
[red]╚══════════════════════════════════════════════════════════════╝[/red]
""")
        sys.exit(1)


@click.group()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.pass_context
def cli(ctx, verbose):
    """HyperFabric Interconnect CLI - Ultra-low-latency fabric management."""
    # STRICT LICENSE VALIDATION - NO BYPASS
    validate_cli_license()
    
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose
    
    if verbose:
        console.print("[dim]HyperFabric CLI - Verbose mode enabled[/dim]")


@cli.command()
@click.argument('node_id')
@click.option('--timeout', '-t', default=1000, help='Timeout in milliseconds')
@click.option('--count', '-c', default=1, help='Number of pings to send')
@click.option('--source', '-s', help='Source node ID (if not specified, uses first available)')
@click.pass_context
def ping(ctx, node_id, timeout, count, source):
    """Ping a fabric node to test connectivity and latency."""
    asyncio.run(_ping_async(node_id, timeout, count, source, ctx.obj['verbose']))


async def _ping_async(node_id: str, timeout: int, count: int, source: Optional[str], verbose: bool):
    """Async ping implementation."""
    protocol = HyperFabricProtocol()
    
    try:
        # Create some demo nodes if none exist
        if not protocol.get_registered_nodes():
            await _create_demo_topology(protocol)
        
        nodes = protocol.get_registered_nodes()
        
        # Determine source node
        if not source:
            available_nodes = [nid for nid in nodes.keys() if nid != node_id]
            if not available_nodes:
                console.print(f"[red]No available source nodes found[/red]")
                return
            source = available_nodes[0]
        
        if source not in nodes:
            console.print(f"[red]Source node '{source}' not found[/red]")
            return
        
        if node_id not in nodes:
            console.print(f"[red]Target node '{node_id}' not found[/red]")
            return
        
        console.print(f"PING {node_id} from {source}")
        
        total_time = 0
        successful_pings = 0
        
        for i in range(count):
            try:
                result = await protocol.ping(source, node_id, timeout)
                
                if result['success']:
                    rtt_ms = result['rtt_ms']
                    total_time += rtt_ms
                    successful_pings += 1
                    
                    console.print(
                        f"Reply from {node_id}: time={rtt_ms:.2f}ms "
                        f"path={' -> '.join(result['path'])} "
                        f"throughput={result['throughput_gbps']:.1f}Gbps"
                    )
                else:
                    console.print(f"[red]Request timed out: {result['error']}[/red]")
                
                if i < count - 1:
                    await asyncio.sleep(1)
                    
            except Exception as e:
                console.print(f"[red]Ping failed: {e}[/red]")
        
        # Summary
        if successful_pings > 0:
            avg_time = total_time / successful_pings
            console.print(f"\nPing statistics for {node_id}:")
            console.print(f"    Packets: Sent = {count}, Received = {successful_pings}, Lost = {count - successful_pings}")
            console.print(f"Average round-trip time: {avg_time:.2f}ms")
        
    finally:
        await protocol.shutdown()


@cli.command()
@click.option('--format', '-f', type=click.Choice(['table', 'json', 'tree']), default='table', help='Output format')
@click.option('--zone', '-z', help='Filter by zone')
@click.pass_context
def topo(ctx, format, zone):
    """Display network topology information."""
    asyncio.run(_topo_async(format, zone, ctx.obj['verbose']))


async def _topo_async(format: str, zone_filter: Optional[str], verbose: bool):
    """Async topology display implementation."""
    protocol = HyperFabricProtocol()
    
    try:
        # Create demo topology if empty
        if not protocol.get_registered_nodes():
            await _create_demo_topology(protocol)
        
        topo_info = await protocol.get_topology_info()
        
        if format == 'json':
            console.print(json.dumps(topo_info, indent=2, default=str))
            
        elif format == 'tree':
            _display_topology_tree(topo_info, zone_filter)
            
        else:  # table format
            _display_topology_table(topo_info, zone_filter, verbose)
    
    finally:
        await protocol.shutdown()


def _display_topology_table(topo_info: Dict[str, Any], zone_filter: Optional[str], verbose: bool):
    """Display topology as tables."""
    # Nodes table
    nodes_table = Table(title="Fabric Nodes")
    nodes_table.add_column("Node ID", style="cyan")
    nodes_table.add_column("Hardware Type", style="green")
    nodes_table.add_column("Bandwidth", style="yellow")
    nodes_table.add_column("Latency", style="magenta")
    nodes_table.add_column("Load", style="red")
    nodes_table.add_column("Status", style="blue")
    
    topology_stats = topo_info.get('topology_stats', {})
    
    # This is a simplified display - in real implementation, you'd access actual node data
    console.print(f"[bold]Topology Overview[/bold]")
    console.print(f"Total Nodes: {topology_stats.get('total_nodes', 0)}")
    console.print(f"Total Zones: {topology_stats.get('total_zones', 0)}")
    console.print(f"Network Connected: {topology_stats.get('is_connected', False)}")
    
    if verbose:
        console.print(f"\n[bold]Performance Statistics[/bold]")
        perf_stats = topo_info.get('performance_stats', {})
        for key, value in perf_stats.items():
            console.print(f"{key}: {value}")


def _display_topology_tree(topo_info: Dict[str, Any], zone_filter: Optional[str]):
    """Display topology as a tree structure."""
    tree = Tree("🌐 HyperFabric Network")
    
    zones_node = tree.add("📦 Zones")
    nodes_node = tree.add("🖥️  Nodes")
    
    # Add zones
    topology_stats = topo_info.get('topology_stats', {})
    zones = topology_stats.get('zones', {})
    
    for zone_id, zone_data in zones.items():
        if zone_filter and zone_filter not in zone_id:
            continue
        
        zone_node = zones_node.add(f"🏢 {zone_id}")
        zone_node.add(f"Type: {zone_data.get('zone_type', 'unknown')}")
        zone_node.add(f"Nodes: {zone_data.get('node_count', 0)}")
        zone_node.add(f"Utilization: {zone_data.get('utilization', 0):.1f}%")
    
    console.print(tree)


@cli.command()
@click.option('--full', '-f', is_flag=True, help='Run full diagnostics')
@click.option('--output', '-o', help='Output file for results')
@click.pass_context
def diagnose(ctx, full, output):
    """Run fabric diagnostics and health checks."""
    asyncio.run(_diagnose_async(full, output, ctx.obj['verbose']))


async def _diagnose_async(full: bool, output: Optional[str], verbose: bool):
    """Async diagnostics implementation."""
    protocol = HyperFabricProtocol()
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            
            # Create demo topology for testing
            task1 = progress.add_task("Setting up test topology...", total=None)
            if not protocol.get_registered_nodes():
                await _create_demo_topology(protocol)
            progress.remove_task(task1)
            
            # Run basic diagnostics
            task2 = progress.add_task("Running basic diagnostics...", total=None)
            topo_info = await protocol.get_topology_info()
            progress.remove_task(task2)
            
            if full:
                # Run comprehensive tests
                task3 = progress.add_task("Running comprehensive tests...", total=None)
                optimization_result = await protocol.optimize_topology()
                progress.remove_task(task3)
            
        # Display results
        _display_diagnostics_results(topo_info, full, verbose)
        
        if output:
            with open(output, 'w') as f:
                json.dump(topo_info, f, indent=2, default=str)
            console.print(f"[green]Diagnostics saved to {output}[/green]")
    
    finally:
        await protocol.shutdown()


def _display_diagnostics_results(topo_info: Dict[str, Any], full: bool, verbose: bool):
    """Display diagnostics results."""
    # Health status panel
    topology_stats = topo_info.get('topology_stats', {})
    perf_stats = topo_info.get('performance_stats', {})
    
    health_status = "🟢 Healthy"
    if not topology_stats.get('is_connected', True):
        health_status = "🔴 Network Partitioned"
    elif perf_stats.get('failed_transfers', 0) > perf_stats.get('successful_transfers', 1) * 0.1:
        health_status = "🟡 Degraded"
    
    health_panel = Panel(
        f"[bold]Overall Health: {health_status}[/bold]\n"
        f"Uptime: {topo_info.get('uptime_seconds', 0):.1f}s\n"
        f"Active Transfers: {topo_info.get('active_transfers', 0)}\n"
        f"Protocol State: {topo_info.get('state', 'unknown')}",
        title="🔍 System Health",
        border_style="green"
    )
    console.print(health_panel)
    
    # Performance metrics
    if verbose or full:
        perf_table = Table(title="Performance Metrics")
        perf_table.add_column("Metric", style="cyan")
        perf_table.add_column("Value", style="yellow")
        
        for key, value in perf_stats.items():
            if isinstance(value, float):
                formatted_value = f"{value:.2f}"
            else:
                formatted_value = str(value)
            perf_table.add_row(key.replace('_', ' ').title(), formatted_value)
        
        console.print(perf_table)


@cli.command()
@click.argument('source')
@click.argument('destination')
@click.option('--size', '-s', default=1024, help='Data size in bytes')
@click.option('--priority', '-p', type=click.Choice(['ultra_high', 'high', 'normal', 'low']), default='normal')
@click.option('--quantum', '-q', is_flag=True, help='Require quantum entanglement')
@click.pass_context
def transfer(ctx, source, destination, size, priority, quantum):
    """Test data transfer between nodes."""
    asyncio.run(_transfer_async(source, destination, size, priority, quantum, ctx.obj['verbose']))


async def _transfer_async(source: str, destination: str, size: int, priority: str, quantum: bool, verbose: bool):
    """Async transfer test implementation."""
    protocol = HyperFabricProtocol()
    
    try:
        # Create demo topology if needed
        if not protocol.get_registered_nodes():
            await _create_demo_topology(protocol)
        
        nodes = protocol.get_registered_nodes()
        
        if source not in nodes:
            console.print(f"[red]Source node '{source}' not found[/red]")
            return
        
        if destination not in nodes:
            console.print(f"[red]Destination node '{destination}' not found[/red]")
            return
        
        # Create test data
        test_data = b'0' * size
        
        # Map priority string to enum
        priority_map = {
            'ultra_high': PacketPriority.ULTRA_HIGH,
            'high': PacketPriority.HIGH,
            'normal': PacketPriority.NORMAL,
            'low': PacketPriority.LOW,
        }
        
        console.print(f"Transferring {size} bytes from {source} to {destination}")
        if quantum:
            console.print("[cyan]Quantum entanglement required[/cyan]")
        
        start_time = time.time()
        
        try:
            result = await protocol.send_data(
                source=source,
                destination=destination,
                data=test_data,
                data_type=DataType.CUSTOM,
                priority=priority_map[priority],
                requires_quantum_entanglement=quantum,
            )
            
            end_time = time.time()
            
            if result.success:
                console.print(f"[green]✓ Transfer completed successfully[/green]")
                console.print(f"Bytes transferred: {result.bytes_transferred}")
                console.print(f"Actual latency: {result.actual_latency_ns / 1e6:.2f}ms")
                console.print(f"Throughput: {result.throughput_gbps:.2f} Gbps")
                console.print(f"Path: {' -> '.join(result.path_taken)}")
                console.print(f"Compression ratio: {result.compression_ratio:.2f}")
            else:
                console.print(f"[red]✗ Transfer failed: {result.error_message}[/red]")
        
        except Exception as e:
            console.print(f"[red]Transfer error: {e}[/red]")
    
    finally:
        await protocol.shutdown()


@cli.command()
@click.option('--export', '-e', help='Export topology to file')
@click.option('--import', '-i', 'import_file', help='Import topology from file')
@click.option('--format', '-f', type=click.Choice(['json', 'gml', 'graphml']), default='json')
@click.pass_context
def topology(ctx, export, import_file, format):
    """Import/export topology configurations."""
    asyncio.run(_topology_async(export, import_file, format, ctx.obj['verbose']))


async def _topology_async(export: Optional[str], import_file: Optional[str], format: str, verbose: bool):
    """Async topology import/export implementation."""
    protocol = HyperFabricProtocol()
    
    try:
        if import_file:
            # Import topology
            with open(import_file, 'r') as f:
                data = f.read()
            
            protocol.topology_manager.import_topology(data, format)
            console.print(f"[green]Topology imported from {import_file}[/green]")
        
        elif export:
            # Create demo topology if needed
            if not protocol.get_registered_nodes():
                await _create_demo_topology(protocol)
            
            # Export topology
            data = protocol.topology_manager.export_topology(format)
            
            with open(export, 'w') as f:
                f.write(data)
            
            console.print(f"[green]Topology exported to {export}[/green]")
        
        else:
            # Display current topology
            topo_info = await protocol.get_topology_info()
            console.print(json.dumps(topo_info, indent=2, default=str))
    
    finally:
        await protocol.shutdown()


async def _create_demo_topology(protocol: HyperFabricProtocol):
    """Create a demo topology for testing."""
    # Create diverse nodes representing different hardware types
    demo_nodes = [
        NodeSignature(
            node_id="gpu-cluster-01",
            hardware_type=HardwareType.NVIDIA_H100,
            bandwidth_gbps=400,
            latency_ns=100,
        ),
        NodeSignature(
            node_id="gpu-cluster-02",
            hardware_type=HardwareType.NVIDIA_A100,
            bandwidth_gbps=300,
            latency_ns=150,
        ),
        NodeSignature(
            node_id="qpu-fabric-01",
            hardware_type=HardwareType.QUANTUM_QPU,
            bandwidth_gbps=10,
            latency_ns=50,
            quantum_coherence_time_us=100.0,
        ),
        NodeSignature(
            node_id="photonic-switch-01",
            hardware_type=HardwareType.PHOTONIC_SWITCH,
            bandwidth_gbps=1000,
            latency_ns=10,
            photonic_channels=64,
        ),
        NodeSignature(
            node_id="neuromorphic-01",
            hardware_type=HardwareType.NEUROMORPHIC_CHIP,
            bandwidth_gbps=50,
            latency_ns=200,
            neuromorphic_neurons=1000000,
        ),
    ]
    
    # Register nodes
    for node in demo_nodes:
        protocol.register_node(node)
    
    # Wait a moment for auto-discovery
    await asyncio.sleep(0.1)


@cli.command()
@click.option('--node', '-n', help='Show details for specific node')
@click.pass_context
def nodes(ctx, node):
    """List and manage fabric nodes."""
    asyncio.run(_nodes_async(node, ctx.obj['verbose']))


async def _nodes_async(node_filter: Optional[str], verbose: bool):
    """Async nodes listing implementation."""
    protocol = HyperFabricProtocol()
    
    try:
        # Create demo topology if needed
        if not protocol.get_registered_nodes():
            await _create_demo_topology(protocol)
        
        nodes = protocol.get_registered_nodes()
        
        if node_filter:
            # Show specific node details
            if node_filter in nodes:
                node = nodes[node_filter]
                _display_node_details(node, verbose)
            else:
                console.print(f"[red]Node '{node_filter}' not found[/red]")
        else:
            # List all nodes
            _display_nodes_table(nodes, verbose)
    
    finally:
        await protocol.shutdown()


def _display_nodes_table(nodes: Dict[str, NodeSignature], verbose: bool):
    """Display nodes in a table format."""
    table = Table(title="Fabric Nodes")
    table.add_column("Node ID", style="cyan")
    table.add_column("Hardware", style="green")
    table.add_column("Bandwidth", style="yellow")
    table.add_column("Latency", style="magenta")
    table.add_column("Status", style="blue")
    
    if verbose:
        table.add_column("Memory", style="orange")
        table.add_column("Compute Units", style="purple")
        table.add_column("Special Features", style="dim")
    
    for node_id, node in nodes.items():
        status = "🟢 Active" if node.is_active and node.is_healthy else "🔴 Inactive"
        
        row = [
            node_id,
            node.hardware_type.value,
            f"{node.bandwidth_gbps:.0f} Gbps",
            f"{node.latency_ns} ns",
            status,
        ]
        
        if verbose:
            features = []
            if node.is_quantum_capable():
                features.append("🔬 Quantum")
            if node.is_photonic_capable():
                features.append("💡 Photonic")
            if node.is_neuromorphic_capable():
                features.append("🧠 Neuromorphic")
            
            row.extend([
                f"{node.memory_gb:.1f} GB",
                f"{node.compute_units:,}",
                " ".join(features) if features else "-",
            ])
        
        table.add_row(*row)
    
    console.print(table)


def _display_node_details(node: NodeSignature, verbose: bool):
    """Display detailed information about a specific node."""
    details = f"""
[bold cyan]{node.node_id}[/bold cyan]
Hardware Type: {node.hardware_type.value}
Bandwidth: {node.bandwidth_gbps} Gbps
Latency: {node.latency_ns} ns
Memory: {node.memory_gb} GB
Compute Units: {node.compute_units:,}
Load: {node.load_percentage:.1f}%
Status: {'🟢 Healthy' if node.is_healthy else '🔴 Unhealthy'}
Active: {'Yes' if node.is_active else 'No'}
"""
    
    if node.is_quantum_capable():
        details += f"Quantum Coherence: {node.quantum_coherence_time_us} μs\n"
    
    if node.is_photonic_capable():
        details += f"Photonic Channels: {node.photonic_channels}\n"
    
    if node.is_neuromorphic_capable():
        details += f"Neuromorphic Neurons: {node.neuromorphic_neurons:,}\n"
    
    if verbose:
        details += f"""
UUID: {node.uuid}
Registration Time: {time.ctime(node.registration_time)}
Last Heartbeat: {time.ctime(node.last_heartbeat)}
Physical Location: {node.physical_location or 'Unknown'}
Temperature: {node.temperature_c}°C
"""
    
    panel = Panel(details.strip(), title=f"Node Details: {node.node_id}", border_style="cyan")
    console.print(panel)


@cli.command()
@click.pass_context
def license(ctx):
    """Display license information and machine ID for activation."""
    from hyperfabric.licensing import LicenseValidator
    
    validator = LicenseValidator()
    machine_info = get_machine_info()
    
    # Check if license is valid
    try:
        validator.validate_license(["core"])
        license_status = "[green]✓ VALID[/green]"
        
        # Try to get additional license info
        try:
            validator.validate_license(["professional"])
            license_tier = "[blue]Professional[/blue]"
        except LicenseError:
            try:
                validator.validate_license(["enterprise"])
                license_tier = "[magenta]Enterprise[/magenta]"
            except LicenseError:
                license_tier = "[green]Basic[/green]"
    
    except LicenseError:
        license_status = "[red]✗ INVALID/MISSING[/red]"
        license_tier = "[red]Unlicensed[/red]"
    
    # Create license information panel
    license_info = f"""
[bold]License Status:[/bold] {license_status}
[bold]License Tier:[/bold] {license_tier}

[bold]Machine Information:[/bold]
Machine ID: [cyan]{machine_info['machine_id']}[/cyan]
Hostname: {machine_info['hostname']}
Platform: {machine_info['platform']}
Architecture: {machine_info['architecture']}

[bold]Licensing Contact:[/bold]
Email: [yellow]{machine_info['contact_email']}[/yellow]

[dim]Include your Machine ID when requesting license activation.[/dim]
"""
    
    panel = Panel(
        license_info.strip(),
        title="HyperFabric License Information",
        border_style="blue"
    )
    console.print(panel)
    
    # Show feature availability
    features_table = Table(title="Feature Availability")
    features_table.add_column("Feature", style="cyan")
    features_table.add_column("Status", justify="center")
    features_table.add_column("Required Tier", style="dim")
    
    # Check each feature tier
    features = [
        ("Core Operations", ["core"], "Basic"),
        ("Advanced Routing", ["professional"], "Professional"),
        ("Quantum Integration", ["professional"], "Professional"),
        ("Enterprise Management", ["enterprise"], "Enterprise"),
        ("Multi-Fabric Orchestration", ["enterprise"], "Enterprise"),
    ]
    
    for feature_name, required_features, tier in features:
        try:
            validator.validate_license(required_features)
            status = "[green]✓ Available[/green]"
        except LicenseError:
            status = "[red]✗ Unavailable[/red]"
        
        features_table.add_row(feature_name, status, tier)
    
    console.print()
    console.print(features_table)


def main():
    """Main CLI entry point."""
    try:
        cli()
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


if __name__ == '__main__':
    main()
