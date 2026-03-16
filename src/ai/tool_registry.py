from src.ai.tools import (
    kanban_metrics_tool,
    platform_engineering_tool,
    pi_planning_dependencies_tool,
    backlog_risk_tool,
)

TOOLS = [
    kanban_metrics_tool,
    platform_engineering_tool,
    pi_planning_dependencies_tool,
    backlog_risk_tool,
]


def list_tools() -> str:
    lines = []
    for tool in TOOLS:
        lines.append(f"- {tool.name}: {tool.description}")
    return "\n".join(lines)

def get_tool_descriptions() -> str:
    lines = []
    for tool in TOOLS:
        lines.append(f"{tool.name}: {tool.description}")
    return "\n".join(lines)

