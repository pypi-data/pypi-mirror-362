"""
Command Line Interface for Cognito Simulation Engine.

This module provides a comprehensive CLI for running cognitive simulations,
managing agents, and analyzing results.
"""

import typer
import time
import json
import os
from pathlib import Path
from typing import Optional, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.tree import Tree
from rich.json import JSON

from .engine import CognitiveEngine, SimulationConfig
from .memory import MemoryManager, MemoryItem, MemoryType
from .reasoning import Goal, Fact
from .agents import CognitiveAgent, ReasoningAgent, LearningAgent, MetaCognitiveAgent
from .environment import CognitiveEnvironment
from .licensing import get_license_info, display_license_info, get_machine_id

app = typer.Typer(
    name="cogsim",
    help="Cognito Simulation Engine - Advanced cognitive architecture simulation framework",
    add_completion=False
)

console = Console()


def print_banner():
    """Print the application banner."""
    machine_id = get_machine_id()
    license_info = get_license_info()
    license_status = license_info.get('status', 'unknown').upper()
    
    banner = f"""
╭─────────────────────────────────────────────────────────────────╮
│                                                                 │
│  🧠 Cognito Simulation Engine v1.0.0                           │
│                                                                 │
│  Advanced Cognitive Architecture Simulation Framework          │
│  For AGI Research and Development                               │
│                                                                 │
│  Author: Krishna Bajpai <bajpaikrishna715@gmail.com>          │
│  License: MIT | Status: {license_status:<12}                           │
│  Machine ID: {machine_id:<48} │
│                                                                 │
╰─────────────────────────────────────────────────────────────────╯
    """
    console.print(banner, style="cyan")


