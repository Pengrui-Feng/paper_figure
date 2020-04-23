!pip install netCDF4
# routine to test "getfvcom" function
# Written by Pengrui in early 2020 derived from other's code
# Modified by JiM to add comments and rename from "get_model_temp.py" to "get_fvcom_model_temp.py"
from datetime import datetime as dt
from datetime import timedelta as td
from dateutil import parser
import pandas as pd
import numpy as np
import netCDF4
import sys



def nearlonlat(lon,lat,lonp,latp): # needed for the next function get_FVCOM_bottom_temp
    """
    i=nearlonlat(lon,lat,lonp,latp) change
    find the closest node in the array (lon,lat) to a point (lonp,latp)
    input:
        lon,lat - np.arrays of the grid nodes, spherical coordinates, degrees
        lonp,latp - point on a sphere
        output:
            i - index of the closest node
            For coordinates on a plane use function nearxy           
            Vitalii Sheremet, FATE Project  
    """
    cp=np.cos(latp*np.pi/180.)
    # approximation for small distance
    dx=(lon-lonp)*cp
    dy=lat-latp
    dist2=dx*dx+dy*dy
    i=np.argmin(dist2)
    return i

def get_FVCOM_url(dtime):
    """dtime: the formate of time is datetime"""
    # get fvcom url based on time wanted
    dtime=dt.strptime(dtime,'%Y-%m-%d %H:%M:%S')
    if (dtime-dt.now())>td(days=-2):
        url='http://www.smast.umassd.edu:8080/thredds/dodsC/FVCOM/NECOFS/Forecasts/NECOFS_GOM3_FORECAST.nc' 
    elif dtime>=dt(2016,7,1):
        url='http://www.smast.umassd.edu:8080/thredds/dodsC/models/fvcom/NECOFS/Archive/NECOFS_GOM/2019/gom4_201907.nc'
        url=url.replace('201907',dtime.strftime('%Y%m'))
        url=url.replace('2019',dtime.strftime('%Y'))
    elif dtime<=dt(2016,1,1):
        url = 'http://www.smast.umassd.edu:8080/thredds/dodsC/fvcom/hindcasts/30yr_gom3'
    else:
        url=np.nan
    return url

def get_FVCOM_temp(lati,loni,dtime,depth): # gets modeled temp using GOM3 forecast
        '''
        Taken primarily from Rich's blog at: http://rsignell-usgs.github.io/blog/blog/2014/01/08/fvcom/ on July 30, 2018
        where lati and loni are the position of interest, dtime is the datetime, and depth is "99999" for bottom
        '''
        urlfvcom=get_FVCOM_url(dtime)
        nc = netCDF4.Dataset(urlfvcom).variables
        #first find the index of the grid 
        lat = nc['lat'][:]
        lon = nc['lon'][:]
        inode = nearlonlat(lon,lat,loni,lati)
        #second find the index of time
        time_var = nc['time']
        dtime=dt.strptime(dtime,'%Y-%m-%d %H:%M:%S')
        itime = netCDF4.date2index(dtime,time_var,select='nearest')# where startime in datetime
        # figure out layer from depth
        w_depth=nc['h'][inode]
        #print(w_depth)
        if depth >= w_depth: # for bottom
            layer=-1
        else:
            layer=int(round(depth/w_depth*45.))
        #print(layer)
        '''
        return nc['temp'][itime,layer,inode]
        '''
        try:
            fvcom_temp = nc['temp'][itime,layer,inode]
            return fvcom_temp
        except:
            fvcom_temp = nc['temp'][itime,-1,inode]
            return fvcom_temp
        
time1='2012-8-12 12:0:0'
time2='2012-6-3 1:0:0'
time3='2013-6-24 19:0:0'
lat1,lon1 = 38.47,-74.38
lat2,lon2 = 37.18,-74.94
lat3,lon3 = 36.0,	-75.17

ftemp = []
for i in range(1,30):
    depth= i
    f = get_FVCOM_temp(lat3,lon3,time3,depth)
    ftemp.append(f)

np.array(ftemp)
