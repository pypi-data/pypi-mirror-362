import click
import asyncio
import json
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List
import logging
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.syntax import Syntax
import os

from .agents.discovery import MaterialsDiscoveryAgent
from .agents.synthesis import SynthesisAgent
from .agents.characterization import CharacterizationAgent
from .agents.optimization import OptimizationAgent
from .database.connection import DatabaseManager
from .utils.config import load_config, Config
from .utils.exceptions import OpenRXNError
from .utils.logging import setup_logging
from .models.crystal_structure import PerovskiteStructure
from .api.main import create_app

console = Console()

# Global configuration
config: Optional[Config] = None
db_manager: Optional[DatabaseManager] = None

def setup_globals(ctx):
    """Setup global configuration and database connection"""
    global config, db_manager
    
    config_path = ctx.obj.get('config_path')
    verbose = ctx.obj.get('verbose', False)
    
    # Load configuration
    config = load_config(config_path)
    
    # Setup logging
    setup_logging(
        level=logging.DEBUG if verbose else logging.INFO,
        log_file=config.logging.file_path if config.logging.file_path else None
    )
    
    # Initialize database
    db_manager = DatabaseManager(config.database.url)

@click.group()
@click.version_option(version="1.0.0")
@click.option('--config', '-c', 
              type=click.Path(exists=True, path_type=Path),
              help='Configuration file path')
@click.option('--verbose', '-v', 
              is_flag=True, 
              help='Enable verbose logging')
@click.pass_context
def cli(ctx, config: Optional[Path], verbose: bool):
    """
    🔬 OpenRXN Perovskite Optimizer
    
    AI-driven perovskite solar cell optimization platform with multi-agent architecture.
    """
    ctx.ensure_object(dict)
    ctx.obj['config_path'] = config
    ctx.obj['verbose'] = verbose
    
    # Setup banner
    console.print(Panel.fit(
        "[bold blue]OpenRXN Perovskite Optimizer[/bold blue]\n"
        "[dim]AI-driven materials discovery and optimization[/dim]",
        border_style="blue"
    ))

@cli.group()
@click.pass_context
def discover(ctx):
    """Materials discovery commands"""
    setup_globals(ctx)

@discover.command()
@click.option('--composition', '-c', 
              required=True,
              help='Base perovskite composition (e.g., MAPbI3)')
@click.option('--target-efficiency', '-e', 
              type=float, 
              default=25.0,
              help='Target power conversion efficiency (%)')
@click.option('--target-stability', '-s', 
              type=float, 
              default=1000.0,
              help='Target stability (hours)')
@click.option('--max-candidates', '-n', 
              type=int, 
              default=10,
              help='Maximum number of candidates to generate')
@click.option('--output-dir', '-o', 
              type=click.Path(path_type=Path),
              default=Path('./results'),
              help='Output directory')
@click.option('--save-intermediates', 
              is_flag=True,
              help='Save intermediate results')
