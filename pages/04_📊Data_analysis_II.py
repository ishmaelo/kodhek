import streamlit as st
import pandas as pd
from datetime import datetime
import altair as alt

###custom modules#############
import pages.modules.utilities as utility
import pages.modules.widgets as widgets
import streamlit.components.v1 as components


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


conn = utility.get_database_connection() #database connection
utility.set_title(st) #Title of the page


### display patient medical readings ###
def display_patient(patient,target):
    utility.patient_header_info(patient,st) #header information having patient name, gender, date of birth, etc
    col1, col2, col3, col4 = st.columns([1,1,1,1])
    col1.markdown("<br/>",unsafe_allow_html=True)
    st.markdown(
        """
        <br/>
        <style>
         a:hover{
            color:#6293f5;
         }
        .st-d6,.st-d5,.st-d4,.st-bu {
            background-color: rgb(236 239 243);
            border-top-color: rgb(170, 196, 244);
            border-bottom-color: rgb(170, 196, 244);
            border-right-color: rgb(170, 196, 244);
            border-left-color: rgb(170, 196, 244);
        }
        .st-emotion-cache-ibsp32{
            background-color: #6293f5;
            border: 2px solid #2153b9;
            padding:8px 5px;            
        }
        hr{
            margin:1em 0px;
            border-bottom: 1px solid rgb(181 188 243 / 20%);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
   
    compute = ''
    col1.write("Select a range of reading dates")
    start = col2.date_input("From",format="YYYY-MM-DD",key="start")
    end = col3.date_input("To",format="YYYY-MM-DD",key="end")
    date_range = " (Latest Readings)"
    col4.markdown("<br/>",unsafe_allow_html=True)
   
   
    
    if col4.button('Load readings for the selected date range',type="primary"):
        start_date = str(st.session_state.start)
        end_date = str(st.session_state.end)
        mnths,total_months = utility.number_of_months(start_date,end_date)
        mnths = utility.format_label(mnths)
        st.markdown('Duration of the analysis: '+ mnths,unsafe_allow_html=True)
        date_range = " (Readings between " + str (start_date) + " and " + str(end_date) + ")"
        if target== 'blood_sugar':
            blood_sugar.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,start_date,end_date,date_range,widgets,components,compute)
        #with st.expander("**2. HBA1C**"):
        if target== 'hba1c':
            hba1c.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,start_date,end_date,date_range,widgets,components,compute)
        #with st.expander("**3. Blood Pressure**"):
        if target== 'blood_pressure':
            blood_pressure.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,start_date,end_date,date_range,widgets,components,compute)
        #with st.expander("**4. Lipids**"):
        if target== 'lipid':
            lipid.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,start_date,end_date,date_range,widgets,components,compute)
        #with st.expander("**5. BMI**"):
        if target== 'bmi':
            bmi.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,start_date,end_date,date_range,widgets,components,compute)
        if target== 'urine':
            urine.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,start_date,end_date,date_range,widgets,components,compute)
        if target== 'eye':
            eye.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,start_date,end_date,date_range,widgets,components,compute)
        if target== 'monofilament':
            monofilament.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,start_date,end_date,date_range,widgets,components,compute)
        if target== 'diet':
            diet.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,start_date,end_date,date_range,widgets,components,compute)
        if target== 'physical_activity':
            physical_activity.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,start_date,end_date,date_range,widgets,components,compute)
        if target== 'education':
            education.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,start_date,end_date,date_range,widgets,components,compute)
        if target== 'comorbidity':
            comorbidity.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,start_date,end_date,date_range,widgets,components,compute)
        if target== 'health_system':
            health_system.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,start_date,end_date,date_range,widgets,components,compute)
        if target== 'socioeconomic':
            socioeconomic.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,start_date,end_date,date_range,widgets,components,compute)
    else:
        if target== 'blood_sugar':
            blood_sugar.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,'','',date_range,widgets,components,compute)
        #with st.expander("**2. HBA1C**"):
        if target== 'hba1c':
            hba1c.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,'','',date_range,widgets,components,compute)
        #with st.expander("**3. Blood Pressure**"):
        if target== 'blood_pressure':
            blood_pressure.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,'','',date_range,widgets,components,compute)
        #with st.expander("**4. Lipids**"):
        if target== 'lipid':
            lipid.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,'','',date_range,widgets,components,compute)
        #with st.expander("**5. BMI**"):
        if target== 'bmi':
            bmi.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,'','',date_range,widgets,components,compute)
        if target== 'urine':
            urine.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,'','',date_range,widgets,components,compute)
        if target== 'eye':
            eye.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,'','',date_range,widgets,components,compute)
        if target== 'monofilament':
            monofilament.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,'','',date_range,widgets,components,compute)
        if target== 'diet':
            diet.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,'','',date_range,widgets,components,compute)
        if target== 'physical_activity':
            physical_activity.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,'','',date_range,widgets,components,compute)
        if target== 'education':
            education.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,'','',date_range,widgets,components,compute)
        if target== 'comorbidity':
            comorbidity.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,'','',date_range,widgets,components,compute)
        if target== 'health_system':
            health_system.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,'','',date_range,widgets,components,compute)
        if target== 'socioeconomic':
            socioeconomic.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,'','',date_range,widgets,components,compute)
    
    
  
# retrieve patient id via URL   
patient_id, target = utility.get_patient_id_via_url(st)

 
# display patient readings if the patient id is not null
if patient_id:
   display_patient(utility.get_patient(conn,patient_id),target)
    
    