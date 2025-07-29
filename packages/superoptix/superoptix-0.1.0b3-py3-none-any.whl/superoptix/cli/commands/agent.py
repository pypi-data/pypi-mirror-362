#!/usr/bin/env python3
import copy
import importlib
import json
import os
import subprocess
import sys
import textwrap
import time
import warnings
from pathlib import Path

import yaml
from rich.console import Console
from rich.panel import Panel
from rich.table import Table


# Helper class to prevent YAML aliases
class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True

# Suppress SQLite resource warnings that are harmless in our use case
# These warnings occur due to Python's garbage collection timing with DSPy evaluation metrics
warnings.filterwarnings("ignore", message="unclosed database", category=ResourceWarning)

from superoptix.cli.utils import run_async
from superoptix.compiler.agent_compiler import AgentCompiler
from superoptix.models.tier_system import TierLevel, tier_system
from superoptix.observability.tracer import SuperOptixTracer
from superoptix.runners.dspy_runner import DSPyRunner
from superoptix.ui.designer_factory import DesignerFactory
from superoptix.validators.playbook_linter import PlaybookLinter, display_lint_results

console = Console()


def compile_agent(args):
    """Handle agent compilation."""
    if not args.name and not args.all:
        console.print(
            "[bold red]❌ You must specify an agent name or use --all.[/bold red]"
        )
        return

    try:
        project_root = Path.cwd()
        super_file = project_root / ".super"
        if not super_file.exists():
            console.print(
                "\n[bold red]❌ Not a valid super project. Run 'super init <project_name>' to get started.[/bold red]"
            )
            return

        with open(super_file) as f:
            config = yaml.safe_load(f)
            project_name = config.get("project")

        agents_dir = project_root / project_name / "agents"
        if not agents_dir.exists():
            console.print(
                f"\n[bold red]❌ Agents directory not found for project '{project_name}'.[/]"
            )
            return

        if args.all:
            playbook_files = sorted(list(agents_dir.rglob("*_playbook.yaml")))
            if not playbook_files:
                console.print(
                    f"\n[yellow]No agent playbooks found in '{agents_dir}'.[/yellow]"
                )
                return

            console.print(
                f"\n[bold blue]🚀 Compiling all {len(playbook_files)} agents in project '{project_name}'...[/]"
            )
            successful_compilations = []
            failed_compilations = []

            for playbook_path in playbook_files:
                agent_name = playbook_path.stem.replace("_playbook", "")
                tier_level = getattr(args, 'tier', None)
                if _compile_single_agent(agent_name, args, tier_level):
                    successful_compilations.append(agent_name)
                else:
                    failed_compilations.append(agent_name)

            console.print("=" * 80)

            # Create summary panel
            if successful_compilations and not failed_compilations:
                console.print(
                    Panel(
                        f"🎉 [bold bright_green]ALL AGENTS COMPILED SUCCESSFULLY![/]\n\n"
                        f"✅ [bold]Successful:[/] {len(successful_compilations)} agent(s)\n"
                        f"🚀 [bold]Ready for testing and customization![/]",
                        title="📊 Compilation Summary",
                        border_style="bright_green",
                        padding=(1, 2),
                    )
                )
            else:
                summary_text = ""
                if successful_compilations:
                    summary_text += f"✅ [bold green]Success:[/] {len(successful_compilations)} agent(s) compiled successfully\n"
                if failed_compilations:
                    summary_text += f"❌ [bold red]Failed:[/] {len(failed_compilations)} agent(s) failed: {', '.join(failed_compilations)}"

                border_color = "red" if failed_compilations else "green"
                console.print(
                    Panel(
                        summary_text,
                        title="📊 Compilation Summary",
                        border_style=border_color,
                        padding=(1, 2),
                    )
                )

                if failed_compilations:
                    sys.exit(1)

        else:  # Compile single agent
            agent_name = args.name.lower()
            # Pass tier level if specified
            tier_level = getattr(args, 'tier', None)
            if not _compile_single_agent(agent_name, args, tier_level):
                sys.exit(1)

    except Exception as e:
        console.print(
            f"\n[bold red]❌ An unexpected error occurred during compilation:[/] {e}"
        )
        sys.exit(1)


def _compile_single_agent(agent_name: str, args, tier_level: str = None):
    """Helper to compile a single agent with enhanced visual feedback and tier awareness."""
    console.print("=" * 80)
    try:
        compile_args = copy.copy(args)
        compile_args.name = agent_name

        # Load playbook data for display
        project_root = Path.cwd()
        with open(project_root / ".super") as f:
            system_name = yaml.safe_load(f).get("project")

        # Find playbook file
        playbook_path = next(
            (project_root / system_name / "agents").rglob(
                f"**/{agent_name}_playbook.yaml"
            ),
            None,
        )
        if not playbook_path:
            package_root = Path(__file__).parent.parent.parent
            playbook_path = next(
                package_root.rglob(f"**/agents/**/{agent_name}_playbook.yaml"), None
            )

        playbook_data = None
        if playbook_path:
            with open(playbook_path) as f:
                playbook_data = yaml.safe_load(f)

        # Get metadata for display
        metadata = playbook_data.get("metadata", {}) if playbook_data else {}
        spec = playbook_data.get("spec", {}) if playbook_data else {}

        console.print(
            f"\n🔨 [bold bright_cyan]Compiling agent '[bold yellow]{agent_name}[/]'...[/]"
        )

        compiler = AgentCompiler()
        pipeline_path = compiler._get_pipeline_path(agent_name)

        # Show what's happening (concise)
        console.print(
            Panel(
                f"🤖 [bold bright_green]COMPILATION IN PROGRESS[/]\n\n"
                f"🎯 [bold]Agent:[/] {metadata.get('name', agent_name.title())}\n"
                f"🏗️ [bold]Framework:[/] DSPy (default) {tier_level.title() if tier_level else 'Junior'} Pipeline — other frameworks coming soon\n"
                f"🔧 [bold]Process:[/] YAML playbook → Executable Python pipeline\n"
                f"📁 [bold]Output:[/] [cyan]{pipeline_path.relative_to(project_root)}[/]",
                title="⚡ Compilation Details",
                border_style="bright_green",
                padding=(1, 2),
            )
        )

        # Determine tier level from various sources
        effective_tier = tier_level
        if not effective_tier and playbook_data:
            effective_tier = playbook_data.get("metadata", {}).get("level", "oracles")

        # Compile the agent (mixin by default, or abstracted if flag provided)
        use_abstracted = getattr(args, 'abstracted', False)

        compiler.compile(compile_args, tier_level=effective_tier, use_abstracted=use_abstracted)

        # Show success
        console.print(
            Panel(
                "🎉 [bold bright_green]COMPILATION SUCCESSFUL![/] Pipeline Generated",
                style="bright_green",
                border_style="bright_green",
            )
        )

        # Show verbose panels only in verbose mode
        if getattr(args, 'verbose', False):
            # Auto-generation notice (verbose only)
            important_notice = """⚠️ [bold bright_yellow]Auto-Generated Pipeline[/]

🚨 [bold]Starting foundation[/] - Customize for production use
💡 [bold]You own this code[/] - Modify for your specific requirements"""

            console.print(
                Panel(
                    important_notice,
                    title="🛠️ Customization Required",
                    border_style="bright_yellow",
                    padding=(1, 2),
                )
            )

            # Testing guidance (verbose only)
            test_count = 0
            if (
                playbook_data
                and "feature_specifications" in spec
                and "scenarios" in spec["feature_specifications"]
            ):
                test_count = len(spec["feature_specifications"]["scenarios"])

            tests_guidance = f"""🧪 [bold]Current BDD Scenarios:[/] {test_count} found

🎯 [bold]Recommendations:[/]
• Add comprehensive test scenarios to your playbook
• Include edge cases and error handling scenarios
• Test with real-world data samples

💡 [bold]Why scenarios matter:[/] Training data for optimization & quality gates"""

            console.print(
                Panel(
                    tests_guidance,
                    title="🧪 Testing Enhancement",
                    border_style="bright_magenta",
                    padding=(1, 2),
                )
            )

            # Next steps guidance (verbose only)
            next_steps = f"""🚀 [bold bright_cyan]NEXT STEPS[/]

[cyan]super agent evaluate {agent_name}[/] - Establish baseline performance
[cyan]super agent optimize {agent_name}[/] - Enhance performance using DSPy
[cyan]super agent evaluate {agent_name}[/] - Measure improvement
[cyan]super agent run {agent_name} --goal "goal"[/] - Execute optimized agent

[dim]💡 Follow BDD/TDD workflow: evaluate → optimize → evaluate → run[/]"""

            console.print(
                Panel(
                    next_steps,
                    title="🎯 Workflow Guide",
                    border_style="bright_cyan",
                    padding=(1, 2),
                )
            )

        # Simple workflow guide (normal mode)
        console.print(f"🎯 [bold cyan]Next:[/] [cyan]super agent evaluate {agent_name}[/] or [cyan]super agent run {agent_name} --goal \"your goal\"[/]")

        # Success summary
        console.print("=" * 80)
        console.print(
            f"🎉 [bold bright_green]Agent '{metadata.get('name', agent_name)}' pipeline ready![/] Time to make it yours! 🚀"
        )

        return True

    except Exception as e:
        console.print(
            Panel(
                f"❌ [bold red]COMPILATION FAILED[/]\n\n"
                f"[red]Error:[/] {str(e)}\n"
                f"[yellow]Agent:[/] {agent_name}\n"
                f"[yellow]Framework:[/] DSPy (default — other frameworks coming soon)\n\n"
                f"[cyan]💡 Troubleshooting Tips:[/]\n"
                f"• Ensure agent playbook exists and is valid YAML\n"
                f"• Check that you're in a valid super project directory\n"
                f"• Verify playbook syntax with: [cyan]super agent lint {agent_name}[/]",
                title="💥 Compilation Error",
                border_style="red",
                padding=(1, 2),
            )
        )
        return False


