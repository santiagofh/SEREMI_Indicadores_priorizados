#%%
import pandas as pd
#%%
path1='data_raw/Serie_Nacimientos_1992_2000.csv'
path2='data_raw/Serie_Nacimientos_2001_2019.csv'
path3='data_raw/BD_NAC_2020_2021.csv'
#%%
df1=pd.read_csv(path1,sep=';',encoding='LATIN1')
df2=pd.read_csv(path2,sep=';',encoding='LATIN1')
df3=pd.read_csv(path3,sep=';',encoding='LATIN1')
# %%
df=pd.concat([df1,df2,df3])
df_s=df[['ANO_NAC','SEXO','GRUPO_ETARIO_MADRE']]
# %%
df_s.to_csv("data_clean/nacimientos.csv")
# %%
