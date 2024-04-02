import pandas as pd 
from datetime import datetime

def get_readings_for_display(conn,patient_id,start_date,end_date):
    cursor = conn.cursor()
    sql = "SELECT reading_date, reading, description FROM health_system WHERE patient_id = " + str(patient_id) + ""
    if start_date:
        sql += " AND reading_date BETWEEN DATE('" + str(start_date) + "') AND DATE('" + str(end_date) + "') ORDER BY reading_date ASC";
    else:
       sql += " ORDER BY reading_date DESC LIMIT 10 "
    cursor=conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall() #database query to retrieve readings
def get_readings_for_graph(conn,patient_id,start_date,end_date):
    cursor = conn.cursor()
    sql = "SELECT reading_date,scale FROM health_system WHERE patient_id = " + str(patient_id) + ""
    if start_date:
        sql += " AND reading_date BETWEEN DATE('" + str(start_date) + "') AND DATE('" + str(end_date) + "') ORDER BY reading_date ASC";
    else:
       sql += " ORDER BY reading_date DESC LIMIT 10 "
    cursor=conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall() #database query to retrieve readings
    
def check_next_appointment(st,conn,patient_id,widgets,components,utility):
    cursor = conn.cursor()
    sql = "SELECT reading_date FROM health_system WHERE patient_id = " + str(patient_id) + " ORDER BY reading_date DESC LIMIT 1"
    cursor.execute(sql)
    readings = cursor.fetchall() #database query to retrieve readings
    last_reading = overdue = ''
    for row in readings:
        last_reading = row[0]    
    years, months = utility.get_daignosis_duration(last_reading)
    if years>0 or months>3:
        overdue = utility.format_warning("next appointment is now overdue")
    else:
       next_date = utility.add_date(last_reading,0,6)
       overdue = utility.format_label("next appointment is on " + next_date)
    st.markdown("Last reading was in " + last_reading + ", " + overdue,unsafe_allow_html=True)
    set_data_capture_form(conn,patient_id,st,widgets,components)
    
def get_readings_for_score(conn,patient_id,start_date,end_date,st,utility,compute):
    cursor = conn.cursor()
    sql = "SELECT score FROM health_system WHERE patient_id = " + str(patient_id) + ""
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
            st.markdown("MPC Score: " + score_str, unsafe_allow_html=True)
    st.session_state.health_system_score = average_score
    
    return divider
    
def get_readings_for_concordance(conn,patient_id,start_date,end_date,st,pd,utility,compute):
    import numpy as np
    import matplotlib.pyplot as plt
    
    cursor = conn.cursor()
    sql = "SELECT reading_date,score FROM health_system WHERE patient_id = " + str(patient_id) + ""
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
    st.session_state.health_system_gradient = gradient
    
    
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
  plt.ylabel('Health System Scores')
  st.pyplot(plt)
  #plt.show()

def get_all_score_description():
    scores = ["Undefined","Poor","Fair","Average","Good","Excellent","Health System scoring","Health System Scoring Performance","Health System scoring in scale"]
    return scores
    
def get_score_description(index):
    scores = get_all_score_description()
    return scores[index]
    

def load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,start_date,end_date,date_range,widgets,components,compute):
    if not compute:
        st.markdown("""---""")
        st.subheader("13. Health System")
    readings = get_readings_for_display(conn,patient_id,start_date,end_date)
    if not compute:
        readings_on_table_display(readings,st,date_range)
    data = get_readings_for_graph(conn,patient_id,start_date,end_date)
    labels = get_all_score_description()    
    if not compute:
        utility.plotly_chart(data,labels,st)
    value = get_readings_for_score(conn,patient_id,start_date,end_date,st,utility,compute)
    if value > 0:
        get_readings_for_concordance(conn,patient_id,start_date,end_date,st,pd,utility,compute)
    if not compute:
        check_next_appointment(st,conn,patient_id,widgets,components,utility)
  
def readings_on_table_display(readings,st,date_range):
    if len(readings)<1:
       st.write("Insufficient readings to display the table")
       return
    st.write("**Health System " + date_range + "**")
    date, bgm, description = st.columns(3)
    with date:
       st.write("**Date**")
    with bgm:
       st.write("**HS - 7 items Scores**")
    with description:
       st.write("**Description**")
    i = 0
    date_reading = list()
    new_format = '%Y-%m-%d'
    for row in readings:
        with date:
            st.write(row[0])
        with bgm:
           st.write(str(row[1]))
        with description:
           st.write(row[2])
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
    sql = "SELECT scale, score FROM health_system WHERE patient_id = " + str(patient_id) + " AND reading_date = '" + str (diagnosis_date) + "'";
    cursor.execute(sql)
    rows = cursor.fetchall()
    reading = reading_scores = 1
    for row in rows:
        reading = row[0]
        reading_scores = row[1]
    return reading_scores, reading
    
def initial_diagnosis_correlation_readings_more(conn, patient_id, old_date_str,new_date_str, initial_readings, initial_readings_scores):
    cursor = conn.cursor()
    sql = "SELECT scale, score FROM health_system WHERE patient_id = " + str(patient_id) + " AND reading_date BETWEEN DATE('" + str(old_date_str) + "') AND DATE('" + str(new_date_str) + "')"
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
    
