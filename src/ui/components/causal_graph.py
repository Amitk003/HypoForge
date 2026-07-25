import streamlit as st
from src.state import CausalGraphData


def render_graph(cg: CausalGraphData):
    st.subheader("Interactive Causal Graph (DAG)")
    try:
        from pyvis.network import Network
        net = Network(height="400px", width="100%", bgcolor="#FFFFFF", font_color="#0F172A")
        net.toggle_physics(True)
        net.set_options('{"physics": {"enabled": true, "stabilization": {"iterations": 100}}}')
        for node in cg.nodes:
            net.add_node(node, label=node, color="#1E293B", border="#38BDF8")
        for edge in cg.edges:
            label = str(edge.weight) if edge.weight else ""
            net.add_edge(edge.source, edge.target, title=label, color="#38BDF8", arrows="to")
        html = net.generate_html()
        st.components.v1.html(html, height=420)
    except Exception:
        if cg.dot_source:
            try:
                st.graphviz_chart(cg.dot_source)
            except Exception:
                st.code(cg.dot_source, language="dot")

    if cg.confounders:
        pills = "".join(
            f'<span class="pill pill--info">Confounder: {c}</span>'
            for c in cg.confounders
        )
        st.markdown(f'<div style="margin-top: 8px;">{pills}</div>', unsafe_allow_html=True)
    if cg.mediators:
        pills = "".join(
            f'<span class="pill pill--info">Mediator: {m}</span>'
            for m in cg.mediators
        )
        st.markdown(f'<div style="margin-top: 4px;">{pills}</div>', unsafe_allow_html=True)
