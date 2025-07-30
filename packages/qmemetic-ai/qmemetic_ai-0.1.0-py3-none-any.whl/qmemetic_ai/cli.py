"""
Command Line Interface for Q-Memetic AI.

🔐 STRICT LICENSING: QuantumMeta license required for all operations
Grace Period: 24 hours only
Support: bajpaikrishna715@gmail.com

Provides comprehensive CLI tools for researchers, operators, and developers
to interact with the memetic system.
"""

import asyncio
import json
import os
import sys
import time
from pathlib import Path
from typing import List, Optional, Dict, Any

import click
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.syntax import Syntax
from rich import print as rprint

# Import Q-Memetic AI modules
from .core.engine import MemeticEngine
from .core.meme import Meme, MemeMetadata
from .licensing.manager import (
    LicenseManager, 
    QMemeticLicenseError,
    validate_qmemetic_license
)
from .visualization.noosphere import NoosphereVisualizer


console = Console()


def print_banner():
    """Print Q-Memetic AI banner with license notice."""
    banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                              Q-Memetic AI                                     ║
║                   Quantum-Inspired Memetic Computing                          ║
║                                                                              ║
║                "Not just an algorithm. A mind-layer for civilization."       ║
║                                                                              ║
║  🔐 LICENSED SOFTWARE - QuantumMeta License Required                         ║
║     Grace Period: 24 hours | Support: bajpaikrishna715@gmail.com             ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """
    rprint(f"[bold cyan]{banner}[/bold cyan]")


def handle_license_error(func):
    """Decorator to handle license errors gracefully with user guidance."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except QMemeticLicenseError as e:
            console.print("\n[red]🔒 Q-MEMETIC AI LICENSE REQUIRED[/red]")
            console.print("=" * 60)
            console.print(f"[red]{e}[/red]")
            console.print("\n[yellow]Quick Actions:[/yellow]")
            console.print("1. Get license: [blue]https://krish567366.github.io/license-server/[/blue]")
            console.print("2. Email support: [blue]bajpaikrishna715@gmail.com[/blue]")
            console.print("3. Set license key: [blue]export QMEMETIC_LICENSE_KEY=your-key[/blue]")
            console.print("=" * 60)
            sys.exit(1)
        except Exception as e:
            console.print(f"[red]Error:[/red] {e}")
            sys.exit(1)
    return wrapper


@click.group()
@click.version_option(version="0.1.0")
@click.option('--license-key', envvar='QMEMETIC_LICENSE_KEY', help='QuantumMeta license key (REQUIRED)')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.pass_context
def main(ctx, license_key, verbose):
    """
    Q-Memetic AI: Quantum-Inspired Memetic Computing System.
    
    🔐 STRICT LICENSING: QuantumMeta license required for all operations
    Grace Period: 24 hours only
    """
    # Ensure context dict exists
    ctx.ensure_object(dict)
    
    # Store global configuration
    ctx.obj['license_key'] = license_key
    ctx.obj['verbose'] = verbose
    
    if verbose:
        import logging
        logging.basicConfig(level=logging.DEBUG)
    
    # Print banner if not in script mode
    if not ctx.obj.get('script_mode', False):
        print_banner()
    
    # Validate license immediately
    try:
        validate_qmemetic_license()
        console.print("[green]✅ License validated successfully[/green]")
    except QMemeticLicenseError as e:
        console.print("\n[red]🔒 Q-MEMETIC AI LICENSE VALIDATION FAILED[/red]")
        console.print("=" * 60)
        console.print(f"[red]{e}[/red]")
        console.print("=" * 60)
        if not license_key:
            console.print("\n[yellow]💡 TIP: Set license key with --license-key or QMEMETIC_LICENSE_KEY[/yellow]")
        sys.exit(1)


