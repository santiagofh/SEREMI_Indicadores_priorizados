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
import streamlit_authenticator as stauth
import requests
from bs4 import BeautifulSoup

#%%

st.write('# Región Metropolitana y sus comunas: Ambiental')
st.write('Este tablero interactivo presenta indicadores ambientales priorizados de la Región Metropolitana de Santiago, proporcionando una visión detallada sobre las emisiones, el consumo de agua, y otros aspectos relevantes para la gestión ambiental y la salud pública.')
#%%
def obtener_datos_calidad_aire():
    url = "https://airechile.mma.gob.cl/comunas/santiago"
    try:
        response = requests.get(url, verify=False)  
        soup = BeautifulSoup(response.content, 'html.parser')
        try:
            panel = soup.find('div', {'class': 'panel panel-medidas'})
            if panel:
                contenido_panel = panel.prettify()
            else:
                contenido_panel = "No se pudo encontrar el panel de medidas."
        except Exception as e:
            contenido_panel = f"Error al obtener el panel: {str(e)}"

        calidad_aire = {
            'contenido_panel': contenido_panel,
        }

    except requests.exceptions.RequestException as e:
        calidad_aire = {
            'contenido_panel': f"Error al realizar la solicitud: {str(e)}"
        }

    return calidad_aire

st.title("Calidad del Aire en Santiago")

st.write("""
Este dashboard proporciona información en tiempo real sobre la calidad del aire en Santiago,
incluyendo estados de emergencia y preemergencia. Los datos son obtenidos del sitio oficial Aire Chile.
""")

st.write(f"### {datetime.now().strftime('%d/%m/%Y')}")
datos_calidad_aire = obtener_datos_calidad_aire()

st.markdown("""
    <style>
    .panel-heading {
        background-color: #f57223;
        padding: 15px;
        border-radius: 5px 5px 0 0;
        font-size: 1.5em;
        color: white;
    }
    .panel-body {
        background-color: #f9f9f9;
        padding: 20px;
        border: 1px solid #ddd;
        border-top: none;
        border-radius: 0 0 5px 5px;
        margin-top: 0;
    }
    .list-block {
        margin: 0;
        padding: 0;
        list-style: none;
    }
    .list-block li {
        display: table;
        width: 100%;
        margin-bottom: 10px;
        padding: 10px 0;
        border-bottom: 1px solid #eee;
    }
    .list-block li img {
        display: table-cell;
        vertical-align: top;
        width: 40px;
        height: 40px;
        margin-right: 20px;
    }
    .list-block li p {
        display: table-cell;
        vertical-align: top;
        margin: 0;
        line-height: 1.5;
    }
    </style>
    """, unsafe_allow_html=True)

st.subheader("Información en tiempo real sobre la calidad del aire en Santiago")
st.markdown(datos_calidad_aire['contenido_panel'], unsafe_allow_html=True)
st.markdown("[Más información sobre la calidad del aire y detalles de la alerta](https://airechile.mma.gob.cl/comunas/santiago)")
st.write("_Fuente: Ministerio de medio ambiente https://airechile.mma.gob.cl/comunas/santiago_")
#%%
st.markdown("""
    <iframe width="100%" height="600" src="https://sinca.mma.gob.cl/mapainteractivo/index.html?q=1719931520&z=0" frameborder="0" allowfullscreen></iframe>
    """, unsafe_allow_html=True)

st.write("_Fuente: Mapa desarrollado por el Ministerio de medio ambiente https://sinca.mma.gob.cl/_")
#%%
st.write('## Emisiones de dióxido de carbono para fuentes puntuales')
st.write('Las emisiones de dióxido de carbono (CO₂) son un indicador clave para evaluar la contribución de diferentes fuentes a la contaminación del aire y al cambio climático. Este gráfico muestra las emisiones de CO₂ por fuentes puntuales de las regiones.')

st.write('### Emisiones de dióxido de carbono CO2, por tipo de fuente segregadas por región, 2019.')
infogram_url0 = "https://infogram.com/1pgd26w1w7ekpgs9p9wg021d0ltwl9rrl3q"
st.components.v1.iframe(infogram_url0,  height=600, scrolling=True)
st.write('fuente: https://retc.mma.gob.cl/indicadores/emisiones-al-aire/')

