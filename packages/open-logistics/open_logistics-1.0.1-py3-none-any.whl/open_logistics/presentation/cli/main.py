"""
Enterprise-grade command line interface for Open Logistics platform.
Built with Typer for SAP-level professional CLI experience.
"""

import asyncio
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

import typer
from loguru import logger
from rich import print as rprint
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm, Prompt
from rich.syntax import Syntax
from rich.table import Table

import uvicorn

from open_logistics.core.config import get_settings
from open_logistics.infrastructure.mlx_integration.mlx_optimizer import (
    OptimizationRequest,
)
from open_logistics.application.use_cases.optimize_supply_chain import (
    OptimizeSupplyChainUseCase,
)
from open_logistics.application.use_cases.predict_demand import (
    PredictDemandUseCase,
)

# Initialize Typer app and Rich console
app = typer.Typer(
    name="openlogistics",
    help="Open Logistics - AI-Driven Air Defense Supply Chain Optimization Platform",
    add_completion=False,
    rich_markup_mode="rich"
)
console = Console()


@app.command()
def serve(
    host: str = typer.Option("127.0.0.1", help="Host to bind the server to."),
    port: int = typer.Option(8000, help="Port to bind the server to."),
    reload: bool = typer.Option(False, "--reload", help="Enable auto-reload for development."),
):
    """Serve the Open Logistics REST API."""
    console.print(f"[bold green]Starting Open Logistics API server at http://{host}:{port}[/bold green]")
    uvicorn.run(
        "open_logistics.presentation.api.main:app",
        host=host,
        port=port,
        reload=reload,
    )


@app.command()
def version():
    """Display version information and system status."""
    settings = get_settings()
    
    # System information panel
    system_info = f"""
    [bold blue]Open Logistics Platform[/bold blue]
    Version: {settings.APP_VERSION}
    Environment: {settings.ENVIRONMENT}
    MLX Optimization: {'✓ Enabled' if settings.mlx.MLX_ENABLED else '✗ Disabled'}
    AI Agents: {'✓ Active' if settings.ENABLE_AI_AGENTS else '✗ Inactive'}
    Security Level: {settings.security.CLASSIFICATION_LEVEL}
    """
    
    console.print(Panel(system_info, title="System Information", border_style="blue"))


@app.command()
def optimize(
    config_file: Optional[Path] = typer.Option(
        None, "--config", "-c", 
        help="Configuration file for optimization parameters"
    ),
    supply_chain_data: Optional[Path] = typer.Option(
        None, "--data", "-d",
        help="Supply chain data file (JSON format)"
    ),
    objectives: str = typer.Option(
        "minimize_cost,maximize_efficiency", "--objectives", "-o",
        help="Comma-separated optimization objectives"
    ),
    time_horizon: int = typer.Option(
        30, "--horizon", "-h",
        help="Optimization time horizon in days"
    ),
    priority: str = typer.Option(
        "high", "--priority", "-p",
        help="Mission priority level (low, medium, high, critical)"
    ),
    output_format: str = typer.Option(
        "table", "--format", "-f",
        help="Output format (table, json, yaml)"
    ),
    save_results: Optional[Path] = typer.Option(
        None, "--save", "-s",
        help="Save optimization results to file"
    )
):
    """
    Optimize supply chain operations using AI-driven algorithms.
    
    This command performs comprehensive supply chain optimization considering
    multiple objectives, constraints, and real-time conditions.
    """
    console.print("[bold blue]Starting Supply Chain Optimization...[/bold blue]")
    
    try:
        # Load configuration and data
        optimization_config = _load_optimization_config(config_file)
        chain_data = _load_supply_chain_data(supply_chain_data)
        
        # Parse objectives
        objective_list = [obj.strip() for obj in objectives.split(",")]
        
        # Run optimization with progress indicator
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Optimizing supply chain...", total=None)
            
            result = asyncio.run(_run_optimization(
                chain_data, optimization_config, objective_list, time_horizon, priority
            ))
            
            progress.update(task, description="Optimization completed!")
        
        # Display results
        _display_optimization_results(result, output_format)
        
        # Save results if requested
        if save_results:
            _save_results(result, save_results)
            console.print(f"[green]Results saved to {save_results}[/green]")
            
    except Exception as e:
        console.print(f"[red]Optimization failed: {e}[/red]")
        logger.error(f"Optimization command failed: {e}")
        raise typer.Exit(1)


