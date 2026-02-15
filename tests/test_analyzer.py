"""Tests for analyzer with mocked AI responses."""

from unittest.mock import patch

import pytest

from projectmaker.core.ai_client import parse_analysis
from projectmaker.core.analyzer import generate_plan, run_analysis
from projectmaker.core.project import create_project


@pytest.fixture
def project_with_ideas():
    proj = create_project("test-project")
    proj["accepted_ideas"] = [
        "Build a REST API with Flask",
        "Use PostgreSQL for data storage",
        "Add JWT authentication",
        "Deploy on AWS",
    ]
    return proj


def test_parse_analysis_ready():
    response = """READY: true
GAPS: none
SUMMARY: Project has sufficient foundation to proceed."""
    result = parse_analysis(response)
    assert result["ready"] is True
    assert result["gaps"] == []
    assert "sufficient" in result["summary"]


def test_parse_analysis_not_ready():
    response = """READY: false
GAPS: authentication approach, deployment strategy, testing plan
SUMMARY: Missing key areas."""
    result = parse_analysis(response)
    assert result["ready"] is False
    assert len(result["gaps"]) == 3
    assert "authentication approach" in result["gaps"]


def test_run_analysis_no_ideas():
    proj = create_project("empty")
    analysis = run_analysis(proj)
    assert analysis["ready"] is False
    assert len(analysis["gaps"]) > 0


@patch("projectmaker.core.analyzer.ai_client.analyze")
def test_run_analysis_ready(mock_analyze, project_with_ideas):
    mock_analyze.return_value = {
        "ready": True,
        "gaps": [],
        "summary": "Ready to proceed.",
    }
    analysis = run_analysis(project_with_ideas)
    assert analysis["ready"] is True
    assert project_with_ideas["analysis"]["ready"] is True


@patch("projectmaker.core.analyzer.ai_client.analyze")
def test_run_analysis_not_ready(mock_analyze, project_with_ideas):
    mock_analyze.return_value = {
        "ready": False,
        "gaps": ["testing strategy"],
        "summary": "Missing testing.",
    }
    analysis = run_analysis(project_with_ideas)
    assert analysis["ready"] is False
    assert "testing strategy" in analysis["gaps"]


@patch("projectmaker.core.analyzer.ai_client.generate_plan")
@patch("projectmaker.core.analyzer.ai_client.analyze")
def test_generate_plan_ready(mock_analyze, mock_plan, project_with_ideas):
    mock_analyze.return_value = {"ready": True, "gaps": [], "summary": "Ready."}
    mock_plan.return_value = "# Implementation Plan\n\n1. Setup project..."
    result = generate_plan(project_with_ideas)
    assert result is not None
    assert "Implementation Plan" in result
    assert project_with_ideas["plan"] is not None


@patch("projectmaker.core.analyzer.ai_client.analyze")
def test_generate_plan_not_ready(mock_analyze, project_with_ideas):
    mock_analyze.return_value = {
        "ready": False,
        "gaps": ["missing items"],
        "summary": "Not ready.",
    }
    result = generate_plan(project_with_ideas)
    assert result is None
    assert project_with_ideas["plan"] is None