@main.command()
@click.option('--input', '-i', required=True, help='Input file or text to evolve')
@click.option('--generations', '-g', default=5, help='Number of evolution generations')
@click.option('--population', '-p', default=20, help='Population size for evolution')
@click.option('--output', '-o', help='Output file for evolved memes')
@click.option('--visualize', is_flag=True, help='Create evolution visualization')
@click.pass_context
@handle_license_error
def evolve(ctx, input, generations, population, output, visualize):
    """Evolve memes using genetic algorithms."""
    console.print(f"[bold green]Starting meme evolution...[/bold green]")
    
    # Initialize engine
    with console.status("[spinner]Initializing Q-Memetic AI Engine..."):
        engine = MemeticEngine(
            license_key=ctx.obj['license_key']
        )
    
    # Load or create initial memes
    with console.status("[spinner]Loading initial memes..."):
        if os.path.isfile(input):
            with open(input, 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            content = input
        
        # Create initial meme
        initial_meme = engine.create_meme(
            content=content,
            author="cli_user",
            domain="evolution"
        )
    
    # Run evolution
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task(f"Evolving over {generations} generations...", total=1)
        
        evolved_memes = engine.evolve(
            memes=[initial_meme],
            generations=generations,
            population_size=population
        )
        
        progress.update(task, completed=1)
    
    # Display results
    console.print(f"[bold green]Evolution complete![/bold green] Generated {len(evolved_memes)} memes.")
    
    # Show top memes
    sorted_memes = sorted(
        evolved_memes, 
        key=lambda m: m.vector.fitness_score if m.vector else 0, 
        reverse=True
    )
    
    table = Table(title="Top Evolved Memes")
    table.add_column("Rank", style="cyan")
    table.add_column("Fitness", style="green")
    table.add_column("Generation", style="yellow")
    table.add_column("Content", style="white")
    
    for i, meme in enumerate(sorted_memes[:10]):
        fitness = meme.vector.fitness_score if meme.vector else 0
        generation = meme.metadata.generation
        content = meme.content[:80] + "..." if len(meme.content) > 80 else meme.content
        
        table.add_row(str(i+1), f"{fitness:.3f}", str(generation), content)
    
    console.print(table)
    
    # Save output
    if output:
        output_data = {
            "evolved_memes": [meme.to_dict() for meme in evolved_memes],
            "evolution_config": {
                "generations": generations,
                "population_size": population,
                "initial_content": content
            }
        }
        
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        console.print(f"[green]Results saved to:[/green] {output}")
    
    # Create visualization
    if visualize:
        with console.status("[spinner]Creating evolution visualization..."):
            viz_path = engine.visualizer.create_evolution_timeline(
                [meme.to_dict() for meme in evolved_memes]
            )
        
        console.print(f"[green]Visualization saved to:[/green] {viz_path}")


@main.command()
@click.option('--node-id', help='Specific node to sync with')
@click.option('--mode', default='bidirectional', type=click.Choice(['push', 'pull', 'bidirectional']), help='Sync mode')
@click.option('--timeout', default=30, help='Sync timeout in seconds')
@click.pass_context
@handle_license_error
def sync(ctx, node_id, mode, timeout):
    """Sync with federated memetic network."""
    console.print(f"[bold blue]Starting federated sync...[/bold blue]")
    
    # Initialize engine with federation
    with console.status("[spinner]Connecting to federated network..."):
        engine = MemeticEngine(
            license_key=ctx.obj['license_key'],
            federated_mode=True
        )
    
    # Perform sync
    async def run_sync():
        with console.status(f"[spinner]Syncing with network (mode: {mode})..."):
            results = await engine.federated_sync(node_id=node_id, sync_mode=mode)
        return results
    
    try:
        results = asyncio.run(asyncio.wait_for(run_sync(), timeout=timeout))
        
        # Display results
        console.print(f"[green]Sync completed successfully![/green]")
        
        table = Table(title="Sync Results")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="white")
        
        table.add_row("Nodes Contacted", str(results.get('nodes_contacted', 0)))
        table.add_row("Memes Sent", str(results.get('total_sent', 0)))
        table.add_row("Memes Received", str(results.get('total_received', 0)))
        table.add_row("Errors", str(len(results.get('errors', []))))
        
        console.print(table)
        
        if results.get('errors'):
            console.print("[yellow]Errors encountered:[/yellow]")
            for error in results['errors']:
                console.print(f"  • {error}")
                
    except asyncio.TimeoutError:
        console.print(f"[red]Sync timed out after {timeout} seconds[/red]")
    except Exception as e:
        console.print(f"[red]Sync failed:[/red] {e}")


