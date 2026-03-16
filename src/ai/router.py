from src.ai.client import ask_model
from src.ai.agent_steps import select_tool_step, run_tool_step, synthesize_step


def route_request(user_input: str) -> tuple[str, str, str, str, str]:

    tool_name, reason, confidence = select_tool_step(user_input)

    if tool_name != "none" and confidence == "high":
        tool_result = run_tool_step(tool_name)
        final_answer = synthesize_step(user_input, tool_result)

        source = f"tool: {tool_name}"
        return source, reason, confidence, tool_result, final_answer

    final_answer = ask_model(user_input)
    source = "model: openai"

    return source, reason, confidence, "", final_answer