import json
import matplotlib.pyplot as plt

# Charger les métriques
with open("analysis/metrics.json", "r") as f:
    metrics = json.load(f)

# Données du tableau
columns = ["Method", "Accuracy", "Success Rate", "Correct", "Incorrect"]
rows = [
    [
        "Standard",
        f"{metrics['standard']['accuracy']:.3f}",
        f"{metrics['standard']['success_rate']:.3f}",
        metrics["standard"]["correct"],
        metrics["standard"]["incorrect"]
    ],
    [
        "Graph-CoT",
        f"{metrics['graph_cot']['accuracy']:.3f}",
        f"{metrics['graph_cot']['success_rate']:.3f}",
        metrics["graph_cot"]["correct"],
        metrics["graph_cot"]["incorrect"]
    ]
]

# Création de la figure
fig, ax = plt.subplots(figsize=(8, 3))
ax.axis('off')

# Créer le tableau
table = ax.table(
    cellText=rows,
    colLabels=columns,
    loc='center',
    cellLoc='center'
)

# Style
table.auto_set_font_size(False)
table.set_fontsize(12)
table.scale(1, 1.8)

# Sauvegarde
plt.savefig("analysis/results_table.png", dpi=300, bbox_inches="tight")
plt.close()

print("✅ Tableau image généré : analysis/results_table.png")
