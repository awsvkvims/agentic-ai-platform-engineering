from src.ai.client import ask_model
from src.ai.tool_registry import TOOLS


def route_request(user_input: str) -> tuple[str, str]:
    text = user_input.lower()

    tool_terms = {
        "kanban_metrics": ["kanban metrics", "lead time", "cycle time", "throughput", "wip"],
        "platform_engineering": ["platform engineering", "developer platform", "internal developer platform"],
        "pi_planning_dependencies": [
            "pi planning dependencies",
            "pi dependencies",
            "program increment dependencies",
        ],
    }

    for tool in TOOLS:
        terms = tool_terms.get(tool.name, [])
        if any(term in text for term in terms):
            return f"tool: {tool.name}", tool.func()

    return "model: openai", ask_model(user_input)
