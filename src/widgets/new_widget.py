import streamlit as st
import pandas as pd

from ..data_store import hospital_admission_df

plot_type_dict = {'bar':st.bar_chart, 'area': st.area_chart, 'line':st.line_chart}

def hospital_admission_widget(key = 0):
    plot_type = st.sidebar.selectbox('Plot type', ['bar', 'area', 'line'])
    

    countries = sorted(list(set(hospital_admission_df.country)))
    romania_index = countries.index('Romania')
    country = st.selectbox('Country', options=countries, index=romania_index, key=key)

    country_df = hospital_admission_df[hospital_admission_df.country == country]
    country_df = country_df.swapaxes(0,1)
    country_df = country_df.rename(columns={'year_week': 'YW'})
    country_df = country_df.set_index('YW')
    #st.header("")
    cd_df = pd.concat( [country_df[country_df.indicator == 'value'].rate_14_day.rename('value'), country_df[country_df.indicator == 'deaths'].rate_14_day.rename('deaths')], axis=1)



    #st.line_chart(cd_df)
    st.header("Hospital admissions")
    plot_type_dict[plot_type](country_df, )
   
   #st.line_chart(country_df.head())

    # st.line_chart()