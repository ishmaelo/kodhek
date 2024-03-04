import pages.modules.blood_sugar as blood_sugar
import pages.modules.hba1c as hba1c
import pages.modules.blood_pressure as blood_pressure
import pages.modules.lipid as lipid
import pages.modules.bmi as bmi
import pages.modules.urine as urine
import pages.modules.eye as eye
import pages.modules.monofilament as monofilament
import pages.modules.diet as diet
import pages.modules.physical_activity as physical_activity
import pages.modules.education as education
import pages.modules.comorbidity as comorbidity
import pages.modules.health_system as health_system
import pages.modules.socioeconomic as socioeconomic

import math

from datetime import date
from datetime import datetime
from dateutil import relativedelta

def set_title(st):
    #st.set_page_config(page_title='Dr. Kodhek - T2DM Optimal care', layout = 'wide', initial_sidebar_state = 'auto')
    st.set_page_config(page_title='Dr. Kodhek - T2DM Optimal care',layout = 'wide',initial_sidebar_state = 'collapsed')
    
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
    target = ''
    qp = st.experimental_get_query_params()
    if "patient" in qp:
        patient_id = qp['patient'][0]
    if "target" in qp:
        target = qp['target'][0]
    return patient_id, target


def get_age(birth_date):
    today = date.today()
    birth_date = datetime.strptime(birth_date, '%d/%m/%Y')
    age = today.year - birth_date.year
    full_year_passed = (today.month, today.day) < (birth_date.month, birth_date.day)
    if not full_year_passed:
        age -= 1
    return age
    
def get_daignosis_duration(the_date):
    today = date.today()
    dx_date = datetime.strptime(the_date, '%Y-%m-%d')
    r = relativedelta.relativedelta(today, dx_date)
    return r.years, r.months
   
def number_of_months(start_date,end_date):
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    r = relativedelta.relativedelta(end_date, start_date)
    total_months = r.months + (12*r.years)
    mnths = "less than a month"
    if r.days > 0:
        total_months += 1
    if (total_months==1):
        mnths = str(total_months)  + " month"
    if (total_months>1):
        mnths = str(total_months) + " months"    
    return mnths,total_months
    
def add_date(the_date,years,months):
    start_date = datetime.strptime(the_date, '%Y-%m-%d')
    new_date = start_date + relativedelta.relativedelta(years=years) + relativedelta.relativedelta(months=months)
    return new_date.strftime('%Y-%m-%d')
   
def patient_header_info(patient,st):    
    st.link_button("Back to list of patients", "Patients")
    patient_id = patient[0]
    st.title(patient[1])
    age = " {} {} ".format(get_age(patient[2]), ' years')
    st.write(patient[3],",", age)
    years, months = get_daignosis_duration(patient[12])
    yrs = mnths = ''
    if (years==1):
        yrs = str(years) + " year"
    if (years>1):
        yrs = str(years) + " years"
    if (months==1):
        mnths = str(months)  + " month"
    if (months>1):
        mnths = str(months) + " months"
    st.write("Diabetic for the last ", yrs, mnths)
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
    
def get_hba1c_data_with_annotations(resultset):
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
def plotly_chart(data,labels,st):
    dates,optimal,normal,elevated,high,very_high,reading = get_row_data(data)
    if len(dates)<1:
       st.write("Insufficient readings to generate graph")
       return
    import plotly.graph_objects as go

    fig = go.Figure()
    
    # Add traces
    fig.add_trace(go.Scatter(x=dates, y=optimal,
                        mode='lines',
                        line=dict(color='green',width=3),
                        name=labels[5]))
    fig.add_trace(go.Scatter(x=dates, y=normal,
                        mode='lines',
                        line=dict(color='blue',width=3),
                        name=labels[4]))
    fig.add_trace(go.Scatter(x=dates, y=elevated,
                        mode='lines',
                        line=dict(color='orange',width=3),
                        name=labels[3]))
    fig.add_trace(go.Scatter(x=dates, y=high,
                        mode='lines',
                        line=dict(color='brown',width=3),
                        name=labels[2]))
    fig.add_trace(go.Scatter(x=dates, y=very_high,
                        mode='lines',
                        line=dict(color='red',width=3),
                        name=labels[1]))
    fig.add_trace(go.Scatter(x=dates, y=reading,
                        mode='lines+markers',
                        line=dict(color='magenta',width=7),
                        name=labels[6]))
    fig.update_layout(title=labels[7],
                   xaxis_title='Date',
                   yaxis_title=labels[8],
                   xaxis=dict(showgrid=True), 
                   yaxis=dict(showgrid=True)
                   )
    st.plotly_chart(fig, use_container_width=True) 
    
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

