#%%
import streamlit as st
import streamlit_authenticator as stauth

if not st.session_state.authentication_status:
    st.info('Please Login from the Home page and try again.')
    st.stop()
# INICIO DE LA PAGINA
st.set_page_config(page_title="Análisis de Comunas en Región Metropolitana", layout='wide', initial_sidebar_state='expanded')
logo_horizontal = 'img/horizontal_remolino_blue.png'
logo_icono = 'img/icon_remolino_blue.png'
st.logo(logo_horizontal, icon_image=logo_icono)
# TITULO INTRODUCCION
st.image('img/seremi-100-años.png', width=300)
st.write('# Región Metropolitana y sus comunas: Estilo de vida')

st.write('Pagina en construcción')
st.image('img/Personajes-Mujer obrera 2.png')