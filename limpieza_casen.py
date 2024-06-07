#%%
import pandas as pd
import numpy as np
path22 = 'data_raw/INDICADORES COMUNALES CASEN 2022 RMS.xlsx'
path17 = 'data_raw/INDICADORES COMUNALES CASEN 2017 RMS.xlsx'
path20 = 'data_raw/INDICADORES COMUNALES CASEN 2020 RMS.xlsx'
def read_casen(path,pestaña):
    df = pd.read_excel(path, sheet_name=pestaña, skiprows=4, nrows=52)
    df = df.replace('**', np.nan)
    df = df.replace('*', np.nan)
    df.dropna(axis=1, how='all', inplace=True)
    df.dropna(axis=0, how='all', inplace=True)
    return df
casen22_pobrezam = read_casen(path22,'POBREZA MULTIDIMENSIONAL (SAE)')
casen22_ingresos = read_casen(path22,'INGRESOS')
casen22_escolaridad_15 = read_casen(path22,'ESCOLARIDAD MAYORES 15')
casen22_escolaridad_18 = read_casen(path22,'ESCOLARIDAD MAYORES 18')
casen22_participacion_laboral = read_casen(path22,'TASAS PARTICIPACIÓN LABORAL')
casen22_prevision = read_casen(path22,'PREVISIÓN DE SALUD')
casen22_migrantes = read_casen(path22,'MIGRANTES')
casen22_etnias = read_casen(path22,'ETNIAS')
casen20_pobrezai = read_casen(path20,'POBREZA DE INGRESOS')
casen20_ingresos = read_casen(path20,'INGRESOS')
casen20_escolaridad_15 = read_casen(path20,'ESCOLARIDAD MAYORES 15')
casen20_escolaridad_18 = read_casen(path20,'ESCOLARIDAD MAYORES 18')
casen20_participacion_laboral = read_casen(path20,'TASAS PARTICIPACIÓN LABORAL')
casen20_prevision = read_casen(path20,'PREVISIÓN DE SALUD')
casen20_migrantes = read_casen(path20,'MIGRANTES')
casen20_etnias = read_casen(path20,'ETNIAS')
casen17_pobrezam = read_casen(path17,'POBREZA MULTIDIMENSIONAL (SAE)')
casen17_pobrezai = read_casen(path17,'POBREZA DE INGRESOS (SAE)')
casen17_ingresos = read_casen(path17,'INGRESOS')
casen17_escolaridad_15 = read_casen(path17,'ESCOLARIDAD MAYORES 15')
casen17_escolaridad_18 = read_casen(path17,'ESCOLARIDAD MAYORES 18')
casen17_participacion_laboral = read_casen(path17,'TASAS PARTICIPACIÓN LABORAL')
casen17_prevision = read_casen(path17,'PREVISIÓN DE SALUD')
casen17_migrantes = read_casen(path17,'MIGRANTES')
casen17_etnias = read_casen(path17,'ETNIAS')
#%%
# casen_combined.to_csv('data_clean/CASEN_RM.csv')
casen22_pobrezam.to_csv('data_clean/casen22_pobrezam.csv')
casen22_ingresos.to_csv('data_clean/casen22_ingresos.csv')
casen22_escolaridad_15.to_csv('data_clean/casen22_escolaridad_15.csv')
casen22_escolaridad_18.to_csv('data_clean/casen22_escolaridad_18.csv')
casen22_participacion_laboral.to_csv('data_clean/casen22_participacion_laboral.csv')
casen22_prevision.to_csv('data_clean/casen22_prevision.csv')
casen22_migrantes.to_csv('data_clean/casen22_migrantes.csv')
casen22_etnias.to_csv('data_clean/casen22_etnias.csv')
# %%
