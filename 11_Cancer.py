import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

lista_comunas = [
    'Región Metropolitana', 'Alhué', 'Buin', 'Calera de Tango', 'Cerrillos', 'Cerro Navia',
    'Colina', 'Conchalí', 'Curacaví', 'El Bosque', 'El Monte', 'Estación Central',
    'Huechuraba', 'Independencia', 'Isla de Maipo', 'La Cisterna', 'La Florida', 'La Granja',
    'La Pintana', 'La Reina', 'Lampa', 'Las Condes', 'Lo Barnechea', 'Lo Espejo',
    'Lo Prado', 'Macul', 'Maipú', 'María Pinto', 'Melipilla', 'Ñuñoa', 'Padre Hurtado',
    'Paine', 'Pedro Aguirre Cerda', 'Peñaflor', 'Peñalolén', 'Pirque', 'Providencia',
    'Pudahuel', 'Puente Alto', 'Quilicura', 'Quinta Normal', 'Recoleta', 'Renca',
    'San Bernardo', 'San Joaquín', 'San José de Maipo', 'San Miguel', 'San Pedro',
    'San Ramón', 'Santiago', 'Talagante', 'Tiltil', 'Vitacura'
]

def humanize_mortalidad(mortalidad):
    mortalidad = mortalidad.replace('_', ' ').replace('.', '')
    mortalidad = mortalidad.title()
    mortalidad = mortalidad.replace('De', 'de').replace('Y', 'y')
    return mortalidad

orden_mortalidades = [
    'Causas_externas', 'Lesiones_autoinflingidas', 'Accidentes_Transporte', 'Caídas', 'Agresiones',
    'Circulatoria', 'Enfermedad_Cerebrovascular', 'Enfermedad_Isquémica', 'Enfermedad_Hipertensiva',
    'Digestivas', 'Enf__Hígado', 'Endocrinas', 'Diabetes'
]

df_mortalidad = pd.read_csv('data_clean/Mortalidad/mortalidad_final.csv')

if 'COMUNA DE RESIDENCIA' in df_mortalidad.columns:
    df_mortalidad = df_mortalidad.sort_values(by='COMUNA DE RESIDENCIA')

df_mortalidad.replace(0, np.nan, inplace=True)

mortalidades = df_mortalidad['Mortalidad'].unique()
mortalidades_humanas = [humanize_mortalidad(mortalidad) for mortalidad in mortalidades]
mortalidad_dict = dict(zip(mortalidades_humanas, mortalidades))
mortalidades_ordenadas = [humanize_mortalidad(mortalidad) for mortalidad in orden_mortalidades if mortalidad in mortalidad_dict.values()]

st.sidebar.write("## Tablero Interactivo de Comunas: Indicadores priorizados")

comuna_seleccionada = st.sidebar.selectbox("Selecciona la Comuna:", lista_comunas, index=0)

genero_seleccionado = st.sidebar.radio('Selecciona el Sexo:', ('Ambos', 'Hombres', 'Mujeres'))

causa_seleccionada_humana = st.sidebar.selectbox('Selecciona la Causa de Mortalidad:', mortalidades_ordenadas)
mortalidad_seleccionada = mortalidad_dict[causa_seleccionada_humana]

st.write('# Región Metropolitana y sus comunas: Mortalidad')

filtered_df = df_mortalidad[df_mortalidad['Mortalidad'] == mortalidad_seleccionada]
filtered_df = filtered_df[filtered_df['COMUNA DE RESIDENCIA'] == comuna_seleccionada]

if genero_seleccionado != 'Ambos':
    filtered_df = filtered_df[filtered_df['Sexo'] == genero_seleccionado]
if genero_seleccionado == 'Ambos':
    df_todas_comunas = df_mortalidad[(df_mortalidad['Mortalidad'] == mortalidad_seleccionada) & (df_mortalidad['COMUNA DE RESIDENCIA'] == 'Región Metropolitana')]
else:
    df_todas_comunas = df_mortalidad[(df_mortalidad['Mortalidad'] == mortalidad_seleccionada) & (df_mortalidad['COMUNA DE RESIDENCIA'] == 'Región Metropolitana') & (df_mortalidad['Sexo'] == genero_seleccionado)]

df_todas_comunas['Comuna_Sexo'] = 'Región Metropolitana (' + df_todas_comunas['Sexo'] + ')'

filtered_df['Comuna_Sexo'] = filtered_df['COMUNA DE RESIDENCIA'] + ' (' + filtered_df['Sexo'] + ')'

filtered_df = pd.concat([filtered_df, df_todas_comunas], ignore_index=True)
filtered_df = filtered_df.drop_duplicates(subset=['Mortalidad','Sexo','COMUNA DE RESIDENCIA'])
filtered_df.columns = filtered_df.columns.str.replace('.0', '', regex=False)
Años = [col for col in filtered_df.columns if col.isdigit()]
df_long = filtered_df.melt(id_vars=['COMUNA DE RESIDENCIA', 'Sexo', 'Comuna_Sexo'], value_vars=Años, var_name='Año', value_name='Tasa de Mortalidad Ajustada')
df_long['Tasa de Mortalidad Ajustada'] = df_long['Tasa de Mortalidad Ajustada'].astype(str)
df_long['Tasa de Mortalidad Ajustada'] = df_long['Tasa de Mortalidad Ajustada'].str.replace(',', '.').astype(float)

fig = px.line(df_long, 
              x='Año', 
              y='Tasa de Mortalidad Ajustada', 
              color='Comuna_Sexo', 
              line_group='Comuna_Sexo', 
              title=f'{causa_seleccionada_humana}')

def format_number(value):
    if pd.isna(value) or value == "":
        return ""
    return f"{float(value):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

df_table = filtered_df.copy()
df_table[Años] = df_table[Años].applymap(format_number)

st.write(f"### {causa_seleccionada_humana} en {comuna_seleccionada}")
st.write(df_table)
st.plotly_chart(fig)

st.write("""
(*) Tasa de Mortalidad Ajustada : Calculada con método de ajuste directo por 100.000 hbtes. 
Población de referencia corresponde a población Región Metropolitana CENSO 2002.
Tasas ajustadas por tramos de edad de 0 a 14; 15 a 34; 35 a 64; 65 a 74 y 75 años y más. \n
En el análisis comunal, se usa como referencia la población regional Censo 2002, por lo tanto, 
sólo es comparable entre comunas de la Región Metropolitana.\n
Fuente: www.deis.cl "Bases de datos de Mortalidad".
Preparado por: Subdepartamento de Epidemiología / Dpto de Salud Pública / SEREMI de Salud R.M
""")
