import streamlit as st
import pandas as pd

import numpy as np
import cufflinks as cf
import plotly.express as px
import plotly.graph_objects as go

cf.go_offline()
cf.set_config_file(offline=False, world_readable=True)

from ..data_store import notification_rate_df

plot_type_dict = {'bar':st.bar_chart, 'area': st.area_chart, 'line':st.line_chart}

def notification_rate_widget(key = 0):
    plot_type = st.sidebar.selectbox('Plot type', ['bar', 'area', 'line'], key=key)
    countries = sorted(list(set(notification_rate_df.country)))
    romania_index = countries.index('Romania')
    country = st.selectbox('Country', options=countries, index=romania_index, key=key)

    country_df = notification_rate_df[notification_rate_df.country == country]
    country_df = country_df.rename(columns={'year_week': 'YW'})
    country_df = country_df.set_index('YW')
    country_df
    st.header("Cases per 100.000, Deaths per 1 mil.")
    cd_df = pd.concat( [country_df[country_df.indicator == 'cases'].rate_14_day.rename('cases'), country_df[country_df.indicator == 'deaths'].rate_14_day.rename('deaths')], axis=1)
    #st.line_chart(cd_df)
    plot_type_dict[plot_type](cd_df)
    st.header("Deaths/Cases")
    #st.line_chart(cd_df.deaths/cd_df.cases/10)
    plot_type_dict[plot_type](cd_df.deaths/cd_df.cases/10)

    # st.line_chart()
    
    
    
    # violin
    
    #cases
    st.header('Distribution of cases')
    st.text('The width of the violin in a certain Y point corresponds with the number of weeks in which there were Y new cases notified"')
    fig1 = px.violin(cd_df, y="cases", box=True, points='all')
    st.plotly_chart(fig1)
    
    #deaths
    st.header('Distribution of deaths')
    st.text('The width of the violin in a certain Y point corresponds with the number of weeks in which there were Y new deaths notified"')
    fig2 = go.Figure(data=go.Violin(y=cd_df['deaths'], box_visible=True, line_color='green',
                               meanline_visible=True, fillcolor='lightseagreen', opacity=0.6,
                               x0='deaths', points='all'))
    st.plotly_chart(fig2)
    