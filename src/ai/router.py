from src.ai.client import ask_model
from src.ai.tools import (
    explain_kanban_metrics,
    explain_platform_engineering,
    explain_pi_planning_dependencies,
)


def route_request(user_input: str) -> tuple[str, str]:
    text = user_input.lower()

    kanban_terms = ["kanban metrics", "lead time", "cycle time", "throughput", "wip"]
    platform_terms = ["platform engineering", "developer platform", "internal developer platform"]
    pi_terms = ["pi planning dependencies", "pi dependencies", "program increment dependencies"]

    if any(term in text for term in kanban_terms):
        return "tool: explain_kanban_metrics", explain_kanban_metrics()
    elif any(term in text for term in platform_terms):
        return "tool: explain_platform_engineering", explain_platform_engineering()
    elif any(term in text for term in pi_terms):
        return "tool: explain_pi_planning_dependencies", explain_pi_planning_dependencies()
    else:
        return "model: openai", ask_model(user_input)