def plotly_chart_blood_sugar(conn,patient_id,start_date,end_date,st):
    import pages.modules.blood_sugar as blood_sugar
    # data
    data = blood_sugar.get_readings_for_graph(conn,patient_id,start_date,end_date)
    dates,optimal,normal,elevated,high,very_high,reading = get_row_data_blood_sugar(data)
    if len(dates)<1:
        st.write("Insufficient readings to generate graph")
        return
    import plotly.graph_objects as go

    fig = go.Figure()
    
    # Add traces
    fig.add_trace(go.Scatter(x=dates, y=optimal,
                        mode='lines',
                        line=dict(color='green',width=5),
                        name='Optimal'))
    fig.add_trace(go.Scatter(x=dates, y=normal,
                        mode='lines',
                        line=dict(color='blue',width=5),
                        name='Normal'))
    fig.add_trace(go.Scatter(x=dates, y=elevated,
                        mode='lines',
                        line=dict(color='orange',width=5),
                        name='Elevated'))
    fig.add_trace(go.Scatter(x=dates, y=high,
                        mode='lines',
                        line=dict(color='brown',width=5),
                        name='High'))
    fig.add_trace(go.Scatter(x=dates, y=very_high,
                        mode='lines',
                        line=dict(color='red',width=5),
                        name='Very high'))
    fig.add_trace(go.Scatter(x=dates, y=reading,
                        mode='lines+markers',
                        line=dict(color='magenta',width=3),
                        name='Patient BGM Reading'))
    fig.update_layout(title='Blood Glucose Performance (Rated in Scale)',
                   xaxis_title='Reading date',
                   yaxis_title='Blood glucose reading in scale',
                   xaxis=dict(showgrid=True), 
                   yaxis=dict(showgrid=True)
                   )
    #st.write(fig)
    st.plotly_chart(fig, use_container_width=True)
def plotly_chart_hba1c(conn,patient_id,start_date,end_date,st):
    import pages.modules.hba1c as hba1c
    # data
    data = hba1c.get_readings_for_graph(conn,patient_id,start_date,end_date)
    dates,optimal,normal,elevated,high,very_high,reading = get_row_data_hba1c(data)
    if len(dates)<1:
       st.write("Insufficient readings to generate graph")
       return
    import plotly.graph_objects as go

    fig = go.Figure()
    
    # Add traces
    fig.add_trace(go.Scatter(x=dates, y=optimal,
                        mode='lines',
                        line=dict(color='green',width=4),
                        name='Optimal'))
    fig.add_trace(go.Scatter(x=dates, y=normal,
                        mode='lines',
                        line=dict(color='blue',width=5),
                        name='Normal'))
    fig.add_trace(go.Scatter(x=dates, y=elevated,
                        mode='lines',
                        line=dict(color='orange',width=7),
                        name='Elevated'))
    fig.add_trace(go.Scatter(x=dates, y=high,
                        mode='lines',
                        line=dict(color='brown',width=8),
                        name='High/Grade 1 hypo'))
    fig.add_trace(go.Scatter(x=dates, y=very_high,
                        mode='lines',
                        line=dict(color='red',width=10),
                        name='Very high/Grade 2 hypo'))
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
    st.plotly_chart(fig, use_container_width=True)   

def plotly_chart_blood_pressure(conn,patient_id,start_date,end_date,st):
    import pages.modules.blood_pressure as blood_pressure
    # data
    data = blood_pressure.get_readings_for_graph(conn,patient_id,start_date,end_date)
    dates,optimal,normal,elevated,high,very_high,reading = get_row_data_blood_pressure(data)
    if len(dates)<1:
        st.write("Insufficient readings to generate graph")
        return
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
    st.plotly_chart(fig, use_container_width=True)

