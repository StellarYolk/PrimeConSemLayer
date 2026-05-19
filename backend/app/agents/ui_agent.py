from typing import Any


def ui_agent_format(result: dict, intent: str) -> dict[str, Any]:
    if not result:
        return {"answer": "No results found.", "chart": None}

    if result.get("type") == "data":
        return {
            "answer": result.get("answer", ""),
            "chart": _build_chart_from_data(result.get("data", [])),
            "raw_data": result.get("data", []),
        }

    if result.get("type") == "process_mining":
        return {
            "answer": result.get("answer", ""),
            "nodes": result.get("nodes", []),
            "edges": result.get("edges", []),
            "metrics": result.get("metrics", {}),
        }

    if result.get("type") == "rca":
        rca_data = result.get("data", {})
        return {
            "answer": result.get("answer", ""),
            "rca": rca_data,
        }

    return {
        "answer": result.get("answer", ""),
        "chart": None,
    }


def _build_chart_from_data(data: list[dict]) -> dict[str, Any]:
    if not data:
        return {"chart_type": "bar", "x_key": "", "y_key": "", "title": "", "data": []}
    keys = list(data[0].keys())
    if len(keys) >= 2:
        return {
            "chart_type": "bar",
            "x_key": keys[0],
            "y_key": keys[1] if len(keys) > 1 else keys[0],
            "title": "Data Overview",
            "data": data[:10],
        }
    return {"chart_type": "bar", "x_key": keys[0] if keys else "", "y_key": "", "title": "", "data": data[:10]}
