#%%

import streamlit as st
from streamlit_authenticator import Authenticate
import yaml
from yaml.loader import SafeLoader
with open('user.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)
authenticator = Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)
authenticator.login()
if st.session_state["authentication_status"]:
    authenticator.logout()
    st.write(f'Bienvenido *{st.session_state["name"]}*')
    logo_horizontal = 'img/horizontal_remolino_blue.png'
    logo_icono = 'img/icon_remolino_blue.png'
    st.logo(logo_horizontal, icon_image=logo_icono)
    st.image('img/seremi-100-años.png', width=300)
    st.markdown('# Región Metropolitana y sus comunas: Indicadores priorizados')
    st.write("""
        ### Bienvenido al Tablero Interactivo de Comunas

        Este tablero está diseñado para proporcionar una visión integral y detallada de los diversos indicadores socioeconómicos, demográficos y urbanos de las comunas que forman la Región Metropolitana de Santiago. Aquí podrás explorar y visualizar datos que abarcan desde distribuciones de población y niveles de ingresos hasta aspectos de salud y educación.

        Utiliza los menús desplegables para seleccionar diferentes comunas y visualizar datos específicos relacionados con cada una. El tablero tiene gráficos interactivos que ayudarán a entender mejor las características y desafíos de cada comuna.

        ### Cómo usar este tablero

        - **Selecciona una comuna:** Utiliza el menú desplegable para elegir una comuna y automáticamente se actualizarán los gráficos y tablas para reflejar los datos correspondientes.
        - **Explora los gráficos:** Interactúa con los gráficos para obtener detalles específicos sobre diferentes indicadores.
        - **Comparación y análisis:** Compara datos entre diferentes comunas ajustando tu selección y analiza las tendencias y patrones de los datos.
        """)
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')



