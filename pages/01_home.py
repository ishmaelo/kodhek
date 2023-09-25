import streamlit as st
import pandas as pd
import numpy as np
import random



st.set_page_config(page_title='Dr. Kodhek - T2DM Optimal care', layout = 'wide', initial_sidebar_state = 'auto')

st.title("Type-2 Diabetes Management Optimal Care")
st.subheader("Author: Dr. Argwings Kodhek - PhD in Epidemiology and Biostatics ")
st.write("A comprehensive medical tool for management of type-2 diabetes")

st.divider()
st.header("SCORING OF THE ELEMENTS")
st.divider()
st.subheader("1.BGM (Each visit outcome measure)")
scale = st.radio(
    "Meaurement type",
    ["FBG", "RBS"],
    index=None,
)
mmol = st.number_input("mmol/lit:")
result = ''
if st.button('Calculate BGM'):
    if scale=='FBG':
       if mmol >= 3.9 and mmol <= 5.5:
        result = 'Optimal'
        st.success(result)
       if mmol >= 5.6 and mmol <= 7.9:
        result = 'Normal'
        st.info(result)
       if mmol >= 8 and mmol <= 9:
        result = 'Elevated'
        st.warning(result)        
       if ((mmol >= 9.1 and mmol <= 10.4) or (mmol >= 3 and mmol <= 3.8)):
        result = 'High/grade 1 hypo'
        st.error(result)
       if mmol > 10 and mmol < 3:
        result = 'Very high/grade 2 hypo'
        st.error(result)
    if scale=='RBS':
       if mmol >= 3.9 and mmol <= 6:
        result = 'Optimal'
        st.success(result)
       if mmol >= 6.1 and mmol <= 6.9:
        result = 'Normal'
        st.info(result)
       if mmol >= 7 and mmol <= 10:
        result = 'Elevated' 
        st.warning(result)
       if mmol >= 10.1 and mmol <= 13.9:
        result = 'High/grade 1 hypo'
        st.error(result)
       if mmol > 13.9:
        result = 'Very high/grade 2 hypo'
        st.error(result)
    if not result:
        st.error('You have not entered valid inputs, please try again')
else:
    scale = ''
    mmol = 0
    




