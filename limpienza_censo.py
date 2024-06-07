#%%
import pandas as pd
path='data_raw/1_1_poblacion.xls'
df_com=pd.read_excel(path, sheet_name='Comuna',skiprows=2)
df_reg=pd.read_excel(path, sheet_name='Región',skiprows=2)
#%%
df_reg_rm=df_reg.loc[df_reg['NOMBRE REGIÓN']=='METROPOLITANA DE SANTIAGO']
df_com_rm=df_com.loc[df_com['CÓDIGO REGIÓN']=='13']
df_reg_rm['NOMBRE COMUNA']='Todas las comunas'
# %%
df_rm=pd.concat([df_reg_rm,df_com_rm])
df_rm.to_csv('data_clean/CENSO17_Poblacion_rm.csv')
# %%
