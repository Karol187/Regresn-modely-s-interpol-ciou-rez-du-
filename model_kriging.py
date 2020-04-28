# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 22:03:12 2020

@author: kocok
"""

import numpy as np
import regresia
from pykrige.ok import OrdinaryKriging

def getclosest_ij(nlats,nlons,latpt,lonpt):# funkcia ktora najde i,j, index mriezky v 2D poliach latudude a Lontitude
    # find squared distance of every point on grid
    dist_sq = (nlats-latpt)**2 + (nlons-lonpt)**2  
    # 1D index of minimum dist_sq element
    minindex_flattened = dist_sq.argmin()    
    # Get 2D index for latvals and lonvals arrays from 1D index
    return np.unravel_index(minindex_flattened, nlats.shape)

################################    
#     
def krigingmodel(DF,dic_polia,dic_latlon): 
    #start_time_of_gmodel = time.time()
    # MODELWI is model without interpolation of shape, it is an array of shape (142,271)
    MODELWI=regresia.model_reg(DF,dic_polia,dic_latlon)[0] 
    # ERROR is caculated as pollutant minus PREDICT, it has shape same as measured pollutant (32)
    ERROR_stanice=regresia.reg_funkcia(DF,dic_polia,dic_latlon)[4]  
    
    x,y,z = list(DF['lon_x']),list(DF['lat_x']),ERROR_stanice
    #xi,yi are new grid coordinates
    xi=np.linspace(np.min(dic_latlon['LON'].flatten()), np.max(dic_latlon['LON'].flatten()), 271)
    yi=np.linspace(np.min(dic_latlon['LAT'].flatten()), np.max(dic_latlon['LAT'].flatten()), 142)
    
    # OK is kriging funkction 
    OK = OrdinaryKriging(x, y, z, variogram_model='spherical')
    """
    OK: is kriging funkction form pykrige package 
    x, y: are latitude and lontitude of measured concentrations from DF(dataframe)
    z : error concentrations of pollutant, from linear regresion model
    variogram model: is tzpe of theoretical variogram
    """
    # z1 is kriging interpolation array 
    z1, ss1 = OK.execute('grid', xi, yi)
    """
    z1: is interpolated array realised on grid 
    xi, yi: are new grid coordinates
    """
    KRIGING_ERROR=z1
    #KOMPLET_MODEL is linear reggresion predict MODELWI plus kriging of residuals
    KOMPLET_MODEL=KRIGING_ERROR+MODELWI
    return KOMPLET_MODEL, KRIGING_ERROR, np.exp(KOMPLET_MODEL), np.exp(KRIGING_ERROR)

    