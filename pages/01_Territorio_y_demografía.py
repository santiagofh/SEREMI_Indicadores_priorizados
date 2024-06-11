#%%
import streamlit as st
import pandas as pd
import plotly.express as px
import geopandas as gpd
import folium
from streamlit_folium import folium_static
from datetime import datetime
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from shapely.geometry import Point

#%%
# Path o rutas para archivos
paths = {
    "censo17": 'data_clean/CENSO17_Poblacion_rm.csv',
    "geo": 'data_clean/Comunas_RM.geojson',
    "ine_proy": 'data_clean/INE_Proyecciones_RM.csv',
    "ine_proy_urb_rur": 'data_clean/INE_Proyecciones_urbano_rural_RM.csv',
    'casen_mideso':'data_clean/casen_17_22.csv',
}

#%%
# LECTURA DE ARCHIVOS
ine17 = pd.read_csv(paths["ine_proy"])
ine17_urb_rur = pd.read_csv(paths["ine_proy_urb_rur"])
censo17 = pd.read_csv(paths["censo17"])
gdf = gpd.read_file(paths["geo"])
casen = pd.read_csv(paths["casen_mideso"])

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
# INICIO DE LA PÁGINA
st.set_page_config(page_title="Territorio y demografía", layout='wide', initial_sidebar_state='expanded')

# Sidebar
st.sidebar.write("## Tablero Interactivo de Comunas: Indicadores priorizados")
comuna_seleccionada = st.sidebar.selectbox("Comuna:", lista_comunas, index=lista_comunas.index("Todas las comunas"))
current_year = datetime.now().year
select_year_int = st.sidebar.slider("Año:", min_value=2002, max_value=2035, value=current_year)
select_year = f'Poblacion {select_year_int}'

# TITULO INTRODUCCION
st.image('img/seremi-100-años.png', width=300)
st.write('# Región Metropolitana y sus comunas: Territorio y demografía')
st.write('A continuación, se presenta un análisis detallado de la distribución territorial y demográfica de las comunas de la Región Metropolitana, incluyendo proyecciones de población, densidad poblacional, y otros indicadores clave que permiten una visión integral del desarrollo y cambios en la población regional.')
def filtrar_comuna(df, column_name, comuna):
    return df.loc[df[column_name].str.upper() == comuna.upper()]

#%%
# Asegúrate de que las columnas de nombre de comuna sean strings
gdf['NOM_COMUNA'] = gdf['NOM_COMUNA'].astype(str)
ine17['Nombre Comuna'] = ine17['Nombre Comuna'].astype(str)
ine17_urb_rur['Nombre Comuna'] = ine17_urb_rur['Nombre Comuna'].astype(str)
censo17['NOMBRE COMUNA'] = censo17['NOMBRE COMUNA'].astype(str)
casen['Comuna'] = casen['Comuna'].astype(str)

# Filtra por comuna seleccionada
comuna_seleccionada_upper = comuna_seleccionada.upper()
gdf_comuna = gdf if comuna_seleccionada == 'Todas las comunas' else filtrar_comuna(gdf, 'NOM_COMUNA', comuna_seleccionada_upper)
ine17_comuna = filtrar_comuna(ine17, 'Nombre Comuna', comuna_seleccionada_upper)
censo17_comuna = filtrar_comuna(censo17, 'NOMBRE COMUNA', comuna_seleccionada_upper)
ine17_urb_rur_comuna = filtrar_comuna(ine17_urb_rur, 'Nombre Comuna', comuna_seleccionada_upper)
casen_comuna = filtrar_comuna(casen, 'Comuna', comuna_seleccionada_upper)

# Región
gdf_rm = gdf
ine17_rm = filtrar_comuna(ine17, 'Nombre Comuna', 'Todas las comunas')
censo17_rm = filtrar_comuna(censo17, 'NOMBRE COMUNA', 'Todas las comunas')
ine17_urb_rur_rm = filtrar_comuna(ine17_urb_rur, 'Nombre Comuna', 'Todas las comunas')

#%%
# Calculo de Casen REGION

#%%
# Calculo de pop y densidad
## Calculo de pop y densidad: Comuna
pop_proy_total = (ine17_comuna[select_year]).sum()
area_comuna = gdf_comuna.Superf_KM2.sum() if not gdf_comuna.empty else 0
densidad_pop = pop_proy_total / area_comuna if area_comuna > 0 else 0

## Calculo de pop y densidad: Región
pop_proy_total_rm = (ine17_rm[select_year]).sum()
area_rm = gdf_rm.Superf_KM2.sum() if not gdf_comuna.empty else 0
densidad_pop_rm = pop_proy_total_rm / area_rm if area_comuna > 0 else 0