def run_agent(args):
    """Handle running an agent pipeline by delegating to the DSPyRunner."""
    tracer = SuperOptixTracer(agent_id=args.name)
    try:
        with tracer.trace_operation(
            "agent_run", f"agent.{args.name}", agent_name=args.name, query=args.goal
        ):
            console.print(f"🚀 [bold cyan]Running agent '[yellow]{args.name}[/]'...[/]")
            console.print()

            # Check if agent has been optimized and tested
            project_root = Path.cwd()
            with open(project_root / ".super") as f:
                project_name = yaml.safe_load(f).get("project")

            agent_dir = project_root / project_name / "agents" / args.name
            optimized_path = agent_dir / "pipelines" / f"{args.name}_optimized.json"

            if not optimized_path.exists():
                console.print("[yellow]💡 For best performance, consider this workflow:[/]")
                console.print(f"   1. [cyan]super agent evaluate {args.name}[/] - Establish baseline performance")
                console.print(f"   2. [cyan]super agent optimize {args.name}[/] - Enhance performance")
                console.print(f"   3. [cyan]super agent evaluate {args.name}[/] - Measure improvement")
                console.print(f"   4. [cyan]super agent run {args.name} --goal 'goal'[/] - Execute optimized agent")
                console.print()
                console.print("[dim]Running with base model (not optimized)...[/]")
                console.print()

            # Handle optimization flag
            if hasattr(args, 'optimize') and args.optimize:
                console.print("[yellow]🚀 Running with optimization enabled (this may take longer)...[/]")
                # First optimize the agent
                optimization_result = run_async(
                    DSPyRunner(agent_name=args.name).optimize(force=False)
                )
                if not optimization_result.get("success", False):
                    console.print(f"[red]❌ Optimization failed: {optimization_result.get('error', 'Unknown error')}[/]")
                    console.print("[yellow]Continuing with base model...[/]")

            # Correctly instantiate the runner first, then run it.
            runner = DSPyRunner(agent_name=args.name)
            # Check if runtime optimization is requested
            runtime_optimize = (hasattr(args, 'optimize') and args.optimize) or (hasattr(args, 'force_optimize') and args.force_optimize)
            force_runtime = hasattr(args, 'force_optimize') and args.force_optimize
            # Use optimization unless explicitly disabled
            use_optimization = True  # Always try to use pre-optimized if available
            run_async(runner.run(query=args.goal, use_optimization=use_optimization, runtime_optimize=runtime_optimize, force_runtime=force_runtime))
            
            # Add next steps guidance after successful run - only in verbose mode
            if getattr(args, 'verbose', False):
                console.print()
                console.print("🎉 [bold green]Agent execution completed successfully![/]")
                console.print()
                
                # Next steps guidance in a panel
                next_steps_content = "🔧 [bold yellow]Improve your agent:[/]\n"
                next_steps_content += f"   [cyan]super agent evaluate {args.name}[/] - Test agent performance with BDD specs\n"
                next_steps_content += f"   [cyan]super agent optimize {args.name}[/] - Optimize for better results\n\n"
                
                next_steps_content += "🎯 [bold green]Create more agents:[/]\n"
                next_steps_content += "   [cyan]super agent add[/] - Add a new agent to your project\n"
                next_steps_content += "   [cyan]super agent design[/] - Design a custom agent with AI assistance\n"
                next_steps_content += "   [cyan]super agent pull <agent_name>[/] - Install a pre-built agent\n\n"
                
                next_steps_content += "🎼 [bold magenta]Build orchestras (multi-agent workflows):[/]\n"
                next_steps_content += "   [cyan]super orchestra create <orchestra_name>[/] - Create a new orchestra\n"
                next_steps_content += "   [cyan]super orchestra list[/] - See existing orchestras\n"
                next_steps_content += "   [cyan]super orchestra run <orchestra_name> --goal \"complex task\"[/] - Run multi-agent workflow\n\n"
                
                next_steps_content += "📊 [bold blue]Explore and manage:[/]\n"
                next_steps_content += "   [cyan]super agent list[/] - See all your agents\n"
                next_steps_content += f"   [cyan]super agent inspect {args.name}[/] - Detailed agent information\n"
                next_steps_content += "   [cyan]super marketplace[/] - Browse available agents and tools\n\n"
                
                next_steps_content += "💡 [dim]Quick tips:[/]\n"
                next_steps_content += "   • Use [cyan]--optimize[/] flag for runtime optimization\n"
                next_steps_content += "   • Add BDD specifications to your playbook for better testing\n"
                next_steps_content += "   • Create orchestras for complex, multi-step workflows"
                
                console.print(Panel(
                    next_steps_content,
                    title="🚀 What would you like to do next?",
                    border_style="bright_cyan",
                    padding=(1, 2)
                ))
                console.print()
    except Exception as e:
        # The runner already prints detailed errors, so we just note that the run failed.
        console.print("\n[bold red]❌ Agent run failed.[/]")
        console.print(f"[red]Debug: {type(e).__name__}: {e}")
        import traceback
        console.print(traceback.format_exc())
        tracer.add_event(
            "agent_run_failed", f"agent.{args.name}", {"error": str(e)}, status="error"
        )
        # Optionally, re-raise if you want the script to exit with a non-zero code
        # raise e
    finally:
        tracer.export_traces()