@click.pass_context
def materials(ctx, composition: str, target_efficiency: float, 
              target_stability: float, max_candidates: int, 
              output_dir: Path, save_intermediates: bool):
    """Discover new perovskite materials using AI agents"""
    
    async def run_discovery():
        try:
            # Create output directory
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Initialize discovery agent
            with console.status("[bold green]Initializing discovery agent..."):
                from .ml.property_prediction import PropertyPredictor
                from .database.crud import MaterialsCRUD
                
                predictor = PropertyPredictor()
                materials_crud = MaterialsCRUD(db_manager)
                
                discovery_agent = MaterialsDiscoveryAgent(
                    predictor=predictor,
                    database=materials_crud,
                    target_properties={
                        'efficiency': target_efficiency,
                        'stability': target_stability
                    }
                )
            
            # Run discovery
            console.print(f"[bold blue]Discovering materials based on {composition}[/bold blue]")
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                
                task = progress.add_task("Generating candidates...", total=None)
                
                results = await discovery_agent.discover_materials(
                    target_properties={
                        'efficiency': target_efficiency,
                        'stability': target_stability
                    },
                    max_candidates=max_candidates
                )
                
                progress.update(task, description="Discovery complete!")
            
            # Display results
            if results:
                table = Table(title="Discovery Results")
                table.add_column("Rank", style="cyan")
                table.add_column("Composition", style="magenta")
                table.add_column("Confidence", style="green")
                table.add_column("Est. Efficiency", style="yellow")
                table.add_column("Stability", style="blue")
                table.add_column("Cost ($/g)", style="red")
                
                for i, result in enumerate(results, 1):
                    table.add_row(
                        str(i),
                        result.composition,
                        f"{result.confidence:.3f}",
                        f"{result.predicted_properties.predicted_efficiency:.1f}%",
                        f"{result.synthesis_feasibility:.3f}",
                        f"${result.cost_estimate:.2f}"
                    )
                
                console.print(table)
                
                # Save results
                results_file = output_dir / "discovery_results.json"
                with open(results_file, 'w') as f:
                    json.dump([
                        {
                            'composition': r.composition,
                            'confidence': r.confidence,
                            'predicted_efficiency': r.predicted_properties.predicted_efficiency,
                            'synthesis_feasibility': r.synthesis_feasibility,
                            'cost_estimate': r.cost_estimate
                        }
                        for r in results
                    ], f, indent=2)
                
                console.print(f"[green]Results saved to {results_file}[/green]")
                
                # Ask user about next steps
                if os.environ.get("TESTING") == "true":
                    proceed = False
                else:
                    proceed = Confirm.ask("Would you like to proceed with synthesis planning?")
                if proceed:
                    # Hand off to synthesis agent
                    synthesis_agent = SynthesisAgent(None, None)  # Initialize properly
                    synthesis_agent.handoff_to_synthesis(results)
                    
                    console.print("[yellow]Synthesis planning initiated![/yellow]")
            
            else:
                console.print("[red]No suitable materials found![/red]")
                
        except OpenRXNError as e:
            console.print(f"[red]Discovery failed: {e}[/red]")
            sys.exit(1)
        except Exception as e:
            console.print(f"[red]Unexpected error: {e}[/red]")
            sys.exit(1)
    
    asyncio.run(run_discovery())

@cli.group()
@click.pass_context
def synthesize(ctx):
    """⚗️ Synthesis planning and execution commands"""
    setup_globals(ctx)

@synthesize.command()
@click.option('--composition', '-c', 
              required=True,
              help='Perovskite composition to synthesize')
@click.option('--method', '-m', 
              type=click.Choice(['solution_processing', 'vapor_deposition', 'solid_state', 'auto']),
              default='auto',
              help='Synthesis method')
@click.option('--batch-size', '-b', 
              type=float, 
              default=1.0,
              help='Batch size (grams)')
@click.option('--output-dir', '-o', 
              type=click.Path(path_type=Path),
              default=Path('./synthesis_results'),
              help='Output directory')
@click.pass_context
def protocol(ctx, composition: str, method: str, batch_size: float, output_dir: Path):
    """Generate synthesis protocol for a perovskite composition"""
    
    async def run_synthesis_planning():
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Initialize synthesis agent
            with console.status("[bold green]Initializing synthesis agent..."):
                from .experimental.synthesis_protocols import SynthesisProtocol
                from .database.crud import ExperimentalCRUD
                
                protocol_library = SynthesisProtocol()
                experimental_crud = ExperimentalCRUD(db_manager)
                
                synthesis_agent = SynthesisAgent(
                    protocol_library=protocol_library,
                    experimental_db=experimental_crud
                )
            
            # Design synthesis protocol
            console.print(f"[bold blue]Designing synthesis protocol for {composition}[/bold blue]")
            
            protocol = await synthesis_agent.design_synthesis_protocol(
                composition=composition,
                target_properties={'efficiency': 25.0, 'stability': 1000.0},
                synthesis_method=method
            )
            
            # Display protocol
            console.print(Panel(
                f"[bold]Synthesis Protocol for {composition}[/bold]\n\n"
                f"Method: {protocol['method']}\n"
                f"Estimated Duration: {protocol['estimated_duration']} hours\n"
                f"Required Equipment: {', '.join(protocol['required_equipment'])}\n\n"
                f"[yellow]Safety Level: {protocol['safety_measures']['level']}[/yellow]",
                title="Synthesis Protocol",
                border_style="green"
            ))
            
            # Show detailed steps
            if Confirm.ask("Show detailed synthesis steps?"):
                for i, step in enumerate(protocol['preparation_steps'], 1):
                    console.print(f"\n[bold cyan]Step {i}: {step['step'].replace('_', ' ').title()}[/bold cyan]")
                    for key, value in step.items():
                        if key != 'step':
                            console.print(f"  {key}: {value}")
            
            # Save protocol
            protocol_file = output_dir / f"{composition}_protocol.json"
            with open(protocol_file, 'w') as f:
                json.dump(protocol, f, indent=2, default=str)
            
            console.print(f"[green]Protocol saved to {protocol_file}[/green]")
            
        except OpenRXNError as e:
            console.print(f"[red]Synthesis planning failed: {e}[/red]")
            sys.exit(1)
        except Exception as e:
            console.print(f"[red]Unexpected error: {e}[/red]")
            sys.exit(1)
    
    asyncio.run(run_synthesis_planning())

