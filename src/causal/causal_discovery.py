import pandas as pd
import numpy as np
from typing import Optional
from itertools import combinations
from src.state import CausalGraphData, CausalEdge

try:
    import networkx as nx
except ImportError:
    nx = None

def calculate_partial_correlation(df: pd.DataFrame, x: str, y: str, z_list: list[str]) -> float:
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


def partial_corr_significant(df: pd.DataFrame, x: str, y: str, z_list: list[str], alpha: float = 0.05) -> bool:
    r = calculate_partial_correlation(df, x, y, z_list)
    n = len(df.dropna(subset=[x, y] + z_list))
    df_reg = n - len(z_list) - 3
    if df_reg < 1:
        return abs(r) > 0.5
    t_stat = abs(r) * np.sqrt(df_reg / (1 - r * r))
    from scipy.stats import t
    p_val = 2 * (1 - t.cdf(t_stat, df_reg))
    return p_val < alpha


def build_pc_skeleton(df: pd.DataFrame, alpha: float = 0.05) -> tuple[list[str], set[tuple[str, str]], dict]:
    nodes = df.select_dtypes(include=[np.number]).columns.tolist()
    if len(nodes) < 2:
        return nodes, set(), {}

    n = len(nodes)
    adj = {v: set(nodes) - {v} for v in nodes}
    sep_sets = {}
    depth = 0

    while True:
        changed = False
        for i in range(n):
            for j in range(i + 1, n):
                vi, vj = nodes[i], nodes[j]
                if vj not in adj[vi]:
                    continue
                neighbors = list(adj[vi] - {vj})
                if depth > len(neighbors):
                    continue
                found_sep = False
                for z_set in combinations(neighbors, depth):
                    z_list = list(z_set)
                    if not partial_corr_significant(df, vi, vj, z_list, alpha):
                        adj[vi].discard(vj)
                        adj[vj].discard(vi)
                        sep_sets[(vi, vj)] = z_list
                        sep_sets[(vj, vi)] = z_list
                        found_sep = True
                        changed = True
                        break
                if not found_sep and depth > 0:
                    fwd_neighbors = list(adj[vj] - {vi})
                    if depth <= len(fwd_neighbors):
                        for z_set in combinations(fwd_neighbors, depth):
                            z_list = list(z_set)
                            if not partial_corr_significant(df, vi, vj, z_list, alpha):
                                adj[vi].discard(vj)
                                adj[vj].discard(vi)
                                sep_sets[(vi, vj)] = z_list
                                sep_sets[(vj, vi)] = z_list
                                changed = True
                                break
        if not changed:
            depth += 1
            if depth > 2:
                break

    skeleton = set()
    for vi in nodes:
        for vj in adj[vi]:
            if vi < vj:
                skeleton.add((vi, vj))
    return nodes, skeleton, sep_sets


def orient_edges(nodes: list[str], skeleton: set, sep_sets: dict, df: pd.DataFrame) -> list[CausalEdge]:
    edges = []
    adjacency = {v: set() for v in nodes}
    for vi, vj in skeleton:
        adjacency[vi].add(vj)
        adjacency[vj].add(vi)

    # Step 1: identify v-structures (colliders)
    v_structures = set()
    for vi in nodes:
        for vj in adjacency[vi]:
            for vk in adjacency[vj]:
                if vi != vk and vi not in adjacency[vk] and vk not in adjacency[vi]:
                    sep_set = sep_sets.get((vi, vk), sep_sets.get((vk, vi), None))
                    if sep_set is not None and vj not in sep_set:
                        v_structures.add((vi, vj))
                        v_structures.add((vj, vk))

    oriented = set(v_structures)

    # Step 2: propagate directions using Meek rules
    changed = True
    while changed:
        changed = False
        for vi in nodes:
            for vj in adjacency[vi]:
                if (vi, vj) in oriented and (vj, vi) not in oriented:
                    for vk in adjacency[vj]:
                        if vk == vi or (vj, vk) in oriented or (vk, vj) in oriented:
                            continue
                        if (vi, vk) not in oriented and (vk, vi) not in oriented:
                            if vk not in adjacency[vi]:
                                oriented.add((vj, vk))
                                changed = True

    # Build edge list from oriented + remaining undirected
    if df is None:
        return edges
    for vi in nodes:
        for vj in adjacency[vi]:
            if vi < vj:
                if (vi, vj) in oriented:
                    src, tgt = vi, vj
                elif (vj, vi) in oriented:
                    src, tgt = vj, vi
                else:
                    var1 = df[vi].var()
                    var2 = df[vj].var()
                    ratio = var1 / var2 if var2 > 0 else 1.0
                    if ratio < 0.8:
                        src, tgt = vi, vj
                    else:
                        src, tgt = vj, vi
                    oriented.add((src, tgt))
                pcorr = calculate_partial_correlation(df, src, tgt, [])
                edges.append(CausalEdge(
                    source=src, target=tgt, edge_type="directed",
                    weight=round(float(pcorr), 3),
                ))
    return edges


