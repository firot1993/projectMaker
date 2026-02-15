"""Tests for project state management."""

import json
import os

import pytest

from projectmaker.core.project import (
    add_round,
    create_project,
    get_round,
    load_project,
    parse_bullets,
    save_project,
    select_bullets,
)


@pytest.fixture
def sample_project():
    return create_project("test-project")


@pytest.fixture
def project_with_round(sample_project):
    ai_response = """Here are some ideas:
- [ ] Use PostgreSQL database
- [ ] Implement real-time updates
- [ ] Add user authentication
- [ ] Build REST API"""
    add_round(sample_project, "I want to build a task manager", ai_response)
    return sample_project


def test_create_project():
    proj = create_project("my-app")
    assert proj["name"] == "my-app"
    assert proj["rounds"] == []
    assert proj["accepted_ideas"] == []
    assert proj["analysis"] is None
    assert proj["plan"] is None
    assert "created_at" in proj


def test_save_and_load_project(tmp_path, sample_project):
    os.chdir(tmp_path)
    save_project(sample_project)
    loaded = load_project()
    assert loaded["name"] == sample_project["name"]
    assert loaded["rounds"] == []


def test_load_project_not_found(tmp_path):
    os.chdir(tmp_path)
    with pytest.raises(FileNotFoundError, match="No project found"):
        load_project()


def test_load_project_corrupted(tmp_path):
    os.chdir(tmp_path)
    (tmp_path / "project.json").write_text("not json{{{")
    with pytest.raises(ValueError, match="Corrupted"):
        load_project()


def test_parse_bullets_checkbox():
    response = """- [ ] Idea one
- [ ] Idea two
- [x] Idea three"""
    bullets = parse_bullets(response)
    assert bullets == ["Idea one", "Idea two", "Idea three"]


def test_parse_bullets_fallback():
    response = """- Idea one
- Idea two
- Idea three"""
    bullets = parse_bullets(response)
    assert bullets == ["Idea one", "Idea two", "Idea three"]


def test_parse_bullets_mixed_content():
    response = """Here are some ideas:

- [ ] Build a REST API
- [ ] Use PostgreSQL
- [ ] Add authentication

Let me know what you think!"""
    bullets = parse_bullets(response)
    assert len(bullets) == 3
    assert bullets[0] == "Build a REST API"


def test_add_round(sample_project):
    response = "- [ ] Idea A\n- [ ] Idea B"
    add_round(sample_project, "test prompt", response)
    assert len(sample_project["rounds"]) == 1
    r = sample_project["rounds"][0]
    assert r["id"] == 1
    assert r["prompt"] == "test prompt"
    assert len(r["bullets"]) == 2
    assert r["bullets"][0]["text"] == "Idea A"
    assert r["bullets"][0]["selected"] is False


def test_add_multiple_rounds(sample_project):
    add_round(sample_project, "p1", "- [ ] A")
    add_round(sample_project, "p2", "- [ ] B")
    assert len(sample_project["rounds"]) == 2
    assert sample_project["rounds"][1]["id"] == 2


def test_select_bullets(project_with_round):
    select_bullets(project_with_round, 1, [1, 3])
    r = project_with_round["rounds"][0]
    assert r["bullets"][0]["selected"] is True
    assert r["bullets"][1]["selected"] is False
    assert r["bullets"][2]["selected"] is True
    assert "Use PostgreSQL database" in project_with_round["accepted_ideas"]
    assert "Add user authentication" in project_with_round["accepted_ideas"]
    assert len(project_with_round["accepted_ideas"]) == 2


def test_select_bullets_invalid_id(project_with_round):
    with pytest.raises(ValueError, match="don't exist"):
        select_bullets(project_with_round, 1, [1, 99])


def test_select_bullets_no_duplicates(project_with_round):
    select_bullets(project_with_round, 1, [1])
    select_bullets(project_with_round, 1, [1])
    assert project_with_round["accepted_ideas"].count("Use PostgreSQL database") == 1


def test_get_round(project_with_round):
    r = get_round(project_with_round, 1)
    assert r["id"] == 1


def test_get_round_not_found(project_with_round):
    with pytest.raises(ValueError, match="Round 5 not found"):
        get_round(project_with_round, 5)
