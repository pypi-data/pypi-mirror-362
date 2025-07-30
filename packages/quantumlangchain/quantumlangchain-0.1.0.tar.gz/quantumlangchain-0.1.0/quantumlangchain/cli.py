"""
Command Line Interface for QuantumLangChain.
"""

import argparse
import asyncio
import json
import logging
from typing import Any, Dict, Optional
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel

from quantumlangchain import (
    QLChain,
    QuantumMemory,
    EntangledAgents,
    QuantumRetriever,
    QiskitBackend
)
from quantumlangchain.core.base import QuantumState

console = Console()
logger = logging.getLogger(__name__)


def setup_logging(level: str = "INFO") -> None:
    """Setup logging configuration."""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )


async def demo_quantum_chain(input_text: str = "Analyze quantum computing applications") -> None:
    """Demonstrate QLChain functionality."""
    
    console.print(Panel.fit("🧬 QuantumLangChain Demo - QLChain", style="bold blue"))
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        
        # Initialize backend
        task1 = progress.add_task("Initializing quantum backend...", total=None)
        backend = QiskitBackend()
        progress.update(task1, description="✅ Quantum backend initialized")
        
        # Initialize memory
        task2 = progress.add_task("Setting up quantum memory...", total=None)
        memory = QuantumMemory(
            classical_dim=256,
            quantum_dim=6,
            backend=backend
        )
        await memory.initialize()
        progress.update(task2, description="✅ Quantum memory ready")
        
        # Initialize chain
        task3 = progress.add_task("Creating QLChain...", total=None)
        chain = QLChain(
            memory=memory,
            backend=backend,
            config={"parallel_branches": 2}
        )
        await chain.initialize()
        progress.update(task3, description="✅ QLChain initialized")
        
        # Execute chain
        task4 = progress.add_task("Running quantum reasoning...", total=None)
        result = await chain.arun(input_text)
        progress.update(task4, description="✅ Quantum processing complete")
    
    # Display results
    console.print("\n📊 Results:")
    console.print(json.dumps(result, indent=2, default=str))
    
    # Display stats
    stats = chain.get_execution_stats()
    
    table = Table(title="QLChain Statistics")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Total Executions", str(stats["total_executions"]))
    table.add_row("Quantum State", stats["quantum_state"])
    table.add_row("Decoherence Level", f"{stats['current_decoherence']:.3f}")
    table.add_row("Entanglement Count", str(stats["entanglement_count"]))
    
    console.print(table)


async def demo_entangled_agents(problem: str = "Optimize quantum circuit design") -> None:
    """Demonstrate EntangledAgents functionality."""
    
    console.print(Panel.fit("🤖 QuantumLangChain Demo - EntangledAgents", style="bold green"))
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        
        # Initialize agents
        task1 = progress.add_task("Creating entangled agents...", total=None)
        agents = EntangledAgents(
            config={
                "agent_count": 3,
                "interference_weight": 0.3,
                "parallel_branches": 2
            }
        )
        await agents.initialize()
        progress.update(task1, description="✅ Agent swarm initialized")
        
        # Collaborative solving
        task2 = progress.add_task("Collaborative problem solving...", total=None)
        solution = await agents.collaborative_solve(problem)
        progress.update(task2, description="✅ Collaborative solution found")
    
    # Display results
    console.print("\n🎯 Collaborative Solution:")
    console.print(json.dumps(solution, indent=2, default=str))
    
    # System status
    status = await agents.get_system_status()
    
    agent_table = Table(title="Agent System Status")
    agent_table.add_column("Agent ID", style="cyan")
    agent_table.add_column("Role", style="yellow")
    agent_table.add_column("Quantum State", style="green")
    agent_table.add_column("Entangled With", style="magenta")
    
    for agent_id, agent_info in status["agent_status"].items():
        entangled = ", ".join(agent_info["entangled_with"][:2])  # Show first 2
        if len(agent_info["entangled_with"]) > 2:
            entangled += "..."
        
        agent_table.add_row(
            agent_id,
            agent_info["role"],
            agent_info["quantum_state"],
            entangled or "None"
        )
    
    console.print(agent_table)


