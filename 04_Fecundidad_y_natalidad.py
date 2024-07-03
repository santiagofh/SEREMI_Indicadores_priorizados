import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit_authenticator as stauth


# LECTURA DE ARCHIVOS
df_fec = pd.read_csv('data_clean/tasa_fecundidad.csv')

# Listado comunas y años
lista_comunas = [
    'Todas las comunas', 'Alhué', 'Buin', 'Calera de Tango', 'Cerrillos', 'Cerro Navia', 'Colina', 
    'Conchalí', 'Curacaví', 'El Bosque', 'El Monte', 'Estación Central', 'Huechuraba', 'Independencia', 
    'Isla de Maipo', 'La Cisterna', 'La Florida', 'La Granja', 'La Pintana', 'La Reina', 'Lampa', 
    'Las Condes', 'Lo Barnechea', 'Lo Espejo', 'Lo Prado', 'Macul', 'Maipú', 'María Pinto', 'Melipilla', 
    'Padre Hurtado', 'Paine', 'Pedro Aguirre Cerda', 'Peñaflor', 'Peñalolén', 'Pirque', 'Providencia', 
    'Pudahuel', 'Puente Alto', 'Quilicura', 'Quinta Normal', 'Recoleta', 'Renca', 'San Bernardo', 
    'San Joaquín', 'San José de Maipo', 'San Miguel', 'San Pedro', 'San Ramón', 'Santiago', 'Talagante', 
    'Tiltil', 'Vitacura', 'Ñuñoa', 'Región Metropolitana'
]
lista_años = ['Todos los años', '2013-2015', '2016-2018', '2019-2021']


# Sidebar
st.sidebar.write("## Tablero Interactivo de Comunas: Indicadores priorizados")
comuna_seleccionada = st.sidebar.selectbox("Comuna:", lista_comunas, index=0)
select_year = st.sidebar.selectbox("Año:", lista_años, index=0)

# Título e introducción
st.title('Tasas de Fecundidad por Grupo de Edad en la Región Metropolitana')
st.write('## Análisis detallado por comuna y año')
st.markdown("""
Este gráfico muestra la tasa de fecundidad por grupo de edad en diferentes comunas de la Región Metropolitana. 
Cada línea representa un grupo de edad específico, permitiendo visualizar tendencias a lo largo de los años seleccionados.
Los puntos marcados en cada línea indican datos anuales específicos, lo que facilita la comparación directa entre años.
""")

# Función para filtrar por comuna y año
def filtrar_datos_grafico(df, comuna, year):
    if comuna == 'Todas las comunas':
        df_filtered = df[df['comuna'] == 'Región Metropolitana']
    else:
        df_filtered = df[df['comuna'].str.upper() == comuna.upper()]
    if year != 'Todos los años':
        df_filtered = df_filtered[df_filtered['año'] == year]
    return df_filtered

# Filtrar datos según la comuna y años seleccionados
df_filtrado = filtrar_datos_grafico(df_fec, comuna_seleccionada, select_year)

# Crear el gráfico con Plotly Express
fig = px.line(df_filtrado, x='año', y=['tasas_10_14', 'tasas_15_19', 'tasas_20_34', 'tasas_35_mas', 'tasa_general'],
              title="Tasas de Fecundidad por Grupo de Edad",
              labels={"value": "Tasa", "variable": "Grupo de Edad"},
              color_discrete_sequence=px.colors.qualitative.Set1,
              markers=True)

# Configuración adicional del gráfico
fig.update_layout(xaxis_title='Año', yaxis_title='Tasa de Fecundidad',
                  legend_title="Grupos de Edad", xaxis={'categoryorder':'total descending'},
                  hovermode='x unified',
                  width=800,  # Ajustar el ancho del gráfico
                  height=600  # Ajustar la altura del gráfico si es necesario
)

# Mostrar el gráfico en Streamlit
st.plotly_chart(fig)
st.write("""
Las tasas de fecundidad fueron elaboradas a partir de los datos de nacidos vivos obtenidos de la página de DEIS-MINSAL y de las proyecciones de población de INE obtenidos de su página web. Se calcularon tasas específicas de fecundidad para las madres en los grupos etarios de 10 a 14 años, 15 a 19 años, 20 a 34 años y 35 y más años (considera a 35 a 49 años). Y para el cálculo de la tasa específica del último grupo, se consideró a los nacidos vivos de madres de hasta 50 a 54 años de edad dentro del rango de 35 a 49 años. 

A continuación, se incluyen los links de las fuentes desde donde se obtuvieron los datos.

Datos de nacidos vivos descargados de "Estadísticas de Nacimiento y Natalidad", pestaña "Tasa Específica de Fecundidad".
https://informesdeis.minsal.cl/SASVisualAnalytics/?reportUri=%2Freports%2Freports%2Fa39b6235-6172-4b09-a8b1-ab5f87c72ea0&sectionIndex=1&sso_guest=true&sas-welcome=false

Proyecciones de población > Proyección base 2017 > estimaciones-y-proyecciones-2002-2035-comuna-y-área-urbana-y-rural
https://www.ine.gob.cl/estadisticas/sociales/demografia-y-vitales/proyecciones-de-poblacion
""")

st.write("_Fuente: SEREMI DE SALUD - Subdepartamento de Epidemiología_")

#%%
url = "https://informesdeis.minsal.cl/SASVisualAnalytics/?reportUri=%2Freports%2Freports%2Fa39b6235-6172-4b09-a8b1-ab5f87c72ea0&sectionIndex=1&sso_guest=true&sas-welcome=false"

# Título del Dashboard
st.write("## DEIS Minsal - Dashboard de Nacimientos")

# Descripción introductoria
st.write("""
Este dashboard proporciona acceso a información detallada sobre los nacimientos en Chile, utilizando los datos proporcionados por el Departamento de Estadísticas e Información de Salud (DEIS) del Ministerio de Salud (Minsal). A través del enlace proporcionado, puedes explorar visualizaciones interactivas que abarcan diversas estadísticas y tendencias sobre los nacimientos en el país.
""")

# Enlace al Dashboard externo
st.markdown(f"[Abrir página web del Dashboard de Nacimientos]({url})")