def test_agent_bdd(args):
    """Handles BDD specification testing of an agent with professional test runner UI."""
    agent_name = args.name.lower()
    project_name = getattr(args, 'project', None)

    # Professional test runner header
    console.print()
    console.print("═" * 100, style="bright_cyan")
    console.print("🧪 [bold bright_cyan]SuperOptiX BDD Spec Runner[/] [dim]- Professional Agent Validation[/]", justify="center")
    console.print("═" * 100, style="bright_cyan")
    console.print()

    # Test session info
    session_info = Table.grid(padding=(0, 2))
    session_info.add_column(style="cyan", min_width=20)
    session_info.add_column(style="white")
    session_info.add_row("🎯 Agent:", f"[bold]{agent_name}[/]")
    session_info.add_row("📅 Session:", f"{time.strftime('%Y-%m-%d %H:%M:%S')}")
    session_info.add_row("🔧 Mode:", f"{'Auto-tune enabled' if args.auto_tune else 'Standard validation'}")
    session_info.add_row("📊 Verbosity:", f"{'Detailed' if args.verbose else 'Summary'}")

    console.print(Panel(session_info, title="📋 Spec Execution Session", border_style="blue"))
    console.print()

    try:
        # Step 1: Pipeline Loading (no spinner)
        console.print("[cyan]Loading pipeline definition...[/]")
        runner = DSPyRunner(agent_name, project_name=project_name)

        spec = importlib.util.spec_from_file_location(
            f"{agent_name}_pipeline", runner.pipeline_path
        )
        if not spec:
            console.print("❌ [bold red]Pipeline Not Found[/]")
            console.print(f"   Expected: {runner.pipeline_path}")
            console.print(f"   💡 Run: [cyan]super agent compile {agent_name}[/]")
            return

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        pipeline_class = None
        for name, obj in module.__dict__.items():
            if name.endswith("Pipeline") and isinstance(obj, type):
                pipeline_class = obj
                break

        if not pipeline_class:
            console.print("❌ [bold red]Pipeline Class Not Found[/]")
            console.print(f"   Expected: Class ending with 'Pipeline' in {runner.pipeline_path}")
            return

        pipeline = pipeline_class()
        console.print("[green]Pipeline loaded successfully[/]")

        # Step 2: Optimization Check (no spinner)
        optimization_status = "🚀 Optimized" if runner.optimized_path.exists() else "⚙️  Base Model"
        if runner.optimized_path.exists():
            console.print("[cyan]Loading optimized weights...[/]")
            try:
                pipeline.load_optimized(str(runner.optimized_path))
                console.print("✅ [green]Optimized weights applied[/]")
            except Exception as e:
                console.print(f"⚠️  [yellow]Using base model - optimization load failed: {e}[/]")
                optimization_status = "⚙️  Base Model (optimization failed)"
        else:
            console.print("ℹ️  [blue]Using base model (no optimization found)[/]")

        # Step 3: BDD Spec Execution with Professional UI
        console.print()
        console.print("🔍 [bold cyan]Discovering BDD Specifications...[/]")

        # Get test scenarios count first
        test_scenarios = getattr(pipeline, 'test_examples', [])
        if not test_scenarios:
            console.print("❌ [bold red]No BDD specifications found![/]")
            console.print()
            console.print("📝 [bold yellow]How to add BDD specifications:[/]")
            console.print("   1. Edit your agent playbook YAML file")
            console.print("   2. Add 'feature_specifications' section with 'scenarios'")
            console.print("   3. Recompile agent: [cyan]super agent compile {agent_name}[/]")
            console.print()
            console.print("💡 [dim]Example specification structure:[/]")
            console.print("""[dim]
feature_specifications:
  scenarios:
    - name: "basic_functionality"
      description: "Agent should handle basic requests"
      input:
        feature_requirement: "Simple task"
      expected_output:
        implementation: "Expected response"[/]""")
            return

        console.print(f"📋 Found [bold green]{len(test_scenarios)}[/] BDD specifications")
        console.print()

        # Professional spec execution with progress tracking
        console.print("🧪 [bold cyan]Executing BDD Specification Suite[/]")
        console.print("─" * 60)

        # Pytest-style progress indicator
        console.print("[dim]Progress:[/]", end=" ")
        
        # Run specs with real-time updates
        results = pipeline.run_bdd_test_suite(
            auto_tune=args.auto_tune,
            ignore_checks=args.ignore_checks
        )

        if not results or not results.get("success"):
            console.print(f"❌ [bold red]Spec execution failed:[/] {results.get('message', 'Unknown error')}")
            return

        # Extract results for professional display
        summary = results.get("summary", {})
        model_analysis = results.get("model_analysis", {})
        recommendations = results.get("recommendations", [])
        bdd_results = results.get("bdd_results", {})
        detailed_results = bdd_results.get("detailed_results", [])

        # Display pytest-style results
        console.print()  # Clear the progress line
        console.print("[bold]Test Results:[/]")
        
        # Show pytest-style output
        for i, result in enumerate(detailed_results, 1):
            if result.get("passed"):
                console.print("[green].[/]", end="")
            else:
                console.print("[red]F[/]", end="")
        
        console.print()  # New line after progress
        console.print()

        # Show detailed table only in verbose mode
        if getattr(args, 'verbose', False):
            # Create progress table with better formatting
            spec_table = Table(show_header=True, header_style="bold magenta")
            spec_table.add_column("Specification", style="cyan", width=28, no_wrap=False)
            spec_table.add_column("Status", justify="center", width=12)
            spec_table.add_column("Score", justify="center", width=8)
            spec_table.add_column("Description", style="dim", width=45, no_wrap=False)

            # Populate spec results table
            for result in detailed_results:
                status_icon = "✅ PASS" if result.get("passed") else "❌ FAIL"
                status_color = "green" if result.get("passed") else "red"
                score = f"{result.get('confidence_score', 0.0):.2f}"

                # Better text handling for long descriptions
                description = result.get('description', 'N/A')
                if len(description) > 42:
                    description = description[:39] + "..."

                spec_name = result.get('scenario_name', 'Unknown')
                if len(spec_name) > 25:
                    spec_name = spec_name[:22] + "..."

                spec_table.add_row(
                    spec_name,
                    f"[{status_color}]{status_icon}[/]",
                    f"[bold]{score}[/]",
                    description
                )

            console.print(spec_table)
            console.print()

        # Professional Summary Dashboard
        total_specs = summary.get("total", len(detailed_results))
        passed_specs = summary.get("passed", 0)
        failed_specs = summary.get("failed", 0)
        pass_rate = (passed_specs / total_specs * 100) if total_specs > 0 else 0

        # Quality gate determination
        if pass_rate >= 80:
            quality_gate = "🎉 EXCELLENT"
            gate_color = "bright_green"
            gate_emoji = "🟢"
        elif pass_rate >= 60:
            quality_gate = "⚠️  GOOD"
            gate_color = "yellow"
            gate_emoji = "🟡"
        else:
            quality_gate = "❌ NEEDS WORK"
            gate_color = "red"
            gate_emoji = "🔴"

        # Main results dashboard
        summary_grid = Table.grid(padding=(0, 2))
        summary_grid.add_column(style="bold cyan", min_width=20)
        summary_grid.add_column(style="white", min_width=15)
        summary_grid.add_column(style="bold cyan", min_width=20)
        summary_grid.add_column(style="white")

        summary_grid.add_row("📊 Total Specs:", f"[bold]{total_specs}[/]", "🎯 Pass Rate:", f"[bold]{pass_rate:.1f}%[/]")
        summary_grid.add_row("✅ Passed:", f"[green]{passed_specs}[/]", "🤖 Model:", f"{model_analysis.get('model_name', 'Unknown')}")
        summary_grid.add_row("❌ Failed:", f"[red]{failed_specs}[/]", "💪 Capability:", f"{model_analysis.get('capability_score', 0.0):.2f}")
        summary_grid.add_row("🏆 Quality Gate:", f"[{gate_color}]{quality_gate}[/]", "🚀 Status:", optimization_status)

        console.print(Panel(
            summary_grid,
            title=f"{gate_emoji} Specification Results Summary",
            border_style=gate_color,
            padding=(1, 2)
        ))

        # Grouped failure analysis (if any failures) - only in verbose mode
        if failed_specs > 0 and getattr(args, 'verbose', False):
            console.print()
            console.print("🔍 [bold red]Failure Analysis - Grouped by Issue Type[/]")
            console.print("─" * 80)

            # Group failures by issue type
            failure_groups = {}
            for result in detailed_results:
                if not result.get("passed"):
                    issue = result.get('failure_reason', 'Unknown issue').lower()
                    
                    # Categorize issues
                    if "semantic" in issue:
                        category = "semantic"
                    elif "keyword" in issue:
                        category = "keyword"
                    elif "structure" in issue:
                        category = "structure"
                    elif "length" in issue:
                        category = "length"
                    else:
                        category = "general"
                    
                    if category not in failure_groups:
                        failure_groups[category] = []
                    failure_groups[category].append(result)

            # Generate fix suggestions for each category
            fix_suggestions_map = {
                "semantic": [
                    "🎯 Make the response more relevant to the expected output",
                    "📝 Use similar terminology and technical concepts",
                    "🔍 Ensure the output addresses all aspects of the input requirement",
                    "💡 Review the expected output format and structure"
                ],
                "keyword": [
                    "🔑 Include more specific technical terms from the expected output",
                    "📚 Use domain-specific vocabulary and concepts",
                    "🎯 Focus on the key terms that define the requirement",
                    "💼 Add industry-standard terminology where appropriate"
                ],
                "structure": [
                    "📋 Match the expected output format and organization",
                    "🔲 Use similar formatting (lists, headers, code blocks)",
                    "📏 Maintain consistent structure and presentation",
                    "🎨 Pay attention to layout and information hierarchy"
                ],
                "length": [
                    "📝 Provide more comprehensive and detailed responses",
                    "🔍 Ensure all aspects of the requirement are covered",
                    "💬 Expand explanations and include more context",
                    "📖 Add examples and implementation details"
                ],
                "general": [
                    "🔍 Review the specification expectations vs actual output",
                    "📝 Improve overall response quality and relevance",
                    "🎯 Focus on addressing the core requirement",
                    "💡 Consider model optimization or prompt refinement"
                ]
            }

            # Display grouped failures
            for category, failures in failure_groups.items():
                category_names = {
                    "semantic": "Semantic Relevance Issues",
                    "keyword": "Keyword/Terminology Issues", 
                    "structure": "Structure/Format Issues",
                    "length": "Length/Completeness Issues",
                    "general": "General Quality Issues"
                }
                
                console.print(f"\n[bold red]📋 {category_names.get(category, category.title())} ({len(failures)} failures)[/]")
                console.print("─" * 60)
                
                # Show fix suggestions for this category
                suggestions = fix_suggestions_map.get(category, [])
                console.print("[bold yellow]💡 Fix Suggestions:[/]")
                for suggestion in suggestions:
                    console.print(f"   {suggestion}")
                
                # List the failing specs in this category
                console.print("\n[bold cyan]Affected Specifications:[/]")
                for failure in failures:
                    spec_name = failure.get('scenario_name', 'Unknown')
                    score = failure.get('confidence_score', 0.0)
                    console.print(f"   • [red]{spec_name}[/] (score: {score:.3f})")
                
                console.print()

        # AI-Powered Recommendations
        if recommendations:
            console.print()
            rec_panel = Panel(
                "\n".join([f"💡 {rec}" for rec in recommendations]),
                title="🎯 AI Recommendations",
                border_style="bright_blue",
                padding=(1, 2)
            )
            console.print(rec_panel)

        # Detailed scenario results (verbose mode)
        if args.verbose and detailed_results:
            console.print()
            console.print("📝 [bold cyan]Detailed Specification Results[/]")
            console.print("═" * 80)

            for i, result in enumerate(detailed_results, 1):
                status = "✅ PASSED" if result.get("passed") else "❌ FAILED"
                status_color = "green" if result.get("passed") else "red"

                # Create detailed result panel
                details_content = f"""
[bold]Specification:[/] {result.get('scenario_name', 'Unknown')}
[bold]Description:[/] {result.get('description', 'N/A')}
[bold]Confidence Score:[/] {result.get('confidence_score', 0.0):.3f}
[bold]Semantic Similarity:[/] {result.get('semantic_similarity', 0.0):.3f}
"""

                if not result.get("passed"):
                    details_content += f"[bold]Failure Reason:[/] {result.get('failure_reason', 'Unknown')}\n"

                    # Add fix guidance
                    details_content += "\n[bold yellow]💡 Fix Guidance:[/]\n"
                    if result.get('confidence_score', 0) < 0.6:
                        details_content += "• Review and improve the response quality\n"
                        details_content += "• Ensure the output addresses all aspects of the input\n"
                    if result.get('semantic_similarity', 0) < 0.5:
                        details_content += "• Make the response more relevant to the expected output\n"
                        details_content += "• Use similar terminology and concepts\n"

                console.print(Panel(
                    details_content.strip(),
                    title=f"[{status_color}]Spec #{i}: {status}[/]",
                    border_style=status_color,
                    padding=(1, 2)
                ))

        # Enhanced Next Steps - Only in verbose mode
        if getattr(args, 'verbose', False):
            console.print()
            next_steps_content = ""

            if failed_specs == 0:
                next_steps_content = f"""🎉 [bold green]All specifications passed! Your agent is ready.[/]

[bold cyan]Recommended next steps:[/]
• [cyan]super agent run {agent_name} --goal "your goal"[/] - Execute your agent
• [cyan]super agent run {agent_name} --goal "Create a Python function"[/] - Try a real goal
• [cyan]super agent optimize {agent_name}[/] - Further tune performance for production
• [cyan]super agent evaluate {agent_name}[/] - Re-evaluate after optimization
• Add more comprehensive test scenarios for edge cases"""
            else:
                next_steps_content = f"""🔧 [bold yellow]{failed_specs} specification(s) need attention.[/]

[bold cyan]Recommended actions for better quality:[/]
• Review the grouped failure analysis above
• [cyan]super agent optimize {agent_name}[/] - Optimize agent performance
• [cyan]super agent evaluate {agent_name}[/] - Re-evaluate to measure improvement
• Use [cyan]--verbose[/] flag for detailed failure analysis

[bold green]You can still test your agent:[/]
• [cyan]super agent run {agent_name} --goal "your goal"[/] - Works even with failing specs
• [cyan]super agent run {agent_name} --goal "Create a simple function"[/] - Try basic goals
• [dim]💡 Agents can often perform well despite specification failures[/]

[bold cyan]For production use:[/]
• Aim for ≥80% pass rate before deploying to production
• Run optimization and re-evaluation cycles until quality gates pass"""

            console.print(Panel(
                next_steps_content,
                title="🎯 Next Steps",
                border_style="bright_cyan",
                padding=(1, 2)
            ))

        # Simple workflow guide (normal mode)
        console.print(f"🎯 [bold cyan]Next:[/] [cyan]super agent run {agent_name} --goal \"your goal\"[/]")

        # Professional footer
        console.print()
        console.print("═" * 100, style="bright_cyan")
        console.print(f"🏁 [bold bright_cyan]Specification execution completed[/] [dim]- {pass_rate:.1f}% pass rate ({passed_specs}/{total_specs} specs)[/]", justify="center")
        console.print("═" * 100, style="bright_cyan")
        console.print()

        # Explicit user guidance in a panel - only in verbose mode
        if getattr(args, 'verbose', False):
            console.print()
            
            guidance_content = ""
            if failed_specs > 0:
                guidance_content += "🔧 [bold yellow]To improve your agent's performance:[/]\n"
                guidance_content += f"   [cyan]super agent optimize {agent_name}[/] - Optimize the pipeline for better results\n\n"
            
            guidance_content += "🚀 [bold green]To run your agent:[/]\n"
            guidance_content += f"   [cyan]super agent run {agent_name} --goal \"your specific goal here\"[/]\n\n"
            
            guidance_content += "💡 [dim]Example goals:[/]\n"
            guidance_content += f"   • [cyan]super agent run {agent_name} --goal \"Create a Python function to calculate fibonacci numbers\"[/]\n"
            guidance_content += f"   • [cyan]super agent run {agent_name} --goal \"Write a React component for a todo list\"[/]\n"
            guidance_content += f"   • [cyan]super agent run {agent_name} --goal \"Design a database schema for an e-commerce site\"[/]"
            
            console.print(Panel(
                guidance_content,
                title="🎯 What would you like to do next?",
                border_style="bright_cyan",
                padding=(1, 2)
            ))
            console.print()

    except FileNotFoundError:
        console.print(f"❌ [bold red]Agent '{agent_name}' not found.[/]")
        console.print("💡 Available agents: [cyan]super agent list[/]")
    except Exception as e:
        console.print(f"❌ [bold red]Specification execution failed:[/] {e}")
        console.print(f"🔧 [dim]Try: super agent compile {agent_name} && super agent evaluate {agent_name}[/]")


