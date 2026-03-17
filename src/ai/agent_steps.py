from src.ai.tool_selector import choose_tool
from src.ai.tool_registry import TOOLS
from src.ai.client import ask_model
from src.ai.prompt_loader import load_prompt
from src.ai.sample_registry import TOOL_SAMPLE_PATHS, read_sample_file


def select_tool_step(user_input):
    return choose_tool(user_input)


def run_tool_step(tool_name):
    for tool in TOOLS:
        if tool.name == tool_name:
            if tool.name in TOOL_SAMPLE_PATHS:
                sample_text = read_sample_file(TOOL_SAMPLE_PATHS[tool.name])
                return tool.func(sample_text)
            return tool.func()
    return ""


def synthesize_step(user_input, tool_result):
    template = load_prompt("synthesis.txt")

    prompt = template.format(
        user_input=user_input,
        tool_result=tool_result
    )

    return ask_model(prompt)

