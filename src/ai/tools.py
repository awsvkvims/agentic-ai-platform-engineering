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