#%%
# Load and prepare data
year_column = f'Poblacion {current_year}'
censo17_comuna_pop = censo17_comuna.loc[censo17_comuna.EDAD.isin(['Total Comuna', 'Total Región'])]
censo17_comuna_edad = censo17_comuna.loc[~censo17_comuna.EDAD.isin(['Total Comuna', 'Total Región'])]
pop_censada = censo17_comuna_pop['TOTAL POBLACIÓN EFECTIVAMENTE CENSADA'].values[0]
pop_h = censo17_comuna_pop['HOMBRES '].values[0]
pop_m = censo17_comuna_pop['MUJERES'].values[0]
pop_h_percentaje = (pop_h / pop_censada) * 100
pop_m_percentaje = (pop_m / pop_censada) * 100
pop_urb_percentage = (censo17_comuna_pop['TOTAL ÁREA URBANA'] / censo17_comuna_pop['TOTAL POBLACIÓN EFECTIVAMENTE CENSADA'] * 100).iloc[0]
pop_rur_percentage = (censo17_comuna_pop['TOTAL ÁREA RURAL'] / censo17_comuna_pop['TOTAL POBLACIÓN EFECTIVAMENTE CENSADA'] * 100).iloc[0]
pop_proy_h = ine17_comuna.loc[ine17_comuna['Sexo (1=Hombre 2=Mujer)'] == 1, select_year].sum()
pop_proy_m = ine17_comuna.loc[ine17_comuna['Sexo (1=Hombre 2=Mujer)'] == 2, select_year].sum()
pop_proy_h_percentaje = (pop_proy_h / pop_proy_total) * 100
pop_proy_m_percentaje = (pop_proy_m / pop_proy_total) * 100
pop_proy_h_urb_comuna = ine17_urb_rur_comuna.loc[(ine17_urb_rur_comuna['Sexo (1=Hombre 2=Mujer)'] == 1) & 
                                        (ine17_urb_rur_comuna['Area (1=Urbano 2=Rural)'] == 1), select_year].sum()
pop_proy_m_urb_comuna = ine17_urb_rur_comuna.loc[(ine17_urb_rur_comuna['Sexo (1=Hombre 2=Mujer)'] == 2) & 
                                        (ine17_urb_rur_comuna['Area (1=Urbano 2=Rural)'] == 1), select_year].sum()
pop_proy_h_rur_comuna = ine17_urb_rur_comuna.loc[(ine17_urb_rur_comuna['Sexo (1=Hombre 2=Mujer)'] == 1) & 
                                        (ine17_urb_rur_comuna['Area (1=Urbano 2=Rural)'] == 2), select_year].sum()
pop_proy_m_rur_comuna = ine17_urb_rur_comuna.loc[(ine17_urb_rur_comuna['Sexo (1=Hombre 2=Mujer)'] == 2) & 
                                        (ine17_urb_rur_comuna['Area (1=Urbano 2=Rural)'] == 2), select_year].sum()
pop_proy_h_urb_rm = ine17_urb_rur_rm.loc[(ine17_urb_rur_rm['Sexo (1=Hombre 2=Mujer)'] == 1) & 
                                        (ine17_urb_rur_rm['Area (1=Urbano 2=Rural)'] == 1), select_year].sum()
pop_proy_m_urb_rm = ine17_urb_rur_rm.loc[(ine17_urb_rur_rm['Sexo (1=Hombre 2=Mujer)'] == 2) & 
                                        (ine17_urb_rur_rm['Area (1=Urbano 2=Rural)'] == 1), select_year].sum()
pop_proy_h_rur_rm = ine17_urb_rur_rm.loc[(ine17_urb_rur_rm['Sexo (1=Hombre 2=Mujer)'] == 1) & 
                                        (ine17_urb_rur_rm['Area (1=Urbano 2=Rural)'] == 2), select_year].sum()
pop_proy_m_rur_rm = ine17_urb_rur_rm.loc[(ine17_urb_rur_rm['Sexo (1=Hombre 2=Mujer)'] == 2) & 
                                        (ine17_urb_rur_rm['Area (1=Urbano 2=Rural)'] == 2), select_year].sum()
pop_proy_urb_rm = pop_proy_h_urb_rm + pop_proy_m_urb_rm
pop_proy_rur_rm = pop_proy_h_rur_rm + pop_proy_m_rur_rm
pop_proy_urb_comuna = pop_proy_h_urb_comuna + pop_proy_m_urb_comuna
pop_proy_rur_comuna = pop_proy_h_rur_comuna + pop_proy_m_rur_comuna
porcentaje_0_14 = ine17_comuna.loc[ine17_comuna['Edad'] <= 14, select_year].sum() / pop_proy_total * 100
porcentaje_15_64 = ine17_comuna.loc[(ine17_comuna['Edad'] >= 15) & (ine17_comuna['Edad'] <= 64), select_year].sum() / pop_proy_total * 100
porcentaje_65_mas = ine17_comuna.loc[ine17_comuna['Edad'] >= 65, select_year].sum() / pop_proy_total * 100
indice_masculinidad = (pop_proy_h / pop_proy_m) * 100
area_comuna = gdf_comuna.Superf_KM2.sum() if not gdf_comuna.empty else 0
densidad_pop_comuna = pop_proy_total / area_comuna if area_comuna > 0 else 0

