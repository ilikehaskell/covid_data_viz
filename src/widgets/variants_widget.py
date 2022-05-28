import streamlit as st
import pandas as pd

import numpy as np
import cufflinks as cf
import plotly.express as px

cf.go_offline()
cf.set_config_file(offline=False, world_readable=True)

from ..data_store import variants_df

plot_type_dict = {'bar':st.bar_chart, 'area': st.area_chart, 'line':st.line_chart}

def variants_widget(key=0):
    
    st.header("Variants")
    plot_type = st.sidebar.selectbox('Plot type', ['bar', 'area', 'line'], key=key)
    
    st.markdown('The coronavirus COVID-19 is affecting 227 countries and territories. The day is reset after midnight GMT+0. The list of countries and their regional classification is based on the United Nations Geoscheme.')
    
    # default country
    countries = sorted(list(set(variants_df.country)))
    romania_index = countries.index('Romania')
    country = st.selectbox('Select country', options=countries, index=romania_index, key=key)
    vdf = variants_df[variants_df.country == country]
    
    # Count df
    df = vdf['variant'].value_counts().sort_values(ascending=False).to_frame()
    
    # classic
    st.header("Variants Count")
    plot_type_dict[plot_type](df['variant'])
    
    
    # box
    st.header('BoxPlot for each feature')
    fig = vdf.iplot(kind='box', asFigure=True)
    st.plotly_chart(fig)
    
    
    # violin
    st.header('Distribution of variants')
    fig1 = px.violin(vdf, y="variant", box=True, points='all')
    st.plotly_chart(fig1)
