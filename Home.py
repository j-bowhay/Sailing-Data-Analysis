import json

import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title="Sailing Data Analysis",
    page_icon="⛵",
)

st.write("# Sailing Data Analysis Tools")

st.markdown(
    """
    A collection of tools for analysing data from sailing regattas.
    
    The following regattas are available through SAP Sailing:
"""
)


@st.cache_resource
def get_data():
    return pd.json_normalize(
        json.loads(
            requests.get("http://www.sapsailing.com/sailingserver/api/v1/regattas").text
        )
    )

regattas_data = get_data()

text_search = st.text_input("Search by regatta name:", value="")

m1 = regattas_data["name"].str.contains(text_search, case=False)

display_data = regattas_data[m1]

st.dataframe(
    display_data[["name", "boatclass"]],
    hide_index=True,
    use_container_width=True,
)
