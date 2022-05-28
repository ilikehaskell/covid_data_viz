import streamlit as st
import pandas as pd
import numpy as np

from ..data_store import vaccine_df
from ..plot_utils import plotable

from .country_info import get_country_info

plot_type_dict = {'bar':st.bar_chart, 'area': st.area_chart, 'line':st.line_chart}

def vaccine_widget(groups, special_groups, key = 0):
    plot_type = st.sidebar.selectbox('Plot type', ['bar', 'area', 'line'], key=key)

    
    st.markdown('The coronavirus COVID-19 is affecting 227 countries and territories. The day is reset after midnight GMT+0. The list of countries and their regional classification is based on the United Nations Geoscheme.')
    
    countries = sorted(list(set(vaccine_df.ReportingCountry)))
    
    

    romania_index = countries.index('RO')
    country = st.selectbox('Country', options=countries, index=romania_index, key=key)
    country_df = vaccine_df[vaccine_df.ReportingCountry == country]

    
    denominator_group_dict = country_df.groupby('TargetGroup').first().Denominator.fillna(0).to_dict()
    with st.expander('Country Info'):
        get_country_info(country, country_df)
    # handle countries with no distinction betweeen underage groups
    underage_group_set = set(["Age0_4","Age5_9","Age10_14","Age15_17"])
    if underage_group_set <= set(groups) and not (set(underage_group_set) <= set(denominator_group_dict)):
        groups = (set(groups) - set(underage_group_set)) | set(["Age<18"])
        groups = list(groups)


    population_considered = sum(denominator_group_dict[group] for group in groups+special_groups if group in denominator_group_dict)

    if not population_considered:
        st.warning('There is no one in the target groups, using data for all population')
        groups = ['ALL']
        population_considered = sum(denominator_group_dict[group] for group in groups+special_groups if group in denominator_group_dict)


    country_population = country_df.groupby('ReportingCountry').first().Population[0]


    country_df = country_df.rename(columns={'YearWeekISO':'YW'})


    full_vaccine_df = country_df[['YW', 'FirstDose', 'SecondDose', 'NumberDosesReceived', 'Vaccine']]
    full_vaccine_df['FullVaccine'] = full_vaccine_df.apply(lambda row: row.FirstDose if row.Vaccine=='JANSS' else row.SecondDose, axis=1)

    # full_vaccine_df['FullVaccine']

    all_df = country_df[country_df.TargetGroup == 'ALL']

    all_df['FirstAndSecondJabs'] = all_df.apply(lambda row: row.FirstDose + row.SecondDose, axis=1) 
    all_df['RemainingJabs'] = all_df['NumberDosesReceived'] - all_df["FirstAndSecondJabs"]

    # full_df['TotalRemainingJabs'] = full_df.RemainingJabs.sum(axis=1)
    # st.header('Number of remaining jabs')
    
    # st.line_chart(
    #     plotable(full_df.RemainingJabs)
    #     )


    all_df = all_df.fillna(0)
    all_df = all_df.pivot_table(
        values = ['NumberDosesReceived', 'RemainingJabs'],
        index='YW',
        columns=['Vaccine'],
        aggfunc=np.sum
        )

    full_vaccine_df = full_vaccine_df[country_df.TargetGroup.isin(groups+special_groups)].fillna(0)
    full_vaccine_df = full_vaccine_df.pivot_table(
        values = ['FullVaccine'],
        index='YW',
        columns=['Vaccine'],
        aggfunc=np.sum
        )

    full_df = pd.concat([full_vaccine_df, all_df[['NumberDosesReceived', 'RemainingJabs']] ], axis=1, join='inner')
    full_df = full_df.fillna(0).cumsum().fillna(0)

    st.header('Number of doses received')
    plot_type_dict[plot_type](
        plotable(full_df['NumberDosesReceived'])
        )

    st.header('Number of doses left')
    plot_type_dict[plot_type](
        plotable(full_df['RemainingJabs'])
        )



    full_df['TotalFullVaccine'] = full_df.FullVaccine.sum(axis=1)

    full_df['FullVaccinePercentageFromGroups'] = full_df.TotalFullVaccine / population_considered
    full_df['FullVaccinePercentage'] = full_df.TotalFullVaccine / country_population
    st.header('Number of fully applied vaccines')
    
    plot_type_dict[plot_type](
        plotable(full_df.FullVaccine)
        )



    st.header('Percentage of fully vaccinated from selected groups / Groups population')
    
    plot_type_dict[plot_type](
        plotable(full_df, ['FullVaccinePercentageFromGroups'])
        )

    st.header('Percentage of fully vaccinated from selected groups / Entire population')
    
    plot_type_dict[plot_type](
        plotable(full_df, ['FullVaccinePercentage'])
        )
    # st.write(plotable(full_df, ['FullVaccinePercentage', 'FullVaccinePercentageFromGroups']).index)
    ##############
    # base = alt.Chart(plotable(full_df, ['FullVaccinePercentage', 'FullVaccinePercentageFromGroups', 'TotalFullVaccine']).reset_index()).mark_point().encode(
    #     x = 'YW'
    # )
    
    # line = base.mark_line(interpolate='monotone').encode(
    #     alt.Y('TotalFullVaccine',
    #         axis=alt.Axis(title='TotalFullVaccine', titleColor='#5276A7'),
    #         scale=alt.Scale(domain=[0, population_considered])
    #         )
    # )
    # line2 = base.mark_line(interpolate='monotone').encode(
    #     alt.Y('FullVaccinePercentageFromGroups',
    #         axis=alt.Axis(title='FullVaccinePercentageFromGroups', titleColor='#5276A7'),
    #         scale=alt.Scale(domain=[0, 1])
    #         )
    # ).interactive()

    # q = alt.layer(line, line2).resolve_scale(
    #     y = 'independent'
    # ).interactive()
    
    # st.altair_chart(q, use_container_width=True)
    ################

    st.header('Number of fully vaccinated')
    plot_type_dict[plot_type](full_df['TotalFullVaccine'])

    