def plotly_chart_lipid(conn,patient_id,start_date,end_date,st):
    import pages.modules.lipid as lipid
    # data
    data = lipid.get_readings_for_graph(conn,patient_id,start_date,end_date)
    dates,optimal,normal,elevated,high,very_high,reading = get_row_data_lipid(data)
    if len(dates)<1:
        st.write("Insufficient readings to generate graph")
        return
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
                        name='Near Normal'))
    fig.add_trace(go.Scatter(x=dates, y=elevated,
                        mode='lines',
                        line=dict(color='orange'),
                        name='Borderline High'))
    fig.add_trace(go.Scatter(x=dates, y=high,
                        mode='lines',
                        line=dict(color='brown'),
                        name='High'))
    fig.add_trace(go.Scatter(x=dates, y=very_high,
                        mode='lines',
                        line=dict(color='red'),
                        name='Severely High'))
    fig.add_trace(go.Scatter(x=dates, y=reading,
                        mode='lines+markers',
                        line=dict(color='magenta',width=7),
                        name='Patient Lipid Profile Reading'))
    fig.update_layout(title='Patient Lipid Profile performance',
                   xaxis_title='Date',
                   yaxis_title='Lipid profile reading in scale',
                   xaxis=dict(showgrid=True), 
                   yaxis=dict(showgrid=True)
                   )
    st.plotly_chart(fig, use_container_width=True)

def plotly_chart_bmi(conn,patient_id,start_date,end_date,st):
    import pages.modules.eye as eye
    # data
    data = eye.get_readings_for_graph(conn,patient_id,start_date,end_date)
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
    st.plotly_chart(fig, use_container_width=True)
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
    
def get_row_data_lipid(resultset):
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

def format_label(label):
    return '<span style="color:green; font-weight: bold;">'+str(label)+'</span>'
    
def format_warning(label):
    return '<span style="color:red; font-weight: bold;">'+str(label)+'</span>'
    
