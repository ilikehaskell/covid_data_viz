import streamlit as st

def intro_widget():
    
    st.markdown('# ** Information Visualization Project **')
    st.markdown('### ** Team: Bogdan Ouatu, Lida Ghadamiyan, Smit Oanea **')
    
    st.markdown("***")
    st.markdown('The COVID-19 pandemic has led to a significant loss of human life throughout the world and poses an unparalleled risk to public health and our lives in general. It also made us learn some important lessons regarding how to protect us and the ones around. In order to do this, it is important to stay informed. This is what we aim to do with this project, by providing the data to be seen in a way that it is easier to be understood by the user. Through this project, the plots are customizable by selecting the prefered display version (bar, line or area). It is also possible to select which category to be shown (HCW, LTCF, AgeUNK) as well as the age group. This project shown data regarding vaccination, variants, notification rate (The number of cases, new and relapse, notified to the national health authorities during a specified period of time per 100,000 population) and hospital admission.')
    
    st.image("https://upload.wikimedia.org/wikipedia/commons/d/d6/Coronavirus_pandemic.png", width=1100)
