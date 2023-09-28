import streamlit as st

from analysis._get_data import get_regattas, get_races


def select_regatta():
    return st.selectbox("Select Regatta:", get_regattas()["name"])


def select_race(regatta):
    return st.selectbox("Select race:", get_races(regatta))