def lint_agent(args):
    """Handle agent playbook linting."""
    if not args.name and not args.all:
        console.print(
            "[bold red]❌ You must specify an agent name or use --all.[/bold red]"
        )
        return

    try:
        project_root = Path.cwd()
        super_file = project_root / ".super"

        if not super_file.exists():
            console.print(
                "\n[bold red]❌ Not a valid super project. Run 'super init <project_name>' to get started.[/bold red]"
            )
            return

        with open(super_file) as f:
            config = yaml.safe_load(f)
            project_name = config.get("project")

                    # Use new SuperSpec structure: agents/ directory at project root
        agents_dir = project_root / "agents"

        if not agents_dir.exists():
            console.print(
                f"\n[bold red]❌ Agents directory not found for project '{project_name}'.[/]"
                f"\n[dim]Expected at: {agents_dir}[/]\n"
                f"[yellow]💡 Tip: Create agents using 'super spec generate'[/]"
            )
            return

        if args.all:
            playbook_files = sorted(list(agents_dir.rglob("*_playbook.yaml")))
            if not playbook_files:
                console.print(
                    f"\n[yellow]No agent playbooks found in '{agents_dir}'.[/yellow]"
                )
                return

            console.print(
                f"\n[bold blue]🔍 Linting all {len(playbook_files)} agents in project '{project_name}'...[/]"
            )
            total_errors = 0
            failed_agents = []

            for playbook_path in playbook_files:
                errors = _lint_playbook(playbook_path)
                if errors:
                    total_errors += len(errors)
                    failed_agents.append(playbook_path.stem.replace("_playbook", ""))

            console.print("=" * 60)
            if total_errors > 0:
                console.print(
                    f"\n[bold red]❌ Linting finished with a total of {total_errors} errors in {len(failed_agents)} agent(s).[/]"
                )
                console.print(
                    f"[bold yellow]Failed agents:[/] {', '.join(failed_agents)}"
                )
                sys.exit(1)
            else:
                console.print(
                    f"\n[bold green]✅ All {len(playbook_files)} agent playbooks passed linting successfully![/]"
                )

        else:
            agent_name = args.name.lower()
            playbook_pattern = f"**/{agent_name}_playbook.yaml"
            matching_playbooks = list(agents_dir.rglob(playbook_pattern))

            if not matching_playbooks:
                console.print(
                    f"\n[bold red]❌ Agent '{agent_name}' not found in project '{project_name}'.[/]"
                )
                sys.exit(1)

            playbook_path = matching_playbooks[0]

            if len(matching_playbooks) > 1:
                console.print(
                    f"[bold yellow]Warning: Found multiple playbooks for '{agent_name}'. Using the first one: {playbook_path}[/]"
                )

            errors = _lint_playbook(playbook_path)

            if errors:
                sys.exit(1)

    except Exception as e:
        console.print(
            f"\n[bold red]❌ An unexpected error occurred during linting:[/] {e}"
        )
        sys.exit(1)


def _lint_playbook(playbook_path: Path):
    """Helper to lint a single playbook file and display results."""
    console.print("=" * 60)
    console.print(f"Linting: [cyan]{playbook_path.relative_to(Path.cwd())}[/]")

    linter = PlaybookLinter(playbook_path)
    errors = linter.lint()

    display_lint_results(playbook_path, linter.playbook, errors)

    if errors:
        console.print(f"[bold red]❌ Found {len(errors)} errors.[/]")
    else:
        console.print("[bold green]✅ No issues found.[/]")

    return errors


