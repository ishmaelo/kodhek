import pandas as pd 
from datetime import datetime

def load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,start_date,end_date,date_range,widgets,components,compute):
    if not compute:
        #st.markdown("""---""")
        st.subheader("1. Blood Glucose")
    readings = get_readings_for_display(conn,patient_id,start_date,end_date)
    if not compute:
        readings_on_table_display(readings,st,datetime,date_range)  
        utility.plotly_chart_blood_sugar(conn,patient_id,start_date,end_date,st)
    value = get_readings_for_score(conn,patient_id,start_date,end_date,st,utility,compute)
    if value > 0:
        if not compute:
            get_readings_for_tir(conn,patient_id,start_date,end_date,st, utility)
        get_readings_for_concordance(conn,patient_id,start_date,end_date,st,pd,utility,compute)    
    #if not compute:
        #set_data_capture_form(conn,patient_id,st,widgets,components)
    
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
    
def get_readings_for_score(conn,patient_id,start_date,end_date,st,utility,compute):
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
    if divider == 0:
        average_score = 0
    else:
        average_score = round(average_score / divider)
        #st.write("**MPC Scoring**")
        description = get_score_description(average_score)
        score_str = utility.format_label(str(average_score)+ ", " + description)
        if not compute:
            st.markdown("MPC Score: " +  score_str, unsafe_allow_html=True)
    st.session_state.blood_sugar_score = average_score
    
    return divider
    
def get_readings_for_concordance(conn,patient_id,start_date,end_date,st,pd,utility,compute):
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
    conco = utility.check_con_dis_cordance(gradient,True)  
    conco_str = utility.format_label(conco)
    #st.write("Gradient: ",gradient)
    #st.markdown(conco, unsafe_allow_html=True)
    
    if not compute:
        plot_regression_line(dates, scores, b, st)
        st.markdown("Concordance: " + conco_str,unsafe_allow_html=True)
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

  plt.title("Graph tracking the trend of blood sugar over time")
  # plotting the actual points as scatter plot
  plt.scatter(x, y, color = "b",
        marker = "x", s = 10)
 
  # predicted response vector
  y_pred = b[0] + b[1]*x
 
  # plotting the regression line
  plot = plt.plot(x, y_pred, color = "m")
 
  # putting labels
  plt.xlabel('Dates')
  plt.ylabel('BGM Scores')
  plt.grid()
  st.pyplot(plt.gcf())
  #plt.show()

def get_score_description(index):
    scores = ["Undefined","Very high/Grade 2 hypo","High/Grade 1 hypo","Elevated","Normal","Optimal"]
    return scores[index]
    
def get_readings_for_tir(conn,patient_id,start_date,end_date,st, utility):
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
    tir_str = utility.format_label(tir)
    #st.write("**TIR values**")
    st.markdown("TIR: " + tir_str,unsafe_allow_html=True)
    

  
def readings_on_table_display(readings,st,datetime,date_range):
    if len(readings)<1:
        st.write("Insufficient readings to display the table")
        return
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

def save_to_db(conn,patient_id,reading_date,reading_category,measurement_type,bgm_reading,scale,score,description,reading_time,data_id):
 
    cursor=conn.cursor()
    if data_id:
        sql_update_query = """UPDATE bgm set reading_date = ?, reading_category=?, measurement_type=?, bgm_reading=?, scale=?, score=?, description=?, reading_time=? where id = ?"""
        data = (str(reading_date),str(reading_category),str(measurement_type),str(bgm_reading),str(scale),str(score),str(description),str(reading_time),str(data_id))
        cursor.execute(sql_update_query, data)
    else:
        conn.execute(f'''
                INSERT INTO bgm (
                patient_id, reading_date,reading_category,measurement_type,bgm_reading,scale,score,description,reading_time
                ) 
                VALUES 
                ('{patient_id}','{reading_date}','{reading_category}','{measurement_type}','{bgm_reading}','{scale}','{score}','{description}','{reading_time}')
                ''')
    conn.commit()    
def delete_readings(conn,st,data_id):
    cursor = conn.cursor()
    sql_delete_query = "DELETE FROM bgm where id = " + str(data_id)
    cursor.execute(sql_delete_query)
    conn.commit()
    st.success('Reading of record ' + str(data_id) + ' deleted.')
    
def set_data_capture_form(conn,patient_id,st,widgets,components,age=''):   
    return       
           
