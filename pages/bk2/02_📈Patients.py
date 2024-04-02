import streamlit as st
import pandas as pd
import numpy as np
import random



st.set_page_config(page_title='Dr. Kodhek - T2DM Optimal care', layout = 'wide', initial_sidebar_state = 'auto')

### reading patient data ###
import sqlite3
# Create a connection to the SQLite database
conn = sqlite3.connect('db/patient.db')

### existing patients ####
st.title("Patients' Page")

st.write("Kindly select a patient record to analyze")
# Execute a SQL query
cursor = conn.cursor()
cursor.execute('SELECT id,patient_name,date_of_birth,sex,race,duration,residence,profession,monthly_income,subsistence_spending,out_of_pocket_spending,non_sp_40  FROM biodata')
df = pd.DataFrame(cursor.fetchall(),columns=['S/N','Patient Name','Date of Birth','Sex','Race','Duration of T2DM','Residence','Profession','Monthly Income','Subsistence Spending','Out of Pocket Health Expenditure','40% of Non SP'])

conn.close()
#You first sort df by Name
#df = df.sort_values(by='id')
df['Patient Name'] = df.apply(
    lambda row: '<a href="{}">{}</a>'.format( 'Data_analysis_I?patient=' + str(row['S/N']), row['Patient Name']),
    axis=1)

# You can choose to drop the Website column
#df = df.drop('Website', axis=1)

st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)
        
        