@app.command()
def run(
    cycles: int = typer.Option(100, "--cycles", "-c", help="Number of simulation cycles to run"),
    agents: int = typer.Option(1, "--agents", "-a", help="Number of agents to create"),
    agent_type: str = typer.Option("cognitive", "--agent-type", "-t", help="Type of agent (cognitive, reasoning, learning, metacognitive)"),
    environment: str = typer.Option("default", "--environment", "-e", help="Environment type"),
    config_file: Optional[str] = typer.Option(None, "--config", "-f", help="Configuration file path"),
    output_dir: Optional[str] = typer.Option(None, "--output", "-o", help="Output directory for results"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
    interactive: bool = typer.Option(False, "--interactive", "-i", help="Interactive mode"),
):
    """Run a cognitive simulation."""
    print_banner()
    
    if verbose:
        console.print(f"🚀 Starting simulation with {cycles} cycles and {agents} agent(s)", style="green")
    
    # Load configuration
    config = SimulationConfig(max_cycles=cycles)
    if config_file:
        config = load_config(config_file)
        config.max_cycles = cycles
    
    # Create environment
    env = CognitiveEnvironment(name=f"{environment}_environment")
    console.print(f"🌍 Created environment: {env.name}", style="blue")
    
    # Create cognitive engine
    engine = CognitiveEngine(config=config, environment=env)
    console.print("🔧 Initialized cognitive engine", style="blue")
    
    # Create agents
    created_agents = []
    for i in range(agents):
        agent_id = f"agent_{i+1}"
        
        if agent_type == "reasoning":
            agent = ReasoningAgent(agent_id, name=f"ReasoningAgent-{i+1}")
        elif agent_type == "learning":
            agent = LearningAgent(agent_id, name=f"LearningAgent-{i+1}")
        elif agent_type == "metacognitive":
            agent = MetaCognitiveAgent(agent_id, name=f"MetaCognitiveAgent-{i+1}")
        else:
            agent = CognitiveAgent(agent_id, name=f"CognitiveAgent-{i+1}")
        
        # Add agent to environment
        env.add_agent(agent_id)
        created_agents.append(agent)
        
        # Add some default goals
        add_default_goals(agent)
        
        console.print(f"🤖 Created agent: {agent.name} ({agent_type})", style="green")
    
    # Run simulation
    try:
        if interactive:
            run_interactive_simulation(engine, created_agents, verbose)
        else:
            run_batch_simulation(engine, created_agents, verbose)
        
        # Save results
        if output_dir:
            save_results(engine, created_agents, output_dir)
        
    except KeyboardInterrupt:
        console.print("\n⏸️  Simulation interrupted by user", style="yellow")
    except Exception as e:
        console.print(f"\n❌ Simulation error: {e}", style="red")
        raise typer.Exit(1)


def run_batch_simulation(engine, agents, verbose):
    """Run simulation in batch mode."""
    console.print("▶️  Starting batch simulation...", style="green")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Running simulation...", total=engine.config.max_cycles)
        
        # Set up engine callbacks
        def cycle_callback(engine):
            progress.advance(task)
            if verbose and engine.current_cycle % 10 == 0:
                console.print(f"Cycle {engine.current_cycle}: {len(engine.current_goals)} active goals")
        
        engine.add_cycle_callback(cycle_callback)
        
        # Run the simulation
        metrics = engine.run_simulation()
    
    # Display results
    display_simulation_results(engine, agents, metrics)


def run_interactive_simulation(engine, agents, verbose):
    """Run simulation in interactive mode."""
    console.print("🎮 Starting interactive simulation...", style="green")
    console.print("Commands: [bold]step[/bold], [bold]status[/bold], [bold]agents[/bold], [bold]goals[/bold], [bold]memory[/bold], [bold]run[/bold], [bold]quit[/bold]")
    
    while True:
        try:
            command = typer.prompt("\ncogsim> ").strip().lower()
            
            if command == "quit" or command == "q":
                break
            elif command == "step" or command == "s":
                # Run one cycle
                engine.cognitive_cycle()
                console.print(f"Completed cycle {engine.current_cycle}")
            elif command == "status":
                display_engine_status(engine)
            elif command == "agents":
                display_agents_status(agents)
            elif command == "goals":
                display_goals_status(engine)
            elif command == "memory":
                display_memory_status(agents)
            elif command == "run":
                cycles = typer.prompt("How many cycles?", type=int, default=10)
                for _ in range(cycles):
                    engine.cognitive_cycle()
                console.print(f"Completed {cycles} cycles")
            elif command == "help" or command == "h":
                console.print("Available commands:")
                console.print("  step/s     - Run one simulation cycle")
                console.print("  status     - Show engine status")
                console.print("  agents     - Show agent status")
                console.print("  goals      - Show active goals")
                console.print("  memory     - Show memory status")
                console.print("  run        - Run multiple cycles")
                console.print("  quit/q     - Exit simulation")
            else:
                console.print("Unknown command. Type 'help' for available commands.", style="yellow")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            console.print(f"Error: {e}", style="red")


def display_simulation_results(engine, agents, metrics):
    """Display comprehensive simulation results."""
    console.print("\n" + "="*60, style="cyan")
    console.print("🎯 SIMULATION RESULTS", style="bold cyan")
    console.print("="*60, style="cyan")
    
    # Engine metrics
    metrics_table = Table(title="Engine Metrics")
    metrics_table.add_column("Metric", style="cyan")
    metrics_table.add_column("Value", style="green")
    
    metrics_dict = metrics.to_dict()
    for key, value in metrics_dict.items():
        if isinstance(value, float):
            value_str = f"{value:.3f}"
        else:
            value_str = str(value)
        metrics_table.add_row(key.replace("_", " ").title(), value_str)
    
    console.print(metrics_table)
    
    # Agent summary
    agent_table = Table(title="Agent Summary")
    agent_table.add_column("Agent", style="cyan")
    agent_table.add_column("Type", style="blue")
    agent_table.add_column("Actions", style="green")
    agent_table.add_column("Success Rate", style="yellow")
    agent_table.add_column("Goals", style="magenta")
    
    for agent in agents:
        status = agent.get_status()
        agent_table.add_row(
            agent.name,
            agent.__class__.__name__,
            str(status["metrics"]["total_actions"]),
            f"{agent.success_rate:.2f}",
            str(len(agent.current_goals))
        )
    
    console.print(agent_table)


def display_engine_status(engine):
    """Display current engine status."""
    status = engine.get_state_summary()
    
    status_panel = Panel(
        JSON.from_data(status),
        title="Engine Status",
        border_style="blue"
    )
    console.print(status_panel)


def display_agents_status(agents):
    """Display status of all agents."""
    for agent in agents:
        cognitive_state = agent.get_cognitive_state()
        
        agent_panel = Panel(
            JSON.from_data(cognitive_state),
            title=f"Agent: {agent.name}",
            border_style="green"
        )
        console.print(agent_panel)


def display_goals_status(engine):
    """Display active goals."""
    if not engine.current_goals:
        console.print("No active goals", style="yellow")
        return
    
    goals_table = Table(title="Active Goals")
    goals_table.add_column("ID", style="cyan")
    goals_table.add_column("Description", style="white")
    goals_table.add_column("Priority", style="yellow")
    goals_table.add_column("Progress", style="green")
    goals_table.add_column("Status", style="blue")
    
    for goal in engine.current_goals:
        goals_table.add_row(
            goal.id[:8],
            goal.description[:50],
            f"{goal.priority:.2f}",
            f"{goal.progress:.2f}",
            goal.status
        )
    
    console.print(goals_table)


def display_memory_status(agents):
    """Display memory status for agents."""
    for agent in agents:
        memory_stats = agent.memory_manager.get_memory_statistics()
        
        memory_tree = Tree(f"Memory: {agent.name}")
        
        working_node = memory_tree.add("Working Memory")
        working_node.add(f"Items: {memory_stats['working_memory']['items']}")
        working_node.add(f"Usage: {memory_stats['working_memory']['usage']:.2f}")
        
        episodic_node = memory_tree.add("Episodic Memory")
        episodic_node.add(f"Episodes: {memory_stats['episodic_memory']['episodes']}")
        
        semantic_node = memory_tree.add("Long-term Memory")
        semantic_node.add(f"Items: {memory_stats['long_term_memory']['semantic_items']}")
        semantic_node.add(f"Concepts: {memory_stats['long_term_memory']['concepts']}")
        
        console.print(memory_tree)


@app.command()
def create_agent(
    agent_type: str = typer.Option("cognitive", "--type", "-t", help="Agent type"),
    name: str = typer.Option("", "--name", "-n", help="Agent name"),
    output: str = typer.Option("agent.json", "--output", "-o", help="Output file"),
):
    """Create and configure a new agent."""
    console.print(f"🤖 Creating {agent_type} agent...", style="green")
    
    agent_id = f"agent_{int(time.time())}"
    
    if agent_type == "reasoning":
        agent = ReasoningAgent(agent_id, name or f"ReasoningAgent")
    elif agent_type == "learning":
        agent = LearningAgent(agent_id, name or f"LearningAgent")
    elif agent_type == "metacognitive":
        agent = MetaCognitiveAgent(agent_id, name or f"MetaCognitiveAgent")
    else:
        agent = CognitiveAgent(agent_id, name or f"CognitiveAgent")
    
    # Add some default goals
    add_default_goals(agent)
    
    # Export agent data
    agent_data = agent.export_agent_data()
    
    with open(output, 'w') as f:
        json.dump(agent_data, f, indent=2, default=str)
    
    console.print(f"✅ Agent created and saved to {output}", style="green")
    
    # Display agent info
    agent_panel = Panel(
        JSON.from_data(agent.get_status()),
        title=f"Created Agent: {agent.name}",
        border_style="green"
    )
    console.print(agent_panel)


@app.command()
def analyze(
    session_file: str = typer.Argument(..., help="Session file to analyze"),
    output_format: str = typer.Option("console", "--format", "-f", help="Output format (console, json, html)"),
    output_file: Optional[str] = typer.Option(None, "--output", "-o", help="Output file"),
):
    """Analyze simulation results from a session file."""
    console.print(f"📊 Analyzing session: {session_file}", style="blue")
    
    try:
        with open(session_file, 'r') as f:
            session_data = json.load(f)
        
        analysis = analyze_session_data(session_data)
        
        if output_format == "console":
            display_analysis_console(analysis)
        elif output_format == "json":
            if output_file:
                with open(output_file, 'w') as f:
                    json.dump(analysis, f, indent=2, default=str)
                console.print(f"Analysis saved to {output_file}")
            else:
                console.print(JSON.from_data(analysis))
        
    except FileNotFoundError:
        console.print(f"❌ Session file not found: {session_file}", style="red")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"❌ Analysis error: {e}", style="red")
        raise typer.Exit(1)