def get_readings_for_edit(st,conn,patient_id):
    cursor = conn.cursor()
    sql = "SELECT reading_date,reading_time,reading_category, bgm_reading, score, scale, description,id FROM bgm WHERE patient_id = " + str(patient_id) + " ORDER BY id ASC"
    cursor=conn.cursor()
    cursor.execute(sql)
    df = pd.DataFrame(cursor.fetchall(),columns=['Reading Date','Reading Time','Reading Category','BGM Reading','Score','Scale','Description','ID'])
    df['Reading Date'] = pd.to_datetime(df['Reading Date'])
    df['Reading Time'] = df['Reading Time'].apply(pd.Timestamp)
    edited_df = st.data_editor(
    df,
    key="blood_sugar_df",
    num_rows="dynamic",
    disabled=["ID","Score","Scale","Description"],
    column_config={
        "Reading Category": st.column_config.SelectboxColumn(
            options=["Random", "Before breakfast", "2 hours after breakfast", "Before lunch", "2 hours after lunch", "Before supper", "2 hours after supper", "Midnight"],
            required=True,
        ),
        "Reading Time": st.column_config.TimeColumn(
            format="h:mm a",
            step=60,
            required=True,
        ),
        "Reading Date": st.column_config.DateColumn(
            format="YYYY-MM-DD",
            step=1,
            required=True,
        ),
        "BGM Reading": st.column_config.NumberColumn(
            required=True,
        ),
       
    },
    hide_index=True,
    use_container_width=True
    )
    
    st.write('In order to add or update a blood sugar record, enter/alter Reading Date, Reading Time, Reading Category and BGM Reading only. The system will automatically fill in the values for the other columns.')
    if st.button('Save Changes',key="blood_sugar_btn"):
        ###Process edited content
        edited_rows = st.session_state["blood_sugar_df"].get("edited_rows")
        edited_items_list = edited_rows.items()
        for index,item in edited_items_list:
            data_id = df.loc[index, 'ID']
            option = df.loc[index, 'Reading Category']
            reading_date = df.loc[index, 'Reading Date']
            reading_time = df.loc[index, 'Reading Time']
            mmol = df.loc[index, 'BGM Reading']
            #check what has changed
            if 'Reading Category' in item:
                if option != item['Reading Category']:
                    option = item['Reading Category']
                    
            if 'Reading Date' in item:
                if reading_date != item['Reading Date']:
                    reading_date = item['Reading Date']
            
            if 'Reading Time' in item:
                if reading_time != item['Reading Time']:
                    reading_time = item['Reading Time']

            if  'BGM Reading' in item:
                if mmol != item['BGM Reading']:
                    mmol = item['BGM Reading']
            save_readings(conn,st,0,option,mmol,reading_date,reading_time,index+1,data_id)
        ##New Records
        added_rows = st.session_state["blood_sugar_df"].get("added_rows")
        index = 0
        for item in added_rows:
            index = index+1
            option = reading_date = reading_time = mmol = ''
            #check what has been added
            if 'Reading Category' in item:
                option = item['Reading Category']
                    
            if 'Reading Date' in item:
                reading_date = item['Reading Date']
            
            if 'Reading Time' in item:
                reading_time = item['Reading Time']

            if  'BGM Reading' in item:
                mmol = item['BGM Reading']
            if option and reading_date and reading_time and mmol:
                save_readings(conn,st,patient_id,option,mmol,reading_date,reading_time,index)
                
        ##Delete Records
        deleted_rows = st.session_state["blood_sugar_df"].get("deleted_rows")
        index = 0
        for item in deleted_rows:
            data_id = df.loc[item, 'ID']
            delete_readings(conn,st,data_id)
   
def save_readings(conn,st,patient_id,option,mmol,reading_date,reading_time,record,data_id=''):
    result = ''
    if option=='Random':
        if mmol >= 3.9 and mmol <= 5.5:
            result = 'Optimal'
            mpc = 1
            score = 5
            #st.success(result)
        if mmol >= 5.6 and mmol <= 7.9:
            result = 'Normal'
            mpc = 2
            score = 4
            #st.info(result)
        if mmol >= 8 and mmol <= 9:
            result = 'Elevated'
            mpc = 3
            score = 3
            #st.warning(result)        
        if ((mmol >= 9.1 and mmol <= 10.4) or (mmol >= 3 and mmol <= 3.8)):
            result = 'High/grade 1 hypo'
            mpc = 4
            score = 2
           # st.error(result)
        if mmol > 10 and mmol < 3:
            result = 'Very high/grade 2 hypo'
            mpc = 5
            score = 1
            #st.error(result)
    else:
        if mmol >= 3.9 and mmol <= 6:
            result = 'Optimal'
            mpc = 1
            score = 5
            #st.success(result)
        if mmol >= 6.1 and mmol <= 6.9:
            result = 'Normal'
            mpc = 2
            score = 4
            #st.info(result)
        if mmol >= 7 and mmol <= 10:
            result = 'Elevated'
            mpc = 3
            score = 3 
            #st.warning(result)
        if mmol >= 10.1 and mmol <= 13.9:
            result = 'High/grade 1 hypo'
            mpc = 4
            score = 2
            #st.error(result)
        if mmol > 13.9:
            result = 'Very high/grade 2 hypo'
            mpc = 5
            score = 1
            #st.error(result)
    if not result:
        if data_id:
            st.error('Updates failed. You have not entered valid inputs for record ' + str(record) +' to be updated. Please try again.')
        else:
            st.error('New record failed to save. You have not entered valid inputs for new record ' + str(record) +'. Please try again.')
    else:
        reading_category = measurement_type = option
        bgm_reading = mmol
        description = result
        scale = mpc
        if data_id:
            reading_date = datetime.strptime(str(reading_date), '%Y-%m-%d %H:%M:%S')
            reading_time = datetime.strptime(str(reading_time), '%Y-%m-%d %H:%M:%S')
        else:
            reading_date = datetime.strptime(str(reading_date), '%Y-%m-%d')
            reading_time = datetime.strptime(str(reading_time), '%H:%M:%S.%f')
        reading_date = reading_date.strftime('%Y-%m-%d')
        
        reading_time = reading_time.strftime('%H:%M:%S')
        save_to_db(conn,patient_id,reading_date,reading_category,measurement_type,bgm_reading,scale,score,description,reading_time,data_id)
        if data_id:
            st.success("Updated readings for record " + str(record) + " saved.")
        else:
            st.success("New readings for record " + str(record) + " saved.")