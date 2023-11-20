import streamlit as st
import pandas as pd
import numpy as np
import random
import time
from datetime import datetime
import altair as alt
###custom modules#############
import pages.modules.utilities as utility
import pages.modules.blood_sugar as blood_sugar
import pages.modules.blood_pressure as blood_pressure
import pages.modules.lipid as lipid
import pages.modules.bmi as bmi


conn = utility.get_database_connection() #database connection
utility.set_title(st) #Title of the page


### display patient medical readings ###
def display_patient(patient):
    utility.patient_header_info(patient,st) #header information having patient name, gender, date of birth, etc
    start = st.date_input("From:",format="YYYY-MM-DD",key="start")
    end = st.date_input("To:",format="YYYY-MM-DD",key="end")
    date_range = " (Latest readings)"
    if st.button('Load readings for the selected range'):
        start_date = st.session_state.start
        end_date = st.session_state.end
        date_range = " (Readings between " + str (start_date) + " and " + str(end_date) + ")"
        blood_sugar.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,start_date,end_date,date_range)
    else:
        blood_sugar.load_readings_with_chart(patient_id,st,conn,utility,pd,alt,datetime,'','',date_range)
   
   
    #blood_sugar.hba1c_readings_with_chart(patient_id,st,conn,utility)
    #blood_pressure.bp_readings_with_chart(patient_id,st,conn,utility)
    #lipid.lipid_readings_with_chart(patient_id,st,conn,utility)
    #bmi.bmi_readings_with_chart(patient_id,st,conn,utility)
  
# retrieve patient id via URL   
patient_id = utility.get_patient_id_via_url(st)
 
# display patient readings if the patient id is not null
if patient_id:
   display_patient(utility.get_patient(conn,patient_id))
    
    