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
    sql = "SELECT reading_date,scale FROM bgm WHERE patient_id = " + str(patient_id) + ""
    if start_date:
        sql += " AND reading_date BETWEEN DATE('" + str(start_date) + "') AND DATE('" + str(end_date) + "') ORDER BY reading_date ASC";
    else:
       sql += " ORDER BY reading_date DESC LIMIT 10 "
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
    

    
def get_score_description(index):
    scores = ["Very high/Grade 2 hypo","High/Grade 1 hypo","Elevated","Normal","Optimal"]
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
    st.divider()
    st.subheader("1. Blood Glucose Monitoring " + date_range)
    readings = get_readings_for_display(conn,patient_id,start_date,end_date)
    readings_on_table_display(readings,st,datetime)  
    #new_df = utility.get_blood_sugar_data_with_annotations(get_readings_for_graph(conn,patient_id),pd) #create plottable dataframe
    #new_df['Reading date'] = pd.to_datetime(new_df['Reading date']) #normalize reading dates
    #utility.annonation_chart(new_df,alt,st)
    utility.plotly_chart_separate(conn,patient_id,start_date,end_date,st)
    get_readings_for_score(conn,patient_id,start_date,end_date,st)
    get_readings_for_tir(conn,patient_id,start_date,end_date,st)
  
def readings_on_table_display(readings,st,datetime):
    st.write("**Patient blood glucose readings**")
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
            st.write('')
           else:
            st.write(row[0])
        with session:
           st.write(row[1])
        with time:
           st.write(row[2])
        with bgm:
           st.write(row[3])
        with description:
           st.write(row[4])
        i += 1
       
       
def load_readings(patient_id,st,conn,utility,pd,alt):
    st.divider()
    st.subheader("I.Blood Glucose Monitoring")
    cursor = conn.cursor()
    sql = "SELECT reading_date,reading_category,bgm_reading,score,scale,description FROM bgm WHERE patient_id = '" + str(patient_id) + "'"
    cursor=conn.cursor()
    cursor.execute(sql)
    resultset = cursor.fetchall()
    dates,optimal,normal,elevated,high,very_high = get_row_data(resultset)
    df = pd.DataFrame(resultset,columns=['Reading date','Reading session','BGM reading','Score','Scale','Description'],index=dates)
    df['Reading date'] = pd.to_datetime(df['Reading date'])
    df['Optimal'] = optimal
    df['Normal'] = normal
    df['Elevated'] = elevated
    df['High/Grade 1 Hypo'] = high
    df['Very High/Grade 2 Hypo'] = very_high
    #df = df.drop('Reading date', axis=1)
    df = df.drop('Reading session', axis=1)
    df = df.drop('Description', axis=1)
    #df = df.drop('MPC scale', axis=1)
    #df = df.drop('mmol/lit', axis=1)
    #df = df.drop('MPC', axis=1)
    #df
    st.line_chart(df, x= "Reading date", y = ["Score","Optimal","Normal","Elevated","High/Grade 1 Hypo","Very High/Grade 2 Hypo"],color=["#ff8000","#ffbf00","#0000ff","#00ff00","#000000","#ff0000"],use_container_width=True)

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