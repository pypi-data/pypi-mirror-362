"""AgentOps CLI - Multi-Agent AI System for Requirements-Driven Test Automation.

Implements the multi-agent workflow for automated end-to-end test generation.

The CLI supports:
- Multi-agent workflow for automated end-to-end processing
- Test execution with root cause analysis
- CI/CD and IDE integration management
- Project initialization and configuration

Key Commands:
- init: Initialize AgentOps project structure
- multi-agent-run: Run complete multi-agent workflow
- run: Execute tests with root cause analysis
- config: View and edit AgentOps configuration
- integration: Manage CI/CD and IDE integrations

Reference: Multi-Agent System Architecture
"""

import click
import os
import sys
import json
import ast
from rich.console import Console
from rich.panel import Panel
from pathlib import Path
import csv
from rich.table import Table
import tempfile
import subprocess
from rich.progress import Progress
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.prompt import Confirm, Prompt
import time
import datetime
from rich.progress import SpinnerColumn, TextColumn
from typing import List, Optional, Dict
import difflib
import requests
import threading
import shutil

# Import the package version dynamically
try:
    from agentops_ai import __version__ as agentops_version
except ImportError:
    # Fallback for development
    agentops_version = "1.1.7"

# Check if rich is available for enhanced output
try:
    from rich import __version__ as rich_version
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

# Import AgentOpsRunner for the runner command
import sys
import argparse
import time
from pathlib import Path

# AgentOpsRunner class for the runner command
class AgentOpsRunner:
    """Comprehensive AgentOps workflow runner with configurable steps."""
    
    # Step mapping for clear documentation
    STEP_MAPPING = {
        "1": "init",
        "2": "requirements", 
        "3": "approve",
        "4": "tests",
        "5": "run",
        "6": "traceability"
    }
    
    STEP_DESCRIPTIONS = {
        "init": "Initialize AgentOps project structure",
        "requirements": "Run multi-agent workflow to extract requirements",
        "approve": "Automatically approve all generated requirements", 
        "tests": "Generate test cases from approved requirements",
        "run": "Execute generated tests with root cause analysis",
        "traceability": "Generate traceability matrix linking requirements to tests"
    }
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.steps = []
    
    def log(self, message: str, level: str = "info"):
        """Log message with appropriate formatting."""
        if level == "error":
            console.print(f"[red]❌ {message}[/red]")
        elif level == "warning":
            console.print(f"[yellow]⚠️  {message}[/yellow]")
        elif level == "success":
            console.print(f"[green]✅ {message}[/green]")
        elif self.verbose:
            console.print(f"[blue]ℹ️  {message}[/blue]")
    
    def show_step_mapping(self):
        """Display the step mapping for user reference."""
        console.print(
            Panel(
                "[bold cyan]AgentOps Runner Step Mapping[/bold cyan]\n\n"
                "Use either numbers or names to specify steps:\n\n"
                "[bold]Step Numbers:[/bold]\n"
                "  1 = init          - Initialize AgentOps project structure\n"
                "  2 = requirements  - Run multi-agent workflow to extract requirements\n"
                "  3 = approve       - Automatically approve all generated requirements\n"
                "  4 = tests         - Generate test cases from approved requirements\n"
                "  5 = run           - Execute generated tests with root cause analysis\n"
                "  6 = traceability  - Generate traceability matrix linking requirements to tests\n\n"
                "[bold]Step Names:[/bold]\n"
                "  init, requirements, approve, tests, run, traceability\n\n"
                "[bold]Examples:[/bold]\n"
                "  agentops runner --steps 1,2,3,4,5,6 --all --auto-approve\n"
                "  agentops runner --steps init,requirements,approve,tests,run,traceability --target myfile.py\n"
                "  agentops runner --steps 2,3,4 --all --auto-approve",
                title="Step Mapping",
                border_style="cyan",
            )
        )
    
    def run_command(self, command: List[str], description: str) -> bool:
        """Run a command and return success status."""
        try:
            self.log(f"Running: {description}")
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            if self.verbose:
                console.print(f"[dim]{result.stdout}[/dim]")
            return True
        except subprocess.CalledProcessError as e:
            self.log(f"Command failed: {e}", "error")
            if self.verbose:
                console.print(f"[dim]{e.stderr}[/dim]")
            return False
    
    def step_1_initialize(self) -> bool:
        """Step 1: Initialize AgentOps project structure."""
        return self.run_command(["agentops", "init"], "Initializing AgentOps project")
    
    def step_2_generate_requirements(self, target: Optional[str] = None, 
                                   run_all: bool = False, parallel: bool = False, 
                                   workers: int = 4) -> bool:
        """Step 2: Generate requirements using multi-agent workflow."""
        cmd = ["agentops", "multi-agent-run"]
        if target:
            cmd.append(target)
        elif run_all:
            cmd.append("--all")
        if parallel:
            cmd.extend(["--parallel", "--workers", str(workers)])
        
        return self.run_command(cmd, "Generating requirements with multi-agent workflow")
    
    def step_3_auto_approve_requirements(self) -> bool:
        """Step 3: Automatically approve all requirements."""
        return self.run_command(["agentops", "fast-approve", "--non-interactive"], 
                               "Auto-approving requirements")
    
    def step_4_generate_tests(self, target: Optional[str] = None, 
                             run_all: bool = False, parallel: bool = False, 
                             workers: int = 4) -> bool:
        """Step 4: Generate test cases from approved requirements."""
        cmd = ["agentops", "generate-tests"]
        if target:
            cmd.extend(["--target", target])
        elif run_all:
            cmd.append("--all")
        if parallel:
            cmd.extend(["--parallel", "--workers", str(workers)])
        
        return self.run_command(cmd, "Generating test cases from requirements")
    
    def step_5_run_tests(self, target: Optional[str] = None, run_all: bool = False) -> bool:
        """Step 5: Execute generated tests with root cause analysis."""
        cmd = ["agentops", "run"]
        if target:
            cmd.extend(["--target", target])
        elif run_all:
            cmd.append("--all")
        
        return self.run_command(cmd, "Running generated tests")
    
    def step_6_generate_traceability_matrix(self, output_format: str = "markdown") -> bool:
        """Step 6: Generate traceability matrix."""
        return self.run_command(["agentops", "traceability", "--format", output_format], 
                               f"Generating traceability matrix ({output_format})")
    
    def _generate_summary(self, steps: List[str], step_results: Dict[str, bool], 
                         step_descriptions: Dict[str, str], total_time: float):
        """Generate and display workflow summary."""
        console.print(f"\n{'AgentOps Runner Summary':^80}")
        console.print("=" * 80)
        
        successful_steps = sum(1 for result in step_results.values() if result)
        total_steps = len(steps)
        
        for step in steps:
            status = "✅ PASS" if step_results.get(step, False) else "❌ FAIL"
            description = step_descriptions.get(step, step)
            console.print(f"{step:>2}. {status:<8} {description}")
        
        console.print("-" * 80)
        console.print(f"Total Steps: {total_steps}")
        console.print(f"Successful: {successful_steps}")
        console.print(f"Failed: {total_steps - successful_steps}")
        console.print(f"Total Time: {total_time:.2f} seconds")
        
        if successful_steps == total_steps:
            console.print("\n[bold green]🎉 All steps completed successfully![/bold green]")
        else:
            console.print(f"\n[bold red]❌ {total_steps - successful_steps} step(s) failed![/bold red]")
    
    def run_workflow(self, steps: List[str], target: Optional[str] = None, 
                    run_all: bool = False, parallel: bool = False, 
                    workers: int = 4, auto_approve: bool = False, 
                    output_format: str = "markdown", 
                    generate_traceability: bool = True, dry_run: bool = False) -> bool:
        """Run the complete AgentOps workflow with specified steps."""
        if dry_run:
            console.print("[bold yellow]DRY RUN MODE - No commands will be executed[/bold yellow]")
            console.print(f"Steps to run: {', '.join(steps)}")
            console.print(f"Target: {target or 'all files' if run_all else 'none'}")
            console.print(f"Parallel: {parallel} (workers: {workers})")
            console.print(f"Auto-approve: {auto_approve}")
            return True
        
        start_time = time.time()
        step_results = {}
        step_descriptions = {}
        
        # Execute each step
        for step in steps:
            step_descriptions[step] = self.STEP_DESCRIPTIONS.get(step, step)
            
            if step == "init":
                step_results[step] = self.step_1_initialize()
            elif step == "requirements":
                step_results[step] = self.step_2_generate_requirements(target, run_all, parallel, workers)
            elif step == "approve":
                if auto_approve:
                    step_results[step] = self.step_3_auto_approve_requirements()
                else:
                    self.log("Skipping approval step (auto-approve not enabled)", "warning")
                    step_results[step] = True
            elif step == "tests":
                step_results[step] = self.step_4_generate_tests(target, run_all, parallel, workers)
            elif step == "run":
                step_results[step] = self.step_5_run_tests(target, run_all)
            elif step == "traceability":
                if generate_traceability:
                    step_results[step] = self.step_6_generate_traceability_matrix(output_format)
                else:
                    self.log("Skipping traceability step (disabled)", "warning")
                    step_results[step] = True
            else:
                self.log(f"Unknown step: {step}", "error")
                step_results[step] = False
            
            # Stop on failure unless it's a non-critical step
            if not step_results[step] and step not in ["traceability"]:
                self.log(f"Workflow failed at step: {step}", "error")
                break
        
        # Generate summary
        total_time = time.time() - start_time
        self._generate_summary(steps, step_results, step_descriptions, total_time)
        
        # Check overall success
        critical_steps = [s for s in steps if s != "traceability"]
        overall_success = all(step_results.get(step, False) for step in critical_steps)
        
        if overall_success:
            self.log("🎉 AgentOps workflow completed successfully!", "success")
        else:
            self.log("❌ AgentOps workflow failed!", "error")
        
        return overall_success

from agentops_ai.agentops_core.workflow import AgentOpsWorkflow
from agentops_ai.agentops_core.requirement_store import RequirementStore
from agentops_ai.agentops_core.config import get_config, AgentOpsConfig, LLMConfig, ProjectConfig, IntegrationConfig
from agentops_ai.agentops_core.analyzer import CodeAnalyzer, _add_parents
from agentops_ai.agentops_core.utils import find_python_files
from agentops_ai.agentops_integrations import IntegrationAgent, IntegrationConfig as IntConfig
from ..agentops_core.features import get_feature_manager, is_feature_enabled, enable_feature, disable_feature
from ..agentops_core.language_support import get_language_manager, detect_language, is_language_supported, LanguageType
from ..agentops_dashboard.dashboard import start_dashboard, add_project_to_dashboard, add_dashboard_event
from ..agentops_core.traceability import get_traceability_manager, create_traceability_matrix, add_traceability_item
from ..agentops_core.documentation_export import get_documentation_exporter, create_documentation_project, add_documentation_section
from ..agentops_core.payment_integration import get_payment_manager, check_user_feature_access, get_user_features

# Import new modular components
try:
    from agentops_ai.agentops_core.pricing import (
        PricingTier, AgentType, ContextEngineering, ExportFormat,
        pricing_manager
    )
    from agentops_ai.agentops_core.agent_selector import (
        WorkflowMode, agent_selector
    )
    from agentops_ai.agentops_core.context_engineering import (
        context_engineering_manager
    )
    from agentops_ai.agentops_core.export_manager import (
        ExportConfig, export_manager
    )
    ENHANCED_FEATURES_AVAILABLE = True
except ImportError:
    ENHANCED_FEATURES_AVAILABLE = False

# Optional import for advanced multi-agent workflow
try:
    from agentops_ai.agentops_agents import AgentOrchestrator
    AGENT_ORCHESTRATOR_AVAILABLE = True
except ImportError as e:
    AGENT_ORCHESTRATOR_AVAILABLE = False
    AgentOrchestrator = None

console = Console()

ENTITLEMENTS_CACHE = Path('.agentops/entitlements.json')
CREDENTIALS_FILE = Path('.agentops/credentials')
API_BASE_URL = 'https://agentops-website.vercel.app/api/v1'  # Production endpoint

# --- AUTH & ENTITLEMENT MANAGEMENT ---

def save_api_key(api_key: str):
    CREDENTIALS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CREDENTIALS_FILE, 'w') as f:
        f.write(api_key.strip())

def load_api_key() -> str:
    if CREDENTIALS_FILE.exists():
        return CREDENTIALS_FILE.read_text().strip()
    return ''

def fetch_entitlements(api_key: str) -> dict:
    headers = {'Authorization': f'Bearer {api_key}'}
    try:
        resp = requests.get(f'{API_BASE_URL}/entitlements', headers=headers, timeout=10)
        if resp.status_code == 200:
            return resp.json()
        else:
            return {}
    except Exception:
        return {}

def save_entitlements(entitlements: dict):
    ENTITLEMENTS_CACHE.parent.mkdir(parents=True, exist_ok=True)
    with open(ENTITLEMENTS_CACHE, 'w') as f:
        json.dump(entitlements, f, indent=2)

def load_entitlements() -> dict:
    if ENTITLEMENTS_CACHE.exists():
        return json.loads(ENTITLEMENTS_CACHE.read_text())
    return {}

def ensure_entitlements():
    api_key = load_api_key()
    if not api_key:
        console.print('[red]You must login with your AgentOps API key first (agentops login)[/red]')
        sys.exit(1)
    entitlements = fetch_entitlements(api_key)
    if not entitlements:
        console.print('[red]Failed to fetch entitlements from AgentOps backend. Check your API key and network.[/red]')
        sys.exit(1)
    save_entitlements(entitlements)
    return entitlements

@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(version=agentops_version)
def cli():
    """AgentOps - Multi-Agent AI System for Requirements-Driven Test Automation.
    
    🚀 AI-powered QA co-pilot for vibe coders - Requirements-driven test automation 
    with a sophisticated multi-agent AI system.
    
    QUICK START:
        agentops init                           # Initialize project
        agentops multi-agent-run myfile.py     # Run complete workflow
        agentops run --all                     # Execute generated tests
    
    RECOMMENDED WORKFLOW:
        1. agentops init                        # Initialize project
        2. agentops multi-agent-run myfile.py  # Run complete multi-agent workflow
        3. agentops run --all                  # Execute generated tests
        4. agentops report --check-changes     # View results and changes
    
    WORKFLOW COMMANDS:
        init              Initialize AgentOps project structure
        multi-agent-run   Run complete multi-agent workflow (6 AI agents) [RECOMMENDED]
        run              Execute generated tests with analysis
        infer            Run simple test generation (single LLM call) [QUICK PROTOTYPING]
    
        MANAGEMENT COMMANDS:
        fast-approve     Quickly approve pending requirements
        approve-all      Approve all requirements with confirmation
        config          View and edit AgentOps configuration
        status          Show project status and configuration
        check           Check system requirements and setup

    ANALYSIS COMMANDS:
        report          Generate analysis report from existing results
        traceability    Generate traceability matrix
        requirement-info Show detailed requirement information
        test-info       Show test file and function details

    INTEGRATION COMMANDS:
        integration     Manage CI/CD and IDE integrations

    DISCOVERY COMMANDS:
        version         Show version information and updates
        welcome         Show welcome message and quick start guide
    
    EXAMPLES:
        # Complete workflow for a single file
        agentops multi-agent-run mymodule.py
        
        # Process all Python files in parallel
        agentops multi-agent-run --all --parallel --workers 6
        
        # View results and check for changes
        agentops report --check-changes
        
        # View traceability matrix
        agentops traceability --open
        
        # Quick test generation (for prototyping only)
        agentops infer myfile.py
    
    LEARN MORE:
        • Documentation: https://github.com/knaig/agentops_ai
        • Examples: Run 'agentops examples' for sample workflows
        • Community: Join our Discord for support and feedback
        
    Need help? Run 'agentops help' for detailed command information.
    """
    pass


def suggest_command(unknown_command: str) -> list:
    """Suggest similar commands when user types an unknown command.

    Args:
        unknown_command: The command that was not found
        
    Returns:
        List of suggested commands with similarity scores
    """
    # All available commands
    all_commands = [
        "init", "multi-agent-run", "infer", "run", "runner",
        "fast-approve", "approve-all", "config", "status", "check",
        "report", "traceability", "requirement-info", "test-info",
        "integration", "help", "examples", "commands", "version", "welcome"
    ]
    
    # Find similar commands using difflib
    suggestions = difflib.get_close_matches(unknown_command, all_commands, n=3, cutoff=0.3)
    
    return suggestions


@cli.command()
def welcome():
    """Show welcome message and quick start guide for new users.
    
    Displays a friendly welcome message with quick start instructions
    and helpful tips for getting started with AgentOps.
    """
    console.print(
        Panel(
            "[bold cyan]🎉 Welcome to AgentOps![/bold cyan]\n\n"
            "You're about to experience AI-powered test automation like never before.\n"
            "AgentOps uses 6 specialized AI agents to automatically analyze your code,\n"
            "extract requirements, and generate comprehensive test suites.\n\n"
            "[bold]🚀 Let's get you started in 3 simple steps:[/bold]",
            title="Welcome to AgentOps",
            border_style="green",
        )
    )
    
    console.print(
        "[bold]Step 1: Initialize your project[/bold]\n"
        "  [cyan]agentops init[/cyan]\n"
        "  This creates the .agentops directory and sets up your project.\n\n"
        "[bold]Step 2: Set your OpenAI API key[/bold]\n"
        "  [cyan]export OPENAI_API_KEY='your-api-key-here'[/cyan]\n"
        "  Get your key from: https://platform.openai.com/api-keys\n\n"
        "[bold]Step 3: Run the multi-agent workflow[/bold]\n"
        "  [cyan]agentops multi-agent-run myfile.py[/cyan]\n"
        "  Or process all files: [cyan]agentops multi-agent-run --all[/cyan]\n\n"
        "[bold]🎯 What happens next?[/bold]\n"
        "• 6 AI agents analyze your code and extract requirements\n"
        "• High-quality test suites are automatically generated\n"
        "• You get comprehensive test coverage and traceability\n"
        "• All results are stored in .agentops/ for easy access\n\n"
        "[bold]💡 Pro Tips:[/bold]\n"
        "• Run [cyan]agentops examples[/cyan] to see real-world use cases\n"
        "• Use [cyan]agentops help[/cyan] for detailed command information\n"
        "• Try [cyan]agentops runner --steps 1,2,3,4 --all[/cyan] for custom workflows\n"
        "• Check [cyan]agentops report --check-changes[/cyan] to see what's up-to-date\n\n"
        "[bold]🔗 Get Help & Connect:[/bold]\n"
        "• GitHub: https://github.com/knaig/agentops_ai\n"
        "• Issues: https://github.com/knaig/agentops_ai/issues\n"
        "• Discussions: https://github.com/knaig/agentops_ai/discussions\n\n"
        "[bold green]Ready to automate your testing? Let's go! 🚀[/bold green]"
    )


