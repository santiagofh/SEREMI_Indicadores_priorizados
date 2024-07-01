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
