import streamlit as st 
import json
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import plotly.express as px
from streamlit_extras.metric_cards import style_metric_cards

# ==================================================
# CONFIGURATION
# ==================================================
st.set_page_config(
    page_title="Graph-CoT | Raisonnement sur graphes",
    page_icon="🧠",
    layout="wide"
)

# ==================================================
# DESIGN LIGHT (INCHANGÉ)
# ==================================================
st.markdown("""<style>
:root {
    --primary: #4f8cff;
    --secondary: #8b5cf6;
    --accent: #22d3ee;
    --bg-main: #f8fafc;
    --glass: rgba(255,255,255,0.78);
    --border-soft: rgba(0,0,0,0.05);
    --text-main: #0f172a;
}
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(circle at 15% 20%, #e0f2fe, transparent 40%),
        radial-gradient(circle at 85% 80%, #ede9fe, transparent 40%),
        linear-gradient(180deg, #f8fafc, #eef2ff);
    font-family: 'Inter', 'Segoe UI', sans-serif;
    color: var(--text-main);
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #ffffff, #f1f5f9);
    border-right: 1px solid var(--border-soft);
    box-shadow: 8px 0 25px rgba(0,0,0,0.04);
}
h1 {
    font-size: 3rem;
    font-weight: 900;
    background: linear-gradient(90deg, var(--primary), var(--secondary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
</style>""", unsafe_allow_html=True)

# ==================================================
# CHARGEMENT DES DONNÉES
# ==================================================
with open("results/standard.json") as f:
    standard = json.load(f)

with open("results/graph_cot.json") as f:
    graph_cot = json.load(f)

# ==================================================
# MÉTRIQUES
# ==================================================
def compute_metrics(data):
    total = len(data)
    correct = sum(1 for x in data if x["prediction"] == x["ground_truth"])
    incorrect = total - correct
    accuracy = correct / total
    return accuracy, correct, incorrect

std_acc, std_correct, std_incorrect = compute_metrics(standard)
cot_acc, cot_correct, cot_incorrect = compute_metrics(graph_cot)

# ==================================================
# SIDEBAR
# ==================================================
with st.sidebar:
    st.title("🧠 Graph-CoT")
    st.markdown("**Raisonnement sur graphes dirigés**")
    st.divider()
    task = st.selectbox(
        "📌 Tâche",
        ["lc210 – Cycle Detection", "lc797 – Path Finding", "Reachability"]
    )
    method = st.radio(
        "⚙️ Méthode",
        ["Standard Prompt", "Graph-CoT"]
    )

# ==================================================
# EN-TÊTE
# ==================================================
st.title("Amélioration du raisonnement sur graphes dans les grands modèles de langage (LLM) via Graph Chain-of-Thought")
st.markdown("""
Ce tableau de bord compare **Standard Prompting** et **Graph-CoT**
pour le raisonnement structuré sur des **graphes dirigés**,
en utilisant une analyse quantitative et qualitative.
""")

# ==================================================
# KPI
# ==================================================
st.subheader("📊 Performance globale")
c1, c2, c3 = st.columns(3)
c1.metric("Accuracy – Standard", f"{std_acc:.3f}")
c2.metric("Accuracy – Graph-CoT", f"{cot_acc:.3f}")
c3.metric("Gain relatif", f"+{(cot_acc - std_acc)*100:.1f}%")
style_metric_cards()

# ==================================================
# GRAPHIQUE 1
# ==================================================
st.subheader("📈 Comparaison des accuracies")
df_acc = pd.DataFrame({
    "Méthode": ["Standard", "Graph-CoT"],
    "Accuracy": [std_acc, cot_acc]
})
fig1 = px.bar(
    df_acc,
    x="Méthode",
    y="Accuracy",
    color="Méthode",
    text="Accuracy"
)
fig1.update_layout(yaxis=dict(range=[0, 1]))
st.plotly_chart(fig1, use_container_width=True)

# ==================================================
# GRAPHIQUE 2
# ==================================================
st.subheader("📊 Raisonnements corrects vs incorrects")
df_ci = pd.DataFrame({
    "Méthode": ["Standard", "Graph-CoT"],
    "Correct": [std_correct, cot_correct],
    "Incorrect": [std_incorrect, cot_incorrect]
})
fig2 = px.bar(
    df_ci,
    x="Méthode",
    y=["Correct", "Incorrect"],
    barmode="stack",
    text_auto=True
)
st.plotly_chart(fig2, use_container_width=True)

# ==================================================
# TABLEAU
# ==================================================
st.subheader("📋 Tableau récapitulatif")
st.dataframe(pd.DataFrame({
    "Méthode": ["Standard", "Graph-CoT"],
    "Accuracy": [std_acc, cot_acc],
    "Correct": [std_correct, cot_correct],
    "Incorrect": [std_incorrect, cot_incorrect]
}), use_container_width=True)

