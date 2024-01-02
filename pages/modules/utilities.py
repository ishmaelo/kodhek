import pages.modules.blood_sugar as blood_sugar
import pages.modules.hba1c as hba1c
import pages.modules.blood_pressure as blood_pressure
import pages.modules.lipid as lipid
import pages.modules.bmi as bmi

import math

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


def get_age(birth_date):
    from datetime import date
    from datetime import datetime
    today = date.today()
    birth_date = datetime.strptime(birth_date, '%d/%m/%Y')
    age = today.year - birth_date.year
    full_year_passed = (today.month, today.day) < (birth_date.month, birth_date.day)
    if not full_year_passed:
        age -= 1
    return age
    
def number_of_months(start_date,end_date):
    from datetime import date
    from datetime import datetime
    from dateutil import relativedelta
    #start_date = datetime.strptime(start_date, '%Y-%m-%d')
    #end_date = datetime.strptime(end_date, '%Y-%m-%d')
    
    r = relativedelta.relativedelta(end_date, start_date)
    total_months = r.months + (12*r.years)
    return total_months

def patient_header_info(patient,st):    
    st.link_button("Back to list of patients", "Patients")
    patient_id = patient[0]
    st.title(patient[1])
    age = ", {} {}".format(get_age(patient[2]), ' years')
    st.write(patient[3], age)
    st.markdown("""---""")
    
def get_score_description(index):
    scores = ["Undefined","Poor Care","Fair Care","Average Care","Good Care","Optimal Care"]
    return scores[index]
    
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
def plotly_chart_blood_sugar(conn,patient_id,start_date,end_date,st):
    import pages.modules.blood_sugar as blood_sugar
    # data
    data = blood_sugar.get_readings_for_graph(conn,patient_id,start_date,end_date)
    dates,optimal,normal,elevated,high,very_high,reading = get_row_data_blood_sugar(data)
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
    fig.update_layout(title='Blood Glucose Performance (Rated in Scale)',
                   xaxis_title='Reading date',
                   yaxis_title='Blood glucose reading in scale',
                   xaxis=dict(showgrid=True), 
                   yaxis=dict(showgrid=True)
                   )
    st.write(fig)
def plotly_chart_hba1c(conn,patient_id,start_date,end_date,st):
    import pages.modules.hba1c as hba1c
    # data
    data = hba1c.get_readings_for_graph(conn,patient_id,start_date,end_date)
    dates,optimal,normal,elevated,high,very_high,reading = get_row_data_hba1c(data)
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
                        name='Patient HBA1C Reading'))
    fig.update_layout(title='Patient HBA1C performance',
                   xaxis_title='Date',
                   yaxis_title='HBA1C reading in scale',
                   xaxis=dict(showgrid=True), 
                   yaxis=dict(showgrid=True)
                   )
    st.write(fig)        

def plotly_chart_blood_pressure(conn,patient_id,start_date,end_date,st):
    import pages.modules.blood_pressure as blood_pressure
    # data
    data = blood_pressure.get_readings_for_graph(conn,patient_id,start_date,end_date)
    dates,optimal,normal,elevated,high,very_high,reading = get_row_data_blood_pressure(data)
    import plotly.graph_objects as go

    fig = go.Figure()
    
    # Add traces
    fig.add_trace(go.Scatter(x=dates, y=optimal,
                        mode='lines',
                        line=dict(color='green'),
                        name='Normal'))
    fig.add_trace(go.Scatter(x=dates, y=normal,
                        mode='lines',
                        line=dict(color='blue'),
                        name='High Normal'))
    fig.add_trace(go.Scatter(x=dates, y=elevated,
                        mode='lines',
                        line=dict(color='orange'),
                        name='Grade 1'))
    fig.add_trace(go.Scatter(x=dates, y=high,
                        mode='lines',
                        line=dict(color='brown'),
                        name='Grade 2'))
    fig.add_trace(go.Scatter(x=dates, y=very_high,
                        mode='lines',
                        line=dict(color='red'),
                        name='Grade 3/Urgency'))
    fig.add_trace(go.Scatter(x=dates, y=reading,
                        mode='lines+markers',
                        line=dict(color='magenta',width=7),
                        name='Patient Blood Pressure Reading'))
    fig.update_layout(title='Patient Blood Pressure performance',
                   xaxis_title='Date',
                   yaxis_title='Blood Pressure reading in scale',
                   xaxis=dict(showgrid=True), 
                   yaxis=dict(showgrid=True)
                   )
    st.write(fig)   
