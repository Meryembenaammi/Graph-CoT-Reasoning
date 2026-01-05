import json
import os

MAX_EXAMPLES = 5

files = {
    "standard": "results/standard.json",
    "graph_cot": "results/graph_cot.json"
}

categories = {
    "correct_standard": [],
    "incorrect_standard": [],
    "correct_graph_cot": [],
    "incorrect_graph_cot": []
}

for mode, path in files.items():
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for sample in data:
        gt = sample["ground_truth"]
        pred = sample["prediction"]

        if gt == pred:
            key = f"correct_{mode}"
        else:
            key = f"incorrect_{mode}"

        if len(categories[key]) < MAX_EXAMPLES:
            categories[key].append({
                "type": key,
                "ground_truth": gt,
                "prediction": pred,
                "comment": ""
            })

# Fusionner toutes les catégories
final_examples = []
for v in categories.values():
    final_examples.extend(v)

os.makedirs("analysis", exist_ok=True)
with open("analysis/reasoning_examples.json", "w", encoding="utf-8") as f:
    json.dump(final_examples, f, indent=2, ensure_ascii=False)

print("✅ reasoning_examples.json généré automatiquement")
