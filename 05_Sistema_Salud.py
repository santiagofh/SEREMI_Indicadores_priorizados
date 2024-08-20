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

# LECTURA DE ARCHIVOS
fonasa = pd.read_csv('data_clean/fonasa_2024.csv')
casen_csv = pd.read_csv('data_clean/casen_17_22.csv')
casen_csv.rename(columns={'Ponlación nacida en Chile':'Población nacida en Chile'}, inplace=True)

# Listado comunas
lista_comunas = [
    'Región Metropolitana', 'Alhué', 'Buin', 'Calera de Tango', 'Cerrillos', 'Cerro Navia',
    'Colina', 'Conchalí', 'Curacaví', 'El Bosque', 'El Monte', 'Estación Central',
    'Huechuraba', 'Independencia', 'Isla de Maipo', 'La Cisterna', 'La Florida', 'La Granja',
    'La Pintana', 'La Reina', 'Lampa', 'Las Condes', 'Lo Barnechea', 'Lo Espejo',
    'Lo Prado', 'Macul', 'Maipú', 'María Pinto', 'Melipilla', 'Ñuñoa', 'Padre Hurtado',
    'Paine', 'Pedro Aguirre Cerda', 'Peñaflor', 'Peñalolén', 'Pirque', 'Providencia',
    'Pudahuel', 'Puente Alto', 'Quilicura', 'Quinta Normal', 'Recoleta', 'Renca',
    'San Bernardo', 'San Joaquín', 'San José de Maipo', 'San Miguel', 'San Pedro',
    'San Ramón', 'Santiago', 'Talagante', 'Tiltil', 'Vitacura'
]

# TITULO INTRODUCCION
st.write('# Región Metropolitana y sus comunas: Sistema de Salud')
st.write('Este tablero interactivo presenta indicadores de Sistema de Salud de la Región Metropolitana de Santiago y sus comunas.')

# Sidebar
st.sidebar.write("## Tablero Interactivo de Comunas: Indicadores priorizados")
st.sidebar.write("Selección de Comuna")
default_index = lista_comunas.index("Región Metropolitana") if "Región Metropolitana" in lista_comunas else 0
comuna_seleccionada = st.sidebar.selectbox("Comuna:", lista_comunas, index=default_index)

filtro_comuna = comuna_seleccionada.upper()

# Convertir las columnas numéricas a float
for df in [fonasa, casen_csv]:
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].astype(float)

# Filtrar y mostrar los DataFrames

if filtro_comuna != "REGIÓN METROPOLITANA":
    df_sexo = fonasa[(fonasa['Category'] == 'SEXO') & (fonasa['COMUNA'] == filtro_comuna)]
    df_tramo = fonasa[(fonasa['Category'] == 'TRAMO FONASA') & (fonasa['COMUNA'] == filtro_comuna)]
    df_edad = fonasa[(fonasa['Category'] == 'TRAMO EDAD') & (fonasa['COMUNA'] == filtro_comuna)]
else:
    df_sexo = fonasa[fonasa['Category'] == 'SEXO']
    df_tramo = fonasa[fonasa['Category'] == 'TRAMO FONASA']
    df_edad = fonasa[fonasa['Category'] == 'TRAMO EDAD']

# Limpiar columnas no deseadas
for df in [df_sexo, df_tramo, df_edad]:
    df.drop(columns=['Category', 'CODIGO'], errors='ignore', inplace=True)
    df.dropna(axis=1, inplace=True)

# Renombrar columnas y eliminar la palabra 'años'
df_edad = df_edad.rename(columns={'00 a 02 años': 'Menor de 2'})
df_edad.columns = df_edad.columns.str.replace('años', '').str.strip()

# Aplicar el formato a los DataFrames con 0 decimales
def format_dataframe(df):
    # Seleccionar solo las columnas numéricas
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    # Aplicar el formato solo a las columnas numéricas
    return df.style.format({col: "{:,.0f}".format for col in numeric_columns}, thousands='.', decimal=',')

df_sexo_formatted = format_dataframe(df_sexo)
df_tramo_formatted = format_dataframe(df_tramo)
df_edad_formatted = format_dataframe(df_edad)

# Mostrar los DataFrames
st.write(f"### Poblacion de beneficiarios FONASA clasificados por sexo en {comuna_seleccionada} 2024")
st.dataframe(df_sexo_formatted)

st.write(f"### Poblacion de beneficiarios FONASA por Tramo en {comuna_seleccionada} 2024")
st.dataframe(df_tramo_formatted)

st.write(f"### Poblacion de beneficiarios FONASA por rango etario en {comuna_seleccionada} 2024")
st.dataframe(df_edad_formatted)
