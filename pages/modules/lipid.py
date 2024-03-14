def get_readings_for_display(conn,patient_id,start_date,end_date):
    cursor = conn.cursor()
    sql = "SELECT reading_date,tg, tc, ldl, hdl, description FROM patient_lipid WHERE patient_id = " + str(patient_id) + ""
    if start_date:
        sql += " AND reading_date BETWEEN DATE('" + str(start_date) + "') AND DATE('" + str(end_date) + "') ORDER BY reading_date ASC";
    else:
       sql += " ORDER BY reading_date DESC LIMIT 10 "
    cursor=conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall() #database query to retrieve readings
def get_readings_for_graph(conn,patient_id,start_date,end_date):
    cursor = conn.cursor()
    sql = "SELECT reading_date,scale FROM patient_lipid WHERE patient_id = " + str(patient_id) + ""
    if start_date:
        sql += " AND reading_date BETWEEN DATE('" + str(start_date) + "') AND DATE('" + str(end_date) + "') ORDER BY reading_date ASC";
    else:
       sql += " ORDER BY reading_date DESC LIMIT 10 "
    cursor=conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall() #database query to retrieve readings
def check_next_appointment(st,conn,patient_id,widgets,components,utility):
    cursor = conn.cursor()
    sql = "SELECT reading_date FROM patient_lipid WHERE patient_id = " + str(patient_id) + " ORDER BY reading_date DESC LIMIT 1"
    cursor.execute(sql)
    readings = cursor.fetchall() #database query to retrieve readings
    last_reading = overdue = ''
    for row in readings:
        last_reading = row[0]    
    years, months = utility.get_daignosis_duration(last_reading)
    if years>1:
        overdue = utility.format_warning("next appointment is now overdue")
    else:
       next_date = utility.add_date(last_reading,1,0)
       overdue = utility.format_label("next appointment is on " + next_date)
    st.markdown("Last reading was in " + last_reading + ", " + overdue,unsafe_allow_html=True)
    set_data_capture_form(conn,patient_id,st,widgets,components)
    
def get_readings_for_score(conn,patient_id,start_date,end_date,st,utility,compute):
    cursor = conn.cursor()
    sql = "SELECT score FROM patient_lipid WHERE patient_id = " + str(patient_id) + ""
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
    st.session_state.lipid_score = average_score
    
    return divider
    
def get_readings_for_concordance(conn,patient_id,start_date,end_date,st,pd,utility,compute):
    import numpy as np
    import matplotlib.pyplot as plt
    
    cursor = conn.cursor()
    sql = "SELECT reading_date,score FROM patient_lipid WHERE patient_id = " + str(patient_id) + ""
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
    st.session_state.lipid_gradient = gradient
    
    
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
  plt.ylabel('Lipid Profile Scores')
  st.pyplot(plt)
  #plt.show()
def check_con_dis_cordance(b):
    if b > 0:
        return '<p style="color:green; font-weight: bold;">Concordant</p>'
    else:
        return '<p style="color:red;font-weight: bold;">Discordant</p>'
  
def get_score_description(index):
    scores = ["Undefined","Severely high","High","Borderline High","Near optimal","Optimal"]
    return scores[index]
    
    
def load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,start_date,end_date,date_range,widgets,components,compute):
    if not compute:
        st.markdown("""---""")
        st.subheader("4. Lipids")
    readings = get_readings_for_display(conn,patient_id,start_date,end_date)
    if not compute:
        readings_on_table_display(readings,st,datetime)  
        utility.plotly_chart_lipid(conn,patient_id,start_date,end_date,st)
    value = get_readings_for_score(conn,patient_id,start_date,end_date,st,utility,compute)
    if value > 0:
        get_readings_for_concordance(conn,patient_id,start_date,end_date,st,pd,utility,compute)
    if not compute:    
        check_next_appointment(st,conn,patient_id,widgets,components,utility)
  
