from src.ai.router import route_request
from src.ai.tool_registry import list_tools

user_input = input("Enter your prompt: ")

if user_input.lower() == "list tools":
    response = list_tools()
    source = "local: tool_registry"
else:
    source, response = route_request(user_input)

print(f"\nSource: {source}\n")
print("Response:\n")
print(response)

with open("interactions.log", "a") as f:
    f.write("USER INPUT:\n")
    f.write(user_input + "\n\n")
    f.write("SOURCE:\n")
    f.write(source + "\n\n")
    f.write("RESPONSE:\n")
    f.write(response + "\n")
    f.write("\n-----------------------------\n\n")