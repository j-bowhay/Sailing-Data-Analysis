from dataclasses import dataclass

import streamlit as st
import matplotlib.pyplot as plt
from matplotlib import ticker

from analysis._get_data import get_regattas, get_races, get_start_data, get_mark_data
from analysis._utils import hide_streamlit


def no_start_data():
    st.error("No starting data available for this regatta/race.")
    st.stop()


st.set_page_config(
    page_title="Sailing Data Analysis: Startline Analysis",
    page_icon="⛵",
)
hide_streamlit()

st.markdown("# Startline Analysis")
st.write("""Highlight where the top `x` sailors by windward mark position started.""")

regatta = st.selectbox("Select Regatta:", get_regattas()["name"])

race = st.selectbox("Select race:", get_races(regatta))

mark_number = st.number_input("Top `x` at windward mark to highlight:", value=10)

start_data = get_start_data(regatta, race)

if start_data is None:
    no_start_data()

ww_mark_data = get_mark_data(regatta, race)["bywaypoint"][1]["markpassings"]

try:
    line_lenght = start_data["startline"]["lengthInMeters"]
except KeyError:
    no_start_data()


@dataclass
class Competitor:
    name: str
    dist_from_strb: float
    dist_from_line: float
    ww_time: int


competitors = []

for c in start_data["competitors"]:
    for ww_pos in ww_mark_data:
        if ww_pos["competitor"]["name"] == c["competitor"]["name"]:
            competitors.append(
                Competitor(
                    name=c["competitor"]["name"],
                    dist_from_strb=c["distanceToStarboardSideOfStartLineInMeters"],
                    dist_from_line=c["distanceToStartLineAtStartOfRaceInMeters"],
                    ww_time=ww_pos["timeasmillis"],
                )
            )

competitors.sort(key=lambda x: x.ww_time)

fig, ax = plt.subplots()
ax.plot(0, 0, "k*", markersize=15)
ax.plot(-line_lenght, 0, "k*", markersize=15)
for i, c in enumerate(competitors):
    if i < mark_number:
        ax.plot(-c.dist_from_strb, 0, "g.")
    else:
        ax.plot(-c.dist_from_strb, 0, "r.")
ax.set_axis_off()
st.pyplot(fig)

st.write("With distance to line:")

fig, ax = plt.subplots()
ax.plot(0, 0, "k*", markersize=15)
ax.plot(-line_lenght, 0, "k*", markersize=15)
for i, c in enumerate(competitors):
    if i < mark_number:
        ax.plot(-c.dist_from_strb, -c.dist_from_line, "g.")
    else:
        ax.plot(-c.dist_from_strb, -c.dist_from_line, "r.")
ax.set_ylabel("Distance from line [m]")
ax.set_xlabel("Distance from Starboard End [m]")
ax.set_xticklabels(
    [label.get_text().replace("−", "") for label in ax.get_xticklabels()]
)
st.pyplot(fig)