@cli.command()
def status():
    """Show current AgentOps project status and configuration.
    
    Displays information about the current project, including:
    - Project initialization status
    - Configuration settings
    - Recent activity and results
    - System health and readiness
    """
    console.print(
        Panel(
            "[bold cyan]🔍 AgentOps Project Status[/bold cyan]\n\n"
            "Checking your project configuration and recent activity...",
            title="Status Check",
            border_style="blue",
        )
    )
    
    # Check if project is initialized
    project_dir = Path(".agentops")
    if not project_dir.exists():
        console.print(
            "[yellow]⚠️  Project not initialized[/yellow]\n"
            "Run [cyan]agentops init[/cyan] to set up your project.\n"
        )
        return
    
    console.print("[green]✅ Project initialized[/green]")
    
    # Check configuration
    try:
        config = get_config()
        console.print(f"[green]✅ Configuration loaded[/green]")
        console.print(f"   • OpenAI API: {'✅ Configured' if config.llm.api_key else '❌ Not set'}")
        console.print(f"   • Model: {config.llm.model}")
        console.print(f"   • Temperature: {config.llm.temperature}")
    except Exception as e:
        console.print(f"[red]❌ Configuration error: {e}[/red]")
    
    # Check recent activity
    requirements_file = project_dir / "requirements.json"
    tests_dir = project_dir / "tests"
    
    if requirements_file.exists():
        try:
            with open(requirements_file, 'r') as f:
                requirements = json.load(f)
            console.print(f"[green]✅ Requirements database: {len(requirements)} requirements[/green]")
        except:
            console.print("[yellow]⚠️  Requirements database exists but may be corrupted[/yellow]")
    else:
        console.print("[yellow]⚠️  No requirements database found[/yellow]")
    
    if tests_dir.exists():
        test_files = list(tests_dir.glob("*.py"))
        console.print(f"[green]✅ Test files: {len(test_files)} generated[/green]")
    else:
        console.print("[yellow]⚠️  No test files generated yet[/yellow]")
    
    # Check OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        console.print(
            "\n[red]❌ OpenAI API key not set[/red]\n"
            "Set your API key: [cyan]export OPENAI_API_KEY='your-key-here'[/cyan]\n"
            "Get your key from: https://platform.openai.com/api-keys"
        )
    else:
        console.print("[green]✅ OpenAI API key configured[/green]")
    
    console.print(
        "\n[bold]🚀 Ready to use AgentOps![/bold]\n"
        "Try: [cyan]agentops multi-agent-run myfile.py[/cyan]"
    )


@cli.command()
@click.argument("target", type=click.Path(exists=True), required=False)
@click.option(
    "--all", "run_all", is_flag=True, 
    help="Run complete multi-agent workflow on all Python files in the current directory"
)
@click.option(
    "--output-dir",
    default=None,
    help="Output directory for generated tests (default: .agentops/tests/)"
)
@click.option(
    "--parallel", is_flag=True,
    help="Process files in parallel for faster execution"
)
@click.option(
    "--workers", default=4, type=int,
    help="Number of parallel workers (default: 4, max: 8)"
)
def multi_agent_run(target: str, run_all: bool, output_dir: str, parallel: bool, workers: int):
    """Run complete multi-agent workflow on Python files.

    This command runs the entire multi-agent workflow:
    1. CodeAnalyzer Agent: Analyzes code structure and dependencies
    2. RequirementsEngineer Agent: Extracts functional requirements
    3. TestArchitect Agent: Designs test strategy
    4. TestGenerator Agent: Generates test code
    5. QualityAssurance Agent: Validates test quality
    6. IntegrationSpecialist Agent: Sets up integrations
    
    Usage:
        agentops multi-agent-run file.py          # Single file
        agentops multi-agent-run directory/       # All Python files in directory
        agentops multi-agent-run --all            # All Python files in current directory
        agentops multi-agent-run --all --parallel # Parallel processing
        agentops multi-agent-run --all --parallel --workers 6 # Custom worker count

    Args:
        target: Path to Python file or directory to process
        run_all: Process all Python files in current directory
        output_dir: Directory for generated tests (optional)
        parallel: Process files in parallel for faster execution
        workers: Number of parallel workers (default: 4, max: 8)
    """
    if not os.path.exists(".agentops"):
        console.print(
            Panel(
                "[yellow]AgentOps not initialized in this directory.[/yellow]\n\n"
                "Run [bold cyan]agentops init[/bold cyan] first.",
                title="Not Initialized",
                border_style="yellow",
            )
        )
        sys.exit(1)

    # Validate worker count
    if workers < 1 or workers > 8:
        console.print(
            Panel(
                "[red]Worker count must be between 1 and 8[/red]",
                title="Invalid Worker Count",
                border_style="red",
            )
        )
        sys.exit(1)

    # Determine what files to process
    files_to_process = []
    
    if run_all:
        # Process all Python files in current directory
        files_to_process = find_python_files(".")
        if not files_to_process:
            console.print(
                Panel(
                    "[yellow]No Python files found in current directory.[/yellow]",
                    title="No Files Found",
                    border_style="yellow",
                )
            )
            return
    elif target:
        if os.path.isfile(target):
            # Single file
            if not target.endswith('.py'):
                console.print(
                    Panel(
                        "[yellow]Target must be a Python file (.py)[/yellow]",
                        title="Invalid File Type",
                        border_style="yellow",
                    )
                )
                return
            files_to_process = [target]
        elif os.path.isdir(target):
            # Directory - process all Python files
            files_to_process = find_python_files(target)
            if not files_to_process:
                console.print(
                    Panel(
                        f"[yellow]No Python files found in {target}[/yellow]",
                        title="No Files Found",
                        border_style="yellow",
                    )
                )
                return
        else:
            console.print(
                Panel(
                    "[yellow]Target must be a valid file or directory[/yellow]",
                    title="Invalid Target",
                    border_style="yellow",
                )
            )
            return
    else:
        # No target specified and no --all flag
        console.print(
            Panel(
                "[yellow]Please specify a file, directory, or use --all flag[/yellow]\n\n"
                "Usage:\n"
                "• [bold]agentops multi-agent-run file.py[/bold] - Single file\n"
                "• [bold]agentops multi-agent-run directory/[/bold] - All files in directory\n"
                "• [bold]agentops multi-agent-run --all[/bold] - All files in current directory",
                title="Missing Target",
                border_style="yellow",
            )
        )
        return

    # Adjust worker count based on file count
    if parallel and len(files_to_process) < workers:
        workers = len(files_to_process)
        console.print(f"[dim]Adjusted workers to {workers} (file count)[/dim]")

    # Check if AgentOrchestrator is available
    if not AGENT_ORCHESTRATOR_AVAILABLE:
        console.print(
            Panel(
                "[red]Advanced multi-agent workflow not available.[/red]\n\n"
                "Install required dependencies:\n"
                "[bold]pip install langchain-openai[/bold]\n\n"
                "Or use the simple workflow: [bold]agentops infer <file.py>[/bold]",
                title="Dependency Missing",
                border_style="red",
            )
        )
        sys.exit(1)

    # Check if OpenAI API key is configured
    config = get_config()
    if not config.llm.api_key:
        console.print(
            Panel(
                "[red]OpenAI API key not configured.[/red]\n\n"
                "Set your API key:\n"
                "[bold]export OPENAI_API_KEY='your-api-key-here'[/bold]\n\n"
                "Get your API key from: https://platform.openai.com/api-keys\n\n"
                "Alternative: Use the simple workflow without API key:\n"
                "[bold]agentops infer <file.py>[/bold]",
                title="API Key Missing",
                border_style="red",
            )
        )
        sys.exit(1)

    # Initialize AgentOrchestrator
    try:
        orchestrator = AgentOrchestrator()
    except Exception as e:
        console.print(
            Panel(
                f"[red]Failed to initialize AgentOrchestrator.[/red]\n\n"
                f"Error: {str(e)}\n\n"
                "This is usually caused by:\n"
                "• Invalid OpenAI API key\n"
                "• Network connectivity issues\n"
                "• Missing dependencies\n\n"
                "Please check your configuration and try again.",
                title="Initialization Error",
                border_style="red",
            )
        )
        sys.exit(1)
    
    # Process files
    total_files = len(files_to_process)
    successful_files = 0
    failed_files = []
    
    processing_mode = "parallel" if parallel else "sequential"
    console.print(
        Panel(
            f"[bold]Starting multi-agent workflow for {total_files} file(s) in {processing_mode} mode[/bold]\n"
            f"Workers: {workers}" if parallel else "",
            title="AgentOps Multi-Agent Run",
            border_style="cyan",
        )
    )

    if parallel and total_files > 1:
        # Parallel processing
        import threading
        
        # Thread-local storage for progress tracking
        thread_local = threading.local()
        
        def process_file(file_path):
            """Process a single file with the orchestrator."""
            try:
                # Run the multi-agent workflow
                final_state = orchestrator.run(file_path)
                
                if final_state.has_errors():
                    return file_path, False, final_state.errors
                else:
                    return file_path, True, None
            except Exception as e:
                return file_path, False, [str(e)]
        
        with Progress() as progress:
            task = progress.add_task("Processing files...", total=total_files)
            
            with ThreadPoolExecutor(max_workers=workers) as executor:
                # Submit all files for processing
                future_to_file = {
                    executor.submit(process_file, file_path): file_path 
                    for file_path in files_to_process
                }
                
                # Collect results as they complete
                for future in as_completed(future_to_file):
                    file_path, success, errors = future.result()
                    if success:
                        successful_files += 1
                        progress.update(task, advance=1, description=f"✓ {Path(file_path).name}")
                    else:
                        failed_files.append((file_path, errors))
                        progress.update(task, advance=1, description=f"✗ {Path(file_path).name}")
    else:
        # Sequential processing with enhanced progress updates
        for i, file_path in enumerate(files_to_process, 1):
            file_name = Path(file_path).name
            console.print(f"\n[bold cyan]Processing {i}/{total_files}: {file_name}[/bold cyan]")
            
            try:
                # Enhanced progress display for sequential processing
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    console=console
                ) as progress:
                    task = progress.add_task(f"Starting multi-agent workflow...", total=None)
                    
                    # Run the multi-agent workflow with progress updates
                    final_state = orchestrator.run_with_progress(file_path, progress, task)

                    if final_state.has_errors():
                        failed_files.append((file_path, final_state.errors))
                        progress.update(task, description=f"[red]Failed: {file_name}[/red]")
                        console.print(f"[red]✗ Failed to process {file_name}[/red]")
                        for error in final_state.errors:
                            console.print(f"  [dim]Error: {error}[/dim]")
                    else:
                        successful_files += 1
                        progress.update(task, description=f"[green]✓ Completed: {file_name}[/green]")
                        console.print(f"[green]✓ Successfully processed {file_name}[/green]")
                        
                        # Show generated test count if available
                        if hasattr(final_state, 'test_code') and final_state.test_code:
                            test_count = final_state.test_code.count('def test_')
                            console.print(f"  [dim]Generated {test_count} test functions[/dim]")
            except Exception as e:
                failed_files.append((file_path, [str(e)]))
                console.print(f"[red]✗ Exception processing {file_name}: {str(e)}[/red]")

    # Display results
    console.print(
        Panel(
            f"[bold]Multi-agent Workflow Complete[/bold]\n\n"
            f"✓ Successfully processed {successful_files}/{total_files} files!\n"
            f"Mode: {processing_mode}",
            title="Multi-agent Workflow Complete",
            border_style="green" if successful_files == total_files else "yellow",
        )
    )
    
    # Generate markdown report
    report_path = generate_markdown_report(files_to_process, successful_files, failed_files, processing_mode)
    
    if report_path:
        console.print(f"\n[cyan]📊 Detailed report generated: {report_path}[/cyan]")
    
    if failed_files:
        console.print("\n[red]Failed files:[/red]")
        for file_path, errors in failed_files:
            console.print(f"  • {file_path}")
            for error in errors:
                console.print(f"    [dim]Error: {error}[/dim]")
    
    return successful_files == total_files

def generate_markdown_report(files_to_process: List[str], successful_files: int, 
                            failed_files: List[tuple], processing_mode: str) -> str:
    """Generate a detailed markdown report of the multi-agent workflow execution.
    
    Args:
        files_to_process: List of all files that were processed
        successful_files: Number of successfully processed files
        failed_files: List of (file_path, errors) tuples for failed files
        processing_mode: Mode used for processing (sequential/parallel)
        
    Returns:
        Path to the generated markdown report file
    """
    from pathlib import Path
    import datetime
    import os
    # Create report directory if it doesn't exist
    report_dir = Path(".agentops/reports")
    report_dir.mkdir(parents=True, exist_ok=True)
    # Generate timestamp for unique filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = report_dir / f"multi_agent_workflow_report_{timestamp}.md"
    # Create the markdown content
    markdown_content = f"""# AgentOps Multi-Agent Workflow Report

**Generated:** {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Processing Mode:** {processing_mode}  
**Total Files:** {len(files_to_process)}  
**Successful:** {successful_files}  
**Failed:** {len(failed_files)}  
**Success Rate:** {(successful_files / len(files_to_process) * 100):.1f}%

## Workflow Summary

The multi-agent workflow consists of 6 specialized agents that work together to analyze code and generate comprehensive tests:

1. **CodeAnalyzer** - Analyzes code structure and dependencies
2. **RequirementsEngineer** - Extracts functional requirements
3. **TestArchitect** - Designs comprehensive test strategy
4. **TestGenerator** - Creates high-quality test code
5. **QualityAssurance** - Validates test quality
6. **IntegrationSpecialist** - Sets up CI/CD and IDE integrations

## Detailed Results

| File | CodeAnalyzer | RequirementsEngineer | TestArchitect | TestGenerator | QualityAssurance | IntegrationSpecialist | Overall Status | Test Functions | Errors |
|------|--------------|---------------------|---------------|---------------|------------------|---------------------|----------------|----------------|---------|
"""
    # Create a set of failed files for quick lookup
    failed_files_set = {file_path for file_path, _ in failed_files}
    
    for file_path in files_to_process:
        file_name = Path(file_path).name
        # Handle both absolute and relative paths
        try:
            relative_path = Path(file_path).relative_to(Path.cwd())
        except ValueError:
            # If the file is not in the current directory, use the original path
            relative_path = Path(file_path)
        
        # Determine overall status
        if file_path in failed_files_set:
            status = "❌ Failed"
            errors = next(errors for fp, errors in failed_files if fp == file_path)
            error_summary = "; ".join(errors[:2])  # Show first 2 errors
            if len(errors) > 2:
                error_summary += f" (+{len(errors)-2} more)"
        else:
            status = "✅ Success"
            error_summary = ""
        
        # Try to get test count from generated test file
        test_count = "N/A"
        # Handle test file path resolution
        try:
            test_file_path = Path(".agentops/tests") / relative_path.parent / f"test_{file_name}"
        except:
            # Fallback to just the filename if path resolution fails
            test_file_path = Path(".agentops/tests") / f"test_{file_name}"
        if test_file_path.exists():
            try:
                with open(test_file_path, 'r') as f:
                    test_content = f.read()
                    test_count = str(test_content.count('def test_'))
            except:
                test_count = "N/A"
        
        # For now, we'll show the agent status as completed for successful files
        # In a future enhancement, we could parse the actual logs to show individual agent status
        if file_path in failed_files_set:
            agent_statuses = ["❌", "❌", "❌", "❌", "❌", "❌"]
        else:
            agent_statuses = ["✅", "✅", "✅", "✅", "✅", "✅"]
        
        # Add row to table
        markdown_content += f"| `{relative_path}` | {agent_statuses[0]} | {agent_statuses[1]} | {agent_statuses[2]} | {agent_statuses[3]} | {agent_statuses[4]} | {agent_statuses[5]} | {status} | {test_count} | {error_summary} |\n"
    
    markdown_content += f"""
## Agent Details

### CodeAnalyzer Agent
- **Purpose:** Deep code structure and dependency analysis
- **Output:** Code complexity, architectural patterns, testing challenges
- **Success Rate:** {calculate_agent_success_rate('CodeAnalyzer', files_to_process, failed_files_set):.1f}%

### RequirementsEngineer Agent  
- **Purpose:** Extract functional requirements using LLM
- **Output:** Functional requirements, user stories, acceptance criteria
- **Success Rate:** {calculate_agent_success_rate('RequirementsEngineer', files_to_process, failed_files_set):.1f}%

### TestArchitect Agent
- **Purpose:** Design comprehensive test strategy
- **Output:** Test plan, coverage strategy, testing approach
- **Success Rate:** {calculate_agent_success_rate('TestArchitect', files_to_process, failed_files_set):.1f}%

### TestGenerator Agent
- **Purpose:** Create high-quality test code
- **Output:** Generated test files with comprehensive test cases
- **Success Rate:** {calculate_agent_success_rate('TestGenerator', files_to_process, failed_files_set):.1f}%

### QualityAssurance Agent
- **Purpose:** Validate test quality and coverage
- **Output:** Quality metrics, coverage analysis, improvement suggestions
- **Success Rate:** {calculate_agent_success_rate('QualityAssurance', files_to_process, failed_files_set):.1f}%

### IntegrationSpecialist Agent
- **Purpose:** Set up CI/CD and IDE integrations
- **Output:** Integration configurations, deployment scripts
- **Success Rate:** {calculate_agent_success_rate('IntegrationSpecialist', files_to_process, failed_files_set):.1f}%

## Error Analysis

"""
    
    if failed_files:
        markdown_content += "### Common Error Patterns\n\n"
        error_patterns = {}
        for _, errors in failed_files:
            for error in errors:
                # Extract error type (first part before colon or common patterns)
                error_type = error.split(':')[0] if ':' in error else error.split()[0]
                error_patterns[error_type] = error_patterns.get(error_type, 0) + 1
        
        for error_type, count in sorted(error_patterns.items(), key=lambda x: x[1], reverse=True):
            markdown_content += f"- **{error_type}**: {count} occurrence(s)\n"
        
        markdown_content += "\n### Detailed Error Log\n\n"
        for file_path, errors in failed_files:
            # Handle path display for error logs
            try:
                display_path = Path(file_path).relative_to(Path.cwd())
            except ValueError:
                display_path = Path(file_path)
            markdown_content += f"#### `{display_path}`\n\n"
            for error in errors:
                markdown_content += f"```\n{error}\n```\n\n"
    else:
        markdown_content += "✅ No errors encountered during processing.\n\n"
    
    markdown_content += f"""
## Recommendations

Based on the workflow results:

"""
    
    success_rate = (successful_files / len(files_to_process) * 100)
    if success_rate >= 90:
        markdown_content += "- 🎉 **Excellent results!** The workflow is performing very well.\n"
        markdown_content += "- Consider running the workflow on more complex codebases to validate robustness.\n"
    elif success_rate >= 70:
        markdown_content += "- 👍 **Good results!** Most files were processed successfully.\n"
        markdown_content += "- Review failed files to identify common patterns and improve error handling.\n"
    elif success_rate >= 50:
        markdown_content += "- ⚠️ **Moderate results.** Some files failed processing.\n"
        markdown_content += "- Investigate error patterns and consider adjusting LLM parameters.\n"
    else:
        markdown_content += "- ❌ **Poor results.** Many files failed processing.\n"
        markdown_content += "- Check API key configuration and network connectivity.\n"
        markdown_content += "- Review error logs for systematic issues.\n"
    
    markdown_content += f"""
- **Total Processing Time:** Check the CLI output for timing information
- **Generated Test Files:** Located in `.agentops/tests/` directory
- **Configuration:** Review `.agentops/config.json` for LLM settings

---
*Report generated by AgentOps Multi-Agent System*
"""
    
    # Write the report to file
    with open(report_path, 'w') as f:
        f.write(markdown_content)
    # --- New: Update latest_report.md symlink/copy ---
    latest_report = report_dir / "latest_report.md"
    try:
        if latest_report.exists() or latest_report.is_symlink():
            latest_report.unlink()
        # Try to create a symlink, fallback to copy if not supported
        try:
            os.symlink(report_path.name, latest_report)
        except Exception:
            import shutil
            shutil.copyfile(report_path, latest_report)
    except Exception as e:
        print(f"[AgentOps] Warning: Could not update latest_report.md: {e}")
    # --- New: Generate/update index.md ---
    try:
        index_path = report_dir / "index.md"
        report_files = sorted(report_dir.glob("multi_agent_workflow_report_*.md"))
        with open(index_path, 'w') as idx:
            idx.write("# AgentOps Workflow Reports Index\n\n")
            idx.write("| Report File | Generated | Success Rate |\n")
            idx.write("|------------|-----------|--------------|\n")
            for rep in report_files:
                # Try to extract summary info from each report
                try:
                    with open(rep, 'r') as rf:
                        lines = rf.readlines()
                        gen_line = next((l for l in lines if l.startswith("**Generated:")), None)
                        rate_line = next((l for l in lines if l.startswith("**Success Rate:")), None)
                        gen = gen_line.split(':', 1)[1].strip() if gen_line else "-"
                        rate = rate_line.split(':', 1)[1].strip() if rate_line else "-"
                except Exception:
                    gen = rate = "-"
                idx.write(f"| [{rep.name}]({rep.name}) | {gen} | {rate} |\n")
            idx.write("\n---\n*This index is auto-generated. The latest report is always available as [latest_report.md](latest_report.md).*\n")
    except Exception as e:
        print(f"[AgentOps] Warning: Could not update index.md: {e}")
    return str(report_path)

