#%%
import pandas as pd
path='data_raw/DEFUNCIONES_FUENTE_DEIS_2022_2024_07052024.csv'
df=pd.read_csv(path, encoding='LATIN1',sep=';',header=None)
#%%
df1=df.iloc[:,[1,2,6,16]]
df2=df1.rename(columns={1:'fecha_def',2:'sexo',6:'comuna',16:'casusa_def'})
df2.to_csv('data_clean/Defunciones_2022_2024.csv')
# %%