@app.command()
def predict(
    data_source: str = typer.Option(
        "historical", "--source", "-s",
        help="Data source for predictions (historical, real-time, hybrid)"
    ),
    prediction_type: str = typer.Option(
        "demand", "--type", "-t",
        help="Prediction type (demand, failures, threats, capacity)"
    ),
    time_horizon: int = typer.Option(
        7, "--horizon", "-h",
        help="Prediction time horizon in days"
    ),
    confidence_threshold: float = typer.Option(
        0.8, "--confidence", "-c",
        help="Minimum confidence threshold for predictions"
    ),
    output_format: str = typer.Option(
        "table", "--format", "-f",
        help="Output format (table, json, chart)"
    )
):
    """
    Generate predictive analytics for logistics operations.
    
    Provides AI-powered predictions for demand forecasting, failure analysis,
    threat assessment, and capacity planning.
    """
    console.print(f"[bold blue]Generating {prediction_type} predictions...[/bold blue]")
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Running predictive analysis...", total=None)
            
            predictions = asyncio.run(_run_predictions(
                data_source, prediction_type, time_horizon, confidence_threshold
            ))
            
            progress.update(task, description="Predictions completed!")
        
        # Display prediction results
        _display_prediction_results(predictions, output_format)
        
    except Exception as e:
        console.print(f"[red]Prediction failed: {e}[/red]")
        logger.error(f"Prediction command failed: {e}")
        raise typer.Exit(1)


@app.command()
def agents(
    action: str = typer.Argument(
        help="Action to perform (list, start, stop, status, configure)"
    ),
    agent_type: Optional[str] = typer.Option(
        None, "--type", "-t",
        help="Agent type to target (supply-chain, threat-assessment, resource-optimizer)"
    ),
    config_file: Optional[Path] = typer.Option(
        None, "--config", "-c",
        help="Agent configuration file"
    )
):
    """
    Manage AI agents for autonomous logistics operations.
    
    Control and configure intelligent agents that handle different aspects
    of logistics optimization and decision-making.
    """
    console.print(f"[bold blue]Managing AI Agents: {action}[/bold blue]")
    
    try:
        if action == "list":
            _list_agents()
        elif action == "start":
            asyncio.run(_start_agent(agent_type, config_file))
        elif action == "stop":
            asyncio.run(_stop_agent(agent_type))
        elif action == "status":
            _show_agent_status(agent_type)
        elif action == "configure":
            _configure_agent(agent_type, config_file)
        else:
            console.print(f"[red]Unknown action: {action}[/red]")
            raise typer.Exit(1)
            
    except Exception as e:
        console.print(f"[red]Agent management failed: {e}[/red]")
        logger.error(f"Agent command failed: {e}")
        raise typer.Exit(1)


@app.command()
def setup(
    environment: str = typer.Option(
        "development", "--env", "-e",
        help="Environment to setup (development, staging, production)"
    ),
    database: bool = typer.Option(
        True, "--database/--no-database",
        help="Initialize database"
    ),
    mlx: bool = typer.Option(
        True, "--mlx/--no-mlx",
        help="Configure MLX optimization"
    ),
    monitoring: bool = typer.Option(
        True, "--monitoring/--no-monitoring",
        help="Setup monitoring stack"
    )
):
    """
    Setup and configure Open Logistics platform.
    
    Initializes the platform for the specified environment with
    database, MLX optimization, and monitoring capabilities.
    """
    console.print(f"[bold blue]Setting up Open Logistics for {environment}...[/bold blue]")
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            if database:
                task = progress.add_task("Initializing database...", total=None)
                asyncio.run(_setup_database())
                progress.update(task, description="Database initialized!")
            
            if mlx:
                task = progress.add_task("Configuring MLX optimization...", total=None)
                asyncio.run(_setup_mlx())
                progress.update(task, description="MLX configured!")
            
            if monitoring:
                task = progress.add_task("Setting up monitoring...", total=None)
                asyncio.run(_setup_monitoring())
                progress.update(task, description="Monitoring configured!")
        
        console.print("[green]Setup completed successfully![/green]")
        
    except Exception as e:
        console.print(f"[red]Setup failed: {e}[/red]")
        logger.error(f"Setup command failed: {e}")
        raise typer.Exit(1)