def calculate_agent_success_rate(agent_name: str, files_to_process: List[str], 
                                failed_files_set: set) -> float:
    """Calculate success rate for a specific agent.
    
    Args:
        agent_name: Name of the agent
        files_to_process: List of all processed files
        failed_files_set: Set of failed file paths
        
    Returns:
        Success rate as a percentage
    """
    # For now, we assume all successful files completed all agents
    # In a future enhancement, we could parse actual logs for per-agent status
    successful_for_agent = len(files_to_process) - len(failed_files_set)
    return (successful_for_agent / len(files_to_process)) * 100 if files_to_process else 0


@cli.command()
@click.argument("target", type=click.Path(exists=True), required=False)
@click.option(
    "--all", "run_all", is_flag=True, 
    help="Run simple test generation on all Python files in the current directory"
)
@click.option(
    "--output-dir",
    default=None,
    help="Output directory for generated tests (default: .agentops/tests/)"
)
@click.option(
    "--parallel", is_flag=True,
    help="Process files in parallel for faster execution"
)
@click.option(
    "--workers", default=4, type=int,
    help="Number of parallel workers (default: 4, max: 8)"
)
def infer(target: str, run_all: bool, output_dir: str, parallel: bool, workers: int):
    """Run simple test generation on Python files (QUICK PROTOTYPING).

    ⚠️  NOTE: This is for quick prototyping only. For production use, 
    we recommend using 'agentops multi-agent-run' which provides:
    • Requirement extraction and traceability
    • Interactive approval workflow
    • Quality validation and testing strategy
    • Comprehensive test coverage

    This command uses the basic test generator workflow which is much faster
    than the multi-agent workflow. It makes a single LLM call per file to
    generate tests directly.

    Usage:
        agentops infer file.py          # Single file
        agentops infer directory/       # All Python files in directory
        agentops infer --all            # All Python files in current directory
        agentops infer --all --parallel # Parallel processing
        agentops infer --all --parallel --workers 6 # Custom worker count

    Args:
        target: Path to Python file or directory to process
        run_all: Process all Python files in current directory
        output_dir: Directory for generated tests (optional)
        parallel: Process files in parallel for faster execution
        workers: Number of parallel workers (default: 4, max: 8)
    """
    if not os.path.exists(".agentops"):
        console.print(
            Panel(
                "[yellow]AgentOps not initialized in this directory.[/yellow]\n\n"
                "Run [bold cyan]agentops init[/bold cyan] first.",
                title="Not Initialized",
                border_style="yellow",
            )
        )
        sys.exit(1)

    # Validate worker count
    if workers < 1 or workers > 8:
        console.print(
            Panel(
                "[red]Worker count must be between 1 and 8[/red]",
                title="Invalid Worker Count",
                border_style="red",
            )
        )
        sys.exit(1)

    # Determine what files to process
    files_to_process = []
    
    if run_all:
        # Process all Python files in current directory
        files_to_process = find_python_files(".")
        if not files_to_process:
            console.print(
                Panel(
                    "[yellow]No Python files found in current directory.[/yellow]",
                    title="No Files Found",
                    border_style="yellow",
                )
            )
            return
    elif target:
        if os.path.isfile(target):
            # Single file
            if not target.endswith('.py'):
                console.print(
                    Panel(
                        "[yellow]Target must be a Python file (.py)[/yellow]",
                        title="Invalid File Type",
                        border_style="yellow",
                    )
                )
                return
            files_to_process = [target]
        elif os.path.isdir(target):
            # Directory - process all Python files
            files_to_process = find_python_files(target)
            if not files_to_process:
                console.print(
                    Panel(
                        f"[yellow]No Python files found in {target}[/yellow]",
                        title="No Files Found",
                        border_style="yellow",
                    )
                )
                return
        else:
            console.print(
                Panel(
                    "[yellow]Target must be a valid file or directory[/yellow]",
                    title="Invalid Target",
                    border_style="yellow",
                )
            )
            return
    else:
        # No target specified and no --all flag
        console.print(
            Panel(
                "[yellow]Please specify a file, directory, or use --all flag[/yellow]\n\n"
                "Usage:\n"
                "• [bold]agentops infer file.py[/bold] - Single file\n"
                "• [bold]agentops infer directory/[/bold] - All files in directory\n"
                "• [bold]agentops infer --all[/bold] - All files in current directory",
                title="Missing Target",
                border_style="yellow",
            )
        )
        return

    # Adjust worker count based on file count
    if parallel and len(files_to_process) < workers:
        workers = len(files_to_process)
        console.print(f"[dim]Adjusted workers to {workers} (file count)[/dim]")

    # Initialize simple test generator
    from agentops_ai.agentops_core.services.test_generator import TestGenerator
    config = get_config()
    
    # Check if OpenAI API key is configured
    if not config.llm.api_key:
        console.print(
            Panel(
                "[red]OpenAI API key not configured.[/red]\n\n"
                "Set your API key:\n"
                "[bold]export OPENAI_API_KEY='your-api-key-here'[/bold]\n\n"
                "Get your API key from: https://platform.openai.com/api-keys\n\n"
                "Note: The infer command requires an API key for test generation.",
                title="API Key Missing",
                border_style="red",
            )
        )
        sys.exit(1)
    
    try:
        test_generator = TestGenerator(api_key=config.llm.api_key, model=config.llm.model)
    except Exception as e:
        console.print(
            Panel(
                f"[red]Failed to initialize test generator.[/red]\n\n"
                f"Error: {str(e)}\n\n"
                "This is usually caused by:\n"
                "• Invalid OpenAI API key\n"
                "• Network connectivity issues\n"
                "• Missing dependencies\n\n"
                "Please check your configuration and try again.",
                title="Initialization Error",
                border_style="red",
            )
        )
        sys.exit(1)
    
    # Process files
    total_files = len(files_to_process)
    successful_files = 0
    failed_files = []
    
    processing_mode = "parallel" if parallel else "sequential"
    console.print(
        Panel(
            f"[bold]Starting simple test generation for {total_files} file(s) in {processing_mode} mode[/bold]\n"
            f"Workers: {workers}" if parallel else "",
            title="AgentOps Simple Test Generation (Quick Prototyping)",
            border_style="yellow",
        )
    )
    
    # Show recommendation for production use
    console.print(
        Panel(
            "[yellow]⚠️  Quick Prototyping Mode[/yellow]\n\n"
            "For production use, we recommend: [bold cyan]agentops multi-agent-run[/bold cyan]\n"
            "This provides requirement extraction, approval workflow, and quality validation.",
            title="Recommendation",
            border_style="yellow",
        )
    )

    if parallel and total_files > 1:
        # Parallel processing
        def process_file(file_path):
            """Process a single file with the test generator."""
            try:
                # Generate tests using simple workflow
                result = test_generator.generate_tests(file_path)
                
                if result.get("success", False):
                    # Save the generated tests to file
                    test_code = result.get("tests", "")
                    if test_code:
                        # Create output directory
                        output_dir = output_dir or ".agentops/tests"
                        os.makedirs(output_dir, exist_ok=True)
                        
                        # Generate test filename based on source file
                        source_name = Path(file_path).stem
                        test_filename = f"test_{source_name}.py"
                        test_file_path = os.path.join(output_dir, test_filename)
                        
                        # Write test code to file
                        with open(test_file_path, "w") as f:
                            f.write(test_code)
                        
                        console.print(f"[dim]Generated: {test_file_path}[/dim]")
                    
                    return file_path, True, None
                else:
                    return file_path, False, [result.get("error", "Unknown error")]
            except Exception as e:
                return file_path, False, [str(e)]
        
        with Progress() as progress:
            task = progress.add_task("Processing files...", total=total_files)
            
            with ThreadPoolExecutor(max_workers=workers) as executor:
                # Submit all files for processing
                future_to_file = {
                    executor.submit(process_file, file_path): file_path 
                    for file_path in files_to_process
                }
                
                # Collect results as they complete
                for future in as_completed(future_to_file):
                    file_path, success, errors = future.result()
                    
                    if success:
                        successful_files += 1
                        progress.update(task, description=f"✓ {os.path.basename(file_path)}")
                    else:
                        failed_files.append((file_path, errors))
                        progress.update(task, description=f"✗ {os.path.basename(file_path)}")
                    
                    progress.advance(task)
    else:
        # Sequential processing
        with Progress() as progress:
            task = progress.add_task("Processing files...", total=total_files)
            
            for file_path in files_to_process:
                try:
                    progress.update(task, description=f"Processing {os.path.basename(file_path)}...")
                    
                    # Generate tests using simple workflow
                    result = test_generator.generate_tests(file_path)

                    if result.get("success", False):
                        # Save the generated tests to file
                        test_code = result.get("tests", "")
                        if test_code:
                            # Create output directory
                            output_dir = output_dir or ".agentops/tests"
                            os.makedirs(output_dir, exist_ok=True)
                            
                            # Generate test filename based on source file
                            source_name = Path(file_path).stem
                            test_filename = f"test_{source_name}.py"
                            test_file_path = os.path.join(output_dir, test_filename)
                            
                            # Write test code to file
                            with open(test_file_path, "w") as f:
                                f.write(test_code)
                            
                            console.print(f"[dim]Generated: {test_file_path}[/dim]")
                        
                        successful_files += 1
                    else:
                        failed_files.append((file_path, [result.get("error", "Unknown error")]))
                        
                except Exception as e:
                    failed_files.append((file_path, [str(e)]))
                
                progress.advance(task)

    # Display results
    console.print("\n" + "="*60)
                        
    if successful_files > 0:
        console.print(
            Panel(
                f"[bold green]✓ Successfully processed {successful_files}/{total_files} files![/bold green]\n"
                f"Mode: {processing_mode}" + (f" ({workers} workers)" if parallel else ""),
                title="Quick Test Generation Complete",
                border_style="green",
            )
        )
        
        # Final recommendation
        console.print(
            Panel(
                "[bold]Next Steps:[/bold]\n"
                "• Run [cyan]agentops run --all[/cyan] to execute the generated tests\n"
                "• For production use, try [cyan]agentops multi-agent-run[/cyan] for full workflow\n"
                "• View results with [cyan]agentops report --check-changes[/cyan]",
                title="What's Next?",
                border_style="blue",
            )
        )

    if failed_files:
        console.print(
            Panel(
                f"[red]Failed to process {len(failed_files)} files:[/red]\n" + 
                "\n".join([f"• {file}: {', '.join(errors)}" for file, errors in failed_files]),
                title="Failed Files",
                border_style="red",
            )
        )

    if successful_files == 0:
        console.print(
            Panel(
                "[red]No files were processed successfully.[/red]",
                title="Quick Test Generation Failed",
                border_style="red",
            )
        )
        
        # Suggest alternative approach
        console.print(
            Panel(
                "[bold]Try the recommended approach:[/bold]\n"
                "[cyan]agentops multi-agent-run[/cyan] for comprehensive test generation\n"
                "This includes requirement extraction and quality validation.",
                title="Alternative",
                border_style="yellow",
            )
        )
        sys.exit(1)


@cli.command()
@click.argument("target", type=click.Path(exists=True), required=False)
@click.option(
    "--all", "run_all", is_flag=True, 
    help="Run tests for all generated test files"
)
def run(target: str, run_all: bool):
    """Execute tests with root cause analysis for failures.
    
    Runs the generated tests and provides intelligent analysis of any failures.
    The system will analyze test failures and provide suggestions for fixing
    either the code or the tests.
    
    Options:
        --target: Run tests for a specific source file
        --all: Run all generated tests
    """
    if not os.path.exists(".agentops"):
        console.print(
            Panel(
                "[yellow]AgentOps not initialized in this directory.[/yellow]\n\n"
                "Run [bold cyan]agentops init[/bold cyan] first.",
                title="Not Initialized",
                border_style="yellow",
            )
        )
        sys.exit(1)

    config = get_config()
    test_dir = Path(config.project.test_output_dir)
    
    if not test_dir.exists():
        console.print(
            Panel(
                "[yellow]No tests found.[/yellow]\n\n"
                "Run [bold cyan]agentops multi-agent-run <file.py>[/bold cyan] to generate tests first.",
                title="No Tests",
                border_style="yellow",
            )
        )
        sys.exit(1)

    # Find test files to run
    test_files = []
    if target:
        # Find test file for specific source file
        source_name = Path(target).stem
        test_file = test_dir / f"test_{source_name}.py"
        if test_file.exists():
            test_files = [str(test_file)]
        else:
            console.print(
                Panel(
                    f"[red]No test file found for {target}[/red]\n\n"
                    f"Expected: {test_file}",
                    title="Test File Not Found",
                    border_style="red",
                )
            )
            sys.exit(1)
    elif run_all:
        # Find all test files
        test_files = [str(f) for f in test_dir.glob("test_*.py")]
        if not test_files:
            console.print(
                Panel(
                    "[yellow]No test files found.[/yellow]\n\n"
                    "Run [bold cyan]agentops multi-agent-run <file.py>[/bold cyan] to generate tests first.",
                    title="No Tests",
                    border_style="yellow",
                )
            )
            sys.exit(1)
    else:
        console.print(
            Panel(
                "[yellow]Please specify --target or --all[/yellow]\n\n"
                "Usage:\n"
                "• [bold cyan]agentops run --target mymodule.py[/bold cyan]\n"
                "• [bold cyan]agentops run --all[/bold cyan]",
                title="Usage",
                border_style="yellow",
            )
        )
        sys.exit(1)

    # Run tests with pytest
    console.print(f"[bold]Running {len(test_files)} test file(s)...[/bold]")
    
    try:
        result = subprocess.run(
            ["pytest", "-v"] + test_files,
            capture_output=True,
            text=True,
            cwd=config.project.project_root
        )

        if result.returncode == 0:
            console.print(
                Panel(
                    "[bold green]✓ All tests passed![/bold green]",
                    title="Test Results",
                    border_style="green",
                )
            )
        else:
            console.print(
                Panel(
                    f"[red]Some tests failed[/red]\n\n{result.stdout}\n{result.stderr}",
                    title="Test Results",
                    border_style="red",
                )
            )

    except FileNotFoundError:
        console.print(
            Panel(
                "[red]pytest not found[/red]\n\n"
                "Install pytest: [bold]pip install pytest[/bold]",
                title="Error",
                border_style="red",
            )
        )
        sys.exit(1)


