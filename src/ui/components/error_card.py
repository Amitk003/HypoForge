import streamlit as st


def render_errors(errors: list[str]):
    if errors:
        with st.expander(f"Warnings / Errors"):
            for err in errors:
                st.warning(err.split("\n")[0])