def design_agent(args):
    """Handle agent design command through Streamlit UI."""
    try:
        # Ensure Streamlit config directory exists to bypass onboarding
        streamlit_config_dir = Path.home() / ".streamlit"
        streamlit_config_dir.mkdir(exist_ok=True)

        # Create config.toml to disable usage stats gathering
        config_path = streamlit_config_dir / "config.toml"
        if not config_path.exists():
            config_content = textwrap.dedent("""
                [browser]
                gatherUsageStats = false
            """)
            config_path.write_text(config_content)
            console.print("[dim]Created Streamlit config to disable usage stats.[/dim]")

        # Create credentials.toml to bypass the email prompt
        credentials_path = streamlit_config_dir / "credentials.toml"
        if not credentials_path.exists():
            credentials_content = textwrap.dedent("""
                [general]
                email = ""
            """)
            credentials_path.write_text(credentials_content)
            console.print(
                "[dim]Created Streamlit credentials to bypass email prompt.[/dim]"
            )

        # Get UI path using DesignerFactory
        designer_factory = DesignerFactory()
        designer_path = designer_factory.get_designer(args.tier)

        panel_content = (
            f"🚀 [bold cyan]super Agent Designer[/]\n\n"
            f"[yellow]Agent:[/] {args.agent.upper()}\n"
            f"[yellow]Tier:[/] {args.tier.capitalize()}\n"
            f"└── [yellow]UI:[/] [link=http://localhost:8501]http://localhost:8501[/link]\n\n"
            f"[dim]Starting designer... Use Ctrl+C to stop when done.[/]"
        )

        console.print(
            Panel(panel_content, title="🎨 Agent Design Studio", border_style="blue")
        )

        env = os.environ.copy()
        env.update({"SUPER_AGENT_NAME": args.agent, "SUPER_AGENT_LEVEL": args.tier})

        cmd = [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            str(designer_path),
            "--server.port=8501",
            "--server.headless=true",  # Run headless to avoid auto-opening browser
            "--",
            args.agent,
            args.tier,
        ]

        process = subprocess.Popen(
            cmd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )

        console.print("[cyan]Waiting for designer UI to launch...[/]")

        app_ready = False
        start_time = time.time()
        startup_timeout = 30  # seconds

        while time.time() - start_time < startup_timeout:
            if process.poll() is not None:
                _, stderr = process.communicate()
                console.print("[bold red]❌ Designer failed to start![/]")
                console.print(
                    Panel(stderr, title="[red]Error Details[/red]", border_style="red")
                )
                sys.exit(1)

            try:
                # Health check to see if the server is up
                import requests

                response = requests.get("http://localhost:8501", timeout=1)
                if response.status_code == 200:
                    app_ready = True
                    break
            except (
                requests.exceptions.ConnectionError,
                requests.exceptions.ReadTimeout,
            ):
                time.sleep(1)  # Wait and retry
            except ImportError:
                console.print(
                    "[yellow]Warning: 'requests' library not found. Using a less reliable health check.[/yellow]"
                )
                # Basic fallback without requests
                import urllib.request

                try:
                    with urllib.request.urlopen(
                        "http://localhost:8501", timeout=1
                    ) as response:
                        if response.getcode() == 200:
                            app_ready = True
                            break
                except Exception:
                    time.sleep(1)

        if app_ready:
            console.print("[bold green]✅ Designer UI is ready![/]")
            console.print(
                "🌐 Visit: [link=http://localhost:8501]http://localhost:8501[/link]"
            )
        else:
            console.print("[bold yellow]⚠️ Designer is taking a long time to start.[/]")
            console.print(
                "It's running in the background. Please try visiting [link=http://localhost:8501]http://localhost:8501[/link] manually."
            )

        try:
            console.print(
                "\n[dim]Designer is running. Press Ctrl+C here to stop the server.[/]"
            )
            process.wait()
            console.print("\n[green]✅ Designer session ended.[/]")
        except KeyboardInterrupt:
            console.print("\n[yellow]🛑 Stopping designer...[/]")
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
            console.print("[green]✅ Designer stopped.[/]")

    except Exception as e:
        console.print(f"\n[bold red]❌ Error launching designer:[/] {e}")
        import traceback

        console.print(f"[red]{traceback.format_exc()}[/]")
        if "process" in locals() and process.poll() is None:
            process.kill()
        sys.exit(1)


def add_agent(args):
    """Handle agent add command with enhanced visual feedback and tier support."""
    try:
        agent_name = args.name.lower()
        tier_level = getattr(args, 'tier', None)
        project_root = Path.cwd()

        # Read system name from .super
        with open(project_root / ".super") as f:
            system_name = yaml.safe_load(f).get("project")

        # Get the correct path to agents directory
        package_root = Path(__file__).parent.parent.parent

        # Simplified playbook search
        source_playbook = next(package_root.rglob(f"**/agents/**/{agent_name}_playbook.yaml"), None)

        if not source_playbook:
            console.print(f"\n[bold red]❌ Agent '{agent_name}' not found.[/]")
            console.print("\n[yellow]💡 Need help finding the right agent?[/yellow]")
            console.print(
                "[cyan]🔍 Browse all available pre-built agents with:[/] super agent list --pre-built"
            )
            console.print(
                "[cyan]🏢 Filter by industry:[/] super agent list --pre-built --industry <industry_name>"
            )
            sys.exit(1)

        target_playbook_dir = project_root / system_name / "agents" / agent_name / "playbook"
        target_playbook_dir.mkdir(parents=True, exist_ok=True)
        target_playbook_path = target_playbook_dir / f"{agent_name}_playbook.yaml"

        # Load playbook to get metadata for rich display
        with open(source_playbook) as f:
            playbook_data = yaml.safe_load(f)

        # Apply tier-specific enhancements to the playbook
        if tier_level == 'genies':
            console.print(f"[cyan]🚀 Enhancing agent '{agent_name}' for Genies tier...[/]")

            # Update metadata
            playbook_data['metadata']['level'] = 'genies'

            spec = playbook_data.get('spec', {})

            # Update model for Genies tier (keeping same model for simplicity)
            spec['language_model'] = {
                'provider': 'ollama',
                'model': 'llama3.1:8b',
                'temperature': 0.1,
                'max_tokens': 2000,
                'api_base': 'http://localhost:11434'
            }
            console.print("[green]  ✅ Model configured for Genies tier: llama3.1:8b[/]")

            # Set task type to react
            if 'tasks' in spec and spec['tasks']:
                for task in spec['tasks']:
                    task['type'] = 'react'

            # Add ReAct configuration
            spec['react_config'] = {
                'max_iters': 5
            }
            console.print("[green]  ✅ ReAct configuration added[/]")

            # Add tools configuration
            spec['tools'] = {
                'builtin_tools': [
                    {'name': 'calculator'},
                    {'name': 'text_analyzer'},
                    {'name': 'file_reader'}
                ]
            }
            console.print("[green]  ✅ Default toolset added (calculator, text_analyzer, file_reader)[/]")

            # Add memory configuration
            spec['memory'] = {
                'enabled': True,
                'types': ['short_term', 'episodic']
            }
            console.print("[green]  ✅ Memory system configured[/]")

            # Ensure agentflow is removed as it's not used in this ReAct setup
            if 'agentflow' in spec:
                del spec['agentflow']

            console.print("[green]  ✅ Preserving optimization and testing sections[/]")

        # Create target directory and write the file
        with open(target_playbook_path, "w") as f:
            yaml.dump(playbook_data, f, Dumper=NoAliasDumper, default_flow_style=False, sort_keys=False)

        # Show success with consistent UI style
        console.print("=" * 80)
        console.print(f"\n🤖 [bold bright_cyan]Adding agent '[bold yellow]{agent_name}[/]'...[/]")

        console.print(
            Panel(
                "🎉 [bold bright_green]AGENT ADDED SUCCESSFULLY![/] Pre-built Agent Ready",
                style="bright_green",
                border_style="bright_green",
            )
        )

        # Agent information panel (concise)
        display_tier = (tier_level or playbook_data.get("metadata", {}).get("level", "oracles")).title()
        tier_emoji = "🧞" if display_tier == 'Genies' else "🔮"
        agent_info = f"""🤖 [bold]Name:[/] {playbook_data.get("metadata", {}).get("name", "Unknown")}
🏢 [bold]Industry:[/] {playbook_data.get("metadata", {}).get("namespace", "general").title()} | {tier_emoji} [bold]Tier:[/] {display_tier}
🔧 [bold]Tasks:[/] {len(playbook_data.get("spec", {}).get("tasks", []))} | 📁 [bold]Location:[/] [cyan]{target_playbook_path.relative_to(project_root)}[/]"""

        if display_tier == 'Genies':
            agent_info += "\n🚀 [bold]Features:[/] ReAct Agents + Tools + Memory"

        console.print(
            Panel(
                agent_info,
                title="📋 Agent Details",
                border_style="bright_cyan",
                padding=(1, 2),
            )
        )

        # Customization guidance panel (concise)
        customization_info = """✨ [bold bright_magenta]Pre-built Agent - Ready to Customize![/]

📝 [bold]Modify:[/] persona, tasks, inputs/outputs, model settings"""

        console.print(
            Panel(
                customization_info,
                title="🛠️ Customization Options",
                border_style="bright_magenta",
                padding=(1, 2),
            )
        )

        # Next steps panel (concise)
        next_steps = f"""🚀 [bold bright_cyan]NEXT STEPS[/]

[cyan]super agent compile {agent_name}[/] - Generate executable pipeline
[cyan]super agent run {agent_name} --goal "goal"[/] - Execute agent

[dim]💡 Comprehensive guide: [cyan]super docs[/] | 🔍 More agents: [cyan]super market[/][/]"""

        console.print(
            Panel(
                next_steps,
                title="🎯 Workflow Guide",
                border_style="bright_cyan",
                padding=(1, 2),
            )
        )

        console.print("=" * 80)
        console.print(
            f"🎉 [bold bright_green]Agent '{playbook_data.get('metadata', {}).get('name', agent_name)}' ready for customization and deployment![/] 🚀"
        )

    except FileNotFoundError as e:
        console.print(f"\n[bold red]❌ Project file not found:[/] {e}")
        console.print(
            "[yellow]💡 Make sure you're in a valid super project directory.[/]"
        )
        console.print("[cyan]Run 'super init <project_name>' to create a new project.[/]")
        sys.exit(1)
    except yaml.YAMLError as e:
        console.print(f"\n[bold red]❌ Error parsing agent playbook:[/] {e}")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[bold red]❌ Failed to add agent:[/] {e}")
        sys.exit(1)


