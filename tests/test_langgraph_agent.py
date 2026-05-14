from unittest.mock import patch
from src.ai.langgraph_agent import run_langgraph_agent

MOCK_SYNTHESIS = "First pass synthesis output."
MOCK_REFINED = "Refined final response."
MOCK_FALLBACK = "Direct model fallback response."


# --- routing: single tool, happy path ---

def test_kanban_route():
    route = ([{"name": "kanban_metrics", "reason": "lead time query"}], "Kanban match", "high")
    with patch("src.ai.langgraph_agent.choose_tools", return_value=route), \
         patch("src.ai.langgraph_agent.synthesize_step", return_value=MOCK_SYNTHESIS), \
         patch("src.ai.langgraph_agent.ask_model", return_value=MOCK_REFINED):
        source, _, confidence, tool_result, response, selected_tools = run_langgraph_agent(
            "What is lead time?"
        )

    assert source == "tools: kanban_metrics"
    assert confidence == "high"
    assert selected_tools[0]["name"] == "kanban_metrics"
    assert "lead time" in tool_result.lower()
    assert len(response) > 0


def test_platform_route():
    route = ([{"name": "platform_engineering", "reason": "IDP question"}], "Platform match", "high")
    with patch("src.ai.langgraph_agent.choose_tools", return_value=route), \
         patch("src.ai.langgraph_agent.synthesize_step", return_value=MOCK_SYNTHESIS), \
         patch("src.ai.langgraph_agent.ask_model", return_value=MOCK_REFINED):
        source, _, confidence, tool_result, response, selected_tools = run_langgraph_agent(
            "What is an internal developer platform?"
        )

    assert source == "tools: platform_engineering"
    assert confidence == "high"
    assert selected_tools[0]["name"] == "platform_engineering"
    assert "platform" in tool_result.lower()
    assert len(response) > 0


# --- routing: multi-tool path ---

def test_multi_tool_selection():
    route = (
        [
            {"name": "terraform_analyzer", "reason": "IaC risk"},
            {"name": "cicd_pipeline_reviewer", "reason": "pipeline risk"},
        ],
        "Two tools matched",
        "high",
    )
    with patch("src.ai.langgraph_agent.choose_tools", return_value=route), \
         patch("src.ai.langgraph_agent.synthesize_step", return_value=MOCK_SYNTHESIS), \
         patch("src.ai.langgraph_agent.ask_model", return_value=MOCK_REFINED):
        _, _, confidence, _, response, selected_tools = run_langgraph_agent(
            "Analyze Terraform and CI/CD pipeline risks"
        )

    tool_names = [tool["name"] for tool in selected_tools]
    assert "terraform_analyzer" in tool_names
    assert "cicd_pipeline_reviewer" in tool_names
    assert confidence == "high"
    assert len(response) > 0


# --- routing: fallback path ---

def test_fallback_path():
    route = ([], "No tool matched", "low")
    with patch("src.ai.langgraph_agent.choose_tools", return_value=route), \
         patch("src.ai.langgraph_agent.ask_model", return_value=MOCK_FALLBACK):
        _, _, confidence, _, response, selected_tools = run_langgraph_agent(
            "Tell me a joke about software engineering"
        )

    assert selected_tools == []
    assert confidence in ["low", "medium"]
    assert len(response) > 0


# --- routing: PR tool with sample file output ---

def test_pr_tool():
    route = ([{"name": "pr_infra_summarizer", "reason": "PR summary request"}], "PR match", "high")
    with patch("src.ai.langgraph_agent.choose_tools", return_value=route), \
         patch("src.ai.langgraph_agent.synthesize_step", return_value=MOCK_SYNTHESIS), \
         patch("src.ai.langgraph_agent.ask_model", return_value=MOCK_REFINED):
        _, _, confidence, tool_result, response, selected_tools = run_langgraph_agent(
            "Summarize this infrastructure pull request"
        )

    assert selected_tools[0]["name"] == "pr_infra_summarizer"
    assert "security group" in tool_result.lower() or "s3" in tool_result.lower()
    assert confidence == "high"
    assert len(response) > 0
