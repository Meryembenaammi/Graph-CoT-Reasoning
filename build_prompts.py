import json
import os

INPUT_DIR = "GraphEval36K_processed"
OUTPUT_DIR = "prompts"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def build_prompt(sample):
    return f"""You are given a directed graph.

Graph:
{sample['graph_text']}

Question:
{sample['question']}

Think step by step and provide the final answer.
"""

tasks = ["lc210", "lc797", "reachability"]

for task in tasks:
    input_path = os.path.join(INPUT_DIR, task, "data.json")
    output_path = os.path.join(OUTPUT_DIR, f"{task}_prompts.json")

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    prompts = []
    for sample in data:
        prompts.append({
            "prompt": build_prompt(sample),
            "answer": sample["answer"]
        })

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(prompts, f, indent=2)

    print(f"{task}: prompts generated ({len(prompts)} samples)")
