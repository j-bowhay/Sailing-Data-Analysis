import json
import re

import streamlit as st
import pandas as pd
import requests


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    """
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    """
    return [atoi(c) for c in re.split(r"(\d+)", text)]


@st.cache_resource
def get_regattas():
    return pd.json_normalize(
        json.loads(
            requests.get("http://www.sapsailing.com/sailingserver/api/v1/regattas").text
        )
    ).sort_values(by="name")


@st.cache_resource
def get_races(regatta):
    data = json.loads(
        requests.get(
            f"http://www.sapsailing.com/sailingserver/api/v1/regattas/{regatta}/races"
        ).text
    )

    if len(data["races"]) > 0:
        return sorted(
            [race["name"].strip() for race in data["races"]], key=natural_keys
        )
    else:
        return [regatta]


@st.cache_resource
def get_start_data(regatta, race):
    try:
        return json.loads(
            requests.get(
                f"https://www.sapsailing.com/sailingserver/api/v1/regattas/{regatta}/races/{race}/startanalysis"
            ).text
        )
    except json.JSONDecodeError:
        return None


@st.cache_resource
def get_mark_data(regatta, race):
    return json.loads(
        requests.get(
            f"https://www.sapsailing.com/sailingserver/api/v1/regattas/{regatta}/races/{race}/markpassings"
        ).text
    )


@st.cache_resource
def get_leg_data(regatta, race):
    return json.loads(
        requests.get(
            f"https://www.sapsailing.com/sailingserver/api/v1/regattas/{regatta}/races/{race}/competitors/legs"
        ).text
    )
