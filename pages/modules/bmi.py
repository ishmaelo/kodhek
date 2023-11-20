def bmi_readings_with_chart(patient_id,st,conn,utility):
    st.divider()
    st.subheader("5.Body Mass Index")
    cursor = conn.cursor()
    sql = "SELECT reading_date,bmi_reading,description,score FROM bmi WHERE patient_id = '" + str(patient_id) + "'"
    cursor=conn.cursor()
    cursor.execute(sql)
    resultset = cursor.fetchall()
    new_df = utility.get_bmi_data_with_annotations(resultset)
    new_df['Reading date'] = pd.to_datetime(new_df['Reading date'])
    source = new_df
    source
    
    base = alt.Chart(source).encode(
        alt.Color("Description").legend(None)
    ).transform_filter(
        "datum.Description !== 'IBM'"
    ).properties(
        width=1100
    )

    line = base.mark_line().encode(x="Reading date", y="Score")


    last_price = base.mark_circle().encode(
        alt.X("last_date['Reading date']:T"),
        alt.Y("last_date['Score']:Q")
    ).transform_aggregate(
        last_date="argmax(Reading date)",
        groupby=["Description"]
    )

    company_name = last_price.mark_text(align="left", dx=4).encode(text="Description")

    chart = (line + last_price + company_name).encode(
        x=alt.X().title("Reading date"),
        y=alt.Y().title("Score")
    )

    chart   