def target_summaries(pd, st, patient_id):
    df = pd.DataFrame(columns=["Care Target","MPC Score","Description","Concordance"])
  
        
    average_score = average_gradient = 0
    #blood sugar
    blood_sugar_score = st.session_state.blood_sugar_score
    blood_sugar_gradient = st.session_state.blood_sugar_gradient
    blood_sugar_score_description = blood_sugar.get_score_description(blood_sugar_score)
    blood_sugar_gradient_description = check_con_dis_cordance(blood_sugar_gradient,True)
    new_row = ["Blood Sugar",blood_sugar_score,blood_sugar_score_description,blood_sugar_gradient_description]
    df.loc[len(df.index)] = new_row
    average_score = blood_sugar_score
    average_gradient += blood_sugar_gradient
    
   
    
    
    #HBA1C
    hba1c_score = st.session_state.hba1c_score
    hba1c_gradient = st.session_state.hba1c_gradient
    hba1c_score_description = hba1c.get_score_description(hba1c_score)
    hba1c_gradient_description = check_con_dis_cordance(hba1c_gradient,True)
    new_row = ["HBA1C",hba1c_score,hba1c_score_description,hba1c_gradient_description]
    df.loc[len(df.index)] = new_row
    average_score += hba1c_score
    average_gradient += hba1c_gradient
    
    
    #BP
    blood_pressure_score = st.session_state.blood_pressure_score
    blood_pressure_gradient = st.session_state.blood_pressure_gradient
    blood_pressure_score_description = blood_pressure.get_score_description(blood_pressure_score)
    blood_pressure_gradient_description = check_con_dis_cordance(blood_pressure_gradient,True)
    new_row = ["Blood Pressure",blood_pressure_score,blood_pressure_score_description,blood_pressure_gradient_description]
    df.loc[len(df.index)] = new_row
    average_score += blood_pressure_score
    average_gradient += blood_pressure_gradient
    
    
    #lipid
    lipid_score = st.session_state.lipid_score
    lipid_gradient = st.session_state.lipid_gradient
    lipid_score_description = lipid.get_score_description(lipid_score)
    lipid_gradient_description = check_con_dis_cordance(lipid_gradient,True)
    new_row = ["Lipids",lipid_score,lipid_score_description,lipid_gradient_description]
    df.loc[len(df.index)] = new_row
    average_score += lipid_score
    average_gradient += lipid_gradient
    
    #BMI
    bmi_score = st.session_state.bmi_score
    bmi_gradient = st.session_state.bmi_gradient
    bmi_score_description = bmi.get_score_description(bmi_score)
    bmi_gradient_description = check_con_dis_cordance(bmi_gradient,True)
    new_row = ["BMI",bmi_score,bmi_score_description,bmi_gradient_description]
    df.loc[len(df.index)] = new_row
    average_score += bmi_score
    average_gradient += bmi_gradient
    
    
    #eye
    eye_score = st.session_state.eye_score
    eye_gradient = st.session_state.eye_gradient
    eye_score_description = eye.get_score_description(eye_score)
    eye_gradient_description = check_con_dis_cordance(eye_gradient,True)
    new_row = ["BMI",eye_score,eye_score_description,eye_gradient_description]
    df.loc[len(df.index)] = new_row
    average_score += eye_score
    average_gradient += eye_gradient
    
        
    #urine
    urine_score = st.session_state.urine_score
    urine_gradient = st.session_state.urine_gradient
    urine_score_description = urine.get_score_description(blood_sugar_score)
    urine_gradient_description = check_con_dis_cordance(urine_gradient,True)
    new_row = ["Urine",urine_score,urine_score_description,urine_gradient_description]
    df.loc[len(df.index)] = new_row
    average_score += urine_score
    average_gradient += urine_gradient
    
    #eye
    eye_score = st.session_state.eye_score
    eye_gradient = st.session_state.eye_gradient
    eye_score_description = eye.get_score_description(eye_score)
    eye_gradient_description = check_con_dis_cordance(eye_gradient,True)
    new_row = ["Eye Tests",eye_score,eye_score_description,eye_gradient_description]
    df.loc[len(df.index)] = new_row
    average_score += eye_score
    average_gradient += eye_gradient
    
    #monofilament
    monofilament_score = st.session_state.monofilament_score
    monofilament_gradient = st.session_state.monofilament_gradient
    monofilament_score_description = monofilament.get_score_description(monofilament_score)
    monofilament_gradient_description = check_con_dis_cordance(monofilament_gradient,True)
    new_row = ["10g Monofilament",monofilament_score,monofilament_score_description,monofilament_gradient_description]
    df.loc[len(df.index)] = new_row
    average_score += monofilament_score
    average_gradient += monofilament_gradient
    
    #diet
    diet_score = st.session_state.diet_score
    diet_gradient = st.session_state.diet_gradient
    diet_score_description = diet.get_score_description(diet_score)
    diet_gradient_description = check_con_dis_cordance(diet_gradient,True)
    new_row = ["Diet",diet_score,diet_score_description,diet_gradient_description]
    df.loc[len(df.index)] = new_row
    average_score += diet_score
    average_gradient += diet_gradient
    
    #physical activity
    physical_activity_score = st.session_state.physical_activity_score
    physical_activity_gradient = st.session_state.physical_activity_gradient
    physical_activity_score_description = physical_activity.get_score_description(blood_sugar_score)
    physical_activity_gradient_description = check_con_dis_cordance(physical_activity_gradient,True)
    new_row = ["Physical Activity",physical_activity_score,physical_activity_score_description,physical_activity_gradient_description]
    df.loc[len(df.index)] = new_row
    average_score += physical_activity_score
    average_gradient += physical_activity_gradient
    
    #education
    education_score = st.session_state.education_score
    education_gradient = st.session_state.education_gradient
    education_score_description = education.get_score_description(education_score)
    education_gradient_description = check_con_dis_cordance(education_gradient,True)
    new_row = ["Education",education_score,education_score_description,education_gradient_description]
    df.loc[len(df.index)] = new_row
    average_score += education_score
    average_gradient += education_gradient
    
    #health system
    health_system_score = st.session_state.health_system_score
    health_system_gradient = st.session_state.health_system_gradient
    health_system_score_description = health_system.get_score_description(health_system_score)
    health_system_gradient_description = check_con_dis_cordance(health_system_gradient,True)
    new_row = ["Health System",health_system_score,health_system_score_description,health_system_gradient_description]
    df.loc[len(df.index)] = new_row
    average_score += health_system_score
    average_gradient += health_system_gradient
    
    #comorbidity
    comorbidity_score = st.session_state.comorbidity_score
    comorbidity_gradient = st.session_state.comorbidity_gradient
    comorbidity_score_description = comorbidity.get_score_description(comorbidity_score)
    comorbidity_gradient_description = check_con_dis_cordance(comorbidity_gradient,True)
    new_row = ["Comorbidity",comorbidity_score,comorbidity_score_description,comorbidity_gradient_description]
    df.loc[len(df.index)] = new_row
    average_score += comorbidity_score
    average_gradient += comorbidity_gradient
    
    #socioeconomic
    socioeconomic_score = st.session_state.socioeconomic_score
    socioeconomic_gradient = st.session_state.socioeconomic_gradient
    socioeconomic_score_description = socioeconomic.get_score_description(socioeconomic_score)
    socioeconomic_gradient_description = check_con_dis_cordance(socioeconomic_gradient,True)
    new_row = ["Socioeconomic",socioeconomic_score,socioeconomic_score_description,socioeconomic_gradient_description]
    df.loc[len(df.index)] = new_row
    average_score += socioeconomic_score
    average_gradient += socioeconomic_gradient
    
    #Summary
    average_score = math.ceil(average_score/14)
    average_gradient = average_gradient/14
    averages_score_description = get_score_description(math.floor(average_score))
    average_gradient_description = check_con_dis_cordance(average_gradient,True)
    
    
    
    #new_row = ["Overall",average_score,averages_score_description,average_gradient_description]
    #df.loc[len(df.index)] = new_row
    
    st.write("Generally, the patient is " + str(average_gradient_description.lower()) + " with treatement, rated to have " + str(averages_score_description.lower()) + ", with  a score of " + str(average_score) + " out of 5.")
    
    df = df.set_index('Care Target')
    #st.write(df,use_container_width=True)
    
    df = df.drop(columns=["Description","Concordance"])
    
    #st.bar_chart(df)
    
    target,score,description,concordance,button = st.columns(5)
    
    with target:
        st.write("**Care Target**")
    with score:
        st.write("**MPC Score (out of 5)**")
    with description:
        st.write("**Description**")
    with concordance:
        st.write("**Concordance**")
    with button:
        st.write("**Action**")
    
    with target:
        st.write("1. Blood Sugar")
    with score:
        st.write(str(blood_sugar_score))
    with description:
        st.write(blood_sugar_score_description)
    with concordance:
        st.write(blood_sugar_gradient_description)
    with button:
        st.write("[view more](Data_analysis_II?patient="+ str(patient_id) + "&target=blood_sugar)")
        
    with target:
        st.write("2. HBA1C")
    with score:
        st.write(str(hba1c_score))
    with description:
        st.write(hba1c_score_description)
    with concordance:
        st.write(hba1c_gradient_description)
    with button:
        st.write("[view more](Data_analysis_II?patient="+ str(patient_id) + "&target=hba1c)")
        
    with target:
        st.write("3. Blood Pressure")
    with score:
        st.write(str(blood_pressure_score))
    with description:
        st.write(blood_pressure_score_description)
    with concordance:
        st.write(blood_pressure_gradient_description)
    with button:
        st.write("[view more](Data_analysis_II?patient="+ str(patient_id) + "&target=blood_pressure)")
    
    with target:
        st.write("4. Lipids")
    with score:
        st.write(str(lipid_score))
    with description:
        st.write(lipid_score_description)
    with concordance:
        st.write(lipid_gradient_description)
    with button:
        st.write("[view more](Data_analysis_II?patient="+ str(patient_id) + "&target=lipid)")
        
    with target:
        st.write("5. BMI")
    with score:
        st.write(str(bmi_score))
    with description:
        st.write(bmi_score_description)
    with concordance:
        st.write(bmi_gradient_description)
    with button:
        st.write("[view more](Data_analysis_II?patient="+ str(patient_id) + "&target=bmi)")
        
    with target:
        st.write("6. Urine")
    with score:
        st.write(str(urine_score))
    with description:
        st.write(urine_score_description)
    with concordance:
        st.write(urine_gradient_description)
    with button:
        st.write("[view more](Data_analysis_II?patient="+ str(patient_id) + "&target=urine)")
        
    with target:
        st.write("7. Eye")
    with score:
        st.write(str(eye_score))
    with description:
        st.write(eye_score_description)
    with concordance:
        st.write(eye_gradient_description)    
    with button:
        st.write("[view more](Data_analysis_II?patient="+ str(patient_id) + "&target=eye)")
        
    with target:
        st.write("8. Monofilament")
    with score:
        st.write(str(monofilament_score))
    with description:
        st.write(monofilament_score_description)
    with concordance:
        st.write(monofilament_gradient_description)        
    with button:
        st.write("[view more](Data_analysis_II?patient="+ str(patient_id) + "&target=monofilament)")
        
    with target:
        st.write("9. Diet")
    with score:
        st.write(str(diet_score))
    with description:
        st.write(diet_score_description)
    with concordance:
        st.write(diet_gradient_description)
    with button:
        st.write("[view more](Data_analysis_II?patient="+ str(patient_id) + "&target=diet)")
        
    with target:
        st.write("10. Physical Activity")
    with score:
        st.write(str(physical_activity_score))
    with description:
        st.write(physical_activity_score_description)
    with concordance:
        st.write(physical_activity_gradient_description)
    with button:
        st.write("[view more](Data_analysis_II?patient="+ str(patient_id) + "&target=physical_activity)")
        
    with target:
        st.write("11. Education")
    with score:
        st.write(str(education_score))
    with description:
        st.write(education_score_description)
    with concordance:
        st.write(education_gradient_description)
    with button:
        st.write("[view more](Data_analysis_II?patient="+ str(patient_id) + "&target=education)")
        
    with target:
        st.write("12. Comorbidity")
    with score:
        st.write(str(comorbidity_score))
    with description:
        st.write(comorbidity_score_description)
    with concordance:
        st.write(comorbidity_gradient_description)
    with button:
        st.write("[view more](Data_analysis_II?patient="+ str(patient_id) + "&target=comorbidity)")
       
        
    with target:
        st.write("13. Health System")
    with score:
        st.write(str(health_system_score))
    with description:
        st.write(health_system_score_description)
    with concordance:
        st.write(health_system_gradient_description)
    with button:
        st.write("[view more](Data_analysis_II?patient="+ str(patient_id) + "&target=health_system)")
        
    with target:
        st.write("14. Socioeconomic")
    with score:
        st.write(str(socioeconomic_score))
    with description:
        st.write(socioeconomic_score_description)
    with concordance:
        st.write(socioeconomic_gradient_description)
    with button:
        st.write("[view more](Data_analysis_II?patient="+ str(patient_id) + "&target=socioeconomic)")


    