st.write('### Emisiones de dióxido de carbono (CO2) desagregadas por región para fuentes puntuales por rubro, 2019')
infogram_url1 = "https://infogram.com/1prdpmyp12vd2xugvp1n53lre1smzy7prrw"
st.components.v1.iframe(infogram_url1,  height=600, scrolling=True)
st.write('fuente: https://retc.mma.gob.cl/indicadores/emisiones-al-aire/')

st.write('## Emisiones de material particulado respirable fino para fuentes puntuales')
st.write('El material particulado respirable fino es una de las principales preocupaciones ambientales debido a sus efectos adversos en la salud humana.')

st.write('### Emisiones de material particulado respirable (MP10) desagregadas por región para fuentes puntuales por rubro, 2019.')
infogram_url2 = "https://infogram.com/1pyxvngg60xnvwt3m51k5g1wv5tyw2xll29"
st.components.v1.iframe(infogram_url2,  height=600, scrolling=True)
st.write('fuente: https://retc.mma.gob.cl/indicadores/emisiones-al-aire/')

st.write('### Emisiones de material particulado respirable fino (MP2,5) desagregadas por región para fuentes puntuales por rubro, 2019.')
infogram_url4 = 'https://infogram.com/1p0lpr29w29en1fex16ylp3wr9fnd9r0l1l'
st.components.v1.iframe(infogram_url4,  height=600, scrolling=True)
st.write('fuente: https://retc.mma.gob.cl/indicadores/emisiones-al-aire/')

import streamlit as st

st.write('## Mapa de Declaraciones de Establecimientos Industriales y/o Municipales 2019')
st.write("""
Contiene el resumen de las declaraciones de los Establecimientos industriales y/o municipales registrados en Ventanilla Única durante el año 2019, de los siguientes sistemas:

- Sistema de Declaración y Seguimiento de Residuos Peligrosos (SIDREP)
- Declaración de Emisiones Atmosféricas (Formulario F138)
- Sistema Nacional de Declaración de Residuos (SINADER)
""")

map_url = "https://umap.openstreetmap.fr/es/map/declaracion-jurada-anual-2018-toneladas_517111?scaleControl=true&miniMap=true&scrollWheelZoom=true&zoomControl=true&allowEdit=false&moreControl=false&searchControl=true&tilelayersControl=true&embedControl=null&datalayersControl=null&onLoadPanel=undefined&captionBar=false&fullscreenControl=true#11/-33.4664/-70.7870"
st.components.v1.iframe(map_url, height=600 ,scrolling=True)
if st.checkbox('Mostrar/ocultar diccionario de datos'):
    st.write('''
        ### Diccionario de datos:

        - **Región**: Región donde se localiza el Establecimiento
        - **Comuna**: Comuna donde se localiza el Establecimiento
        - **Latitud**: Latitud del establecimiento
        - **Longitud**: Longitud del establecimiento
        - **Empresa**: Razón Social del Establecimiento
        - **Establecim**: Nombre del Establecimiento
        - **Rubro**: Rubro del Establecimiento
        - **ID_VU**: Número Identificador del Establecimiento en RETC
        - **CO2**: Emisiones de Dióxido de carbono (CO2) del Establecimiento durante el año 2019 (medida en tonelada/año)
        - **MP**: Emisiones de Material Particulado durante el año 2019 (medida en tonelada/año)
        - **SO2**: Emisiones de Dióxido de Azufre (SO2) del Establecimiento durante el año 2019 (medida en tonelada/año)
        - **NOX**: Emisiones de Óxidos de nitrógeno (NOx) del Establecimiento durante el año 2019 (medida en tonelada/año)
        - **RESPEL**: Generación de Residuos Peligrosos del Establecimiento durante el año 2019 (medida en tonelada/año)
        - **RESNOPEL**: Generación de Residuos No Peligrosos del Establecimiento durante el año 2019 (medida en tonelada/año)
        - **DESTINATAR**: Destinatario de Residuos No Peligrosos del Establecimiento durante el año 2019 (medida en tonelada/año)         
        ''')
        # st.write('## Incidencia de intoxicaciones agudas por plaguicidas (IAP)')
        # st.write('La incidencia de intoxicaciones agudas por plaguicidas es un importante indicador de los riesgos asociados al uso de estos productos químicos en la agricultura y otros sectores.')
        # st.write('## Riesgo de impactos de salud a consecuencias de olas de calor')
        # st.write('## Consumo promedio de agua por comuna')
        # st.write('## Decretos de Zonas de Escasez Hídrica 2008-2023')
        # st.write('## Nº de VIRS (instalaciones de interés sanitario) por comuna + MAPA')
#  %%
