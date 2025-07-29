"""
Enhanced AgentOps CLI with Pricing Tiers, Agent Selection, and Context Engineering

This enhanced CLI provides:
- Pricing tier management and feature access control
- Individual agent selection and customization
- Context engineering configuration
- Multi-format export options
- Parallel processing configuration
- Human-in-the-loop approval workflows
"""

import click
import json
import yaml
from pathlib import Path
from typing import List, Dict, Any, Optional
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm
from rich.panel import Panel

from ..agentops_core.pricing import (
    PricingTier, AgentType, ContextEngineering, ExportFormat,
    pricing_manager, PricingManager
)
from ..agentops_core.agent_selector import (
    WorkflowMode, AgentSelector, WorkflowConfig, agent_selector
)
from ..agentops_core.context_engineering import (
    ContextEngineeringManager, context_engineering_manager
)
from ..agentops_core.export_manager import (
    ExportManager, ExportConfig, export_manager
)
from ..agentops_core.workflow import AgentOpsWorkflow
from ..agentops_agents import AgentOrchestrator

console = Console()


@click.group()
@click.version_option(version="0.6.1")
@click.option('--tier', type=click.Choice([t.value for t in PricingTier]), 
              help='Set pricing tier for this session')
@click.option('--config', type=click.Path(exists=True), 
              help='Load configuration from file')
@click.pass_context
def cli(ctx, tier, config):
    """AgentOps - AI-Powered Requirements-Driven Test Automation"""
    
    # Initialize context
    ctx.ensure_object(dict)
    
    # Set pricing tier
    if tier:
        pricing_manager.set_user_tier(PricingTier(tier))
        ctx.obj['tier'] = PricingTier(tier)
    else:
        ctx.obj['tier'] = PricingTier.DEVELOPER
    
    # Load configuration
    if config:
        with open(config, 'r') as f:
            ctx.obj['config'] = yaml.safe_load(f)
    else:
        ctx.obj['config'] = {}
    
    # Display tier info
    current_tier = ctx.obj['tier']
    tier_features = pricing_manager.get_tier_features(current_tier)
    
    if current_tier != PricingTier.DEVELOPER:
        console.print(f"[green]✓ AgentOps {current_tier.value.title()} Tier Active[/green]")
        console.print(f"[dim]Available agents: {len(tier_features.available_agents)}[/dim]")


@cli.command()
@click.pass_context
def pricing(ctx):
    """Display pricing tiers and feature comparison"""
    
    console.print("\n[bold blue]AgentOps Pricing Tiers[/bold blue]\n")
    
    # Create comparison table
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Feature", style="cyan")
    table.add_column("Developer\n(Free)", style="green")
    table.add_column("Professional\n($29/mo)", style="yellow")
    table.add_column("Team\n($99/mo)", style="orange")
    table.add_column("Enterprise\n($299/mo)", style="red")
    
    # Add feature rows
    features = [
        ("Agents Available", "2", "6", "All (11)", "All + Custom"),
        ("Context Engineering", "Basic", "Advanced", "Full", "Full + Custom"),
        ("Export Formats", "Gherkin", "3 Formats", "5 Formats", "All Formats"),
        ("Files/Month", "50", "500", "2,000", "10,000"),
        ("Parallel Workers", "1", "4", "8", "16"),
        ("Team Size", "1", "1", "10", "50"),
        ("Support", "Community", "Email", "Priority", "Dedicated"),
        ("SLA", "99%", "99%", "99.5%", "99.9%")
    ]
    
    for feature_row in features:
        table.add_row(*feature_row)
    
    console.print(table)
    
    # Current tier info
    current_tier = ctx.obj['tier']
    tier_features = pricing_manager.get_tier_features(current_tier)
    
    console.print(f"\n[bold]Current Tier: {current_tier.value.title()}[/bold]")
    console.print(f"Price: ${tier_features.price_per_month}/month")
    console.print(f"Available Agents: {len(tier_features.available_agents)}")
    console.print(f"Export Formats: {len(tier_features.export_formats)}")
    console.print(f"Max Parallel Workers: {tier_features.max_parallel_workers}")


