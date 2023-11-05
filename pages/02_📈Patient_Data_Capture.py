import streamlit as st
import pandas as pd
import numpy as np
import random



st.set_page_config(page_title='Dr. Kodhek - T2DM Optimal care', layout = 'wide', initial_sidebar_state = 'auto')

st.title("Patient Data Capture Page")
st.divider()
st.write("This page will contain the interface for capturing medical data pertaining to patients")


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
mpc = ''
score = ''
if st.button('Calculate BGM'):
    if scale=='FBG':
       if mmol >= 3.9 and mmol <= 5.5:
        result = 'Optimal'
        mpc = 1
        score = 5
        st.success(result)
       if mmol >= 5.6 and mmol <= 7.9:
        result = 'Normal'
        mpc = 2
        score = 4
        st.info(result)
       if mmol >= 8 and mmol <= 9:
        result = 'Elevated'
        mpc = 3
        score = 3
        st.warning(result)        
       if ((mmol >= 9.1 and mmol <= 10.4) or (mmol >= 3 and mmol <= 3.8)):
        result = 'High/grade 1 hypo'
        mpc = 4
        score = 2
        st.error(result)
       if mmol > 10 and mmol < 3:
        result = 'Very high/grade 2 hypo'
        mpc = 5
        score = 1
        st.error(result)
    if scale=='RBS':
       if mmol >= 3.9 and mmol <= 6:
        result = 'Optimal'
        mpc = 1
        score = 5
        st.success(result)
       if mmol >= 6.1 and mmol <= 6.9:
        result = 'Normal'
        mpc = 2
        score = 4
        st.info(result)
       if mmol >= 7 and mmol <= 10:
        result = 'Elevated'
        mpc = 3
        score = 3 
        st.warning(result)
       if mmol >= 10.1 and mmol <= 13.9:
        result = 'High/grade 1 hypo'
        mpc = 4
        score = 2
        st.error(result)
       if mmol > 13.9:
        result = 'Very high/grade 2 hypo'
        mpc = 5
        score = 1
        st.error(result)

    st.write('MPC Scale: ', mpc)
    st.write('Score: ', score)
    if not result:
        st.error('You have not entered valid inputs, please try again')
else:
    scale = ''
    mmol = 0
    mpc = ''
    score = ''


# == Working with databases ==

st.write('Working with Databases')

import streamlit as st
import sqlite3

# Create a connection to the SQLite database
conn = sqlite3.connect('db/patient.db')

# Execute a SQL query
cursor = conn.cursor()
cursor.execute('SELECT * FROM biodata')

# Get the results of the query
users = cursor.fetchall()



st.divider()

st.subheader('Adding patient records')

# Display the results in Streamlit
st.table(users)

## Test saving of data to the db
import time
def get_connection_to_db():
    return sqlite3.connect('db/patient.db')# <-- Replace with your db connection method

connx = get_connection_to_db()

def store_in_db(name,dob):
    #st.write(data)  # <-- Replace with your db storage method e.g. conn.write(data)
    connx.execute(f'''
            INSERT INTO biodata (patient_name, date_of_birth) VALUES ('{name}','{dob}')
            ''')
    connx.commit()


st.header("New patient")
form = st.form(key="match")
with form:
    name = st.text_input("Patient name")
    dob = st.text_input("Date of birth")
    timestamp = time.time()
    submit = st.form_submit_button("Submit")
    if submit:
        store_in_db(name,dob)
