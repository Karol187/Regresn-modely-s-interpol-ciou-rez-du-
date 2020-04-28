# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 16:40:49 2019

@author: kocok
"""
############################
#Import libraries
#############

import numpy as np
import regresia

#import time
############################

def getclosest_ij(nlats,nlons,latpt,lonpt):# funkcia ktora najde i,j, index mriezky v 2D poliach latudude a Lontitude
    # find squared distance of every point on grid
    dist_sq = (nlats-latpt)**2 + (nlons-lonpt)**2  
    # 1D index of minimum dist_sq element
    minindex_flattened = dist_sq.argmin()    
    # Get 2D index for latvals and lonvals arrays from 1D index
    return np.unravel_index(minindex_flattened, nlats.shape)
##############################
#IDW INTERPOLATION FUNKCTION
#############################
# Distance calculation, degree to km (Haversine method)
def harvesine(lon1, lat1, lon2, lat2):
    #start_time_of_harvesine = time.time()
    rad = np.pi / 180  # degree to radian
    R = 6378.1 
    dlon = (lon2 - lon1) * rad
    dlat = (lat2 - lat1) * rad
    a = (np.sin(dlat / 2)) ** 2 + np.cos(lat1 * rad) * \
        np.cos(lat2 * rad) * (np.sin(dlon / 2)) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    d = R * c
    #print('Harvesine {0:.3f}'.format(time.time() - start_time_of_harvesine))
    return(d)
# ------------------------------------------------------------
# IDW
def idwr(y, x, z, yi, xi):
    """
    inputs:
    x, y : lat_x, lon_x from dataframe upravene na mriezky  
    z : error concentrations of pollutant
    xi, yi : 1-D array of lon and lat 
    return 
    """
    d=np.array(list(map(lambda y,x: harvesine(y, x, yi, xi),y,x)))
    IDW = np.matmul(z,1/d**2)/np.sum(1/d**2,axis=0)

    return IDW;

################################    
#     
def idwmodel(DF,dic_polia,dic_latlon): 
    #start_time_of_gmodel = time.time()
    # MODELWI is model without interpolation of shape, it is an array of shape (142,271)
    MODELWI=regresia.model_reg(DF,dic_polia,dic_latlon)[0] 
    # ERROR is caculated as pollutant minus PREDICT, it has shape same as measured pollutant (32)
    ERROR_stanice=regresia.reg_funkcia(DF,dic_polia,dic_latlon)[4]  
   
    
    x,y,z = list(DF['lat_x']),list(DF['lon_x']),ERROR_stanice
    
    #xi,yi are new grid coordinates
    xi=dic_latlon['LAT'].flatten()
    yi=dic_latlon['LON'].flatten()
    IDW_ERROR=np.asarray(idwr(y,x,z,yi,xi))
    IDW_ERROR= np.reshape(IDW_ERROR,(142,271))
    
    # adding pollutant values to interpolated errror array (IDW_ERROR) which shape is (142,271)
    
    for i in range(0,len(x)):
        ix, iy = getclosest_ij(dic_latlon['LAT'],dic_latlon['LON'],x[i],y[i])
        IDW_ERROR[ix,iy]=ERROR_stanice[i]
        
    #KOMPLET_MODEL is linear reggresion predict MODELWI plus IDW of residuals
    KOMPLET_MODEL=IDW_ERROR+MODELWI
    #print('gmodel {0:.3f}'.format(time.time() - start_time_of_gmodel))
    return KOMPLET_MODEL, IDW_ERROR, np.exp(KOMPLET_MODEL), np.exp(IDW_ERROR)