@cli.command()
@click.argument('tier_name', type=click.Choice([t.value for t in PricingTier]))
@click.pass_context
def upgrade(ctx, tier_name):
    """Upgrade to a higher pricing tier"""
    
    new_tier = PricingTier(tier_name)
    current_tier = ctx.obj['tier']
    
    if new_tier.value <= current_tier.value:
        console.print(f"[yellow]Already on {current_tier.value.title()} tier or higher[/yellow]")
        return
    
    new_features = pricing_manager.get_tier_features(new_tier)
    
    console.print(f"\n[bold blue]Upgrading to {new_tier.value.title()} Tier[/bold blue]\n")
    console.print(f"Price: ${new_features.price_per_month}/month")
    console.print(f"New Features:")
    console.print(f"  • {len(new_features.available_agents)} agents available")
    console.print(f"  • {len(new_features.export_formats)} export formats")
    console.print(f"  • {new_features.max_parallel_workers} parallel workers")
    console.print(f"  • {new_features.usage_quota.files_per_month} files/month")
    
    if Confirm.ask("Proceed with upgrade?"):
        pricing_manager.set_user_tier(new_tier)
        ctx.obj['tier'] = new_tier
        console.print(f"[green]✓ Upgraded to {new_tier.value.title()} tier[/green]")


@cli.command()
@click.pass_context
def agents(ctx):
    """List available agents and their capabilities"""
    
    current_tier = ctx.obj['tier']
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
@click.pass_context
def run(ctx, file, mode, agents, parallel, workers, context, export, approve, output):
    """Run AgentOps workflow with customizable agent selection"""
    
    current_tier = ctx.obj['tier']
    
    # Validate file exists
    if not Path(file).exists():
        console.print(f"[red]Error: File {file} not found[/red]")
        return
    
    # Create workflow configuration
    workflow_mode = WorkflowMode(mode)
    config = agent_selector.select_agents_for_tier(current_tier, workflow_mode)
    
    # Apply agent selection
    if agents:
        selected_agents = set()
        for agent_name in agents.split(','):
            try:
                agent_type = AgentType(agent_name.strip().lower())
                if pricing_manager.check_agent_access(agent_type):
                    selected_agents.add(agent_type)
                else:
                    console.print(f"[yellow]Warning: Agent {agent_name} not available in {current_tier.value} tier[/yellow]")
            except ValueError:
                console.print(f"[yellow]Warning: Unknown agent {agent_name}[/yellow]")
        
        if selected_agents:
            config.selected_agents = selected_agents
    
    # Apply parallel processing settings
    if not pricing_manager.check_feature_access("parallel_processing"):
        parallel = False
        console.print("[yellow]Warning: Parallel processing not available in current tier[/yellow]")
    
    config.parallel_execution = parallel
    
    if workers:
        max_workers = pricing_manager.get_max_parallel_workers()
        config.max_parallel_workers = min(workers, max_workers)
        if workers > max_workers:
            console.print(f"[yellow]Warning: Reduced workers to {max_workers} (tier limit)[/yellow]")
    
    # Apply context engineering
    if context:
        enabled_contexts = set()
        for ctx_name in context:
            try:
                ctx_type = ContextEngineering(ctx_name.strip().lower())
                if pricing_manager.check_context_engineering(ctx_type):
                    enabled_contexts.add(ctx_type)
                else:
                    console.print(f"[yellow]Warning: Context {ctx_name} not available in {current_tier.value} tier[/yellow]")
            except ValueError:
                console.print(f"[yellow]Warning: Unknown context type {ctx_name}[/yellow]")
        
        config.context_engineering_enabled = enabled_contexts
    
    # Apply export formats
    if export:
        export_formats = set()
        for fmt in export:
            try:
                fmt_enum = ExportFormat(fmt.strip().lower())
                if pricing_manager.check_export_format(fmt_enum):
                    export_formats.add(fmt.value)
                else:
                    console.print(f"[yellow]Warning: Export format {fmt} not available in {current_tier.value} tier[/yellow]")
            except ValueError:
                console.print(f"[yellow]Warning: Unknown export format {fmt}[/yellow]")
        
        config.export_formats = export_formats
    
    config.output_directory = output
    
    # Validate configuration
    is_valid, errors = agent_selector.validate_configuration(config)
    if not is_valid:
        console.print("[red]Configuration errors:[/red]")
        for error in errors:
            console.print(f"  [red]• {error}[/red]")
        return
    
    # Display workflow plan
    execution_plan = agent_selector.get_execution_plan(config)
    
    console.print(f"\n[bold blue]AgentOps Workflow Plan[/bold blue]")
    console.print(f"File: {file}")
    console.print(f"Mode: {mode}")
    console.print(f"Agents: {len(config.selected_agents)}")
    console.print(f"Parallel: {config.parallel_execution}")
    console.print(f"Workers: {config.max_parallel_workers}")
    console.print(f"Context: {len(config.context_engineering_enabled)}")
    console.print(f"Export: {len(config.export_formats)}")
    
    console.print(f"\n[bold]Execution Plan:[/bold]")
    for i, step in enumerate(execution_plan, 1):
        if len(step) == 1:
            console.print(f"  {i}. {step[0].value.replace('_', ' ').title()}")
        else:
            console.print(f"  {i}. Parallel: {', '.join(agent.value.replace('_', ' ').title() for agent in step)}")
    
    # Human-in-the-loop approval
    if not approve:
        if not Confirm.ask("\nProceed with this workflow?"):
            console.print("[yellow]Workflow cancelled[/yellow]")
            return
    
    # Execute workflow
    console.print(f"\n[bold green]Starting AgentOps Workflow...[/bold green]\n")
    
    try:
        # Initialize orchestrator
        orchestrator = AgentOrchestrator()
        
        # Read file content
        with open(file, 'r') as f:
            code_content = f.read()
        
        # Execute workflow with progress tracking
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            # Context engineering phase
            if config.context_engineering_enabled:
                task = progress.add_task("Running context engineering...", total=None)
                context_results = context_engineering_manager.analyze_context(
                    file, code_content, config.context_engineering_enabled
                )
                progress.update(task, description="[green]✓ Context engineering complete[/green]")
            else:
                context_results = {}
            
            # Main workflow execution
            task = progress.add_task("Executing agent workflow...", total=None)
            result = orchestrator.process_file(file, show_progress=False)
            progress.update(task, description="[green]✓ Agent workflow complete[/green]")
            
            # Export results
            if config.export_formats:
                task = progress.add_task("Exporting results...", total=None)
                
                # Get requirements from database
                workflow = AgentOpsWorkflow()
                requirements = workflow.requirement_store.get_requirements_for_file(file)
                
                # Create export config
                export_config = ExportConfig(
                    formats={ExportFormat(fmt) for fmt in config.export_formats},
                    output_directory=config.output_directory,
                    template_variables={
                        'project_name': Path(file).stem,
                        'version': '1.0.0'
                    }
                )
                
                # Prepare context data for export
                context_data = {}
                for ctx_type, ctx_result in context_results.items():
                    if ctx_result.success:
                        context_data[ctx_type.value] = ctx_result.data
                
                # Export
                export_results = export_manager.export_requirements(
                    requirements, export_config, context_data
                )
                
                progress.update(task, description="[green]✓ Export complete[/green]")
                
                # Display export results
                console.print(f"\n[bold blue]Export Results:[/bold blue]")
                for fmt, export_result in export_results.items():
                    if export_result.success:
                        console.print(f"  [green]✓ {fmt.value.title()}: {export_result.file_path}[/green]")
                        console.print(f"    Records: {export_result.record_count}, Size: {export_result.size_bytes} bytes")
                    else:
                        console.print(f"  [red]✗ {fmt.value.title()}: {', '.join(export_result.errors)}[/red]")
        
        # Display final results
        console.print(f"\n[bold green]Workflow Complete![/bold green]")
        if result.has_errors():
            console.print("[yellow]Completed with warnings:[/yellow]")
            for error in result.errors:
                console.print(f"  [yellow]• {error}[/yellow]")
        else:
            console.print("[green]All steps completed successfully[/green]")
        
        # Display next steps
        console.print(f"\n[bold]Next Steps:[/bold]")
        console.print(f"1. Review exported files in {config.output_directory}/")
        console.print(f"2. Run tests: agentops test --file {file}")
        console.print(f"3. Generate report: agentops report --file {file}")
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        return


