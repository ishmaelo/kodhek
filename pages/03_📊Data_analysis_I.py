import streamlit as st
import pandas as pd
import numpy as np
import random
import time
from datetime import datetime
import altair as alt

### reading patient data ###
import sqlite3
# Create a connection to the SQLite database
conn = sqlite3.connect('db/patient.db')

st.set_page_config(page_title='Dr. Kodhek - T2DM Optimal care', layout = 'wide', initial_sidebar_state = 'auto')
### if a patient is selected :: query parameters ###
def testing2():
    import altair as alt
    from vega_datasets import data
    cursor = conn.cursor()
    sql = "SELECT reading_date,reading_time,fbg,mpc_scale,mpc,score,description FROM bgm WHERE patient_id = '" + str(patient_id) + "'"
    cursor=conn.cursor()
    cursor.execute(sql)
    resultset = cursor.fetchall()
    dates,optimal,normal,elevated,high,very_high = get_row_data(resultset)
    df = pd.DataFrame(resultset,columns=['Reading date','Reading time','mmol/lit','MPC scale','MPC','Score','Description'],index=dates)
    df['Reading date'] = pd.to_datetime(df['Reading date'])
    df['Optimal'] = optimal
    df['Normal'] = normal
    df['Elevated'] = elevated
    df['High/Grade 1 Hypo'] = high
    df['Very High/Grade 2 Hypo'] = very_high
    #df = df.drop('Reading date', axis=1)
    df = df.drop('Reading time', axis=1)
    #df = df.drop('Description', axis=1)
    df = df.drop('MPC scale', axis=1)
    #df = df.drop('mmol/lit', axis=1)
    df = df.drop('MPC', axis=1)
    data.stocks()
    source = data.stocks()
    source
    source = df
    source
    base = alt.Chart(source).encode(
        alt.Color("Description").legend(None)
    ).transform_filter(
        "datum.Description !== 'IBM'"
    ).properties(
        width=500
    )

    line = base.mark_line().encode(x="Reading date", y="Score")


    last_price = base.mark_circle().encode(
        alt.X("last_date['Reading date']:T"),
        alt.Y("last_date['Score']:Q")
    ).transform_aggregate(
        last_date="argmax(Reading date)",
        groupby=["Description"]
    )

    company_name = last_price.mark_text(align="left", dx=4).encode(text="Description")

    chart = (line + last_price + company_name).encode(
        x=alt.X().title("Reading date"),
        y=alt.Y().title("Score")
    )

    chart
def testing():
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    dataset_url = ('https://raw.githubusercontent.com/m-mehdi/pandas_tutorials/main/weekly_stocks.csv')
    df = pd.read_csv(dataset_url, parse_dates=['Date'], index_col='Date')
    pd.set_option('display.max.columns', None)
    df
    #print(df.head())
    #df.plot(y='MSFT', figsize=(9,6))
    #df.plot.line(y=['FB', 'AAPL', 'MSFT'], figsize=(10,6))
    #df.plot(y='FB', figsize=(10,6), title='Facebook Stock', ylabel='USD')
    st.line_chart(df)
def load_readings_with_chart(patient_id):
    st.divider()
    st.subheader("I.Blood Glucose Monitoring")
    cursor = conn.cursor()
    sql = "SELECT reading_date,reading_time,fbg,mpc_scale,mpc,score,description FROM bgm WHERE patient_id = '" + str(patient_id) + "'"
    cursor=conn.cursor()
    cursor.execute(sql)
    resultset = cursor.fetchall()
    new_df = get_row_data_with_annotations(resultset)
    new_df['Reading date'] = pd.to_datetime(new_df['Reading date'])
    source = new_df
    source
    
    base = alt.Chart(source).encode(
        alt.Color("Description").legend(None)
    ).transform_filter(
        "datum.Description !== 'IBM'"
    ).properties(
        width=500
    )

    line = base.mark_line().encode(x="Reading date", y="Score")


    last_price = base.mark_circle().encode(
        alt.X("last_date['Reading date']:T"),
        alt.Y("last_date['Score']:Q")
    ).transform_aggregate(
        last_date="argmax(Reading date)",
        groupby=["Description"]
    )

    company_name = last_price.mark_text(align="left", dx=4).encode(text="Description")

    chart = (line + last_price + company_name).encode(
        x=alt.X().title("Reading date"),
        y=alt.Y().title("Score")
    )

    chart
