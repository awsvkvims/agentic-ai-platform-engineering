from typing import TypedDict

from langgraph.graph import StateGraph, END

from src.ai.agent_steps import run_tool_step, synthesize_step
from src.ai.multi_tool_selector import choose_tools
from src.ai.client import ask_model


class AgentState(TypedDict):
    user_input: str
    selected_tools: list[str]
    current_tool_index: int
    reason: str
    confidence: str
    tool_result: str
    final_answer: str
    source: str


def select_tool_node(state: AgentState) -> AgentState:
    selected_tools, reason, confidence = choose_tools(state["user_input"])

    # guardrails
    if confidence != "high":
        selected_tools = []

    if len(selected_tools) > 2:
        selected_tools = selected_tools[:2]

    state["selected_tools"] = selected_tools
    state["current_tool_index"] = 0
    state["reason"] = reason
    state["confidence"] = confidence

    return state

def run_tool_node(state: AgentState) -> AgentState:
    if state["current_tool_index"] >= len(state["selected_tools"]):
        return state

    tool_info = state["selected_tools"][state["current_tool_index"]]
    tool_name = tool_info["name"]
    result = run_tool_step(tool_name)

    if state["tool_result"]:
        state["tool_result"] += "\n\n"
    state["tool_result"] += f"[{tool_name}]\n{result}"

    state["current_tool_index"] += 1

    return state

def should_continue_tools(state: AgentState) -> str:
    if state["current_tool_index"] < len(state["selected_tools"]):
        return "more_tools"
    return "synthesize"


def synthesize_node(state: AgentState) -> AgentState:
    first_pass = synthesize_step(state["user_input"], state["tool_result"])

    refinement_prompt = (
        "Refine the following answer to be clearer and more actionable:\n\n"
        f"{first_pass}"
    )

    final_answer = ask_model(refinement_prompt)

    selected_tools = [tool["name"] for tool in state["selected_tools"]]
    state["final_answer"] = final_answer
    state["source"] = f'tools: {", ".join(selected_tools)}'

    return state


def fallback_model_node(state: AgentState) -> AgentState:
    final_answer = ask_model(state["user_input"])
    state["final_answer"] = final_answer
    state["source"] = "model: openai"
    state["tool_result"] = ""
    return state


def should_use_tool(state: AgentState) -> str:
    if state["selected_tools"] and state["confidence"] == "high":
        return "use_tools"
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
        "use_tools": "run_tool",
        "fallback": "fallback_model",
    },
)

graph.set_entry_point("select_tool")

graph.add_conditional_edges(
    "select_tool",
    lambda s: "use_tools" if s["selected_tools"] and s["confidence"] == "high" else "fallback",
    {
        "use_tools": "run_tool",
        "fallback": "fallback_model",
    },
)

graph.add_conditional_edges(
    "run_tool",
    should_continue_tools,
    {
        "more_tools": "run_tool",
        "synthesize": "synthesize",
    },
)

graph.add_edge("synthesize", END)
graph.add_edge("fallback_model", END)

agent_graph = graph.compile()


def run_langgraph_agent(user_input: str) -> tuple[str, str, str, str, str]:
    result = agent_graph.invoke(
        {
           "user_input": user_input,
            "tselected_tools": [],
            "current_tool_index": 0,
            "reason": "",
            "confidence": "",
            "tool_result": "",
            "final_answer": "",
            "source": "",
        }
    )

    return (
        result.get("source", ""),
        result.get("reason", ""),
        result.get("confidence", ""),
        result.get("tool_result", ""),
        result.get("final_answer", ""),
        result.get("selected_tools", []),  # this is your list of dicts
    )
    
def get_graph():
    return agent_graph

