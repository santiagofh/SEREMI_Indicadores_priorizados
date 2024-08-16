#%%
import pandas as pd
import numpy as np

#%%
# Define file paths
path17 = 'data_raw/INDICADORES COMUNALES CASEN 2017 RMS.xlsx'
path20 = 'data_raw/INDICADORES COMUNALES CASEN 2020 RMS.xlsx'
path22 = 'data_raw/INDICADORES COMUNALES CASEN 2022 RMS.xlsx'

#%%
def read_casen(path, sheet_name):
    df = pd.read_excel(path, sheet_name=sheet_name, skiprows=4, nrows=53)
    df = df.replace('**', np.nan)
    df = df.replace('*', np.nan)
    df.dropna(axis=1, how='all', inplace=True)
    df.dropna(axis=0, how='all', inplace=True)
    return df

def read_all_sheets_to_dict(path, year, rename_dict):
    sheets = pd.ExcelFile(path).sheet_names
    data_dict = {}
    for sheet in sheets:
        df = read_casen(path, sheet)
        df['Año'] = year
        unified_sheet_name = rename_dict.get(sheet.strip(), sheet.strip())
        if unified_sheet_name in data_dict:
            data_dict[unified_sheet_name] = pd.concat([data_dict[unified_sheet_name], df], ignore_index=True)
        else:
            data_dict[unified_sheet_name] = df
    return data_dict

rename_dict = {
    'POBREZA DE INGRESOS': 'POBREZA DE INGRESOS',
    'POBREZA DE INGRESOS (SAE)': 'POBREZA DE INGRESOS',
    ' POBREZA DE INGRESOS (SAE)': 'POBREZA DE INGRESOS',
    'POBREZA MULTIDIMENSIONAL (SAE)': 'POBREZA MULTIDIMENSIONAL',
    'ÍNDICE DE HACINAMIENTO': 'HACINAMIENTO'
}
#%%
data_2017_dict = read_all_sheets_to_dict(path17, 2017, rename_dict)
data_2020_dict = read_all_sheets_to_dict(path20, 2020, rename_dict)
data_2022_dict = read_all_sheets_to_dict(path22, 2022, rename_dict)

# %%
keys_to_exclude = ['ÍNDICE', 'NOTAS']
all_dataframes = []
def add_year_and_category(df, year, category):
    df['Año'] = year
    df['Category'] = category
    cols = ['Año', 'Category'] + [col for col in df.columns if col not in ['Año', 'Category']]
    return df[cols]
for key, data_dict in zip([2017, 2020, 2022], [data_2017_dict, data_2020_dict, data_2022_dict]):
    for sheet_name in data_dict:
        if sheet_name not in keys_to_exclude:
            df = data_dict[sheet_name]
            df = add_year_and_category(df, key, sheet_name)
            all_dataframes.append(df)   
combined_df = pd.concat(all_dataframes, ignore_index=True)
#%%

# %%
# Para la Category 'POBREZA DE INGRESOS', combinar la variable 'Pobres 2020' con 'Pobres'
combined_df.loc[combined_df['Category'] == 'POBREZA DE INGRESOS', 'Pobres'] = combined_df.loc[combined_df['Category'] == 'POBREZA DE INGRESOS', 'Pobres'].combine_first(combined_df.loc[combined_df['Category'] == 'POBREZA DE INGRESOS', 'Pobres 2020'])
#%%
# Actualizar las columnas de ingresos con 'No reporta' si son NaN para la categoría 'INGRESOS'
income_categories = ['Ingreso Autónomo', 'Ingreso Monetario', 'Ingresos del trabajo', 'Ingreso Total']
combined_df.loc[combined_df['Category'] == 'INGRESOS', income_categories] = combined_df.loc[combined_df['Category'] == 'INGRESOS', income_categories].fillna('NA')

# Ordenar las columnas según el orden especificado
ordered_columns = ['Año', 'Category', 'Comuna', 'Pobres', 'No pobres', 'Total'] + income_categories + [col for col in combined_df.columns if col not in ['Año', 'Category', 'Comuna', 'Pobres', 'No pobres', 'Total'] + income_categories]

# Reordenar el DataFrame
combined_df = combined_df[ordered_columns]
combined_df = combined_df.drop(columns=['Pobres 2020','Unnamed: 8'])

# Guardar el DataFrame final en un archivo CSV
combined_df.to_csv('data_clean/casen_17_22.csv', index=False)

# %%