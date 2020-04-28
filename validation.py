#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 09:40:59 2020

@author: p6001
"""
import regresia
import model_idw
import model_kriging
import numpy as np

def validation(DF,dic_polia,dic_latlon, model_type) :
    """
    leaving-one-out validation of linear reggresion model,
    linear reggresion model + idw interpolation of residulas,
    linear gergession model + kriging interpolation if residuals
    """
    
    print('###########################')
    print('leaving one validation for: ' + model_type)      
    
    predicted_value=[]# this is the list of arrays, each array has 1 station dropped.
    for i, row in DF.iterrows():
        DF1=DF.drop([i])
        ix, iy = regresia.getclosest_ij(dic_latlon['LAT'],dic_latlon['LON'],row['lat_x'],row['lon_x'] )
        if model_type == 'regresia + IDW':
           value = model_idw.idwmodel(DF1,dic_polia,dic_latlon)[2][ix,iy]
        elif model_type == 'regresia':
           value = regresia.model_reg(DF1,dic_polia,dic_latlon)[1][ix,iy]
        elif model_type == 'regresia + kriging':
            value = model_kriging.krigingmodel(DF1,dic_polia,dic_latlon)[2][ix,iy]
        predicted_value.append(value)  
        #print('EOI = {}, model = {}, measured = {} '.format(row['EOI'],value,row['pollutant']))
        #print('{}      {}      {}      {}'.format(row['name'], row['EOI'], value,  row['pollutant']))
    predicted_value=np.array(predicted_value)    
    RMSE=((np.sum((DF['pollutant']-predicted_value)**2))*(1/len((DF['pollutant']-predicted_value))))**0.5
    BIAS=np.sum((predicted_value-DF['pollutant']))/predicted_value.shape[0]
    r=np.corrcoef(predicted_value,DF['pollutant'] )[0,1]
    print('RMSE={}, BIAS={}, r={}'.format(RMSE,BIAS,r))
    
    