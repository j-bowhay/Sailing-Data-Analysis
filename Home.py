import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Sailing Data Analysis Tools")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    A collection of tools for analysing data from sailing regattas.
    
    The following regatta are available through SAP Sailing:
"""
)