#%%
import streamlit as st
import pandas as pd
import plotly.express as px
import geopandas as gpd
import folium
from streamlit_folium import folium_static
from datetime import datetime
import json
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np
import streamlit_authenticator as stauth

#%%
# Path o rutas para archivos
paths = {
    "censo17": 'data_clean/CENSO17_Poblacion_rm.csv',
    "geo": 'data_clean/Comunas_RM.geojson',
    "ine_proy": 'data_clean/INE_Proyecciones_RM.csv',
    "defunciones": 'data_clean/Defunciones_2022_2024.csv',
    "casen_csv": 'data_clean/casen_17_22.csv'
}

#%%
# LECTURA DE ARCHIVOS
ine17 = pd.read_csv(paths["ine_proy"])
censo17 = pd.read_csv(paths["censo17"])
gdf = gpd.read_file(paths["geo"])
defunciones = pd.read_csv(paths["defunciones"])
casen_csv = pd.read_csv(paths["casen_csv"])
casen_csv.rename(columns={'Ponlación nacida en Chile':'Población nacida en Chile'}, inplace=True)
#%%
# Listado comunas
lista_comunas = [
    'Región Metropolitana', 
    'Alhué', 
    'Buin', 
    'Calera de Tango', 
    'Cerrillos', 
    'Cerro Navia', 
    'Colina', 
    'Conchalí', 
    'Curacaví', 
    'El Bosque', 
    'El Monte', 
    'Estación Central', 
    'Huechuraba', 
    'Independencia', 
    'Isla de Maipo',
    'La Cisterna',
    'La Florida',
    'La Granja',
    'La Pintana',
    'La Reina',
    'Lampa', 
    'Las Condes',
    'Lo Barnechea',
    'Lo Espejo',
    'Lo Prado',
    'Macul',
    'Maipú',
    'María Pinto',
    'Melipilla',
    'Ñuñoa',
    'Padre Hurtado',
    'Paine',
    'Pedro Aguirre Cerda',
    'Peñaflor',
    'Peñalolén',
    'Pirque',
    'Providencia', 
    'Pudahuel',
    'Puente Alto',
    'Quilicura',
    'Quinta Normal',
    'Recoleta',
    'Renca',
    'San Bernardo', 
    'San Joaquín',
    'San José de Maipo',
    'San Miguel',
    'San Pedro',
    'San Ramón',
    'Santiago',
    'Talagante', 
    'Tiltil',
    'Vitacura'
]
#%%
# INICIO DE LA PAGINA
#%%
# Sidebar
st.sidebar.write("## Tablero Interactivo de Comunas: Indicadores priorizados")
st.sidebar.write("Selección de Comuna")
default_index = lista_comunas.index("Región Metropolitana") if "Región Metropolitana" in lista_comunas else 0
comuna_seleccionada = st.sidebar.selectbox("Comuna:", lista_comunas, index=default_index)

#%%
# Filtrar DataFrame según comuna seleccionada
filtro_comuna = comuna_seleccionada

#%%

#%%
import streamlit as st
import pandas as pd

st.write(f"## Visor de variables socioeconómicas para {comuna_seleccionada}")

casen_csv['Comuna'] = casen_csv['Comuna'].str.upper()
casen_csv['Category'] = casen_csv['Category'].str.upper()
filtro_comuna = filtro_comuna.upper()
casen_comuna = casen_csv.loc[casen_csv['Comuna'] == filtro_comuna]
categorias = [
    'POBREZA DE INGRESOS', 
    'POBREZA MULTIDIMENSIONAL', 
    'ESCOLARIDAD MAYORES 15', 
    'ESCOLARIDAD MAYORES 18', 
    'TASAS PARTICIPACIÓN LABORAL', 
    'TASAS DE OCUPACIÓN', 
    'JEFES DE HOGAR', 
    'PREVISIÓN DE SALUD', 
    'ÍNDICE DE SANEAMIENTO', 
    'MATERIALIDAD DE LA VIVIENDA', 
    'HACINAMIENTO', 
    'MIGRANTES', 
    'ETNIAS', 
    'DISCAPACIDAD', 
    'PARTICIPACIÓN'
]

# Crear un diccionario para almacenar los DataFrames filtrados
df_dict = {}

for categoria in categorias:
    df_dict[categoria] = casen_comuna.loc[casen_comuna['Category'] == categoria].dropna(axis=1, how='all')

# Menú desplegable para seleccionar la categoría
categoria_seleccionada = st.selectbox("Seleccione la categoría de indicadores socioeconómicos:", [cat.capitalize() for cat in categorias])

# Convertir la categoría seleccionada a mayúsculas para el filtrado
categoria_seleccionada_upper = categoria_seleccionada.upper()