# REGIÓN
censo17_rm_pop = censo17_rm.loc[censo17_rm.EDAD.isin(['Total Comuna', 'Total Región'])]
censo17_rm_edad = censo17_rm.loc[~censo17_rm.EDAD.isin(['Total Comuna', 'Total Región'])]
pop_censada_rm = censo17_rm_pop['TOTAL POBLACIÓN EFECTIVAMENTE CENSADA'].values[0]
pop_h_rm = censo17_rm_pop['HOMBRES '].values[0]
pop_m_rm = censo17_rm_pop['MUJERES'].values[0]
pop_h_percentaje_rm = (pop_h_rm / pop_censada_rm) * 100
pop_m_percentaje_rm = (pop_m_rm / pop_censada_rm) * 100
pop_urb_percentage = (censo17_rm_pop['TOTAL ÁREA URBANA'] / censo17_rm_pop['TOTAL POBLACIÓN EFECTIVAMENTE CENSADA'] * 100).iloc[0]
pop_rur_percentage = (censo17_rm_pop['TOTAL ÁREA RURAL'] / censo17_rm_pop['TOTAL POBLACIÓN EFECTIVAMENTE CENSADA'] * 100).iloc[0]

pop_proy_h_rm = ine17_rm.loc[ine17_rm['Sexo (1=Hombre 2=Mujer)'] == 1, select_year].sum()
pop_proy_m_rm = ine17_rm.loc[ine17_rm['Sexo (1=Hombre 2=Mujer)'] == 2, select_year].sum()
pop_proy_h_percentaje_rm = (pop_proy_h_rm / pop_proy_total_rm) * 100
pop_proy_m_percentaje_rm = (pop_proy_m_rm / pop_proy_total_rm) * 100

area_rm = gdf_rm.Superf_KM2.sum() if not gdf_rm.empty else 0
densidad_pop_rm = pop_proy_total / area_rm if area_rm > 0 else 0

pop_proy_percentaje_comuna_rm = (pop_proy_total / pop_proy_total_rm) * 100

pop_0_14 = ine17_comuna.loc[ine17_comuna['Edad'] <= 14, select_year].sum()
pop_15_64 = ine17_comuna.loc[(ine17_comuna['Edad'] >= 15) & (ine17_comuna['Edad'] <= 64), select_year].sum()
pop_65_mas = ine17_comuna.loc[ine17_comuna['Edad'] >= 65, select_year].sum()

indice_dependencia = ((pop_0_14 + pop_65_mas) / pop_15_64) * 100
indice_renovacion_vejez = (pop_65_mas / pop_0_14) * 100

# Calcula la Tasa Bruta de Natalidad 2020
poblacion_2020 = ine17_comuna['Poblacion 2020'].sum()

# Calcula la Tasa Específica de Fecundidad por Edad
def age_group(age):
    if age >= 50:
        return "50 O MAS AÑOS"
    elif age >= 45:
        return "45 A 49 AÑOS"
    elif age >= 40:
        return "40 A 44 AÑOS"
    elif age >= 35:
        return "35 A 39 AÑOS"
    elif age >= 30:
        return "30 A 34 AÑOS"
    elif age >= 25:
        return "25 A 29 AÑOS"
    elif age >= 20:
        return "20 A 24 AÑOS"
    elif age >= 15:
        return "15 A 19 AÑOS"
    else:
        return "MENORES 15 AÑOS"

poblacion_2020_grupo_etario = ine17_comuna[ine17_comuna['Sexo (1=Hombre 2=Mujer)'] == 2].groupby('Edad')['Poblacion 2020'].sum().reset_index()
poblacion_2020_grupo_etario['GRUPO_ETARIO_MADRE'] = poblacion_2020_grupo_etario['Edad'].apply(age_group)
poblacion_2020_grupo_etario = poblacion_2020_grupo_etario.groupby('GRUPO_ETARIO_MADRE')['Poblacion 2020'].sum().reset_index()

# Población nacida fuera de Chile y Pueblos originarios del 2022
poblacion_total_2022 = casen[casen['Año'] == 2022]['Población nacida fuera de Chile'].sum()

# Filtrar datos del 2022

