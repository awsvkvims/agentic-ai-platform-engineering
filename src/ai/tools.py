from src.ai.tool_definition import Tool

def explain_kanban_metrics():
    return """
Key Kanban flow metrics:

Cycle Time
The time from when work starts to when it finishes.

Lead Time
The time from when a request is made to when it is delivered.

Work In Progress (WIP)
The number of tasks currently in progress.

Throughput
The number of tasks completed in a time period.

These metrics help teams understand flow efficiency and identify bottlenecks.
"""

def explain_platform_engineering():
	return """
Platform engineering is the practice of building and operating internal developer platforms that help teams deliver software more safely, quickly, and consistently.

It usually includes capabilities such as self-service infrastructure, CI/CD templates, golden paths, developer portals, governance guardrails, and reusable automation.

The goal is to improve developer experience while increasing standardization, reliability, and operational efficiency.

"""

def explain_pi_planning_dependencies():
    return """
In SAFe PI Planning, dependencies are relationships where one team or work item relies on another team to deliver something first or in coordination.

Common dependency types include:
- feature sequencing dependencies
- shared platform or infrastructure dependencies
- external vendor or compliance dependencies
- integration dependencies across teams

Managing dependencies well helps reduce delivery risk, improve coordination, and expose blockers early during PI execution.
"""
def summarize_backlog_risk():
    return """
A backlog may show delivery risk when it contains too many large items, unclear priorities, unresolved dependencies, blocked work, or too much work in progress at the same time.

Common warning signs include:
- oversized stories or features
- many items marked blocked
- dependencies across teams
- weak acceptance criteria
- high WIP and low throughput

A useful first response is to split large items, clarify priorities, reduce WIP, and make dependencies visible early.
"""

def analyze_backlog_items(backlog_text: str) -> str:
    lines = [line.strip() for line in backlog_text.splitlines() if line.strip()]

    blocked_items = [line for line in lines if "blocked" in line.lower()]
    in_progress_items = [line for line in lines if "in progress" in line.lower()]
    large_items = [line for line in lines if "too large" in line.lower() or "spans multiple teams" in line.lower()]
    unclear_items = [line for line in lines if "unclear" in line.lower()]

    results = []
    results.append("Backlog analysis summary:")
    results.append(f"- Total items: {len(lines)}")
    results.append(f"- Blocked items: {len(blocked_items)}")
    results.append(f"- In progress items: {len(in_progress_items)}")
    results.append(f"- Large or cross-team items: {len(large_items)}")
    results.append(f"- Unclear ownership or requirements items: {len(unclear_items)}")

    if blocked_items:
        results.append("")
        results.append("Blocked items:")
        for item in blocked_items:
            results.append(f"- {item}")

    if large_items:
        results.append("")
        results.append("Large or cross-team items:")
        for item in large_items:
            results.append(f"- {item}")

    if unclear_items:
        results.append("")
        results.append("Items needing clarification:")
        for item in unclear_items:
            results.append(f"- {item}")

    results.append("")
    results.append("Recommended actions:")
    results.append("- Reduce blocked work by resolving ownership and review delays")
    results.append("- Split large items into smaller deliverables")
    results.append("- Limit concurrent work in progress where possible")
    results.append("- Clarify ownership and acceptance criteria early")

    return "\n".join(results)





kanban_metrics_tool = Tool(
    name="kanban_metrics",
    description="Explain key Kanban flow metrics such as lead time, cycle time, throughput, and WIP.",
    func=explain_kanban_metrics,
)

platform_engineering_tool = Tool(
    name="platform_engineering",
    description="Use this only when the user is asking for a definition or explanation of platform engineering or internal developer platforms. Do not use it for Terraform generation, CI/CD generation, or implementation tasks.",
    func=explain_platform_engineering,
)

pi_planning_dependencies_tool = Tool(
    name="pi_planning_dependencies",
    description="Explain SAFe PI Planning dependencies and why they matter.",
    func=explain_pi_planning_dependencies,
)

backlog_risk_tool = Tool(
    name="backlog_risk",
    description="Use this when the user asks about backlog risk, delivery risk in a backlog, blocked backlog items, or signs that a backlog may be unhealthy.",
    func=summarize_backlog_risk,
)

backlog_analysis_tool = Tool(
    name="backlog_analysis",
    description="Use this when the user asks about analyzing backlog items, backlog health, or delivery risks in backlog work.",
    func=analyze_backlog_items,
)
