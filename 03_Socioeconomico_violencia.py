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
import streamlit_authenticator as stauth

#%%
# Path o rutas para archivos
paths = {
    "violencia": 'data_clean/tasa_violencia_2023.csv',
}

#%%
# LECTURA DE ARCHIVOS
violencia_2023 = pd.read_csv(paths["violencia"])
#%%
# Listado comunas
lista_comunas = [
    'Región Metropolitana', 
    'Alhué', 
    'Buin', 
    'Calera de Tango', 
    'Cerrillos', 
    'Cerro Navia', 
    'Colina', 
    'Conchalí', 
    'Curacaví', 
    'El Bosque', 
    'El Monte', 
    'Estación Central', 
    'Huechuraba', 
    'Independencia', 
    'Isla de Maipo',
    'La Cisterna',
    'La Florida',
    'La Granja',
    'La Pintana',
    'La Reina',
    'Lampa', 
    'Las Condes',
    'Lo Barnechea',
    'Lo Espejo',
    'Lo Prado',
    'Macul',
    'Maipú',
    'María Pinto',
    'Melipilla',
    'Ñuñoa',
    'Padre Hurtado',
    'Paine',
    'Pedro Aguirre Cerda',
    'Peñaflor',
    'Peñalolén',
    'Pirque',
    'Providencia', 
    'Pudahuel',
    'Puente Alto',
    'Quilicura',
    'Quinta Normal',
    'Recoleta',
    'Renca',
    'San Bernardo', 
    'San Joaquín',
    'San José de Maipo',
    'San Miguel',
    'San Pedro',
    'San Ramón',
    'Santiago',
    'Talagante', 
    'Tiltil',
    'Vitacura'
]

#%%
# INICIO DE LA PAGINA
#%%
# Sidebar
st.sidebar.write("## Tablero Interactivo de Comunas: Tasas de violencia")
st.sidebar.write("Selección de Comuna")

default_index = lista_comunas.index("Región Metropolitana") if "Región Metropolitana" in lista_comunas else 0
comuna_seleccionada = st.sidebar.multiselect("Comuna:", lista_comunas, default=[lista_comunas[default_index]])

# Trabajo del DF
filtro_comuna = [comuna.upper() for comuna in comuna_seleccionada]  # Convertir a mayúsculas

def format_comunas(comunas):
    if not comunas:
        return None  # Retorna None si la lista está vacía
    elif len(comunas) == 1:
        return comunas[0]
    elif len(comunas) == 2:
        return f'{comunas[0]} y {comunas[1]}'
    else:
        return ', '.join(comunas[:-1]) + f' y {comunas[-1]}'

if not comuna_seleccionada:
    st.error("Por favor, selecciona al menos una comuna.")
    st.stop()  # Detiene la ejecución del código de Streamlit en este punto

# Formatear las comunas seleccionadas
comunas_formateadas = format_comunas(comuna_seleccionada)

violencia_2023['Comuna'] = violencia_2023['Comuna'].str.upper()  # Asegúrate de que la columna 'Comuna' esté en mayúsculas
violencia_intra_rm = violencia_2023['Tasa de denuncia de violencia intrafamiliar'].loc[violencia_2023['Comuna'] == 'REGIÓN METROPOLITANA'].iloc[0]
violencia_delit_rm = violencia_2023['Tasa de denuncia de delitos de mayor connotación'].loc[violencia_2023['Comuna'] == 'REGIÓN METROPOLITANA'].iloc[0]

violencia_2023['comuna_rm_intra'] = np.where(
    violencia_2023['Tasa de denuncia de violencia intrafamiliar'] > violencia_intra_rm,
    'Tasa sobre la RM',
    'Tasa bajo de la RM'
)
violencia_2023['comuna_rm_delit'] = np.where(
    violencia_2023['Tasa de denuncia de delitos de mayor connotación'] > violencia_delit_rm,
    'Tasa sobre la RM',
    'Tasa bajo de la RM'
)

if 'REGIÓN METROPOLITANA' in filtro_comuna:
    violencia_2023_comuna = violencia_2023