async def demo_quantum_memory(test_data: Optional[Dict[str, Any]] = None) -> None:
    """Demonstrate QuantumMemory functionality."""
    
    console.print(Panel.fit("🧠 QuantumLangChain Demo - QuantumMemory", style="bold magenta"))
    
    if test_data is None:
        test_data = {
            "concept_1": "Quantum superposition allows qubits to exist in multiple states",
            "concept_2": "Entanglement creates correlations between quantum particles",
            "concept_3": "Decoherence causes quantum systems to lose their quantum properties"
        }
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        
        # Initialize memory
        task1 = progress.add_task("Initializing quantum memory...", total=None)
        memory = QuantumMemory(
            classical_dim=128,
            quantum_dim=4
        )
        await memory.initialize()
        progress.update(task1, description="✅ Quantum memory initialized")
        
        # Store data
        task2 = progress.add_task("Storing quantum-enhanced data...", total=None)
        for key, value in test_data.items():
            await memory.store(key, value, quantum_enhanced=True)
        progress.update(task2, description="✅ Data stored with quantum enhancement")
        
        # Create entanglement
        task3 = progress.add_task("Creating memory entanglement...", total=None)
        entanglement_id = await memory.entangle_memories(list(test_data.keys()))
        progress.update(task3, description="✅ Memory entanglement created")
        
        # Create snapshot
        task4 = progress.add_task("Creating memory snapshot...", total=None)
        snapshot_id = await memory.create_memory_snapshot()
        progress.update(task4, description="✅ Memory snapshot saved")
        
        # Test retrieval
        task5 = progress.add_task("Testing quantum retrieval...", total=None)
        retrieved = await memory.retrieve("concept_1", quantum_search=True)
        progress.update(task5, description="✅ Quantum retrieval complete")
    
    # Display results
    console.print(f"\n📥 Retrieved data: {retrieved}")
    console.print(f"🔗 Entanglement ID: {entanglement_id}")
    console.print(f"📸 Snapshot ID: {snapshot_id}")
    
    # Memory stats
    stats = await memory.get_stats()
    
    memory_table = Table(title="Quantum Memory Statistics")
    memory_table.add_column("Metric", style="cyan")
    memory_table.add_column("Value", style="green")
    
    memory_table.add_row("Total Entries", str(stats["total_entries"]))
    memory_table.add_row("Quantum Enhanced", str(stats["quantum_enhanced_entries"]))
    memory_table.add_row("Entangled Entries", str(stats["entangled_entries"]))
    memory_table.add_row("Memory Efficiency", f"{stats['memory_efficiency']:.2%}")
    memory_table.add_row("Quantum State", stats["quantum_state"])
    
    console.print(memory_table)


async def demo_quantum_retriever(query: str = "quantum machine learning") -> None:
    """Demonstrate QuantumRetriever functionality."""
    
    console.print(Panel.fit("🔍 QuantumLangChain Demo - QuantumRetriever", style="bold yellow"))
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        
        # Initialize retriever
        task1 = progress.add_task("Initializing quantum retriever...", total=None)
        retriever = QuantumRetriever(
            config={
                "grover_iterations": 3,
                "quantum_speedup": True,
                "max_results": 5
            }
        )
        await retriever.initialize()
        progress.update(task1, description="✅ Quantum retriever ready")
        
        # Perform retrieval
        task2 = progress.add_task("Quantum-enhanced search...", total=None)
        results = await retriever.aretrieve(query, quantum_enhanced=True)
        progress.update(task2, description="✅ Search complete")
    
    # Display results
    console.print(f"\n🔍 Query: '{query}'")
    console.print(f"📋 Found {len(results)} results:")
    
    for i, result in enumerate(results, 1):
        console.print(f"\n{i}. Score: {result.get('score', 0):.3f}")
        console.print(f"   Content: {result.get('content', 'N/A')[:100]}...")
        console.print(f"   Quantum Enhanced: {result.get('quantum_enhanced', False)}")
    
    # Retrieval stats
    stats = await retriever.get_retrieval_stats()
    
    retrieval_table = Table(title="Quantum Retrieval Statistics")
    retrieval_table.add_column("Metric", style="cyan")
    retrieval_table.add_column("Value", style="green")
    
    retrieval_table.add_row("Total Retrievals", str(stats["total_retrievals"]))
    retrieval_table.add_row("Quantum Enhancement Rate", f"{stats['quantum_enhancement_rate']:.2%}")
    retrieval_table.add_row("Average Results/Query", f"{stats['average_results_per_query']:.1f}")
    retrieval_table.add_row("Average Score", f"{stats['average_result_score']:.3f}")
    retrieval_table.add_row("Grover Iterations", str(stats["grover_iterations"]))
    
    console.print(retrieval_table)


