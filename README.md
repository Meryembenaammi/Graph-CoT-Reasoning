# Graph-CoT: Structured Reasoning over Graphs

This repository contains the implementation and evaluation of **Graph Chain-of-Thought (Graph-CoT)**,
a structured reasoning approach for Large Language Models on graph-based problems.

## Dataset

The dataset used in this project is based on directed graph benchmarks
(e.g., LC210, LC797, Reachability).

Due to its large size, the dataset is not stored directly in the GitHub repository.
It can be obtained from:

- GraphEval benchmark
- Custom generated directed graph datasets

The directory structure is expected to be:

dataset-main/
 └── data/
     └── directed/


## Tasks
- Cycle Detection (lc210)
- Path Finding (lc797)
- Reachability

## Methodology
- Graph encoding
- Structured Chain-of-Thought
- Comparative evaluation with standard prompting

## Results
Graph-CoT improves accuracy from **65.3%** to **83.5%** on GraphEval36K benchmarks.

## Demo
An interactive Streamlit dashboard is provided to visualize results and reasoning behavior.

## Author
Meryem Benaammi  
Université Internationale de Rabat  
2026
