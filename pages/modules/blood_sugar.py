def get_readings_for_display(conn,patient_id,start_date,end_date):
    cursor = conn.cursor()
    sql = "SELECT reading_date,reading_category,reading_time, bgm_reading, description FROM bgm WHERE patient_id = " + str(patient_id) + ""
    if start_date:
        sql += " AND reading_date BETWEEN DATE('" + str(start_date) + "') AND DATE('" + str(end_date) + "') ORDER BY reading_date ASC";
    else:
       sql += " ORDER BY reading_date DESC LIMIT 10 "
    cursor=conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall() #database query to retrieve readings
def get_readings_for_graph(conn,patient_id,start_date,end_date):
    cursor = conn.cursor()
    sql = "SELECT reading_date,AVG(scale) FROM bgm WHERE patient_id = " + str(patient_id) + ""
    if start_date:
        sql += " AND reading_date BETWEEN DATE('" + str(start_date) + "') AND DATE('" + str(end_date) + "') GROUP BY reading_date ORDER BY reading_date ASC";
    else:
       sql += " GROUP BY reading_date ORDER BY reading_date DESC LIMIT 10 "
    cursor=conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall() #database query to retrieve readings
    
def get_readings_for_score(conn,patient_id,start_date,end_date,st):
    cursor = conn.cursor()
    sql = "SELECT score FROM bgm WHERE patient_id = " + str(patient_id) + ""
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
    average_score = round(average_score / divider)
    st.write("**MPC Scoring**")
    description = get_score_description(average_score)
    st.write("Score:",average_score,description)
    st.session_state.blood_sugar_score = average_score
    
def get_readings_for_concordance(conn,patient_id,start_date,end_date,st,pd,utility):
    import numpy as np
    import matplotlib.pyplot as plt
    
    cursor = conn.cursor()
    sql = "SELECT reading_date,AVG(scale) FROM bgm WHERE patient_id = " + str(patient_id) + ""
    if start_date:
        sql += " AND reading_date BETWEEN DATE('" + str(start_date) + "') AND DATE('" + str(end_date) + "') GROUP BY reading_date ORDER BY reading_date ASC";
    else:
        sql += " GROUP BY reading_date ORDER BY reading_date DESC LIMIT 10 "
    cursor=conn.cursor()
    cursor.execute(sql)
    readings = cursor.fetchall()
    scores = list()
    dates = list()
    for row in readings:
        dates.append(row[0])
        scores.append(row[1])
    #st.write(dates,scores)
    dates = np.array(dates)
    dates = pd.to_datetime(dates).map(lambda d: d.toordinal())
    scores = np.array(scores)
    #plot
    b = estimate_linear_regression_coefs(np,dates, scores)
    intercept, gradient = b
    conco = utility.check_con_dis_cordance(gradient)  
    st.write("**Concordance/Discordance Test** - using a regression model")
    st.write("Gradient: ",gradient)
    st.markdown(conco, unsafe_allow_html=True)
    plot_regression_line(dates, scores, b, st)
    st.session_state.blood_sugar_gradient = gradient
    
    
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
  # plotting the actual points as scatter plot
  plt.scatter(x, y, color = "b",
        marker = "x", s = 30)
 
  # predicted response vector
  y_pred = b[0] + b[1]*x
 
  # plotting the regression line
  plot = plt.plot(x, y_pred, color = "m")
 
  # putting labels
  plt.xlabel('Dates')
  plt.ylabel('BGM Scores')
  st.pyplot(plt)
  #plt.show()

def get_score_description(index):
    scores = ["Undefined","Very high/Grade 2 hypo","High/Grade 1 hypo","Elevated","Normal","Optimal"]
    return scores[index]
    
def get_readings_for_tir(conn,patient_id,start_date,end_date,st):
    cursor = conn.cursor()
    sql = "SELECT bgm_reading FROM bgm WHERE patient_id = " + str(patient_id) + ""
    if start_date:
        sql += " AND reading_date BETWEEN DATE('" + str(start_date) + "') AND DATE('" + str(end_date) + "') ORDER BY reading_date ASC";
    else:
        sql += " ORDER BY reading_date DESC LIMIT 10 "
    cursor=conn.cursor()
    cursor.execute(sql)
    readings = cursor.fetchall()
    average_score = 0
    divider = 0
    if len(readings) < 84:
        return
    tir = 0
    count = len(readings)
    for row in readings:
        val = row[0]
        if val >= 3.9 and val <= 10:
           tir += 1
    
    tir = (tir / count) * 100
    st.write("**TIR values**")
    st.write("TIR:",tir)
    
def load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,start_date,end_date,date_range):
    readings = get_readings_for_display(conn,patient_id,start_date,end_date)
    readings_on_table_display(readings,st,datetime,date_range)  
    utility.plotly_chart_blood_sugar(conn,patient_id,start_date,end_date,st)
    get_readings_for_score(conn,patient_id,start_date,end_date,st)
    get_readings_for_tir(conn,patient_id,start_date,end_date,st)
    get_readings_for_concordance(conn,patient_id,start_date,end_date,st,pd,utility)
  
def readings_on_table_display(readings,st,datetime,date_range):
    st.write("**Blood Glucose Readings " + date_range + "**")
    date, session, time, bgm, description = st.columns(5)
    with date:
       st.write("**Date**")
    with session:
       st.write("**Reading session**")
    with time:
       st.write("**Time recorded**")
    with bgm:
       st.write("**BGM (mmol/lit)**")
    with description:
       st.write("**Description**")
    i = 0
    date_reading = list()
    new_format = '%Y-%m-%d'
    for row in readings:
        date_reading.append(row[0])
        j = i-1
        previous_reading = ''        
        if i > 0:
            previous_reading =  date_reading[j]
            
        with date:
           if i > 0 and previous_reading == row[0]:
            st.write("'")
           else:
            st.write(row[0])
        with session:
           st.write(row[1])
        with time:
           st.write(row[2])
        with bgm:
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