@main.command()
@click.option('--meme-id', required=True, help='Starting meme ID for entanglement exploration')
@click.option('--depth', default=3, help='Exploration depth')
@click.option('--layout', default='force_directed', help='Visualization layout')
@click.option('--output', '-o', help='Output file for visualization')
@click.pass_context
@handle_license_error
def entangle(ctx, meme_id, depth, layout, output):
    """Visualize meme entanglement networks."""
    console.print(f"[bold magenta]Exploring entanglement network...[/bold magenta]")
    
    # Initialize engine
    with console.status("[spinner]Initializing entanglement system..."):
        engine = MemeticEngine(
            license_key=ctx.obj['license_key']
        )
    
    # Create entanglement network
    with console.status("[spinner]Calculating quantum entanglements..."):
        network_data = engine.entangle()
    
    # Perform quantum walk
    with console.status(f"[spinner]Performing quantum walk from {meme_id}..."):
        walk_path = engine.quantum_walk(
            start_meme=meme_id,
            steps=depth * 20,
            teleport_probability=0.15
        )
    
    # Display walk results
    console.print(f"[green]Quantum walk completed![/green] Visited {len(set(walk_path))} unique memes.")
    
    # Show walk path
    if len(walk_path) > 0:
        console.print(f"[cyan]Walk path:[/cyan] {' → '.join(walk_path[:10])}{'...' if len(walk_path) > 10 else ''}")
    
    # Create visualization
    with console.status("[spinner]Creating entanglement visualization..."):
        viz_path = engine.visualize_noosphere(
            network_data=network_data,
            layout=layout,
            save_path=output
        )
    
    console.print(f"[green]Entanglement visualization saved to:[/green] {viz_path}")
    
    # Display network statistics
    stats = network_data.get('statistics', {})
    
    table = Table(title="Entanglement Network Statistics")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="white")
    
    table.add_row("Total Nodes", str(stats.get('total_nodes', 0)))
    table.add_row("Total Edges", str(stats.get('total_edges', 0)))
    table.add_row("Average Entanglement", f"{stats.get('average_entanglement', 0):.3f}")
    table.add_row("Network Density", f"{stats.get('density', 0):.3f}")
    table.add_row("Clustering Coefficient", f"{stats.get('clustering_coefficient', 0):.3f}")
    
    console.print(table)


@main.command()
@click.option('--status', is_flag=True, help='Show license status')
@click.option('--validate', is_flag=True, help='Validate current license')
@click.option('--features', is_flag=True, help='List available features')
@click.pass_context
def license(ctx, status, validate, features):
    """Manage QuantumMeta license."""
    console.print(f"[bold blue]License Management[/bold blue]")
    
    try:
        license_manager = LicenseManager(
            license_key=ctx.obj['license_key']
            # Strict licensing - no research mode or dev mode
        )
        
        if status or not (validate or features):
            # Show license status
            status_info = license_manager.get_license_status()
            
            table = Table(title="License Status")
            table.add_column("Property", style="cyan")
            table.add_column("Value", style="white")
            
            table.add_row("Valid", "✅ Yes" if status_info['valid'] else "❌ No")
            table.add_row("Tier", status_info.get('tier', 'unknown'))
            table.add_row("Features", str(len(status_info.get('features', []))))
            
            if status_info.get('expires_at'):
                import datetime
                expires = datetime.datetime.fromtimestamp(status_info['expires_at'])
                table.add_row("Expires", expires.strftime('%Y-%m-%d %H:%M:%S'))
            
            table.add_row("Hardware ID", status_info.get('hardware_id', 'unknown')[:16] + "...")
            
            console.print(table)
            
            # Show limits
            limits = status_info.get('limits', {})
            if limits:
                console.print("\n[bold]License Limits:[/bold]")
                for limit_name, limit_value in limits.items():
                    console.print(f"  • {limit_name}: {limit_value}")
            
            # Show capabilities
            capabilities = status_info.get('capabilities', {})
            if capabilities:
                console.print("\n[bold]Capabilities:[/bold]")
                for cap_name, cap_enabled in capabilities.items():
                    status_icon = "✅" if cap_enabled else "❌"
                    console.print(f"  • {cap_name}: {status_icon}")
        
        if validate:
            with console.status("[spinner]Validating license..."):
                license_info = license_manager.validate_license()
            
            console.print(f"[green]License validation successful![/green]")
            console.print(f"Tier: {license_info.tier}")
            console.print(f"Features: {len(license_info.features)}")
        
        if features:
            available_features = license_manager.get_available_features()
            
            console.print(f"\n[bold]Available Features ({len(available_features)}):[/bold]")
            for feature in available_features:
                console.print(f"  ✅ {feature}")
            
            # Show unavailable features for comparison
            all_features = []
            for tier_features in license_manager.TIER_FEATURES.values():
                all_features.extend(tier_features)
            
            unavailable = set(all_features) - set(available_features)
            if unavailable:
                console.print(f"\n[bold]Unavailable Features ({len(unavailable)}):[/bold]")
                for feature in unavailable:
                    console.print(f"  ❌ {feature}")
                
                console.print("\n[yellow]Upgrade your license to access more features:[/yellow]")
                console.print("https://krish567366.github.io/license-server/")
    
    except QMemeticLicenseError as e:
        console.print(f"[red]License Error:[/red] {e}")
        console.print("[yellow]Get a license at:[/yellow] https://krish567366.github.io/license-server/")
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")


