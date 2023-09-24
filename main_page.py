import streamlit as st
import pandas as pd
import numpy as np
import random

st.set_page_config(page_title='Dr. Kodhek - T2DM Optimal care', layout = 'wide', initial_sidebar_state = 'auto')

st.title("Dr. Kodhek : Type-2 Diabetes Management Optimal Care")
st.write("A comprehensive medical tool for management of type-2 diabetes")

st.divider()
df = pd.DataFrame(
    {
        "name": ["Patient I", "Patient II", "Patient III"],
        "url": ["https://roadmap.streamlit.app", "https://extras.streamlit.app", "https://issues.streamlit.app"],
        "stars": [random.randint(0, 1000) for _ in range(3)],
        "views_history": [[random.randint(0, 5000) for _ in range(30)] for _ in range(3)],
    }
)
st.dataframe(
    df,
    column_config={
        "name": "Patient name",
        "stars": st.column_config.NumberColumn(
            "MPC Scores",
            help="Number of stars on GitHub",
            format="%d ⭐",
        ),
        "url": st.column_config.LinkColumn("Link"),
        "views_history": st.column_config.LineChartColumn(
            "Blood glucose (past 30 days)", y_min=0, y_max=5000
        ),
    },
    hide_index=True,
)
st.divider()