def list_agents(args):
    """List agents based on the provided arguments."""
    if hasattr(args, "pre_built") and args.pre_built:
        list_pre_built_agents(args)
    else:
        list_project_agents(args)


def list_project_agents(args):
    """List agents in the current super project."""
    try:
        project_root = Path.cwd()
        super_file = project_root / ".super"

        if not super_file.exists():
            console.print(
                "\n[bold red]❌ Not a valid super project. Run 'super init <project_name>' to get started.[/bold red]"
            )
            console.print(
                "[cyan]💡 Quick start: super init my_project && cd my_project[/cyan]"
            )
            return

        with open(super_file) as f:
            config = yaml.safe_load(f)
            project_name = config.get("project")

        agents_dir = project_root / project_name / "agents"

        if not agents_dir.exists() or not any(agents_dir.iterdir()):
            console.print(f"\n[bold blue]📋 Project Agents - {project_name}[/bold blue]")
            console.print("[yellow]No agents found in your project yet.[/yellow]")
            console.print("\n[cyan]🚀 Get started with pre-built agents:[/cyan]")
            console.print("   [bold]super agent list --pre-built[/bold]           - Browse all available agents")
            console.print("   [bold]super agent list --pre-built --industry tech[/bold] - Filter by industry")
            console.print("   [bold]super agent pull developer[/bold]                - Add a specific agent")
            console.print("\n[cyan]💡 Or create your own:[/cyan]")
            console.print("   [bold]super agent design[/bold]                      - Interactive agent designer")
            return

        playbook_files = list(agents_dir.rglob("*_playbook.yaml"))
        if not playbook_files:
            console.print(f"\n[bold blue]📋 Project Agents - {project_name}[/bold blue]")
            console.print("[yellow]No agent playbooks found in your project.[/yellow]")
            console.print("\n[cyan]🔧 This might happen if:[/cyan]")
            console.print("   • Agents were added but playbooks are missing")
            console.print("   • Playbooks don't follow the *_playbook.yaml naming convention")
            console.print("\n[cyan]💡 Quick fixes:[/cyan]")
            console.print("   [bold]super agent pull <agent_name>[/bold]    - Add a pre-built agent")
            console.print("   [bold]super agent list --pre-built[/bold]   - See available agents")
            return

        agents = []
        for playbook_file in playbook_files:
            try:
                with open(playbook_file, "r") as f:
                    playbook = yaml.safe_load(f)
                if playbook and "metadata" in playbook:
                    metadata = playbook["metadata"]
                    playbook_ref = playbook_file.stem.replace("_playbook", "")

                    # Check compilation status
                    agent_dir = playbook_file.parent.parent
                    pipeline_dir = agent_dir / "pipelines"
                    compiled_pipeline = pipeline_dir / f"{playbook_ref}_pipeline.py"
                    optimized_pipeline = pipeline_dir / f"{playbook_ref}_optimized.json"

                    # Determine status
                    if optimized_pipeline.exists():
                        status = "🚀 Optimized"
                        status_color = "bright_green"
                    elif compiled_pipeline.exists():
                        status = "⚡ Compiled"
                        status_color = "yellow"
                    else:
                        status = "📋 Playbook"
                        status_color = "blue"

                    # Check for recent traces
                    trace_path = project_root / ".superoptix" / "traces" / f"{playbook_ref}.jsonl"
                    last_run = "Never"
                    if trace_path.exists():
                        try:
                            import datetime
                            import os
                            mtime = os.path.getmtime(trace_path)
                            last_run = datetime.datetime.fromtimestamp(mtime).strftime("%m-%d %H:%M")
                        except:
                            last_run = "Unknown"

                    agents.append(
                        {
                            "name": metadata.get("name", "Unknown"),
                            "id": metadata.get("id", "No ID"),
                            "type": metadata.get("agent_type", "Unknown"),
                            "level": metadata.get("level", "oracles"),
                            "ref": playbook_ref,
                            "status": status,
                            "status_color": status_color,
                            "last_run": last_run,
                        }
                    )
            except yaml.YAMLError as e:
                console.print(
                    f"[yellow]Warning: Could not parse {playbook_file.name}: {e}[/]"
                )
            except Exception as e:
                console.print(
                    f"[yellow]Warning: Could not process {playbook_file.name}: {e}[/]"
                )

        agents.sort(key=lambda x: x["name"])

        table = Table(
            title=f"📋 Project Agents: {project_name}", border_style="green"
        )
        table.add_column("Name", style="yellow")
        table.add_column("Agent ID", style="magenta")
        table.add_column("Status", style="white")
        table.add_column("Level", style="green")
        table.add_column("Last Run", style="cyan")
        table.add_column("Playbook Ref", style="bold blue")

        for agent in agents:
            status_styled = f"[{agent['status_color']}]{agent['status']}[/]"
            table.add_row(
                agent["name"],
                agent["id"],
                status_styled,
                agent["level"],
                agent["last_run"],
                agent["ref"]
            )
        console.print(table)

        # Show helpful next steps
        console.print("\n[cyan]💡 Quick Actions:[/cyan]")
        console.print("   [bold]super agent ps[/bold] or [bold]super agent list[/bold]     - Refresh this list")
        console.print("   [bold]super agent compile <name>[/bold]         - Compile an agent")
        console.print("   [bold]super agent optimize <name>[/bold]        - Optimize performance")
        console.print("   [bold]super agent run <name> -i \"task\"[/bold]   - Execute an agent")
        console.print("   [bold]super agent inspect <name>[/bold]         - View agent details")

    except FileNotFoundError:
        console.print(
            f"\n[bold red]❌ Project directory for '{project_name}' not found.[/bold red]"
        )
    except Exception as e:
        console.print(f"\n[bold red]❌ Failed to list project agents:[/] {e}")
        sys.exit(1)


def list_pre_built_agents(args):
    """List all available pre-built agents, optionally filtered by industry."""
    try:
        package_root = Path(__file__).parent.parent.parent
        agents_dir = package_root / "agents"

        if not agents_dir.exists():
            console.print(
                f"\n[bold red]❌ Agents directory not found at:[/] {agents_dir}"
            )
            return

        available_industries = sorted(
            [d.name for d in agents_dir.iterdir() if d.is_dir()]
        )

        # Show industry filter info if filtering
        industry_filter = None
        if hasattr(args, "industry") and args.industry:
            industry_filter = args.industry.lower()
            industry_dir = agents_dir / industry_filter
            if not industry_dir.exists():
                console.print(f"\n[bold red]❌ Industry '{args.industry}' not found.[/]")
                console.print("\n[cyan]📊 Available Industries:[/cyan]")
                table = Table(show_header=False, box=None)
                num_columns = 3
                rows = [
                    available_industries[i : i + num_columns]
                    for i in range(0, len(available_industries), num_columns)
                ]
                for row in rows:
                    table.add_row(*[f"• [blue]{item.replace('_', ' ').title()}[/blue]" for item in row])
                console.print(table)
                console.print("\n[cyan]💡 Try:[/cyan] [bold]super agent list --pre-built --industry <industry_name>[/bold]")
                return
        else:
            console.print(f"\n[cyan]📊 Available Industries ([magenta]{len(available_industries)}[/magenta]):[/cyan]")
            table = Table(show_header=False, box=None)
            num_columns = 3
            rows = [
                available_industries[i : i + num_columns]
                for i in range(0, len(available_industries), num_columns)
            ]
            for row in rows:
                table.add_row(*[f"• [blue]{item.replace('_', ' ').title()}[/blue]" for item in row])
            console.print(table)
            console.print()

        if industry_filter:
            playbook_files = list((agents_dir / industry_filter).rglob("*_playbook.yaml"))
        else:
            playbook_files = list(agents_dir.rglob("*_playbook.yaml"))

        if not playbook_files:
            console.print("\n[yellow]No agents found for the specified criteria.[/]")
            return

        agents = []
        for playbook_file in playbook_files:
            try:
                with open(playbook_file, "r") as f:
                    playbook = yaml.safe_load(f)
                if playbook and "metadata" in playbook:
                    metadata = playbook["metadata"]
                    industry = metadata.get("namespace", "Unknown")
                    if industry_filter and industry.lower() != industry_filter:
                        continue

                    playbook_ref = playbook_file.stem.replace("_playbook", "")
                    agents.append(
                        {
                            "name": metadata.get("name", "Unknown"),
                            "id": metadata.get("id", "No ID"),
                            "type": metadata.get("agent_type", "Unknown"),
                            "level": metadata.get("level", "oracles"),
                            "ref": playbook_ref,
                            "industry": industry,
                        }
                    )
            except yaml.YAMLError as e:
                console.print(
                    f"[yellow]Warning: Could not parse {playbook_file.name}: {e}[/]"
                )
            except Exception as e:
                console.print(
                    f"[yellow]Warning: Could not process {playbook_file.name}: {e}[/]"
                )

        agents.sort(key=lambda x: (x["industry"], x["name"]))

        title = "📋 Available Pre-built Agents"
        if industry_filter:
            title += f" in '{industry_filter.capitalize()}'"

        table = Table(title=title, border_style="blue")
        table.add_column("Industry", style="cyan", no_wrap=True)
        table.add_column("Name", style="yellow")
        table.add_column("ID", style="magenta")
        table.add_column("Level", style="green")
        table.add_column("Type", style="white")
        table.add_column("Playbook Ref", style="bold blue")

        for agent in agents:
            table.add_row(
                agent["industry"].capitalize(),
                agent["name"],
                agent["id"],
                agent["level"],
                agent["type"],
                agent["ref"],
            )

        console.print(table)

        # Show count and helpful instructions
        agent_count = len(agents)
        console.print(f"\n[bright_green]✅ Found {agent_count} pre-built agent(s)[/bright_green]")

        console.print("\n[cyan]🚀 Next Steps:[/cyan]")
        console.print("   [bold]super agent pull <playbook_ref>[/bold]           - Add an agent to your project")
        if not industry_filter:
            console.print("   [bold]super agent list --pre-built --industry <name>[/bold] - Filter by industry")
        else:
            console.print("   [bold]super agent list --pre-built[/bold]                  - Show all industries")
        console.print("   [bold]super agent design[/bold]                        - Create a custom agent")

        if agent_count > 0:
            # Show example with first agent
            example_ref = agents[0]["ref"]
            console.print(f"\n[cyan]💡 Example:[/cyan] [bold]super agent pull {example_ref}[/bold]")

    except Exception as e:
        console.print(f"\n[bold red]❌ Failed to list pre-built agents:[/] {e}")
        sys.exit(1)


