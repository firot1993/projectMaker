"""Project state management - load/save project.json."""

import json
import re
from datetime import datetime, timezone
from pathlib import Path

PROJECT_FILE = "project.json"


def get_project_path() -> Path:
    return Path.cwd() / PROJECT_FILE


def create_project(name: str) -> dict:
    """Create a new project state."""
    return {
        "name": name,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "rounds": [],
        "accepted_ideas": [],
        "analysis": None,
        "plan": None,
    }


def load_project() -> dict:
    """Load project from project.json in current directory."""
    path = get_project_path()
    if not path.exists():
        raise FileNotFoundError(
            "No project found. Run 'projectmaker init <name>' first."
        )
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as e:
        raise ValueError(f"Corrupted project.json: {e}")


def save_project(project: dict) -> None:
    """Save project state to project.json."""
    path = get_project_path()
    tmp_path = path.with_suffix(".json.tmp")
    tmp_path.write_text(json.dumps(project, indent=2) + "\n")
    tmp_path.replace(path)


def add_round(project: dict, prompt: str, ai_response: str) -> dict:
    """Parse AI response into bullets and add as a new round."""
    bullets = parse_bullets(ai_response)
    round_id = len(project["rounds"]) + 1
    new_round = {
        "id": round_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "prompt": prompt,
        "bullets": [
            {"id": i + 1, "text": text, "selected": False}
            for i, text in enumerate(bullets)
        ],
        "raw_response": ai_response,
    }
    project["rounds"].append(new_round)
    return project


def parse_bullets(response: str) -> list[str]:
    """Extract bullet items from AI markdown response."""
    bullets = []
    for line in response.splitlines():
        line = line.strip()
        match = re.match(r"^[-*]\s*\[[ x]\]\s*(.+)$", line)
        if match:
            bullets.append(match.group(1).strip())
    if not bullets:
        for line in response.splitlines():
            line = line.strip()
            match = re.match(r"^[-*]\s+(.+)$", line)
            if match:
                bullets.append(match.group(1).strip())
    return bullets


def select_bullets(project: dict, round_id: int, bullet_ids: list[int]) -> dict:
    """Mark bullets as selected and update accepted_ideas."""
    round_data = get_round(project, round_id)
    valid_ids = {b["id"] for b in round_data["bullets"]}
    invalid = set(bullet_ids) - valid_ids
    if invalid:
        raise ValueError(
            f"Bullets {sorted(invalid)} don't exist in round {round_id}. "
            f"Valid: 1-{len(round_data['bullets'])}"
        )
    for bullet in round_data["bullets"]:
        if bullet["id"] in bullet_ids:
            bullet["selected"] = True
            if bullet["text"] not in project["accepted_ideas"]:
                project["accepted_ideas"].append(bullet["text"])
    return project


def get_round(project: dict, round_id: int) -> dict:
    """Get a specific round by ID."""
    for r in project["rounds"]:
        if r["id"] == round_id:
            return r
    available = [r["id"] for r in project["rounds"]]
    raise ValueError(
        f"Round {round_id} not found. Available rounds: {available}"
    )