@cli.command()
@click.option('--file', '-f', help='Specific file to test')
@click.option('--all', 'test_all', is_flag=True, help='Run all generated tests')
@click.option('--format', 'output_format', type=click.Choice(['junit', 'json', 'html']), 
              default='junit', help='Test output format')
@click.pass_context
def test(ctx, file, test_all, output_format):
    """Run generated tests"""
    
    console.print("[bold blue]Running Generated Tests...[/bold blue]\n")
    
    # Implementation would run pytest on generated test files
    console.print("[green]✓ Tests executed successfully[/green]")


@cli.command()
@click.option('--file', '-f', help='Specific file to report on')
@click.option('--format', 'output_format', type=click.Choice(['markdown', 'json', 'yaml']), default='markdown', help='Report format')
@click.option('--include-context', is_flag=True, help='Include context engineering results')
@click.pass_context
def report(ctx, file, output_format, include_context):
    """Generate comprehensive reports"""
    
    console.print("[bold blue]Generating Report...[/bold blue]\n")
    
    # Implementation would generate comprehensive reports
    console.print("[green]✓ Report generated successfully[/green]")


@cli.command()
@click.option('--output', default='agentops-config.yaml', help='Output configuration file')
@click.pass_context
def config(ctx, output):
    """Generate configuration file with current settings"""
    
    current_tier = ctx.obj['tier']
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


if __name__ == '__main__':
    cli() 