import json
import os

INPUT_DIR = "GraphEval36K_processed"
OUTPUT_DIR = "prompts"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def graph_cot_template(sample, task):
    if task == "lc210":
        reasoning_steps = """
Step 1: Identify all nodes and their outgoing edges.
Step 2: Explore paths starting from each node.
Step 3: Check if any path leads back to a previously visited node.
Step 4: If such a path exists, a cycle is present.
"""
    elif task == "lc797":
        reasoning_steps = """
Step 1: Identify the source node and the target node.
Step 2: Explore all possible paths from the source.
Step 3: Check whether at least one path reaches the target.
"""
    else:  # reachability
        reasoning_steps = """
Step 1: Identify the source and target nodes.
Step 2: Traverse the graph starting from the source.
Step 3: Determine whether the target node is reachable.
"""

    return f"""You are given a directed graph.

Graph:
{sample['graph_text']}

Question:
{sample['question']}

{reasoning_steps}
Provide the final answer (Yes or No).
"""

tasks = ["lc210", "lc797", "reachability"]

for task in tasks:
    input_path = os.path.join(INPUT_DIR, task, "data.json")
    output_path = os.path.join(OUTPUT_DIR, f"{task}_graph_cot.json")

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    prompts = []
    for sample in data:
        prompts.append({
            "prompt": graph_cot_template(sample, task),
            "answer": sample["answer"]
        })

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(prompts, f, indent=2)

    print(f"{task}: Graph-CoT prompts generated ({len(prompts)} samples)")
