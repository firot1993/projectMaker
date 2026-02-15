"""Sufficiency analysis logic."""

from datetime import datetime, timezone

from . import ai_client


def run_analysis(project: dict, client=None) -> dict:
    """Run analysis on project's accepted ideas and update project state."""
    accepted = project.get("accepted_ideas", [])
    if not accepted:
        return {
            "last_run": datetime.now(timezone.utc).isoformat(),
            "ready": False,
            "gaps": ["No ideas accepted yet. Run brainstorm and select commands first."],
            "summary": "No accepted ideas to analyze.",
        }

    result = ai_client.analyze(accepted, client=client)
    analysis = {
        "last_run": datetime.now(timezone.utc).isoformat(),
        "ready": result["ready"],
        "gaps": result["gaps"],
        "summary": result.get("summary", ""),
    }
    project["analysis"] = analysis
    return analysis


def generate_plan(project: dict, client=None) -> str:
    """Generate implementation plan. Runs analysis first."""
    analysis = run_analysis(project, client=client)
    if not analysis["ready"]:
        return None
    plan = ai_client.generate_plan(
        project["accepted_ideas"], project["name"], client=client
    )
    project["plan"] = plan
    return plan
