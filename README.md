# ProjectMaker

Interactive AI-powered project brainstorming CLI tool that helps you develop project ideas through iterative conversations with Claude AI.

## Features

- 🤖 AI-powered brainstorming with Claude
- ✅ Selective idea acceptance with checkboxes
- 📊 Project readiness analysis
- 📝 Automatic implementation plan generation
- 💾 Persistent project state in JSON format

## Installation

```bash
pip install -e .
```

For development:
```bash
pip install -e .[dev]
```

## Setup

1. **Get an Anthropic API Key**
   - Sign up at [anthropic.com](https://www.anthropic.com/)
   - Create an API key from your account dashboard

2. **Set Environment Variable**
   ```bash
   export ANTHROPIC_API_KEY='your-api-key-here'
   ```
   
   Or add to your `~/.bashrc` or `~/.zshrc`:
   ```bash
   echo 'export ANTHROPIC_API_KEY="your-api-key-here"' >> ~/.bashrc
   source ~/.bashrc
   ```

## Usage

### 1. Initialize a Project

```bash
projectmaker init "my-web-app"
```

Creates a `project.json` file in your current directory to track project state.

### 2. Brainstorm Ideas

```bash
projectmaker brainstorm "I want to build a task manager with real-time updates"
```

Claude will generate 4-8 ideas as checkbox bullets. Each brainstorming session is saved as a "round".

### 3. Select Ideas

```bash
projectmaker select 1
# Enter bullet numbers: 1,3,5
```

Choose which ideas you want to accept. Selected ideas become context for future brainstorming rounds.

### 4. Analyze Project Readiness

```bash
projectmaker analyze
```

Claude evaluates if you have enough accepted ideas to proceed with implementation planning.

### 5. Generate Implementation Plan

```bash
projectmaker plan
```

When your project is ready, this generates a detailed implementation plan based on all accepted ideas.

## Example Workflow

```bash
# Start a new project
projectmaker init "todo-app"

# First brainstorming round
projectmaker brainstorm "I want a web-based todo app"
projectmaker select 1
# Select ideas: 1,2,4

# Dive deeper into specific aspects
projectmaker brainstorm "What database should I use?"
projectmaker select 2
# Select: 2

projectmaker brainstorm "How should users authenticate?"
projectmaker select 3
# Select: 1,3

# Check if ready
projectmaker analyze

# Generate plan when ready
projectmaker plan
```

## Project Structure

- `project.json` - Your project's state (created in current directory)
- Contains all rounds, accepted ideas, analysis, and plans
- Can be manually edited or version controlled

## Development

Run tests:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=projectmaker
```

## Architecture

- **CLI Layer** (`cli.py`) - User interface with Click
- **Core Logic** (`core/`) - Business logic, AI client, analysis
- **Data Layer** (`project.py`) - JSON persistence

See [design.md](design.md) for detailed architecture documentation.

## Requirements

- Python 3.10+
- Anthropic API key
- Dependencies: click, rich, anthropic

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]
