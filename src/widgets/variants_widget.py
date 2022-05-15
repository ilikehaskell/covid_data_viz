import streamlit as st
import pandas as pd

from ..data_store import variants_df

plot_type_dict = {'bar':st.bar_chart, 'area': st.area_chart, 'line':st.line_chart}

def variants_widget(key=0):
    
    plot_type = st.sidebar.selectbox('Plot type', ['bar', 'area', 'line'])

    st.write(variants_df.head())
    country_df = variants_df[variants_df.country == "Romania"]
    #df_variants = variants_df['variant'].value_counts().rename_axis('unique_values').reset_index(name='counts')



    #plot_type_dict[plot_type](df_variants)
