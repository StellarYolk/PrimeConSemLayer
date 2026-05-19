from typing import Any
from app.process_mining.event_log import generate_sample_event_log
from app.process_mining.discovery import discover_dfg
from app.process_mining.react_flow_converter import dfg_to_react_flow


def process_mining_agent_execute(query: str) -> dict[str, Any]:
    query_lower = query.lower()
    process_type = "order-to-cash"
    if "procure" in query_lower or "p2p" in query_lower or "purchase" in query_lower:
        process_type = "procure-to-pay"
    elif "record" in query_lower or "r2r" in query_lower or "financial" in query_lower:
        process_type = "record-to-report"

    event_log = generate_sample_event_log(process_type, num_cases=50)
    dfg, start_activities, end_activities = discover_dfg(event_log)
    react_flow_data = dfg_to_react_flow(dfg, start_activities, end_activities)

    metrics = {
        "num_cases": len(event_log["case_id"].unique()),
        "num_events": len(event_log),
        "num_activities": len(event_log["activity"].unique()),
        "process_type": process_type,
    }

    return {
        "type": "process_mining",
        "nodes": react_flow_data["nodes"],
        "edges": react_flow_data["edges"],
        "metrics": metrics,
        "answer": f"Discovered {process_type} process flow with {metrics['num_cases']} cases and {metrics['num_activities']} activities.",
    }
