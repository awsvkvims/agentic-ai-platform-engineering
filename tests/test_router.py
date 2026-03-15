from src.ai.router import route_request


def test_kanban_route():
    source, response = route_request("What is lead time?")
    assert source == "tool: explain_kanban_metrics"
    assert "Lead Time" in response


def test_platform_route():
    source, response = route_request("What is an internal developer platform?")
    assert source == "tool: explain_platform_engineering"
    assert "Platform engineering" in response