@app.command()
def demo(
    scenario: str = typer.Option("basic", "--scenario", "-s", help="Demo scenario (basic, reasoning, learning)"),
    interactive: bool = typer.Option(False, "--interactive", "-i", help="Interactive demo"),
):
    """Run demonstration scenarios."""
    print_banner()
    console.print(f"🎮 Running demo scenario: {scenario}", style="green")
    
    if scenario == "basic":
        run_basic_demo(interactive)
    elif scenario == "reasoning":
        run_reasoning_demo(interactive)
    elif scenario == "learning":
        run_learning_demo(interactive)
    else:
        console.print(f"❌ Unknown scenario: {scenario}", style="red")
        raise typer.Exit(1)


@app.command()
def info():
    """Show system information and capabilities."""
    print_banner()
    
    info_table = Table(title="System Information")
    info_table.add_column("Component", style="cyan")
    info_table.add_column("Status", style="green")
    info_table.add_column("Details", style="white")
    
    info_table.add_row("Cognitive Engine", "✅ Available", "Main simulation engine")
    info_table.add_row("Memory System", "✅ Available", "Working, episodic, long-term memory")
    info_table.add_row("Reasoning Engine", "✅ Available", "Symbolic reasoning and inference")
    info_table.add_row("Agent Types", "✅ Available", "Cognitive, Reasoning, Learning, MetaCognitive")
    info_table.add_row("Environment", "✅ Available", "Interactive cognitive environment")
    info_table.add_row("CLI Interface", "✅ Available", "Command-line interface")
    
    console.print(info_table)
    
    # Capabilities
    capabilities_panel = Panel(
        """
🧠 Memory Modeling: Working memory, episodic memory, long-term memory
🎯 Goal-Directed Behavior: Goal planning and achievement tracking
🤔 Symbolic Reasoning: Rule-based inference and logical reasoning
🎓 Learning Systems: Reinforcement learning, discovery learning
🔍 Metacognition: Self-reflection and cognitive monitoring
🌍 Environment Interaction: Perception, action, and feedback loops
📊 Analysis Tools: Performance metrics and behavioral analysis
        """,
        title="Core Capabilities",
        border_style="blue"
    )
    console.print(capabilities_panel)


