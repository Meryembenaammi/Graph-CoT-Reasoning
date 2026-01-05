import json
import os

INPUT_DIR = "prompts"
OUTPUT_DIR = "prompts_structured"

os.makedirs(OUTPUT_DIR, exist_ok=True)

for file in os.listdir(INPUT_DIR):
    if not file.endswith(".json"):
        continue

    with open(os.path.join(INPUT_DIR, file), "r", encoding="utf-8") as f:
        data = json.load(f)

    new_data = []

    for sample in data:
        new_sample = {
            "graph_text": sample["prompt"].split("Question:")[0].strip(),
            "question": sample["prompt"].split("Question:")[1].split("Step 1")[0].strip(),
            "steps": [
                "Identify all nodes and their outgoing edges.",
                "Explore paths starting from each node.",
                "Check if any path leads back to a previously visited node.",
                "If such a path exists, a cycle is present."
            ],
            "final_instruction": "Provide the final answer (Yes or No).",
            "answer": sample["answer"]
        }
        new_data.append(new_sample)

    out_path = os.path.join(OUTPUT_DIR, file)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(new_data, f, indent=2, ensure_ascii=False)

    print(f"{file} → structured format generated")