def identify_confounders_and_mediators(nodes: list[str], edges: list[CausalEdge]) -> tuple[list[str], list[str]]:
    parents = {v: [] for v in nodes}
    children = {v: [] for v in nodes}
    for e in edges:
        parents[e.target].append(e.source)
        children[e.source].append(e.target)

    confounders = []
    mediators = []
    for v in nodes:
        if len(parents[v]) >= 2:
            confounders.extend(parents[v])
        if len(parents[v]) >= 1 and len(children[v]) >= 1:
            mediators.append(v)
    confounders = list(set(confounders))
    mediators = list(set(mediators))
    return confounders, mediators


def build_pc_dag(df: pd.DataFrame, alpha: float = 0.05) -> CausalGraphData:
    nodes, skeleton, sep_sets = build_pc_skeleton(df, alpha)
    edges = orient_edges(nodes, skeleton, sep_sets, df)
    confounders, mediators = identify_confounders_and_mediators(nodes, edges)

    dot_lines = ["digraph CausalDAG {", '  node [shape=ellipse, style=filled, fillcolor="#1E293B", fontcolor="#E2E8F0"];']
    for e in edges:
        dot_lines.append(f'  "{e.source}" -> "{e.target}" [label="{e.weight}", color="#38BDF8"];')
    if confounders:
        conf_str = " ".join([f'"{c}"' for c in confounders])
        dot_lines.append(f'  {{rank = same; {conf_str}}};')
    dot_lines.append("}")

    return CausalGraphData(
        nodes=nodes, edges=edges, confounders=confounders,
        mediators=mediators, dot_source="\n".join(dot_lines),
    )



def build_correlation_dag(df: pd.DataFrame, threshold: float = 0.3) -> CausalGraphData:
    num_df = df.select_dtypes(include=[np.number]).dropna()
    if num_df.shape[1] < 2:
        return CausalGraphData()
    nodes = num_df.columns.tolist()
    corr = num_df.corr()
    edges = []
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            r_val = corr.iloc[i, j]
            if abs(r_val) >= threshold:
                n1, n2 = nodes[i], nodes[j]
                other_nodes = [n for n in nodes if n not in (n1, n2)]
                p_corr = calculate_partial_correlation(num_df, n1, n2, other_nodes[:3])
                if abs(p_corr) >= threshold * 0.5:
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
                        source=src, target=tgt, edge_type="directed",
                        weight=round(float(p_corr), 3),
                    ))
    # Identify confounders from the resulting graph
    parents = {v: [] for v in nodes}
    for e in edges:
        parents[e.target].append(e.source)
    confounders = list(set([p for v in parents for p in parents[v] if len(parents[v]) >= 2]))
    mediators = [v for v in nodes if any(e.target == v for e in edges) and any(e.source == v for e in edges)]

    dot_lines = ["digraph CausalDAG {", '  node [shape=ellipse, style=filled, fillcolor="#1E293B", fontcolor="#E2E8F0"];']
    for e in edges:
        dot_lines.append(f'  "{e.source}" -> "{e.target}" [label="{e.weight}", color="#38BDF8"];')
    dot_lines.append("}")
    return CausalGraphData(
        nodes=nodes, edges=edges, confounders=confounders,
        mediators=mediators, dot_source="\n".join(dot_lines),
    )


def build_graph_from_data(df: pd.DataFrame, method: str = "pc", alpha: float = 0.05) -> CausalGraphData:
    if method == "correlation":
        return build_correlation_dag(df)
    return build_pc_dag(df, alpha=alpha)


def get_graphviz_dag(cg: CausalGraphData):
    if nx is None:
        return None
    G = nx.DiGraph()
    for node in cg.nodes:
        G.add_node(node)
    for edge in cg.edges:
        G.add_edge(edge.source, edge.target, weight=edge.weight)
    return G