# ==================================================
# FONCTION EXPLICATION
# ==================================================
def explain_prediction(task, edges, selected, method):
    explanation = f"**Tâche :** {task}\n\n"
    explanation += f"- **Graphe considéré :** {edges}\n"
    explanation += f"- **Méthode utilisée :** {method}\n"
    explanation += f"- **Ground Truth :** {selected['ground_truth']}\n"
    explanation += f"- **Prediction :** {selected['prediction']}\n"

    # Verdict du modèle avec HTML color
    if selected["prediction"] == selected["ground_truth"]:
        explanation += "- **Verdict du modèle :** <span style='color:#16a34a; font-weight:700;'>Correct</span> ✅\n"
    else:
        explanation += "- **Verdict du modèle :** <span style='color:#dc2626; font-weight:700;'>Incorrect</span> ❌\n"

    G = nx.DiGraph()
    G.add_edges_from(edges)

    # ----- lc210 -----
    if task == "lc210 – Cycle Detection":
        cycles = list(nx.simple_cycles(G))
        explanation += (
            f"- **Réalité du graphe :** "
            f"{'le graphe contient le(s) cycle(s) ' + str(cycles) if cycles else 'le graphe ne contient aucun cycle'}\n"
        )
        if str(selected['ground_truth']).lower() in ["yes", "true", "1"]:
            explanation += "- **Ground Truth attendu :** le graphe doit contenir un cycle\n"
        else:
            explanation += "- **Ground Truth attendu :** le graphe ne doit pas contenir de cycle\n"

    # ----- lc797 -----
    elif task == "lc797 – Path Finding":
        target_node = max(G.nodes)
        path_exists = nx.has_path(G, 0, target_node)
        explanation += (
            f"- **Réalité du graphe :** "
            f"{'il existe un chemin' if path_exists else 'aucun chemin n’existe'} "
            f"entre le noeud 0 et le noeud {target_node}\n"
        )
        if str(selected['ground_truth']).lower() in ["yes", "true", "1"]:
            explanation += "- **Ground Truth attendu :** un chemin doit exister\n"
        else:
            explanation += "- **Ground Truth attendu :** aucun chemin ne doit exister\n"

    # ----- Reachability -----
    elif task == "Reachability":
        strongly_connected = nx.is_strongly_connected(G)
        explanation += (
            f"- **Réalité du graphe :** "
            f"{'tous les noeuds ne sont pas atteignables entre eux' if strongly_connected else 'les noeuds sont  tous atteignables entre eux'}\n"
        )
        if str(selected['ground_truth']).lower() in ["yes", "true", "1"]:
            explanation += "- **Ground Truth attendu :** le graphe doit être fortement connecté\n"
        else:
            explanation += "- **Ground Truth attendu :** le graphe ne doit pas être fortement connecté\n"

    return explanation

# ==================================================
# ANALYSE QUALITATIVE
# ==================================================
st.subheader("🔍 Analyse qualitative du raisonnement")
idx = st.slider("Sélectionner un exemple", 0, len(graph_cot) - 1, 0)
selected = graph_cot[idx] if method == "Graph-CoT" else standard[idx]

edges = (
    [(0, 1), (1, 2), (2, 0)]
    if task == "lc210 – Cycle Detection"
    else [(0, 1), (1, 3), (3, 4)]
)

G = nx.DiGraph()
G.add_edges_from(edges)

fig, ax = plt.subplots(figsize=(3.5, 3.5))
nx.draw(
    G,
    with_labels=True,
    node_color="#93c5fd",
    edge_color="#6366f1",
    node_size=650,
    font_size=11,
    ax=ax
)
st.pyplot(fig)

cA, cB, cC = st.columns(3)
cA.success(f"Ground Truth : {selected['ground_truth']}")
cB.info(f"Prédiction ({method}) : {selected['prediction']}")
if selected["prediction"] == selected["ground_truth"]:
    cC.markdown("<span style='color:#16a34a; font-weight:700;'>Correct</span>", unsafe_allow_html=True)
else:
    cC.markdown("<span style='color:#dc2626; font-weight:700;'>Incorrect</span>", unsafe_allow_html=True)

# 🔹 **IMPORTANT** : unsafe_allow_html=True ajouté ici
st.markdown("### 💡 Explication automatique")
st.markdown(explain_prediction(task, edges, selected, method), unsafe_allow_html=True)

# ==================================================
# FOOTER
# ==================================================
st.divider()
st.caption("Université Internationale de Rabat — 2026")
