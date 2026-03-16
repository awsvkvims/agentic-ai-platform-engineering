from src.ai.router import route_request


def test_kanban_route():
    source, reason, confidence, tool_result, response = route_request("What is lead time?")
    assert source == "tool: kanban_metrics"
    assert confidence == "high"
    assert "Lead Time" in tool_result
    assert len(response) > 0


def test_platform_route():
    source, reason, confidence, tool_result, response = route_request("What is an internal developer platform?")
    assert source == "tool: platform_engineering"
    assert confidence == "high"
    assert "Platform engineering" in tool_result
    assert len(response) > 0