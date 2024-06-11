import pandas as pd

# Path o rutas para archivos
path = 'data_raw/Caracterización Beneficiarios Fonasa Desagregado por comuna RM.xlsx'

# Leer los datos
df_sexo = pd.read_excel(path, sheet_name='SEXO ', skiprows=4)
df_tramo = pd.read_excel(path, sheet_name='TRAMO FONASA', skiprows=4)
df_edad = pd.read_excel(path, sheet_name='TRAMO EDAD', skiprows=4)

# Diccionario para renombrar columnas
dict_col = {
    'Unnamed: 0': 'CODIGO',
    'Unnamed: 1': 'COMUNA',
    'Unnamed: 5': 'TOTAL',
    'Unnamed: 6': 'TOTAL'
}

# Renombrar columnas en cada DataFrame
df_sexo.rename(columns=dict_col, inplace=True)
df_tramo.rename(columns=dict_col, inplace=True)
df_edad.rename(columns=dict_col, inplace=True)

# Añadir la columna Category
df_sexo['Category'] = 'SEXO'
df_tramo['Category'] = 'TRAMO FONASA'
df_edad['Category'] = 'TRAMO EDAD'

# Concatenar los DataFrames
df_concatenado = pd.concat([df_sexo, df_tramo, df_edad], ignore_index=True)

# Guardar el DataFrame concatenado a un archivo CSV
df_concatenado.to_csv('data_clean/fonasa_2024.csv', index=False)

# Mostrar el DataFrame concatenado
print("DataFrame Concatenado:")
print(df_concatenado.head())
