from typing import Any
from app.rca.engine import analyze_rca
from app.rca.kpi_tracker import KPI_DEFINITIONS, get_kpi


def rca_agent_execute(query: str) -> dict[str, Any]:
    query_lower = query.lower()
    matched_kpi = None
    for kpi_id, kpi_def in KPI_DEFINITIONS.items():
        if any(word in query_lower for word in kpi_def["name"].lower().split()):
            matched_kpi = kpi_id
            break

    if not matched_kpi:
        for keyword in ["cycle", "procure", "order", "ar", "inventory", "po", "delivery", "invoice", "vendor", "production", "quality", "maverick", "budget", "cash", "backorder", "return", "compliance"]:
            for kpi_id in KPI_DEFINITIONS:
                if keyword in kpi_id:
                    matched_kpi = kpi_id
                    break
            if matched_kpi:
                break

    if matched_kpi:
        rca_result = analyze_rca(matched_kpi)
        return {
            "type": "rca",
            "data": rca_result,
            "answer": rca_result.get("summary", f"Root cause analysis completed for {matched_kpi}."),
        }

    return {
        "type": "general",
        "answer": f"Processed RCA query: '{query}'. Specify a KPI name for detailed root cause analysis.",
    }