casen_migrantes = casen.loc[casen['Category'] == 'MIGRANTES']
rename_migrantes = {
    'Año': 'Año', 
    'Comuna': 'Comuna', 
    'Ponlación nacida en Chile': 'Población nacida en Chile', 
    'Población nacida fuera de Chile': 'Población nacida fuera de Chile'
}
casen_migrantes.rename(columns=rename_migrantes, inplace=True)

casen_migrantes = casen_migrantes[['Año', 'Comuna', 'Población nacida en Chile', 'Población nacida fuera de Chile']]

if comuna_seleccionada == "Todas las comunas":
    casen_migrantes_comuna = casen_migrantes[casen_migrantes['Comuna'] == 'Región Metropolitana']
else:
    casen_migrantes_comuna = casen_migrantes[casen_migrantes['Comuna'].str.upper() == comuna_seleccionada_upper]

casen_migrantes_2022 = casen_migrantes_comuna[casen_migrantes_comuna['Año'] == 2022]

casen_etnias = casen.loc[casen['Category'] == 'ETNIAS']
casen_etnias = casen_etnias.dropna(axis=1)

if comuna_seleccionada == "Todas las comunas":
    casen_etnias_comuna = casen_etnias[casen_etnias['Comuna'] == 'Región Metropolitana']
else:
    casen_etnias_comuna = casen_etnias[casen_etnias['Comuna'].str.upper() == comuna_seleccionada_upper]

casen_etnias_comuna = casen_etnias_comuna.groupby('Año').agg(
    {'Pertenece a algún pueblo originario': 'sum', 'No pertenece a ningún pueblo originario': 'sum'}
).reset_index()


casen_etnias_2022 = casen_etnias_comuna[casen_etnias_comuna['Año'] == 2022]

# Calcular los porcentajes
poblacion_nacida_fuera_de_chile_2022 = casen_migrantes_2022['Población nacida fuera de Chile'].values[0]
poblacion_nacida_fuera_de_chile_2022_percent = (poblacion_nacida_fuera_de_chile_2022)

poblacion_pertenece_pueblos_2022 = casen_etnias_2022['Pertenece a algún pueblo originario'].values[0]
poblacion_pertenece_pueblos_2022_percent = (poblacion_pertenece_pueblos_2022)


# Formateo de valores
formatted_values = {
    "pop_censada": f"{int(pop_censada):,}".replace(',', '.'),
    "pop_h": f"{int(pop_h):,}".replace(',', '.'),
    "pop_m": f"{int(pop_m):,}".replace(',', '.'),
    "pop_h_percentaje": "{:.2f}%".format(pop_h_percentaje).replace('.', ','),
    "pop_m_percentaje": "{:.2f}%".format(pop_m_percentaje).replace('.', ','),
    "pop_urb_percentage": f"{pop_urb_percentage:.2f}%".replace('.', ','),
    "pop_rur_percentage": f"{pop_rur_percentage:.2f}%".replace('.', ','),
    "pop_proy_total": f"{int(pop_proy_total):,}".replace(',', '.'),
    "pop_proy_h": f"{int(pop_proy_h):,}".replace(',', '.'),
    "pop_proy_m": f"{int(pop_proy_m):,}".replace(',', '.'),
    'pop_proy_h_percentaje': "{:.2f}%".format(pop_proy_h_percentaje).replace('.', ','),
    'pop_proy_m_percentaje': "{:.2f}%".format(pop_proy_m_percentaje).replace('.', ','),
    "area_comuna": f"{int(area_comuna):,} km²".replace(',', '.'),
    "densidad_pop_comuna": "{:.2f} hab/km²".format(densidad_pop_comuna).replace('.', ','),
    "area_rm": f"{int(area_rm):,} km²".replace(',', '.'),
    "densidad_pop_rm": "{:.2f} hab/km²".format(densidad_pop_rm).replace('.', ','),
    "pop_proy_total_rm": f"{int(pop_proy_total_rm):,}".replace(',', '.'),
    "pop_percentaje_comuna_rm": "{:.2f}%".format(pop_proy_percentaje_comuna_rm).replace('.', ','),
    "porcentaje_0_14": "{:.2f}%".format(porcentaje_0_14).replace('.', ','),
    "porcentaje_15_64": "{:.2f}%".format(porcentaje_15_64).replace('.', ','),
    "porcentaje_65_mas": "{:.2f}%".format(porcentaje_65_mas).replace('.', ','),
    "indice_masculinidad": "{:.2f}".format(indice_masculinidad).replace('.', ','),
    "pop_proy_urb_comuna": f"{int(pop_proy_urb_comuna):,}".replace(',', '.'),
    "pop_proy_rur_comuna": f"{int(pop_proy_rur_comuna):,}".replace(',', '.'),
    "indice_dependencia": "{:.2f}".format(indice_dependencia).replace('.', ','),
    "indice_renovacion_vejez": "{:.2f}".format(indice_renovacion_vejez).replace('.', ','),
    # "tasa_bruta_natalidad_2020": "{:.2f}".format(tasa_bruta_natalidad_2020).replace('.', ','),
    # 'Tasa Fecundidad': (fecundidad_2020['Nacimientos'] / fecundidad_2020['Poblacion 2020']) * 1000,
    # "tasa_bruta_reproduccion_2020": "{:.2f}".format(tasa_bruta_reproduccion_2020).replace('.', ','),
    "poblacion_nacida_fuera_de_chile_2022" : f"{poblacion_nacida_fuera_de_chile_2022_percent:.2f}%".replace('.', ','),
    "poblacion_pertenece_pueblos_2022" : f"{poblacion_pertenece_pueblos_2022_percent:.2f}%".replace('.', ',')


}

