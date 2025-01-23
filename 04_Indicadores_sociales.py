#%%
import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit_authenticator as stauth
#%%
st.title("Región Metropolitana y sus comunas: Indice de prioridad social (IPS)")
st.write("""
Información sobre los indicadores de prioridad social de cada comuna.
""")
#%%
df_ips = pd.read_excel('data_raw/IPS_2022.xlsx')
fig = px.bar(df_ips, 
             x='Comuna', 
             y='IPS 2022', 
             color='Categoría', 
             title='Índice de Prioridad Social 2022 por Comuna',
             labels={'IPS 2022': 'Puntaje IPS', 'Comuna': 'Comuna'},
             color_discrete_map={
                 'ALTA PRIORIDAD': 'red',
                 'MEDIA ALTA PRIORIDAD': 'orange',
                 'MEDIA BAJA PRIORIDAD': 'yellow',
                 'BAJA PRIORIDAD': 'green',
                 'SIN PRIORIDAD': 'lightgreen'
             })
fig.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig, use_container_width=True)
