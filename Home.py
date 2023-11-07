import streamlit as st
import pandas as pd
import numpy as np
import random



st.set_page_config(page_title='Dr. Kodhek - T2DM Optimal Care Menology', layout = 'wide', initial_sidebar_state = 'auto')

st.title("T2DM Optimal Care Menology")


st.sidebar.title("Management Performance Composite Score Tool for Type 2 Diabetes Melitus (MPCST)")
st.sidebar.subheader("Author: Dr. Argwings Kodhek - PhD in Epidemiology and Biostatics ")



chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['Patient 1', 'Patient 2', 'Patient 3'])

st.line_chart(chart_data)



    