#%%
# Crear el DataFrame con los datos formateados
data = {
    "Indicador": [
        "Población proyectada año 2024",
        "Población proyectada año 2024 región",
        "Porcentaje población de comuna sobre el total de la región",
        "Superficie",
        "Densidad poblacional 2024",
        "Porcentaje Hombres 2024",
        "Porcentaje de mujeres 2024",
        "Porcentaje de personas de 0-14 años. 2024",
        "Porcentaje de personas de 15-64 años. 2024",
        "Porcentaje de personas de 65 años y más. 2024",
        "Índice De Masculinidad 2024",
        "Población urbana (proyección 2024)",
        "Población rural (proyección 2024)",
        "Índice De Dependencia 2024",
        "Índice De Renovación O Vejez 2024",
        "Tasa bruta de natalidad 2020 (por 1.000 hab.)",
        "Tasa específica de Fecundidad por edad",
        "Tasa bruta de reproducción",
        "Indice de desarrollo humano (IDH)",
        "% Pueblos Indigenas/Originarios",
        "Personas nacidas en el extranjero"
    ],
    "Fuente de dato": [
        "INE, CENSO 2017 (proyección)", 
        "INE, CENSO 2017 (proyección)", 
        "INE, CENSO 2017 (proyección)",
        "base de datos Epi MINSAL, en base a CENSO 2017",
        "base de datos Epi MINSAL, en base a CENSO 2017",
        "base de datos Epi MINSAL, en base a CENSO 2017",
        "base de datos Epi MINSAL, en base a CENSO 2017",
        "INE, CENSO 2017 (proyección)",
        "INE, CENSO 2017 (proyección)",
        "INE, CENSO 2017 (proyección)",
        "Estimaciones y proyecciones 2002-2035. Instituto Nacional de Estadísticas (INE).",
        "Estimaciones y proyecciones 2002-2035. Instituto Nacional de Estadísticas (INE).",
        "Estimaciones y proyecciones 2002-2035. Instituto Nacional de Estadísticas (INE).",
        "Estimaciones y proyecciones 2002-2035. Instituto Nacional de Estadísticas (INE).",
        "Estimaciones y proyecciones 2002-2035. Instituto Nacional de Estadísticas (INE).",
        "Tablero de estadísticas de nacimientos y natalidad. DEIS",
        "Tablero de estadísticas de nacimientos y natalidad. DEIS",
        "Tablero de estadísticas de nacimientos y natalidad. DEIS",
        "Informe universidad Autonoma",
        "CASEN 2022",
        "CASEN 2022"
    ],
    "Valor": [
        formatted_values["pop_proy_total"],
        formatted_values["pop_proy_total_rm"],
        formatted_values["pop_percentaje_comuna_rm"],
        formatted_values["area_comuna"],
        formatted_values["densidad_pop_comuna"],
        formatted_values["pop_h_percentaje"],
        formatted_values["pop_m_percentaje"],
        formatted_values["porcentaje_0_14"],
        formatted_values["porcentaje_15_64"],
        formatted_values["porcentaje_65_mas"],
        formatted_values["indice_masculinidad"],
        formatted_values["pop_proy_urb_comuna"],
        formatted_values["pop_proy_rur_comuna"],
        formatted_values["indice_dependencia"],
        formatted_values["indice_renovacion_vejez"],
        "",
        "",
        "",
        "",
        formatted_values["poblacion_nacida_fuera_de_chile_2022"],
        formatted_values["poblacion_pertenece_pueblos_2022"]
    ],
    "Enlace": [
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "https://informesdeis.minsal.cl/SASVisualAnalytics/?reportUri=%2Freports%2Freports%2Fa39b6235-6172-4b09-a8b1-ab5f87c72ea0&sectionIndex=1&sso_guest=true&sas-welcome=false",
        "https://informesdeis.minsal.cl/SASVisualAnalytics/?reportUri=%2Freports%2Freports%2Fa39b6235-6172-4b09-a8b1-ab5f87c72ea0&sectionIndex=1&sso_guest=true&sas-welcome=false",
        "https://informesdeis.minsal.cl/SASVisualAnalytics/?reportUri=%2Freports%2Freports%2Fa39b6235-6172-4b09-a8b1-ab5f87c72ea0&sectionIndex=1&sso_guest=true&sas-welcome=false",
        "https://informesdeis.minsal.cl/SASVisualAnalytics/?reportUri=%2Freports%2Freports%2Fa39b6235-6172-4b09-a8b1-ab5f87c72ea0&sectionIndex=1&sso_guest=true&sas-welcome=false",
        "https://informesdeis.minsal.cl/SASVisualAnalytics/?reportUri=%2Freports%2Freports%2Fa39b6235-6172-4b09-a8b1-ab5f87c72ea0&sectionIndex=1&sso_guest=true&sas-welcome=false",
        "https://repositorio.uautonoma.cl/bitstream/handle/20.500.12728/6742/V11_digital_final.pdf?sequence=1&isAllowed=y",
        "",
        ""
    ]
}

