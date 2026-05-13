from src.ai.langgraph_agent import run_langgraph_agent

test_inputs = [
    "What is lead time?",
    "What is an internal developer platform?",
    "Explain PI planning dependencies",
    "What are signs that a backlog may have delivery risk?",
    "How should I analyze backlog items for delivery risk?",
    "How can AI help generate Terraform modules?",
    "Analyze this Terraform for security and best practice risks",
    "Review this CI/CD pipeline for delivery risks",
    "Summarize this infrastructure pull request",
    "Analyze Terraform and CI/CD pipeline risks",
]

for user_input in test_inputs:
    source, reason, confidence, tool_result, response, selected_tools = run_langgraph_agent(user_input)

    print("=" * 80)
    print(f"INPUT: {user_input}")
    print(f"SOURCE: {source}")
    print(f"CONFIDENCE: {confidence}")
    print(f"REASON: {reason}")

    if selected_tools:
        print("SELECTED TOOLS:")
        for tool in selected_tools:
            print(f"- {tool['name']}: {tool['reason']}")

    if tool_result:
        print("TOOL RESULT:")
        print(tool_result[:500])
        if len(tool_result) > 500:
            print("...")

    print("RESPONSE:")
    print(response)
    print()