@main.command()
@click.option('--format', default='table', type=click.Choice(['table', 'json']), help='Output format')
@click.pass_context
@handle_license_error
def status(ctx, format):
    """Show Q-Memetic AI system status."""
    console.print(f"[bold green]Q-Memetic AI System Status[/bold green]")
    
    # Initialize engine
    with console.status("[spinner]Gathering system status..."):
        engine = MemeticEngine(
            license_key=ctx.obj['license_key']
        )
        
        system_status = engine.get_system_status()
    
    if format == 'json':
        console.print(Syntax(json.dumps(system_status, indent=2), "json"))
        return
    
    # System Info
    system_info = system_status.get('system_info', {})
    table = Table(title="System Information")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="white")
    
    table.add_row("Session ID", system_info.get('session_id', 'unknown')[:16] + "...")
    table.add_row("Uptime", f"{system_info.get('uptime_seconds', 0):.1f} seconds")
    table.add_row("Federated Mode", "✅" if system_info.get('federated_mode') else "❌")
    
    console.print(table)
    
    # License Status
    license_status = system_status.get('license_status', {})
    table = Table(title="License Status")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="white")
    
    table.add_row("Tier", license_status.get('tier', 'unknown'))
    table.add_row("Valid", "✅" if license_status.get('valid') else "❌")
    table.add_row("Features", str(len(license_status.get('features_available', []))))
    
    console.print(table)
    
    # Data Metrics
    data_metrics = system_status.get('data_metrics', {})
    table = Table(title="Data Metrics")
    table.add_column("Metric", style="cyan")
    table.add_column("Count", style="white")
    
    table.add_row("Total Memes", str(data_metrics.get('total_memes', 0)))
    table.add_row("Entanglement Edges", str(data_metrics.get('entanglement_edges', 0)))
    table.add_row("Cognitive Models", str(data_metrics.get('cognitive_models', 0)))
    table.add_row("Average Fitness", f"{data_metrics.get('average_fitness', 0):.3f}")
    
    console.print(table)
    
    # Network Health
    network_health = system_status.get('network_health', {})
    table = Table(title="Network Health")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="white")
    
    table.add_row("Graph Density", f"{network_health.get('graph_density', 0):.3f}")
    table.add_row("Connected Components", str(network_health.get('connected_components', 0)))
    table.add_row("Average Clustering", f"{network_health.get('average_clustering', 0):.3f}")
    
    console.print(table)


