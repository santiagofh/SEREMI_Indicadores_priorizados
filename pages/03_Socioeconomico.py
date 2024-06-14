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
def display_centered_chart(fig):
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        st.plotly_chart(fig, use_container_width=True)
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
logo_horizontal = 'img/horizontal_remolino_blue.png'
logo_icono = 'img/icon_remolino_blue.png'
st.logo(logo_horizontal, icon_image=logo_horizontal)
#%%
# Sidebar
st.image('img/seremi-100-años.png', width=300)
st.sidebar.write("## Tablero Interactivo de Comunas: Indicadores priorizados")
st.sidebar.write("Selección de Comuna")
default_index = lista_comunas.index("Todas las comunas") if "Todas las comunas" in lista_comunas else 0
comuna_seleccionada = st.sidebar.selectbox("Comuna:", lista_comunas, index=default_index)



#%%
# Filtrar DataFrame según comuna seleccionada
if comuna_seleccionada == "Todas las comunas":
    filtro_comuna = "Región Metropolitana"
else:
    filtro_comuna = comuna_seleccionada

#%%
# TITULO INTRODUCCION
st.write('# Región Metropolitana y sus comunas: Socioeconómicos')
st.write('Este tablero interactivo presenta indicadores socioeconomicos priorizados de la Región Metropolitana de Santiago y sus comunas.')

st.markdown('<a name="indicadores-socioeconomicos"></a>', unsafe_allow_html=True)
st.write("## Indicadores Socioeconómicos")

# Lista de categorías con columnas en porcentaje
percentage_categories = [
    'Pobreza De Ingresos', 'Pobreza Multidimensional', 'Escolaridad Mayores 15', 'Escolaridad Mayores 18',
    'Tasas Participación Laboral', 'Tasas De Ocupación', 'Jefes De Hogar', 'Previsión De Salud',
    'Índice De Saneamiento', 'Materialidad De La Vivienda', 'Hacinamiento', 'Migrantes', 'Etnias',
    'Discapacidad', 'Participación'
]

# Obtener las categorías únicas
categories = casen_csv['Category'].unique()

# Crear un diccionario para almacenar las tablas por categoría
tables = {}

for category in categories:
    # Filtrar los datos por categoría y comuna seleccionada
    df_cat = casen_csv[(casen_csv['Category'] == category) & (casen_csv['Comuna'] == filtro_comuna)]
    
    # Identificar y eliminar las columnas con valores nulos
    df_cat = df_cat.dropna(axis=1, how='any')
    
    # Eliminar las columnas 'Category' y 'Comuna'
    if 'Category' in df_cat.columns:
        df_cat = df_cat.drop(columns=['Category'])
    if 'Comuna' in df_cat.columns:
        df_cat = df_cat.drop(columns=['Comuna'])
    
    # Convertir la columna 'Año' a enteros
    if 'Año' in df_cat.columns:
        df_cat['Año'] = df_cat['Año'].astype(int)
    
    # Guardar la tabla en el diccionario
    tables[category] = df_cat

# Mostrar las tablas en Streamlit
for category, table in tables.items():
    category_title = ' '.join(word.capitalize() for word in category.split())
    st.write(f"### {category_title}")
    
    # Formatear las columnas excepto 'Año'
    formatted_table = table.copy()
    for col in formatted_table.columns:
        if col == 'Año':
            continue
        if category in percentage_categories:
            formatted_table[col] = formatted_table[col].apply(lambda x: f"{x*100:,.2f}%".replace(",", "X").replace(".", ",").replace("X", "."))
        else:
            formatted_table[col] = formatted_table[col].apply(lambda x: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    
    st.dataframe(formatted_table.reset_index(drop=True))


#%%

# Pobreza de ingresos
st.write(f"### Pobreza de ingresos para {comuna_seleccionada}")
casen_pobrezai = casen_csv.loc[casen_csv.Category == 'POBREZA DE INGRESOS']
casen_pobrezai_comuna = casen_pobrezai[casen_pobrezai['Comuna'] == filtro_comuna]
casen_pobrezai_comuna['Pobres'].fillna(casen_pobrezai_comuna['Pobres 2020'], inplace=True)
casen_pobrezai_comuna['Pobres'] = casen_pobrezai_comuna['Pobres'] / 100
fig_pobreza_ingresos = px.bar(
    casen_pobrezai_comuna,
    x='Año',
    y='Pobres',
    title=f"Pobreza de ingresos en {comuna_seleccionada}",
    labels={'Pobres': 'Porcentaje de Pobreza de Ingresos', 'Año': 'Año'},
    text=casen_pobrezai_comuna['Pobres'].apply(lambda x: '{0:1.2f}%'.format(x*100)),
    width=800,  # Ajustar el ancho del gráfico
    height=600  # Ajustar la altura del gráfico si es necesario
)
fig_pobreza_ingresos.update_layout(
    yaxis_tickformat=",.2%",
    yaxis_title='Porcentaje de Pobreza de Ingresos'
)
fig_pobreza_ingresos.update_traces(texttemplate='%{text}', textposition='outside')

st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
st.plotly_chart(fig_pobreza_ingresos, use_container_width=False)
st.markdown("</div>", unsafe_allow_html=True)


# display_centered_chart(fig_pobreza_ingresos)

st.write('_Fuente: Elaboración propia a partir de encuesta CASEN 2017, 2020 y 2022_')
st.write('_https://observatorio.ministeriodesarrollosocial.gob.cl/encuesta-casen_')

#%%
# Pobreza multidimensional
st.write(f"### Pobreza multidimensional para {comuna_seleccionada}")
casen_pobrezam = casen_csv.loc[casen_csv.Category == 'POBREZA MULTIDIMENSIONAL']
casen_pobrezam_comuna = casen_pobrezam[casen_pobrezam['Comuna'] == filtro_comuna]
casen_pobrezam_comuna['Pobres'] = casen_pobrezam_comuna['Pobres'] / 100
fig_pobreza_multidimensional = px.bar(
    casen_pobrezam_comuna,
    x='Año',
    y='Pobres',
    title=f"Pobreza multidimensional en {comuna_seleccionada}",
    labels={'Pobres': 'Porcentaje de Pobreza Multidimensional', 'Año': 'Año'},
    text=casen_pobrezam_comuna['Pobres'].apply(lambda x: '{0:1.2f}%'.format(x*100)),
    width=800,  # Ajustar el ancho del gráfico
    height=600  # Ajustar la altura del gráfico si es necesario
)
fig_pobreza_multidimensional.update_layout(
    yaxis_tickformat=",.2%",
    yaxis_title='Porcentaje de Pobreza Multidimensional'
)
fig_pobreza_multidimensional.update_traces(texttemplate='%{text}', textposition='outside')

st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
st.plotly_chart(fig_pobreza_multidimensional, use_container_width=False)
st.markdown("</div>", unsafe_allow_html=True)
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
    width=800,  # Ajustar el ancho del gráfico
    height=600  # Ajustar la altura del gráfico si es necesario
)
fig_ingresos.update_layout(
    yaxis_tickformat=".0f"
)

st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
st.plotly_chart(fig_ingresos, use_container_width=False)
st.markdown("</div>", unsafe_allow_html=True)
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

st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
st.plotly_chart(fig_participacion_laboral, use_container_width=False)
st.markdown("</div>", unsafe_allow_html=True)
st.write('_Fuente: Elaboración propia a partir de encuesta CASEN 2017, 2020 y 2022_')
st.write('_https://observatorio.ministeriodesarrollosocial.gob.cl/encuesta-casen_')
