import streamlit as st
import pandas as pd


import numpy as np
import cufflinks as cf
import plotly.express as px
import plotly.graph_objects as go

cf.go_offline()
cf.set_config_file(offline=False, world_readable=True)

from ..data_store import hospital_admission_df

plot_type_dict = { 'area': st.area_chart, 'bar':st.bar_chart,'line':st.line_chart}

def hospital_admission_widget(key = 0):
    plot_type = st.sidebar.selectbox('Plot type', ['area', 'bar', 'line'])
    

    countries = sorted(list(set(hospital_admission_df.country)))
    romania_index = countries.index('Czechia')
    country = st.selectbox('Country', options=countries, index=romania_index, key=key)
    country_df = hospital_admission_df[hospital_admission_df.country == country]

    
    # Daily adm
    cd_df1 = country_df.set_index('date')
    cd_df1 = cd_df1[cd_df1.indicator == 'Daily hospital occupancy']

    st.header("Hospital admissions")
    plot_type_dict[plot_type](cd_df1['value'])
   

    # Daily ICU
    cd_df2 = country_df.set_index('date')
    cd_df2 = cd_df2[cd_df2.indicator == 'Daily ICU occupancy']

    st.header("Daily ICU occupancy")
    plot_type_dict[plot_type](cd_df2['value'])
    
    
    # Weekly adm
    cd_df3 = country_df.set_index('year_week')
    cd_df3 = cd_df3[cd_df3.indicator == 'Weekly new hospital admissions per 100k']

    st.header("Weekly new hospital admissions per 100k")
    plot_type_dict[plot_type](cd_df3['value'])
    
    
    