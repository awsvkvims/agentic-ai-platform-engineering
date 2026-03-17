from src.ai.langgraph_agent import run_langgraph_agent
from src.ai.tool_registry import list_tools, get_tool_descriptions

user_input = input("Enter your prompt: ")

if user_input.lower() == "help":
    source = "local: help"
    reason = ""
    confidence = ""
    tool_result = ""
    response = """Available commands:
- help
- list tools
- show tool descriptions
- analyze backlog

Or ask a normal question, such as:
- What is lead time?
- What are signs that a backlog may have delivery risk?
- How should I analyze backlog items for delivery risk?
- What is an internal developer platform?
"""

elif user_input.lower() == "list tools":
    source = "local: tool_registry"
    reason = ""
    confidence = ""
    tool_result = ""
    response = list_tools()
elif user_input.lower() == "show tool descriptions":
    source = "local: tool_registry"
    reason = ""
    confidence = ""
    tool_result = ""
    response = get_tool_descriptions()
elif user_input.lower() == "analyze backlog":
    source = "local: backlog_file"
    reason = ""
    confidence = ""
    with open("samples/backlog/sample_backlog.txt", "r") as f:
        tool_result = f.read()
    response = tool_result
elif user_input.lower() == "analyze terraform":
    source = "local: terraform_file"
    reason = ""
    confidence = ""
    with open("samples/terraform/sample_terraform.tf", "r") as f:
        tool_result = f.read()
    response = tool_result
elif user_input.lower() == "analyze pipeline":
    source = "local: pipeline_file"
    reason = ""
    confidence = ""
    with open("samples/pipeline/sample_pipeline.yml", "r") as f:
        tool_result = f.read()
    response = tool_result
else:
    source, reason, confidence, tool_result, response = run_langgraph_agent(user_input)

print(f"\nSource: {source}")
if confidence:
    print(f"Confidence: {confidence}")
if reason:
    print(f"Reason: {reason}")
print("\nResponse:\n")
print(response)

with open("logs/interactions.log", "a") as f:
    f.write("USER INPUT:\n")
    f.write(user_input + "\n\n")
    f.write("SOURCE:\n")
    f.write(source + "\n\n")
    if confidence:
        f.write("CONFIDENCE:\n")
        f.write(confidence + "\n\n")
    if reason:
        f.write("REASON:\n")
        f.write(reason + "\n\n")
    if tool_result:
        f.write("TOOL RESULT:\n")
        f.write(tool_result + "\n\n")
    f.write("RESPONSE:\n")
    f.write(response + "\n")
    f.write("\n-----------------------------\n\n")