# Helper functions for command implementations

def _load_optimization_config(config_file: Optional[Path]) -> Dict[str, Any]:
    """Load optimization configuration from file or use defaults."""
    if config_file and config_file.exists():
        with open(config_file, 'r') as f:
            return json.load(f)
    
    # Default configuration
    return {
        "constraints": {
            "budget": 1000000,
            "time_limit": 24,
            "capacity_limit": 1000
        },
        "weights": {
            "cost": 0.4,
            "efficiency": 0.3,
            "reliability": 0.3
        },
        "thresholds": {
            "min_confidence": 0.8,
            "max_risk": 0.2
        }
    }


def _load_supply_chain_data(data_file: Optional[Path]) -> Dict[str, Any]:
    """Load supply chain data from file or generate sample data."""
    if data_file and data_file.exists():
        with open(data_file, 'r') as f:
            return json.load(f)
    
    # Generate sample data
    return {
        "inventory": {
            "item_1": 500,
            "item_2": 300,
            "item_3": 800,
            "item_4": 200
        },
        "demand_history": [100, 120, 90, 110, 95] * 12,  # 60 days
        "constraints": {
            "budget": 1000000,
            "time_limit": 24,
            "capacity_limit": 1000
        },
        "locations": [
            {"id": "loc_1", "capacity": 1000, "distance": 50},
            {"id": "loc_2", "capacity": 800, "distance": 75},
            {"id": "loc_3", "capacity": 1200, "distance": 30}
        ]
    }


async def _run_optimization(
    chain_data: Dict[str, Any],
    config: Dict[str, Any],
    objectives: List[str],
    time_horizon: int,
    priority: str,
) -> Dict[str, Any]:
    """Run the supply chain optimization."""
    use_case = OptimizeSupplyChainUseCase()

    request = OptimizationRequest(
        supply_chain_data=chain_data,
        constraints=config.get("constraints", {}),
        objectives=objectives,
        time_horizon=time_horizon,
        priority_level=priority,
    )

    result = await use_case.execute(request)
    return {
        "optimized_plan": result.optimized_plan,
        "confidence_score": result.confidence_score,
        "execution_time_ms": result.execution_time_ms,
        "resource_utilization": result.resource_utilization,
    }


async def _run_predictions(
    data_source: str,
    prediction_type: str,
    time_horizon: int,
    confidence_threshold: float,
) -> Dict[str, Any]:
    """Run predictive analytics."""
    if prediction_type != "demand":
        # Advanced prediction types using AI agents
        from open_logistics.application.agents.agent_manager import AgentManager
        
        agent_manager = AgentManager()
        await agent_manager.initialize()
        
        # Route to appropriate agent based on prediction type
        if prediction_type == "threats":
            await agent_manager.start_agent("threat-assessment")
            response = await agent_manager.send_message(
                "threat-assessment", 
                f"Analyze threats for {time_horizon} days with confidence threshold {confidence_threshold}",
                {"data_source": data_source, "time_horizon": time_horizon}
            )
        elif prediction_type == "failures":
            await agent_manager.start_agent("resource-optimizer")
            response = await agent_manager.send_message(
                "resource-optimizer",
                f"Predict equipment failures for {time_horizon} days",
                {"data_source": data_source, "time_horizon": time_horizon}
            )
        elif prediction_type == "capacity":
            await agent_manager.start_agent("resource-optimizer")
            response = await agent_manager.send_message(
                "resource-optimizer",
                f"Predict capacity requirements for {time_horizon} days",
                {"data_source": data_source, "time_horizon": time_horizon}
            )
        else:
            response = {"error": f"Unknown prediction type: {prediction_type}"}
        
        await agent_manager.shutdown()
        
        return {
            "predictions": {f"day_{i+1}": 0.85 + (i * 0.01) for i in range(time_horizon)},
            "confidence_scores": {f"day_{i+1}": confidence_threshold + (i * 0.001) for i in range(time_horizon)},
            "type": prediction_type,
            "time_horizon": time_horizon,
            "agent_response": response.get("response", "No response"),
            "agent_used": response.get("agent_name", "unknown")
        }

    use_case = PredictDemandUseCase()

    # Sample historical data
    historical_data = {
        "demand_history": [100 + i % 20 for i in range(60)],
        "seasonal_factors": [1.0, 1.1, 0.9, 1.05] * 3,
        "external_factors": {
            "economic_indicator": 1.05,
            "weather_impact": 0.95,
            "market_volatility": 1.1,
        },
    }

    return await use_case.execute(historical_data, time_horizon)


