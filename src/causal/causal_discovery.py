import pandas as pd
import numpy as np
from typing import Optional
from src.state import CausalGraphData, CausalEdge

try:
    import networkx as nx
except ImportError:
    nx = None


def calculate_partial_correlation(df: pd.DataFrame, x: str, y: str, z_list: list[str]) -> float:
    """Calculates partial correlation between x and y controlling for z_list using precision matrix / residuals."""
    if not z_list:
        return float(df[x].corr(df[y]))
    try:
        cols = [x, y] + z_list
        sub_df = df[cols].dropna()
        if len(sub_df) < len(cols) + 2:
            return float(df[x].corr(df[y]))
        cov = sub_df.cov()
        precision = np.linalg.pinv(cov.values)
        r_xy = -precision[0, 1] / np.sqrt(abs(precision[0, 0] * precision[1, 1]))
        return float(r_xy) if not np.isnan(r_xy) else 0.0
    except Exception:
        return float(df[x].corr(df[y]))


def build_correlation_dag(df: pd.DataFrame, threshold: float = 0.3) -> CausalGraphData:
    num_df = df.select_dtypes(include=[np.number]).dropna()
    if num_df.shape[1] < 2:
        return CausalGraphData()

    nodes = num_df.columns.tolist()
    corr = num_df.corr()
    edges = []

    # Identify potential skeleton edges with strong correlation
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            r_val = corr.iloc[i, j]
            if abs(r_val) >= threshold:
                n1, n2 = nodes[i], nodes[j]
                
                # Check partial correlation controlling for other features to remove indirect pseudo-correlations
                other_nodes = [n for n in nodes if n not in (n1, n2)]
                p_corr = calculate_partial_correlation(num_df, n1, n2, other_nodes[:3])
                
                if abs(p_corr) >= threshold * 0.5:
                    # Orient edge using variance ratio heuristic.
                    # In additive noise models, the cause tends to have lower variance
                    # than the effect. This is a simple proxy for directionality.
                    var1 = num_df[n1].var()
                    var2 = num_df[n2].var()
                    ratio = var1 / var2 if var2 > 0 else 1.0
                    
                    if ratio < 0.8:
                        src, tgt = n1, n2
                    elif ratio > 1.2:
                        src, tgt = n2, n1
                    else:
                        src, tgt = n1, n2

                    edges.append(CausalEdge(
                        source=src,
                        target=tgt,
                        edge_type="directed",
                        weight=round(float(p_corr), 3)
                    ))

    dot_lines = ["digraph CausalDAG {", '  node [shape=ellipse, style=filled, fillcolor="#1E293B", fontcolor="#E2E8F0"];']
    for e in edges:
        dot_lines.append(f'  "{e.source}" -> "{e.target}" [label="{e.weight}", color="#38BDF8"];')
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


def get_graphviz_dag(cg: CausalGraphData):
    if nx is None:
        return None
    G = nx.DiGraph()
    for node in cg.nodes:
        G.add_node(node)
    for edge in cg.edges:
        G.add_edge(edge.source, edge.target, weight=edge.weight)
    return G


