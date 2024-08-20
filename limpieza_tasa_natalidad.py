import os
import pandas as pd

# Ruta de la carpeta que contiene los archivos Excel
carpeta = 'data_raw/Tasa de Natalidad por año'

# Lista para almacenar todos los DataFrames
dataframes = []

# Recorrer todos los archivos en la carpeta
for archivo in os.listdir(carpeta):
    if archivo.endswith('.xlsx') or archivo.endswith('.xls'):
        # Leer el archivo Excel
        df = pd.read_excel(os.path.join(carpeta, archivo))
        
        # Agregar una columna con el nombre del archivo (sin la extensión)
        df['Comuna'] = os.path.splitext(archivo)[0]
        
        # Agregar el DataFrame a la lista
        dataframes.append(df)

# Concatenar todos los DataFrames en uno solo
df_concatenado = pd.concat(dataframes, ignore_index=True)

# Mostrar el DataFrame resultante

print(df_concatenado)

# Si deseas guardar el resultado en un archivo CSV o Excel
df_concatenado.to_csv('data_clean/Nacimiento/tasa_natalidad_consolidado.csv', index=False)
# df_concatenado.to_excel('tasa_natalidad_consolidado.xlsx', index=False)
