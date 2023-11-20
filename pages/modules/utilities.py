def set_title(st):
    st.set_page_config(page_title='Dr. Kodhek - T2DM Optimal care', layout = 'wide', initial_sidebar_state = 'auto')
    
def get_database_connection():
    import sqlite3
    # Create a connection to the SQLite database
    return sqlite3.connect('db/patient.db')
    
def get_patient(conn,patient_id):
    sql = "SELECT * FROM biodata WHERE id = ?"
    cursor=conn.cursor()
    cursor.execute(sql,patient_id)
    result, = cursor.fetchall()
    return result
def get_patient_id_via_url(st):
    patient_id = ''
    qp = st.experimental_get_query_params()
    if "patient" in qp:
        patient_id = qp['patient'][0]
    return patient_id
    
def patient_header_info(patient,st):    
    st.link_button("Back to list of patients", "Patients")
    patient_id = patient[0]
    st.title(patient[1])
    st.write('Date of birth: ', patient[2])
    st.write('Sex: ', patient[3])
    
        
def get_blood_sugar_data_with_annotations(resultset,pd):
    df = pd.DataFrame(columns=["Reading date","Description","Scale"])
    for row in resultset:
       new_row = [row[0], "Reading", row[1]]
       df.loc[len(df.index)] = new_row
       new_row = [row[0], "Very High/Grade 2 Hypo", 5]
       df.loc[len(df.index)] = new_row
       new_row = [row[0], "High/Grade 2 Hypo", 4]
       df.loc[len(df.index)] = new_row
       new_row = [row[0], "Elevated", 3]
       df.loc[len(df.index)] = new_row
       new_row = [row[0], "Normal", 2]
       df.loc[len(df.index)] = new_row
       new_row = [row[0], "Optimal", 1]
       df.loc[len(df.index)] = new_row
    return df
    
def get_bp_data_with_annotations(resultset):
    df = pd.DataFrame(columns=["Reading date","Description","Score"])
    for row in resultset:
       new_row = [row[0], "Reading", row[3]]
       df.loc[len(df.index)] = new_row
       new_row = [row[0], "Grade 3/Urgency", 1]
       df.loc[len(df.index)] = new_row
       new_row = [row[0], "Grade 2", 2]
       df.loc[len(df.index)] = new_row
       new_row = [row[0], "Grade 1", 3]
       df.loc[len(df.index)] = new_row
       new_row = [row[0], "Normal high", 4]
       df.loc[len(df.index)] = new_row
       new_row = [row[0], "Normal", 5]
       df.loc[len(df.index)] = new_row
    return df
    
def get_lipid_data_with_annotations(resultset):
    df = pd.DataFrame(columns=["Reading date","Description","Score"])
    for row in resultset:
       new_row = [row[0], "Reading", row[3]]
       df.loc[len(df.index)] = new_row
       new_row = [row[0], "Severely high", 1]
       df.loc[len(df.index)] = new_row
       new_row = [row[0], "High", 2]
       df.loc[len(df.index)] = new_row
       new_row = [row[0], "Borderline high", 3]
       df.loc[len(df.index)] = new_row
       new_row = [row[0], "Near optimal", 4]
       df.loc[len(df.index)] = new_row
       new_row = [row[0], "Optimal", 5]
       df.loc[len(df.index)] = new_row
    return df
    
def get_bmi_data_with_annotations(resultset):
    df = pd.DataFrame(columns=["Reading date","Description","Score"])
    for row in resultset:
       new_row = [row[0], "Reading", row[3]]
       df.loc[len(df.index)] = new_row
       new_row = [row[0], "Extreme obesity/Underweight", 1]
       df.loc[len(df.index)] = new_row
       new_row = [row[0], "Obesity class 2", 2]
       df.loc[len(df.index)] = new_row
       new_row = [row[0], "Obesity class 1", 3]
       df.loc[len(df.index)] = new_row
       new_row = [row[0], "Overweight", 4]
       df.loc[len(df.index)] = new_row
       new_row = [row[0], "Normal", 5]
       df.loc[len(df.index)] = new_row
    return df
    
def annonation_chart(source,alt,st):
    base = alt.Chart(source).encode(
        alt.Color("Description").legend(None)
    ).transform_filter(
        "datum.Description !== 'IBM'"
    )

    line = base.mark_line().encode(x="Reading date", y="Scale")


    last_reading = base.mark_circle().encode(
        alt.X("last_date['Reading date']:T"),
        alt.Y("last_date['Scale']:Q")
    ).transform_aggregate(
        last_date="argmax(Reading date)",
        groupby=["Description"]
    )
    
    description = last_reading.mark_text(align="left", dx=4).encode(text="Description")

    chart = (line + last_reading + description).encode(
        x=alt.X().title("Reading date"),
        y=alt.Y().title("Scale")
    )

    st.write(chart,use_container_width=True)
    
def plotly_chart_together(df,st):
    import plotly.express as px
    fig = px.line(df, x="Reading date", y="Scale", color='Description',markers=True)
    st.write(fig)
def plotly_chart_separate(conn,patient_id,start_date,end_date,st):
    import pages.modules.blood_sugar as blood_sugar
    # data
    dates,optimal,normal,elevated,high,very_high,reading = get_row_data(blood_sugar.get_readings_for_graph(conn,patient_id,start_date,end_date))
    
    import plotly.graph_objects as go

    fig = go.Figure()
    
    # Add traces
    fig.add_trace(go.Scatter(x=dates, y=optimal,
                        mode='lines',
                        line=dict(color='green'),
                        name='Optimal'))
    fig.add_trace(go.Scatter(x=dates, y=normal,
                        mode='lines',
                        line=dict(color='blue'),
                        name='Normal'))
    fig.add_trace(go.Scatter(x=dates, y=elevated,
                        mode='lines',
                        line=dict(color='orange'),
                        name='Elevated'))
    fig.add_trace(go.Scatter(x=dates, y=high,
                        mode='lines',
                        line=dict(color='brown'),
                        name='High'))
    fig.add_trace(go.Scatter(x=dates, y=very_high,
                        mode='lines',
                        line=dict(color='red'),
                        name='Very high'))
    fig.add_trace(go.Scatter(x=dates, y=reading,
                        mode='lines+markers',
                        line=dict(color='magenta',width=7),
                        name='Patient BGM Reading'))
    fig.update_layout(title='Patient blood glucose performance',
                   xaxis_title='Date',
                   yaxis_title='Blood glucose reading in scale',
                   xaxis=dict(showgrid=True), 
                   yaxis=dict(showgrid=True)
                   )
    st.write(fig)
        
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
    reading = list()
    for row in resultset:
       dates.append(row[0])
       optimal.append(1)
       normal.append(2)
       elevated.append(3)
       high.append(4)
       very_high.append(5)
       reading.append(row[1])
    return dates,optimal,normal,elevated,high,very_high,reading
    

    