def show_tier_status(args):
    """Show current tier status and available features."""
    # Get user tier from config or default to ORACLES
    user_tier = getattr(args, "tier", None)
    if user_tier is None:
        user_tier = TierLevel.ORACLES
    elif isinstance(user_tier, str):
        user_tier = TierLevel(user_tier.lower())

    console.print("\n[bold blue]🎯 Current Tier Status[/bold blue]")

    # Show current tier
    tier_panel = Panel(
        f"[bold green]{user_tier.value.title()}[/bold green]",
        title="Your Active Tier",
        border_style="green",
    )
    console.print(tier_panel)

    # Show available features
    console.print(
        f"\n[bold cyan]✅ Features Available in {user_tier.value.title()} Tier[/bold cyan]"
    )
    accessible_features = tier_system.get_accessible_features(user_tier)

    available_table = Table()
    available_table.add_column("Feature", style="green")
    available_table.add_column("Description", style="white")
    available_table.add_column("Status", style="blue")

    for feature in accessible_features:
        status = "Beta" if feature.beta else "Available"
        if feature.enterprise_only:
            status += " (Enterprise)"

        available_table.add_row(
            feature.name,
            feature.description[:60] + "..."
            if len(feature.description) > 60
            else feature.description,
            status,
        )

    console.print(available_table)

    # Show upgrade options
    next_tier_features = []
    for tier_level in TierLevel:
        if (
            tier_system.tier_hierarchy[tier_level]
            > tier_system.tier_hierarchy[user_tier]
        ):
            tier_features = [
                f for f in tier_system.features.values() if f.min_tier == tier_level
            ]
            if tier_features:
                next_tier_features.extend(
                    tier_features[:3]
                )  # Show first 3 features from next tier
                break

    if next_tier_features:
        console.print("\n[bold yellow]🚀 Upgrade to unlock more features[/bold yellow]")

        upgrade_table = Table(title="Next Tier Features")
        upgrade_table.add_column("Feature", style="yellow")
        upgrade_table.add_column("Description", style="white")
        upgrade_table.add_column("Required Tier", style="red")

        for feature in next_tier_features:
            upgrade_table.add_row(
                feature.name,
                feature.description[:50] + "..."
                if len(feature.description) > 50
                else feature.description,
                feature.min_tier.value.title(),
            )

        console.print(upgrade_table)

        # Show upgrade info
        upgrade_info = Panel(
            """
[bold]🔓 Ready to upgrade?[/bold]

• Visit: https://super-agentic.ai/upgrade
• Email: upgrade@super-agentic.ai
• Schedule a demo: https://calendly.com/shashikant-super-agentic/30min

[dim]Get access to advanced DSPy capabilities, priority support, and early access to beta features.[/dim]
            """,
            title="Upgrade Information",
            border_style="yellow",
        )
        console.print(upgrade_info)


def optimize_agent(args):
    """Handle agent optimization."""
    console.print("=" * 80)
    console.print(f"\n🚀 [bold bright_cyan]Optimizing agent '[bold yellow]{args.name}[/]'...[/]")

    try:
        project_root = Path.cwd()
        super_file = project_root / ".super"
        if not super_file.exists():
            console.print(
                "\n[bold red]❌ Not a valid super project. Run 'super init <project_name>' to get started.[/bold red]"
            )
            return

        with open(super_file) as f:
            config = yaml.safe_load(f)
            project_name = config.get("project")

        agent_name = args.name.lower()
        agent_dir = project_root / project_name / "agents" / agent_name
        pipeline_path = agent_dir / "pipelines" / f"{agent_name}_pipeline.py"
        optimized_path = agent_dir / "pipelines" / f"{agent_name}_optimized.json"

        if not pipeline_path.exists():
            console.print(
                f"\n[bold red]❌ Pipeline not found for agent '{agent_name}'. Run 'super agent compile {agent_name}' first.[/bold red]"
            )
            return

        # Load and run optimization
        runner = DSPyRunner(agent_name=agent_name)

        # Show what's happening (concise)
        console.print(
            Panel(
                f"🤖 [bold bright_green]OPTIMIZATION IN PROGRESS[/]\n\n"
                f"🎯 [bold]Agent:[/] {agent_name.title()}\n"
                f"🔧 [bold]Strategy:[/] DSPy BootstrapFewShot\n"
                f"📊 [bold]Data Source:[/] BDD scenarios from playbook\n"
                f"💾 [bold]Output:[/] [cyan]{optimized_path.relative_to(project_root)}[/]",
                title="⚡ Optimization Details",
                border_style="bright_green",
                padding=(1, 2),
            )
        )

        # Perform optimization
        strategy = getattr(args, 'strategy', 'bootstrap')
        force = getattr(args, 'force', False)
        optimization_result = run_async(runner.optimize(strategy=strategy, force=force))

        if optimization_result.get("success", False):
            console.print(
                Panel(
                    "🎉 [bold bright_green]OPTIMIZATION SUCCESSFUL![/] Agent Enhanced",
                    style="bright_green",
                    border_style="bright_green",
                )
            )

            # Performance metrics (concise)
            training_examples = optimization_result.get('training_examples', 'N/A')
            score = optimization_result.get('score', 'N/A')

            optimization_info = f"""📈 [bold]Performance Improvement:[/]
• Training Examples: {training_examples}
• Optimization Score: {score}

💡 [bold]What changed:[/] DSPy optimized prompts and reasoning chains
🚀 [bold]Ready for testing:[/] Enhanced agent performance validated"""

            console.print(
                Panel(
                    optimization_info,
                    title="📊 Optimization Results",
                    border_style="bright_cyan",
                    padding=(1, 2),
                )
            )

            # Show verbose panels only in verbose mode
            if getattr(args, 'verbose', False):
                # Auto-tuning notice (verbose only)
                auto_tune_info = """🧠 [bold]Smart Optimization:[/] DSPy BootstrapFewShot

⚡ [bold]Automatic improvements:[/] Better prompts, reasoning chains
🎯 [bold]Quality assurance:[/] Test before production use"""

                console.print(
                    Panel(
                        auto_tune_info,
                        title="🤖 AI Enhancement",
                        border_style="bright_magenta",
                        padding=(1, 2),
                    )
                )

                # Next steps guidance (verbose only)
                next_steps = f"""🚀 [bold bright_cyan]NEXT STEPS[/]

[cyan]super agent evaluate {agent_name}[/] - Measure optimization improvement
[cyan]super agent run {agent_name} --goal "goal"[/] - Execute enhanced agent
[cyan]super orchestra create[/] - Ready for multi-agent orchestration

[dim]💡 Follow BDD/TDD workflow: evaluate → optimize → evaluate → run[/]"""

                console.print(
                    Panel(
                        next_steps,
                        title="🎯 Workflow Guide",
                        border_style="bright_cyan",
                        padding=(1, 2),
                    )
                )

            # Simple workflow guide (normal mode)
            console.print(f"🎯 [bold cyan]Next:[/] [cyan]super agent evaluate {agent_name}[/] or [cyan]super agent run {agent_name} --goal \"your goal\"[/]")

            # Success summary
            console.print("=" * 80)
            console.print(
                f"🎉 [bold bright_green]Agent '{agent_name}' optimization complete![/] Ready for testing! 🚀"
            )
        else:
            error_msg = optimization_result.get("error", "Unknown error")

            # Create a more helpful error panel
            error_panel_content = (
                f"❌ [bold red]OPTIMIZATION FAILED[/]\n\n"
                f"[bold]Agent:[/] {agent_name}\n"
                f"[bold]Strategy:[/] {strategy}\n\n"
                f"[bold red]Error Details:[/] \n{error_msg}\n\n"
                f"--- \n"
                f"💡 [bold bright_cyan]Troubleshooting Tips[/]\n"
                f"1. [bold]Check BDD Scenarios:[/]\n"
                f"   - Ensure your playbook has valid `feature_specifications` with `scenarios`.\n"
                f"   - Each scenario needs an `input` and an `expected_output`.\n"
                f"   - Run [cyan]super agent lint {agent_name}[/] to check syntax.\n\n"
                f"2. [bold]Verify Model Connection:[/]\n"
                f"   - Make sure your local Ollama server is running and accessible.\n"
                f"   - Check the `api_base` URL in your agent's playbook.\n\n"
                f"3. [bold]Inspect Pipeline Code:[/]\n"
                f"   - The auto-generated pipeline might need customization.\n"
                f"   - Look for issues in: [dim]{pipeline_path}[/]\n\n"
                f"4. [bold]Run with Verbose Output:[/]\n"
                f"   - Re-run the command with `--verbose` for more detailed logs."
            )

            console.print(
                Panel(
                    error_panel_content,
                    title="💥 Optimization Error",
                    border_style="red",
                    padding=(1, 2),
                )
            )

    except Exception as e:
        console.print(f"\n[bold red]❌ An unexpected error occurred during optimization: {e}[/bold red]")


