from src.tools.agile_tools import (
    kanban_metrics_tool,
    pi_planning_dependencies_tool,
    backlog_risk_tool,
    backlog_analysis_tool,
)

from src.tools.platform_tools import platform_engineering_tool
from src.tools.terraform_analyzer import terraform_analyzer_tool
from src.tools.ci_cd_tools import cicd_pipeline_reviewer_tool

TOOLS = [
    kanban_metrics_tool,
    platform_engineering_tool,
    pi_planning_dependencies_tool,
    backlog_risk_tool,
    backlog_analysis_tool,
    terraform_analyzer_tool,
    cicd_pipeline_reviewer_tool,
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

