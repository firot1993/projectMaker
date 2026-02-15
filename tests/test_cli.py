"""Tests for CLI commands using Click's test runner."""

import json
import os
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from projectmaker.cli import cli


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def project_dir(tmp_path):
    os.chdir(tmp_path)
    return tmp_path


def test_init(runner, project_dir):
    result = runner.invoke(cli, ["init", "my-app"])
    assert result.exit_code == 0
    assert "initialized" in result.output

    proj = json.loads((project_dir / "project.json").read_text())
    assert proj["name"] == "my-app"


def test_init_empty_name(runner, project_dir):
    """Test that empty project name is rejected."""
    result = runner.invoke(cli, ["init", ""])
    assert result.exit_code != 0
    assert "cannot be empty" in result.output


def test_init_invalid_characters(runner, project_dir):
    """Test that invalid characters in project name are rejected."""
    result = runner.invoke(cli, ["init", "my/project"])
    assert result.exit_code != 0
    assert "invalid characters" in result.output


def test_init_already_exists(runner, project_dir):
    runner.invoke(cli, ["init", "my-app"])
    result = runner.invoke(cli, ["init", "my-app"])
    assert result.exit_code != 0
    assert "already exists" in result.output


@patch("projectmaker.cli.ai_client.brainstorm")
def test_brainstorm(mock_brainstorm, runner, project_dir):
    mock_brainstorm.return_value = "- [ ] Idea A\n- [ ] Idea B\n- [ ] Idea C"
    runner.invoke(cli, ["init", "test-proj"])
    result = runner.invoke(cli, ["brainstorm", "build something cool"])
    assert result.exit_code == 0
    assert "round 1" in result.output

    proj = json.loads((project_dir / "project.json").read_text())
    assert len(proj["rounds"]) == 1
    assert len(proj["rounds"][0]["bullets"]) == 3


@patch("projectmaker.cli.ai_client.brainstorm")
def test_brainstorm_no_project(mock_brainstorm, runner, project_dir):
    result = runner.invoke(cli, ["brainstorm", "test"])
    assert result.exit_code != 0
    assert "No project found" in result.output


@patch("projectmaker.cli.ai_client.brainstorm")
def test_select(mock_brainstorm, runner, project_dir):
    mock_brainstorm.return_value = "- [ ] Idea A\n- [ ] Idea B\n- [ ] Idea C"
    runner.invoke(cli, ["init", "test-proj"])
    runner.invoke(cli, ["brainstorm", "test"])
    result = runner.invoke(cli, ["select", "1"], input="1,3\n")
    assert result.exit_code == 0
    assert "Accepted 2 idea(s)" in result.output

    proj = json.loads((project_dir / "project.json").read_text())
    assert len(proj["accepted_ideas"]) == 2


def test_select_invalid_round(runner, project_dir):
    runner.invoke(cli, ["init", "test-proj"])
    result = runner.invoke(cli, ["select", "99"])
    assert result.exit_code != 0
    assert "not found" in result.output


@patch("projectmaker.cli.analyzer.run_analysis")
def test_analyze(mock_analysis, runner, project_dir):
    mock_analysis.return_value = {
        "ready": False,
        "gaps": ["authentication", "deployment"],
        "summary": "Missing key areas.",
    }
    runner.invoke(cli, ["init", "test-proj"])
    result = runner.invoke(cli, ["analyze"])
    assert result.exit_code == 0
    assert "Not ready" in result.output
    assert "authentication" in result.output


@patch("projectmaker.cli.analyzer.run_analysis")
def test_analyze_ready(mock_analysis, runner, project_dir):
    mock_analysis.return_value = {
        "ready": True,
        "gaps": [],
        "summary": "Good to go.",
    }
    runner.invoke(cli, ["init", "test-proj"])
    result = runner.invoke(cli, ["analyze"])
    assert result.exit_code == 0
    assert "Ready" in result.output


@patch("projectmaker.cli.analyzer.generate_plan")
def test_plan_ready(mock_plan, runner, project_dir):
    mock_plan.return_value = "# Plan\n\n1. Do stuff"
    runner.invoke(cli, ["init", "test-proj"])
    result = runner.invoke(cli, ["plan"])
    assert result.exit_code == 0
    assert "saved" in result.output


@patch("projectmaker.cli.analyzer.generate_plan")
def test_plan_not_ready(mock_plan, runner, project_dir):
    mock_plan.return_value = None
    runner.invoke(cli, ["init", "test-proj"])

    # Need to set analysis state since generate_plan updates project in-place
    proj_path = project_dir / "project.json"
    proj = json.loads(proj_path.read_text())
    proj["analysis"] = {"ready": False, "gaps": ["testing"], "summary": "Not ready."}
    proj_path.write_text(json.dumps(proj))

    result = runner.invoke(cli, ["plan"])
    assert result.exit_code != 0
    assert "not ready" in result.output.lower()