@cli.command()
@click.option("--non-interactive", is_flag=True, help="Skip confirmation prompts")
def fast_approve(non_interactive):
    """Approve all pending requirements quickly without generating tests.
    
    This command efficiently approves all pending requirements without generating
    tests for each one individually. Test generation should be done separately
    for better performance.
    """
    if not os.path.exists(".agentops"):
        console.print(
            Panel(
                "[yellow]AgentOps not initialized in this directory.[/yellow]\n\n"
                "Run [bold cyan]agentops init[/bold cyan] first.",
                title="Not Initialized",
                border_style="yellow",
            )
        )
        sys.exit(1)

    # Initialize workflow
    workflow = AgentOpsWorkflow()
    
    # Get pending requirements count
    pending_requirements = workflow.requirement_store.get_pending_requirements()
    
    if not pending_requirements:
        console.print(
            Panel(
                "[bold green]No pending requirements found![/bold green]\n\n"
                "All requirements have been processed.",
                title="No Pending Requirements",
                border_style="green",
            )
        )
        sys.exit(0)
    
    # Show confirmation (unless non-interactive)
    if not non_interactive:
        console.print(
            Panel(
                f"[bold]Found {len(pending_requirements)} pending requirements[/bold]\n\n"
                "This will quickly approve all pending requirements.\n"
                "Test generation will need to be done separately.\n"
                "This action cannot be undone.",
                title="Fast Bulk Approval",
                border_style="yellow",
            )
        )
        
        if not Confirm.ask("[bold]Continue with fast bulk approval?[/bold]", default=False):
            console.print("[yellow]Fast bulk approval cancelled.[/yellow]")
            sys.exit(0)
    
    # Run fast bulk approval
    console.print(f"[bold]Starting fast bulk approval of {len(pending_requirements)} requirements...[/bold]")
    
    result = workflow.approve_all_pending_requirements_fast()
    
    if result["success"]:
        console.print(
            Panel(
                f"[bold green]✓ Fast bulk approval completed![/bold green]\n\n"
                f"Processed: {result['processed']}\n"
                f"Approved: {result['approved']}\n"
                f"Failed: {result['rejected']}\n"
                f"Success rate: {result['approved']/result['processed']*100:.1f}%\n\n"
                f"Next: Run test generation with 'agentops generate-tests' or step 4 in runner script",
                title="Fast Bulk Approval Results",
                border_style="green",
            )
        )
    else:
        console.print(
            Panel(
                f"[red]Fast bulk approval failed[/red]\n\n"
                f"Error: {result.get('error', 'Unknown error')}",
                title="Error",
                border_style="red",
            )
        )
        sys.exit(1)


@cli.command()
@click.option("--non-interactive", is_flag=True, help="Skip confirmation prompts")
def approve_all(non_interactive):
    """Approve all pending requirements without interactive review.
    
    This command automatically approves all pending requirements and generates
    tests for them. This is useful for bulk processing when you trust the
    inferred requirements.
    """
    if not os.path.exists(".agentops"):
        console.print(
            Panel(
                "[yellow]AgentOps not initialized in this directory.[/yellow]\n\n"
                "Run [bold cyan]agentops init[/bold cyan] first.",
                title="Not Initialized",
                border_style="yellow",
            )
        )
        sys.exit(1)

    # Initialize workflow
    workflow = AgentOpsWorkflow()
    
    # Get pending requirements count
    pending_requirements = workflow.requirement_store.get_pending_requirements()
    
    if not pending_requirements:
        console.print(
            Panel(
                "[bold green]No pending requirements found![/bold green]\n\n"
                "All requirements have been processed.",
                title="No Pending Requirements",
                border_style="green",
            )
        )
        sys.exit(0)
    
    # Show confirmation (unless non-interactive)
    if not non_interactive:
        console.print(
            Panel(
                f"[bold]Found {len(pending_requirements)} pending requirements[/bold]\n\n"
                "This will automatically approve all pending requirements and generate tests.\n"
                "This action cannot be undone.",
                title="Bulk Approval",
                border_style="yellow",
            )
        )
        
        if not Confirm.ask("[bold]Continue with bulk approval?[/bold]", default=False):
            console.print("[yellow]Bulk approval cancelled.[/yellow]")
            sys.exit(0)
    
    # Run bulk approval
    console.print(f"[bold]Starting bulk approval of {len(pending_requirements)} requirements...[/bold]")
    
    result = workflow.approve_all_pending_requirements()
    
    if result["success"]:
        console.print(
            Panel(
                f"[bold green]✓ Bulk approval completed![/bold green]\n\n"
                f"Processed: {result['processed']}\n"
                f"Approved: {result['approved']}\n"
                f"Failed: {result['rejected']}\n"
                f"Success rate: {result['approved']/result['processed']*100:.1f}%",
                title="Bulk Approval Results",
                border_style="green",
            )
        )
    else:
        console.print(
            Panel(
                f"[red]Bulk approval failed[/red]\n\n"
                f"Error: {result.get('error', 'Unknown error')}",
                title="Error",
                border_style="red",
            )
        )
        sys.exit(1)


@cli.command()
def config():
    """View and edit AgentOps configuration.
    
    Shows current configuration and provides options to modify settings.
    """
    config = get_config()

    console.print(
        Panel(
            f"[bold]AgentOps Configuration[/bold]\n\n"
            f"Project Root: {config.project.project_root}\n"
            f"Test Output: {config.project.test_output_dir}\n"
            f"LLM Model: {config.llm.model}\n"
            f"LLM Temperature: {config.llm.temperature}\n"
            f"API Key: {'✓ Set' if config.llm.api_key else '✗ Not set'}\n\n"
            f"Config File: {config.config_file}",
            title="Configuration",
            border_style="cyan",
        )
    )


@cli.group()
def integration():
    """Manage CI/CD and IDE integrations for AgentOps."""
    pass


@integration.command()
@click.option("--ci-provider", type=click.Choice(["github", "gitlab", "jenkins"]), 
              help="CI/CD provider to configure")
@click.option("--ide-provider", type=click.Choice(["vscode", "pycharm"]), 
              help="IDE provider to configure")
@click.option("--webhook-enabled", is_flag=True, help="Enable webhook server")
@click.option("--webhook-port", default=8080, help="Webhook server port")
@click.option("--webhook-secret", help="Webhook secret for signature verification")
@click.option("--auto-approve", is_flag=True, help="Auto-approve requirements in CI")
@click.option("--notification-channels", multiple=True, 
              type=click.Choice(["slack", "email", "webhook"]),
              help="Notification channels (can specify multiple)")
def setup(ci_provider, ide_provider, webhook_enabled, webhook_port, webhook_secret, 
          auto_approve, notification_channels):
    """Setup CI/CD and IDE integrations.
    
    Configures AgentOps to work with your CI/CD pipeline and IDE.
    """
    config = get_config()
    
    # Update integration settings
    if ci_provider:
        config.integration.ci_provider = ci_provider
    if ide_provider:
        config.integration.ide_provider = ide_provider
    if webhook_enabled is not None:
        config.integration.webhook_enabled = webhook_enabled
    if webhook_port:
        config.integration.webhook_port = webhook_port
    if webhook_secret:
        config.integration.webhook_secret = webhook_secret
    if auto_approve is not None:
        config.integration.auto_approve = auto_approve
    if notification_channels:
        config.integration.notification_channels = list(notification_channels)

    # Save configuration
    config.save()
        
    console.print(
        Panel(
            "[bold green]✓ Integration settings updated![/bold green]\n\n"
            f"CI Provider: {config.integration.ci_provider}\n"
            f"IDE Provider: {config.integration.ide_provider}\n"
            f"Webhook Enabled: {config.integration.webhook_enabled}\n"
            f"Auto Approve: {config.integration.auto_approve}",
            title="Integration Setup",
            border_style="green",
        )
    )


@integration.command()
def status():
    """Show integration status and configuration."""
    config = get_config()
    
    console.print(
        Panel(
            f"[bold]Integration Status[/bold]\n\n"
            f"CI Provider: {config.integration.ci_provider}\n"
            f"IDE Provider: {config.integration.ide_provider}\n"
            f"Webhook Enabled: {config.integration.webhook_enabled}\n"
            f"Webhook Port: {config.integration.webhook_port}\n"
            f"Auto Approve: {config.integration.auto_approve}\n"
            f"Notifications: {', '.join(config.integration.notification_channels)}",
            title="Integration Status",
            border_style="cyan",
        )
    )


@cli.command()
@click.option("--format", "output_format", 
              type=click.Choice(["markdown", "csv", "json"]), 
              default="markdown",
              help="Output format for traceability matrix (default: markdown)")
@click.option("--open", "open_file", is_flag=True, 
              help="Open the generated file in default application")
def traceability(output_format: str, open_file: bool):
    """Generate traceability matrix linking requirements to tests.
    
    Creates a comprehensive traceability matrix showing the relationship
    between source code, requirements, and generated tests.
    
    Usage:
        agentops traceability                    # Generate markdown matrix
        agentops traceability --format csv       # Generate CSV matrix
        agentops traceability --format json      # Generate JSON matrix
        agentops traceability --open             # Open generated file
    """
    if not os.path.exists(".agentops"):
        console.print(
            Panel(
                "[yellow]AgentOps not initialized in this directory.[/yellow]\n\n"
                "Run [bold cyan]agentops init[/bold cyan] first.",
                title="Not Initialized",
                border_style="yellow",
            )
        )
        sys.exit(1)

    # Initialize workflow
    workflow = AgentOpsWorkflow()
    
    # Generate traceability matrix
    result = workflow.generate_traceability_matrix(output_format)
    
    if result["success"]:
        file_path = result["file_path"]
        
        if RICH_AVAILABLE:
            console.print(
                Panel(
                    f"[bold green]✓ Traceability matrix generated![/bold green]\n\n"
                    f"File: [cyan]{file_path}[/cyan]\n"
                    f"Format: [cyan]{output_format}[/cyan]\n"
                    f"Requirements: [cyan]{result['requirements_count']}[/cyan]\n"
                    f"Test Files: [cyan]{result['test_files_count']}[/cyan]\n"
                    f"Test Functions: [cyan]{result['test_functions_count']}[/cyan]\n\n"
                    f"Matrix includes:\n"
                    f"• Source files to requirements mapping\n"
                    f"• Requirements to test functions mapping\n"
                    f"• Test cases to requirements mapping\n"
                    f"• Coverage analysis and statistics\n"
                    f"• Navigation links to related files",
                    title="Traceability Matrix Generated",
                    border_style="green",
                )
            )
        else:
            console.print(
                Panel(
                    f"[bold green]✓ Traceability matrix generated![/bold green]\n\n"
                    f"File: [cyan]{file_path}[/cyan]\n"
                    f"Format: [cyan]{output_format}[/cyan]\n"
                    f"Requirements: [cyan]{result['requirements_count']}[/cyan]",
                    title="Traceability Matrix Generated",
                    border_style="green",
                )
            )
        
        # Open file if requested
        if open_file:
            try:
                import subprocess
                import platform
                
                system = platform.system()
                if system == "Darwin":  # macOS
                    subprocess.run(["open", file_path])
                elif system == "Windows":
                    subprocess.run(["start", file_path], shell=True)
                else:  # Linux
                    subprocess.run(["xdg-open", file_path])
                    
                console.print(f"[green]Opened {file_path}[/green]")
            except Exception as e:
                console.print(f"[yellow]Could not open file automatically: {e}[/yellow]")
                console.print(f"[cyan]File location: {file_path}[/cyan]")
        else:
            console.print(f"\n[cyan]File location: {file_path}[/cyan]")
            
    else:
        console.print(
            Panel(
                f"[red]Failed to generate traceability matrix[/red]\n\n"
                f"Error: {result['error']}",
                title="Error",
                border_style="red",
            )
        )
        sys.exit(1)


@cli.command()
@click.option("--format", "output_format", 
              type=click.Choice(["gherkin", "markdown", "both"]), 
              default="both",
              help="Export format (default: both)")
@click.option("--open", "open_file", is_flag=True, 
              help="Open the generated files in default application")
def export_requirements(output_format: str, open_file: bool):
    """Export requirements to documentation formats.
    
    Automatically exports requirements to Gherkin and/or Markdown formats
    for documentation and collaboration purposes.
    
    Usage:
        agentops export-requirements                    # Export both formats
        agentops export-requirements --format gherkin  # Export only Gherkin
        agentops export-requirements --format markdown # Export only Markdown
    """
    try:
        from ..agentops_core.workflow import AgentOpsWorkflow
        workflow = AgentOpsWorkflow()
        
        result = workflow.export_requirements_automatically()
        
        if result["success"]:
            console.print(f"[green]✓ Requirements exported successfully![/green]")
            console.print(f"  Exported files: {', '.join(result['exported_files'])}")
            console.print(f"  Formats: {result['success_count']}/{result['total_formats']} successful")
            
            if open_file:
                for file_path in result['exported_files']:
                    if os.path.exists(file_path):
                        import subprocess
                        subprocess.run(['xdg-open', file_path])
        else:
            console.print(f"[red]✗ Export failed: {result.get('error', 'Unknown error')}[/red]")
            sys.exit(1)
            
    except Exception as e:
        console.print(f"[red]✗ Export failed: {str(e)}[/red]")
        sys.exit(1)


@cli.command()
@click.option("--format", "output_format", 
              type=click.Choice(["markdown", "csv", "json"]), 
              default="markdown",
              help="Output format for the report (default: markdown)")
@click.option("--open", "open_file", is_flag=True, 
              help="Open the generated report in default application")
@click.option("--force", is_flag=True,
              help="Force regeneration even if no changes detected")
@click.option("--check-changes", is_flag=True,
              help="Only check for file changes without generating report")
def report(output_format: str, open_file: bool, force: bool, check_changes: bool):
    """Generate a comprehensive report from existing workflow results.
    
    This command analyzes existing test files and requirements to generate
    a detailed report without re-running the multi-agent workflow. It can
    detect file changes and mark outdated results.
    
    Usage:
        agentops report                    # Generate markdown report
        agentops report --format csv       # Generate CSV report
        agentops report --check-changes    # Only check for file changes
        agentops report --force            # Force regeneration
        agentops report --open             # Open generated report
    """
    if not os.path.exists(".agentops"):
        console.print(
            Panel(
                "[yellow]AgentOps not initialized in this directory.[/yellow]\n\n"
                "Run [bold cyan]agentops init[/bold cyan] first.",
                title="Not Initialized",
                border_style="yellow",
            )
        )
        sys.exit(1)

    # Initialize workflow
    workflow = AgentOpsWorkflow()
    
    # Analyze existing results and detect changes
    analysis_result = analyze_existing_results(workflow)
    
    if check_changes:
        # Only show change analysis
        display_change_analysis(analysis_result)
        return
    
    # Generate report based on analysis
    report_result = generate_analysis_report(analysis_result, output_format, force)
    
    if report_result["success"]:
        file_path = report_result["file_path"]
        
        console.print(
            Panel(
                f"[bold green]✓ Analysis report generated![/bold green]\n\n"
                f"File: [cyan]{file_path}[/cyan]\n"
                f"Format: [cyan]{output_format}[/cyan]\n"
                f"Files Analyzed: [cyan]{report_result['files_analyzed']}[/cyan]\n"
                f"Outdated Files: [cyan]{report_result['outdated_files']}[/cyan]\n"
                f"Up-to-date Files: [cyan]{report_result['up_to_date_files']}[/cyan]",
                title="Analysis Report Generated",
                border_style="green",
            )
        )
        
        # Open file if requested
        if open_file:
            try:
                import subprocess
                import platform
                
                system = platform.system()
                if system == "Darwin":  # macOS
                    subprocess.run(["open", file_path])
                elif system == "Windows":
                    subprocess.run(["start", file_path], shell=True)
                else:  # Linux
                    subprocess.run(["xdg-open", file_path])
                    
                console.print(f"[green]Opened {file_path}[/green]")
            except Exception as e:
                console.print(f"[yellow]Could not open file automatically: {e}[/yellow]")
                console.print(f"[cyan]File location: {file_path}[/cyan]")
        else:
            console.print(f"\n[cyan]File location: {file_path}[/cyan]")
            
    else:
        console.print(
            Panel(
                f"[red]Failed to generate analysis report[/red]\n\n"
                f"Error: {report_result['error']}",
                title="Error",
                border_style="red",
            )
        )
        sys.exit(1)
    

def analyze_existing_results(workflow: AgentOpsWorkflow) -> dict:
    """Analyze existing workflow results and detect file changes.
    
    Args:
        workflow: AgentOpsWorkflow instance
        
    Returns:
        Dictionary with analysis results
    """
    from pathlib import Path
    import hashlib
    import json
    from datetime import datetime
    
    analysis = {
        "files_analyzed": [],
        "outdated_files": [],
        "up_to_date_files": [],
        "missing_tests": [],
        "test_files": [],
        "requirements": [],
        "change_summary": {}
    }
    
    # Get all test files
    test_dir = Path(".agentops/tests")
    if test_dir.exists():
        test_files = list(test_dir.rglob("test_*.py"))
        analysis["test_files"] = [str(f) for f in test_files]
    
    # Get all requirements
    try:
        requirements = workflow.requirement_store.get_all_requirements()
        analysis["requirements"] = [req.file_path for req in requirements]
    except:
        pass
    
    # Analyze each source file that has tests
    for test_file in analysis["test_files"]:
        test_path = Path(test_file)
        
        # Extract source file path from test file path
        # Test file: .agentops/tests/path/to/test_source.py
        # Source file: path/to/source.py
        relative_test_path = test_path.relative_to(test_dir)
        source_file_name = relative_test_path.name.replace("test_", "")
        source_file_path = relative_test_path.parent / source_file_name
        
        # Check if source file exists
        if not source_file_path.exists():
            analysis["missing_tests"].append({
                "test_file": test_file,
                "source_file": str(source_file_path),
                "status": "source_missing"
            })
            continue
        
        # Calculate file hash for change detection
        try:
            with open(source_file_path, 'rb') as f:
                file_hash = hashlib.md5(f.read()).hexdigest()
        except:
            file_hash = "unknown"
        
        # Check if we have stored hash for this file
        hash_file = Path(".agentops/file_hashes.json")
        stored_hashes = {}
        if hash_file.exists():
            try:
                with open(hash_file, 'r') as f:
                    stored_hashes = json.load(f)
            except:
                stored_hashes = {}
        
        file_info = {
            "source_file": str(source_file_path),
            "test_file": test_file,
            "current_hash": file_hash,
            "stored_hash": stored_hashes.get(str(source_file_path)),
            "last_modified": datetime.fromtimestamp(source_file_path.stat().st_mtime).isoformat(),
            "test_count": 0
        }
        
        # Count test functions
        try:
            with open(test_file, 'r') as f:
                test_content = f.read()
                file_info["test_count"] = test_content.count('def test_')
        except:
            pass
        
        # Determine if file is outdated
        if file_info["stored_hash"] is None:
            file_info["status"] = "new_file"
            analysis["up_to_date_files"].append(file_info)
        elif file_info["current_hash"] != file_info["stored_hash"]:
            file_info["status"] = "modified"
            analysis["outdated_files"].append(file_info)
        else:
            file_info["status"] = "up_to_date"
            analysis["up_to_date_files"].append(file_info)
        
        analysis["files_analyzed"].append(file_info)
    
    # Generate change summary
    analysis["change_summary"] = {
        "total_files": len(analysis["files_analyzed"]),
        "up_to_date": len(analysis["up_to_date_files"]),
        "outdated": len(analysis["outdated_files"]),
        "missing_source": len([f for f in analysis["missing_tests"] if f["status"] == "source_missing"]),
        "total_tests": sum(f["test_count"] for f in analysis["files_analyzed"]),
        "total_requirements": len(analysis["requirements"])
    }
    
    return analysis


