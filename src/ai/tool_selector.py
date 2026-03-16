import json
from src.ai.client import ask_model
from src.ai.tool_registry import get_tool_descriptions


def choose_tool(user_input: str) -> str:
    tool_descriptions = get_tool_descriptions()

    prompt = f"""
You are a tool selector.

Available tools:
{tool_descriptions}

User request:
{user_input}

Respond ONLY in JSON like this:

{{"tool": "tool_name"}}

Valid tool names:
- kanban_metrics
- platform_engineering
- pi_planning_dependencies
- none
"""

    response = ask_model(prompt)

    try:
        data = json.loads(response)
        return data.get("tool", "none")
    except Exception:
        return "none"