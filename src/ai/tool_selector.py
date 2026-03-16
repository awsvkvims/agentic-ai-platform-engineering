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

Return only one of these:
- kanban_metrics
- platform_engineering
- pi_planning_dependencies
- none

Do not explain your answer. Return only the tool name or none.
"""

    response = ask_model(prompt)
    return response.strip().lower()