def target_correlations(conn, patient, pd, st):
    df = pd.DataFrame(columns=["Period/Date","HBA1C","Blood Pressure","Lipids","BMI","Urine","Eye","Monofilament","Diet","Physical Activity","Education","Comorbidity","Health System","Socioeconomic"])
    df_scores = pd.DataFrame(columns=["Period/Date","HBA1C","Blood Pressure","Lipids","BMI","Urine","Eye","Monofilament","Diet","Physical Activity","Education","Comorbidity","Health System","Socioeconomic"])
    
    #date difference
    daignosis_date = patient[12] #diagnosis date 
    today_date = date.today()
    today = today_date.strftime('%Y-%m-%d')
    duration,months = number_of_months(daignosis_date,today)
    st.write("Duration: ",duration)
    
    #initial date readings
    hba1c_initial_readings_scores, hba1c_initial_readings = hba1c.initial_diagnosis_correlation_readings(conn, patient[0], daignosis_date)
    blood_pressure_initial_readings_scores, blood_pressure_initial_readings = blood_pressure.initial_diagnosis_correlation_readings(conn, patient[0], daignosis_date)
    lipid_initial_readings_scores, lipid_initial_readings = lipid.initial_diagnosis_correlation_readings(conn, patient[0], daignosis_date)
    bmi_initial_readings_scores, bmi_initial_readings = bmi.initial_diagnosis_correlation_readings(conn, patient[0], daignosis_date)
    urine_initial_readings_scores, urine_initial_readings = urine.initial_diagnosis_correlation_readings(conn, patient[0], daignosis_date)
    eye_initial_readings_scores, eye_initial_readings = eye.initial_diagnosis_correlation_readings(conn, patient[0], daignosis_date)
    monofilament_initial_readings_scores, monofilament_initial_readings = monofilament.initial_diagnosis_correlation_readings(conn, patient[0], daignosis_date)
    diet_initial_readings_scores, diet_initial_readings = diet.initial_diagnosis_correlation_readings(conn, patient[0], daignosis_date)
    physical_activity_initial_readings_scores, physical_activity_initial_readings = physical_activity.initial_diagnosis_correlation_readings(conn, patient[0], daignosis_date)
    education_initial_readings_scores, education_initial_readings = education.initial_diagnosis_correlation_readings(conn, patient[0], daignosis_date)
    comorbidity_initial_readings_scores, comorbidity_initial_readings = comorbidity.initial_diagnosis_correlation_readings(conn, patient[0], daignosis_date)
    health_system_initial_readings_scores, health_system_initial_readings = health_system.initial_diagnosis_correlation_readings(conn, patient[0], daignosis_date)
    socioeconomic_initial_readings_scores, socioeconomic_initial_readings = socioeconomic.initial_diagnosis_correlation_readings(conn, patient[0], daignosis_date)
    daignosis_date_str = "As at " + str(daignosis_date)
    
    #add the date readings into the datframe
    new_row = [daignosis_date,hba1c_initial_readings,blood_pressure_initial_readings,lipid_initial_readings,bmi_initial_readings,\
    urine_initial_readings,eye_initial_readings,monofilament_initial_readings,diet_initial_readings,physical_activity_initial_readings,\
    education_initial_readings,comorbidity_initial_readings,health_system_initial_readings,socioeconomic_initial_readings]
    
    new_row_scores = [daignosis_date,hba1c_initial_readings_scores,blood_pressure_initial_readings_scores,lipid_initial_readings_scores,bmi_initial_readings_scores,\
    urine_initial_readings_scores,eye_initial_readings_scores,monofilament_initial_readings_scores,diet_initial_readings_scores,physical_activity_initial_readings_scores,\
    education_initial_readings_scores,comorbidity_initial_readings_scores,health_system_initial_readings_scores,socioeconomic_initial_readings_scores]
    
    df.loc[len(df.index)] = new_row
    df_scores.loc[len(df_scores.index)] = new_row_scores
    
    #subsequent readings
    phases = math.ceil(months/12)
    old_date = datetime.strptime(daignosis_date, '%Y-%m-%d')
    for phase in range(phases):
        old_date_str = old_date.strftime('%Y-%m-%d')
        new_daignosis_date = datetime.strptime(old_date_str, '%Y-%m-%d')
        new_date = pd.to_datetime(old_date_str)+pd.DateOffset(months=12)
        if new_date > pd.Timestamp(today_date):
            new_date = pd.to_datetime(today)
        new_date_str = new_date.strftime('%Y-%m-%d')
        #capture readings as at new date
        hba1c_initial_readings_scores,hba1c_initial_readings = hba1c.initial_diagnosis_correlation_readings_more(conn, patient[0], old_date_str,new_date_str,hba1c_initial_readings,hba1c_initial_readings_scores)
        lipid_initial_readings_scores, lipid_initial_readings = lipid.initial_diagnosis_correlation_readings_more(conn, patient[0], old_date_str,new_date_str,lipid_initial_readings, lipid_initial_readings_scores)
        blood_pressure_initial_readings_scores, blood_pressure_initial_readings = blood_pressure.initial_diagnosis_correlation_readings_more(conn, patient[0], old_date_str,new_date_str,blood_pressure_initial_readings, blood_pressure_initial_readings_scores)
        bmi_initial_readings_scores, bmi_initial_readings = bmi.initial_diagnosis_correlation_readings_more(conn, patient[0], old_date_str,new_date_str,bmi_initial_readings, bmi_initial_readings_scores)
        urine_initial_readings_scores, urine_initial_readings = urine.initial_diagnosis_correlation_readings_more(conn, patient[0], old_date_str,new_date_str,urine_initial_readings, urine_initial_readings_scores)
        eye_initial_readings_scores, eye_initial_readings = eye.initial_diagnosis_correlation_readings_more(conn, patient[0], old_date_str,new_date_str,eye_initial_readings, eye_initial_readings_scores)
        monofilament_initial_readings_scores, monofilament_initial_readings = monofilament.initial_diagnosis_correlation_readings_more(conn, patient[0], old_date_str,new_date_str,monofilament_initial_readings, monofilament_initial_readings_scores)
        diet_initial_readings_scores, diet_initial_readings = diet.initial_diagnosis_correlation_readings_more(conn, patient[0], old_date_str,new_date_str,diet_initial_readings, diet_initial_readings_scores)
        physical_activity_initial_readings_scores, physical_activity_initial_readings = physical_activity.initial_diagnosis_correlation_readings_more(conn, patient[0], old_date_str,new_date_str,physical_activity_initial_readings, physical_activity_initial_readings_scores)
        education_initial_readings_scores, education_initial_readings = education.initial_diagnosis_correlation_readings_more(conn, patient[0], old_date_str,new_date_str,education_initial_readings, education_initial_readings_scores)
        comorbidity_initial_readings_scores, comorbidity_initial_readings = comorbidity.initial_diagnosis_correlation_readings_more(conn, patient[0], old_date_str,new_date_str,comorbidity_initial_readings, comorbidity_initial_readings_scores)
        health_system_initial_readings_scores, health_system_initial_readings = health_system.initial_diagnosis_correlation_readings_more(conn, patient[0], old_date_str,new_date_str,health_system_initial_readings, health_system_initial_readings_scores)
        socioeconomic_initial_readings_scores, socioeconomic_initial_readings = socioeconomic.initial_diagnosis_correlation_readings_more(conn, patient[0], old_date_str,new_date_str,socioeconomic_initial_readings, socioeconomic_initial_readings_scores)
        
        #add the date readings into the datframe
        new_row = [new_date_str,hba1c_initial_readings,blood_pressure_initial_readings,lipid_initial_readings,bmi_initial_readings,\
        urine_initial_readings,eye_initial_readings,monofilament_initial_readings,diet_initial_readings,physical_activity_initial_readings,\
        education_initial_readings,comorbidity_initial_readings,health_system_initial_readings,socioeconomic_initial_readings]
        df.loc[len(df.index)] = new_row
        
        new_row_scores = [new_date_str,hba1c_initial_readings_scores,blood_pressure_initial_readings_scores,lipid_initial_readings_scores,bmi_initial_readings_scores,\
        urine_initial_readings_scores,eye_initial_readings_scores,monofilament_initial_readings_scores,diet_initial_readings_scores,physical_activity_initial_readings_scores,\
        education_initial_readings_scores,comorbidity_initial_readings_scores,health_system_initial_readings_scores,socioeconomic_initial_readings_scores]
        df_scores.loc[len(df_scores.index)] = new_row_scores
    
        #progress date
        old_date = new_date

    df = df.set_index('Period/Date')
    df_scores = df_scores.set_index('Period/Date')
    
    st.write("Dataset")
    st.write(df)
    st.write("Correlation Matrix")
    st.write(df.corr(method='pearson'))
    
    ## Proceed to Logistic Regression with the same dataset
    #st.write("Dataset")
    logistic_regression(df_scores, st, pd)
    