@cli.group()
@click.pass_context
def optimize(ctx):
    """Optimization commands"""
    setup_globals(ctx)

@optimize.command()
@click.option('--composition', '-c', 
              required=True,
              help='Perovskite composition to optimize')
@click.option('--objective', '-obj', 
              type=click.Choice(['efficiency', 'stability', 'cost', 'multi']),
              default='multi',
              help='Optimization objective')
@click.option('--iterations', '-i', 
              type=int, 
              default=50,
              help='Number of optimization iterations')
@click.option('--population-size', '-p', 
              type=int, 
              default=100,
              help='Population size for genetic algorithm')
@click.option('--output-dir', '-o', 
              type=click.Path(path_type=Path),
              default=Path('./optimization_results'),
              help='Output directory')
@click.pass_context
def composition(ctx, composition: str, objective: str, iterations: int, 
               population_size: int, output_dir: Path):
    """Optimize perovskite composition using genetic algorithms"""
    
    async def run_optimization():
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Initialize optimization agent
            with console.status("[bold green]Initializing optimization agent..."):
                from .agents.optimization import OptimizationAgent
                from .ml.optimization import GeneticOptimizer
                
                optimizer = GeneticOptimizer()
                optimization_agent = OptimizationAgent(optimizer=optimizer)
            
            # Run optimization
            console.print(f"[bold blue]Optimizing {composition} for {objective}[/bold blue]")
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                
                task = progress.add_task("Running optimization...", total=iterations)
                
                results = await optimization_agent.optimize_composition(
                    base_composition=composition,
                    objective=objective,
                    max_iterations=iterations,
                    population_size=population_size,
                    progress_callback=lambda i: progress.update(task, advance=1)
                )
                
                progress.update(task, description="Optimization complete!")
            
            # Display results
            if results:
                console.print(f"[bold green]Optimization completed![/bold green]")
                console.print(f"Best composition: {results['best_composition']}")
                console.print(f"Best score: {results['best_score']:.4f}")
                
                # Show convergence plot
                if Confirm.ask("Show convergence plot?"):
                    import matplotlib.pyplot as plt
                    
                    plt.figure(figsize=(10, 6))
                    plt.plot(results['convergence_history'])
                    plt.title(f"Optimization Convergence - {objective}")
                    plt.xlabel("Iteration")
                    plt.ylabel("Best Score")
                    plt.grid(True)
                    plt.savefig(output_dir / "convergence.png")
                    plt.show()
            
            else:
                console.print("[red]Optimization failed![/red]")
                
        except OpenRXNError as e:
            console.print(f"[red]Optimization failed: {e}[/red]")
            sys.exit(1)
        except Exception as e:
            console.print(f"[red]Unexpected error: {e}[/red]")
            sys.exit(1)
    
    asyncio.run(run_optimization())

@cli.group()
@click.pass_context
def serve(ctx):
    """🌐 Web services commands"""
    setup_globals(ctx)

@serve.command()
@click.option('--host', 
              default='localhost',
              help='Host address')
@click.option('--port', 
              type=int, 
              default=8000,
              help='Port number')
@click.option('--reload', 
              is_flag=True,
              help='Enable auto-reload for development')
@click.option('--workers', 
              type=int, 
              default=1,
              help='Number of worker processes')
@click.pass_context
def api(ctx, host: str, port: int, reload: bool, workers: int):
    """Start the REST API server"""
    try:
        import uvicorn
        
        console.print(f"[bold blue]Starting API server at http://{host}:{port}[/bold blue]")
        
        # Create FastAPI app
        app = create_app(config)
        
        # Start server
        uvicorn.run(
            app,
            host=host,
            port=port,
            reload=reload,
            workers=workers,
            log_level="info" if not ctx.obj.get('verbose') else "debug"
        )
        
    except ImportError:
        console.print("[red]uvicorn not installed. Install with: pip install uvicorn[standard][/red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Failed to start API server: {e}[/red]")
        sys.exit(1)

@serve.command()
@click.option('--port', 
              type=int, 
              default=8501,
              help='Streamlit port')
