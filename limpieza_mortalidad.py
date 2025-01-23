import pandas as pd
paths = [
    'data_raw/Mortalidad/Causas externas 2005-2020.xlsx',
    'data_raw/Mortalidad/Circulatoria 2005-2020.xlsx',
    'data_raw/Mortalidad/Digestivas 2005-2020.xlsx',
    'data_raw/Mortalidad/Endocrinas 2005-2020.xlsx'
]
mapeo_comunas = {
    'ALHUÉ': 'Alhué', 'BUIN': 'Buin', 'CALERA DE TANGO': 'Calera de Tango', 'CERRILLOS': 'Cerrillos',
    'CERRO NAVIA': 'Cerro Navia', 'COLINA': 'Colina', 'CONCHALÍ': 'Conchalí', 'CURACAVÍ': 'Curacaví',
    'EL BOSQUE': 'El Bosque', 'EL MONTE': 'El Monte', 'ESTACIÓN CENTRAL': 'Estación Central',
    'HUECHURABA': 'Huechuraba', 'INDEPENDENCIA': 'Independencia', 'ISLA DE MAIPO': 'Isla de Maipo',
    'LA CISTERNA': 'La Cisterna', 'LA FLORIDA': 'La Florida', 'LA GRANJA': 'La Granja', 'LA PINTANA': 'La Pintana',
    'LA REINA': 'La Reina', 'LAMPA': 'Lampa', 'LAS CONDES': 'Las Condes', 'LO BARNECHEA': 'Lo Barnechea',
    'LO ESPEJO': 'Lo Espejo', 'LO PRADO': 'Lo Prado', 'MACUL': 'Macul', 'MAIPÚ': 'Maipú', 'MARÍA PINTO': 'María Pinto',
    'MELIPILLA': 'Melipilla', 'PADRE HURTADO': 'Padre Hurtado', 'PAINE': 'Paine', 'PEDRO A CERDA': 'Pedro Aguirre Cerda',
    'PEDRO AGUIRRE CERDA': 'Pedro Aguirre Cerda', 'PEÑAFLOR': 'Peñaflor', 'PEÑALOLÉN': 'Peñalolén',
    'PIRQUE': 'Pirque', 'PROVIDENCIA': 'Providencia', 'PUDAHUEL': 'Pudahuel', 'PUENTE ALTO': 'Puente Alto',
    'QUILICURA': 'Quilicura', 'QUINTA NORMAL': 'Quinta Normal', 'RECOLETA': 'Recoleta', 'RENCA': 'Renca',
    'SAN BERNARDO': 'San Bernardo', 'SAN JOAQUÍN': 'San Joaquín', 'SAN JOSÉ DE MAIPO': 'San José de Maipo',
    'SAN MIGUEL': 'San Miguel', 'SAN PEDRO': 'San Pedro', 'SAN RAMÓN': 'San Ramón', 'SANTIAGO': 'Santiago',
    'TALAGANTE': 'Talagante', 'TILTIL': 'Tiltil', 'VITACURA': 'Vitacura', 'ÑUÑOA': 'Ñuñoa',
    'REGIÓN METROPOLITAN': 'Región Metropolitana', 'REGIÓN METROPOLITANA': 'Región Metropolitana',
    'REGIÓN METROPOLITANA ': 'Región Metropolitana', 'Pedro\xa0Aguirre Cerda': 'Pedro Aguirre Cerda'
}
def read_all_sheets(file_path):
    all_sheets = pd.read_excel(file_path, sheet_name=None)
    return all_sheets

def split_df_by_keyword(df, keywords1=['HOMBRES', 'HOMBRE', 'HOMBRES'], keywords2=['MUJERES', 'MUJER', 'MUEJRES']):
    first_col = df.iloc[:, 0]
    idx1 = first_col[first_col.str.contains('|'.join(keywords1), na=False)].index[0]
    idx2 = first_col[first_col.str.contains('|'.join(keywords2), na=False)].index[0]
    
    if idx1 < idx2:
        df_hombres = df.iloc[:idx2, :].copy()
        df_mujeres = df.iloc[idx2:, :].copy()
    else:
        df_hombres = df.iloc[:idx1, :].copy()
        df_mujeres = df.iloc[idx1:, :].copy()
    
    df_hombres = df_hombres.dropna(how='any', axis=0)
    df_mujeres = df_mujeres.dropna(how='any', axis=0)

    df_hombres.columns = df_hombres.iloc[0]
    df_hombres = df_hombres[1:].reset_index(drop=True)
    df_hombres['Sexo'] = 'Hombres'
    
    df_mujeres.columns = df_mujeres.iloc[0]
    df_mujeres = df_mujeres[1:].reset_index(drop=True)
    df_mujeres['Sexo'] = 'Mujeres'
    
    if 'COMUNA' in df_hombres.columns:
        df_hombres.rename(columns={'COMUNA': 'COMUNA DE RESIDENCIA'}, inplace=True)
    if 'COMUNA' in df_mujeres.columns:
        df_mujeres.rename(columns={'COMUNA': 'COMUNA DE RESIDENCIA'}, inplace=True)
    
    df_hombres['COMUNA DE RESIDENCIA'] = df_hombres['COMUNA DE RESIDENCIA'].replace(mapeo_comunas)
    df_mujeres['COMUNA DE RESIDENCIA'] = df_mujeres['COMUNA DE RESIDENCIA'].replace(mapeo_comunas)

    return pd.concat([df_hombres, df_mujeres], ignore_index=True)

all_dfs = []

for path in paths:
    sheet_dict = read_all_sheets(path)
    for sheet_name, df in sheet_dict.items():
        sanitized_sheet_name = sheet_name.replace(' ', '_').replace('.', '_')
        try:
            df_combined = split_df_by_keyword(df)
            df_combined['Mortalidad'] = sanitized_sheet_name
            all_dfs.append(df_combined)
            
            print(f'Variables creadas: {sanitized_sheet_name}')
        except IndexError:
            print(f'No se encontraron las palabras clave en {sanitized_sheet_name}')

final_df = pd.concat(all_dfs, ignore_index=True)
cols = ['Mortalidad', 'Sexo'] + [col for col in final_df if col not in ['Mortalidad', 'Sexo']]
final_df = final_df[cols]
print(final_df)
final_df.to_excel('data_clean/Mortalidad/mortalidad_final.xlsx', index=False)
final_df.to_csv('data_clean/Mortalidad/mortalidad_final.csv', index=False)
