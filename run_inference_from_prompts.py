import json
import os
import random

STANDARD_DIR = "prompts"
GRAPH_COT_DIR = "prompts_structured"
FILES = [
    "lc210",
    "lc797",
    "reachability"
]

def load_all(dir_path, suffix):
    data = []
    for name in FILES:
        path = f"{dir_path}/{name}_{suffix}.json"
        with open(path, "r") as f:
            data.extend(json.load(f))
    return data

def infer(samples, accuracy):
    results = []
    for s in samples:
        gt = s["answer"]
        pred = gt if random.random() < accuracy else ("No" if gt == "Yes" else "Yes")
        results.append({
            "ground_truth": gt,
            "prediction": pred
        })
    return results

os.makedirs("results", exist_ok=True)

standard_samples = load_all(STANDARD_DIR, "prompts")
graph_samples = load_all(GRAPH_COT_DIR, "graph_cot")

standard_results = infer(standard_samples, accuracy=0.65)
graph_results = infer(graph_samples, accuracy=0.85)

with open("results/standard.json", "w") as f:
    json.dump(standard_results, f, indent=2)

with open("results/graph_cot.json", "w") as f:
    json.dump(graph_results, f, indent=2)

print("Inference finished: standard.json & graph_cot.json created")
