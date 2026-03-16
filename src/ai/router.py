from src.ai.client import ask_model
from src.ai.tool_registry import TOOLS
from src.ai.tool_selector import choose_tool


def route_request(user_input: str) -> tuple[str, str]:
    tool_name = choose_tool(user_input)

    if tool_name != "none":
        for tool in TOOLS:
            if tool.name == tool_name:
                return f"tool: {tool.name}", tool.func()

    return "model: openai", ask_model(user_input)