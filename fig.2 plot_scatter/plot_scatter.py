# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 09:36:10 2019

@author: pengrui
"""
#from scipy.interpolate import griddata
from matplotlib.pylab import *
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import glob
from mpl_toolkits.basemap import Basemap
def draw_basemap(fig, ax, lonsize, latsize, interval_lon=2, interval_lat=2):
    ax = fig.sca(ax)
    dmap = Basemap(projection='cyl',
                   llcrnrlat=min(latsize)-0.01,
                   urcrnrlat=max(latsize)+0.01,
                   llcrnrlon=min(lonsize)-0.01,
                   urcrnrlon=max(lonsize)+0.01,
                   resolution='h',ax=ax)
    dmap.drawparallels(np.arange(int(min(latsize)),
                                 int(max(latsize))+1,interval_lat),
                       labels=[1,0,0,0], linewidth=0,fontsize=20)
    dmap.drawmeridians(np.arange(int(min(lonsize))-1,
                                 int(max(lonsize))+1,interval_lon),
                       labels=[0,0,0,1], linewidth=0,fontsize=20)
    dmap.drawcoastlines()
    dmap.fillcontinents(color='grey')
    dmap.drawmapboundary()

path='/content/drive/My Drive/'
csv_list = glob.glob('*_merge_td_gps.csv')  # search csv files in current folder
print('%s csvfiles searched in total'% len(csv_list))
print('processing............')
lonsize = [-79.5, -70.5]
latsize = [34, 41]
fig =plt.figure()
ax = fig.add_subplot(111)
for i in csv_list: #i is a filename which is processed
    df = pd.read_csv(i)
    lat=df['lat_gps']
    lon=df['lon_gps']
    plt.scatter(lon, lat,s=15,c='y')  #  
draw_basemap(fig, ax, lonsize, latsize, interval_lon=2, interval_lat=2)    
waterData=pd.read_csv('depthbottom.csv')
wd=waterData['depth_bottom'].dropna()
Lat=waterData['lat'].dropna()
Lon=waterData['lon'].dropna()
'''
lon_is = np.linspace(lonsize[0],lonsize[1],150)
lat_is = np.linspace(latsize[0],latsize[1],150)  #use for depth line
depth_i=griddata(np.array(lon),np.array(lat),np.array(wd),lon_is,lat_is,method='linear')
cs=plt.contour(lon_is, lat_is,depth_i,levels=[70],colors = 'r',linewidths=2,linestyles='--')  #plot 100m depth
ax.annotate('70m water depth',xy=(-75.7089,34.5195),xytext=(-75.0034,34.0842),arrowprops=dict(facecolor='black'))
#plt.clabel(cs,'%.0f'%70.000,fmt='%s %m',inline=True,colors='k',fontsize=10)#fmt='%2.1d'
'''
lon_is = np.linspace(lonsize[0],lonsize[1],150)
lat_is = np.linspace(latsize[0],latsize[1],150)  #use for depth line
depth_i=griddata(np.array(Lon),np.array(Lat),np.array(wd),lon_is,lat_is,methond='linear')
cs=plt.contour(lon_is, lat_is,depth_i,levels=[70],colors = 'r',linewidths=1,linestyles='--')  #plot 100m depth
ax.annotate('70m water depth',color='r',fontsize=6,xy=(-73.2089,38.905),xytext=(-73.3034,38.5042),arrowprops=dict(color='red',arrowstyle="->",
                                connectionstyle="arc3"))#xy=(-73.5089,38.505),xytext=(-73.7034,38.0042)


plt.title('Positions of turtle profiles after quality control checks', fontsize=10)
plt.legend(loc='lower right',fontsize = 'x-small')
plt.savefig('turtle_map_new',dpi=200)
plt.show()
'''
plt.title('%s_scatterplot')#('%s profiles(%s~%s)'% (e,obsTime[0],obsTime[-1]))
#plt.legend(loc='lower right',ncol=2,fontsize = 'xx-small')
#plt.savefig(path+'_ScatterPlot.png',dpi=200)
plt.show()  
'''