def save_to_db(conn,patient_id,reading_date,reading,scale,score,description,data_id):
    cursor=conn.cursor()
    if data_id:
        sql_update_query = """UPDATE health_system set reading_date = ?,reading=?, scale=?, score=?, description=? where id = ?"""
        data = (str(reading_date),str(reading),str(scale),str(score),str(description),str(data_id))
        cursor.execute(sql_update_query, data)
    else:
        conn.execute(f'''
                INSERT INTO health_system (
                patient_id, reading_date, reading, scale, score, description
                ) 
                VALUES 
                ('{patient_id}','{reading_date}','{reading}','{scale}','{score}','{description}')
                ''')
    conn.commit()    
    
def delete_readings(conn,st,data_id):
    cursor = conn.cursor()
    sql_delete_query = "DELETE FROM health_system where id = " + str(data_id)
    cursor.execute(sql_delete_query)
    conn.commit()
    st.success('Reading of record ' + str(data_id) + ' deleted.')
    
def set_data_capture_form(conn,patient_id,st,widgets,components,age=''):   
   return
   
def get_readings_for_edit(st,conn,patient_id):
    cursor = conn.cursor()
    sql = "SELECT reading_date,reading, score, scale, description,id FROM health_system WHERE patient_id = " + str(patient_id) + " ORDER BY id ASC"
    cursor=conn.cursor()
    cursor.execute(sql)
    df = pd.DataFrame(cursor.fetchall(),columns=['Reading Date','Health System Score','Score','Scale','Description','ID'])
    df['Reading Date'] = pd.to_datetime(df['Reading Date'])
    edited_df = st.data_editor(
    df,
    key="health_system_df",
    num_rows="dynamic",
    disabled=["ID","Score","Description"],
    column_config={
        "Reading Date": st.column_config.DateColumn(
            format="YYYY-MM-DD",
            step=1,
            required=True,
        ),
       
    },
    hide_index=True,
    use_container_width=True
    )
    st.write('In order to add or update an Physical Activity record, enter/alter Reading Date, and the Health System Score. The system will automatically fill in the values for the other columns.')    
    if st.button('Save Changes',key="bp_btn"):
        ###Process edited content
        edited_rows = st.session_state["health_system_df"].get("edited_rows")
        edited_items_list = edited_rows.items()
        for index,item in edited_items_list:
            data_id = df.loc[index, 'ID']
            reading_date = df.loc[index, 'Reading Date']
            test = df.loc[index, 'Health System Score']
                    
            #check what has changed
            if 'Reading Date' in item:
                if reading_date != item['Reading Date']:
                    reading_date = item['Reading Date']
            if  'Health System Score' in item:
                if test != item['Health System Score']:
                    test = item['Health System Score']
            save_readings(conn,st,0,test,reading_date,index+1,data_id)
        ##New Records
        added_rows = st.session_state["health_system_df"].get("added_rows")
        index = 0
        for item in added_rows:
            index = index+1
            reading_date = test = ''
            #check what has been added
            if 'Reading Date' in item:
                if reading_date != item['Reading Date']:
                    reading_date = item['Reading Date']
            if  'Health System Score' in item:
                if test != item['Health System Score']:
                    test = item['Health System Score']
            if test:
                save_readings(conn,st,patient_id,test,reading_date,index)
                
        ##Delete Records
        deleted_rows = st.session_state["health_system_df"].get("deleted_rows")
        index = 0
        for item in deleted_rows:
            data_id = df.loc[item, 'ID']
            delete_readings(conn,st,data_id)
   
def save_readings(conn,st,patient_id,test,reading_date,record,data_id=''):
    result = ''
    test = int(test)
    if  test >= 29 and test <=35:
        result = 'Excellent'
        mpc = 1
        score = 5
        
    if test >= 22 and test <=28:
        result = 'Good'
        mpc = 2
        score = 4
       
    if test >= 13 and test <= 21:
        result = 'Average'
        mpc = 3
        score = 3
            
    if test >= 8 and test <=14:
        result = 'Fair'
        mpc = 4
        score = 2
       
    if test >= 1 and test <=7:
        result = 'Poor'
        mpc = 5
        score = 1
    if not result:
        if data_id:
            st.error('Updates failed. You have not entered valid inputs for record ' + str(record) +' to be updated. Please try again.')
        else:
            st.error('New record failed to save. You have not entered valid inputs for new record ' + str(record) +'. Please try again.')
    else:
        description = result
        scale = mpc
        if data_id:
            reading_date = datetime.strptime(str(reading_date), '%Y-%m-%d %H:%M:%S')
        else:
            reading_date = datetime.strptime(str(reading_date), '%Y-%m-%d')
        reading_date = reading_date.strftime('%Y-%m-%d')
        save_to_db(conn,patient_id,reading_date,test,scale,score,description,data_id)
        if data_id:
            st.success("Updated readings for record " + str(record) + " saved.")
        else:
            st.success("New readings for record " + str(record) + " saved.")