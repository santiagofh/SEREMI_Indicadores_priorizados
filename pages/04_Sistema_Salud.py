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
    'Todas las comunas', 'Alhué', 'Buin', 'Calera de Tango', 'Cerrillos', 'Cerro Navia', 'Colina', 
    'Conchalí', 'Curacaví', 'El Bosque', 'El Monte', 'Estación Central', 'Huechuraba', 'Independencia', 
    'Isla de Maipo', 'La Cisterna', 'La Florida', 'La Granja', 'La Pintana', 'La Reina', 'Lampa', 
    'Las Condes', 'Lo Barnechea', 'Lo Espejo', 'Lo Prado', 'Macul', 'Maipú', 'María Pinto', 'Melipilla', 
    'Padre Hurtado', 'Paine', 'Pedro Aguirre Cerda', 'Peñaflor', 'Peñalolén', 'Pirque', 'Providencia', 
    'Pudahuel', 'Puente Alto', 'Quilicura', 'Quinta Normal', 'Recoleta', 'Renca', 'San Bernardo', 
    'San Joaquín', 'San José de Maipo', 'San Miguel', 'San Pedro', 'San Ramón', 'Santiago', 'Talagante', 
    'Tiltil', 'Vitacura', 'Ñuñoa'
]

#%%
# INICIO DE LA PAGINA
st.set_page_config(page_title="Análisis de Comunas en Región Metropolitana", layout='wide', initial_sidebar_state='expanded')
# TITULO INTRODUCCION
st.write('# Región Metropolitana y sus comunas: Sistema de Salud')
st.write('Este tablero interactivo presenta indicadores de Sistema de Salud de la Región Metropolitana de Santiago y sus comunas.')

#%%
# Sidebar
st.sidebar.write("## Tablero Interactivo de Comunas: Indicadores priorizados")
st.sidebar.write("Selección de Comuna")
default_index = lista_comunas.index("Todas las comunas") if "Todas las comunas" in lista_comunas else 0
comuna_seleccionada = st.sidebar.selectbox("Comuna:", lista_comunas, index=default_index)

st.sidebar.header("Selección año de proyección de población del INE")
current_year = datetime.now().year
select_year_int = st.sidebar.slider("Año:", min_value=2002, max_value=2035, value=current_year)
select_year = f'Poblacion {select_year_int}'

#%%
# Filtrar DataFrame según comuna seleccionada
if comuna_seleccionada == "Todas las comunas":
    filtro_comuna = "Región Metropolitana"
else:
    filtro_comuna = comuna_seleccionada
#%%

import statsmodels.api as sm

# Afiliación a Sistemas de Previsión
st.write(f"### Afiliación a Sistemas de Previsión en {comuna_seleccionada}")
column_rename_map = {
    'fonasa': 'FONASA',
    'ff.aa. y del orden': 'FF.AA. y del Orden',
    'isapre': 'Isapre',
    'ninguno (particular)': 'Ninguno (Particular)',
    'otro sistema': 'Otro Sistema',
    'no sabe': 'No Sabe'
}
color_map = {
    'FONASA': '#0068c9',
    'Isapre': '#83c9ff',
    'FF.AA. y del Orden': '#29b09d',
    'Otro Sistema': '#7defa1',
    'No Sabe': '#ffabab',
    'Ninguno (Particular)': '#ff2b2b'
}
casen_prevision_salud = casen_csv[casen_csv['Category'] == 'PREVISIÓN DE SALUD']
casen_prevision_salud_comuna = casen_prevision_salud[casen_prevision_salud['Comuna'] == filtro_comuna]
casen_prevision_salud_comuna = casen_prevision_salud_comuna.rename(columns=column_rename_map)

for col in column_rename_map.values():
    if col in casen_prevision_salud_comuna.columns:
        casen_prevision_salud_comuna[col] = casen_prevision_salud_comuna[col] / 100

casen_prevision_salud_comuna_long = pd.melt(
    casen_prevision_salud_comuna,
    id_vars=['Año'],
    value_vars=list(column_rename_map.values()),
    var_name='Tipo de Previsión',
    value_name='Porcentaje'
)
fig_bar = px.bar(
    casen_prevision_salud_comuna_long,
    x='Año',
    y='Porcentaje',
    color='Tipo de Previsión',
    barmode='group',
    title=f"Distribución de Previsión de Salud en {comuna_seleccionada}",
    labels={'Porcentaje': 'Porcentaje de la Población', 'Año': 'Año'},
    color_discrete_map=color_map
)

# Realizar la regresión lineal para FONASA
casen_prevision_salud_comuna['Año'] = casen_prevision_salud_comuna['Año'].astype(int)
X = casen_prevision_salud_comuna[['Año']]
X = sm.add_constant(X)  # Agregar una constante (intercepto) al modelo
y = casen_prevision_salud_comuna['FONASA']
model = sm.OLS(y, X).fit()
predictions = model.predict(X)

# Obtener los parámetros del modelo
intercept = model.params['const']
slope = model.params['Año']
r_squared = model.rsquared
formula = f"y = {intercept:.2f} + {slope:.2f}*x"

# Añadir la línea de tendencia al gráfico de barras
fig_trend = px.scatter(
    casen_prevision_salud_comuna,
    x='Año',
    y='FONASA',
    trendline="ols",
    labels={'FONASA': 'Porcentaje de la Población', 'Año': 'Año'}
)
fig_trend.data[1].marker.color = 'red'
fig_trend.data[1].name = 'Tendencia FONASA'
fig_trend.data[0].showlegend = False
fig = fig_bar.add_traces(fig_trend.data[1:])
fig.update_layout(
    yaxis_tickformat=".2%",
    yaxis_title='Porcentaje de la Población'
)
st.plotly_chart(fig)

# Mostrar la fórmula de la regresión lineal y el R cuadrado debajo del gráfico
st.write(f"**Fórmula de la regresión lineal para FONASA:** {formula}")
st.write(f"**R² (coeficiente de determinación):** {r_squared:.2f}")
st.write("El R² es una medida de qué tan bien los valores observados son replicados por el modelo, basado en la proporción de la variabilidad total de los resultados que puede ser explicada por el modelo.")

st.write('_Fuente: Elaboración propia a partir de encusta CASEN 2017, 2020 y 2022_')
st.write('_https://observatorio.ministeriodesarrollosocial.gob.cl/encuesta-casen_')

