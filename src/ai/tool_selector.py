import json
from src.ai.client import ask_model
from src.ai.tool_registry import TOOLS, get_tool_descriptions


def choose_tool(user_input: str) -> str:
    tool_descriptions = get_tool_descriptions()
    valid_tool_names = [tool.name for tool in TOOLS]
    valid_tool_names_text = "\n".join(f"- {name}" for name in valid_tool_names)

    prompt = f"""
You are a tool selector.

Available tools:
{tool_descriptions}

User request:
{user_input}

Respond ONLY in JSON like this:

{{"tool": "tool_name"}}

Valid tool names:
{valid_tool_names_text}
- none
"""

    response = ask_model(prompt)

    try:
        data = json.loads(response)
        selected_tool = data.get("tool", "none")
        if selected_tool in valid_tool_names or selected_tool == "none":
            return selected_tool
        return "none"
    except Exception:
        return "none"