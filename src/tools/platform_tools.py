
from src.ai.tool_definition import Tool

def explain_platform_engineering():
	return """
Platform engineering is the practice of building and operating internal developer platforms that help teams deliver software more safely, quickly, and consistently.

It usually includes capabilities such as self-service infrastructure, CI/CD templates, golden paths, developer portals, governance guardrails, and reusable automation.

The goal is to improve developer experience while increasing standardization, reliability, and operational efficiency.

"""

platform_engineering_tool = Tool(
    name="platform_engineering",
    description="Use this only when the user is asking for a definition or explanation of platform engineering or internal developer platforms. Do not use it for Terraform generation, CI/CD generation, or implementation tasks.",
    func=explain_platform_engineering,
)
