# ProjectMaker - Interactive AI Brainstorming Tool Design

**Date:** 2026-02-15
**Purpose:** CLI tool for iterative AI-powered project brainstorming with selective idea acceptance

## Overview

ProjectMaker helps users brainstorm project ideas with AI through an iterative process where the AI presents ideas as checkbox bullets, users select what they want, and subsequent discussions build on accepted ideas. The tool analyzes when enough ideas have been gathered and offers to generate implementation plans.

## Use Case

Personal project brainstorming where users:
1. Explore ideas through multiple brainstorming rounds
2. Accept/reject AI suggestions selectively
3. Build project foundation iteratively
4. Get AI analysis on readiness to proceed
5. Generate implementation plans when ready

## Architecture

### Tech Stack
- **Python** - Core language
- **click** - Command-line interface framework
- **rich** - Terminal markdown rendering and formatting
- **anthropic** - Claude API SDK
- **pytest** - Testing framework

### Project Structure
```
projectmaker/
├── cli.py              # Click commands (init, brainstorm, select, analyze, plan)
├── core/
│   ├── project.py      # Project state management (load/save JSON)
│   ├── ai_client.py    # Claude API wrapper
│   └── analyzer.py     # Sufficiency analysis logic
├── project.json        # User's project data (created by init)
└── tests/
    ├── test_project.py
    ├── test_analyzer.py
    └── test_cli.py
```

### Design Principles
- **Clean separation:** CLI interface, core logic, and data storage are independent
- **Stateless commands:** Each command is a pure function operating on project.json
- **Web-ready:** Core logic in `core/` can be reused with Flask/FastAPI later
- **Simple data model:** Single JSON file for portability and transparency

## Components & Commands

### 1. `projectmaker init <project-name>`
**Purpose:** Initialize new project

**Behavior:**
- Creates `project.json` in current directory
- Initializes structure: `{"name": "...", "rounds": [], "accepted_ideas": []}`
- No AI call required

**Example:**
```bash
projectmaker init "my-web-app"
```

### 2. `projectmaker brainstorm <prompt>`
**Purpose:** Generate new ideas from AI

**Behavior:**
- Sends prompt + all accepted ideas (context) to Claude
- Claude responds with markdown bullet list containing `[ ]` checkboxes
- Saves response as new round in `project.json` with bullets unchecked
- Renders formatted markdown in terminal using `rich`

**Example:**
```bash
projectmaker brainstorm "I want to build a task manager"
```

**AI Prompt Template:**
```
Context: {accepted_ideas}
User request: {user_prompt}

Generate 4-8 ideas as a markdown bullet list with checkboxes.
Format each as: - [ ] <idea description>
```

### 3. `projectmaker select <round-id>`
**Purpose:** Select bullets to accept from a brainstorming round

**Behavior:**
- Displays specified round's bullets with numbers
- Prompts: "Enter bullet numbers to accept (e.g., 1,3,5):"
- Updates `project.json` marking selected bullets as accepted
- Adds accepted bullet text to global `accepted_ideas` list

**Example:**
```bash
projectmaker select 1
# Shows:
# 1. [ ] Use PostgreSQL database
# 2. [ ] Implement real-time updates
# 3. [ ] Add user authentication
# Enter numbers: 1,3
```

### 4. `projectmaker analyze`
**Purpose:** Check if project foundation is sufficient

**Behavior:**
- Sends all `accepted_ideas` to Claude with analysis prompt
- Claude evaluates:
  - **Completeness:** Core requirements covered (purpose, features, constraints, success criteria)
  - **Clarity:** Ideas are specific and unambiguous
  - **Feasibility:** Ideas are achievable and non-contradictory
- Returns "Ready" or "Missing: [specific gaps]"
- Displays assessment with recommendations

**Example:**
```bash
projectmaker analyze
# Output:
# Analysis: Not ready
# Missing:
#   - Authentication approach
#   - Deployment strategy
# Recommendation: Run more brainstorming rounds to address gaps
```

### 5. `projectmaker plan`
**Purpose:** Generate implementation plan from accepted ideas

**Behavior:**
- Runs analyze internally first
- If not ready: shows gaps and suggests more brainstorming
- If ready: sends accepted ideas to Claude requesting implementation plan
- Saves plan to `project.json` under `plan` field
- Displays formatted plan in terminal

**Example:**
```bash
projectmaker plan
# If ready: generates and displays implementation plan
# If not: "Project not ready. Missing: [gaps]"
```

## Data Model

### project.json Structure
```json
{
  "name": "my-project",
  "created_at": "2026-02-15T10:30:00Z",
  "rounds": [
    {
      "id": 1,
      "timestamp": "2026-02-15T10:31:00Z",
      "prompt": "I want to build a task manager",
      "bullets": [
        {
          "id": 1,
          "text": "Use PostgreSQL database",
          "selected": true
        },
        {
          "id": 2,
          "text": "Implement real-time updates",
          "selected": false
        },
        {
          "id": 3,
          "text": "Add user authentication",
          "selected": true
        }
      ]
    }
  ],
  "accepted_ideas": [
    "Use PostgreSQL database",
    "Add user authentication"
  ],
  "analysis": {
    "last_run": "2026-02-15T10:35:00Z",
    "ready": false,
    "gaps": ["authentication approach", "deployment strategy"]
  },
  "plan": null
}
```