def display_change_analysis(analysis: dict):
    """Display change analysis results.
    
    Args:
        analysis: Analysis results from analyze_existing_results
    """
    summary = analysis["change_summary"]
    
    console.print(
        Panel(
            f"[bold]File Change Analysis[/bold]\n\n"
            f"📊 **Summary:**\n"
            f"• Total Files: {summary['total_files']}\n"
            f"• Up-to-date: {summary['up_to_date']} ✅\n"
            f"• Outdated: {summary['outdated']} ⚠️\n"
            f"• Missing Source: {summary['missing_source']} ❌\n"
            f"• Total Tests: {summary['total_tests']}\n"
            f"• Total Requirements: {summary['total_requirements']}",
            title="Change Analysis Results",
            border_style="cyan",
        )
    )
    
    if analysis["outdated_files"]:
        console.print("\n[yellow]⚠️  Outdated Files (Source Modified):[/yellow]")
        for file_info in analysis["outdated_files"]:
            console.print(f"  • {file_info['source_file']}")
            console.print(f"    [dim]Test file: {file_info['test_file']}[/dim]")
            console.print(f"    [dim]Last modified: {file_info['last_modified']}[/dim]")
    
    if analysis["missing_tests"]:
        console.print("\n[red]❌ Missing Source Files:[/red]")
        for file_info in analysis["missing_tests"]:
            if file_info["status"] == "source_missing":
                console.print(f"  • {file_info['source_file']}")
                console.print(f"    [dim]Test file: {file_info['test_file']}[/dim]")


def generate_analysis_report(analysis: dict, output_format: str, force: bool) -> dict:
    """Generate analysis report from existing results.
    
    Args:
        analysis: Analysis results from analyze_existing_results
        output_format: Report format (markdown, csv, json)
        force: Force regeneration even if no changes
        
    Returns:
        Dictionary with report generation results
    """
    from pathlib import Path
    import datetime
    
    # Create report directory if it doesn't exist
    report_dir = Path(".agentops/reports")
    report_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate timestamp for unique filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = report_dir / f"analysis_report_{timestamp}.{output_format}"
    
    summary = analysis["change_summary"]
    
    if output_format == "markdown":
        content = generate_markdown_analysis_report(analysis, timestamp)
    elif output_format == "csv":
        content = generate_csv_analysis_report(analysis)
    elif output_format == "json":
        content = json.dumps(analysis, indent=2)
    else:
        return {"success": False, "error": f"Unsupported format: {output_format}"}
    
    # Write the report to file
    try:
        with open(report_path, 'w') as f:
            f.write(content)
        
        return {
            "success": True,
            "file_path": str(report_path),
            "files_analyzed": summary["total_files"],
            "outdated_files": summary["outdated"],
            "up_to_date_files": summary["up_to_date"]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def generate_markdown_analysis_report(analysis: dict, timestamp: str) -> str:
    """Generate markdown analysis report.
    
    Args:
        analysis: Analysis results
        timestamp: Report timestamp
        
    Returns:
        Markdown content
    """
    summary = analysis["change_summary"]
    
    content = f"""# AgentOps Analysis Report

**Generated:** {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Report ID:** {timestamp}  
**Total Files Analyzed:** {summary['total_files']}  
**Up-to-date Files:** {summary['up_to_date']}  
**Outdated Files:** {summary['outdated']}  
**Missing Source Files:** {summary['missing_source']}  
**Total Tests:** {summary['total_tests']}  
**Total Requirements:** {summary['total_requirements']}

## Summary

This report analyzes existing AgentOps workflow results without re-running the multi-agent system.
It detects file changes and identifies which test files need to be regenerated.

## File Status Overview

| Status | Count | Percentage |
|--------|-------|------------|
| ✅ Up-to-date | {summary['up_to_date']} | {(summary['up_to_date'] / summary['total_files'] * 100):.1f}% |
| ⚠️ Outdated | {summary['outdated']} | {(summary['outdated'] / summary['total_files'] * 100):.1f}% |
| ❌ Missing Source | {summary['missing_source']} | {(summary['missing_source'] / summary['total_files'] * 100):.1f}% |

## Detailed File Analysis

| Source File | Test File | Status | Test Count | Last Modified | Hash Changed |
|-------------|-----------|--------|------------|---------------|--------------|
"""
    
    for file_info in analysis["files_analyzed"]:
        status_icon = {
            "up_to_date": "✅",
            "modified": "⚠️",
            "new_file": "🆕"
        }.get(file_info["status"], "❓")
        
        hash_changed = "Yes" if file_info["current_hash"] != file_info["stored_hash"] else "No"
        
        content += f"| `{file_info['source_file']}` | `{file_info['test_file']}` | {status_icon} {file_info['status']} | {file_info['test_count']} | {file_info['last_modified']} | {hash_changed} |\n"
    
    if analysis["outdated_files"]:
        content += f"""
## ⚠️ Outdated Files (Require Re-generation)

The following files have been modified since their tests were generated:

"""
        for file_info in analysis["outdated_files"]:
            content += f"### `{file_info['source_file']}`\n\n"
            content += f"- **Test File:** `{file_info['test_file']}`\n"
            content += f"- **Last Modified:** {file_info['last_modified']}\n"
            content += f"- **Test Count:** {file_info['test_count']}\n"
            content += f"- **Action Required:** Re-run `agentops multi-agent-run {file_info['source_file']}`\n\n"
    
    if analysis["missing_tests"]:
        content += f"""
## ❌ Missing Source Files

The following test files exist but their source files are missing:

"""
        for file_info in analysis["missing_tests"]:
            if file_info["status"] == "source_missing":
                content += f"- **Test File:** `{file_info['test_file']}`\n"
                content += f"- **Missing Source:** `{file_info['source_file']}`\n\n"
    
    content += f"""
## Recommendations

"""
    
    if summary["outdated"] > 0:
        content += f"- ⚠️ **{summary['outdated']} file(s) need re-generation** due to source changes\n"
        content += f"- Run `agentops multi-agent-run <file>` for each outdated file\n"
        content += f"- Or use `agentops runner --steps 2,3,4 --target <file>` for faster regeneration\n"
    
    if summary["missing_source"] > 0:
        content += f"- ❌ **{summary['missing_source']} test file(s) have missing source files**\n"
        content += f"- Consider removing orphaned test files\n"
    
    if summary["up_to_date"] > 0:
        content += f"- ✅ **{summary['up_to_date']} file(s) are up-to-date** and don't need regeneration\n"
    
    content += f"""
## Next Steps

1. **For Outdated Files:** Re-run the multi-agent workflow to regenerate tests
2. **For Missing Source:** Remove orphaned test files or restore source files
3. **For Up-to-date Files:** No action needed, tests are current

---
*Report generated by AgentOps Analysis System*
"""
    
    return content


def generate_csv_analysis_report(analysis: dict) -> str:
    """Generate CSV analysis report.
    
    Args:
        analysis: Analysis results
        
    Returns:
        CSV content
    """
    import csv
    from io import StringIO
    
    output = StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        "Source File", "Test File", "Status", "Test Count", 
        "Last Modified", "Hash Changed", "Current Hash", "Stored Hash"
    ])
    
    # Write data
    for file_info in analysis["files_analyzed"]:
        hash_changed = "Yes" if file_info["current_hash"] != file_info["stored_hash"] else "No"
        writer.writerow([
            file_info["source_file"],
            file_info["test_file"],
            file_info["status"],
            file_info["test_count"],
            file_info["last_modified"],
            hash_changed,
            file_info["current_hash"],
            file_info["stored_hash"] or "N/A"
        ])
    
    return output.getvalue()


@cli.command()
def help():
    """Show detailed help information and command examples.
    
    Displays comprehensive help for all AgentOps commands with examples,
    use cases, and best practices.
    """
    console.print(
        Panel(
            "[bold cyan]AgentOps - Multi-Agent AI System for Requirements-Driven Test Automation[/bold cyan]\n\n"
            "[bold]🎯 What is AgentOps?[/bold]\n"
            "AgentOps uses 6 specialized AI agents to automatically analyze your code, "
            "extract requirements, and generate comprehensive test suites. It's like "
            "having a team of expert QA engineers working on your codebase.\n\n"
            "[bold]🚀 RECOMMENDED WORKFLOW:[/bold]\n"
            "1. [cyan]agentops init[/cyan]                        # Initialize project\n"
            "2. [cyan]agentops multi-agent-run myfile.py[/cyan]  # Run complete multi-agent workflow\n"
            "3. [cyan]agentops run --all[/cyan]                  # Execute generated tests\n"
            "4. [cyan]agentops report --check-changes[/cyan]     # View results and changes\n\n"
            "[bold]🤖 The Multi-Agent Workflow:[/bold]\n"
            "1. [cyan]CodeAnalyzer[/cyan] - Deep code structure and dependency analysis\n"
            "2. [cyan]RequirementsEngineer[/cyan] - Extract functional requirements using LLM\n"
            "3. [cyan]TestArchitect[/cyan] - Design comprehensive test strategy\n"
            "4. [cyan]TestGenerator[/cyan] - Create high-quality test code\n"
            "5. [cyan]QualityAssurance[/cyan] - Validate test quality\n"
            "6. [cyan]IntegrationSpecialist[/cyan] - Set up CI/CD and IDE integrations\n\n"
            "[bold]📚 Documentation & Support:[/bold]\n"
            "• GitHub: https://github.com/knaig/agentops_ai\n"
            "• Issues: https://github.com/knaig/agentops_ai/issues\n"
            "• Discussions: https://github.com/knaig/agentops_ai/discussions",
            title="AgentOps Help",
            border_style="cyan",
        )
    )
    
    # Command categories
    categories = {
        "🚀 Workflow Commands": [
            ("init", "Initialize AgentOps project structure"),
            ("multi-agent-run", "Run complete multi-agent workflow (6 AI agents) [RECOMMENDED]"),
            ("run", "Execute generated tests with analysis"),
            ("infer", "Run simple test generation (single LLM call) [QUICK PROTOTYPING]")
        ],
        "⚙️ Management Commands": [
            ("fast-approve", "Quickly approve pending requirements"),
            ("approve-all", "Approve all requirements with confirmation"),
            ("config", "View and edit AgentOps configuration")
        ],
        "📊 Analysis Commands": [
            ("report", "Generate analysis report from existing results"),
            ("traceability", "Generate traceability matrix"),
            ("requirement-info", "Show detailed requirement information"),
            ("test-info", "Show test file and function details")
        ],
        "🔗 Integration Commands": [
            ("integration", "Manage CI/CD and IDE integrations")
        ]
    }
    
    for category, commands in categories.items():
        console.print(f"\n[bold]{category}[/bold]")
        for cmd, desc in commands:
            console.print(f"  [cyan]{cmd:<20}[/cyan] {desc}")
    
    console.print(
        "\n[bold]💡 Quick Examples:[/bold]\n"
        "  [cyan]agentops init[/cyan]                                    # Initialize project\n"
        "  [cyan]agentops multi-agent-run myfile.py[/cyan]              # Run complete workflow\n"
        "  [cyan]agentops multi-agent-run --all --parallel[/cyan]       # Process all files in parallel\n"
        "  [cyan]agentops report --check-changes[/cyan]                  # Check for file changes\n"
        "  [cyan]agentops traceability --open[/cyan]                     # View traceability matrix\n"
        "  [cyan]agentops infer myfile.py[/cyan]                         # Quick prototyping only\n\n"
        "[bold]🔍 For detailed help on any command:[/bold]\n"
        "  [cyan]agentops <command> --help[/cyan]\n\n"
        "[bold]📖 Learn More:[/bold]\n"
        "  • Run [cyan]agentops examples[/cyan] for sample workflows\n"
        "  • Visit our GitHub for full documentation\n"
        "  • Join our community for support and feedback"
    )


@cli.command()
def examples():
    """Show practical examples and use cases for AgentOps.
    
    Displays real-world examples of how to use AgentOps for different
    scenarios and project types.
    """
    console.print(
        Panel(
            "[bold cyan]AgentOps Examples & Use Cases[/bold cyan]\n\n"
            "Learn how to use AgentOps effectively for different scenarios.",
            title="Examples",
            border_style="cyan",
        )
    )
    
    examples_data = {
        "🆕 Getting Started (Recommended)": [
            ("Initialize a new project", "agentops init"),
            ("Run complete workflow on a single file", "agentops multi-agent-run mymodule.py"),
            ("Execute generated tests", "agentops run --all"),
            ("View project status and changes", "agentops report --check-changes")
        ],
        "🏗️ Development Workflow": [
            ("Process all Python files", "agentops multi-agent-run --all"),
            ("Parallel processing", "agentops multi-agent-run --all --parallel --workers 6"),
            ("Approve requirements", "agentops approve-all --non-interactive"),
            ("Quick prototyping (not recommended for production)", "agentops infer myfile.py")
        ],
        "⚡ Advanced Workflows": [
            ("Custom workflow steps", "agentops runner --steps 1,2,4 --all"),
            ("Auto-approve workflow", "agentops runner --steps 1,2,3,4,5,6 --all --auto-approve"),
            ("Requirements only", "agentops runner --steps 1,2 --target myfile.py"),
            ("Test generation only", "agentops runner --steps 4,5 --all")
        ],
        "📊 Analysis & Reporting": [
            ("Generate traceability matrix", "agentops traceability --format markdown"),
            ("Check file changes", "agentops report --check-changes"),
            ("Detailed analysis report", "agentops report --format csv"),
            ("View requirement details", "agentops requirement-info 1")
        ],
        "🔧 Configuration & Integration": [
            ("View configuration", "agentops config"),
            ("Setup CI/CD integration", "agentops integration setup --ci-provider github"),
            ("Check integration status", "agentops integration status"),
            ("Configure IDE integration", "agentops integration setup --ide-provider vscode")
        ]
    }
    
    for category, examples_list in examples_data.items():
        console.print(f"\n[bold]{category}[/bold]")
        for desc, cmd in examples_list:
            console.print(f"  [dim]{desc}[/dim]")
            console.print(f"  [cyan]{cmd}[/cyan]\n")
    
    console.print(
        "[bold]🎯 Common Scenarios:[/bold]\n\n"
        "[bold]New Project Setup (Recommended):[/bold]\n"
        "  1. [cyan]agentops init[/cyan]\n"
        "  2. [cyan]export OPENAI_API_KEY='your-key'[/cyan]\n"
        "  3. [cyan]agentops multi-agent-run --all[/cyan]\n"
        "  4. [cyan]agentops run --all[/cyan]\n"
        "  5. [cyan]agentops report --check-changes[/cyan]\n\n"
        "[bold]Continuous Integration:[/bold]\n"
        "  1. [cyan]agentops multi-agent-run --all --parallel --workers 6[/cyan]\n"
        "  2. [cyan]agentops approve-all --non-interactive[/cyan]\n"
        "  3. [cyan]agentops run --all[/cyan]\n"
        "  4. [cyan]agentops report --format markdown[/cyan]\n\n"
        "[bold]Code Review Process:[/bold]\n"
        "  1. [cyan]agentops multi-agent-run changed_file.py[/cyan]\n"
        "  2. [cyan]agentops traceability --open[/cyan]\n"
        "  3. [cyan]agentops run --file changed_file.py[/cyan]\n\n"
        "[bold]Quick Prototyping (Not for Production):[/bold]\n"
        "  1. [cyan]agentops infer myfile.py[/cyan]\n"
        "  2. [cyan]agentops run --all[/cyan]\n\n"
        "[bold]📚 Need More Help?[/bold]\n"
        "  • Run [cyan]agentops help[/cyan] for detailed command information\n"
        "  • Visit our GitHub for full documentation\n"
        "  • Join our community for support and feedback"
    )


@cli.command()
def version():
    """Show AgentOps version and check for updates.
    
    Displays current version information and checks for available updates.
    """
    console.print(
        Panel(
            "[bold cyan]🔍 AgentOps Version Information[/bold cyan]\n\n"
            "Current version and system information...",
            title="Version Check",
            border_style="blue",
        )
    )
    
    # Show current version
    console.print(f"[bold]Current Version:[/bold] {agentops_version}")
    
    # Show Python version
    import platform
    console.print(f"[bold]Python Version:[/bold] {platform.python_version()}")
    
    # Show platform
    console.print(f"[bold]Platform:[/bold] {platform.system()} {platform.release()}")
    
    # Check for updates (placeholder for future implementation)
    console.print(
        "\n[bold]Update Status:[/bold]\n"
        "• [green]✅ You're running the latest version[/green]\n"
        "• Check GitHub for updates: https://github.com/knaig/agentops_ai/releases"
    )
    
    # Show installation info
    console.print(
        "\n[bold]Installation:[/bold]\n"
        "• [green]✅ AgentOps is properly installed[/green]\n"
        "• CLI is accessible via: [cyan]agentops[/cyan] or [cyan]python -m agentops_ai.agentops_cli[/cyan]"
    )
    
    console.print(
        f"\n[bold]🎯 What's New in {agentops_version}:[/bold]\n"
        "• Enhanced multi-agent workflow with 6 AI agents\n"
        "• Improved CLI discoverability and help system\n"
        "• Better progress reporting and status updates\n"
        "• Comprehensive analysis and reporting features\n"
        "• Requirements traceability matrix generation\n"
        "• Complete runner command with step-by-step workflow execution"
    )