def hba1c_readings_with_chart(patient_id):
    st.divider()
    st.subheader("2.HBA1C")
    cursor = conn.cursor()
    sql = "SELECT reading_date,reading_time,bgm,id, description,score FROM hba1c WHERE patient_id = '" + str(patient_id) + "'"
    cursor=conn.cursor()
    cursor.execute(sql)
    resultset = cursor.fetchall()
    new_df = get_row_data_with_annotations(resultset)
    new_df['Reading date'] = pd.to_datetime(new_df['Reading date'])
    source = new_df
    source
    
    base = alt.Chart(source).encode(
        alt.Color("Description").legend(None)
    ).transform_filter(
        "datum.Description !== 'IBM'"
    ).properties(
        width=500
    )

    line = base.mark_line().encode(x="Reading date", y="Score")


    last_price = base.mark_circle().encode(
        alt.X("last_date['Reading date']:T"),
        alt.Y("last_date['Score']:Q")
    ).transform_aggregate(
        last_date="argmax(Reading date)",
        groupby=["Description"]
    )

    company_name = last_price.mark_text(align="left", dx=4).encode(text="Description")

    chart = (line + last_price + company_name).encode(
        x=alt.X().title("Reading date"),
        y=alt.Y().title("Score")
    )

    chart    
def bp_readings_with_chart(patient_id):
    st.divider()
    st.subheader("3.Blood Pressure Monitoring")
    cursor = conn.cursor()
    sql = "SELECT reading_date,reading_time,bgm,id, description,score FROM hba1c WHERE patient_id = '" + str(patient_id) + "'"
    cursor=conn.cursor()
    cursor.execute(sql)
    resultset = cursor.fetchall()
    new_df = get_row_data_with_annotations(resultset)
    new_df['Reading date'] = pd.to_datetime(new_df['Reading date'])
    source = new_df
    source
    
    base = alt.Chart(source).encode(
        alt.Color("Description").legend(None)
    ).transform_filter(
        "datum.Description !== 'IBM'"
    ).properties(
        width=500
    )

    line = base.mark_line().encode(x="Reading date", y="Score")


    last_price = base.mark_circle().encode(
        alt.X("last_date['Reading date']:T"),
        alt.Y("last_date['Score']:Q")
    ).transform_aggregate(
        last_date="argmax(Reading date)",
        groupby=["Description"]
    )

    company_name = last_price.mark_text(align="left", dx=4).encode(text="Description")

    chart = (line + last_price + company_name).encode(
        x=alt.X().title("Reading date"),
        y=alt.Y().title("Score")
    )

    chart   
def lipid_readings_with_chart(patient_id):
    st.divider()
    st.subheader("4.Lipids (mmol/lit)")
    cursor = conn.cursor()
    sql = "SELECT reading_date,reading_time,bgm,id, description,score FROM hba1c WHERE patient_id = '" + str(patient_id) + "'"
    cursor=conn.cursor()
    cursor.execute(sql)
    resultset = cursor.fetchall()
    new_df = get_row_data_with_annotations(resultset)
    new_df['Reading date'] = pd.to_datetime(new_df['Reading date'])
    source = new_df
    source
    
    base = alt.Chart(source).encode(
        alt.Color("Description").legend(None)
    ).transform_filter(
        "datum.Description !== 'IBM'"
    ).properties(
        width=500
    )

    line = base.mark_line().encode(x="Reading date", y="Score")


    last_price = base.mark_circle().encode(
        alt.X("last_date['Reading date']:T"),
        alt.Y("last_date['Score']:Q")
    ).transform_aggregate(
        last_date="argmax(Reading date)",
        groupby=["Description"]
    )

    company_name = last_price.mark_text(align="left", dx=4).encode(text="Description")

    chart = (line + last_price + company_name).encode(
        x=alt.X().title("Reading date"),
        y=alt.Y().title("Score")
    )

    chart   
