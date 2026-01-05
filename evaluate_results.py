import json
import os

def evaluate(predictions):
    total = len(predictions)
    correct = 0
    incorrect = 0
    valid = 0

    for p in predictions:
        if p["prediction"] in ["Yes", "No"]:
            valid += 1
            if p["prediction"] == p["ground_truth"]:
                correct += 1
            else:
                incorrect += 1

    accuracy = correct / total
    success_rate = valid / total

    return accuracy, success_rate, correct, incorrect


for setting in ["standard", "graph_cot"]:
    path = f"results/{setting}.json"

    with open(path, "r") as f:
        preds = json.load(f)

    acc, sr, correct, incorrect = evaluate(preds)

    print(f"{setting.upper()} RESULTS")
    print(f"Accuracy: {acc:.3f}")
    print(f"Success Rate: {sr:.3f}")
    print(f"Correct reasoning: {correct}")
    print(f"Incorrect reasoning: {incorrect}")
    print("-" * 30)
results = {}

for setting in ["standard", "graph_cot"]:
    path = f"results/{setting}.json"

    with open(path, "r") as f:
        preds = json.load(f)

    acc, sr, correct, incorrect = evaluate(preds)

    results[setting] = {
        "accuracy": acc,
        "success_rate": sr,
        "correct": correct,
        "incorrect": incorrect
    }

with open("analysis/metrics.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)
