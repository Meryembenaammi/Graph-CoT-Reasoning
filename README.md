# Graph-CoT: Structured Reasoning over Graphs

## 📌 Overview

**Graph Chain-of-Thought (Graph-CoT)** is a structured reasoning framework designed to enhance the reasoning capabilities of Large Language Models (LLMs) on **graph-based problems**, particularly **directed graphs**.

Instead of relying on implicit or free-form reasoning, Graph-CoT introduces an **explicit, structured, and step-by-step reasoning process** that mirrors classical graph algorithms (DFS, BFS, topological traversal). This approach significantly improves model reliability, interpretability, and accuracy on graph reasoning tasks.

---

## 🎯 Motivation

Recent LLMs show strong performance in natural language tasks but struggle with:
- Multi-step logical reasoning
- Graph traversal and dependency tracking
- Avoiding hallucinated paths or cycles

Graph-CoT addresses these limitations by:
- Transforming raw graph structures into **textual structured representations**
- Guiding the model through **algorithm-inspired reasoning steps**
- Reducing reasoning shortcuts and logical errors

---

## 📂 Dataset

### Source
The dataset is derived from:
- **GraphEval benchmark**
- **Custom-generated directed graph datasets**
- Problems inspired by LeetCode-style graph challenges

### Tasks Covered
- **Cycle Detection** (LC210 – Course Schedule)
- **Path Finding** (LC797 – All Paths From Source to Target)
- **Reachability**

### Dataset Format
Due to its large size, the dataset is **not included** in this repository.

Expected directory structure:
dataset-main/
└── data/
└── directed/
├── lc210/
├── lc797/
└── reachability/

Each instance typically includes:
- Graph nodes and directed edges
- A natural language question
- Ground Truth answer (Yes / No or path)
- Structured reasoning annotation (Graph-CoT)

---

## 🧠 Methodology

### 1. Graph Encoding
Raw graph data (edge lists or adjacency lists) are transformed into:
- Structured textual representations
- Clear parent → child relationships
- Explicit node dependencies

### 2. Graph Chain-of-Thought (Graph-CoT)
The reasoning process is decomposed into:
- Step-by-step node exploration
- Explicit visited-node tracking
- Clear decision rules (cycle detected / path exists / unreachable)

This mirrors classical graph algorithms while remaining interpretable by LLMs.

### 3. Baseline Comparison
Graph-CoT is compared against:
- **Standard Prompting** (no explicit reasoning)
- Same model, same data, same evaluation protocol

---

## 📊 Evaluation & Results

### Benchmark
- **GraphEval36K**

### Accuracy
| Method               | Accuracy |
|----------------------|----------|
| Standard Prompting   | 65.3%    |
| **Graph-CoT**        | **83.5%** |

### Key Observations
- Significant reduction in false positives for cycle detection
- Improved consistency in path-finding tasks
- More faithful reasoning aligned with graph structure

---

## 🖥️ Demo & Visualization

An **interactive Streamlit dashboard** is provided to:
- Visualize graph instances
- Compare predictions vs ground truth
- Inspect reasoning steps produced by Graph-CoT
- Analyze common failure cases

To run the demo:
```bash
streamlit run streamlit_app.py