# Mostrar la tabla correspondiente a la categoría seleccionada
if categoria_seleccionada_upper:
    st.write(f"### {categoria_seleccionada.capitalize()}")
    df_seleccionado = df_dict[categoria_seleccionada_upper].applymap(lambda x: x if isinstance(x, str) else '{:.0f}'.format(x))
    st.dataframe(df_seleccionado.reset_index())


#%%


st.write(f"## Graficos socioeconomicos en: {comuna_seleccionada}")

st.write(f"### Pobreza de ingresos para {comuna_seleccionada}")


casen_pobrezai = casen_csv.loc[casen_csv.Category == 'POBREZA DE INGRESOS']
casen_pobrezai_comuna = casen_pobrezai[casen_pobrezai['Comuna'] == filtro_comuna]
casen_pobrezai_comuna['Pobres'] = casen_pobrezai_comuna['Pobres'] / 100
casen_pobrezai_comuna['No pobres'] = casen_pobrezai_comuna['No pobres'] / 100

# Crear gráfico de puntos con líneas
fig_pobreza_ingresos = px.scatter(
    casen_pobrezai_comuna, 
    x='Año',
    y='Pobres',
    title=f"Pobreza de ingresos en {comuna_seleccionada}",
    labels={'Pobres': 'Porcentaje de Pobreza de Ingresos', 'Año': 'Año'},
    text=casen_pobrezai_comuna['Pobres'].apply(lambda x: '{0:1.2f}%'.format(x*100)),
)

# Añadir líneas
fig_pobreza_ingresos.update_traces(mode='lines+markers+text', textposition='top center')

# Ajustar la escala del eje y
fig_pobreza_ingresos.update_layout(
    yaxis_tickformat=",.2%",
    yaxis_range=[0, 1],  # La escala del eje y de 0 a 1 (100% en términos porcentuales)
    yaxis_title='Porcentaje de Pobreza de Ingresos'
)

# Configurar el gráfico en Streamlit
col1, col2 = st.columns([2, 2])  # Ajusta el ancho de las columnas según sea necesario
df_casen_pobrezai=casen_pobrezai_comuna[['Año','Pobres','No pobres']].reset_index(drop=True)

df_casen_pobrezai[['Pobres', 'No pobres']] = df_casen_pobrezai[['Pobres', 'No pobres']] * 100
df_casen_pobrezai = df_casen_pobrezai.style.format(
    {
        'Año': '{:d}',  
        'Pobres': '{:1.2f}%',
        'No pobres': '{:1.2f}%'
    }
)

st.plotly_chart(fig_pobreza_ingresos, use_container_width=True)
st.dataframe(df_casen_pobrezai, use_container_width=True)

st.write('_Fuente: Elaboración propia a partir de encuesta CASEN 2017, 2020 y 2022_')
st.write('_https://observatorio.ministeriodesarrollosocial.gob.cl/encuesta-casen_')

#%%

# Pobreza multidimensiona
st.write(f"### Pobreza de multidimensional para {comuna_seleccionada}")


casen_pobrezam = casen_csv.loc[casen_csv.Category == 'POBREZA MULTIDIMENSIONAL']
casen_pobrezam_comuna = casen_pobrezam[casen_pobrezam['Comuna'] == filtro_comuna]
casen_pobrezam_comuna['Pobres'] = casen_pobrezam_comuna['Pobres'] / 100
casen_pobrezam_comuna['No pobres'] = casen_pobrezam_comuna['No pobres'] / 100
# Crear gráfico de puntos con líneas
fig_pobreza_ingresos = px.scatter(
    casen_pobrezam_comuna, 
    x='Año',
    y='Pobres',
    title=f"Pobreza de multidimensional en {comuna_seleccionada}",
    labels={'Pobres': 'Porcentaje de Pobreza de Ingresos', 'Año': 'Año'},
    text=casen_pobrezam_comuna['Pobres'].apply(lambda x: '{0:1.2f}%'.format(x*100)),
)

# Añadir líneas
fig_pobreza_ingresos.update_traces(mode='lines+markers+text', textposition='top center')

# Ajustar la escala del eje y
fig_pobreza_ingresos.update_layout(
    yaxis_tickformat=",.2%",
    yaxis_range=[0, 1],  # La escala del eje y de 0 a 1 (100% en términos porcentuales)
    yaxis_title='Porcentaje de Pobreza de Ingresos'
)

df_casen_pobrezam=casen_pobrezam_comuna[['Año','Pobres','No pobres']].reset_index(drop=True)
df_casen_pobrezam[['Pobres', 'No pobres']] = df_casen_pobrezam[['Pobres', 'No pobres']] * 100
df_casen_pobrezam = df_casen_pobrezam.style.format(
    {
        'Año': '{:d}',  
        'Pobres': '{:,.1f}%',  
        'No pobres': '{:,.1f}%'
    }
)

