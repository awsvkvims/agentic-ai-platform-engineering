from src.ai.langgraph_agent import run_langgraph_agent


def test_kanban_route():
    source, reason, confidence, tool_result, response, selected_tools = run_langgraph_agent(
        "What is lead time?"
    )

    assert source == "tools: kanban_metrics"
    assert confidence == "high"
    assert selected_tools[0]["name"] == "kanban_metrics"
    assert "lead time" in tool_result.lower()
    assert len(response) > 0


def test_platform_route():
    source, reason, confidence, tool_result, response, selected_tools = run_langgraph_agent(
        "What is an internal developer platform?"
    )

    assert source == "tools: platform_engineering"
    assert confidence == "high"
    assert selected_tools[0]["name"] == "platform_engineering"
    assert "platform" in tool_result.lower()
    assert len(response) > 0


def test_multi_tool_selection():
    source, reason, confidence, tool_result, response, selected_tools = run_langgraph_agent(
        "Analyze Terraform and CI/CD pipeline risks"
    )

    tool_names = [tool["name"] for tool in selected_tools]

    assert "terraform_analyzer" in tool_names
    assert "cicd_pipeline_reviewer" in tool_names
    assert confidence == "high"
    assert len(response) > 0


def test_fallback_path():
    source, reason, confidence, tool_result, response, selected_tools = run_langgraph_agent(
        "Tell me a joke about software engineering"
    )

    # No tools expected
    assert selected_tools == []
    assert confidence in ["low", "medium"]
    assert len(response) > 0


def test_pr_tool():
    source, reason, confidence, tool_result, response, selected_tools = run_langgraph_agent(
        "Summarize this infrastructure pull request"
    )

    assert selected_tools[0]["name"] == "pr_infra_summarizer"
    assert "security group" in tool_result.lower() or "s3" in tool_result.lower()
    assert confidence == "high"
    assert len(response) > 0