@main.command()
@click.option('--content', required=True, help='Meme content to create')
@click.option('--author', help='Author name')
@click.option('--domain', help='Content domain')
@click.option('--tags', help='Comma-separated tags')
@click.pass_context
@handle_license_error
def create(ctx, content, author, domain, tags):
    """Create a new meme."""
    console.print(f"[bold green]Creating new meme...[/bold green]")
    
    # Initialize engine
    with console.status("[spinner]Initializing Q-Memetic AI Engine..."):
        engine = MemeticEngine(
            license_key=ctx.obj['license_key']
        )
    
    # Parse tags
    tag_list = [tag.strip() for tag in tags.split(',')] if tags else []
    
    # Create meme
    with console.status("[spinner]Creating meme with vector representation..."):
        meme = engine.create_meme(
            content=content,
            author=author or "cli_user",
            domain=domain,
            tags=tag_list
        )
    
    console.print(f"[green]Meme created successfully![/green]")
    
    # Display meme info
    table = Table(title="Created Meme")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="white")
    
    table.add_row("ID", meme.meme_id)
    table.add_row("Content", meme.content[:100] + "..." if len(meme.content) > 100 else meme.content)
    table.add_row("Author", meme.metadata.author or "unknown")
    table.add_row("Domain", meme.metadata.domain or "none")
    table.add_row("Tags", ", ".join(meme.metadata.tags) if meme.metadata.tags else "none")
    table.add_row("Fitness", f"{meme.vector.fitness_score:.3f}" if meme.vector else "0.000")
    table.add_row("Vector Dimension", str(meme.vector.dimension) if meme.vector else "none")
    
    console.print(table)


@main.command()
@click.argument('meme_id')
@click.pass_context
@handle_license_error
def analyze(ctx, meme_id):
    """Analyze a specific meme."""
    console.print(f"[bold cyan]Analyzing meme: {meme_id}[/bold cyan]")
    
    # Initialize engine
    with console.status("[spinner]Loading meme data..."):
        engine = MemeticEngine(
            license_key=ctx.obj['license_key']
        )
        
        try:
            analytics = engine.get_meme_analytics(meme_id)
        except ValueError as e:
            console.print(f"[red]Error:[/red] {e}")
            return
    
    # Basic Info
    basic_info = analytics.get('basic_info', {})
    table = Table(title="Basic Information")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="white")
    
    for key, value in basic_info.items():
        table.add_row(key.replace('_', ' ').title(), str(value))
    
    console.print(table)
    
    # Fitness Metrics
    fitness_metrics = analytics.get('fitness_metrics', {})
    table = Table(title="Fitness Metrics")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="white")
    
    for key, value in fitness_metrics.items():
        table.add_row(key.replace('_', ' ').title(), str(value))
    
    console.print(table)
    
    # Network Position
    network_position = analytics.get('network_position', {})
    if network_position.get('status') != 'not_entangled':
        table = Table(title="Network Position")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="white")
        
        for key, value in network_position.items():
            if key != 'neighbors':
                table.add_row(key.replace('_', ' ').title(), f"{value:.3f}" if isinstance(value, float) else str(value))
        
        console.print(table)
        
        # Show neighbors
        neighbors = network_position.get('neighbors', [])
        if neighbors:
            console.print(f"\n[bold]Connected Memes ({len(neighbors)}):[/bold]")
            for neighbor in neighbors[:10]:  # Show first 10
                console.print(f"  • {neighbor}")
            if len(neighbors) > 10:
                console.print(f"  ... and {len(neighbors) - 10} more")
    else:
        console.print("[yellow]Meme is not entangled with any others[/yellow]")
    
    # Evolution Lineage
    lineage = analytics.get('evolution_lineage', {})
    if lineage:
        console.print(f"\n[bold]Evolution Lineage:[/bold]")
        console.print(f"Family size: {lineage.get('family_size', 0)} memes")
        
        ancestors = lineage.get('ancestors', [])
        if ancestors:
            console.print(f"\n[cyan]Ancestors ({len(ancestors)}):[/cyan]")
            for ancestor in ancestors:
                console.print(f"  • {ancestor['meme_id']} (Gen {ancestor['generation']}): {ancestor['content_preview']}")
        
        descendants = lineage.get('descendants', [])
        if descendants:
            console.print(f"\n[green]Descendants ({len(descendants)}):[/green]")
            for descendant in descendants:
                console.print(f"  • {descendant['meme_id']} (Gen {descendant['generation']}): {descendant['content_preview']}")


if __name__ == '__main__':
    main()
