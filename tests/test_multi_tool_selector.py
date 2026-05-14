import json
from unittest.mock import patch
from src.ai.multi_tool_selector import choose_tools

MOCK_TEMPLATE = "tools: {tool_descriptions}\ninput: {user_input}\nnames: {valid_tool_names}"


def _model_response(**kwargs) -> str:
    return json.dumps(kwargs)


def _patch(model_response: str):
    return patch("src.ai.multi_tool_selector.ask_model", return_value=model_response), \
           patch("src.ai.multi_tool_selector.load_prompt", return_value=MOCK_TEMPLATE)


# --- happy path ---

def test_choose_tools_returns_two_valid_tools():
    response = _model_response(
        tools=[
            {"name": "terraform_analyzer", "reason": "IaC risk"},
            {"name": "cicd_pipeline_reviewer", "reason": "pipeline risk"},
        ],
        reason="Two tools matched",
        confidence="high",
    )
    with patch("src.ai.multi_tool_selector.ask_model", return_value=response), \
         patch("src.ai.multi_tool_selector.load_prompt", return_value=MOCK_TEMPLATE):
        tools, reason, confidence = choose_tools("analyze terraform and pipeline")

    assert len(tools) == 2
    assert tools[0]["name"] == "terraform_analyzer"
    assert tools[1]["name"] == "cicd_pipeline_reviewer"
    assert confidence == "high"
    assert reason == "Two tools matched"


def test_choose_tools_returns_single_valid_tool():
    response = _model_response(
        tools=[{"name": "kanban_metrics", "reason": "asked about lead time"}],
        reason="One tool matched",
        confidence="high",
    )
    with patch("src.ai.multi_tool_selector.ask_model", return_value=response), \
         patch("src.ai.multi_tool_selector.load_prompt", return_value=MOCK_TEMPLATE):
        tools, reason, confidence = choose_tools("what is lead time?")

    assert len(tools) == 1
    assert tools[0]["name"] == "kanban_metrics"
    assert tools[0]["reason"] == "asked about lead time"


# --- edge cases ---

def test_choose_tools_filters_unknown_tool_names():
    response = _model_response(
        tools=[
            {"name": "nonexistent_tool", "reason": "hallucinated"},
            {"name": "kanban_metrics", "reason": "real tool"},
        ],
        reason="mixed",
        confidence="high",
    )
    with patch("src.ai.multi_tool_selector.ask_model", return_value=response), \
         patch("src.ai.multi_tool_selector.load_prompt", return_value=MOCK_TEMPLATE):
        tools, _, _ = choose_tools("some prompt")

    assert len(tools) == 1
    assert tools[0]["name"] == "kanban_metrics"


def test_choose_tools_caps_at_two_tools():
    response = _model_response(
        tools=[
            {"name": "kanban_metrics", "reason": "a"},
            {"name": "terraform_analyzer", "reason": "b"},
            {"name": "cicd_pipeline_reviewer", "reason": "c"},
        ],
        reason="three tools",
        confidence="high",
    )
    with patch("src.ai.multi_tool_selector.ask_model", return_value=response), \
         patch("src.ai.multi_tool_selector.load_prompt", return_value=MOCK_TEMPLATE):
        tools, _, _ = choose_tools("big question")

    assert len(tools) == 2


def test_choose_tools_deduplicates_repeated_tool():
    response = _model_response(
        tools=[
            {"name": "kanban_metrics", "reason": "first"},
            {"name": "kanban_metrics", "reason": "duplicate"},
        ],
        reason="repeated",
        confidence="high",
    )
    with patch("src.ai.multi_tool_selector.ask_model", return_value=response), \
         patch("src.ai.multi_tool_selector.load_prompt", return_value=MOCK_TEMPLATE):
        tools, _, _ = choose_tools("lead time again")

    assert len(tools) == 1
    assert tools[0]["name"] == "kanban_metrics"


def test_choose_tools_normalizes_invalid_confidence_to_low():
    response = _model_response(
        tools=[{"name": "kanban_metrics", "reason": "ok"}],
        reason="odd confidence",
        confidence="very_sure",
    )
    with patch("src.ai.multi_tool_selector.ask_model", return_value=response), \
         patch("src.ai.multi_tool_selector.load_prompt", return_value=MOCK_TEMPLATE):
        _, _, confidence = choose_tools("prompt")

    assert confidence == "low"


def test_choose_tools_skips_non_dict_items_in_tools_list():
    response = _model_response(
        tools=["not_a_dict", {"name": "kanban_metrics", "reason": "valid"}],
        reason="mixed types",
        confidence="high",
    )
    with patch("src.ai.multi_tool_selector.ask_model", return_value=response), \
         patch("src.ai.multi_tool_selector.load_prompt", return_value=MOCK_TEMPLATE):
        tools, _, _ = choose_tools("prompt")

    assert len(tools) == 1
    assert tools[0]["name"] == "kanban_metrics"


# --- invalid / missing input ---

def test_choose_tools_invalid_json_returns_empty_and_low():
    with patch("src.ai.multi_tool_selector.ask_model", return_value="not json at all"), \
         patch("src.ai.multi_tool_selector.load_prompt", return_value=MOCK_TEMPLATE):
        tools, reason, confidence = choose_tools("any prompt")

    assert tools == []
    assert reason == "Model did not return valid JSON."
    assert confidence == "low"


def test_choose_tools_tools_field_not_a_list_returns_empty():
    response = _model_response(tools="kanban_metrics", reason="wrong shape", confidence="high")
    with patch("src.ai.multi_tool_selector.ask_model", return_value=response), \
         patch("src.ai.multi_tool_selector.load_prompt", return_value=MOCK_TEMPLATE):
        tools, reason, confidence = choose_tools("any prompt")

    assert tools == []
    assert reason == "Model did not return a valid tools list."
    assert confidence == "low"
