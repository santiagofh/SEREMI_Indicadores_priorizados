#%%
import streamlit as st
#%%
st.image('img/seremi-100-años.png', width=300)
logo_horizontal = 'img/horizontal_SEREMIRM_blue.png'
logo_icono = 'img/icon_SEREMIRM.png'
st.logo(logo_horizontal, icon_image=logo_icono)
#%%
# Página principal
def home():
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
    
def ira_era():
    st.page_link("https://ira-era-rm.streamlit.app/", label="Dashboard de atenciones de urgencia - Enfermedades Respiratorias", icon="🌎")
def prais():
    st.page_link("https://lookerstudio.google.com/reporting/394316c8-9431-44ce-b38a-a1fc1c3b6d97/page/LELkD?s=pDwtKUp4lEE", label="Dashboard PRAIS", icon="🌎")

#%%

pages = {
    "Inicio":[
        st.Page(home, default=True, title="Pagina de inicio", icon=":material/home:")
    ],
    "Indicadores Demográficos y Ambientales" : [
        st.Page("01_Territorio_y_demografía.py", title="Territorio y demografía", icon=":material/public:"),
        st.Page("02_Ambiental.py", title="Ambiental", icon=":material/eco:"),
        st.Page("04_Fecundidad_y_natalidad.py", title="Fecundidad y natalidad", icon=":material/pregnant_woman:"),
    ],
    "Indices sociales y seguridad" : [
        st.Page("03_Socioeconomico.py", title="Socioeconomico", icon=":material/attach_money:"),
        st.Page("03_Socioeconomico_violencia.py", title="Violencia", icon=":material/attach_money:"),
        st.Page("04_Indicadores_sociales.py", title="Indice Prioridad Social", icon=":material/monitoring:"),
    ],
    "Indicadores de Salud" : [
        # st.Page("04_Fecundidad_y_natalidad.py", title="Fecundidad y natalidad", icon=":material/pregnant_woman:"),
        st.Page("05_Sistema_Salud.py", title="Sistema Salud", icon=":material/health_and_safety:"),
        # st.Page("06_Estilos_de_vida‍.py", title="Estilos de vida‍", icon=":material/close:"),
        # st.Page("07_Morbilidad.py", title="Morbilidad", icon=":material/close:"),
        # st.Page("08_Estratificacion.py", title="Estratificacion", icon=":material/close:"),
        st.Page("09_Mortalidad.py", title="_Mortalidad", icon=":material/deceased:"),
        st.Page(ira_era, title="Visor de Atenciones de urgencias - Respiratorias", icon=":material/health_and_safety:")
    ],
    "PRAIS":[
        st.Page(prais, title="Visor PRAIS", icon=":material/health_and_safety:")
    ],
    "Recursos" : [
        st.Page("99_Fuentes_archivos.py", title="Fuentes y archivos", icon=":material/description:")
    ]
}
pg = st.navigation(pages)
pg.run()
