import pages.modules.blood_sugar as blood_sugar
import pages.modules.hba1c as hba1c
import pages.modules.blood_pressure as blood_pressure
import pages.modules.lipid as lipid
import pages.modules.bmi as bmi

import math

from datetime import date
from datetime import datetime
from dateutil import relativedelta

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
    
    today = date.today()
    birth_date = datetime.strptime(birth_date, '%d/%m/%Y')
    age = today.year - birth_date.year
    full_year_passed = (today.month, today.day) < (birth_date.month, birth_date.day)
    if not full_year_passed:
        age -= 1
    return age
    
def number_of_months(start_date,end_date):
 
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    
    r = relativedelta.relativedelta(end_date, start_date)
    total_months = r.months + (12*r.years)
    return total_months

def patient_header_info(patient,st):    
    st.link_button("Back to list of patients", "Patients")
    patient_id = patient[0]
    st.title(patient[1])
    age = ", {} {}".format(get_age(patient[2]), ' years')
    st.write(patient[3], age)
    st.write("Diabetic since ", patient[12])
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
    hba1c_gradient_description = check_con_dis_cordance(hba1c_gradient,True)
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
    
    
def target_correlations(conn, patient, pd, st):
    df = pd.DataFrame(columns=["Period/Date","HBA1C","Blood Pressure","Lipids","BMI"])
    df_scores = pd.DataFrame(columns=["Period/Date","HBA1C","Blood Pressure","Lipids","BMI"])
    
    #date difference
    daignosis_date = patient[12] #diagnosis date 
    today_date = date.today()
    today = today_date.strftime('%Y-%m-%d')
    duration = number_of_months(daignosis_date,today)
    st.write("Duration: ",duration, " months")
    
    #initial date readings
    hba1c_initial_readings_scores, hba1c_initial_readings = hba1c.initial_diagnosis_correlation_readings(conn, patient[0], daignosis_date)
    lipid_initial_readings_scores, lipid_initial_readings = lipid.initial_diagnosis_correlation_readings(conn, patient[0], daignosis_date)
    blood_pressure_initial_readings_scores, blood_pressure_initial_readings = blood_pressure.initial_diagnosis_correlation_readings(conn, patient[0], daignosis_date)
    bmi_initial_readings_scores, bmi_initial_readings = bmi.initial_diagnosis_correlation_readings(conn, patient[0], daignosis_date)
    daignosis_date_str = "As at " + str(daignosis_date)
    
    #add the date readings into the datframe
    new_row = [daignosis_date,hba1c_initial_readings,blood_pressure_initial_readings,lipid_initial_readings,bmi_initial_readings]
    new_row_scores = [daignosis_date,hba1c_initial_readings_scores,blood_pressure_initial_readings_scores,lipid_initial_readings_scores,bmi_initial_readings_scores]
    
    df.loc[len(df.index)] = new_row
    df_scores.loc[len(df_scores.index)] = new_row_scores
    
    #subsequent readings
    phases = math.ceil(duration/3)+1
    old_date = datetime.strptime(daignosis_date, '%Y-%m-%d')
    for phase in range(phases):
        old_date_str = old_date.strftime('%Y-%m-%d')
        new_daignosis_date = datetime.strptime(old_date_str, '%Y-%m-%d')
        new_date = pd.to_datetime(old_date_str)+pd.DateOffset(months=3)
        if new_date > pd.Timestamp(today_date):
            new_date = pd.to_datetime(today)
        new_date_str = new_date.strftime('%Y-%m-%d')
        #capture readings as at new date
        hba1c_initial_readings_scores,hba1c_initial_readings = hba1c.initial_diagnosis_correlation_readings_more(conn, patient[0], old_date_str,new_date_str,hba1c_initial_readings,hba1c_initial_readings_scores)
        lipid_initial_readings_scores, lipid_initial_readings = lipid.initial_diagnosis_correlation_readings_more(conn, patient[0], old_date_str,new_date_str,lipid_initial_readings, lipid_initial_readings_scores)
        blood_pressure_initial_readings_scores, blood_pressure_initial_readings = blood_pressure.initial_diagnosis_correlation_readings_more(conn, patient[0], old_date_str,new_date_str,blood_pressure_initial_readings, blood_pressure_initial_readings_scores)
        bmi_initial_readings_scores, bmi_initial_readings = bmi.initial_diagnosis_correlation_readings_more(conn, patient[0], old_date_str,new_date_str,bmi_initial_readings, bmi_initial_readings_scores)
        
        #add the date readings into the datframe
        new_row = [new_date_str,hba1c_initial_readings,blood_pressure_initial_readings,lipid_initial_readings,bmi_initial_readings]
        df.loc[len(df.index)] = new_row
        
        new_row_scores = [new_date_str,hba1c_initial_readings_scores,blood_pressure_initial_readings_scores,lipid_initial_readings_scores,bmi_initial_readings_scores]
        df_scores.loc[len(df_scores.index)] = new_row_scores
    
        #progress date
        old_date = new_date

    df = df.set_index('Period/Date')
    df_scores = df_scores.set_index('Period/Date')
    
    st.write(df)
    st.write(df.corr(method='pearson'))
    
    ## Proceed to Logistic Regression with the same dataset
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
    st.subheader("Part IV - Logistic Regression between Care Targets (independent variables) and HBA1C (dependent variable) [from scores]")
    st.write(df_scores)
    from sklearn import linear_model

    # Select features and target variable
    X = df_scores[["Blood Pressure","Lipids","BMI"]]  # Replace with your feature names
    y = df_scores["HBA1C"]
    
    model = linear_model.LinearRegression()
    model.fit(X, y)
    
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
    st.write("Coefficients:", model.coef_)
    st.write("Intercept:", model.intercept_)
    
    
