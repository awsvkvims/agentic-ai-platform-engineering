from src.ai.langgraph_agent import get_graph

graph = get_graph()
mermaid = graph.get_graph().draw_mermaid()

with open("docs/langgraph_diagram.md", "w") as f:
    f.write("# LangGraph Diagram\n\n")
    f.write("```mermaid\n")
    f.write(mermaid)
    f.write("\n```\n")

print("Wrote docs/langgraph_diagram.md")