df_indicadores = pd.DataFrame(data)

# Configuración de columnas
columns_config = {
    "Indicador": st.column_config.TextColumn("Indicador"),
    "Fuente de dato": st.column_config.TextColumn("Fuente de dato"),
    "Valor": st.column_config.TextColumn("Valor"),
    "Enlace": st.column_config.LinkColumn("Enlace", width=300)
}

# Mostrar el DataFrame en Streamlit con configuración de columnas
st.dataframe(df_indicadores, column_config=columns_config)



#%%
# Indicadores territoriales y de población
st.markdown('## Indicadores de población')
cols = st.columns(5)

#%%
# Población censada y proyectada
cols[0].metric("Población efectivamente censada 2017", formatted_values["pop_censada"])
cols[1].metric("Total hombres (censo 2017)", formatted_values["pop_h"])
cols[2].metric("Total mujeres (censo 2017)", formatted_values["pop_m"])
cols[3].metric("Porcentaje de hombres (censo 2017)", formatted_values["pop_h_percentaje"])
cols[4].metric("Porcentaje de mujeres (censo 2017)", formatted_values["pop_m_percentaje"])

cols[0].metric(f"Población proyectada ({select_year})", formatted_values["pop_proy_total"])
cols[1].metric(f"Total hombres ({select_year})", formatted_values["pop_proy_h"])
cols[2].metric(f"Total mujeres ({select_year})", formatted_values["pop_proy_m"])
cols[3].metric(f"Porcentaje de hombres ({select_year})", formatted_values["pop_proy_h_percentaje"])
cols[4].metric(f"Porcentaje de mujeres ({select_year})", formatted_values["pop_proy_m_percentaje"])

st.write('_Fuente: Elaboración propia a partir de INE 2017_ _(https://www.ine.gob.cl/estadisticas/sociales/demografia-y-vitales/proyecciones-de-poblacion)_')

#%%
# Mapa
st.write(f"## Visualizar mapa de {comuna_seleccionada}")

def get_zoom_level(area):
    scaled_area = area * 1000 
    if scaled_area > 100:
        return 8
    elif scaled_area > 50:
        return 10
    elif scaled_area > 20:
        return 11
    elif scaled_area > 10:
        return 11
    elif scaled_area > 5:
        return 12
    else:
        return 13

if not gdf_comuna.empty:
    area = gdf_comuna.geometry.area.sum()
    centroid = gdf_comuna.geometry.centroid.iloc[0]
    zoom_start = get_zoom_level(area)
    m = folium.Map(location=[centroid.y, centroid.x], zoom_start=zoom_start)
    folium.GeoJson(gdf_comuna, name='geojson').add_to(m)
    folium.LayerControl().add_to(m)
    folium_static(m)
else:
    st.write("No se encontró la comuna seleccionada en los datos geográficos.")

#%%
# Datos adicionales de la comuna
cols = st.columns(4)
cols[0].metric("Área total de la comuna (población proyectada 2024)", formatted_values["area_comuna"])
cols[1].metric("Densidad poblacional de la comuna (población proyectada)", formatted_values["densidad_pop_comuna"])
cols[0].metric("Porcentaje área urbana (censo 2017)", formatted_values["pop_urb_percentage"])
cols[1].metric("Porcentaje área rural (censo 2017)", formatted_values["pop_rur_percentage"])

st.write('_Fuente: Elaboración propia a partir de datos geográficos nacionales (https://www.ine.gob.cl/herramientas/portal-de-mapas/geodatos-abiertos)_')

#%%
# Poblacion proyectada
st.write('## Poblacion proyectada')