@click.option('--theme', 
              type=click.Choice(['light', 'dark', 'auto']),
              default='auto',
              help='Dashboard theme')
@click.pass_context
def dashboard(ctx, port: int, theme: str):
    """Launch the interactive dashboard"""
    try:
        import subprocess
        import sys
        
        console.print(f"[bold blue]Launching dashboard at http://localhost:{port}[/bold blue]")
        
        # Set theme
        env = {}
        if theme != 'auto':
            env['STREAMLIT_THEME_BASE'] = theme
        
        # Start Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run",
            "src/openrxn_perovskite_optimizer/web/dashboard.py",
            "--server.port", str(port),
            "--server.headless", "false"
        ], env=env)
        
    except ImportError:
        console.print("[red]streamlit not installed. Install with: pip install streamlit[/red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Failed to start dashboard: {e}[/red]")
        sys.exit(1)

@cli.group()
@click.pass_context
def data(ctx):
    """Data management commands"""
    setup_globals(ctx)

@data.command()
@click.option('--format', 
              type=click.Choice(['json', 'csv', 'xlsx', 'hdf5']),
              default='json',
              help='Export format')
@click.option('--output', '-o', 
              type=click.Path(path_type=Path),
              help='Output file path')
@click.option('--filter', 
              help='Filter criteria (JSON format)')
@click.pass_context
def export(ctx, format: str, output: Optional[Path], filter: Optional[str]):
    """Export optimization results and data"""
    try:
        # Parse filter if provided
        filter_criteria = {}
        if filter:
            filter_criteria = json.loads(filter)
        
        # Export data
        from .database.crud import DataExporter
        exporter = DataExporter(db_manager)
        
        if not output:
            output = Path(f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format}")
        
        with console.status(f"[bold green]Exporting data to {format}..."):
            exporter.export_data(
                output_path=output,
                format=format,
                filter_criteria=filter_criteria
            )
        
        console.print(f"[green]Data exported to {output}[/green]")
        
    except Exception as e:
        console.print(f"[red]Export failed: {e}[/red]")
        sys.exit(1)

@cli.group()
@click.pass_context
def db(ctx):
    """🗄️ Database management commands"""
    setup_globals(ctx)

@db.command()
@click.pass_context
def init(ctx):
    """Initialize the database schema"""
    try:
        with console.status("[bold green]Initializing database..."):
            db_manager.init_database()
        
        console.print("[green]Database initialized successfully![/green]")
        
    except Exception as e:
        console.print(f"[red]Database initialization failed: {e}[/red]")
        sys.exit(1)

@db.command()
@click.pass_context
def migrate(ctx):
    """Run database migrations"""
    try:
        with console.status("[bold green]Running migrations..."):
            db_manager.run_migrations()
        
        console.print("[green]Database migrations completed![/green]")
        
    except Exception as e:
        console.print(f"[red]Migration failed: {e}[/red]")
        sys.exit(1)

@db.command()
@click.pass_context
def status(ctx):
    """Show database status"""
    try:
        status_info = db_manager.get_status()
        
        table = Table(title="Database Status")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")
        
        for key, value in status_info.items():
            table.add_row(key, str(value))
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]Failed to get database status: {e}[/red]")
        sys.exit(1)

@cli.command()
@click.option('--include-examples', 
              is_flag=True,
              help='Include example data')
@click.pass_context
def setup(ctx, include_examples: bool):
    """Setup the complete environment"""
    try:
        setup_globals(ctx)
        
        console.print("[bold blue]Setting up OpenRXN Perovskite Optimizer...[/bold blue]")
        
        # Initialize database
        with console.status("[bold green]Setting up database..."):
            db_manager.init_database()
        
        # Load example data if requested
        if include_examples:
            with console.status("[bold green]Loading example data..."):
                from .data.examples import load_example_data
                load_example_data(db_manager)
        
        console.print("[green]Setup completed successfully![/green]")
        console.print("\nNext steps:")
        console.print("1. Run [bold]perovskite-optimizer discover materials --composition MAPbI3[/bold]")
        console.print("2. Launch dashboard with [bold]perovskite-optimizer serve dashboard[/bold]")
        console.print("3. Start API server with [bold]perovskite-optimizer serve api[/bold]")
        
    except Exception as e:
        console.print(f"[red]Setup failed: {e}[/red]")
        sys.exit(1)

def main():
    """Main entry point"""
    try:
        cli()
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")
        sys.exit(1)

if __name__ == '__main__':
    main()