import jsonlines
import json
import os

input_path = "dataset-main/data/directed/lc797/sparse.jsonl"
output_path = "GraphEval36K_processed/reachability/data.json"

output_data = []

with jsonlines.open(input_path) as reader:
    for obj in reader:
        for category, content in obj.items():
            graphs = content["graphs"]
            labels = content["labels"]

            for g, label in zip(graphs, labels):
                sample = {
                    "graph": {
                        "edges": g
                    },
                    "question": "Can the target node be reached from the source node?",
                    "answer": "Yes" if label else "No"
                }
                output_data.append(sample)

os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2)

print(f"Reachability conversion done. Samples: {len(output_data)}")
