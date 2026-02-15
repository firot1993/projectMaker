"""Claude API wrapper with retry logic."""

import time

import anthropic

MODEL = "claude-sonnet-4-5-20250929"
MAX_RETRIES = 3
BASE_DELAY = 1.0


def create_client() -> anthropic.Anthropic:
    """Create Anthropic client (uses ANTHROPIC_API_KEY env var)."""
    return anthropic.Anthropic()


def call_claude(prompt: str, system: str = "", client: anthropic.Anthropic | None = None) -> str:
    """Send a prompt to Claude with retry logic. Returns response text."""
    if client is None:
        client = create_client()

    messages = [{"role": "user", "content": prompt}]
    last_error = None

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            kwargs = {"model": MODEL, "max_tokens": 4096, "messages": messages}
            if system:
                kwargs["system"] = system
            response = client.messages.create(**kwargs)
            return response.content[0].text
        except (anthropic.APIConnectionError, anthropic.RateLimitError, anthropic.APIStatusError) as e:
            last_error = e
            if attempt < MAX_RETRIES:
                delay = BASE_DELAY * (2 ** (attempt - 1))
                time.sleep(delay)

    raise RuntimeError(f"AI request failed after {MAX_RETRIES} attempts: {last_error}")


def brainstorm(user_prompt: str, accepted_ideas: list[str], client: anthropic.Anthropic | None = None) -> str:
    """Generate brainstorming ideas."""
    context = ""
    if accepted_ideas:
        ideas_list = "\n".join(f"- {idea}" for idea in accepted_ideas)
        context = f"Previously accepted ideas:\n{ideas_list}\n\n"

    prompt = f"""{context}User request: {user_prompt}

Generate 4-8 ideas as a markdown bullet list with checkboxes.
Format each as: - [ ] <idea description>
Each idea should be specific and actionable."""

    system = "You are a project brainstorming assistant. Generate creative, practical ideas formatted as markdown checkbox bullets."
    return call_claude(prompt, system=system, client=client)


def analyze(accepted_ideas: list[str], client: anthropic.Anthropic | None = None) -> dict:
    """Analyze if accepted ideas form a sufficient project foundation."""
    ideas_list = "\n".join(f"- {idea}" for idea in accepted_ideas)

    prompt = f"""Evaluate these project ideas for readiness to proceed to implementation planning:

{ideas_list}

Evaluate:
1. **Completeness:** Are core requirements covered (purpose, features, constraints, success criteria)?
2. **Clarity:** Are ideas specific and unambiguous?
3. **Feasibility:** Are ideas achievable and non-contradictory?

Respond in this exact format:
READY: true or false
GAPS: comma-separated list of missing areas (or "none")
SUMMARY: 1-2 sentence assessment"""

    system = "You are a project analysis assistant. Evaluate project readiness objectively."
    response = call_claude(prompt, system=system, client=client)
    return parse_analysis(response)


def parse_analysis(response: str) -> dict:
    """Parse analysis response into structured data."""
    ready = False
    gaps = []
    summary = ""

    for line in response.splitlines():
        line = line.strip()
        upper = line.upper()
        if upper.startswith("READY:"):
            ready = "true" in line.lower().split(":", 1)[1]
        elif upper.startswith("GAPS:"):
            gaps_text = line.split(":", 1)[1].strip()
            if gaps_text.lower() != "none":
                gaps = [g.strip() for g in gaps_text.split(",") if g.strip()]
        elif upper.startswith("SUMMARY:"):
            summary = line.split(":", 1)[1].strip()

    return {"ready": ready, "gaps": gaps, "summary": summary}


def generate_plan(accepted_ideas: list[str], project_name: str, client: anthropic.Anthropic | None = None) -> str:
    """Generate an implementation plan from accepted ideas."""
    ideas_list = "\n".join(f"- {idea}" for idea in accepted_ideas)

    prompt = f"""Create an implementation plan for the project "{project_name}" based on these accepted ideas:

{ideas_list}

Provide a structured plan with:
1. Project overview
2. Architecture decisions
3. Implementation phases with specific tasks
4. Tech stack recommendations
5. Key milestones"""

    system = "You are a software architect. Create clear, actionable implementation plans."
    return call_claude(prompt, system=system, client=client)
