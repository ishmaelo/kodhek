import streamlit as st
import pandas as pd
import numpy as np
import random



st.set_page_config(page_title='Dr. Kodhek - T2DM Optimal care', layout = 'wide', initial_sidebar_state = 'auto')

st.title("Type-2 Diabetes Management Optimal Care")
st.subheader("Author: Dr. Argwings Kodhek - PhD in Epidemiology and Biostatics ")

st.sidebar.title("Type-2 Diabetes Management Optimal Care")
st.sidebar.subheader("Author: Dr. Argwings Kodhek - PhD in Epidemiology and Biostatics ")
st.sidebar.write("A comprehensive medical tool for management of type-2 diabetes")


chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['Patient 1', 'Patient 2', 'Patient 3'])

st.line_chart(chart_data)



    




