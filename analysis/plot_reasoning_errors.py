import json
import matplotlib.pyplot as plt
import numpy as np

with open("analysis/metrics.json", "r") as f:
    metrics = json.load(f)

labels = ["Correct", "Incorrect"]
standard = [
    metrics["standard"]["correct"],
    metrics["standard"]["incorrect"]
]
graph_cot = [
    metrics["graph_cot"]["correct"],
    metrics["graph_cot"]["incorrect"]
]

x = np.arange(len(labels))
width = 0.35

plt.figure()
plt.bar(x - width/2, standard, width, label="Standard")
plt.bar(x + width/2, graph_cot, width, label="Graph-CoT")

plt.xticks(x, labels)
plt.ylabel("Number of samples")
plt.title("Reasoning Outcome Comparison")
plt.legend()

plt.savefig("analysis/reasoning_comparison.png")
plt.show()
