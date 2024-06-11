#%%
import streamlit as st
import pandas as pd
import plotly.express as px
#%%
# Configuración de la página
st.set_page_config(page_title="Análisis de Comunas en Región Metropolitana: IPS", layout='wide', initial_sidebar_state='expanded')
#%%

st.image('img/seremi-100-años.png', width=300)
st.title("Análisis de Comunas en Región Metropolitana: Indice de prioridad social (IPS)")
st.write("""
    Bienvenido al dashboard de análisis de comunas en la Región Metropolitana. 
    Aquí puedes encontrar información sobre los indicadores de prioridad social de cada comuna.
""")
#%%
# Cargar los datos
df_ips = pd.read_excel('data_raw/IPS_2022.xlsx')

# Crear el gráfico
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
                 'SIN PRIORIDAD': 'green'
             })

# Personalizar el gráfico
fig.update_layout(xaxis_tickangle=-45)

# Mostrar el gráfico en Streamlit
st.plotly_chart(fig, use_container_width=True)
