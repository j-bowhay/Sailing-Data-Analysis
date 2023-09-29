from dataclasses import dataclass

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker
from scipy.stats import linregress

from analysis._get_data import get_regattas, get_races, get_start_data, get_mark_data
from analysis._utils import hide_streamlit
from analysis._selection import select_regatta, select_race


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

regatta = select_regatta()

race = select_race(regatta)

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
    speed_start: float


competitors = []

for c in start_data["competitors"]:
    for ww_pos in ww_mark_data:
        if ww_pos["competitor"]["name"] == c["competitor"]["name"]:
            competitors.append(
                Competitor(
                    name=c["competitor"]["name"],
                    dist_from_strb=c["distanceToStarboardSideOfStartLineInMeters"],
                    dist_from_line=c["distanceToStartLineAtStartOfRaceInMeters"],
                    speed_start=c["speedOverGroundAtStartOfRaceInKnots"],
                    ww_time=ww_pos["timeasmillis"],
                )
            )

ww_sorted_competitior = sorted(competitors, key=lambda x: x.ww_time)

st.header("Bias")
st.write(
    f"Biased end is {start_data['startline']['favoredEnd'].lower()}"
    f" by {start_data['startline']['biasInMeters']}m over a "
    f"{start_data['startline']['lengthInMeters']}m long line."
)

st.header("Start Line Distribution")

fig, ax = plt.subplots()
ax.set_title("Distribution along start line")
ax.plot(0, 0, "k*", markersize=15)
ax.plot(-line_lenght, 0, "k*", markersize=15)
for i, c in enumerate(ww_sorted_competitior):
    if i < mark_number:
        ax.plot(-c.dist_from_strb, 0, "g.", zorder=3)
    else:
        ax.plot(-c.dist_from_strb, 0, "r.")
ax.get_yaxis().set_visible(False)
ax.set_xlabel("Distance from Starboard End [m]")
ax.set_xticks(ax.get_xticks().tolist())
ax.set_xticklabels(
    [label.get_text().replace("−", "") for label in ax.get_xticklabels()]
)
st.pyplot(fig)

x = []
y = []
fig, ax = plt.subplots()
for i, c in enumerate(ww_sorted_competitior):
    x.append(c.dist_from_strb)
    y.append(i + 1)

result_pos = linregress(x, y)

ax.plot(
    x, result_pos.intercept + result_pos.slope * np.asarray(x), "r-", label="Best Fit"
)
ax.plot(x, y, "k.", label="Data")
ax.legend()

ax.set_xlabel("Distance from Starboard End [m]")
ax.set_ylabel("Windward Mark Position")
st.pyplot(fig)
st.write(f"R = {result_pos.rvalue}, p-value = {result_pos.pvalue}")


st.header("Speed At Go")

fig, ax = plt.subplots()
ax.plot(0, 0, "k*", markersize=15)
ax.plot(-line_lenght, 0, "k*", markersize=15)
for i, c in enumerate(ww_sorted_competitior):
    if i < mark_number:
        ax.plot(-c.dist_from_strb, c.speed_start, "g.", zorder=3)
    else:
        ax.plot(-c.dist_from_strb, c.speed_start, "r.")
ax.set_ylabel("Speed at go [knots]")
ax.set_xlabel("Distance from Starboard End [m]")
ax.set_xticks(ax.get_xticks().tolist())
ax.set_xticklabels(
    [label.get_text().replace("−", "") for label in ax.get_xticklabels()]
)
st.pyplot(fig)

fig, ax = plt.subplots()
x = []
for i, c in enumerate(ww_sorted_competitior):
    x.append(c.speed_start)

result_speed = linregress(x, y)

ax.plot(
    x,
    result_speed.intercept + result_speed.slope * np.asarray(x),
    "r-",
    label="Best Fit",
)
ax.plot(x, y, "k.", label="Data")
ax.legend()

ax.set_xlabel("Speed at go [knots]")
ax.set_ylabel("Windward Mark Position")
st.pyplot(fig)
st.write(f"R = {result_speed.rvalue}, p-value = {result_speed.pvalue}")

st.header("Distance to Line:")

fig, ax = plt.subplots()
ax.plot(0, 0, "k*", markersize=15)
ax.plot(-line_lenght, 0, "k*", markersize=15)
for i, c in enumerate(ww_sorted_competitior):
    if i < mark_number:
        ax.plot(-c.dist_from_strb, -c.dist_from_line, "g.", zorder=3)
    else:
        ax.plot(-c.dist_from_strb, -c.dist_from_line, "r.")
ax.set_ylabel("Distance from line [m]")
ax.set_xlabel("Distance from Starboard End [m]")
ax.set_xticks(ax.get_xticks().tolist())
ax.set_xticklabels(
    [label.get_text().replace("−", "") for label in ax.get_xticklabels()]
)
st.pyplot(fig)

fig, ax = plt.subplots()
x = []
for i, c in enumerate(ww_sorted_competitior):
    x.append(c.dist_from_line)

result_dist = linregress(x, y)

ax.plot(
    x, result_dist.intercept + result_dist.slope * np.asarray(x), "r-", label="Best Fit"
)
ax.plot(x, y, "k.", label="Data")
ax.legend()

ax.set_xlabel("Distance from line [m]")
ax.set_ylabel("Windward Mark Position")
st.pyplot(fig)
st.write(f"R = {result_dist.rvalue}, p-value = {result_dist.pvalue}")

st.header("Start Priority:")
st.write(
    "Here the greater the value of R^2, the greater proportion of the windward "
    "mark position can be attributed to the feature."
)
fig, ax = plt.subplots()
ax.bar(
    ["Start Position", "Speed at Go", "Distance from Line"],
    [result_pos.rvalue**2, result_speed.rvalue**2, result_dist.rvalue**2],
)
ax.set_ylim([0, 1])
ax.set_ylabel("R^2")
st.pyplot(fig)
