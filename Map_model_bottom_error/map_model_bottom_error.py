# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 13:45:11 2017
plot mean error,absolute mean error and rms of difference temperature between observe and model
@author: pengrui
"""
from matplotlib.mlab import griddata
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import netCDF4
from datetime import datetime, timedelta
import math
from turtleModule import str2ndlist,draw_basemap,whichArea

url='http://tds.marine.rutgers.edu/thredds/dodsC/roms/espresso/2009_da/his'
modData = netCDF4.Dataset(url)
modLons = modData.variables['lon_rho'][:]
modLats = modData.variables['lat_rho'][:] #the lon and lat are ROMS`s

obsData = pd.read_csv('tu94wModel.csv')
modTemp = pd.Series(str2ndlist(obsData['romsTemp'],bracket=True), index=obsData.index) # if str has '[' and ']', bracket should be True
obsTemp = pd.Series(str2ndlist(obsData['obstemp']), index=obsData.index)
obsDepth = pd.Series(str2ndlist(obsData['depth']), index=obsData.index)
depthBottom = pd.Series(obsData['depth_bottom'],index=obsData.index)
for i in obsData.index:
    if depthBottom[i]>200:
        depthBottom[i]=200     #Just a little points are deeper than 200m.Removing them can plot depth better
obsLon, obsLat = obsData['LON'], obsData['LAT']     #use for plotting depth line
modNearestIndex = pd.Series(str2ndlist(obsData['modNearestIndex'], bracket=True), index=obsData.index)
data = pd.DataFrame({'obstemp': obsTemp,'modtemp':modTemp, 
                     'nearestIndex': modNearestIndex,
                     'obsdepth':obsDepth,'moddepth':depthBottom},index=obsData.index)
  
lon_m=[]
lat_n=[]
dataNum = []
for i in range(82):  # just create a list with all zero to calculate error number 
    j=[0]*130
    dataNum.append(j)
sumdata = []                   #use for calculating mean error
for i in range(82):     # just create a list with all zero to calculate error number 
    j=[0]*130    
    sumdata.append(j)
abs_sumdata = []               #use for calculating absolulate mean error
for i in range(82):     # just create a list with all zero to calculate error number 
    j=[0]*130
    abs_sumdata.append(j)
rms=[]                         #use for calculating RMS
for i in range(82):     # just create a list with all zero to calculate error number 
    j=[0]*130    
    rms.append(j)

for i in data.index:
    m=int(data['nearestIndex'][i][0])
    n=int(data['nearestIndex'][i][1])   #find grid the point belong to.
    if abs(data['obsdepth'][i][-1]- data['moddepth'][i])<10:
                dataNum[m][n] += 1 
                
                diff=np.array(data['obstemp'][i][-1])-np.array(data['modtemp'][i][-1])
                sumdata[m][n] = sumdata[m][n]+diff
                
                absdiff=abs(np.array(data['obstemp'][i][-1])-np.array(data['modtemp'][i][-1]))
                abs_sumdata[m][n] = abs_sumdata[m][n]+absdiff
                
                dif=np.sum(diff*diff)
                rms[m][n]=rms[m][n]+dif 
mean=np.array(sumdata)/np.array(dataNum)            #calculate mean error
abs_mean=np.array(abs_sumdata)/np.array(dataNum)    #calculate absolulate mean error
rms=np.sqrt(np.array(rms)/np.array(dataNum))        #calculate rms

Mean=[]
Absmean=[]
Rms=[]
for i in range(82):
    for j in range(130):
        Mean.append(mean[i][j])
        Absmean.append(abs_mean[i][j])
        Rms.append(rms[i][j])
modLon=[]
modLat=[]
for i in range(len(modLons)):
    for j in range(len(modLons[i])):
        modLon.append(modLons[i][j])
        modLat.append(modLats[i][j])                #use for griddata

lonsize = [-79.5, -72.5]
latsize = [34.5, 41]                            #range of basemap
lon_i = np.linspace(lonsize[0],lonsize[1],1000)
lat_i = np.linspace(latsize[0],latsize[1],1000)  #use for mean error,absolute mean error and rms

lon_is = np.linspace(lonsize[0],lonsize[1],100)
lat_is = np.linspace(latsize[0],latsize[1],100)  #use for depth line
mean_i = griddata(np.array(modLon),np.array(modLat),np.array(Mean),lon_i,lat_i,interp='linear')
abs_mean_i=griddata(np.array(modLon),np.array(modLat),np.array(Absmean),lon_i,lat_i,interp='linear')
RMS_i=griddata(np.array(modLon),np.array(modLat),np.array(Rms),lon_i,lat_i,interp='linear')
depth_i=griddata(np.array(obsLon),np.array(obsLat),np.array(depthBottom),lon_is,lat_is,interp='linear')
temp_i=[mean_i,abs_mean_i,RMS_i]
title=['mean_error','abs_mean_error','rms']   # use for loop
for k in range(len(title)):
    if k==0:    #plot mean error
        fig = plt.figure()
        ax = fig.add_subplot(111)
        draw_basemap(fig, ax, lonsize, latsize)
        CS = plt.contourf(lon_i, lat_i, temp_i[k], np.arange(temp_i[k].min(),temp_i[k].max()+0.1,0.1), cmap=plt.cm.bwr,
                  vmax=temp_i[k].max(), vmin=temp_i[k].min())
        CS1=plt.contour(lon_is, lat_is,depth_i,1,colors = 'r',linestyles='--')  #plot 100m depth
        ax.annotate('100m depth',color='r',fontsize=8,xy=(-75.289,35.0395),xytext=(-74.7034,34.9842),arrowprops=dict(color='r',arrowstyle="->",connectionstyle="arc3"))
        cbar=plt.colorbar(CS,ticks=[-6,-4,-2,0,2,4,6])
        cbar.ax.tick_params(labelsize=10) 
        cbar.set_label('temperature difference',fontsize=12, rotation=90)
        #plt.scatter(np.array(obsLon),np.array(obsLat), marker='o', c='b', s=1, zorder=1)
        plt.title('bottom:'+title[k],fontsize=16)
        plt.savefig('bottom:'+title[k]+'.png',dpi=200)
    if k>0:    #plot absolute mean error and RMS
        fig = plt.figure()
        ax = fig.add_subplot(111)
        draw_basemap(fig, ax, lonsize, latsize)
        CS = plt.contourf(lon_i, lat_i, temp_i[k], np.arange(temp_i[k].min(),temp_i[k].max()+0.1,0.1), cmap=plt.cm.bwr,
                  vmax=temp_i[k].max(), vmin=temp_i[k].min())
        CS1=plt.contour(lon_is, lat_is,depth_i,1,colors = 'r',linestyles='--')  #plot 100m depth
        ax.annotate('100m depth',color='r',fontsize=8,xy=(-75.289,35.0395),xytext=(-74.7034,34.9842),arrowprops=dict(color='r',arrowstyle="->",connectionstyle="arc3"))
        cbar=plt.colorbar(CS,ticks=[1,2,3,4,5,6,7,8])
        cbar.ax.tick_params(labelsize=10)
        cbar.set_label('temperature difference',fontsize=12, rotation=90)
        #plt.scatter(np.array(obsLon),np.array(obsLat), marker='o', c='b', s=1, zorder=1)
        plt.title('bottom:'+title[k],fontsize=16)
        plt.savefig('bottom:'+title[k]+'.png',dpi=200)   
plt.show()
