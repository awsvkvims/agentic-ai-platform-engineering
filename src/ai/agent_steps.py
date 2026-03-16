from src.ai.tool_selector import choose_tool
from src.ai.tool_registry import TOOLS
from src.ai.client import ask_model
from src.ai.prompt_loader import load_prompt


def select_tool_step(user_input):
    return choose_tool(user_input)


def run_tool_step(tool_name):
    for tool in TOOLS:
        if tool.name == tool_name:
            if tool.name == "backlog_analysis":
                with open("samples/backlog/sample_backlog.txt", "r") as f:
                    return tool.func(f.read())
            elif tool.name == "terraform_analyzer":
                with open("samples/terraform/sample_terraform.tf", "r") as f:
                    return tool.func(f.read())
            elif tool.name == "cicd_pipeline_reviewer":
                with open("samples/pipeline/sample_pipeline.yml", "r") as f:
                    return tool.func(f.read())
            return tool.func()
    return ""


def synthesize_step(user_input, tool_result):
    template = load_prompt("synthesis.txt")

    prompt = template.format(
        user_input=user_input,
        tool_result=tool_result
    )

    return ask_model(prompt)