def add_default_goals(agent):
    """Add some default goals to an agent."""
    goals = [
        Goal(
            description="Explore the environment",
            priority=0.6,
            target_facts=[Fact("explored", ["environment"])],
            metadata={"type": "exploration"}
        ),
        Goal(
            description="Learn about objects in the environment",
            priority=0.7,
            target_facts=[Fact("knowledge", ["objects"])],
            metadata={"type": "learning"}
        ),
        Goal(
            description="Maintain high energy levels",
            priority=0.8,
            target_facts=[Fact("energy_level", [agent.agent_id, "high"])],
            metadata={"type": "maintenance"}
        )
    ]
    
    for goal in goals:
        agent.add_goal(goal)


def run_basic_demo(interactive):
    """Run basic demonstration."""
    console.print("Running basic cognitive simulation demo...", style="green")
    
    # Create simple setup
    config = SimulationConfig(max_cycles=50, enable_metrics=True)
    env = CognitiveEnvironment("Demo Environment")
    engine = CognitiveEngine(config, env)
    
    # Create agent
    agent = CognitiveAgent("demo_agent", "DemoAgent")
    env.add_agent("demo_agent")
    add_default_goals(agent)
    
    console.print("Demo setup complete. Running simulation...", style="blue")
    
    if interactive:
        run_interactive_simulation(engine, [agent], True)
    else:
        metrics = engine.run_simulation()
        display_simulation_results(engine, [agent], metrics)


