# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 20:56:00 2019

@author: kocok
"""
###############################
#imported lybraries
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap



#########
#imported modules
import regresia
import model_idw
import model_kriging
# setting of basemap
plt.rcParams['figure.figsize'] =20,7
meridians = np.arange(16.,35.,1.)
pararels = np.arange(46.,50.,1.)
d03={'projection': 'lcc',
     'llcrnrlon': 16.804249173287925,
     'llcrnrlat': 47.67911406210376,
     'urcrnrlon': 22.66823971637524,
     'urcrnrlat': 49.53739914689373,
     'resolution': 'i',
     'lat_1': 46.24470138549805,
     'lat_2': 46.24470138549805,
     'lat_0': 46.24470138549805,
     'lon_0': 17.0,
     'rsphere': 6370000.0}
mapb=Basemap(**d03)

def mapy(DF,dic_polia,dic_latlon,name):
    """
    mapy is funkction which produce prediction maps transformed from ln(pollutant) to pollutant of linear reggresion in 3 forms:
    1) only prediction of linear reggresion
    2) prediction of linear reggresion + kriging interpolation of residuals
    3) prediction of linear reggresion + idw interpolation of residuals
    """
    ################################
    
    for i in (regresia.model_reg(DF,dic_polia,dic_latlon)[1],model_idw.idwmodel(DF,dic_polia, dic_latlon)[2],model_kriging.krigingmodel(DF,dic_polia, dic_latlon)[2]): 
         mapb.drawcountries()
         mapb.pcolormesh(dic_latlon['LON'],dic_latlon['LAT'],i,cmap=plt.cm.jet,latlon=True) 
         mapb.readshapefile('C:/Users/kocok/Desktop/Shapefile0/slovensko','slovensko', drawbounds= True,linewidth=4)
         if i in regresia.model_reg(DF,dic_polia,dic_latlon)[1]:
             plt.colorbar(label=name+' [$\mu$g.$m^{-3}$]',extend='max')
             plt.title('Koncentrácia ' +name+ ' za rok 2017 (lineárna regresia)',fontsize=15)
             plt.clim(0,40)
             mapb.scatter(DF['lon_x'].values, DF['lat_x'].values,c=DF['pollutant'].values,s=30 , latlon=True,cmap='jet',alpha=1, edgecolors='black')
             plt.clim(0,40)
             #plt.show() 
             plt.savefig('lnNO2 expregresia {}.png'.format(len(dic_polia.keys())),bbox_inches='tight',dpi=600)
             plt.clf()
         elif i in model_kriging.krigingmodel(DF,dic_polia,dic_latlon)[2]:
             plt.colorbar(label=name+ ' [$\mu$g.$m^{-3}$]',extend='max')
             plt.clim(0,40)
             plt.title('Koncentrácia '+name+' za rok 2017 (lineárna regresia + OK interpolácia rezíduí)',fontsize=15)
             mapb.scatter(DF['lon_x'].values, DF['lat_x'].values,c=DF['pollutant'].values,s=30 , latlon=True,cmap='jet',alpha=1, edgecolors='black')
             plt.clim(0,40)
             #plt.show()
             plt.savefig('lnNO2 expregresia+ok pocet poli {}.png'.format(len(dic_polia.keys())),bbox_inches='tight',dpi=600)
             plt.clf()
         else:
             plt.colorbar(label=name+ ' [$\mu$g.$m^{-3}$]',extend='max')  
             plt.clim(0,40)
             plt.title('Koncentrácia '+name+' za rok 2017 (lineárna regresia + IDW interpolácia rezíduí)',fontsize=15)
             mapb.scatter(DF['lon_x'].values, DF['lat_x'].values,c=DF['pollutant'].values,s=30 , latlon=True,cmap='jet',alpha=1, edgecolors='black')
             plt.clim(0,40)
             #plt.show()
             plt.savefig('lnNO2 expregresia+idw pocet poli {}.png'.format(len(dic_polia.keys())),bbox_inches='tight',dpi=600)
             plt.clf()
 

def lnmapy(DF,dic_polia,dic_latlon,name):
    """
    lnmapy is funkction which produce prediction maps of ln(pollutant) in 3 forms:
    1) only prediction of linear reggresion
    2) prediction of linear reggresion + kriging interpolation of residuals
    3) prediction of linear reggresion + idw interpolation of residuals
    """
    ##################################
    for i in (regresia.model_reg(DF,dic_polia,dic_latlon)[0],model_idw.idwmodel(DF,dic_polia, dic_latlon)[0],model_kriging.krigingmodel(DF,dic_polia, dic_latlon)[0]):   
        mapb.drawcountries()
        mapb.pcolormesh(dic_latlon['LON'],dic_latlon['LAT'],i,cmap=plt.cm.jet,latlon=True) 
        mapb.readshapefile('C:/Users/kocok/Desktop/Shapefile0/slovensko','slovensko', drawbounds= True,linewidth=4)
        if i in regresia.model_reg(DF,dic_polia,dic_latlon)[0]:
            plt.colorbar(label='ln('+name+')[$\mu$g.$m^{-3}$]',extend='both')
            plt.clim(0,np.log(40))
            plt.title('Koncentrácia ln('+name+') za rok 2017 (lineárna regresia)',fontsize=15)
            mapb.scatter(DF['lon_x'].values, DF['lat_x'].values,c=np.log(DF['pollutant'].values),s=30 , latlon=True,cmap='jet',alpha=1, edgecolors='black')
            plt.clim(0,np.log(40))
            #plt.show() 
            plt.savefig('lnPM10 regresia {}.png'.format(len(dic_polia.keys())),bbox_inches='tight',dpi=600)
            plt.clf()
        elif i in model_kriging.krigingmodel(DF,dic_polia,dic_latlon)[0]:
             plt.colorbar(label='ln('+name+')[$\mu$g.$m^{-3}$]',extend='both')
             plt.clim(0,np.log(40))            
             plt.title('Koncentrácia ln('+name+') za rok 2017 (lineárna regresia + OK interpolácia rezíduí)',fontsize=15)
             mapb.scatter(DF['lon_x'].values, DF['lat_x'].values,c=np.log(DF['pollutant'].values),s=30 , latlon=True,cmap='jet',alpha=1, edgecolors='black')
             plt.clim(0,np.log(40))
             #plt.show()  
             plt.savefig('lnPM10 regresia+ok pocet poli {}.png'.format(len(dic_polia.keys())),bbox_inches='tight',dpi=600)
             plt.clf()
        else:
            plt.colorbar(label='ln('+name+')[$\mu$g.$m^{-3}$]',extend='both')
            plt.clim(0,np.log(40))           
            plt.title('Koncentrácia ln('+name+') za rok 2017 (lineárna regresia + IDW interpolácia rezíduí)',fontsize=15)
            mapb.scatter(DF['lon_x'].values, DF['lat_x'].values,c=np.log(DF['pollutant'].values),s=30 , latlon=True,cmap='jet',alpha=1, edgecolors='black')
            plt.clim(0,np.log(40))
            #plt.show()  
            plt.savefig('lnPM10 regresia+idw pocet poli {}.png'.format(len(dic_polia.keys())),bbox_inches='tight',dpi=600)
            plt.clf()

def lnmapy_error(DF,dic_polia,dic_latlon):
    """
    lnmapy_error is funkction which produce prediction maps interpolated residuals in 2 forms:
    1) idw interpolation of residuals calculated from linear regression
    2) kriging interpolation of residuals calculated from linear regression
    """
    ######################################
    for i in (model_idw.idwmodel(DF,dic_polia, dic_latlon)[1], model_kriging.krigingmodel(DF,dic_polia, dic_latlon)[1]):
        mapb.drawcountries()
        mapb.pcolormesh(dic_latlon['LON'],dic_latlon['LAT'],i,cmap=plt.cm.jet,latlon=True) 
        mapb.readshapefile('C:/Users/kocok/Desktop/Shapefile0/slovensko','slovensko', drawbounds= True,linewidth=4)
        
        if i in model_idw.idwmodel(DF,dic_polia, dic_latlon)[1]:
            plt.colorbar(label='Hodnoty rezíduí [$\mu$g.$m^{-3}$]')
            plt.title('IDW interpolácia rezíduí',fontsize=15)
            plt.clim(min(regresia.reg_funkcia(DF,dic_polia,dic_latlon)[4]),max(regresia.reg_funkcia(DF,dic_polia,dic_latlon)[4]))
            mapb.scatter(DF['lon_x'].values, DF['lat_x'].values,c=regresia.reg_funkcia(DF,dic_polia,dic_latlon)[4],s=30 , latlon=True,cmap='jet',alpha=1, edgecolors='black')
            #plt.show() 
            plt.savefig('lnidw res {}.png'.format(len(dic_polia.keys())),bbox_inches='tight',dpi=600)           
            plt.clf()
        else:
            plt.colorbar(label='Hodnoty rezíduí [$\mu$g.$m^{-3}$]')
            plt.title('OK interpolácia rezíduí',fontsize=15)
            plt.clim(min(regresia.reg_funkcia(DF,dic_polia,dic_latlon)[4]),max(regresia.reg_funkcia(DF,dic_polia,dic_latlon)[4]))
            mapb.scatter(DF['lon_x'].values, DF['lat_x'].values,c=regresia.reg_funkcia(DF,dic_polia,dic_latlon)[4],s=30 , latlon=True,cmap='jet',alpha=1, edgecolors='black')
            #plt.show()
            plt.savefig('lnok res {}.png'.format(len(dic_polia.keys())),bbox_inches='tight',dpi=600)           
            plt.clf()
        
    