# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 20:56:00 2019

@author: kocok
"""
###############################
#imported lybraries
import numpy as np
import pandas as pd
import netCDF4



#########
#imported modules

import mapy
import validation
import regresia


#########
#inputs 
#########
#import dataframe DF with flexible heads
DF=pd.read_csv(r"C:\Users\kocok\Desktop\Bakalarska praca hlavne programy\inputs\tabulka_surova_PM10.csv",delimiter=',')
#DF=pd.read_csv(r"C:\Users\kocok\Desktop\Bakalarska praca hlavne programy\inputs\tabulka_surova_NO2_2017.csv",delimiter=',')
DF['pollutant']=DF['PM10']
DF['lat_x']=DF['lat_x']
DF['lon_x']=DF['lon_x']
name='PM$_{10}$'
#name='NO$_{2}$'
###############################
# get netcdf4 dataset as f
f = netCDF4.Dataset(r"C:\Users\kocok\Desktop\Bakalarska praca hlavne programy\inputs\GRIDCRO2D_2017-01-01.nc") 
#########
#get dictonary, which contain arrays of different supplementary quantities of shape (241,172), arrays are 2D
dic_polia={}
for i in list(f.variables.keys()):
    if i not in ['MSFX2','TFLAG','LWMASK', 'LAT', 'LON','LUFRAC_07','LUFRAC_11','LUFRAC_24','LUFRAC_23','LUFRAC_22','LUFRAC_21','LUFRAC_20','LUFRAC_19','LUFRAC_18','LUFRAC_17','LUFRAC_15','LUFRAC_14','LUFRAC_13','LUFRAC_12','LUFRAC_10','LUFRAC_09','LUFRAC_08','LUFRAC_04','LUFRAC_03']: 
    #if i not in ['MSFX2','TFLAG','LWMASK', 'LAT', 'LON','LUFRAC_11']:
    #if i in ['HT', 'LUFRAC_06']:   
       dic_polia[i]=np.array(f.variables[i][0,0,:,:])
dic_polia['TOTALPM10']=np.float32(np.load(r"C:\Users\kocok\Desktop\Bakalarska praca hlavne programy\inputs\total_PM10.npy"))
#dic_polia['TOTALNO2']=np.float32(np.load(r"C:\Users\kocok\Desktop\Bakalarska praca hlavne programy\inputs\total_NO2.npy"))
dic_polia['HUSTOTA_OBYVATELSTVA']=np.float32(np.load(r"C:\Users\kocok\Desktop\Bakalarska praca hlavne programy\inputs\HUSTOTA_OBYVATELSTVA.npy"))
dic_polia['mapa_pm10_v6']=np.float32(np.load(r"C:\Users\kocok\Desktop\Bakalarska praca hlavne programy\inputs\mapa_pm10_v6.npy"))
########
# get disctonary, which contains LAT an LON arrays of shape (241,172), arrays are 2D
dic_latlon={}
for i in list(f.variables.keys()):
    if i in ['LAT','LON']:
       dic_latlon[i]=np.array(f.variables[i][0,0,:,:])
#############################################################################################
#USPORIADANIE POLI PODLA NAJMENSEJ RMSE RESPEKTIVE NAJVACSEJ KORELACIE S NAMERANYM PM10   
#############################################################################################       
zoznam_rmse=[]
zoznam_keys=[]
for i in dic_polia.keys():
    dic_x={i:dic_polia[i]}
    print('key={}, a={}, c={}, rmse={},mse={},mae={},r2={}'.format(i,regresia.reg_funkcia(DF,dic_x,dic_latlon)[0],regresia.reg_funkcia(DF,dic_x,dic_latlon)[1],regresia.reg_funkcia(DF,dic_x,dic_latlon)[6],regresia.reg_funkcia(DF,dic_x,dic_latlon)[7],regresia.reg_funkcia(DF,dic_x,dic_latlon)[8],regresia.reg_funkcia(DF,dic_x,dic_latlon)[9]))
    zoznam_rmse.append(regresia.reg_funkcia(DF,dic_x,dic_latlon)[6])
    zoznam_keys.append(i)  
dic_pairs=dict(zip(zoznam_keys, zoznam_rmse))
from operator import itemgetter
from collections import OrderedDict 
dic_sorted_pairs = OrderedDict(sorted(dic_pairs.items(), key=lambda t: t[1]))
print('#################################################################')
for k,v in dic_sorted_pairs.items():
    print('key={}, rmse={}'.format(k,v))
print('#################################################################')
#############################################################################################
#VSETKY POLIA ZORADENE PODLA RMSE RESPEKTIVE NAJVACSEJ KORELACIE S NAMERANYM PM10
#############################################################################################

zoradeny_dict = OrderedDict(sorted(dic_polia.items(), key=lambda x: dic_sorted_pairs.get(x[0])))
print('#################################################################')
print('Mapa obsahuje vsetky polia={}'.format(zoradeny_dict.keys()))
#print('Logaritmický regresný model (typ log-linear regression model) a jeho parametre')
#print('keys={}, koeficieny_a1...an={}, c={}'.format(zoradeny_dict.keys(),regresia.reg_funkcia(DF,zoradeny_dict,dic_latlon)[0],regresia.reg_funkcia(DF,zoradeny_dict,dic_latlon)[1]))
#mapy.mapy(DF,zoradeny_dict,dic_latlon,name)
mapy.lnmapy(DF,zoradeny_dict,dic_latlon,name)
#mapy.lnmapy_error(DF,zoradeny_dict,dic_latlon)
#print('Cross-Validácia, transformácia interpolovaných polí na exp')
#validation.validation(DF,zoradeny_dict,dic_latlon, model_type='regresia + IDW')
#validation.validation(DF,zoradeny_dict,dic_latlon, model_type='regresia')
#validation.validation(DF,zoradeny_dict,dic_latlon, model_type='regresia + kriging')
print('#################################################################')
#############################################################################################
#POSTUPNE PRIDAVA POLIA, RESP. VYPUSTA PODLA RMSE
#############################################################################################      
for key in reversed(list(zoradeny_dict.keys())):
    if len(list(zoradeny_dict.keys())) == 1:
         break 
    else:
          del zoradeny_dict[key]
          print('#################################################################')
          #print('Logaritmický regresný model (typ log-linear regression model) a jeho parametre')
          #print('keys={}, koeficieny_a1...an={}, c={}'.format(zoradeny_dict.keys(),regresia.reg_funkcia(DF,zoradeny_dict,dic_latlon)[0],regresia.reg_funkcia(DF,zoradeny_dict,dic_latlon)[1]))
          print('Mapa obsahuje nasledovné polia={}'.format(zoradeny_dict.keys()))
          #mapy.mapy(DF,zoradeny_dict,dic_latlon,name)
          mapy.lnmapy(DF,zoradeny_dict,dic_latlon,name)
          #mapy.lnmapy_error(DF,zoradeny_dict,dic_latlon)
          #print('Mapa obsahuje nasledovné polia={}'.format(zoradeny_dict.keys()))
          #print('Cross-Validácia, transformácia interpolovaných polí na exp')
          #validation.validation(DF,zoradeny_dict,dic_latlon, model_type='regresia + IDW')
          #validation.validation(DF,zoradeny_dict,dic_latlon, model_type='regresia')
          #validation.validation(DF,zoradeny_dict,dic_latlon, model_type='regresia + kriging')




























