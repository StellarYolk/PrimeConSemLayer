from typing import Any


def validate_react_flow_payload(data: dict[str, Any]) -> bool:
    if "nodes" not in data or "edges" not in data:
        return False
    if not isinstance(data["nodes"], list) or not isinstance(data["edges"], list):
        return False
    for node in data["nodes"]:
        if not all(k in node for k in ("id", "position", "data")):
            return False
        if not isinstance(node["position"], dict):
            return False
        if "x" not in node["position"] or "y" not in node["position"]:
            return False
    for edge in data["edges"]:
        if not all(k in edge for k in ("id", "source", "target")):
            return False
    return True


def validate_chart_config(config: dict[str, Any]) -> bool:
    required = ("chart_type", "x_key", "y_key", "data")
    return all(k in config for k in required) and isinstance(config["data"], list)
