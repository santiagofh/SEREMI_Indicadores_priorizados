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
# LECTURA DE ARCHIVOS
fonasa=pd.read_csv('data_clean/fonasa_2024.csv')
casen_csv = pd.read_csv('data_clean/casen_17_22.csv')
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
# TITULO INTRODUCCION
st.write('# Región Metropolitana y sus comunas: Sistema de Salud')
st.write('Este tablero interactivo presenta indicadores de Sistema de Salud de la Región Metropolitana de Santiago y sus comunas.')

#%%
# Sidebar
st.sidebar.write("## Tablero Interactivo de Comunas: Indicadores priorizados")
st.sidebar.write("Selección de Comuna")
default_index = lista_comunas.index("Todas las comunas") if "Todas las comunas" in lista_comunas else 0
comuna_seleccionada = st.sidebar.selectbox("Comuna:", lista_comunas, index=default_index)

#%%
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
    'Ninguno (Particular)': 'gray'
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

order = ['FONASA', 'Isapre', 'FF.AA. y del Orden', 'Otro Sistema', 'No Sabe', 'Ninguno (Particular)']

casen_prevision_salud_comuna_long['Tipo de Previsión'] = pd.Categorical(
    casen_prevision_salud_comuna_long['Tipo de Previsión'],
    categories=order,
    ordered=True
)

casen_prevision_salud_comuna_long = casen_prevision_salud_comuna_long.sort_values('Tipo de Previsión')

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
fig_trend.data[1].marker.color = 'blue'
fig_trend.data[1].name = 'Tendencia FONASA'
fig_trend.data[0].showlegend = False
fig = fig_bar.add_traces(fig_trend.data[1:])
fig.update_layout(
    yaxis_tickformat=".2%",
    yaxis_title='Porcentaje de la Población',
    # width=1200,  # Ancho del gráfico
    # height=600,  # Altura del gráfico
    margin=dict(l=50, r=50, t=50, b=50)  # Margen para centrar
)

st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
st.plotly_chart(fig, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# Mostrar la fórmula de la regresión lineal y el R cuadrado debajo del gráfico
st.write(f"**Fórmula de la regresión lineal para FONASA:** {formula}")
st.write(f"**R² (coeficiente de determinación):** {r_squared:.2f}")
st.write("El R² es una medida de qué tan bien los valores observados son replicados por el modelo, basado en la proporción de la variabilidad total de los resultados que puede ser explicada por el modelo.")

st.write('_Fuente: Elaboración propia a partir de encusta CASEN 2017, 2020 y 2022_')
st.write('_https://observatorio.ministeriodesarrollosocial.gob.cl/encuesta-casen_')
#%%
# Gráfico de Sexo

# Convertir filtro_comuna a mayúsculas
filtro_comuna = filtro_comuna.upper()

# Asegurarse de que los valores en la columna 'COMUNA' de 'fonasa' estén en mayúsculas
fonasa['COMUNA'] = fonasa['COMUNA'].str.upper()

# Filtrar datos si no es "TODAS LAS COMUNAS"
if filtro_comuna != "REGIÓN METROPOLITANA":
    df_sexo = fonasa[(fonasa['Category'] == 'SEXO') & (fonasa['COMUNA'] == filtro_comuna)]
else:
    df_sexo = fonasa[fonasa['Category'] == 'SEXO']

df_sexo = df_sexo.drop(columns=['Category'], errors='ignore')
df_sexo = df_sexo.drop(columns=['CODIGO'], errors='ignore')
df_sexo = df_sexo.dropna(axis=1)


# %%
# Gráfico de Sexo

# Convertir filtro_comuna a mayúsculas
filtro_comuna = filtro_comuna.upper()

# Asegurarse de que los valores en la columna 'COMUNA' de 'fonasa' estén en mayúsculas
fonasa['COMUNA'] = fonasa['COMUNA'].str.upper()

# Filtrar datos si no es "TODAS LAS COMUNAS"
if filtro_comuna != "REGIÓN METROPOLITANA":
    df_tramo = fonasa[(fonasa['Category'] == 'TRAMO FONASA') & (fonasa['COMUNA'] == filtro_comuna)]
else:
    df_tramo = fonasa[fonasa['Category'] == 'TRAMO FONASA']

df_tramo = df_tramo.drop(columns=['Category'], errors='ignore')
df_tramo = df_tramo.drop(columns=['CODIGO'], errors='ignore')
df_tramo = df_tramo.dropna(axis=1)

# %%
# %%
# Gráfico de Sexo

# Convertir filtro_comuna a mayúsculas
filtro_comuna = filtro_comuna.upper()

# Asegurarse de que los valores en la columna 'COMUNA' de 'fonasa' estén en mayúsculas
fonasa['COMUNA'] = fonasa['COMUNA'].str.upper()

# Filtrar datos si no es "TODAS LAS COMUNAS"
if filtro_comuna != "REGIÓN METROPOLITANA":
    df_edad = fonasa[(fonasa['Category'] == 'TRAMO EDAD') & (fonasa['COMUNA'] == filtro_comuna)]
else:
    df_edad = fonasa[fonasa['Category'] == 'TRAMO EDAD']

df_edad = df_edad.drop(columns=['Category'], errors='ignore')
df_edad = df_edad.drop(columns=['CODIGO'], errors='ignore')
df_edad = df_edad.dropna(axis=1)
df_edad = df_edad.rename(columns={'00 a 02 años':'Menor de 2'})
df_edad.columns = df_edad.columns.str.replace('años', '').str.strip()

# %%
# Convertir columnas numéricas a float o int
# Convertir columnas numéricas a float o int
for col in df_sexo.columns:
    if pd.api.types.is_numeric_dtype(df_sexo[col]):  # Verifica si la columna es numérica
        df_sexo[col] = df_sexo[col].astype(float)

# Convertir columnas numéricas a float o int para df_tramo
for col in df_tramo.columns:
    if pd.api.types.is_numeric_dtype(df_tramo[col]):  # Verifica si la columna es numérica
        df_tramo[col] = df_tramo[col].astype(float)

# Convertir columnas numéricas a float o int para df_edad
for col in df_edad.columns:
    if pd.api.types.is_numeric_dtype(df_edad[col]):  # Verifica si la columna es numérica
        df_edad[col] = df_edad[col].astype(float)
 
def format_number(value):
    if isinstance(value, (int, float)):
        return f"{value:.0f}".replace(",", "")
    return value

df_sexo_formatted = df_sexo.applymap(format_number)
df_tramo_formatted = df_tramo.applymap(format_number)
df_edad_formatted = df_edad.applymap(format_number)

# st.write(f"### Poblacion de beneficiarios FONASA clasificados por sexo en {comuna_seleccionada} 2024")
# st.write(df_sexo_formatted)
# st.write(f"### Poblacion de beneficiarios FONASA por Tramo en {comuna_seleccionada} 2024")
# st.write(df_tramo_formatted)
# st.write(f"### Poblacion de beneficiarios FONASA por rango etario en {comuna_seleccionada} 2024")
# st.write(df_edad_formatted)

#%%
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
#%%

#%%
# Mostrar los DataFrames
st.write(f"### Poblacion de beneficiarios FONASA clasificados por sexo en {comuna_seleccionada} 2024")
st.dataframe(df_sexo_formatted)

st.write(f"### Poblacion de beneficiarios FONASA por Tramo en {comuna_seleccionada} 2024")
st.dataframe(df_tramo_formatted)

st.write(f"### Poblacion de beneficiarios FONASA por rango etario en {comuna_seleccionada} 2024")
st.dataframe(df_edad_formatted)
