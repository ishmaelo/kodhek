def get_readings_for_display(conn,patient_id,start_date,end_date):
    cursor = conn.cursor()
    sql = "SELECT reading_date,dbp, sbp, mean_abp, description FROM bp_reading WHERE patient_id = " + str(patient_id) + ""
    if start_date:
        sql += " AND reading_date BETWEEN DATE('" + str(start_date) + "') AND DATE('" + str(end_date) + "') ORDER BY reading_date ASC";
    else:
       sql += " ORDER BY reading_date DESC LIMIT 10 "
    cursor=conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall() #database query to retrieve readings
def get_readings_for_graph(conn,patient_id,start_date,end_date):
    cursor = conn.cursor()
    sql = "SELECT reading_date,scale FROM bp_reading WHERE patient_id = " + str(patient_id) + ""
    if start_date:
        sql += " AND reading_date BETWEEN DATE('" + str(start_date) + "') AND DATE('" + str(end_date) + "') ORDER BY reading_date ASC";
    else:
       sql += " ORDER BY reading_date DESC LIMIT 10 "
    cursor=conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall() #database query to retrieve readings
    
def get_readings_for_score(conn,patient_id,start_date,end_date,st,utility,compute):
    cursor = conn.cursor()
    sql = "SELECT score FROM bp_reading WHERE patient_id = " + str(patient_id) + ""
    if start_date:
        sql += " AND reading_date BETWEEN DATE('" + str(start_date) + "') AND DATE('" + str(end_date) + "') ORDER BY reading_date ASC";
    else:
        sql += " ORDER BY reading_date DESC LIMIT 10 "
    cursor=conn.cursor()
    cursor.execute(sql)
    readings = cursor.fetchall()
    average_score = 0
    divider = 0
    for row in readings:
        average_score += row[0]
        divider += 1
    if divider == 0:
        average_score = 0
    else:
        average_score = round(average_score / divider)
        #st.write("**MPC Scoring**")
        description = get_score_description(average_score)
        score_str = utility.format_label(str(average_score)+ ", " + description)
        if not compute:
            st.markdown("MPC Score: " +  score_str, unsafe_allow_html=True)
    st.session_state.blood_pressure_score = average_score
    
    return divider
    
def get_readings_for_concordance(conn,patient_id,start_date,end_date,st,pd, utility,compute):
    import numpy as np
    import matplotlib.pyplot as plt
    
    cursor = conn.cursor()
    sql = "SELECT reading_date,score FROM bp_reading WHERE patient_id = " + str(patient_id) + ""
    if start_date:
        sql += " AND reading_date BETWEEN DATE('" + str(start_date) + "') AND DATE('" + str(end_date) + "') ORDER BY reading_date ASC";
    else:
        sql += " ORDER BY reading_date DESC LIMIT 10 "
    cursor=conn.cursor()
    cursor.execute(sql)
    readings = cursor.fetchall()
    scores = list()
    dates = list()
    for row in readings:
        dates.append(row[0])
        scores.append(row[1])
    
    dates = np.array(dates)
    dates = pd.to_datetime(dates).map(lambda d: d.toordinal())
    scores = np.array(scores)
   #plot
    b = estimate_linear_regression_coefs(np,dates, scores)
    intercept, gradient = b
    conco = utility.check_con_dis_cordance(gradient,True)  
    conco_str = utility.format_label(conco)
    
    #st.write("Gradient: ",gradient)
    #st.markdown(conco, unsafe_allow_html=True)
    if not compute:
        plot_regression_line(dates, scores, b, st)
        st.markdown("Concordance: " + conco_str,unsafe_allow_html=True)
    st.session_state.blood_pressure_gradient = gradient
    
    
def estimate_linear_regression_coefs(np, x, y):
  # number of observations/points
  n = np.size(x)
 
  # mean of x and y vector
  m_x = np.mean(x)
  m_y = np.mean(y)
 
  # calculating cross-deviation and deviation about x
  SS_xy = np.sum(y*x) - n*m_y*m_x
  SS_xx = np.sum(x*x) - n*m_x*m_x
 
  # calculating regression coefficients
  b_1 = SS_xy / SS_xx
  b_0 = m_y - b_1*m_x
 
  return  (b_0, b_1)
  
def plot_regression_line(x, y, b, st):
  import matplotlib.pyplot as plt
  plt.clf()  
  # plotting the actual points as scatter plot
  plt.scatter(x, y, color = "b",
        marker = "x", s = 30)
 
  # predicted response vector
  y_pred = b[0] + b[1]*x
 
  # plotting the regression line
  plot = plt.plot(x, y_pred, color = "m")
 
  # putting labels
  plt.xlabel('Reading Dates')
  plt.ylabel('Blood Pressure Scores')
  st.pyplot(plt)
  #plt.show()
def check_con_dis_cordance(b):
    if b > 0:
        return '<p style="color:green; font-weight: bold;">Concordant</p>'
    else:
        return '<p style="color:red;font-weight: bold;">Discordant</p>'
  
def get_score_description(index):
    scores = ["Undefined","Grade 3/urgency","Grade 2","Grade 1","High Normal","Normal"]
    return scores[index]
    
    
