import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

st.set_page_config(
    page_title="Ventec Industries – Tableau de Bord KPI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden; height: 0%; position: fixed;}
    .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }
    [data-testid="stAppViewContainer"] {
        padding: 0 !important;
        margin: 0 !important;
    }
    iframe {
        display: block;
        width: 100%;
        border: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

html_path = Path(__file__).parent / "index.html"
html_code = html_path.read_text(encoding="utf-8")

# IMPORTANT:
# Keep the iframe close to the browser viewport height.
# If the iframe is huge, CSS fixed elements such as modals and notifications
# are positioned relative to the full iframe height and may appear invisible.
components.html(
    html_code,
    height=930,
    scrolling=True
)
