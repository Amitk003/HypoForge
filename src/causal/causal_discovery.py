import pandas as pd
import numpy as np
import networkx as nx
from typing import Optional
from src.state import CausalGraphData, CausalEdge


def build_correlation_dag(df: pd.DataFrame, threshold: float = 0.3) -> CausalGraphData:
    num_df = df.select_dtypes(include=[np.number])
    if num_df.shape[1] < 2:
        return CausalGraphData()

    corr = num_df.corr().abs()
    nodes = num_df.columns.tolist()
    edges = []

    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            if corr.iloc[i, j] >= threshold:
                if corr.iloc[i, j] > 0:
                    source = nodes[i] if num_df[nodes[i]].std() < num_df[nodes[j]].std() else nodes[j]
                    target = nodes[j] if source == nodes[i] else nodes[i]
                    edges.append(CausalEdge(source=source, target=target))

    dot_lines = ["digraph CausalDAG {"]
    for e in edges:
        dot_lines.append(f'  "{e.source}" -> "{e.target}";')
    dot_lines.append("}")

    return CausalGraphData(
        nodes=nodes,
        edges=edges,
        dot_source="\n".join(dot_lines),
    )


def build_graph_from_data(df: pd.DataFrame, method: str = "correlation") -> CausalGraphData:
    if method == "correlation":
        return build_correlation_dag(df)
    return CausalGraphData()


def get_graphviz_dag(cg: CausalGraphData) -> nx.DiGraph:
    G = nx.DiGraph()
    for node in cg.nodes:
        G.add_node(node)
    for edge in cg.edges:
        G.add_edge(edge.source, edge.target)
    return G
