from src.tools.agile_tools import (
    explain_kanban_metrics,
    explain_pi_planning_dependencies,
    summarize_backlog_risk,
    analyze_backlog_items,
)


# --- explain_kanban_metrics ---

def test_kanban_metrics_returns_all_four_metrics():
    result = explain_kanban_metrics()
    assert "cycle time" in result.lower()
    assert "lead time" in result.lower()
    assert "throughput" in result.lower()
    assert "work in progress" in result.lower() or "wip" in result.lower()


def test_kanban_metrics_returns_non_empty_string():
    result = explain_kanban_metrics()
    assert isinstance(result, str)
    assert len(result.strip()) > 0


def test_kanban_metrics_mentions_flow_or_bottleneck():
    result = explain_kanban_metrics()
    assert "flow" in result.lower() or "bottleneck" in result.lower()


# --- explain_pi_planning_dependencies ---

def test_pi_planning_returns_dependency_types():
    result = explain_pi_planning_dependencies()
    assert "dependency" in result.lower() or "dependencies" in result.lower()


def test_pi_planning_returns_non_empty_string():
    result = explain_pi_planning_dependencies()
    assert isinstance(result, str)
    assert len(result.strip()) > 0


def test_pi_planning_mentions_risk_or_coordination():
    result = explain_pi_planning_dependencies()
    assert "risk" in result.lower() or "coordination" in result.lower()


# --- summarize_backlog_risk ---

def test_backlog_risk_returns_warning_signs():
    result = summarize_backlog_risk()
    assert "blocked" in result.lower() or "wip" in result.lower() or "large" in result.lower()


def test_backlog_risk_returns_non_empty_string():
    result = summarize_backlog_risk()
    assert isinstance(result, str)
    assert len(result.strip()) > 0


def test_backlog_risk_includes_recommended_actions():
    result = summarize_backlog_risk()
    assert "split" in result.lower() or "reduce" in result.lower() or "clarify" in result.lower()


# --- analyze_backlog_items ---

def test_analyze_backlog_items_counts_blocked_and_in_progress():
    backlog = "Feature A - blocked\nFeature B - in progress\nFeature C - done"
    result = analyze_backlog_items(backlog)
    assert "- Blocked items: 1" in result
    assert "- In progress items: 1" in result
    assert "- Total items: 3" in result


def test_analyze_backlog_items_detects_large_and_unclear_items():
    backlog = "Feature X - too large to deliver\nFeature Y - spans multiple teams\nFeature Z - unclear ownership"
    result = analyze_backlog_items(backlog)
    assert "- Large or cross-team items: 2" in result
    assert "- Unclear ownership or requirements items: 1" in result


def test_analyze_backlog_items_empty_string_returns_zero_counts():
    result = analyze_backlog_items("")
    assert "- Total items: 0" in result
    assert "- Blocked items: 0" in result
    assert "- In progress items: 0" in result
