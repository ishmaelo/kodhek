import streamlit as st
import pandas as pd
import numpy as np
import random
import pages.modules.analysis as analysis
import pages.modules.utilities as utility


st.set_page_config(page_title='Dr. Kodhek - T2DM Optimal Care', layout = 'wide', initial_sidebar_state = 'auto')

### reading patient data ###
import sqlite3
# Create a connection to the SQLite database
conn = sqlite3.connect('db/patient.db')


# Execute a SQL query
cursor = conn.cursor()
cursor.execute('SELECT patient_name  FROM biodata')
df = pd.DataFrame(cursor.fetchall(),columns=['Patient Name'])



### Sidebar ####
st.sidebar.title("T2DM Optimal Care")
st.sidebar.markdown("<hr/>",unsafe_allow_html=True)
st.sidebar.subheader('Current patients')    
patient = st.sidebar.selectbox('Choose a patient for analysis', df)


#retrieve patient ID
patient_id = utility.get_patient_by_name(conn,patient)

#display analysis page
analysis.display(conn,patient_id)
        
st.sidebar.markdown("<hr/>",unsafe_allow_html=True)
st.sidebar.write('Author: Dr. Kodhek')
       
conn.close()