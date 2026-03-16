from src.ai.client import ask_model
from src.ai.tool_registry import TOOLS
from src.ai.tool_selector import choose_tool


def route_request(user_input: str) -> tuple[str, str, str, str, str]:
    tool_name, reason, confidence = choose_tool(user_input)

    if tool_name != "none" and confidence == "high":
        for tool in TOOLS:
            if tool.name == tool_name:
                if tool.name == "backlog_analysis":
                    with open("sample_backlog.txt", "r") as f:
                        tool_result = tool.func(f.read())
                else:
                    tool_result = tool.func()

                synthesis_prompt = f"""
You are an assistant helping with Agile delivery, DevOps enablement, and platform engineering.

User question:
{user_input}

Tool result:
{tool_result}

Write a final answer for the user based directly on the tool result.

Requirements:
- Use the specific counts from the tool result
- Mention specific backlog items when relevant
- Do not give only generic advice
- Summarize the main risks found in this backlog
- End with a short list of practical actions
- Do not mention that a tool was used
"""

                final_answer = ask_model(synthesis_prompt)
                source = f"tool: {tool.name}"
                return source, reason, confidence, tool_result, final_answer

    final_answer = ask_model(user_input)
    source = "model: openai"
    return source, reason, confidence, "", final_answer