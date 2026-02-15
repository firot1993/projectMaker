"""ProjectMaker CLI - Interactive AI brainstorming tool."""

import click
from rich.console import Console
from rich.markdown import Markdown

from .core import ai_client, analyzer, project

console = Console()


@click.group()
def cli():
    """ProjectMaker - Interactive AI-powered project brainstorming."""
    pass


@cli.command()
@click.argument("name")
def init(name):
    """Initialize a new project."""
    # Validate project name
    if not name or not name.strip():
        console.print("[red]Error:[/red] Project name cannot be empty.")
        raise SystemExit(1)
    
    # Check for invalid characters that could cause filesystem issues
    invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|', '\0']
    if any(char in name for char in invalid_chars):
        console.print(f"[red]Error:[/red] Project name contains invalid characters: {invalid_chars}")
        raise SystemExit(1)
    
    path = project.get_project_path()
    if path.exists():
        console.print(f"[red]Error:[/red] project.json already exists in this directory.")
        raise SystemExit(1)

    proj = project.create_project(name)
    project.save_project(proj)
    console.print(f"[green]Project '{name}' initialized.[/green]")
    console.print(f"Created {path}")


@cli.command()
@click.argument("prompt")
def brainstorm(prompt):
    """Generate brainstorming ideas from AI."""
    try:
        proj = project.load_project()
    except (FileNotFoundError, ValueError) as e:
        console.print(f"[red]Error:[/red] {e}")
        raise SystemExit(1)

    console.print(f"\n[bold]Brainstorming:[/bold] {prompt}\n")

    try:
        response = ai_client.brainstorm(prompt, proj["accepted_ideas"])
    except RuntimeError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise SystemExit(1)

    project.add_round(proj, prompt, response)
    project.save_project(proj)

    round_data = proj["rounds"][-1]
    console.print(Markdown(response))
    console.print(f"\n[dim]Saved as round {round_data['id']} with {len(round_data['bullets'])} bullets.[/dim]")
    console.print(f"[dim]Run 'projectmaker select {round_data['id']}' to accept ideas.[/dim]")


@cli.command()
@click.argument("round_id", type=int)
def select(round_id):
    """Select bullets to accept from a brainstorming round."""
    try:
        proj = project.load_project()
    except (FileNotFoundError, ValueError) as e:
        console.print(f"[red]Error:[/red] {e}")
        raise SystemExit(1)

    try:
        round_data = project.get_round(proj, round_id)
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise SystemExit(1)

    console.print(f"\n[bold]Round {round_id}:[/bold] {round_data['prompt']}\n")
    for bullet in round_data["bullets"]:
        check = "x" if bullet["selected"] else " "
        console.print(f"  {bullet['id']}. [{check}] {bullet['text']}")

    console.print()
    selection = click.prompt("Enter bullet numbers to accept (e.g., 1,3,5)", default="", show_default=False)

    if not selection.strip():
        console.print("[yellow]No bullets selected. Nothing changed.[/yellow]")
        return

    try:
        bullet_ids = [int(x.strip()) for x in selection.split(",") if x.strip()]
    except ValueError:
        console.print("[red]Error:[/red] Invalid input. Use comma-separated numbers (e.g., 1,3,5).")
        raise SystemExit(1)

    try:
        project.select_bullets(proj, round_id, bullet_ids)
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise SystemExit(1)

    project.save_project(proj)
    console.print(f"\n[green]Accepted {len(bullet_ids)} idea(s).[/green]")
    console.print(f"[dim]Total accepted ideas: {len(proj['accepted_ideas'])}[/dim]")


@cli.command()
def analyze():
    """Analyze if project foundation is sufficient."""
    try:
        proj = project.load_project()
    except (FileNotFoundError, ValueError) as e:
        console.print(f"[red]Error:[/red] {e}")
        raise SystemExit(1)

    console.print("\n[bold]Analyzing project readiness...[/bold]\n")

    try:
        analysis = analyzer.run_analysis(proj)
    except RuntimeError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise SystemExit(1)

    project.save_project(proj)

    if analysis["ready"]:
        console.print("[green bold]Analysis: Ready to proceed![/green bold]")
    else:
        console.print("[yellow bold]Analysis: Not ready[/yellow bold]")

    if analysis.get("summary"):
        console.print(f"\n{analysis['summary']}")

    if analysis["gaps"]:
        console.print("\n[bold]Missing:[/bold]")
        for gap in analysis["gaps"]:
            console.print(f"  - {gap}")

    if not analysis["ready"]:
        console.print("\n[dim]Recommendation: Run more brainstorming rounds to address gaps.[/dim]")
    else:
        console.print("\n[dim]Run 'projectmaker plan' to generate an implementation plan.[/dim]")


@cli.command()
def plan():
    """Generate implementation plan from accepted ideas."""
    try:
        proj = project.load_project()
    except (FileNotFoundError, ValueError) as e:
        console.print(f"[red]Error:[/red] {e}")
        raise SystemExit(1)

    console.print("\n[bold]Generating implementation plan...[/bold]\n")

    try:
        result = analyzer.generate_plan(proj)
    except RuntimeError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise SystemExit(1)

    if result is None:
        analysis = proj.get("analysis", {})
        console.print("[yellow]Project not ready for planning.[/yellow]")
        if analysis.get("gaps"):
            console.print("\n[bold]Missing:[/bold]")
            for gap in analysis["gaps"]:
                console.print(f"  - {gap}")
        console.print("\n[dim]Run more brainstorming rounds to address gaps, then try again.[/dim]")
        raise SystemExit(1)

    project.save_project(proj)
    console.print(Markdown(result))
    console.print("\n[green]Plan saved to project.json.[/green]")
