# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 12:50:39 2019

@author: kocok
"""
#########################
#imported libraries
import numpy as np 
from sklearn.linear_model import LinearRegression
from sklearn import metrics
#########################
#funkction which fidns ix and iy indexes of grid
def getclosest_ij(nlats,nlons,latpt,lonpt):
    # find squared distance of every point on grid
    dist_sq = (nlats-latpt)**2 + (nlons-lonpt)**2  
    # 1D index of minimum dist_sq element
    minindex_flattened = dist_sq.argmin()    
    # Get 2D index for latvals and lonvals arrays from 1D index
    return np.unravel_index(minindex_flattened, nlats.shape)
#########################
# reg_funkcia returns coeficients a and c, pollutant (PM10,NO2...),error and PREDICT 
# hodnoty - which are values in points of measurement for all arrays in dic_polia.
def reg_funkcia(DF,dic_polia,dic_latlon): 
    #hodnoty (shape is same as measured pollutant)
    hodnoty={} 
    for q in dic_polia.keys():
        hodnota=[]
        for i,row in DF.iterrows():
            lat_x=row['lat_x']
            lon_x=row['lon_x']
            ix, iy = getclosest_ij(dic_latlon['LAT'],dic_latlon['LON'],lat_x,lon_x)
            hodnota.append(dic_polia[q][ix,iy])    
        hodnoty[q]=np.asarray(hodnota)
    # pollutant (PM10, NO2.... shape is the same as pollutant in DF )
    pollutant=np.array(DF['pollutant'])
    # X is a reshape type of values in grid point, in points which polutants was measured, this is neccesary for 
    # linear reggresion library sklearn
    X=[]
    for i in hodnoty.keys():
        xi=hodnoty[i].reshape(-1,1) 
        X.append(xi)  
    XH=np.hstack(X)
    #XH is special shape of X which is necessary for multivariable Linear regression
    y=np.log(pollutant)
    # model is linear reggresion fit
    model = LinearRegression().fit(XH, y)
    # a, c are coeficcients of linear reggresion model
    a=model.coef_
    c=model.intercept_
    # PREDICT is a predicted values in points of measurments, shape is the same as pollutant
    PREDICT=c
    suciny=[]
    for q in range (len(dic_polia.values())):
        suciny.append(list(hodnoty.values())[q]*a[q])
        PREDICT+=suciny[q]
    #evaluation of error (or residual), shape is the same as pollutant
    rmse=np.sqrt(metrics.mean_squared_error(np.log(pollutant),PREDICT))
    r2=metrics.r2_score(np.log(pollutant),PREDICT)
    mse=metrics.mean_squared_error(np.log(pollutant),PREDICT)
    mae=metrics.mean_absolute_error(np.log(pollutant),PREDICT)
    error=np.log(pollutant)-PREDICT   
    return a,c,pollutant,hodnoty,error,PREDICT,rmse,mse,mae,r2

# fmode lunkction returns MODELWI array of size (241,172)
def model_reg(DF,dic_polia,dic_latlon):
    """
    MODELWI (Model without interopolation) is array which is  c+ a1*'HT'(241,172)+a2*LUFRAC_01(241,172)+...... = MODELWI(241,172)
    this is only prediction values for all grid points, not only in points of polutants are measured.
    MODELWI is in simplicity prediction of linear reggresion model in array form.
    """
    a=reg_funkcia(DF,dic_polia,dic_latlon)[0]
    c=reg_funkcia(DF,dic_polia,dic_latlon)[1]
    
    MODELWI=c
    suciny=[]
    for i in range(a.shape[0]):
        # c+ a1*'HT'(241,172)+a2*LUFRAC_01(241,172)+...... = MODELWI(241,172)
        suciny.append(a[i]*list(dic_polia.values())[i])
        MODELWI+=suciny[i]
        
       
    return MODELWI, np.exp(MODELWI)