def remove_agent(args):
    """Handle agent removal."""
    if not args.name:
        console.print("[bold red]❌ You must specify an agent name to remove.[/bold red]")
        return

    agent_name = args.name.lower()

    try:
        project_root = Path.cwd()
        super_file = project_root / ".super"
        if not super_file.exists():
            console.print(
                "\n[bold red]❌ Not a valid super project. Run 'super init <project_name>' to get started.[/bold red]"
            )
            return

        with open(super_file) as f:
            config = yaml.safe_load(f)
            project_name = config.get("project")

        # Find agent playbook
        agents_dir = project_root / project_name / "agents"
        playbook_path = next(agents_dir.rglob(f"**/{agent_name}_playbook.yaml"), None)

        # Find compiled pipeline
        compiler = AgentCompiler()
        pipeline_path = compiler._get_pipeline_path(agent_name)

        if not playbook_path and not pipeline_path.exists():
            console.print(
                f"\n[bold yellow]🟡 Agent '{agent_name}' not found. Nothing to remove.[/bold yellow]"
            )
            return

        console.print(
            f"\n[bold red]🔥 Preparing to remove agent '{agent_name}'[/bold red]"
        )
        files_to_remove = []
        if playbook_path and playbook_path.exists():
            files_to_remove.append(f"Playbook: {playbook_path}")
        if pipeline_path.exists():
            files_to_remove.append(f"Pipeline: {pipeline_path}")

        summary = "\n".join(files_to_remove)
        console.print(
            Panel(
                f"The following files will be permanently deleted:\n\n{summary}",
                title="🚨 Confirmation Required",
                border_style="bold red",
                padding=(1, 2),
            )
        )

        from rich.prompt import Confirm

        if Confirm.ask(
            f"Are you sure you want to delete these files for agent '{agent_name}'?",
            default=False,
        ):
            playbook_dir = None
            if playbook_path and playbook_path.exists():
                playbook_dir = playbook_path.parent
                playbook_path.unlink()
                console.print(f"✅ [green]Removed playbook:[/] {playbook_path}")

            if pipeline_path.exists():
                pipeline_dir = pipeline_path.parent
                pipeline_path.unlink()
                console.print(f"✅ [green]Removed pipeline:[/] {pipeline_path}")
                # Clean up the 'pipelines' directory if it's empty
                if pipeline_dir.is_dir() and not any(pipeline_dir.iterdir()):
                    pipeline_dir.rmdir()
                    console.print(
                        f"✅ [green]Removed empty pipelines directory:[/] {pipeline_dir}"
                    )

            # Clean up the agent's main directory if it's empty
            if playbook_dir and playbook_dir.is_dir() and not any(playbook_dir.iterdir()):
                # Ensure we don't delete the root 'agents' directory
                if playbook_dir.name != "agents":
                    playbook_dir.rmdir()
                    console.print(
                        f"✅ [green]Removed empty agent directory:[/] {playbook_dir}"
                    )

            console.print(
                f"\n[bold green]🎉 Successfully removed agent '{agent_name}'.[/bold green]"
            )
        else:
            console.print("\n[yellow]🟡 Removal cancelled by user.[/yellow]")

    except Exception as e:
        console.print(
            f"\n[bold red]❌ An unexpected error occurred during removal:[/] {e}"
        )
        sys.exit(1)


def inspect_agent(args):
    """Show detailed information about a single agent."""
    if not args.name:
        console.print(
            "[bold red]❌ You must specify an agent name to inspect.[/bold red]"
        )
        return

    agent_name = args.name.lower()
    try:
        project_root = Path.cwd()
        with open(project_root / ".super") as f:
            system_name = yaml.safe_load(f).get("project")

        # Find playbook file in project or pre-built agents
        playbook_path = next(
            (project_root / system_name / "agents").rglob(
                f"**/{agent_name}_playbook.yaml"
            ),
            None,
        )
        if not playbook_path:
            package_root = Path(__file__).parent.parent.parent
            playbook_path = next(
                package_root.rglob(f"**/agents/**/{agent_name}_playbook.yaml"), None
            )

        if not playbook_path or not playbook_path.exists():
            console.print(
                f"\n[bold red]❌ Agent playbook for '{agent_name}' not found.[/bold red]"
            )
            return

        with open(playbook_path) as f:
            data = yaml.safe_load(f)

        metadata = data.get("metadata", {})
        spec = data.get("spec", {})
        title = metadata.get("name", agent_name.title())
        description = metadata.get("description", "No description provided.")

        panel_content = f"[bold bright_cyan]{title}[/]\n"
        panel_content += f"[dim]{playbook_path}[/dim]\n\n"
        panel_content += f"{description}\n\n"
        panel_content += (
            f"[bold]Author:[/] {metadata.get('author', 'N/A')}\n"
            f"[bold]Version:[/] {metadata.get('version', 'N/A')}\n"
            f"[bold]License:[/] {metadata.get('license', 'N/A')}"
        )

        console.print(
            Panel(
                panel_content,
                title="🕵️ Agent Details",
                border_style="bright_blue",
                padding=(1, 2),
            )
        )

        # Display capabilities
        capabilities = spec.get("capabilities", [])
        if capabilities:
            table = Table(
                title="🛠️ Capabilities", show_header=True, header_style="bold magenta"
            )
            table.add_column("Capability", style="cyan")
            table.add_column("Description", style="white")
            for cap in capabilities:
                table.add_row(cap.get("name"), cap.get("description"))
            console.print(table)

        # Display dependencies
        dependencies = spec.get("dependencies", {})
        if dependencies.get("tools") or dependencies.get("apis"):
            dep_table = Table(
                title="🔗 Dependencies", show_header=True, header_style="bold yellow"
            )
            dep_table.add_column("Type", style="cyan")
            dep_table.add_column("Dependency", style="white")
            for tool in dependencies.get("tools", []):
                dep_table.add_row("Tool", tool)
            for api in dependencies.get("apis", []):
                dep_table.add_row("API", api)
            console.print(dep_table)

        # Display recent traces
        trace_path = project_root / ".superoptix" / "traces" / f"{agent_name}.jsonl"
        if trace_path.exists():
            trace_table = Table(
                title=f"📜 Recent Traces for '{agent_name}'",
                show_header=True,
                header_style="bold blue",
            )
            trace_table.add_column("Timestamp", style="dim", width=26)
            trace_table.add_column("Event", style="cyan")
            trace_table.add_column("Component", style="green")
            trace_table.add_column("Duration (ms)", style="magenta", justify="right")
            trace_table.add_column("Status", style="white")

            with open(trace_path) as f:
                lines = f.readlines()
                # Display the last 10 events
                for line in lines[-10:]:
                    try:
                        trace = json.loads(line)
                        timestamp = trace.get("timestamp", "")
                        event_type = trace.get("event_type", "N/A")
                        component = trace.get("component", "N/A")
                        duration = trace.get("duration_ms")
                        status = trace.get("status", "N/A")

                        # Format status with an emoji
                        status_emoji = {
                            "success": "✅",
                            "error": "❌",
                            "warning": "⚠️",
                            "info": "ℹ️",
                        }.get(status, "")

                        trace_table.add_row(
                            timestamp,
                            event_type,
                            component,
                            f"{duration:.2f}" if duration is not None else "N/A",
                            f"{status_emoji} {status.title()}",
                        )
                    except json.JSONDecodeError:
                        # Skip corrupted lines
                        continue
            console.print(trace_table)

            # Display raw trace file content
            console.print(
                Panel(
                    "".join(lines[-10:]),
                    title=f"📄 Raw Content: {trace_path.name}",
                    border_style="dim blue",
                    padding=(1, 2),
                )
            )
        else:
            console.print(
                Panel(
                    f"No traces found for agent '{agent_name}'.\n\n"
                    "To generate traces, run the agent first:\n"
                    f"[bold cyan]super agent run {agent_name} --goal \"your goal\"[/]",
                    title="📜 Trace Information",
                    border_style="yellow",
                    padding=(1, 2),
                )
            )

    except Exception as e:
        console.print(
            f"\n[bold red]❌ An unexpected error occurred during inspection:[/] {e}"
        )
        sys.exit(1)
