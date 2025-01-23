import os
import pandas as pd
carpeta = 'data_raw/Tasa de Natalidad por año'
dataframes = []
for archivo in os.listdir(carpeta):
    if archivo.endswith('.xlsx') or archivo.endswith('.xls'):
        df = pd.read_excel(os.path.join(carpeta, archivo))
        df['Comuna'] = os.path.splitext(archivo)[0]
        dataframes.append(df)
df_concatenado = pd.concat(dataframes, ignore_index=True)
print(df_concatenado)
df_concatenado.to_csv('data_clean/Nacimiento/tasa_natalidad_consolidado.csv', index=False)