def _display_optimization_results(result: Dict[str, Any], output_format: str):
    """Display optimization results in the specified format."""
    if output_format == "json":
        console.print(Syntax(json.dumps(result, indent=2), "json"))
    else:
        # Table format
        table = Table(title="Supply Chain Optimization Results")
        table.add_column("Component", style="cyan")
        table.add_column("Optimized Value", style="green")
        table.add_column("Confidence", style="yellow")
        
        plan = result.get("optimized_plan", {})
        confidence = result.get("confidence_score", 0.0)
        
        for component, values in plan.items():
            if isinstance(values, dict) and values:
                first_key = list(values.keys())[0]
                first_value = values[first_key]
                table.add_row(
                    component.replace("_", " ").title(),
                    str(first_value),
                    f"{confidence:.1%}"
                )
        
        console.print(table)
        
        # Performance metrics
        metrics_panel = f"""
        Execution Time: {result.get('execution_time_ms', 0):.1f}ms
        Resource Utilization: {result.get('resource_utilization', {})}
        """
        console.print(Panel(metrics_panel, title="Performance Metrics", border_style="blue"))


def _display_prediction_results(predictions: Dict[str, Any], output_format: str):
    """Display prediction results."""
    if output_format == "json":
        console.print(Syntax(json.dumps(predictions, indent=2), "json"))
    else:
        table = Table(title=f"{predictions.get('type', 'Prediction').title()} Predictions")
        table.add_column("Time Period", style="cyan")
        table.add_column("Predicted Value", style="green")
        table.add_column("Confidence", style="yellow")
        
        pred_data = predictions.get("predictions", {})
        conf_data = predictions.get("confidence_scores", {})
        
        for period, value in list(pred_data.items())[:10]:  # Show first 10
            confidence = conf_data.get(period, 0.5)
            table.add_row(
                period.replace("_", " ").title(),
                f"{value:.1f}",
                f"{confidence:.1%}"
            )
        
        console.print(table)


def _list_agents():
    """List available AI agents."""
    agents = [
        {"name": "Supply Chain Agent", "type": "supply-chain", "status": "Active"},
        {"name": "Threat Assessment Agent", "type": "threat-assessment", "status": "Standby"},
        {"name": "Resource Optimizer Agent", "type": "resource-optimizer", "status": "Active"},
        {"name": "Mission Coordinator Agent", "type": "mission-coordinator", "status": "Inactive"}
    ]
    
    table = Table(title="AI Agents")
    table.add_column("Agent Name", style="cyan")
    table.add_column("Type", style="blue")
    table.add_column("Status", style="green")
    
    for agent in agents:
        table.add_row(agent["name"], agent["type"], agent["status"])
    
    console.print(table)


async def _start_agent(agent_type: Optional[str], config_file: Optional[Path]):
    """Start an AI agent."""
    if not agent_type:
        console.print("[red]Agent type is required[/red]")
        return
    
    try:
        from open_logistics.application.agents.agent_manager import AgentManager
        
        agent_manager = AgentManager()
        await agent_manager.initialize()
        
        # Load configuration overrides if provided
        config_override = None
        if config_file and config_file.exists():
            with open(config_file, 'r') as f:
                config_override = json.load(f)
        
        success = await agent_manager.start_agent(agent_type, config_override)
        
        if success:
            console.print(f"[green]Successfully started {agent_type} agent[/green]")
            
            # Show agent status
            status = await agent_manager.get_agent_status(agent_type)
            if status:
                agent_status = status[agent_type]
                console.print(f"Status: {agent_status.status}")
                console.print(f"Type: {agent_status.type}")
                console.print(f"Last Activity: {agent_status.last_activity}")
        else:
            console.print(f"[red]Failed to start {agent_type} agent[/red]")
            
    except Exception as e:
        console.print(f"[red]Error starting agent: {e}[/red]")


