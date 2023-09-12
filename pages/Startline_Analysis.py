import streamlit as st

from analysis._utils import get_regattas, get_races

st.set_page_config(
    page_title="Sailing Data Analysis: Startline Analysis",
    page_icon="⛵",
)

st.markdown("# Startline Analysis")
st.write(
    """Highlight where the top `x` sailors by windward mark position started."""
)

regatta = st.selectbox("Select Regatta:", get_regattas()["name"])

st.selectbox("Select race:", get_races(regatta))