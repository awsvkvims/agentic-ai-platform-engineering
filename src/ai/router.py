from src.ai.client import ask_model
from src.ai.tool_registry import TOOLS
from src.ai.tool_selector import choose_tool
from src.ai.prompt_loader import load_prompt


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

                template = load_prompt("synthesis.txt")
                synthesis_prompt = template.format(
                    user_input=user_input,
                    tool_result=tool_result,
                )

                final_answer = ask_model(synthesis_prompt)
                source = f"tool: {tool.name}"
                return source, reason, confidence, tool_result, final_answer

    final_answer = ask_model(user_input)
    source = "model: openai"
    return source, reason, confidence, "", final_answer