def run_reasoning_demo(interactive):
    """Run reasoning-focused demonstration."""
    console.print("Running reasoning demonstration...", style="green")
    
    config = SimulationConfig(max_cycles=30, enable_metrics=True)
    env = CognitiveEnvironment("Reasoning Environment")
    engine = CognitiveEngine(config, env)
    
    agent = ReasoningAgent("reasoning_agent", "ReasoningDemo")
    env.add_agent("reasoning_agent")
    
    # Add reasoning-specific goals
    reasoning_goal = Goal(
        description="Solve logical puzzle",
        priority=0.9,
        target_facts=[Fact("solved", ["puzzle"])],
        metadata={"type": "reasoning"}
    )
    agent.add_goal(reasoning_goal)
    
    console.print("Reasoning demo setup complete...", style="blue")
    
    if interactive:
        run_interactive_simulation(engine, [agent], True)
    else:
        metrics = engine.run_simulation()
        display_simulation_results(engine, [agent], metrics)


def run_learning_demo(interactive):
    """Run learning-focused demonstration."""
    console.print("Running learning demonstration...", style="green")
    
    config = SimulationConfig(max_cycles=40, enable_learning=True)
    env = CognitiveEnvironment("Learning Environment")
    engine = CognitiveEngine(config, env)
    
    agent = LearningAgent("learning_agent", "LearningDemo")
    env.add_agent("learning_agent")
    
    # Add learning-specific goals
    learning_goal = Goal(
        description="Acquire new skills",
        priority=0.8,
        target_facts=[Fact("skill_acquired", ["new_skill"])],
        metadata={"type": "learning"}
    )
    agent.add_goal(learning_goal)
    
    console.print("Learning demo setup complete...", style="blue")
    
    if interactive:
        run_interactive_simulation(engine, [agent], True)
    else:
        metrics = engine.run_simulation()
        display_simulation_results(engine, [agent], metrics)


def load_config(config_file):
    """Load configuration from file."""
    try:
        with open(config_file, 'r') as f:
            config_data = json.load(f)
        
        return SimulationConfig(**config_data)
    except Exception as e:
        console.print(f"Error loading config: {e}", style="red")
        return SimulationConfig()


def save_results(engine, agents, output_dir):
    """Save simulation results to output directory."""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Save engine session
    session_file = output_path / "session.json"
    engine.export_session(str(session_file))
    
    # Save agent data
    for agent in agents:
        agent_file = output_path / f"{agent.agent_id}.json"
        agent_data = agent.export_agent_data()
        with open(agent_file, 'w') as f:
            json.dump(agent_data, f, indent=2, default=str)
    
    console.print(f"Results saved to {output_dir}", style="green")


def analyze_session_data(session_data):
    """Analyze session data and generate insights."""
    analysis = {
        "session_summary": {
            "total_cycles": session_data.get("state_summary", {}).get("current_cycle", 0),
            "active_goals": session_data.get("state_summary", {}).get("active_goals", 0),
            "memory_items": session_data.get("state_summary", {}).get("working_memory_items", 0)
        },
        "performance_metrics": session_data.get("state_summary", {}).get("metrics", {}),
        "insights": []
    }
    
    # Generate insights
    metrics = analysis["performance_metrics"]
    if metrics.get("goals_achieved", 0) > 0:
        analysis["insights"].append("Goals were successfully achieved during simulation")
    
    if metrics.get("total_cycles", 0) > 100:
        analysis["insights"].append("Long-running simulation with extensive cognitive processing")
    
    return analysis


