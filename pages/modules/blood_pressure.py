import pandas as pd 
from datetime import datetime

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
       
def save_to_db(conn,patient_id,reading_date,dbp,sbp,mean_abp,special,scale,score,description,data_id):
    cursor=conn.cursor()
    if data_id:
        sql_update_query = """UPDATE bp_reading set reading_date = ?, dbp=?, sbp=?, mean_abp=?, special_case=?, scale=?, score=?, description=? where id = ?"""
        data = (str(reading_date),str(dbp),str(sbp),str(mean_abp),str(special),str(scale),str(score),str(description),str(data_id))
        cursor.execute(sql_update_query, data)
    else:
        conn.execute(f'''
                INSERT INTO bp_reading (
                patient_id, reading_date, dbp,sbp,mean_abp, special_case, scale, score, description
                ) 
                VALUES 
                ('{patient_id}','{reading_date}','{dbp}','{sbp}','{mean_abp}','{special}','{scale}','{score}','{description}')
                ''')
    conn.commit()    
    
def delete_readings(conn,st,data_id):
    cursor = conn.cursor()
    sql_delete_query = "DELETE FROM bp_reading where id = " + str(data_id)
    cursor.execute(sql_delete_query)
    conn.commit()
    st.success('Reading of record ' + str(data_id) + ' deleted.')
    
def set_data_capture_form(conn,patient_id,st,widgets,components,age=''):   
   return
   
def get_readings_for_edit(st,conn,patient_id):
    cursor = conn.cursor()
    sql = "SELECT reading_date, sbp, dbp, special_case, mean_abp, score, scale, description,id FROM bp_reading WHERE patient_id = " + str(patient_id) + " ORDER BY id ASC"
    cursor=conn.cursor()
    cursor.execute(sql)
    df = pd.DataFrame(cursor.fetchall(),columns=['Reading Date','Systolic Reading','Diastolic Reading','Is Special Case?','Mean Arterial Reading','Score','Scale','Description','ID'])
    df['Reading Date'] = pd.to_datetime(df['Reading Date'])
    edited_df = st.data_editor(
    df,
    key="bp_df",
    num_rows="dynamic",
    disabled=["ID","Score","Description","Mean Arterial Reading"],
    column_config={
        "Reading Date": st.column_config.DateColumn(
            format="YYYY-MM-DD",
            step=1,
            required=True,
        ),
        "Systolic Reading": st.column_config.NumberColumn(
            required=True,
        ),
        "Diastolic Reading": st.column_config.NumberColumn(
            required=True,
        ),
        "Is Special Case?": st.column_config.CheckboxColumn(
            required=True,
        ),
       
    },
    hide_index=True,
    use_container_width=True
    )
    st.write('In order to add or update a BP record, enter/alter Reading Date, Systolic Reading, Diastolic Reading, and specify whether it is a Special Case or not. The system will automatically fill in the values for the other columns.')    
    if st.button('Save Changes',key="bp_btn"):
        ###Process edited content
        edited_rows = st.session_state["bp_df"].get("edited_rows")
        edited_items_list = edited_rows.items()
        for index,item in edited_items_list:
            data_id = df.loc[index, 'ID']
            reading_date = df.loc[index, 'Reading Date']
            sbp = df.loc[index, 'Systolic Reading']
            dbp = df.loc[index, 'Diastolic Reading']
            special = df.loc[index, 'Is Special Case?'] 
            #check what has changed
            if 'Reading Date' in item:
                if reading_date != item['Reading Date']:
                    reading_date = item['Reading Date']
            if  'Systolic Reading' in item:
                if sbp != item['Systolic Reading']:
                    sbp = item['Systolic Reading']
            if  'Diastolic Reading' in item:
                if dbp != item['Diastolic Reading']:
                    dbp = item['Diastolic Reading']
            if 'Is Special Case?' in item:
                if special != item['Is Special Case?']:
                    special = item['Is Special Case?']
            save_readings(conn,st,0,sbp,dbp,reading_date,special,index+1,data_id)
        ##New Records
        added_rows = st.session_state["bp_df"].get("added_rows")
        index = 0
        for item in added_rows:
            index = index+1
            reading_date = sbp = dbp = special = ''
            #check what has been added
            if 'Reading Date' in item:
                if reading_date != item['Reading Date']:
                    reading_date = item['Reading Date']
            if  'Systolic Reading' in item:
                if sbp != item['Systolic Reading']:
                    sbp = item['Systolic Reading']
            if  'Diastolic Reading' in item:
                if dbp != item['Diastolic Reading']:
                    dbp = item['Diastolic Reading']
            if 'Is Special Case?' in item:
                if special != item['Is Special Case?']:
                    special = item['Is Special Case?']
            if reading_date and sbp and dbp:
                save_readings(conn,st,patient_id,sbp,dbp,reading_date,special,index)
                
        ##Delete Records
        deleted_rows = st.session_state["bp_df"].get("deleted_rows")
        index = 0
        for item in deleted_rows:
            data_id = df.loc[item, 'ID']
            delete_readings(conn,st,data_id)
   
def save_readings(conn,st,patient_id,systolic,diastolic,reading_date,special,record,data_id=''):
    result = ''
    if special:
        if (systolic >= 100 and systolic < 140) or (diastolic >= 60 and diastolic <= 90):
            result = 'Normal'
            mpc = 1
            score = 5

        if (systolic >= 140 and systolic <= 150) or (diastolic >= 91 and diastolic < 95):
            result = 'High normal'
            mpc = 2
            score = 4

        if (systolic >= 151 and systolic <= 160) or (diastolic >= 95 and diastolic < 100):
            result = 'Grade 1'
            mpc = 3
            score = 3
                
        if (systolic >= 161 and systolic <= 179) or (diastolic >= 100 and diastolic < 109):
            result = 'Grade 2'
            mpc = 4
            score = 2
        if (systolic >= 180 or diastolic >= 110) or (systolic < 100 or diastolic < 60):
            result = 'Grade 3/urgency'
            mpc = 5
            score = 1
    else:
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
                
        if (systolic >= 160 and systolic <= 179) or (diastolic >= 100 and diastolic < 109):
            result = 'Grade 2'
            mpc = 4
            score = 2
        if (systolic >= 180 or diastolic >= 110) or (systolic < 100 or diastolic < 60):
            result = 'Grade 3/urgency'
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
        mean_abp = int((2*diastolic + systolic)/3)
        if data_id:
            reading_date = datetime.strptime(str(reading_date), '%Y-%m-%d %H:%M:%S')
        else:
            reading_date = datetime.strptime(str(reading_date), '%Y-%m-%d')
        reading_date = reading_date.strftime('%Y-%m-%d')
        save_to_db(conn,patient_id,reading_date,diastolic,systolic,mean_abp,special,scale,score,description,data_id)
        if data_id:
            st.success("Updated readings for record " + str(record) + " saved.")
        else:
            st.success("New readings for record " + str(record) + " saved.")