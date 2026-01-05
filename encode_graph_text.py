import json
from collections import defaultdict

def edges_to_text(edges):
    adj = defaultdict(list)
    nodes = set()

    # Sécurité : vérifier que edges est bien une liste de paires
    for edge in edges:
        if not isinstance(edge, list):
            continue
        if len(edge) != 2:
            continue

        u, v = edge
        adj[u].append(v)
        nodes.add(u)
        nodes.add(v)

    # Cas graphe vide
    if not nodes:
        return "Graph has no edges."

    text_lines = []
    for node in sorted(nodes):
        neighbors = adj[node] if node in adj else []
        text_lines.append(f"Node {node} -> {neighbors}")

    return "\n".join(text_lines)


tasks = ["lc210", "lc797", "reachability"]

for task in tasks:
    path = f"GraphEval36K_processed/{task}/data.json"

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for sample in data:
        edges = sample["graph"]["edges"]
        sample["graph_text"] = edges_to_text(edges)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"{task}: graph encoding added successfully")
