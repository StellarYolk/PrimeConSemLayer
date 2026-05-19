from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional, Any
from app.agents.sap_data_agent import sap_data_agent_execute
from app.agents.process_mining_agent import process_mining_agent_execute
from app.agents.rca_agent import rca_agent_execute
from app.agents.ui_agent import ui_agent_format


class AgentState(TypedDict):
    query: str
    intent: str
    result: Optional[dict[str, Any]]
    formatted_response: Optional[dict[str, Any]]


def classify_intent(state: AgentState) -> AgentState:
    query = state["query"].lower()
    process_keywords = ["process", "flow", "cycle", "bottleneck", "mining", "discover", "conformance"]
    rca_keywords = ["why", "root cause", "spike", "anomaly", "decrease", "increase", "deviation", "issue"]
    if any(kw in query for kw in process_keywords):
        state["intent"] = "process_mining"
    elif any(kw in query for kw in rca_keywords):
        state["intent"] = "rca"
    else:
        state["intent"] = "data_query"
    return state


def route_to_agent(state: AgentState) -> str:
    return state["intent"]


def execute_data_query(state: AgentState) -> AgentState:
    result = sap_data_agent_execute(state["query"])
    state["result"] = result
    return state


def execute_process_mining(state: AgentState) -> AgentState:
    result = process_mining_agent_execute(state["query"])
    state["result"] = result
    return state


def execute_rca(state: AgentState) -> AgentState:
    result = rca_agent_execute(state["query"])
    state["result"] = result
    return state


def format_response(state: AgentState) -> AgentState:
    formatted = ui_agent_format(state["result"], state["intent"])
    state["formatted_response"] = formatted
    return state


def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("classify", classify_intent)
    graph.add_node("data_agent", execute_data_query)
    graph.add_node("process_mining_agent", execute_process_mining)
    graph.add_node("rca_agent", execute_rca)
    graph.add_node("format", format_response)

    graph.set_entry_point("classify")
    graph.add_conditional_edges(
        "classify",
        route_to_agent,
        {
            "data_query": "data_agent",
            "process_mining": "process_mining_agent",
            "rca": "rca_agent",
        },
    )
    graph.add_edge("data_agent", "format")
    graph.add_edge("process_mining_agent", "format")
    graph.add_edge("rca_agent", "format")
    graph.add_edge("format", END)

    return graph.compile()


orchestrator = build_graph()
