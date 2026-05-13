import json
from src.ai.client import ask_model
from src.ai.tool_registry import TOOLS, get_tool_descriptions
from src.ai.prompt_loader import load_prompt


def choose_tools(user_input: str) -> tuple[list[dict], str, str]:
    tool_descriptions = get_tool_descriptions()
    valid_tool_names = [tool.name for tool in TOOLS]
    valid_tool_names_text = "\n".join(valid_tool_names)

    template = load_prompt("tool_selector_multi.txt")

    prompt = template.format(
        tool_descriptions=tool_descriptions,
        user_input=user_input,
        valid_tool_names=valid_tool_names_text,
    )

    response = ask_model(prompt)

    try:
        data = json.loads(response)
        selected_tools = data.get("tools", [])
        reason = data.get("reason", "").strip()
        confidence = data.get("confidence", "low").strip().lower()

        if confidence not in ["high", "medium", "low"]:
            confidence = "low"

        if not isinstance(selected_tools, list):
            return [], "Model did not return a valid tools list.", "low"

        filtered_tools = []
        seen = set()

        for item in selected_tools:
            if not isinstance(item, dict):
                continue

            name = item.get("name", "").strip()
            tool_reason = item.get("reason", "").strip()

            if name in valid_tool_names and name not in seen:
                filtered_tools.append(
                    {
                        "name": name,
                        "reason": tool_reason,
                    }
                )
                seen.add(name)

            if len(filtered_tools) == 2:
                break

        return filtered_tools, reason, confidence

    except Exception:
        return [], "Model did not return valid JSON.", "low"
    