### Context Handling
- **Flat iteration:** Rounds are independent; context flows only through `accepted_ideas`
- **Cumulative context:** Each `brainstorm` command sends ALL `accepted_ideas` to Claude
- **User control:** Users decide what context matters by selecting bullets

## Data Flow

### Typical Workflow
```
1. projectmaker init "my-web-app"
   → Creates project.json

2. projectmaker brainstorm "I want to build a task manager"
   → AI generates bullets with checkboxes
   → Saves as round 1
   → Displays in terminal

3. projectmaker select 1
   → User selects bullets 1,3
   → Updates project.json
   → Adds to accepted_ideas

4. projectmaker brainstorm "What database should I use?"
   → AI sees context from round 1
   → Generates database option bullets
   → Saves as round 2

5. projectmaker select 2
   → User selects database choice

6. projectmaker analyze
   → AI evaluates accepted ideas
   → Returns gaps: "Missing: authentication, deployment"

7. projectmaker brainstorm "How should users authenticate?"
   → Continue iterating...

8. projectmaker analyze
   → AI returns: "Ready to proceed"

9. projectmaker plan
   → Generates implementation plan
   → Saved and displayed
```

### State Persistence
- Every state-modifying command saves immediately to `project.json`
- No in-memory sessions - each command is fully stateless
- Easy inspection and manual editing of project state

## Error Handling

### AI API Failures
- **Network errors, rate limits, invalid keys:**
  - Display clear error message
  - Don't corrupt `project.json`
  - Retry logic: 3 attempts with exponential backoff
  - User sees: "AI request failed: [reason]. Retrying... (attempt 2/3)"

### File System Errors
- **Missing project.json:**
  - Show: "No project found. Run 'projectmaker init <name>' first"
- **Corrupted project.json:**
  - Attempt parse, show specific error
  - Offer to backup and reinitialize
- **Permission errors:**
  - Clear message about file permissions

### Invalid User Input
- **Invalid round ID:**
  - "Round 3 not found. Available rounds: 1, 2"
- **Invalid bullet numbers:**
  - "Bullets 5,7 don't exist in round 1. Valid: 1-4"
- **Empty selections:**
  - "No bullets selected. Nothing changed."

### AI Response Validation
- **Non-markdown or missing checkboxes:**
  - Retry with clarified prompt
  - If retry fails: save raw response, warn user, allow manual fixing

### Graceful Degradation
- All errors preserve existing `project.json` state
- Failed operations never leave partial writes
- Users can inspect/manually edit `project.json` as fallback

## Testing Strategy

### Unit Tests (pytest)
- **test_project.py:** Project state management (load, save, add rounds, select bullets)
- **test_analyzer.py:** Analysis logic with mocked AI responses
- **test_cli.py:** Command parsing and execution with Click's test runner

### Integration Tests
- Mock Anthropic API responses using `pytest-mock` or `responses`
- Test full command flows: init → brainstorm → select → analyze → plan
- Verify `project.json` state after each command
- Test error scenarios (missing files, invalid inputs, API failures)

### Test Structure Example
```python
def test_select_updates_project(tmp_path):
    # Setup: Create project.json with one round
    # Execute: Run select command with bullet IDs
    # Assert: Check accepted_ideas updated correctly

def test_brainstorm_with_context(mock_anthropic):
    # Setup: Mock AI response, project with accepted ideas
    # Execute: Run brainstorm command
    # Assert: Verify AI received accepted ideas as context
```

### Coverage Goals
- >80% coverage on core logic
- Most tests use mocked AI calls for speed/determinism
- Optional end-to-end tests with real API (gated by env var)
- Pytest fixtures for common setup (temp dirs, sample project.json)

### Benefits of Command-Based Design
- Each command is pure function: input → state change → output
- Easy to test in isolation
- No complex session state to mock

## Future Migration Path

### To Web Application
- Reuse entire `core/` package unchanged
- Build Flask/FastAPI backend wrapping commands
- Frontend: React/Vue with rich markdown rendering
- WebSocket for real-time AI streaming responses
- Same `project.json` format, stored per-user

### Potential Enhancements (YAGNI for v1)
- Export to different formats (PDF, Notion)
- Team collaboration features
- Project templates
- Undo/redo functionality
- Git integration for project versioning

## Success Criteria

1. User can complete full workflow: init → multiple brainstorm rounds → select ideas → analyze → generate plan
2. All accepted ideas persist correctly across rounds
3. AI receives proper context in each brainstorm
4. Analysis accurately identifies gaps
5. Commands handle errors gracefully without corrupting state
6. Tests provide confidence in core logic
7. Clean architecture enables web migration

## Next Steps

Proceed to implementation planning with step-by-step tasks for building the CLI tool.
