from src.ai.router import route_request

test_inputs = [
    "What is lead time?",
    "What is an internal developer platform?",
    "Explain PI planning dependencies",
    "What are signs that a backlog may have delivery risk?",
    "How should I analyze backlog items for delivery risk?",
    "How can AI help generate Terraform modules?",
]

for user_input in test_inputs:
    source, reason, confidence, tool_result, response = route_request(user_input)

    print("=" * 80)
    print(f"INPUT: {user_input}")
    print(f"SOURCE: {source}")
    print(f"CONFIDENCE: {confidence}")
    print(f"REASON: {reason}")
    print("RESPONSE:")
    print(response)
    print()

