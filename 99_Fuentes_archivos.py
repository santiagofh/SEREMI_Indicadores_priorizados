import streamlit as st
import streamlit_authenticator as stauth
st.write('# Región Metropolitana y sus comunas: Descarga de archivos')
links = [
    {"Nombre": "Censo de Población y Vivienda", "Categoría": "CENSO", "URL": "https://www.ine.gob.cl/estadisticas/sociales/censos-de-poblacion-y-vivienda/censo-de-poblacion-y-vivienda"},
    {"Nombre": "Pobreza Comunal (CASEN)", "Categoría": "CASEN", "URL": "https://observatorio.ministeriodesarrollosocial.gob.cl/pobreza-comunal"},
    {"Nombre": "Defunciones por Causa", "Categoría": "Defunciones", "URL": "https://repositoriodeis.minsal.cl/DatosAbiertos/VITALES/DEFUNCIONES_FUENTE_DEIS_1990_2021_CIFRAS_OFICIALES.zip"}
]
import pandas as pd
df = pd.DataFrame(links)
st.write('## Tabla de Enlaces de Descarga')
st.table(df)