def target_correlations_initial_readings(patient, pd, st):
    cursor = conn.cursor()
    sql = "SELECT reading_date,scale FROM hba1c WHERE patient_id = " + str(patient_id) + ""
    if start_date:
        sql += " AND reading_date BETWEEN DATE('" + str(start_date) + "') AND DATE('" + str(end_date) + "') ORDER BY reading_date ASC";
    else:
       sql += " ORDER BY reading_date DESC LIMIT 10 "
    cursor=conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall() #database query to retrieve readings
    
    
def logistic_regression(df_scores, st, pd):
    st.subheader("Logistic Regression between Care Targets (independent variables) and HBA1C (dependent variable)")
    st.write("Dataset")
    st.write(df_scores)
    #from ordinal import OrderedLogit
    from statsmodels.miscmodels.ordinal_model import OrderedModel
    
    #convert to categorical
    cols1 = ['HBA1C']
    df_scores[cols1] = df_scores[cols1].astype('category')
    
    #convert to float
    cols2 = ["Blood Pressure","Lipids","BMI","Urine","Eye","Monofilament","Diet","Physical Activity","Education","Comorbidity","Health System","Socioeconomic"]
    df_scores[cols2] = df_scores[cols2].astype('float')
    
    import numpy as np
    import pandas as pd
    #data types
    #st.write(df_scores.dtypes)
    
    
    #st.write(df_scores['HBA1C'].dtype)

    # Select features and target variable
    X = df_scores[["Blood Pressure","Lipids","BMI","Urine","Eye","Monofilament","Diet","Physical Activity","Education","Comorbidity","Health System","Socioeconomic"]]  # Replace with your feature names
    y = df_scores["HBA1C"]
    
    #st.write(df_scores['HBA1C'])
    
    # Fit the ordinal regression model
    model = OrderedModel(y, X, distr='logit',hasconst=False)
    res_log = model.fit(method='bfgs', disp=False)
      
    
    #st.write(regr)

    # Split data into training and testing sets
    #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    # Create a logistic regression model instance
    #model = LogisticRegression()

    # Train the model on the training data
    #model.fit(X_train, y_train)

    # Make predictions on the testing data
    #y_pred = model.predict(X_test)

    # Print model coefficients and intercept
    #st.write(res_log.summary())
    #st.write("Intercept:", model.intercept_)
    
    df = pd.read_html(res_log.summary().tables[1].as_html(),header=0,index_col=0)[0]
    
    #formula
    
    formula = "Y-Glycaemia=" 
    
    a=df['coef'].values[1]
    bp=df['coef'].values[0]
    
    st.write("Y-Glycaemia = ",df['coef'].values[0],"Blood Pressure + ",df['coef'].values[1],"Lipids + ",df['coef'].values[2],"BMI + ",df['coef'].values[3],"Urine + ",df['coef'].values[4],"Eye + ",\
    df['coef'].values[5],"Monofilament + ",df['coef'].values[6],"Diet + ",df['coef'].values[7],"Physical Activity + ",df['coef'].values[8],"Education + ",df['coef'].values[10],"Comorbidity + ",df['coef'].values[11],"Health System + ",df['coef'].values[12],"Socioeconomic")
    
    
