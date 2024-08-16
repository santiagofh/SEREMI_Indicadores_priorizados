#%%
import pandas as pd
path_ine='data_raw/ine_estimaciones-y-proyecciones-2002-2035_base-2017_comunas0381d25bc2224f51b9770a705a434b74.csv'
path_ine_proy_reg='data_raw/ine_estimaciones-y-proyecciones-2002-2035_base-2017_reg_área_base.csv'
path_ine_urb="data_raw/estimaciones-y-proyecciones-2002-2035-comuna-y-área-urbana-y-rural.csv"

ine_proy=pd.read_csv(path_ine, encoding='LATIN1')
ine_proy_urb=pd.read_csv(path_ine_urb,sep=";", encoding='LATIN1',skiprows=1)
ine_proy_urb.dropna(axis=0,inplace=True)

#%%
ine_proy_com_rm=ine_proy.loc[ine_proy.Region==13]
#%%
ine_proy_reg_rm=ine_proy.loc[ine_proy['Nombre Region']=='Metropolitana de Santiago']
ine_proy_reg_rm=ine_proy_reg_rm.groupby(by=['Nombre Region','Sexo (1=Hombre 2=Mujer)','Edad']).sum()

ine_proy_reg_rm.Region=13
ine_proy_reg_rm.Provincia='Región Metropolitana'
ine_proy_reg_rm['Nombre Provincia']='Región Metropolitana'
ine_proy_reg_rm['Nombre Comuna']='Región Metropolitana'
ine_proy_reg_rm['Comuna']='Región Metropolitana'
ine_proy_reg_rm=ine_proy_reg_rm.reset_index()
#%%
ine_proy_area_com=ine_proy_urb.loc[ine_proy_urb['Nombre Region']=='Metropolitana de Santiago']
ine_proy_area_com.loc[:, ine_proy_area_com.columns.str.startswith('Poblacion')] = ine_proy_area_com.loc[:, ine_proy_area_com.columns.str.startswith('Poblacion')].astype(int)
ine_proy_area_com=ine_proy_area_com.reset_index()

#%%
ine_proy_area_rm=ine_proy_urb.loc[ine_proy_urb['Nombre Region']=='Metropolitana de Santiago']
ine_proy_area_rm.loc[:, ine_proy_area_rm.columns.str.startswith('Poblacion')] = ine_proy_area_rm.loc[:, ine_proy_area_rm.columns.str.startswith('Poblacion')].astype(int)
ine_proy_area_rm['Poblacion 2002']=ine_proy_area_rm['Poblacion 2002'].astype(int)
ine_proy_area_rm=ine_proy_area_rm.groupby(by=['Nombre Region','Sexo (1=Hombre 2=Mujer)','Area (1=Urbano 2=Rural)','Grupo edad']).sum()
ine_proy_area_rm.reset_index(inplace=True)
ine_proy_area_rm.Region=13
ine_proy_area_rm.Provincia='Región Metropolitana'
ine_proy_area_rm['Nombre Provincia']='Región Metropolitana'
ine_proy_area_rm['Nombre Comuna']='Región Metropolitana'
ine_proy_area_rm['Comuna']='Región Metropolitana'
#%%
ine_proy_urb_rm_comuna=pd.concat([ine_proy_area_com,ine_proy_area_rm])
# %%
ine_proy_rm=pd.concat([ine_proy_com_rm,ine_proy_reg_rm])
ine_proy_rm.reset_index()
df_long = pd.melt(ine_proy_rm, 
                  id_vars=['Region', 'Nombre Region', 'Provincia', 'Nombre Provincia', 'Comuna', 'Nombre Comuna', 'Sexo (1=Hombre 2=Mujer)', 'Edad'], 
                  value_vars=[col for col in ine_proy_rm.columns if col.startswith('Poblacion')],
                  var_name='Año', 
                  value_name='Poblacion')
df_long['Año'] = df_long['Año'].str.extract('(\d+)').astype(int)

# df_long2 = pd.melt(ine_proy_urb_rm_comuna, 
#                   id_vars=['Region', 'Nombre Region', 'Provincia', 'Nombre Provincia', 'Comuna', 'Nombre Comuna', 'Sexo (1=Hombre 2=Mujer)', 'Edad'], 
#                   value_vars=[col for col in ine_proy_urb_rm_comuna.columns if col.startswith('Poblacion')],
#                   var_name='Año', 
#                   value_name='Poblacion')
# df_long2['Año'] = df_long2['Año'].str.extract('(\d+)').astype(int)
# %%
ine_proy_rm.to_csv('data_clean/INE_Proyecciones_RM.csv')
ine_proy_urb_rm_comuna.to_csv('data_clean/INE_Proyecciones_urbano_rural_RM.csv')
# df_long.to_csv('data_clean/INE_Proyecciones_RM_long.csv')
# df_long2.to_csv('data_clean/INE_Proyecciones_urbano_rural_RM_long.csv')

# %%
