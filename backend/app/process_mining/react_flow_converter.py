import networkx as nx
from typing import Optional


def dfg_to_react_flow(dfg: dict, start_activities: set, end_activities: set) -> dict:
    G = nx.DiGraph()
    for (source, target), frequency in dfg.items():
        G.add_edge(source, target, weight=frequency)

    pos = _hierarchical_layout(G, start_activities)

    nodes = []
    node_ids = {}
    idx = 0
    for node in G.nodes():
        node_id = f"node-{idx}"
        node_ids[node] = node_id
        is_start = node in start_activities
        is_end = node in end_activities
        node_type = "start" if is_start else ("end" if is_end else "activity")
        total_in = sum(dfg.get((s, node), 0) for s in G.predecessors(node))
        total_out = sum(dfg.get((node, t), 0) for t in G.successors(node))
        frequency = max(total_in, total_out, 1)
        nodes.append({
            "id": node_id,
            "type": "custom",
            "position": {"x": pos[node][0], "y": pos[node][1]},
            "data": {
                "label": node,
                "frequency": frequency,
                "node_type": node_type,
            },
        })
        idx += 1

    edges = []
    edge_idx = 0
    for (source, target), frequency in dfg.items():
        if source in node_ids and target in node_ids:
            edges.append({
                "id": f"edge-{edge_idx}",
                "source": node_ids[source],
                "target": node_ids[target],
                "label": str(frequency),
                "animated": True,
                "style": {"strokeWidth": max(1, min(frequency / 10, 4))},
            })
            edge_idx += 1

    return {"nodes": nodes, "edges": edges}


def _hierarchical_layout(G: nx.DiGraph, start_activities: set) -> dict:
    levels = {}
    queue = list(start_activities)
    visited = set()
    level = 0
    while queue:
        next_queue = []
        for node in queue:
            if node in visited:
                continue
            visited.add(node)
            levels[node] = level
            for successor in G.successors(node):
                if successor not in visited:
                    next_queue.append(successor)
        queue = next_queue
        level += 1

    for node in G.nodes():
        if node not in levels:
            levels[node] = level

    level_groups = {}
    for node, lvl in levels.items():
        level_groups.setdefault(lvl, []).append(node)

    pos = {}
    x_spacing = 220
    y_spacing = 140
    for lvl, nodes_in_level in sorted(level_groups.items()):
        y = lvl * y_spacing
        total_width = (len(nodes_in_level) - 1) * x_spacing
        start_x = -total_width / 2
        for i, node in enumerate(nodes_in_level):
            pos[node] = (start_x + i * x_spacing, y)

    return pos