population_data = ine17_comuna[['Nombre Comuna', 'Sexo (1=Hombre 2=Mujer)'] + [f'Poblacion {year}' for year in range(2002, 2036)]]
population_data_melted = population_data.melt(id_vars=['Nombre Comuna', 'Sexo (1=Hombre 2=Mujer)'], var_name='Año', value_name='Población')
population_data_melted['Año'] = population_data_melted['Año'].str.extract('(\d+)').astype(int)
total_population_by_gender = population_data_melted.groupby(['Año', 'Sexo (1=Hombre 2=Mujer)'])['Población'].sum().reset_index()
total_population_by_gender.sort_values(by=['Año', 'Sexo (1=Hombre 2=Mujer)'], inplace=True)
total_population_by_gender['Sexo (1=Hombre 2=Mujer)'] = total_population_by_gender['Sexo (1=Hombre 2=Mujer)'].map({1: 'Hombre', 2: 'Mujer'})

fig = px.line(
    total_population_by_gender,
    x='Año',
    y='Población',
    color='Sexo (1=Hombre 2=Mujer)',
    title='Total población proyectada ' + comuna_seleccionada,
    labels={'Sexo (1=Hombre 2=Mujer)': 'Sexo', 'Año': 'Año', 'Población': 'Población'}
)
fig.add_vline(x=select_year_int, line_width=2, line_dash="dash", line_color="red")
fig.add_annotation(
    x=select_year_int,
    xref="x",
    yref="paper",
    text=f"Año: {select_year_int}",
    showarrow=False,
    font=dict(color="red", size=15)
)
fig.update_layout(
    yaxis_title='Total población',
    xaxis_title='Año',
    legend_title='Sexo',
)
st.plotly_chart(fig)
st.write('_Fuente: Elaboración propia a partir de INE 2017_ _(https://www.ine.gob.cl/estadisticas/sociales/demografia-y-vitales/proyecciones-de-poblacion)_')

#%%
# Piramide poblacional
st.write(f'## Piramide poblacional para {comuna_seleccionada}')

ine17_comuna['Sexo'] = ine17_comuna['Sexo (1=Hombre 2=Mujer)'].map({1: 'Hombres', 2: 'Mujeres'})
years = [f'Poblacion {year}' for year in range(2002, 2036)]
data_melted = ine17_comuna.melt(id_vars=['Edad', 'Sexo'], value_vars=years, var_name='Year', value_name='Population')
data_melted['Year'] = data_melted['Year'].str.extract('(\d+)').astype(int)
grouped_data = data_melted.groupby(['Year', 'Sexo', 'Edad']).agg({'Population': 'sum'}).reset_index()

def age_group(age):
    if age >= 80:
        return "80 y más"
    elif age >= 75:
        return "75 a 79"
    elif age >= 70:
        return "70 a 74"
    elif age >= 65:
        return "65 a 69"
    elif age >= 60:
        return "60 a 64"
    elif age >= 55:
        return "55 a 59"
    elif age >= 50:
        return "50 a 54"
    elif age >= 45:
        return "45 a 49"
    elif age >= 40:
        return "40 a 44"
    elif age >= 35:
        return "35 a 39"
    elif age >= 30:
        return "30 a 34"
    elif age >= 25:
        return "25 a 29"
    elif age >= 20:
        return "20 a 24"
    elif age >= 15:
        return "15 a 19"
    elif age >= 10:
        return "10 a 14"
    elif age >= 5:
        return "05 a 09"
    else:
        return "0 a 04"

grouped_data['Age Group'] = grouped_data['Edad'].apply(age_group)
grouped_data = grouped_data.groupby(['Year', 'Sexo', 'Age Group']).agg({'Population': 'sum'}).reset_index()
fig = make_subplots(rows=1, cols=2, shared_yaxes=True, subplot_titles=['Hombres', 'Mujeres'], horizontal_spacing=0.02, x_title='Población')

for year in range(2002, 2036):
    for sexo in ['Hombres', 'Mujeres']:
        subset = grouped_data[(grouped_data['Year'] == year) & (grouped_data['Sexo'] == sexo)]
        subset = subset.sort_values(by='Age Group')
        fig.add_trace(
            go.Bar(x=-subset['Population'] if sexo == 'Hombres' else subset['Population'], y=subset['Age Group'],
                   orientation='h', name=sexo, visible=(year == datetime.now().year)),
            1, 1 if sexo == 'Hombres' else 2
        )

steps = []
for i, year in enumerate(range(2002, 2036)):
    step = dict(
        method="update",
        args=[{"visible": [False] * len(fig.data)}],
        label=str(year)
    )
    for j in range(len(fig.data)):
        step["args"][0]["visible"][2 * i + j % 2] = True
    steps.append(step)

