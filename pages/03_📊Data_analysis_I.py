import streamlit as st
import pandas as pd
import numpy as np
import random
import time
from datetime import datetime

### reading patient data ###
import sqlite3
# Create a connection to the SQLite database
conn = sqlite3.connect('db/patient.db')

st.set_page_config(page_title='Dr. Kodhek - T2DM Optimal care', layout = 'wide', initial_sidebar_state = 'auto')
### if a patient is selected :: query parameters ###

def store_in_db(patient_id,reading_date,reading_time,measurement_type,fbg,rbc_ppg,mpc_scale,mpc,score,description):
   conn.execute(f'''
            INSERT INTO bgm (patient_id, reading_date,reading_time,
            measurement_type,fbg,rbc_ppg,mpc_scale,mpc,score,description) 
            VALUES ('{patient_id}','{reading_date}','{reading_time}','{measurement_type}','{fbg}'
            ,'{rbc_ppg}','{mpc_scale}','{mpc}','{score}','{description}')
            ''')
   conn.commit()
   #conn.close()
    
def load_readings(patient_id):
     # Execute a SQL query
    cursor = conn.cursor()
    sql = "SELECT reading_date,reading_time,fbg,mpc_scale,mpc,score,description FROM bgm WHERE patient_id = '" + str(patient_id) + "'"
    cursor=conn.cursor()
    cursor.execute(sql)
    df = pd.DataFrame(cursor.fetchall(),columns=['Reading date','Reading time','mmol/lit','MPC scale','MPC','Score','Description'])
    print(df.count())
    """
    if not df.empty:
       last_row = df.iloc[-1]
       last_mmlot = last_row['mmol/lit']
       last2_row = df.iloc[-2]
       last2_mmlot = last2_row['mmol/lit']
       diff = last_mmlot - last2_mmlot
       st.metric(label="FBG", value=str(last_mmlot) + " mmol/lit", delta = str(diff) + "mmol/lit")
    st.dataframe(df,use_container_width=True)
    df = df.drop('Reading date', axis=1)
    df = df.drop('Reading time', axis=1)
    df = df.drop('Description', axis=1)
    df = df.drop('MPC scale', axis=1)
    """
    st.line_chart(df)


def record_bgm(patient_id):
    form = st.form(key="match")
    with form:
        st.subheader("Record BGM for the patient")
        scale = st.radio(
            "Meaurement type",
            ["FBG", "RBS"],
            index=None,
        )
        mmol = st.number_input("mmol/lit:")
        submit = st.form_submit_button("Save BGM reading")
        result = ''
        mpc = ''
        score = ''
        if submit:
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
            reading_date = datetime.today().strftime('%d/%m/%Y')
            reading_time =  time.time()
            measurement_type = 1
            if scale=='RBS':
                measurement_type = 2
            fbg = mmol
            rbc_ppg = mmol
            mpc_scale = scale
            description = result
            if not result:
                st.error('You have not entered valid inputs, please try again')
            else:
                if submit:
                    store_in_db(patient_id,reading_date,reading_time,measurement_type,fbg,rbc_ppg,mpc_scale,mpc,score,description)
                    st.success('BGM recorded successfully')
                
        else:
            scale = ''
            mmol = 0
            mpc = ''
            score = ''

def get_patient(conn,patient_id):
    sql = "SELECT * FROM biodata WHERE id = ?"
    cursor=conn.cursor()
    cursor.execute(sql,patient_id)
    result, = cursor.fetchall()
    #conn.close()
    return result
    
def display_patient(patient):
    st.link_button("Back to list of patients", "Data_analysis_I")
    patient_id = patient[0]
    st.title(patient[1])
    st.write('Date of birth: ', patient[2])
    st.write('Sex: ', patient[3])
    st.divider()
    st.write("This page contains basic descriptive analysis of the patient")
    load_readings(patient_id)
    record_bgm(patient_id)

    


patient_id = ''
qp = st.experimental_get_query_params()
if "patient" in qp:
    patient_id = qp['patient'][0]
    
if patient_id:
    patient = get_patient(conn,patient_id)
    display_patient(patient)
   











else:
    ### existing patients ####
    st.title("Data Analysis I")
    st.divider()
    st.write("This page contains basic descriptive analysis")


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