def load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,start_date,end_date,date_range,widgets,components,compute):
    if not compute:
        st.markdown("""---""")
        st.subheader("3. Blood Pressure")
    readings = get_readings_for_display(conn,patient_id,start_date,end_date)
    if not compute:
        readings_on_table_display(readings,st,date_range)  
        utility.plotly_chart_blood_pressure(conn,patient_id,start_date,end_date,st)
    value = get_readings_for_score(conn,patient_id,start_date,end_date,st,utility,compute)
    if value > 0:
        get_readings_for_concordance(conn,patient_id,start_date,end_date,st,pd,utility,compute)
    if not compute:    
        set_data_capture_form(conn,patient_id,st,widgets,components)
  
def readings_on_table_display(readings,st,date_range):
    if len(readings)<1:
      st.write("Insufficient readings to display the table")
      return
    st.write("**Blood Pressure " + date_range + "**")
    date, bp, mbp, description = st.columns(4)
    with date:
       st.write("**Date**")
    with bp:
       st.write("**Blood Pressure Reading**")
    with mbp:
       st.write("**Mean Arterial BP**")
    with description:
       st.write("**Description**")
    i = 0
    date_reading = list()
    new_format = '%Y-%m-%d'
    for row in readings:
        with date:
           st.write(row[0])
        with bp:
           st.write(str(row[1]),'/',str(row[2]))
        with mbp:
           st.write(str(row[3]))
        with description:
           st.write(row[4])
        i += 1
       
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
    
def initial_diagnosis_correlation_readings(conn, patient_id, diagnosis_date):
    cursor = conn.cursor()
    sql = "SELECT scale, score FROM bp_reading WHERE patient_id = " + str(patient_id) + " AND reading_date = '" + str (diagnosis_date) + "'";
    cursor.execute(sql)
    rows = cursor.fetchall()
    reading = reading_scores = 1
    for row in rows:
        reading = row[0]
        reading_scores = row[1]
    return reading_scores, reading
    
def initial_diagnosis_correlation_readings_more(conn, patient_id, old_date_str,new_date_str, initial_readings, initial_readings_scores):
    cursor = conn.cursor()
    sql = "SELECT scale, score FROM bp_reading WHERE patient_id = " + str(patient_id) + " AND reading_date BETWEEN DATE('" + str(old_date_str) + "') AND DATE('" + str(new_date_str) + "')"
    cursor.execute(sql)
    rows = cursor.fetchall()
    reading = initial_readings
    if initial_readings_scores<=3:
        initial_readings_scores = initial_readings_scores - 0.01
    else:
        if initial_readings_scores<5:
            initial_readings_scores = initial_readings_scores + 0.01
    reading_scores = initial_readings_scores
    divider = average_score = average_score_scores = 0
    for row in rows:
        average_score += row[0]
        average_score_scores += row[1]
        divider += 1
       
    if divider > 0:
        reading = average_score/divider
        reading_scores = average_score_scores/divider
    return reading_scores, reading
    
def save_to_db(conn,patient_id,reading_date,dbp,sbp,mean_abp,scale,score,description,mpc):
    conn.execute(f'''
            INSERT INTO bp_reading (patient_id,reading_date,dbp,sbp,mean_abp,scale,score,description,mpc) 
            VALUES 
            ('{patient_id}','{reading_date}','{dbp}','{sbp}','{mean_abp}','{scale}','{score}','{description}','{mpc}')
            ''')
    conn.commit()    
    
def set_data_capture_form(conn,patient_id,st,widgets,components,age=''):   
    ##modal widgets##
    modal = widgets.create_modal_widget("Capture blood pressure reading","blood_pressure",50,600)
    open_modal = st.button("Capture blood pressure reading","blood_pressure")
    
    if open_modal:
        modal.open()
        
    if modal.is_open():
       
        with modal.container():
            result = ''
            mpc = ''
            score = ''
            scale = ''
            reading_date = st.date_input("Reading date",format="YYYY-MM-DD",key="bp-date")
            systolic = st.number_input("Systolic in mm Hg",key="bp-systolic")
            diastolic = st.number_input("Diastolic in mm Hg",key="bp-diastolic")
            st.write('Age:',age)
            if st.button('Submit reading',key="bp-submit"):
                if (systolic >= 100 and systolic <= 129) or (diastolic >= 60 and diastolic < 84):
                    result = 'Normal'
                    mpc = 1
                    score = 5
        
                if (systolic >= 130 and systolic <= 139) or (diastolic >= 85 and diastolic < 89):
                    result = 'High normal'
                    mpc = 2
                    score = 4
                   
                if (systolic >= 140 and systolic <= 159) or (diastolic >= 90 and diastolic < 99):
                    result = 'Grade 1'
                    mpc = 3
                    score = 3
                    st.warning(result)        
                if (systolic >= 160 and systolic <= 179) or (diastolic >= 100 and diastolic < 109):
                    result = 'Grade 2'
                    mpc = 4
                    score = 2
                    st.error(result)
                if (systolic >= 180 and diastolic >= 110) or (systolic < 100 and diastolic < 60):
                    result = 'Grade 3/urgency'
                    mpc = 5
                    score = 1
                    st.error(result)
                if not result:
                    st.error('You have not entered valid inputs, please try again')
                else:
                    description = result
                    scale = mpc
                    mean_abp = (2*diastolic + systolic)/3
                    save_to_db(conn,patient_id,reading_date,diastolic,systolic,mean_abp,scale,score,description,mpc)
                    st.success("Reading saved")
