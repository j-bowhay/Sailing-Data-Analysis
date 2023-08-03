import streamlit as st
import time
import numpy as np

st.set_page_config(
    page_title="Sailing Data Analysis: Startline Analysis",
    page_icon="⛵",
)

st.markdown("# Startline Analysis")
st.write(
    """Highlight where the top `x`% started on the start line."""
)
