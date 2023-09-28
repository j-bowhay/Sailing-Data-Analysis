from itertools import groupby

import streamlit as st
import pandas as pd
import numpy as np

from analysis._utils import hide_streamlit
from analysis._selection import select_race, select_regatta
from analysis._get_data import get_leg_data

st.set_page_config(
    page_title="Sailing Data Analysis: Position Analysis",
    page_icon="⛵",
)
hide_streamlit()

regatta = select_regatta()

race = select_race(regatta)

data = pd.json_normalize(
    get_leg_data(regatta, race)["legs"], ["competitors"], ["from", "to"]
)[["name", "rank", "to"]].set_index("name")
combined_data = data.groupby("name")["rank"].apply(list).reset_index()

to = data.to.values
marks = [k for k, g in groupby(to) if k != 0]
mark_positions = pd.DataFrame(
    combined_data["rank"].values.tolist(), index=combined_data.name, columns=marks
)
s = mark_positions.columns.to_series().groupby(mark_positions.columns)
mark_positions.columns = np.where(
    s.transform("size") > 1,
    mark_positions.columns + ":" + s.cumcount().add(1).astype(str),
    mark_positions.columns,
)

deltas = (mark_positions.diff(axis=1) * -1).dropna(axis=1)
deltas.columns = [f"Change {i+1}" for i in range(len(deltas.columns))]
deltas["Total Place Change"] = deltas.sum(axis=1)

final_data = pd.concat([mark_positions, deltas], axis=1)
final_data = final_data[
    [item for items in zip(mark_positions.columns, deltas.columns) for item in items]
]

st.dataframe(final_data)
