import pandas as pd
path = 'data_raw/Tasas trienales de fecundidad por comuna en la RM.xlsx'
df = pd.read_excel(path, skiprows=4)
df = df.dropna(axis=1, how='all')
dic_col_tasas_2013_2015 = {
    'Comuna': 'comuna',
    '10 a 14 años': 'tasas_10_14',
    '15 a 19 años': 'tasas_15_19',
    '20 a 34 años': 'tasas_20_34',
    '35 y más años': 'tasas_35_mas',
    'Tasa comunal general': 'tasa_general',
}

dic_col_tasas_2016_2018 = {
    'Comuna.1': 'comuna',
    '10 a 14 años.1': 'tasas_10_14',
    '15 a 19 años.1': 'tasas_15_19',
    '20 a 34 años.1': 'tasas_20_34',
    '35 y más años.1': 'tasas_35_mas',
    'Tasa comunal general.1': 'tasa_general',
}

dic_col_tasas_2019_2021 = {
    'Comuna.2': 'comuna',
    '10 a 14 años.2': 'tasas_10_14',
    '15 a 19 años.2': 'tasas_15_19',
    '20 a 34 años.2': 'tasas_20_34',
    '35 y más años.2': 'tasas_35_mas',
    'Tasa comunal general.2': 'tasa_general',
}
df_2013_2015 = df[['Comuna', '10 a 14 años', '15 a 19 años', '20 a 34 años', '35 y más años', 'Tasa comunal general']].rename(columns=dic_col_tasas_2013_2015)
df_2013_2015['año'] = '2013-2015'

df_2016_2018 = df[['Comuna.1', '10 a 14 años.1', '15 a 19 años.1', '20 a 34 años.1', '35 y más años.1', 'Tasa comunal general.1']].rename(columns=dic_col_tasas_2016_2018)
df_2016_2018['año'] = '2016-2018'

df_2019_2021 = df[['Comuna.2', '10 a 14 años.2', '15 a 19 años.2', '20 a 34 años.2', '35 y más años.2', 'Tasa comunal general.2']].rename(columns=dic_col_tasas_2019_2021)
df_2019_2021['año'] = '2019-2021'

df_final = pd.concat([df_2013_2015, df_2016_2018, df_2019_2021])
replacements = {
    'Tasa Regional 2013-2015': 'Región Metropolitana',
    'Tasa Regional 2016-2018': 'Región Metropolitana',
    'Tasa Regional 2019-2021': 'Región Metropolitana'
}
df_final['comuna'] = df_final['comuna'].replace(replacements)

df_final = df_final[~df_final['comuna'].str.contains('50 a 54 años', na=False)]
df_final = df_final.dropna(subset=['comuna'])

df_sorted = df_final.sort_values(by=['comuna', 'año'])

print(df_sorted.head())

df_sorted.to_csv('data_clean/tasa_fecundidad.csv')

 