from src.ai.client import ask_model
from src.ai.tool_registry import TOOLS
from src.ai.tool_selector import choose_tool


def route_request(user_input: str) -> tuple[str, str, str]:
    tool_name, reason = choose_tool(user_input)

    if tool_name != "none":
        for tool in TOOLS:
            if tool.name == tool_name:
                tool_result = tool.func()

                synthesis_prompt = f"""
You are an assistant helping with Agile delivery, DevOps enablement, and platform engineering.

User question:
{user_input}

Tool result:
{tool_result}

Use the tool result to produce a helpful final answer for the user.
Do not mention that a tool was used.
"""

                final_answer = ask_model(synthesis_prompt)

                return f"tool: {tool.name} | reason: {reason}", tool_result, final_answer

    final_answer = ask_model(user_input)
    return f"model: openai | reason: {reason}", "", final_answer