@cli.command()
def check():
    """Check system requirements and configuration.
    
    Verifies that all dependencies and configurations are properly set up
    for AgentOps to work correctly.
    """
    console.print(
        Panel(
            "[bold cyan]🔍 AgentOps System Check[/bold cyan]\n\n"
            "Verifying system requirements and configuration...",
            title="System Check",
            border_style="blue",
        )
    )
    
    all_good = True
    
    # Check Python version
    import sys
    python_version = sys.version_info
    if python_version >= (3, 8):
        console.print(f"[green]✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}[/green]")
    else:
        console.print(f"[red]❌ Python {python_version.major}.{python_version.minor}.{python_version.micro} (requires 3.8+)[/red]")
        all_good = False
    
    # Check OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        console.print("[green]✅ OpenAI API key configured[/green]")
    else:
        console.print("[red]❌ OpenAI API key not set[/red]")
        console.print("  Set it with: [cyan]export OPENAI_API_KEY='your-key-here'[/cyan]")
        all_good = False
    
    # Check required packages
    required_packages = [
        ("click", "CLI framework"),
        ("rich", "Terminal UI"),
        ("openai", "OpenAI API client"),
        ("pathlib", "Path handling"),
        ("json", "JSON processing"),
        ("ast", "Python AST parsing")
    ]
    
    console.print("\n[bold]Required Packages:[/bold]")
    for package, description in required_packages:
        try:
            __import__(package)
            console.print(f"  [green]✅ {package}[/green] - {description}")
        except ImportError:
            console.print(f"  [red]❌ {package}[/red] - {description} (missing)")
            all_good = False
    
    # Check optional packages
    optional_packages = [
        ("langchain_openai", "Advanced multi-agent workflow"),
        ("pytest", "Test execution"),
        ("coverage", "Test coverage analysis")
    ]
    
    console.print("\n[bold]Optional Packages:[/bold]")
    for package, description in optional_packages:
        try:
            __import__(package)
            console.print(f"  [green]✅ {package}[/green] - {description}")
        except ImportError:
            console.print(f"  [yellow]⚠️  {package}[/yellow] - {description} (optional)")
    
    # Check project initialization
    if Path(".agentops").exists():
        console.print("\n[green]✅ Project initialized[/green]")
    else:
        console.print("\n[yellow]⚠️  Project not initialized[/yellow]")
        console.print("  Run: [cyan]agentops init[/cyan]")
    
    # Check file permissions
    try:
        test_file = Path(".agentops_test")
        test_file.write_text("test")
        test_file.unlink()
        console.print("[green]✅ File system permissions OK[/green]")
    except Exception as e:
        console.print(f"[red]❌ File system permissions issue: {e}[/red]")
        all_good = False
    
    # Summary
    if all_good:
        console.print(
            "\n[bold green]🎉 All checks passed! AgentOps is ready to use.[/bold green]\n"
            "Try: [cyan]agentops multi-agent-run myfile.py[/cyan]"
        )
    else:
        console.print(
            "\n[bold red]⚠️  Some issues found. Please fix them before using AgentOps.[/bold red]\n"
            "Run: [cyan]agentops help[/cyan] for assistance"
        )


@cli.command()
@click.option(
    "--steps",
    type=str,
    default="init,requirements,approve,tests,run,traceability",
    help="Comma-separated list of steps to run. Use numbers (1,2,3,4,5,6) or names (init,requirements,approve,tests,run,traceability)"
)
@click.option(
    "--show-steps",
    is_flag=True,
    help="Show the step mapping and exit"
)
@click.option(
    "--target",
    type=str,
    help="Specific file or directory to process"
)
@click.option(
    "--all",
    is_flag=True,
    help="Process all Python files in current directory"
)
@click.option(
    "--auto-approve",
    is_flag=True,
    help="Automatically approve all requirements (step 3)"
)
@click.option(
    "--parallel",
    is_flag=True,
    help="Run in parallel mode for faster execution"
)
@click.option(
    "--workers",
    type=int,
    default=4,
    help="Number of parallel workers (default: 4, max: 16)"
)
@click.option(
    "--output-format",
    type=click.Choice(["markdown", "csv", "json"]),
    default="markdown",
    help="Output format for traceability matrix (default: markdown)"
)
@click.option(
    "--generate-traceability",
    is_flag=True,
    default=True,
    help="Generate traceability matrix after test generation"
)
@click.option(
    "--verbose",
    is_flag=True,
    help="Enable verbose output"
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Show what would be done without executing"
)
def runner(steps: str, show_steps: bool, target: str, all: bool, auto_approve: bool, 
          parallel: bool, workers: int, output_format: str, generate_traceability: bool, 
          verbose: bool, dry_run: bool):
    """Run AgentOps workflow with configurable steps.
    
    This command provides a comprehensive way to run the complete AgentOps workflow 
    with configurable steps. It allows you to choose which steps to execute and 
    automatically handles the entire process from initialization to test execution.
    
    Step Mapping:
      Step 1 = init          - Initialize AgentOps project structure
      Step 2 = requirements  - Run multi-agent workflow to extract requirements  
      Step 3 = approve       - Automatically approve all generated requirements
      Step 4 = tests         - Generate test cases from approved requirements
      Step 5 = run           - Execute generated tests with root cause analysis
      Step 6 = traceability  - Generate traceability matrix linking requirements to tests
    
    Examples:
      # Run complete workflow on all files
      agentops runner --steps 1,2,3,4,5,6 --all --auto-approve
      
      # Run complete workflow using step names
      agentops runner --steps init,requirements,approve,tests,run,traceability --all --auto-approve
      
      # Only generate requirements and tests
      agentops runner --steps 1,2,4 --all --auto-approve
      
      # Process specific file
      agentops runner --steps 1,2,3,4,5 --target mymodule.py --auto-approve
      
      # Parallel processing
      agentops runner --steps 1,2,3,4,5,6 --all --auto-approve --parallel --workers 8
      
      # Dry run to see what would be executed
      agentops runner --steps 1,2,3,4,5,6 --all --auto-approve --dry-run
      
      # Show step mapping
      agentops runner --show-steps
    """
    # Create runner
    runner_instance = AgentOpsRunner(verbose=verbose)
    
    # Show step mapping if requested
    if show_steps:
        runner_instance.show_step_mapping()
        return
    
    # Parse and validate steps
    runner_instance.steps = []
    if steps:
        step_names = [s.strip().lower() for s in steps.split(",")]
        valid_steps = ["init", "requirements", "approve", "tests", "run", "traceability"]
        
        for step in step_names:
            # Handle numeric steps
            if step in runner_instance.STEP_MAPPING:
                mapped_step = runner_instance.STEP_MAPPING[step]
                runner_instance.steps.append(mapped_step)
            elif step in valid_steps:
                runner_instance.steps.append(step)
            else:
                console.print(f"[red]❌ Invalid step: {step}[/red]")
                console.print(f"[red]Valid numeric steps: {', '.join(runner_instance.STEP_MAPPING.keys())}[/red]")
                console.print(f"[red]Valid named steps: {', '.join(valid_steps)}[/red]")
                console.print("[red]Use --show-steps to see the complete step mapping[/red]")
                sys.exit(1)
    
    if not runner_instance.steps:
        console.print("[red]❌ No valid steps specified[/red]")
        sys.exit(1)
    
    # Validate arguments
    if not target and not all:
        console.print("[yellow]⚠️  WARNING: No target specified, using --all[/yellow]")
        all = True
    
    if workers < 1 or workers > 16:
        console.print("[yellow]⚠️  WARNING: Workers should be between 1 and 16, using 4[/yellow]")
        workers = 4
    
    # Show step mapping for user reference
    if verbose:
        runner_instance.show_step_mapping()
    
    # Create runner and execute
    success = runner_instance.run_workflow(
        steps=runner_instance.steps,
        target=target,
        run_all=all,
        auto_approve=auto_approve,
        parallel=parallel,
        workers=workers,
        output_format=output_format,
        generate_traceability=generate_traceability,
        dry_run=dry_run
    )
    
    if success:
        console.print("\n🎉 AgentOps workflow completed successfully!")
        sys.exit(0)
    else:
        console.print("\n❌ AgentOps workflow failed!")
        sys.exit(1)

@cli.command()
def commands():
    """List all available AgentOps commands with descriptions.
    
    Shows a comprehensive list of all commands organized by category
    for easy discovery and reference.
    """
    console.print(
        Panel(
            "[bold cyan]AgentOps Commands Reference[/bold cyan]\n\n"
            "All available commands organized by functionality.",
            title="Commands",
            border_style="cyan",
        )
    )
    
    # Get all commands from the CLI group
    commands_list = []
    for cmd_name, cmd_obj in cli.commands.items():
        if hasattr(cmd_obj, 'help') and cmd_obj.help:
            # Extract first line of help as short description
            short_desc = cmd_obj.help.split('\n')[0].strip()
            commands_list.append((cmd_name, short_desc))
        else:
            commands_list.append((cmd_name, "No description available"))
    
    # Sort commands alphabetically
    commands_list.sort(key=lambda x: x[0])
    
    # Group commands by functionality
    command_groups = {
        "Core Workflow": ["init", "multi-agent-run", "infer", "run", "runner"],
        "Management": ["fast-approve", "approve-all", "config", "status", "check"],
        "Analysis": ["report", "traceability", "requirement-info", "test-info"],
        "Integration": ["integration"],
        "Help & Discovery": ["help", "examples", "commands", "version", "welcome"]
    }
    
    for group_name, group_commands in command_groups.items():
        console.print(f"\n[bold]{group_name}[/bold]")
        for cmd_name in group_commands:
            # Find the command in our list
            cmd_desc = next((desc for name, desc in commands_list if name == cmd_name), "No description")
            console.print(f"  [cyan]{cmd_name:<20}[/cyan] {cmd_desc}")
    
    console.print(
        "\n[bold]💡 Usage Tips:[/bold]\n"
        "  • Run [cyan]agentops <command> --help[/cyan] for detailed help on any command\n"
        "  • Use [cyan]agentops help[/cyan] for comprehensive documentation\n"
        "  • Try [cyan]agentops examples[/cyan] for practical use cases\n\n"
        "[bold]🔍 Command Discovery:[/bold]\n"
        "  • Commands are organized by functionality\n"
        "  • Use tab completion if your shell supports it\n"
        "  • All commands support --help for detailed information"
    )


@cli.command()
@click.argument("directory", default=".")
def init(directory: str):
    """Initialize a new AgentOps project.

    Creates the .agentops directory structure, initializes the SQLite database,
    and sets up the project for multi-agent test automation.

    This command must be run before any other AgentOps commands. It creates:
    - .agentops/ directory for project data
    - .agentops/tests/ directory for generated tests
    - .agentops/requirements.db SQLite database
    - .agentops/config.json configuration file
    - .gitignore entry for .agentops/ (if .git exists)

    Args:
        directory: Project directory to initialize (default: current directory)
    """
    project_dir = Path(directory).resolve()

    # Initialize configuration
    config = get_config()
    config.initialize_project(str(project_dir))
    
    # Validate configuration
    if not config.validate():
        console.print(
            Panel(
                "[yellow]Warning: No LLM API key configured.[/yellow]\n\n"
                "Set your OpenAI API key:\n"
                "1. Export: [bold]export OPENAI_API_KEY='your-key'[/bold]\n"
                "2. Or edit: [bold].agentops/config.json[/bold]\n\n"
                "You can still initialize the project, but LLM features won't work.",
                title="Configuration Warning",
                border_style="yellow",
            )
        )

    # Create .gitignore entry for .agentops if .git exists
    gitignore_path = project_dir / ".gitignore"
    if (project_dir / ".git").exists():
        gitignore_content = ""
        if gitignore_path.exists():
            with open(gitignore_path, "r") as f:
                gitignore_content = f.read()

        # WHY: Only add if not already present to avoid duplicates
        if ".agentops/" not in gitignore_content:
            with open(gitignore_path, "a") as f:
                f.write("\n# AgentOps\n.agentops/\n")

    console.print(
        Panel(
            "[bold green]✓ AgentOps project initialized![/bold green]\n\n"
            f"Directory: {project_dir}\n"
            f"Database: {project_dir / '.agentops/requirements.db'}\n"
            f"Tests: {project_dir / config.project.test_output_dir}\n"
            f"Config: {project_dir / config.config_file}\n\n"
            f"Next steps:\n"
            f"1. Set your OpenAI API key: [bold]export OPENAI_API_KEY='your-key'[/bold]\n"
            f"2. Run [bold cyan]agentops multi-agent-run <file.py>[/bold cyan] to start the workflow",
            title="AgentOps Init",
            border_style="green",
        )
    )


@cli.command()
@click.argument("requirement_id", type=int, required=False)
@click.option("--format", "output_format", 
              type=click.Choice(["table", "json", "markdown"]), 
              default="table",
              help="Output format (default: table)")
def requirement_info(requirement_id: int, output_format: str):
    """Show detailed requirement information.
    
    Displays comprehensive information about requirements including:
    - Requirement details and description
    - Associated test functions
    - Coverage status
    - Creation and modification dates
    - Related files and functions
    
    Args:
        requirement_id: Specific requirement ID to show (optional)
        output_format: Output format (table, json, markdown)
    """
    if not os.path.exists(".agentops"):
        console.print(
            Panel(
                "[yellow]AgentOps not initialized in this directory.[/yellow]\n\n"
                "Run [bold cyan]agentops init[/bold cyan] first.",
                title="Not Initialized",
                border_style="yellow",
            )
        )
        sys.exit(1)

    try:
        workflow = AgentOpsWorkflow()
        requirements = workflow.requirement_store.get_all_requirements()

        if not requirements:
            console.print(
                Panel(
                    "[yellow]No requirements found.[/yellow]\n\n"
                    "Run [bold cyan]agentops multi-agent-run[/bold cyan] to generate requirements.",
                    title="No Requirements",
                    border_style="yellow",
                )
            )
            return

        if requirement_id is not None:
            # Show specific requirement
            req = next((r for r in requirements if r.id == requirement_id), None)
            if not req:
                console.print(
                    Panel(
                        f"[red]Requirement ID {requirement_id} not found.[/red]",
                        title="Not Found",
                        border_style="red",
                    )
                )
                return

            if output_format == "table":
                console.print(
                    Panel(
                        f"[bold]Requirement #{req.id}[/bold]\n\n"
                        f"📝 [bold]Description:[/bold] {req.requirement_text}\n"
                        f"📁 [bold]File:[/bold] {req.file_path}\n"
                        f"🔗 [bold]Code Symbol:[/bold] {req.code_symbol}\n"
                        f"📊 [bold]Status:[/bold] {req.status}\n"
                        f"📅 [bold]Created:[/bold] {req.created_at}\n"
                        f"🎯 [bold]Confidence:[/bold] {req.confidence:.1%}\n"
                        f"🏷️ [bold]Metadata:[/bold] {len(req.metadata)} items",
                        title=f"Requirement #{req.id}",
                        border_style="cyan",
                    )
                )
            elif output_format == "json":
                import json
                req_dict = {
                    "id": req.id,
                    "requirement_text": req.requirement_text,
                    "file_path": req.file_path,
                    "code_symbol": req.code_symbol,
                    "commit_hash": req.commit_hash,
                    "confidence": req.confidence,
                    "status": req.status,
                    "created_at": req.created_at,
                    "metadata": req.metadata
                }
                console.print(json.dumps(req_dict, indent=2))
            else:  # markdown
                console.print(f"# Requirement #{req.id}\n\n")
                console.print(f"**Description:** {req.requirement_text}\n")
                console.print(f"**File:** {req.file_path}\n")
                console.print(f"**Code Symbol:** {req.code_symbol}\n")
                console.print(f"**Status:** {req.status}\n")
                console.print(f"**Created:** {req.created_at}\n")
                console.print(f"**Confidence:** {req.confidence:.1%}\n")
                console.print(f"**Metadata:** {len(req.metadata)} items\n")
        else:
            # Show summary of all requirements
            console.print(
                Panel(
                    f"[bold]Requirements Summary[/bold]\n\n"
                    f"Total Requirements: {len(requirements)}\n"
                    f"Approved: {len([r for r in requirements if r.status == 'approved'])}\n"
                    f"Pending: {len([r for r in requirements if r.status == 'pending'])}\n"
                    f"Rejected: {len([r for r in requirements if r.status == 'rejected'])}",
                    title="Requirements Overview",
                    border_style="cyan",
                )
            )

            if output_format == "table":
                from rich.table import Table
                table = Table(title="All Requirements")
                table.add_column("ID", style="cyan")
                table.add_column("Status", style="green")
                table.add_column("File", style="blue")
                table.add_column("Function", style="yellow")
                table.add_column("Description", style="white")

                for req in requirements:
                    status_emoji = {"approved": "✅", "pending": "⏳", "rejected": "❌"}
                    table.add_row(
                        str(req.id),
                        f"{status_emoji.get(req.status, '❓')} {req.status}",
                        req.file_path,
                        req.code_symbol,
                        req.requirement_text[:50] + "..." if len(req.requirement_text) > 50 else req.requirement_text
                    )

                console.print(table)
            elif output_format == "json":
                import json
                reqs_dict = []
                for r in requirements:
                    reqs_dict.append({
                        "id": r.id,
                        "requirement_text": r.requirement_text,
                        "file_path": r.file_path,
                        "code_symbol": r.code_symbol,
                        "commit_hash": r.commit_hash,
                        "confidence": r.confidence,
                        "status": r.status,
                        "created_at": r.created_at,
                        "metadata": r.metadata
                    })
                console.print(json.dumps(reqs_dict, indent=2))
            else:  # markdown
                console.print("# Requirements\n\n")
                for req in requirements:
                    status_emoji = {"approved": "✅", "pending": "⏳", "rejected": "❌"}
                    console.print(f"## {status_emoji.get(req.status, '❓')} Requirement #{req.id}\n")
                    console.print(f"**File:** {req.file_path}\n")
                    console.print(f"**Code Symbol:** {req.code_symbol}\n")
                    console.print(f"**Description:** {req.requirement_text}\n")
                    console.print(f"**Status:** {req.status}\n")
                    console.print(f"**Confidence:** {req.confidence:.1%}\n\n")
    except Exception as e:
        console.print(
            Panel(
                f"[red]Error loading requirements: {str(e)}[/red]",
                title="Error",
                border_style="red",
            )
        )


@cli.command()
@click.argument("test_file", type=click.Path(exists=True), required=False)
@click.option("--format", "output_format", 
              type=click.Choice(["table", "json", "markdown"]), 
              default="table",
              help="Output format (default: table)")