year_index = select_year_int - 2002

sliders = [dict(
    active=year_index,
    currentvalue={"prefix": "Año: "},
    pad={"t": 50},
    steps=steps
)]

max_population = grouped_data['Population'].max()

fig.update_layout(
    sliders=sliders,
    title=f"Pirámide Poblacional de {comuna_seleccionada} por Año",
    xaxis_title="Población",
    yaxis_title="Rango Etario",
    showlegend=False,
    xaxis=dict(range=[-max_population, 0]),
    xaxis2=dict(range=[0, max_population])
)

st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
st.plotly_chart(fig, use_container_width=False)
st.markdown("</div>", unsafe_allow_html=True)
st.write('_Fuente: Elaboración propia a partir de INE 2017_ _(https://www.ine.gob.cl/estadisticas/sociales/demografia-y-vitales/proyecciones-de-poblacion)_')


#%%
# Población nacida fuera de Chile
st.write('## Porcentaje de población nacida fuera de Chile')

casen_migrantes_comuna['Total'] = casen_migrantes_comuna['Población nacida en Chile'] + casen_migrantes_comuna['Población nacida fuera de Chile']
casen_migrantes_comuna['% Nacida en Chile'] = (casen_migrantes_comuna['Población nacida en Chile'] / casen_migrantes_comuna['Total']) * 100
casen_migrantes_comuna['% Nacida fuera de Chile'] = (casen_migrantes_comuna['Población nacida fuera de Chile'] / casen_migrantes_comuna['Total']) * 100

df_melted = casen_migrantes_comuna.melt(id_vars=['Año', 'Comuna'], value_vars=['% Nacida en Chile', '% Nacida fuera de Chile'],
                                         var_name='Origen', value_name='Porcentaje')

fig_migrantes = px.bar(
    df_melted,
    x='Año',
    y='Porcentaje',
    color='Origen',
    text=df_melted['Porcentaje'].apply(lambda x: '{0:1.2f}%'.format(x)),
    title=f'Porcentaje de población nacida fuera de Chile en {comuna_seleccionada}',
    labels={'Porcentaje': 'Porcentaje', 'Origen': 'Origen'},
    width=800,  # Ajustar el ancho del gráfico
    height=600  # Ajustar la altura del gráfico si es necesario
)

fig_migrantes.update_traces(texttemplate='%{text}', textposition='outside')
fig_migrantes.update_yaxes(range=[0, 110],ticksuffix="%")

# Centrar el gráfico en Streamlit
st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
st.plotly_chart(fig_migrantes, use_container_width=False)
st.markdown("</div>", unsafe_allow_html=True)
st.write('_Fuente: Elaboración propia a partir de encuesta CASEN 2017, 2020 y 2022_')
st.write('_https://observatorio.ministeriodesarrollosocial.gob.cl/encuesta-casen_')

# %%
st.write('## Porcentaje de población perteneciente a una etnia')

casen_etnias_comuna['Total'] = casen_etnias_comuna['Pertenece a algún pueblo originario'] + casen_etnias_comuna['No pertenece a ningún pueblo originario']
casen_etnias_comuna['% Pertenece a algún pueblo originario'] = (casen_etnias_comuna['Pertenece a algún pueblo originario'] / casen_etnias_comuna['Total']) * 100
casen_etnias_comuna['% No pertenece a ningún pueblo originario'] = (casen_etnias_comuna['No pertenece a ningún pueblo originario'] / casen_etnias_comuna['Total']) * 100

fig_etnias = px.bar(
    casen_etnias_comuna, 
    x='Año', 
    y=[ '% No pertenece a ningún pueblo originario','% Pertenece a algún pueblo originario'], 
    title=f'Porcentaje de población perteneciente a una etnia en {comuna_seleccionada}',
    labels={'value': 'Porcentaje', 'variable': 'Origen'},
    text_auto=True
)
fig_etnias.update_layout(yaxis=dict(range=[0, 110]))

st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
st.plotly_chart(fig_etnias, use_container_width=False)
st.markdown("</div>", unsafe_allow_html=True)

st.write('_Fuente: Elaboración propia a partir de encusta CASEN 2017, 2020 y 2022_')
st.write('_https://observatorio.ministeriodesarrollosocial.gob.cl/encuesta-casen_')

#%%
import streamlit as st
url = "https://informesdeis.minsal.cl/SASVisualAnalytics/?reportUri=%2Freports%2Freports%2Fa39b6235-6172-4b09-a8b1-ab5f87c72ea0&sectionIndex=1&sso_guest=true&sas-welcome=false"
st.title("Datos de nacimiento")
st.write("Haz clic en el siguiente enlace para abrir la página en una nueva pestaña:")
st.markdown(f"[Abrir página web]({url})")