def bmi_readings_with_chart(patient_id):
    st.divider()
    st.subheader("5.Body Mass Index")
    cursor = conn.cursor()
    sql = "SELECT reading_date,reading_time,bgm,id, description,score FROM hba1c WHERE patient_id = '" + str(patient_id) + "'"
    cursor=conn.cursor()
    cursor.execute(sql)
    resultset = cursor.fetchall()
    new_df = get_row_data_with_annotations(resultset)
    new_df['Reading date'] = pd.to_datetime(new_df['Reading date'])
    source = new_df
    source
    
    base = alt.Chart(source).encode(
        alt.Color("Description").legend(None)
    ).transform_filter(
        "datum.Description !== 'IBM'"
    ).properties(
        width=500
    )

    line = base.mark_line().encode(x="Reading date", y="Score")


    last_price = base.mark_circle().encode(
        alt.X("last_date['Reading date']:T"),
        alt.Y("last_date['Score']:Q")
    ).transform_aggregate(
        last_date="argmax(Reading date)",
        groupby=["Description"]
    )

    company_name = last_price.mark_text(align="left", dx=4).encode(text="Description")

    chart = (line + last_price + company_name).encode(
        x=alt.X().title("Reading date"),
        y=alt.Y().title("Score")
    )

    chart   
def get_row_data_with_annotations(resultset):
    df = pd.DataFrame(columns=["Reading date","Description","Score"])
    for row in resultset:
       new_row = [row[0], "Reading", row[5]]
       df.loc[len(df.index)] = new_row
       new_row = [row[0], "Very High/Grade 2 Hypo", 1]
       df.loc[len(df.index)] = new_row
       new_row = [row[0], "High/Grade 2 Hypo", 2]
       df.loc[len(df.index)] = new_row
       new_row = [row[0], "Elevated", 3]
       df.loc[len(df.index)] = new_row
       new_row = [row[0], "Normal", 4]
       df.loc[len(df.index)] = new_row
       new_row = [row[0], "Optimal", 5]
       df.loc[len(df.index)] = new_row
    return df
 
def load_readings(patient_id):
    st.divider()
    st.subheader("I.Blood Glucose Monitoring")
    cursor = conn.cursor()
    sql = "SELECT reading_date,reading_time,fbg,mpc_scale,mpc,score,description FROM bgm WHERE patient_id = '" + str(patient_id) + "'"
    cursor=conn.cursor()
    cursor.execute(sql)
    resultset = cursor.fetchall()
    dates,optimal,normal,elevated,high,very_high = get_row_data(resultset)
    df = pd.DataFrame(resultset,columns=['Reading date','Reading time','mmol/lit','MPC scale','MPC','Score','Description'],index=dates)
    df['Reading date'] = pd.to_datetime(df['Reading date'])
    df['Optimal'] = optimal
    df['Normal'] = normal
    df['Elevated'] = elevated
    df['High/Grade 1 Hypo'] = high
    df['Very High/Grade 2 Hypo'] = very_high
    #df = df.drop('Reading date', axis=1)
    df = df.drop('Reading time', axis=1)
    df = df.drop('Description', axis=1)
    df = df.drop('MPC scale', axis=1)
    #df = df.drop('mmol/lit', axis=1)
    df = df.drop('MPC', axis=1)
    #df
    st.line_chart(df, x= "Reading date", y = ["Score","Optimal","Normal","Elevated","High/Grade 1 Hypo","Very High/Grade 2 Hypo"],color=["#ff8000","#ffbf00","#0000ff","#00ff00","#000000","#ff0000"],use_container_width=True)
  

def get_row_data(resultset):
    dates = list()
    optimal = list()
    normal = list()
    elevated = list()
    high = list()
    very_high = list()
    for row in resultset:
       dates.append(row[0])
       optimal.append(5)
       normal.append(4)
       elevated.append(3)
       high.append(2)
       very_high.append(1)
    return dates,optimal,normal,elevated,high,very_high
    
def get_patient(conn,patient_id):
    sql = "SELECT * FROM biodata WHERE id = ?"
    cursor=conn.cursor()
    cursor.execute(sql,patient_id)
    result, = cursor.fetchall()
    return result
    
def display_patient(patient):
    st.link_button("Back to list of patients", "Patients")
    patient_id = patient[0]
    st.title(patient[1])
    st.write('Date of birth: ', patient[2])
    st.write('Sex: ', patient[3])
    load_readings_with_chart(patient_id)
    hba1c_readings_with_chart(patient_id)
    bp_readings_with_chart(patient_id)
    lipid_readings_with_chart(patient_id)
    bmi_readings_with_chart(patient_id)
  
   
patient_id = ''
qp = st.experimental_get_query_params()
if "patient" in qp:
    patient_id = qp['patient'][0]
    
if patient_id:
    patient = get_patient(conn,patient_id)
    display_patient(patient)
    #testing2()
    