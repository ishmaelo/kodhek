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




### display patient medical readings ###
def display_patient(conn,patient):
    age = utility.get_age(patient[2])
    patient_id = patient[0]   
    utility.patient_header_info(patient,st) #header information having patient name, gender, date of birth, etc
   
    with st.expander("**Readings**"):
        reading_option = st.selectbox(
        'Choose reading category',
        ('Blood Sugar', 'HBA1C', 'Blood Pressure','Lipid','BMI','Urine','Eye','Monofilament','Diet','Physical Activity','Education','Comorbidity','Health System','Socioeconomic','Patients'))
        st.write("**Selected reading category: " + reading_option + "**")
        utility.load_data(st,conn,patient_id,reading_option)    
    
       
    compute = 1
    with st.sidebar:
        st.markdown("<hr/>",unsafe_allow_html=True)
        st.markdown("**Select date range**", unsafe_allow_html=True)
        start = st.date_input("From",format="YYYY-MM-DD",key="start")
        end = st.date_input("To",format="YYYY-MM-DD",key="end")
        date_range = " (Latest Readings)"
        
        
    if not compute:
        st.subheader("Analysis of the individual Care Target")
        
    if st.sidebar.button('Load readings'):
        start_date = str(st.session_state.start)
        end_date = str(st.session_state.end)
        mnths,total_months = utility.number_of_months(start_date,end_date)
        mnths = utility.format_label(mnths)
        st.markdown('Duration of the analysis: '+ mnths,unsafe_allow_html=True)
        date_range = " (Readings between " + str (start_date) + " and " + str(end_date) + ")"
        with st.expander("**1. Blood Sugar**"):
            blood_sugar.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,start_date,end_date,date_range,widgets,components,compute)
        with st.expander("**2. HBA1C**"):
            hba1c.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,start_date,end_date,date_range,widgets,components,compute)
        with st.expander("**3. Blood Pressure**"):
            blood_pressure.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,start_date,end_date,date_range,widgets,components,compute)
        with st.expander("**4. Lipids**"):
            lipid.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,start_date,end_date,date_range,widgets,components,compute)
        with st.expander("**5. BMI**"):
            bmi.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,start_date,end_date,date_range,widgets,components,compute)
        with st.expander("**6. Urine**"):
            urine.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,start_date,end_date,date_range,widgets,components,compute)
        with st.expander("**7. Eye**"):
            eye.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,start_date,end_date,date_range,widgets,components,compute)
        with st.expander("**8. Monofilament**"):
            monofilament.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,start_date,end_date,date_range,widgets,components,compute)
        with st.expander("**9. Diet**"):
            diet.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,start_date,end_date,date_range,widgets,components,compute)
        with st.expander("**10. Physical Activity**"):
            physical_activity.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,start_date,end_date,date_range,widgets,components,compute)
        with st.expander("**11. Education**"):
            education.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,start_date,end_date,date_range,widgets,components,compute)
        with st.expander("**12. Comorbidity**"): 
            comorbidity.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,start_date,end_date,date_range,widgets,components,compute)
        with st.expander("**13. Health System**"):  
            health_system.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,start_date,end_date,date_range,widgets,components,compute)
        with st.expander("**14. Socioeconomic**"):
            socioeconomic.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,start_date,end_date,date_range,widgets,components,compute)
    else:
        with st.expander("**1. Blood Sugar**"):
            blood_sugar.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,'','',date_range,widgets,components,compute)
        with st.expander("**2. HBA1C**"):
            hba1c.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,'','',date_range,widgets,components,compute)
        with st.expander("**3. Blood Pressure**"):
            blood_pressure.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,'','',date_range,widgets,components,compute)
        with st.expander("**4. Lipids**"):
            lipid.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,'','',date_range,widgets,components,compute)
        with st.expander("**5. BMI**"):
            bmi.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,'','',date_range,widgets,components,compute)
        with st.expander("**6. Urine**"):
            urine.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,'','',date_range,widgets,components,compute)
        with st.expander("**7. Eye**"):
            eye.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,'','',date_range,widgets,components,compute)
        with st.expander("**8. Monofilament**"):
            monofilament.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,'','',date_range,widgets,components,compute)
        with st.expander("**9. Diet**"):
            diet.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,'','',date_range,widgets,components,compute)
        with st.expander("**10. Physical Activity**"):
            physical_activity.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,'','',date_range,widgets,components,compute)
        with st.expander("**11. Education**"):
            education.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,'','',date_range,widgets,components,compute)
        with st.expander("**12. Comorbidity**"):
            comorbidity.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,'','',date_range,widgets,components,compute)
        with st.expander("**13. Health System**"):
            health_system.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,'','',date_range,widgets,components,compute)
        with st.expander("**14. Socioeconomic**"):
            socioeconomic.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,'','',date_range,widgets,components,compute)
    
    #st.sidebar.markdown("<hr/>",unsafe_allow_html=True)
        
    st.header("Summary of all Care Targets with the Final MPC Score")
    utility.target_summaries(pd,st,patient_id)
    
    
    st.header("Corelation between HBA1C (dependent variable) and the other Care Targets")
    utility.target_correlations(conn, patient,pd,st)
 
def display(conn,patient_id):
    display_patient(conn,utility.get_patient(conn,patient_id))

    
    