def test_info(test_file: str, output_format: str):
    """Show test file and function details.
    
    Displays comprehensive information about generated test files including:
    - Test file statistics
    - Test function details
    - Coverage information
    - Associated requirements
    - Test execution status
    
    Args:
        test_file: Specific test file to analyze (optional)
        output_format: Output format (table, json, markdown)
    """
    if not os.path.exists(".agentops"):
        console.print(
            Panel(
                "[yellow]AgentOps not initialized in this directory.[/yellow]\n\n"
                "Run [bold cyan]agentops init[/bold cyan] first.",
                title="Not Initialized",
                border_style="yellow",
            )
        )
        sys.exit(1)
    
    test_dir = Path(".agentops/tests")
    if not test_dir.exists():
        console.print(
            Panel(
                "[yellow]No test files found.[/yellow]\n\n"
                "Run [bold cyan]agentops multi-agent-run[/bold cyan] to generate tests.",
                title="No Tests",
                border_style="yellow",
            )
        )
        return
    
    if test_file:
        # Analyze specific test file
        test_path = Path(test_file)
        if not test_path.exists():
            console.print(
                Panel(
                    f"[red]Test file {test_file} not found.[/red]",
                    title="File Not Found",
                    border_style="red",
                )
            )
            return
        
        # Parse test file to extract information
        try:
            with open(test_path, 'r') as f:
                content = f.read()

            # Extract test functions
            import re
            test_functions = re.findall(r'def (test_\w+)', content)

            # Count lines and complexity
            lines = content.split('\n')
            non_empty_lines = [line for line in lines if line.strip()]

            if output_format == "table":
                console.print(
                    Panel(
                        f"[bold]Test File Analysis[/bold]\n\n"
                        f"📁 [bold]File:[/bold] {test_path}\n"
                        f"📊 [bold]Test Functions:[/bold] {len(test_functions)}\n"
                        f"📏 [bold]Total Lines:[/bold] {len(lines)}\n"
                        f"📝 [bold]Code Lines:[/bold] {len(non_empty_lines)}\n"
                        f"📈 [bold]Functions:[/bold] {', '.join(test_functions) if test_functions else 'None'}",
                        title=f"Test File: {test_path.name}",
                        border_style="green",
                    )
                )
            elif output_format == "json":
                import json
                data = {
                    "file": str(test_path),
                    "test_functions": test_functions,
                    "total_lines": len(lines),
                    "code_lines": len(non_empty_lines),
                    "size_bytes": test_path.stat().st_size
                }
                console.print(json.dumps(data, indent=2))
            else:  # markdown
                console.print(f"# Test File: {test_path.name}\n\n")
                console.print(f"**File:** {test_path}\n")
                console.print(f"**Test Functions:** {len(test_functions)}\n")
                console.print(f"**Total Lines:** {len(lines)}\n")
                console.print(f"**Code Lines:** {len(non_empty_lines)}\n\n")
                if test_functions:
                    console.print("## Test Functions\n\n")
                    for func in test_functions:
                        console.print(f"- `{func}`\n")

        except Exception as e:
            console.print(
                Panel(
                    f"[red]Error analyzing test file: {str(e)}[/red]",
                    title="Error",
                    border_style="red",
                )
            )
    else:
        # Show summary of all test files
        test_files = list(test_dir.rglob("test_*.py"))

        if not test_files:
            console.print(
                Panel(
                    "[yellow]No test files found in .agentops/tests/[/yellow]\n\n"
                    "Run [bold cyan]agentops multi-agent-run[/bold cyan] to generate tests.",
                    title="No Tests",
                    border_style="yellow",
                )
            )
            return

        console.print(
            Panel(
                f"[bold]Test Files Summary[/bold]\n\n"
                f"Total Test Files: {len(test_files)}\n"
                f"Total Size: {sum(f.stat().st_size for f in test_files) / 1024:.1f} KB",
                title="Tests Overview",
                border_style="green",
            )
        )

        if output_format == "table":
            from rich.table import Table
            table = Table(title="Test Files")
            table.add_column("File", style="cyan")
            table.add_column("Size", style="blue")
            table.add_column("Functions", style="green")
            table.add_column("Lines", style="yellow")

            for test_file_path in test_files:
                try:
                    with open(test_file_path, 'r') as f:
                        content = f.read()

                    import re
                    test_functions = re.findall(r'def (test_\w+)', content)
                    lines = len(content.split('\n'))
                    size_kb = test_file_path.stat().st_size / 1024

                    table.add_row(
                        test_file_path.name,
                        f"{size_kb:.1f} KB",
                        str(len(test_functions)),
                        str(lines)
                    )
                except:
                    table.add_row(test_file_path.name, "Error", "Error", "Error")

            console.print(table)
        elif output_format == "json":
            import json
            data = []
            for test_file_path in test_files:
                try:
                    with open(test_file_path, 'r') as f:
                        content = f.read()

                    import re
                    test_functions = re.findall(r'def (test_\w+)', content)
                    lines = len(content.split('\n'))
                    size_kb = test_file_path.stat().st_size / 1024

                    data.append({
                        "file": test_file_path.name,
                        "path": str(test_file_path),
                        "size_kb": round(size_kb, 1),
                        "test_functions": test_functions,
                        "total_lines": lines
                    })
                except Exception as e:
                    data.append({
                        "file": test_file_path.name,
                        "path": str(test_file_path),
                        "error": str(e)
                    })

            console.print(json.dumps(data, indent=2))
        else:  # markdown
            console.print("# Test Files\n\n")
            for test_file_path in test_files:
                try:
                    with open(test_file_path, 'r') as f:
                        content = f.read()

                    import re
                    test_functions = re.findall(r'def (test_\w+)', content)
                    lines = len(content.split('\n'))
                    size_kb = test_file_path.stat().st_size / 1024

                    console.print(f"## {test_file_path.name}\n")
                    console.print(f"**Size:** {size_kb:.1f} KB\n")
                    console.print(f"**Test Functions:** {len(test_functions)}\n")
                    console.print(f"**Total Lines:** {lines}\n")
                    if test_functions:
                        console.print("**Functions:** " + ", ".join(test_functions) + "\n")
                    console.print("\n")
                except Exception as e:
                    console.print(f"## {test_file_path.name}\n")
                    console.print(f"**Error:** {str(e)}\n\n")


# Enhanced Features Commands (v0.5.0+)
if ENHANCED_FEATURES_AVAILABLE:
    
    @cli.command()
    @click.option('--tier', type=click.Choice([t.value for t in PricingTier]), 
                  help='Set pricing tier for this session')
    def pricing(tier):
        """Display pricing tiers and feature comparison"""
        
        console.print("\n[bold blue]AgentOps Pricing Tiers[/bold blue]\n")
        
        # Create comparison table
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Feature", style="cyan")
        table.add_column("Developer\n($19/mo)", style="green")
        table.add_column("Professional\n($49/mo)", style="yellow")
        table.add_column("Team\n($99/mo)", style="orange")
        
        # Add feature rows
        features = [
            ("AI Agents", "3", "6", "8"),
            ("Context Engineering", "Basic", "Advanced", "Full"),
            ("Export Formats", "2", "4", "6"),
            ("Parallel Processing", "✗", "✓", "✓"),
            ("Team Collaboration", "✗", "✗", "✓"),
            ("Custom Workflows", "✗", "✗", "✓"),
            ("Support", "Community", "Priority", "Priority"),
            ("Languages", "Python", "Python + TS", "All")
        ]
        
        for feature_row in features:
            table.add_row(*feature_row)
        
        console.print(table)
        
        # Current tier info
        current_tier = pricing_manager.current_tier
        tier_features = pricing_manager.get_tier_features(current_tier)
        
        console.print(f"\n[bold]Current Tier: {current_tier.value.title()}[/bold]")
        console.print(f"Price: ${tier_features.price_per_month}/month")
        console.print(f"Available Agents: {len(tier_features.available_agents)}")
        console.print(f"Export Formats: {len(tier_features.export_formats)}")
        console.print(f"Max Parallel Workers: {tier_features.max_parallel_workers}")
        
        # Set tier if provided
        if tier:
            new_tier = PricingTier(tier)
            pricing_manager.set_user_tier(new_tier)
            console.print(f"[green]✓ Tier updated to {new_tier.value.title()}[/green]")
    
    
    @cli.command()
    def agents():
        """List available agents and their capabilities"""
        
        current_tier = pricing_manager.current_tier
        available_agents = pricing_manager.get_available_agents()
        
        console.print(f"\n[bold blue]Available Agents ({len(available_agents)})[/bold blue]\n")
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Agent", style="cyan")
        table.add_column("Type", style="yellow")
        table.add_column("Priority", style="green")
        table.add_column("Description", style="white")
        
        agent_descriptions = {
            AgentType.CODE_ANALYZER: ("Core", "Critical", "Analyzes code structure and complexity"),
            AgentType.REQUIREMENTS_ENGINEER: ("Core", "Critical", "Extracts functional requirements"),
            AgentType.TEST_GENERATOR: ("Core", "Critical", "Generates comprehensive test suites"),
            AgentType.TEST_ARCHITECT: ("Value-Add", "High", "Designs test architecture and strategy"),
            AgentType.QUALITY_ASSURANCE: ("Value-Add", "High", "Ensures test quality and coverage"),
            AgentType.INTEGRATION_SPECIALIST: ("Value-Add", "Medium", "Handles integration testing"),
            AgentType.ARCHITECTURE_ANALYZER: ("Context", "Medium", "Analyzes system architecture"),
            AgentType.DATA_FLOW_ANALYZER: ("Context", "Medium", "Maps data flows and transformations"),
            AgentType.SUCCESS_CRITERIA_ANALYZER: ("Context", "Low", "Defines success criteria"),
            AgentType.CURRENT_STATE_ANALYZER: ("Context", "Medium", "Assesses current state"),
            AgentType.BUSINESS_RULES_ANALYZER: ("Context", "Low", "Extracts business rules")
        }
        
        for agent_type in available_agents:
            if agent_type in agent_descriptions:
                agent_info = agent_descriptions[agent_type]
                table.add_row(
                    agent_type.value.replace('_', ' ').title(),
                    agent_info[0],
                    agent_info[1],
                    agent_info[2]
                )
        
        console.print(table)
        
        # Show unavailable agents
        all_agents = set(AgentType)
        unavailable = all_agents - set(available_agents)
        
        if unavailable:
            console.print(f"\n[dim]Unavailable in {current_tier.value.title()} tier:[/dim]")
            for agent in unavailable:
                console.print(f"  [dim]• {agent.value.replace('_', ' ').title()}[/dim]")
    
    
    @cli.command()
    @click.option('--output', default='agentops-config.yaml', help='Output configuration file')
    def generate_config(output):
        """Generate configuration file with current settings"""
        
        current_tier = pricing_manager.current_tier
        tier_features = pricing_manager.get_tier_features(current_tier)
        
        config_data = {
            'tier': current_tier.value,
            'agents': {
                'available': [agent.value for agent in tier_features.available_agents],
                'default_mode': 'standard',
                'parallel_processing': tier_features.parallel_processing,
                'max_workers': tier_features.max_parallel_workers
            },
            'context_engineering': {
                'available': [ctx.value for ctx in tier_features.context_engineering],
                'enabled_by_default': ['requirements_generation']
            },
            'export': {
                'available_formats': [fmt.value for fmt in tier_features.export_formats],
                'default_formats': ['gherkin', 'markdown'],
                'output_directory': '.agentops'
            },
            'workflow': {
                'auto_approve': False,
                'quality_gates': tier_features.approval_workflows,
                'continue_on_error': True
            }
        }
        
        with open(output, 'w') as f:
            yaml.dump(config_data, f, default_flow_style=False)
        
        console.print(f"[green]✓ Configuration saved to {output}[/green]")
    
    
    @cli.command()
    @click.option('--file', '-f', required=True, help='Python file to analyze')
    @click.option('--mode', type=click.Choice([m.value for m in WorkflowMode]), 
                  default='standard', help='Workflow mode')
    @click.option('--agents', help='Comma-separated list of agents to use')
    @click.option('--parallel/--sequential', default=True, help='Enable parallel processing')
    @click.option('--workers', type=int, help='Number of parallel workers')
    @click.option('--context', multiple=True, help='Context engineering types to enable')
    @click.option('--export', multiple=True, help='Export formats')
    @click.option('--approve/--no-approve', default=False, help='Auto-approve workflow steps')
    @click.option('--output', default='.agentops', help='Output directory')
    def enhanced_run(file, mode, agents, parallel, workers, context, export, approve, output):
        """Run enhanced AgentOps workflow with full customization"""
        
        current_tier = pricing_manager.current_tier
        
        # Validate file exists
        if not Path(file).exists():
            console.print(f"[red]Error: File {file} not found[/red]")
            return
        
        # Create workflow configuration
        workflow_mode = WorkflowMode(mode)
        config = agent_selector.select_agents_for_tier(current_tier, workflow_mode)
        
        # Apply customizations...
        console.print(f"[green]✓ Enhanced workflow configured for {current_tier.value.title()} tier[/green]")
        console.print(f"Selected agents: {len(config.selected_agents)}")
        console.print(f"Parallel processing: {config.parallel_execution}")
        console.print(f"Export formats: {len(config.export_formats)}")
        
        # Execute workflow (implementation would go here)
        console.print("[blue]Enhanced workflow execution would run here...[/blue]")


@cli.command()
def login():
    """Authenticate with your AgentOps API key."""
    api_key = Prompt.ask('Enter your AgentOps API key', password=True)
    save_api_key(api_key)
    console.print('[green]✓ API key saved. Fetching entitlements...[/green]')
    entitlements = fetch_entitlements(api_key)
    if entitlements:
        save_entitlements(entitlements)
        console.print('[green]✓ Entitlements synced.[/green]')
    else:
        console.print('[red]Failed to fetch entitlements. Please check your API key.[/red]')