async def run_full_demo() -> None:
    """Run comprehensive demo of all components."""
    
    console.print(Panel.fit("🌟 QuantumLangChain - Full System Demo", style="bold white"))
    
    await demo_quantum_chain()
    console.print("\n" + "="*50 + "\n")
    
    await demo_entangled_agents()
    console.print("\n" + "="*50 + "\n")
    
    await demo_quantum_memory()
    console.print("\n" + "="*50 + "\n")
    
    await demo_quantum_retriever()
    
    console.print(Panel.fit("✨ Demo Complete! Thank you for exploring QuantumLangChain!", style="bold green"))


def create_parser() -> argparse.ArgumentParser:
    """Create command line argument parser."""
    
    parser = argparse.ArgumentParser(
        description="QuantumLangChain CLI - Quantum-enhanced AI framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  qlchain demo --full                    # Run complete demo
  qlchain demo --chain "analyze quantum"  # Demo QLChain
  qlchain demo --agents "solve problem"   # Demo EntangledAgents
  qlchain demo --memory                   # Demo QuantumMemory
  qlchain demo --retriever "search term"  # Demo QuantumRetriever
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Demo command
    demo_parser = subparsers.add_parser("demo", help="Run demonstrations")
    demo_parser.add_argument("--full", action="store_true", help="Run full system demo")
    demo_parser.add_argument("--chain", type=str, help="Demo QLChain with input text")
    demo_parser.add_argument("--agents", type=str, help="Demo EntangledAgents with problem")
    demo_parser.add_argument("--memory", action="store_true", help="Demo QuantumMemory")
    demo_parser.add_argument("--retriever", type=str, help="Demo QuantumRetriever with query")
    
    # Info command
    info_parser = subparsers.add_parser("info", help="Show system information")
    info_parser.add_argument("--version", action="store_true", help="Show version")
    info_parser.add_argument("--backends", action="store_true", help="Show available backends")
    
    # Global options
    parser.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    parser.add_argument("--no-color", action="store_true", help="Disable colored output")
    
    return parser


async def handle_demo_command(args) -> None:
    """Handle demo command."""
    
    if args.full:
        await run_full_demo()
    elif args.chain:
        await demo_quantum_chain(args.chain)
    elif args.agents:
        await demo_entangled_agents(args.agents)
    elif args.memory:
        await demo_quantum_memory()
    elif args.retriever:
        await demo_quantum_retriever(args.retriever)
    else:
        console.print("Please specify a demo option. Use --help for details.")


def handle_info_command(args) -> None:
    """Handle info command."""
    
    if args.version:
        from quantumlangchain import __version__
        console.print(f"QuantumLangChain version: {__version__}")
    
    elif args.backends:
        console.print("Available Quantum Backends:")
        console.print("  • Qiskit (IBM Quantum)")
        console.print("  • PennyLane (Xanadu)")
        console.print("  • Amazon Braket (AWS)")
        console.print("  • Cirq (Google)")
        console.print("  • Qulacs (High-performance simulator)")
    
    else:
        console.print("QuantumLangChain - Quantum-enhanced AI Framework")
        console.print("Use --help for available options.")


async def main() -> None:
    """Main CLI entry point."""
    
    parser = create_parser()
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.log_level)
    
    # Handle color output
    if args.no_color:
        console._color_system = None
    
    try:
        if args.command == "demo":
            await handle_demo_command(args)
        elif args.command == "info":
            handle_info_command(args)
        else:
            parser.print_help()
    
    except KeyboardInterrupt:
        console.print("\n[yellow]Demo interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        logger.error(f"CLI error: {e}", exc_info=True)


if __name__ == "__main__":
    asyncio.run(main())
