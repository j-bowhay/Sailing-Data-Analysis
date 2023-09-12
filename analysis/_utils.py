import json

import streamlit as st
import pandas as pd
import requests

@st.cache_resource
def get_regattas():
    return pd.json_normalize(
        json.loads(
            requests.get("http://www.sapsailing.com/sailingserver/api/v1/regattas").text
        )
    )

@st.cache_resource
def get_races(regatta):
    data = json.loads(
            requests.get(f"http://www.sapsailing.com/sailingserver/api/v1/regattas/{regatta}/races").text
    )
    
    if len(data["races"]) > 0:
        return [race["name"].strip() for race in data["races"]]
    else:
        return [regatta]