st.plotly_chart(fig_pobreza_ingresos, use_container_width=True)
st.dataframe(df_casen_pobrezam, use_container_width=True)

st.write('_Fuente: Elaboración propia a partir de encuesta CASEN 2017, 2020 y 2022_')
st.write('_https://observatorio.ministeriodesarrollosocial.gob.cl/encuesta-casen_')

#%%
# Ingresos
st.write(f"### Ingresos en {comuna_seleccionada}")
casen_ingresos = casen_csv[casen_csv['Category'] == 'INGRESOS']
casen_ingresos_comuna = casen_ingresos[casen_ingresos['Comuna'] == filtro_comuna]

casen_ingresos_comuna_long = pd.melt(
    casen_ingresos_comuna,
    id_vars=['Año'],
    value_vars=['Ingreso Autónomo', 'Ingreso Monetario', 'Ingresos del trabajo', 'Ingreso Total'],
    var_name='Tipo de Ingreso',
    value_name='Monto'
)

casen_ingresos_comuna_long['Año'] = casen_ingresos_comuna_long['Año'].astype(str)

fig_ingresos = px.bar(
    casen_ingresos_comuna_long,
    x='Año',
    y='Monto',
    color='Tipo de Ingreso',
    barmode='group',
    title=f"Distribución de Ingresos en {comuna_seleccionada}",
    labels={'Monto': 'Monto de Ingreso', 'Año': 'Año'},
)
fig_ingresos.update_layout(
    yaxis_tickformat=".0f"
)
df_casen_ingresos_comuna = casen_ingresos_comuna[['Año','Ingreso Autónomo','Ingreso Monetario','Ingresos del trabajo','Ingreso Total']].reset_index(drop=True)
df_casen_ingresos_comuna = df_casen_ingresos_comuna.style.format(
    {
        'Año': '{:d}',  
        'Ingreso Autónomo': '{:,.1f}',  
        'Ingreso Monetario': '{:,.1f}',  
        'Ingresos del trabajo': '{:,.1f}',
        'Ingreso Total': '{:,.1f}'
    },
    decimal=',',
    thousands='.'
)
st.plotly_chart(fig_ingresos, use_container_width=False)
st.dataframe(df_casen_ingresos_comuna, use_container_width=True)

st.write('_Fuente: Elaboración propia a partir de encuesta CASEN 2017, 2020 y 2022_')
st.write('_https://observatorio.ministeriodesarrollosocial.gob.cl/encuesta-casen_')

#%%
# Participación laboral
st.write(f"### Participación laboral en {comuna_seleccionada}")
casen_tasas_participacion = casen_csv.loc[casen_csv.Category == 'TASAS PARTICIPACIÓN LABORAL']
casen_tasas_participacion_comuna = casen_tasas_participacion[casen_tasas_participacion['Comuna'] == filtro_comuna]
casen_tasas_participacion_comuna['Hombres'] = casen_tasas_participacion_comuna['Hombres'] / 100
casen_tasas_participacion_comuna['Mujeres'] = casen_tasas_participacion_comuna['Mujeres'] / 100
casen_tasas_participacion_comuna_long = pd.melt(
    casen_tasas_participacion_comuna,
    id_vars=['Año'],
    value_vars=['Hombres', 'Mujeres'],
    var_name='Sexo',
    value_name='Porcentaje'
)
fig_participacion_laboral = px.bar(
    casen_tasas_participacion_comuna_long,
    x='Año',
    y='Porcentaje',
    color='Sexo',
    barmode='group',
    title=f"Tasas de participación laboral en {comuna_seleccionada}",
    labels={'Porcentaje': 'Porcentaje de Participación', 'Año': 'Año'},
    text=casen_tasas_participacion_comuna_long['Porcentaje'].apply(lambda x: '{0:1.2f}%'.format(x*100)),
    width=800,  # Ajustar el ancho del gráfico
    height=600  # Ajustar la altura del gráfico si es necesario
)
fig_participacion_laboral.update_layout(
    yaxis_tickformat=".2%",
    yaxis_title='Porcentaje de Participación'
)
fig_participacion_laboral.update_traces(texttemplate='%{text}', textposition='outside')
st.plotly_chart(fig_participacion_laboral, use_container_width=False)
st.write('_Fuente: Elaboración propia a partir de encuesta CASEN 2017, 2020 y 2022_')
st.write('_https://observatorio.ministeriodesarrollosocial.gob.cl/encuesta-casen_')
