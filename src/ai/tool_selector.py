import json
from src.ai.client import ask_model
from src.ai.tool_registry import TOOLS, get_tool_descriptions


def choose_tool(user_input: str) -> tuple[str, str, str]:
    tool_descriptions = get_tool_descriptions()
    valid_tool_names = [tool.name for tool in TOOLS]
    valid_tool_names_text = "\n".join(f"- {name}" for name in valid_tool_names)

    prompt = f"""
You are a tool selector.

Available tools:
{tool_descriptions}

User request:
{user_input}

Choose a tool only if it is a strong match for the user's request.
If none of the tools is a strong match, return none.

Respond ONLY in JSON like this:

{{"tool": "tool_name", "reason": "short reason", "confidence": "high"}}

Valid tool names:
{valid_tool_names_text}
- none

Valid confidence values:
- high
- medium
- low
"""

    response = ask_model(prompt)

    try:
        data = json.loads(response)
        selected_tool = data.get("tool", "none")
        reason = data.get("reason", "").strip()
        confidence = data.get("confidence", "low").strip().lower()

        if confidence not in ["high", "medium", "low"]:
            confidence = "low"

        if selected_tool in valid_tool_names or selected_tool == "none":
            return selected_tool, reason, confidence

        return "none", "Model returned an invalid tool name.", "low"
    except Exception:
        return "none", "Model did not return valid JSON.", "low"