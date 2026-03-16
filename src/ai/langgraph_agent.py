from typing import TypedDict

from langgraph.graph import StateGraph, END

from src.ai.agent_steps import select_tool_step, run_tool_step, synthesize_step
from src.ai.client import ask_model


class AgentState(TypedDict):
    user_input: str
    tool_name: str
    reason: str
    confidence: str
    tool_result: str
    final_answer: str
    source: str


def select_tool_node(state: AgentState) -> AgentState:
    tool_name, reason, confidence = select_tool_step(state["user_input"])

    state["tool_name"] = tool_name
    state["reason"] = reason
    state["confidence"] = confidence

    return state


def run_tool_node(state: AgentState) -> AgentState:
    tool_result = run_tool_step(state["tool_name"])
    state["tool_result"] = tool_result
    return state


def synthesize_node(state: AgentState) -> AgentState:
    final_answer = synthesize_step(state["user_input"], state["tool_result"])
    state["final_answer"] = final_answer
    state["source"] = f'tool: {state["tool_name"]}'
    return state


def fallback_model_node(state: AgentState) -> AgentState:
    final_answer = ask_model(state["user_input"])
    state["final_answer"] = final_answer
    state["source"] = "model: openai"
    state["tool_result"] = ""
    return state


def should_use_tool(state: AgentState) -> str:
    if state["tool_name"] != "none" and state["confidence"] == "high":
        return "use_tool"
    return "fallback"


graph = StateGraph(AgentState)

graph.add_node("select_tool", select_tool_node)
graph.add_node("run_tool", run_tool_node)
graph.add_node("synthesize", synthesize_node)
graph.add_node("fallback_model", fallback_model_node)

graph.set_entry_point("select_tool")

graph.add_conditional_edges(
    "select_tool",
    should_use_tool,
    {
        "use_tool": "run_tool",
        "fallback": "fallback_model",
    },
)

graph.add_edge("run_tool", "synthesize")
graph.add_edge("synthesize", END)
graph.add_edge("fallback_model", END)

agent_graph = graph.compile()


def run_langgraph_agent(user_input: str) -> tuple[str, str, str, str, str]:
    result = agent_graph.invoke(
        {
            "user_input": user_input,
            "tool_name": "",
            "reason": "",
            "confidence": "",
            "tool_result": "",
            "final_answer": "",
            "source": "",
        }
    )

    return (
        result["source"],
        result["reason"],
        result["confidence"],
        result["tool_result"],
        result["final_answer"],
    )
    
def get_graph():
    return agent_graph