def readings_on_table_display(readings,st,datetime):
    date,tg,tc,ldl,hdl,description = st.columns(6)
    with date:
       st.write("**Date**")
    with tg:
       st.write("**Triglycerides**")
    with tc:
       st.write("**Total Cholestral**")
    with ldl:
       st.write("**Low Density Cholestral**")
    with hdl:
       st.write("**High Density Cholestral**")
    with description:
       st.write("**Description**")
    i = 0
    date_reading = list()
    new_format = '%Y-%m-%d'
    for row in readings:
        with date:
           st.write(str(row[0]))
        with tg:
           st.write(str(row[1]))
        with tc:
           st.write(str(row[2]))
        with ldl:
           st.write(str(row[3]))
        with hdl:
           st.write(str(row[4]))
        with description:
           st.write(row[5])
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
    sql = "SELECT scale, score FROM patient_lipid WHERE patient_id = " + str(patient_id) + " AND reading_date = '" + str (diagnosis_date) + "'";
    cursor.execute(sql)
    rows = cursor.fetchall()
    reading = reading_scores = 1
    for row in rows:
        reading = row[0]
        reading_scores = row[1]
    return reading_scores, reading
    
    
def initial_diagnosis_correlation_readings_more(conn, patient_id, old_date_str,new_date_str, initial_readings, initial_readings_scores):
    cursor = conn.cursor()
    sql = "SELECT scale, score FROM patient_lipid WHERE patient_id = " + str(patient_id) + " AND reading_date BETWEEN DATE('" + str(old_date_str) + "') AND DATE('" + str(new_date_str) + "')"
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

def save_to_db(conn,patient_id,reading_date,tg,tc,ldl,hdl,scale,score,description):
    conn.execute(f'''
            INSERT INTO patient_lipid (
            patient_id, reading_date,tg,tc,ldl,hdl,scale,score,description
            ) 
            VALUES 
            ('{patient_id}','{reading_date}','{tg}','{tc}','{ldl}','{hdl}','{scale}','{score}','{description}')
            ''')
    conn.commit()    
    
def set_data_capture_form(conn,patient_id,st,widgets,components,age=''):   
    ##modal widgets##
    modal = widgets.create_modal_widget("Capture Lipids reading","lipids",50,600)
    open_modal = st.button("Capture Lipids reading","lipids")
    
    if open_modal:
        modal.open()
        
    if modal.is_open():
       
        with modal.container():
            result = ''
            mpc = ''
            score = ''
            scale = ''
            reading_date = st.date_input("Reading date",format="YYYY-MM-DD",key="lipids-date")
            
            tg = st.number_input("Triglycerides:",key="lipids-tg")
            tc = st.number_input("Total cholestral:",key="lipids-tc")
            ldl = st.number_input("Low Density Cholestral:",key="lipids-ldl")
            hdl = st.number_input("High Density Cholestral:",key="lipids-hdl")
            if st.button('Submit reading',key="lipids-submit"):
                if tg < 1.7 and tc <= 5.17 and ldl < 2 and hdl > 1.55:
                    result = 'Optimal'
                    mpc = 1
                    score = 5
                    st.success(result)
                if (tg >= 1.7 and tg <= 5.63) or (tc >= 5.18 and tc <= 5.51) or (ldl >= 2.1 and hdl <= 2.5) or (hdl >= 1.55 and hdl <= 1.32):
                    result = 'Near Optimal'
                    mpc = 2
                    score = 4
                    st.info(result)
                if (tg >= 5.64 and tg <= 7.5) or (tc >= 5.52 and tc <= 5.86) or (ldl >= 2.6 and hdl <= 3.3) or (hdl >= 1.31 and hdl <= 1.18):
                    result = 'Borderline High'
                    mpc = 3
                    score = 3
                    st.warning(result)        
                if (tg >= 7.51 and tg <= 10) or (tc >= 5.87 and tc <= 6.18) or (ldl >= 3.4 and hdl <= 4.9) or (hdl >= 1.17 and hdl <= 1.03):
                    result = 'High'
                    mpc = 4
                    score = 2
                    st.error(result)
                if tg >10 and tc > 6.18 and ldl < 4.9 and hdl <1.03:
                    result = 'Severely High'
                    mpc = 5
                    score = 1
                    st.error(result)
                if not result:
                    st.error('You have not entered valid inputs, please try again')
                else:
                    description = result
                    scale = mpc
                    save_to_db(conn,patient_id,reading_date,tg,tc,ldl,hdl,scale,score,description)
                    st.success("Reading saved")