def plotly_chart_bmi(conn,patient_id,start_date,end_date,st):
    import pages.modules.bmi as bmi
    # data
    data = bmi.get_readings_for_graph(conn,patient_id,start_date,end_date)
    dates,optimal,normal,elevated,high,very_high,reading = get_row_data_blood_pressure(data)
    import plotly.graph_objects as go

    fig = go.Figure()
    
    # Add traces
    fig.add_trace(go.Scatter(x=dates, y=optimal,
                        mode='lines',
                        line=dict(color='green'),
                        name='Normal'))
    fig.add_trace(go.Scatter(x=dates, y=normal,
                        mode='lines',
                        line=dict(color='blue'),
                        name='Overweight'))
    fig.add_trace(go.Scatter(x=dates, y=elevated,
                        mode='lines',
                        line=dict(color='orange'),
                        name='Obesity Class 1'))
    fig.add_trace(go.Scatter(x=dates, y=high,
                        mode='lines',
                        line=dict(color='brown'),
                        name='Obesity Class 2'))
    fig.add_trace(go.Scatter(x=dates, y=very_high,
                        mode='lines',
                        line=dict(color='red'),
                        name='Extreme Obesity/Underweight'))
    fig.add_trace(go.Scatter(x=dates, y=reading,
                        mode='lines+markers',
                        line=dict(color='magenta',width=7),
                        name='Patient BMI Reading'))
    fig.update_layout(title='Patient BMI performance',
                   xaxis_title='Date',
                   yaxis_title='BMI reading in scale',
                   xaxis=dict(showgrid=True), 
                   yaxis=dict(showgrid=True)
                   )
    st.write(fig)   
def get_row_data_blood_sugar(resultset):
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
    
def get_row_data_hba1c(resultset):
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
 
def get_row_data_blood_pressure(resultset):
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
    
def check_con_dis_cordance(b,formating=False):
    if formating:
        if b > 0:
            return 'Concordant'
        else:
            return 'Discordant'
        
    if b > 0:
        return '<p style="color:green; font-weight: bold;">Concordant</p>'
    else:
        return '<p style="color:red;font-weight: bold;">Discordant</p>'
  
def target_summaries(pd, st):
    df = pd.DataFrame(columns=["Care Target","MPC Score","Description","Gradient","Concordance"])
    
    #blood sugar
    blood_sugar_score = st.session_state.blood_sugar_score
    blood_sugar_gradient = st.session_state.blood_sugar_gradient
    blood_sugar_score_description = blood_sugar.get_score_description(blood_sugar_score)
    blood_sugar_gradient_description = check_con_dis_cordance(blood_sugar_gradient,True)
    new_row = ["Blood Sugar",blood_sugar_score,blood_sugar_score_description,blood_sugar_gradient,blood_sugar_gradient_description]
    df.loc[len(df.index)] = new_row
    
    #HBA1C
    hba1c_score = st.session_state.hba1c_score
    hba1c_gradient = st.session_state.hba1c_gradient
    hba1c_score_description = hba1c.get_score_description(blood_sugar_score)
    hba1c_gradient_description = check_con_dis_cordance(blood_sugar_gradient,True)
    new_row = ["HBA1C",hba1c_score,hba1c_score_description,hba1c_gradient,hba1c_gradient_description]
    df.loc[len(df.index)] = new_row
    
    #Summary
    average_score = (blood_sugar_score+hba1c_score)/2
    average_gradient = (blood_sugar_gradient+hba1c_gradient)/2
    averages_score_description = get_score_description(math.floor(average_score))
    average_gradient_description = check_con_dis_cordance(average_gradient,True)
    
    
    new_row = ["Overall",average_score,averages_score_description,average_gradient,average_gradient_description]
    df.loc[len(df.index)] = new_row
    
    df = df.set_index('Care Target')
    st.write(df)