import json
from src.ai.client import ask_model
from src.ai.tool_registry import TOOLS, get_tool_descriptions
from src.ai.prompt_loader import load_prompt


def choose_tool(user_input: str) -> tuple[str, str, str]:
    tool_descriptions = get_tool_descriptions()

    valid_tool_names = [tool.name for tool in TOOLS]
    valid_tool_names_text = "\n".join(valid_tool_names)

    template = load_prompt("tool_selector.txt")

    prompt = template.format(
        tool_descriptions=tool_descriptions,
        user_input=user_input,
        valid_tool_names=valid_tool_names_text,
    )

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