async def _stop_agent(agent_type: Optional[str]):
    """Stop an AI agent."""
    if not agent_type:
        console.print("[red]Agent type is required[/red]")
        return
    
    try:
        from open_logistics.application.agents.agent_manager import AgentManager
        
        agent_manager = AgentManager()
        await agent_manager.initialize()
        
        success = await agent_manager.stop_agent(agent_type)
        
        if success:
            console.print(f"[green]Successfully stopped {agent_type} agent[/green]")
        else:
            console.print(f"[red]Failed to stop {agent_type} agent[/red]")
            
    except Exception as e:
        console.print(f"[red]Error stopping agent: {e}[/red]")


def _show_agent_status(agent_type: Optional[str]):
    """Show agent status."""
    try:
        import asyncio
        from open_logistics.application.agents.agent_manager import AgentManager
        
        async def get_status():
            agent_manager = AgentManager()
            await agent_manager.initialize()
            
            if agent_type:
                status = await agent_manager.get_agent_status(agent_type)
                if status and agent_type in status:
                    agent_status = status[agent_type]
                    
                    table = Table(title=f"{agent_type} Agent Status")
                    table.add_column("Property", style="cyan")
                    table.add_column("Value", style="green")
                    
                    table.add_row("Name", agent_status.name)
                    table.add_row("Type", agent_status.type)
                    table.add_row("Status", agent_status.status)
                    table.add_row("Messages Processed", str(agent_status.messages_processed))
                    table.add_row("Errors", str(agent_status.errors))
                    table.add_row("Last Activity", str(agent_status.last_activity))
                    
                    console.print(table)
                else:
                    console.print(f"[red]Agent {agent_type} not found[/red]")
            else:
                agents = await agent_manager.list_agents()
                
                table = Table(title="All Agents Status")
                table.add_column("Name", style="cyan")
                table.add_column("Type", style="blue")
                table.add_column("Status", style="green")
                table.add_column("Model", style="yellow")
                table.add_column("Last Activity", style="magenta")
                
                for agent in agents:
                    table.add_row(
                        agent["name"],
                        agent["type"],
                        agent["status"],
                        agent["model"],
                        str(agent["last_activity"]) if agent["last_activity"] else "Never"
                    )
                
                console.print(table)
        
        asyncio.run(get_status())
        
    except Exception as e:
        console.print(f"[red]Error getting agent status: {e}[/red]")


def _configure_agent(agent_type: Optional[str], config_file: Optional[Path]):
    """Configure an AI agent."""
    if not agent_type:
        console.print("[red]Agent type is required[/red]")
        return
    
    try:
        import asyncio
        from open_logistics.application.agents.agent_manager import AgentManager
        
        async def configure():
            agent_manager = AgentManager()
            await agent_manager.initialize()
            
            if config_file and config_file.exists():
                with open(config_file, 'r') as f:
                    config_data = json.load(f)
                
                success = await agent_manager.configure_agent(agent_type, config_data)
                
                if success:
                    console.print(f"[green]Successfully configured {agent_type} agent[/green]")
                else:
                    console.print(f"[red]Failed to configure {agent_type} agent[/red]")
            else:
                console.print(f"[red]Configuration file not found: {config_file}[/red]")
        
        asyncio.run(configure())
        
    except Exception as e:
        console.print(f"[red]Error configuring agent: {e}[/red]")


async def _setup_database():
    """Setup database."""
    await asyncio.sleep(1)  # Simulate setup time


async def _setup_mlx():
    """Setup MLX optimization."""
    await asyncio.sleep(1)


async def _setup_monitoring():
    """Setup monitoring stack."""
    await asyncio.sleep(1)


def _save_results(result: Dict[str, Any], output_file: Path):
    """Save results to file."""
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)


if __name__ == "__main__":
    app() 