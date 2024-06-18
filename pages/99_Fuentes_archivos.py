import streamlit as st
import streamlit_authenticator as stauth

if not st.session_state.authentication_status:
    st.info('Please Login from the Home page and try again.')
    st.stop()
    
st.set_page_config(page_title="Descarga de archivos", layout='wide', initial_sidebar_state='expanded')
logo_horizontal = 'img/horizontal_remolino_blue.png'
logo_icono = 'img/icon_remolino_blue.png'
st.logo(logo_horizontal, icon_image=logo_icono)
#%%
# TITULO INTRODUCCION
st.image('img/seremi-100-años.png', width=300)
st.write('# Región Metropolitana y sus comunas: Descarga de archivos')

# Definimos los datos de los enlaces en una lista de diccionarios
links = [
    {"Nombre": "Censo de Población y Vivienda", "Categoría": "CENSO", "URL": "https://www.ine.gob.cl/estadisticas/sociales/censos-de-poblacion-y-vivienda/censo-de-poblacion-y-vivienda"},
    {"Nombre": "Pobreza Comunal (CASEN)", "Categoría": "CASEN", "URL": "https://observatorio.ministeriodesarrollosocial.gob.cl/pobreza-comunal"},
    {"Nombre": "Defunciones por Causa", "Categoría": "Defunciones", "URL": "https://repositoriodeis.minsal.cl/DatosAbiertos/VITALES/DEFUNCIONES_FUENTE_DEIS_1990_2021_CIFRAS_OFICIALES.zip"}
]

# Convertimos la lista de diccionarios en un dataframe
import pandas as pd
df = pd.DataFrame(links)

# Mostramos la tabla en Streamlit
st.write('## Tabla de Enlaces de Descarga')
st.table(df)

# Opcional: Creamos enlaces clicables
st.write('## Enlaces de Descarga Clicables')
for link in links:
    st.markdown(f"- [{link['Nombre']}]({link['URL']}) ({link['Categoría']})")
