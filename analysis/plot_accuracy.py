import json
import matplotlib.pyplot as plt

with open("analysis/metrics.json", "r") as f:
    metrics = json.load(f)

methods = ["Standard", "Graph-CoT"]
accuracy = [
    metrics["standard"]["accuracy"],
    metrics["graph_cot"]["accuracy"]
]

plt.figure()
plt.bar(methods, accuracy)
plt.ylim(0, 1)
plt.ylabel("Accuracy")
plt.title("Accuracy Comparison")

plt.savefig("analysis/accuracy_comparison.png")
plt.show()