else:
    violencia_2023_comuna = violencia_2023.loc[violencia_2023['Comuna'].isin(filtro_comuna) |
                                               (violencia_2023['Comuna'] == 'REGIÓN METROPOLITANA')]

# Ordenar por 'Comuna'
violencia_2023_comuna['Comuna'] = pd.Categorical(violencia_2023_comuna['Comuna'], categories=[c.upper() for c in lista_comunas], ordered=True)
violencia_2023_comuna = violencia_2023_comuna.sort_values('Comuna')

#%%
import streamlit as st
import pandas as pd

st.write(f"## Visor de tasas de violencia para {comunas_formateadas}")
tabla_violencia=violencia_2023_comuna[['Comuna','Tasa de denuncia de violencia intrafamiliar','Tasa de denuncia de delitos de mayor connotación']]
tabla_violencia['Tasa de denuncia de violencia intrafamiliar'] = tabla_violencia['Tasa de denuncia de violencia intrafamiliar'].apply(lambda x: f"{x:,.2f}".replace('.',',').replace(',',''))
tabla_violencia['Tasa de denuncia de delitos de mayor connotación'] = tabla_violencia['Tasa de denuncia de delitos de mayor connotación'].apply(lambda x: f"{x:,.2f}".replace('.',',').replace(',',''))

st.write(tabla_violencia)

st.write(f"### Tasa de denuncia de violencia intrafamiliar para {comunas_formateadas}")

fig_violencia_intra= px.bar(
    violencia_2023_comuna,
    x='Comuna',
    y='Tasa de denuncia de violencia intrafamiliar',
    title=f"Tasa de denuncia de violencia intrafamiliar en {comunas_formateadas}",
    color='comuna_rm_intra',
    color_discrete_map={'Tasa sobre la RM': 'red', 'Tasa bajo de la RM': 'blue'},
    labels={'Tasa de denuncia de violencia intrafamiliar': 'Tasa de denuncia', 
            'Comuna': 'Comuna',
            'comuna_rm_intra':'Tasa de violencia sobre la RM'
            }
)
fig_violencia_intra.update_layout(
    yaxis_tickformat=".0f",
    xaxis=dict(
        tickfont=dict(size=10),
        categoryorder='array',
        categoryarray=list(violencia_2023_comuna['Comuna'])
    ),
    showlegend=False
)
fig_violencia_intra.add_shape(
    type="line",
    x0=0,
    x1=1,
    y0=violencia_intra_rm,
    y1=violencia_intra_rm,
    line=dict(color="black", width=2, dash="dash"),
    xref='paper',
    yref='y'
)
st.write(fig_violencia_intra)
st.write(f'''
- Azul: Comunas con tasas menores a la de la Región Metropolitana
- Rojo: Comunas con tasas mayores a la de la Región Metropolitana
''')
# %%
st.write(f"### Tasa de denuncia de delitos de mayor connotación para {comunas_formateadas}")

fig_violencia_delit= px.bar(
    violencia_2023_comuna,
    x='Comuna',
    y='Tasa de denuncia de delitos de mayor connotación',
    title=f"Tasa de denuncia de delitos de mayor connotación en {comunas_formateadas}",
    color='comuna_rm_delit',
    color_discrete_map={'Tasa sobre la RM': 'red', 'Tasa bajo de la RM': 'blue'},
    labels={'Tasa de denuncia de delitos de mayor connotación': 'Tasa de denuncia', 
            'Comuna': 'Comuna',
            'comuna_rm_delit':'Tasa de violencia sobre la RM'
            }
)
fig_violencia_delit.update_layout(
    yaxis_tickformat=".0f",
    xaxis=dict(
        tickfont=dict(size=10),
        categoryorder='array',
        categoryarray=list(violencia_2023_comuna['Comuna'])
    ),
    showlegend=False
)
fig_violencia_delit.add_shape(
    type="line",
    x0=0,
    x1=1,
    y0=violencia_delit_rm,
    y1=violencia_delit_rm,
    line=dict(color="red", width=2, dash="dash"),
    xref='paper',
    yref='y'
)
st.write(fig_violencia_delit)
st.write(f'''
- Azul: Comunas con tasas menores a la de la Región Metropolitana
- Rojo: Comunas con tasas mayores a la de la Región Metropolitana
''')