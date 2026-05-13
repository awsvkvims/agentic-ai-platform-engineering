from src.ai.tool_registry import TOOLS, list_tools, get_tool_descriptions

EXPECTED_TOOL_NAMES = {
    "kanban_metrics",
    "pi_planning_dependencies",
    "backlog_risk",
    "backlog_analysis",
    "platform_engineering",
    "terraform_analyzer",
    "cicd_pipeline_reviewer",
    "pr_infra_summarizer",
}


def test_all_expected_tools_are_registered():
    registered_names = {tool.name for tool in TOOLS}
    assert EXPECTED_TOOL_NAMES == registered_names


def test_every_tool_has_required_fields():
    for tool in TOOLS:
        assert isinstance(tool.name, str) and len(tool.name) > 0, f"{tool.name}: empty name"
        assert isinstance(tool.description, str) and len(tool.description) > 0, f"{tool.name}: empty description"
        assert callable(tool.func), f"{tool.name}: func is not callable"


def test_list_tools_output_contains_all_tool_names():
    output = list_tools()
    for name in EXPECTED_TOOL_NAMES:
        assert name in output, f"list_tools() missing: {name}"
