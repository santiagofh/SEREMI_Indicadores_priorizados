#%%
import pandas as pd
path="data_raw/DRDSS_Matriz_indicadores_y_datos_2023_FINAL (1).xlsx"
df=pd.read_excel(path, sheet_name='Datos 2023 ')
df.rename(columns={
    'Unnamed: 0':'Nº',
    'Unnamed: 1':'Código',
    'Variable':'Comuna'
},inplace=True)
df_filtered = df[df['Código'].astype(str).str.startswith('13')]
df_filtered['Comuna'].replace('Pedro Aguirre Cerda','Pedro Aguirre Cerda',inplace=True)
# %%
df.columns
# %%
var=["Código",
 "Comuna",
 "Tasa de denuncia de violencia intrafamiliar",
 "Tasa de denuncia de delitos de mayor connotación"]
df_violencia=df_filtered[var]
df_violencia.Comuna.loc[df_violencia.Comuna == 'Región Metropolitana'] = 'Región Metropolitana'
# %%
df_violencia.to_csv("data_clean/tasa_violencia_2023.csv")
# %%