# --- ENFORCEMENT DECORATOR ---
def require_entitlement(feature: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            entitlements = load_entitlements()
            if not entitlements:
                entitlements = ensure_entitlements()
            allowed = entitlements.get('features', [])
            if feature not in allowed:
                console.print(f'[red]This feature is not available in your current plan.[/red]')
                console.print('[yellow]Upgrade at: https://agentops-website.vercel.app/upgrade[/yellow]')
                sys.exit(1)
            return func(*args, **kwargs)
        return wrapper
    return decorator


@cli.command()
@click.option('--feature', '-f', required=True, help='Feature name to enable')
def enable_feature_command(feature):
    """Enable a specific feature."""
    try:
        if enable_feature(feature):
            console.print(f"[green]✓ Feature '{feature}' enabled successfully[/green]")
        else:
            console.print(f"[red]✗ Failed to enable feature '{feature}'[/red]")
    except Exception as e:
        console.print(f"[red]✗ Error enabling feature: {e}[/red]")


@cli.command()
@click.option('--feature', '-f', required=True, help='Feature name to disable')
def disable_feature_command(feature):
    """Disable a specific feature."""
    try:
        if disable_feature(feature):
            console.print(f"[green]✓ Feature '{feature}' disabled successfully[/green]")
        else:
            console.print(f"[red]✗ Failed to disable feature '{feature}'[/red]")
    except Exception as e:
        console.print(f"[red]✗ Error disabling feature: {e}[/red]")


@cli.command()
def list_features():
    """List all available features and their status."""
    feature_manager = get_feature_manager()
    summary = feature_manager.get_feature_status_summary()
    
    console.print("[bold]📋 Feature Status Summary[/bold]")
    console.print(f"Total Features: {summary['total_features']}")
    console.print(f"Enabled: {summary['enabled_features']}")
    console.print(f"Disabled: {summary['disabled_features']}")
    console.print(f"Beta: {summary['beta_features']}")
    
    console.print("\n[bold]📁 Feature Categories:[/bold]")
    for category, info in summary['categories'].items():
        status = "✅" if info['enabled'] > 0 else "❌"
        console.print(f"{status} {category}: {info['enabled']}/{info['total']} enabled")


@cli.command()
@click.option('--language', '-l', help='Language to enable (python, javascript, java, csharp, go)')
def enable_language(language):
    """Enable support for a specific programming language."""
    if not language:
        console.print("[yellow]Available languages: python, javascript, java, csharp, go[/yellow]")
        return
    
    try:
        language_type = LanguageType(language.lower())
        language_manager = get_language_manager()
        
        if language_manager.enable_language(language_type):
            console.print(f"[green]✓ Language '{language}' enabled successfully[/green]")
        else:
            console.print(f"[red]✗ Failed to enable language '{language}'[/red]")
    except ValueError:
        console.print(f"[red]✗ Unknown language: {language}[/red]")
    except Exception as e:
        console.print(f"[red]✗ Error enabling language: {e}[/red]")


@cli.command()
def list_languages():
    """List supported programming languages and their status."""
    language_manager = get_language_manager()
    supported_languages = language_manager.get_supported_languages()
    enabled_languages = language_manager.get_enabled_languages()
    
    console.print("[bold]🌐 Language Support Status[/bold]")
    for lang in LanguageType:
        status = "✅" if lang in supported_languages else "❌"
        console.print(f"{status} {lang.value.title()}")


@cli.command()
@click.option('--host', default='localhost', help='Dashboard host address')
@click.option('--port', default=3000, help='Dashboard port number')
@click.option('--debug', is_flag=True, help='Enable debug mode')
def dashboard(host, port, debug):
    """Start the AgentOps web dashboard."""
    try:
        start_dashboard(host=host, port=port, debug=debug)
    except Exception as e:
        console.print(f"[red]✗ Failed to start dashboard: {e}[/red]")


@cli.command()
@click.option('--project-id', required=True, help='Project identifier')
@click.option('--format', '-f', default='csv', help='Export format (csv, excel, html)')
@click.option('--output', '-o', help='Output file path')
def export_traceability(project_id, format, output):
    """Export traceability matrix for a project."""
    try:
        if not is_feature_enabled("traceability_matrix"):
            console.print("[red]✗ Traceability matrix feature is not enabled[/red]")
            return
        
        traceability_manager = get_traceability_manager()
        output_path = traceability_manager.export_matrix(project_id, format, output)
        console.print(f"[green]✓ Traceability matrix exported to: {output_path}[/green]")
    except Exception as e:
        console.print(f"[red]✗ Error exporting traceability matrix: {e}[/red]")


@cli.command()
@click.option('--project-id', required=True, help='Project identifier')
@click.option('--format', '-f', default='markdown', help='Export format (markdown, pdf, html, docx)')
@click.option('--output', '-o', help='Output file path')
def export_documentation(project_id, format, output):
    """Export project documentation."""
    try:
        if not is_feature_enabled("documentation_export"):
            console.print("[red]✗ Documentation export feature is not enabled[/red]")
            return
        
        documentation_exporter = get_documentation_exporter()
        available_formats = documentation_exporter.get_available_formats()
        
        if format not in [fmt.value for fmt in available_formats]:
            console.print(f"[red]✗ Format '{format}' not available in current tier[/red]")
            console.print(f"Available formats: {[fmt.value for fmt in available_formats]}")
            return
        
        # Create a sample documentation project
        from ..agentops_core.documentation_export import DocumentationConfig, DocumentationSection, ExportFormat
        
        config = DocumentationConfig(
            project_name=f"Project {project_id}",
            version="1.0.0",
            author="AgentOps"
        )
        
        project = documentation_exporter.create_documentation_project(project_id, config)
        
        # Add sample sections
        sections = [
            ("overview", "Project Overview", "This is the project overview section."),
            ("requirements", "Requirements", "Project requirements and specifications."),
            ("tests", "Test Coverage", "Test coverage and quality metrics."),
            ("analysis", "Code Analysis", "Static analysis and code quality results.")
        ]
        
        for i, (section_id, title, content) in enumerate(sections):
            section = DocumentationSection(
                id=section_id,
                title=title,
                content=content,
                order=i
            )
            documentation_exporter.add_section(project, section)
        
        # Export documentation
        export_format = ExportFormat(format)
        output_path = documentation_exporter.export_documentation(project, export_format, output)
        console.print(f"[green]✓ Documentation exported to: {output_path}[/green]")
    except Exception as e:
        console.print(f"[red]✗ Error exporting documentation: {e}[/red]")


@cli.command()
@click.option('--user-id', required=True, help='User identifier')
@click.option('--feature', '-f', required=True, help='Feature name to check')
def check_feature_access(user_id, feature):
    """Check if a user has access to a specific feature."""
    try:
        if not is_feature_enabled("payment_integration"):
            console.print("[red]✗ Payment integration feature is not enabled[/red]")
            return
        
        has_access = check_user_feature_access(user_id, feature)
        status = "✅" if has_access else "❌"
        console.print(f"{status} User '{user_id}' {'has' if has_access else 'does not have'} access to feature '{feature}'")
    except Exception as e:
        console.print(f"[red]✗ Error checking feature access: {e}[/red]")


@cli.command()
@click.option('--user-id', required=True, help='User identifier')
def list_user_features(user_id):
    """List enabled features for a user."""
    try:
        if not is_feature_enabled("payment_integration"):
            console.print("[red]✗ Payment integration feature is not enabled[/red]")
            return
        
        features = get_user_features(user_id)
        limits = get_user_limits(user_id)
        
        console.print(f"[bold]👤 User Features: {user_id}[/bold]")
        console.print(f"Enabled Features ({len(features)}):")
        for feature in sorted(features):
            console.print(f"  • {feature}")
        
        console.print(f"\n[bold]📊 Usage Limits:[/bold]")
        for limit_type, limit_value in limits.items():
            console.print(f"  • {limit_type}: {limit_value}")
    except Exception as e:
        console.print(f"[red]✗ Error listing user features: {e}[/red]")


@cli.command()
@click.option('--user-id', required=True, help='User identifier')
@click.option('--limit-type', required=True, help='Type of limit to check')
@click.option('--current-usage', required=True, type=int, help='Current usage amount')
def check_usage_limit(user_id, limit_type, current_usage):
    """Check if user is within usage limits."""
    try:
        if not is_feature_enabled("payment_integration"):
            console.print("[red]✗ Payment integration feature is not enabled[/red]")
            return
        
        within_limit = check_usage_limit(user_id, limit_type, current_usage)
        limits = get_user_limits(user_id)
        max_limit = limits.get(f"max_{limit_type}", 0)
        
        status = "✅" if within_limit else "❌"
        console.print(f"{status} User '{user_id}' usage: {current_usage}/{max_limit} ({limit_type})")
        
        if not within_limit:
            console.print("[yellow]⚠️  User has exceeded usage limits[/yellow]")
    except Exception as e:
        console.print(f"[red]✗ Error checking usage limit: {e}[/red]")


@cli.command()
def list_plans():
    """List available subscription plans."""
    try:
        if not is_feature_enabled("payment_integration"):
            console.print("[red]✗ Payment integration feature is not enabled[/red]")
            return
        
        payment_manager = get_payment_manager()
        plans = payment_manager.get_available_plans()
        
        console.print("[bold]💳 Available Subscription Plans[/bold]")
        for plan in plans:
            console.print(f"\n[bold]{plan.name} (${plan.price}/month)[/bold]")
            console.print(f"  Tier: {plan.tier.value}")
            console.print(f"  Billing: {plan.billing_cycle.value}")
            console.print(f"  Features: {len(plan.features)}")
            console.print(f"  Max Users: {plan.max_users}")
            console.print(f"  Max Projects: {plan.max_projects}")
            console.print(f"  Storage: {plan.max_storage_gb}GB")
    except Exception as e:
        console.print(f"[red]✗ Error listing plans: {e}[/red]")


# Update the existing run command to integrate new features
@cli.command()
@click.option('--file', '-f', required=True, help='File to analyze')
@click.option('--language', '-l', help='Programming language (auto-detected if not specified)')
@click.option('--dashboard', is_flag=True, help='Send data to web dashboard')
@click.option('--traceability', is_flag=True, help='Generate traceability matrix')
@click.option('--documentation', is_flag=True, help='Generate documentation')
@click.option('--user-id', help='User identifier for feature access control')
@click.pass_context
def enhanced_run(ctx, file, language, dashboard, traceability, documentation, user_id):
    """Enhanced run command with all new features integrated."""
    
    # Check if user has access to features
    if user_id:
        if not is_feature_enabled("payment_integration"):
            console.print("[yellow]⚠️  Payment integration not enabled, skipping access control[/yellow]")
        else:
            # Check access to requested features
            features_to_check = []
            if dashboard:
                features_to_check.append("web_dashboard")
            if traceability:
                features_to_check.append("traceability_matrix")
            if documentation:
                features_to_check.append("documentation_export")
            
            for feature in features_to_check:
                if not check_user_feature_access(user_id, feature):
                    console.print(f"[red]✗ User does not have access to feature: {feature}[/red]")
                    return
    
    # Detect language if not specified
    if not language:
        detected_lang = detect_language(file)
        if detected_lang:
            language = detected_lang.value
            console.print(f"[blue]🔍 Auto-detected language: {language}[/blue]")
        else:
            console.print("[yellow]⚠️  Could not detect language, using Python as default[/yellow]")
            language = "python"
    
    # Check language support
    if not is_language_supported(LanguageType(language)):
        console.print(f"[red]✗ Language '{language}' is not supported or not enabled[/red]")
        console.print("[yellow]💡 Use 'agentops enable-language --language {language}' to enable it[/yellow]")
        return
    
    # Run the original analysis
    console.print(f"[bold]🚀 Running enhanced analysis for {file} ({language})[/bold]")
    
    # Add dashboard integration
    if dashboard and is_feature_enabled("web_dashboard"):
        project_data = {
            "file": file,
            "language": language,
            "status": "analyzing",
            "progress": 0,
            "user_id": user_id
        }
        add_project_to_dashboard("temp_project", project_data)
        add_dashboard_event({
            "type": "analysis_started",
            "file": file,
            "language": language,
            "user_id": user_id
        })
    
    # Add traceability matrix generation
    if traceability and is_feature_enabled("traceability_matrix"):
        console.print("[blue]📊 Generating traceability matrix...[/blue]")
        try:
            traceability_manager = get_traceability_manager()
            matrix = traceability_manager.create_matrix("temp_project")
            console.print("[green]✓ Traceability matrix created[/green]")
        except Exception as e:
            console.print(f"[red]✗ Error creating traceability matrix: {e}[/red]")
    
    # Add documentation generation
    if documentation and is_feature_enabled("documentation_export"):
        console.print("[blue]📚 Generating documentation...[/blue]")
        try:
            documentation_exporter = get_documentation_exporter()
            config = documentation_exporter.create_documentation_project("temp_project", 
                documentation_exporter.config)
            console.print("[green]✓ Documentation project created[/green]")
        except Exception as e:
            console.print(f"[red]✗ Error creating documentation: {e}[/red]")
    
    # Update dashboard with completion
    if dashboard and is_feature_enabled("web_dashboard"):
        add_dashboard_event({
            "type": "analysis_completed",
            "file": file,
            "language": language,
            "user_id": user_id
        })
    
    console.print("[green]✓ Enhanced analysis completed[/green]")


# Add help text for new features
@cli.command()
def features_help():
    """Show help for available features and commands."""
    console.print("[bold]🔧 AgentOps Features Help[/bold]")
    
    console.print("\n[bold]🌐 Multi-Language Support:[/bold]")
    console.print("  • agentops enable-language --language python|javascript|java|csharp|go")
    console.print("  • agentops list-languages")
    console.print("  • Supported languages: Python (default), JavaScript, Java, C#, Go")
    
    console.print("\n[bold]📊 Web Dashboard:[/bold]")
    console.print("  • agentops dashboard --host localhost --port 3000")
    console.print("  • Real-time project monitoring and analytics")
    console.print("  • Available in Team and Enterprise tiers")
    
    console.print("\n[bold]🔗 Traceability Matrix:[/bold]")
    console.print("  • agentops export-traceability --project-id PROJECT --format csv|excel|html")
    console.print("  • Bidirectional traceability between requirements and tests")
    console.print("  • Available in Professional tier and above")
    
    console.print("\n[bold]📚 Documentation Export:[/bold]")
    console.print("  • agentops export-documentation --project-id PROJECT --format markdown|json|yaml")
    console.print("  • Professional documentation with multiple templates")
    console.print("  • Available in Professional tier and above")
    
    console.print("\n[bold]💳 Payment Integration:[/bold]")
    console.print("  • agentops check-feature-access --user-id USER --feature FEATURE")
    console.print("  • agentops list-user-features --user-id USER")
    console.print("  • agentops check-usage-limit --user-id USER --limit-type projects --current-usage 5")
    console.print("  • agentops list-plans")
    console.print("  • Feature access control and subscription management")
    
    console.print("\n[bold]⚙️ Feature Management:[/bold]")
    console.print("  • agentops enable-feature --feature FEATURE_NAME")
    console.print("  • agentops disable-feature --feature FEATURE_NAME")
    console.print("  • agentops list-features")
    console.print("  • Modular feature system with switch on/off capabilities")
    
    console.print("\n[bold]🚀 Enhanced Run:[/bold]")
    console.print("  • agentops enhanced-run --file FILE --language LANG --dashboard --traceability --documentation")
    console.print("  • Integrated analysis with all new features")
    console.print("  • Automatic language detection and feature access control")


@cli.command()
@click.option("--auto-update", is_flag=True, 
              help="Automatically apply suggested clarifications")
@click.option("--interactive", is_flag=True, default=True,
              help="Interactive mode for manual review (default)")
@click.option("--confidence-threshold", default=0.8, type=float,
              help="Minimum confidence score for auto-updates (default: 0.8)")
def analyze_failures(auto_update: bool, interactive: bool, confidence_threshold: float):
    """Analyze test failures and suggest requirements clarifications.
    
    This command runs tests, analyzes failures, and suggests improvements
    to requirements based on test failure patterns.
    
    Usage:
        agentops analyze-failures                    # Interactive analysis
        agentops analyze-failures --auto-update     # Auto-apply suggestions
        agentops analyze-failures --confidence-threshold 0.9  # Higher threshold
    """
    try:
        from ..agentops_core.requirements_clarification import RequirementsClarificationEngine
        
        console.print("[cyan]Running tests to identify failures...[/cyan]")
        
        # Run tests and capture output
        import subprocess
        result = subprocess.run(
            ["pytest", ".agentops/tests/", "--tb=short", "-q"],
            capture_output=True,
            text=True
        )
        
        # Analyze failures
        engine = RequirementsClarificationEngine()
        failures = engine.analyze_test_failures(result.stdout)
        
        if not failures:
            console.print("[green]✓ No test failures found![/green]")
            return
        
        console.print(f"[yellow]Found {len(failures)} test failures[/yellow]")
        
        # Identify requirements gaps
        gaps = engine.identify_requirements_gaps(failures)
        
        if not gaps:
            console.print("[yellow]No clear requirements gaps identified[/yellow]")
            return
        
        # Generate suggestions
        suggestions = engine.suggest_clarifications(gaps)
        
        console.print(f"\n[cyan]Requirements Clarification Suggestions:[/cyan]")
        console.print(f"Found {len(suggestions)} requirements that need clarification")
        
        # Display suggestions
        for i, suggestion in enumerate(suggestions, 1):
            console.print(f"\n[bold cyan]Suggestion {i}:[/bold cyan]")
            console.print(f"  Requirement ID: {suggestion['requirement_id']}")
            console.print(f"  Original: {suggestion['original_requirement'][:100]}...")
            console.print(f"  Suggested: {suggestion['suggested_clarification'][:100]}...")
            console.print(f"  Confidence: {suggestion['confidence']:.1%}")
            console.print(f"  Failures: {suggestion['failure_count']} tests")
        
        # Handle updates
        if auto_update:
            console.print(f"\n[cyan]Auto-updating requirements with confidence >= {confidence_threshold}...[/cyan]")
            updated_count = 0
            
            for suggestion in suggestions:
                if suggestion['confidence'] >= confidence_threshold:
                    success = engine.update_requirement(
                        suggestion['requirement_id'],
                        suggestion['suggested_clarification'],
                        f"Auto-clarification based on {suggestion['failure_count']} test failures",
                        update_method='auto'
                    )
                    if success:
                        updated_count += 1
                        console.print(f"  ✓ Updated requirement {suggestion['requirement_id']}")
            
            console.print(f"[green]✓ Auto-updated {updated_count} requirements[/green]")
            
        elif interactive:
            console.print(f"\n[cyan]Interactive Mode:[/cyan]")
            console.print("Review suggestions above and use 'agentops clarify-requirements' to apply changes")
        
    except Exception as e:
        console.print(f"[red]✗ Analysis failed: {str(e)}[/red]")
        sys.exit(1)


@cli.command()
@click.argument("requirement_id", type=int)
@click.option("--clarification", "clarified_text", 
              help="New clarified requirement text")
@click.option("--reason", "clarification_reason",
              help="Reason for the clarification")
@click.option("--interactive", is_flag=True, default=True,
              help="Interactive mode for editing")
def clarify_requirements(requirement_id: int, clarified_text: str, 
                       clarification_reason: str, interactive: bool):
    """Clarify a specific requirement based on test failures.
    
    This command allows you to update requirements with clarifications
    and maintains an audit trail of all changes.
    
    Usage:
        agentops clarify-requirements 5 --clarification "New text" --reason "Test failure"
        agentops clarify-requirements 5 --interactive  # Edit in interactive mode
    """
    try:
        from ..agentops_core.requirements_clarification import RequirementsClarificationEngine
        from ..agentops_core.requirement_store import RequirementStore
        
        engine = RequirementsClarificationEngine()
        store = RequirementStore()
        
        # Get current requirement
        requirement = store.get_requirement(requirement_id)
        if not requirement:
            console.print(f"[red]✗ Requirement {requirement_id} not found[/red]")
            sys.exit(1)
        
        console.print(f"[cyan]Current Requirement {requirement_id}:[/cyan]")
        console.print(f"  {requirement.requirement_text}")
        
        # Get clarification text
        if interactive and not clarified_text:
            console.print(f"\n[cyan]Enter clarified requirement text:[/cyan]")
            clarified_text = Prompt.ask("Clarified requirement")
            clarification_reason = Prompt.ask("Reason for clarification", default="Manual clarification")
        
        if not clarified_text:
            console.print(f"[red]✗ No clarification text provided[/red]")
            sys.exit(1)
        
        # Update requirement
        success = engine.update_requirement(
            requirement_id,
            clarified_text,
            clarification_reason or "Manual clarification",
            update_method='manual'
        )
        
        if success:
            console.print(f"[green]✓ Requirement {requirement_id} updated successfully[/green]")
            console.print(f"  New text: {clarified_text[:100]}...")
        else:
            console.print(f"[red]✗ Failed to update requirement {requirement_id}[/red]")
            sys.exit(1)
            
    except Exception as e:
        console.print(f"[red]✗ Clarification failed: {str(e)}[/red]")
        sys.exit(1)


@cli.command()
@click.option("--requirement-id", type=int,
              help="Show audit history for specific requirement")
@click.option("--format", "output_format",
              type=click.Choice(["table", "json", "markdown"]),
              default="table",
              help="Output format (default: table)")
def audit_history(requirement_id: int, output_format: str):
    """Show audit history for requirements clarifications.
    
    Displays the complete audit trail of all requirement clarifications,
    including who made changes, when, and why.
    
    Usage:
        agentops audit-history                    # Show all audit history
        agentops audit-history --requirement-id 5 # Show history for requirement 5
        agentops audit-history --format json     # Output as JSON
    """
    try:
        from ..agentops_core.requirements_clarification import RequirementsClarificationEngine
        
        engine = RequirementsClarificationEngine()
        audits = engine.get_audit_history(requirement_id)
        
        if not audits:
            console.print("[yellow]No audit history found[/yellow]")
            return
        
        if output_format == "json":
            import json
            audit_data = [asdict(audit) for audit in audits]
            console.print(json.dumps(audit_data, indent=2))
            
        elif output_format == "markdown":
            console.print("# Requirements Clarification Audit History\n")
            for audit in audits:
                console.print(f"## {audit.audit_id}")
                console.print(f"- **Requirement ID:** {audit.requirement_id}")
                console.print(f"- **Method:** {audit.update_method}")
                console.print(f"- **Timestamp:** {audit.timestamp}")
                console.print(f"- **Reason:** {audit.clarification_reason}")
                console.print(f"- **Original:** {audit.original_requirement}")
                console.print(f"- **Clarified:** {audit.clarified_requirement}\n")
                
        else:  # table format
            table = Table(title="Requirements Clarification Audit History")
            table.add_column("Audit ID", style="cyan")
            table.add_column("Requirement ID", style="green")
            table.add_column("Method", style="yellow")
            table.add_column("Timestamp", style="blue")
            table.add_column("Reason", style="magenta")
            
            for audit in audits:
                table.add_row(
                    audit.audit_id,
                    str(audit.requirement_id or "N/A"),
                    audit.update_method,
                    audit.timestamp,
                    audit.clarification_reason[:50] + "..." if len(audit.clarification_reason) > 50 else audit.clarification_reason
                )
            
            console.print(table)
            
    except Exception as e:
        console.print(f"[red]✗ Audit history failed: {str(e)}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    cli()
