import streamlit as st
import pandas as pd

#import iplot
import cufflinks as cf

cf.go_offline()
cf.set_config_file(offline=False, world_readable=True)

from ..data_store import variants_df

plot_type_dict = {'bar':st.bar_chart, 'area': st.area_chart, 'line':st.line_chart}

def variants_widget(key=0):
    
    plot_type = st.sidebar.selectbox('Plot typeg', ['bar', 'area', 'line'])

    st.write(variants_df.head())
    country_df = variants_df[variants_df.country == "Romania"]

    #series = variants_df['variant'].value_counts().sort_values(ascending=False).to_frame()
    #df_variants_plot = series.iplot('''kind='bar''', yTitle="Number of samples", title="Variants")
     


    #plot_type_dict[plot_type](df_variants_plot)