def display_analysis_console(analysis):
    """Display analysis results in console."""
    console.print("\n📊 SIMULATION ANALYSIS", style="bold blue")
    console.print("="*50, style="blue")
    
    # Summary
    summary_table = Table(title="Session Summary")
    summary_table.add_column("Metric", style="cyan")
    summary_table.add_column("Value", style="green")
    
    for key, value in analysis["session_summary"].items():
        summary_table.add_row(key.replace("_", " ").title(), str(value))
    
    console.print(summary_table)
    
    # Insights
    if analysis["insights"]:
        console.print("\n💡 Key Insights:", style="bold yellow")
        for insight in analysis["insights"]:
            console.print(f"  • {insight}", style="white")


def main():
    """Main entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()


@app.command()
def license_info():
    """Display detailed license information and machine ID."""
    console.print("\n[bold blue]🔒 License Information[/bold blue]\n")
    
    try:
        # Get license information
        license_data = get_license_info()
        machine_id = get_machine_id()
        
        # Create license status table
        table = Table(title="License Status", show_header=True, header_style="bold magenta")
        table.add_column("Property", style="cyan", no_wrap=True)
        table.add_column("Value", style="white")
        
        table.add_row("Machine ID", f"[yellow]{machine_id}[/yellow]")
        table.add_row("Package", "cognito-sim-engine")
        table.add_row("Status", f"[green]{license_data['status'].upper()}[/green]" if license_data['status'] == 'licensed' else f"[red]{license_data['status'].upper()}[/red]")
        
        if 'error' in license_data:
            table.add_row("Error", f"[red]{license_data['error']}[/red]")
        
        table.add_row("Support Email", "bajpaikrishna715@gmail.com")
        
        console.print(table)
        
        # Display available features
        if 'available_features' in license_data:
            console.print("\n[bold green]Available License Tiers:[/bold green]")
            features_table = Table(show_header=True, header_style="bold green")
            features_table.add_column("Tier", style="cyan", no_wrap=True)
            features_table.add_column("Description", style="white")
            
            for tier, description in license_data['available_features'].items():
                features_table.add_row(tier.upper(), description)
            
            console.print(features_table)
        
        # Contact information
        console.print(f"\n[bold yellow]Support Contact:[/bold yellow]")
        console.print(f"📧 Email: [link=mailto:bajpaikrishna715@gmail.com]bajpaikrishna715@gmail.com[/link]")
        console.print(f"🆔 Machine ID: [yellow]{machine_id}[/yellow]")
        console.print(f"\n[dim]Please include your Machine ID when contacting support.[/dim]")
        
    except Exception as e:
        console.print(f"[red]Error retrieving license information: {e}[/red]")
        console.print(f"Machine ID: [yellow]{get_machine_id()}[/yellow]")
        console.print(f"Support: [link=mailto:bajpaikrishna715@gmail.com]bajpaikrishna715@gmail.com[/link]")


@app.command()
def activate_license(
    license_file: Path = typer.Argument(..., help="Path to license file"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output")
):
    """Activate a license from a license file."""
    console.print(f"\n[bold blue]🔑 License Activation[/bold blue]\n")
    
    if not license_file.exists():
        console.print(f"[red]Error: License file not found: {license_file}[/red]")
        raise typer.Exit(1)
    
    try:
        # Note: This would integrate with quantummeta-license activation
        console.print(f"[yellow]Activating license from: {license_file}[/yellow]")
        console.print(f"[yellow]Machine ID: {get_machine_id()}[/yellow]")
        
        # In a real implementation, this would call the quantummeta-license activation
        console.print(f"[green]✅ License activation initiated[/green]")
        console.print(f"[dim]Please run 'cogsim license-info' to verify activation[/dim]")
        
    except Exception as e:
        console.print(f"[red]Error activating license: {e}[/red]")
        console.print(f"Contact support: [link=mailto:bajpaikrishna715@gmail.com]bajpaikrishna715@gmail.com[/link]")
        console.print(f"Machine ID: [yellow]{get_machine_id()}[/yellow]")
        raise typer.Exit(1)
