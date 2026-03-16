from src.ai.router import route_request
from src.ai.tool_registry import list_tools, get_tool_descriptions

user_input = input("Enter your prompt: ")

if user_input.lower() == "list tools":
    source = "local: tool_registry"
    tool_result = ""
    response = list_tools()
elif user_input.lower() == "show tool descriptions":
    source = "local: tool_registry"
    tool_result = ""
    response = get_tool_descriptions()
else:
    source, tool_result, response = route_request(user_input)

print(f"\nSource: {source}\n")
print("Response:\n")
print(response)

with open("interactions.log", "a") as f:
    f.write("USER INPUT:\n")
    f.write(user_input + "\n\n")
    f.write("SOURCE:\n")
    f.write(source + "\n\n")
    if tool_result:
        f.write("TOOL RESULT:\n")
        f.write(tool_result + "\n\n")
    f.write("RESPONSE:\n")
    f.write(response + "\n")
    f.write("\n-----------------------------\n\n")