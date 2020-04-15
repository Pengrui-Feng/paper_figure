!pip install netCDF4
# routine to test "getfvcom" function
from datetime import datetime as dt
from datetime import timedelta as td
from dateutil import parser
import pandas as pd
import numpy as np
import netCDF4
import sys

time1='2012-8-12 12:0:0'
time2='2012-6-3 1:0:0'
time3='2018-9-15 0:0:0'
lat1,lon1 = 38.47,-74.38
lat2,lon2 = 37.18,-74.94
lat3,lon3 = 40.55,-72.5

ftemp = []
etemp = []
for i in range(1,42):
    depth= i
    f = get_FVCOM_temp(lat3,lon3,time3,depth)
    #e = get_espresso_temp(time3,lat3,lon3,depth)
    e=get_doppio(lat3,lon3,time3,depth)
    #fetemp.append(f)
    etemp.append(e)

np.array(etemp)



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
def get_doppio_url(date):
    url='http://tds.marine.rutgers.edu/thredds/dodsC/roms/doppio/2017_da/his/runs/History_RUN_2018-11-12T00:00:00Z'
    return url.replace('2018-11-12',date)

#get_doppio no fitting
def get_doppio(lat,lon,time,depth):
    """
    notice:
        the format of time is like "%Y-%m-%d %H:%M:%S"
        the default depth is under the bottom depth
    the module only output the temperature of point location
    """
    time=dt.strptime(time,'%Y-%m-%d %H:%M:%S') # transform time format
    if (time -datetime.datetime(2017,11,1,0,0,0)).total_seconds()<0:
        print('the date can\'t be earlier than 2017-11-1')
        return np.nan
    
    url_time=time.strftime('%Y-%m-%d')#
    url=get_doppio_url(url_time)
    nc=netCDF4.Dataset(url).variables
    #first find the index of the grid 
    lons=nc['lon_rho'][:]
    lats=nc['lat_rho'][:]
    temp=nc['temp']
    #second find the index of time
    doppio_time=nc['time']
    itime = netCDF4.date2index(time,doppio_time,select='nearest')# where startime in datetime
    # figure out layer from depth
    
    min_distance=dist(lat1=lat,lon1=lon,lat2=lats[0][0],lon2=lons[0][0])   
    index_1,index_2=0,0
    for i in range(len(lons)):
        for j in range(len(lons[i])):
            if min_distance>dist(lat1=lat,lon1=lon,lat2=lats[i][j],lon2=lons[i][j]):
                min_distance=dist(lat1=lat,lon1=lon,lat2=lats[i][j],lon2=lons[i][j])
                index_1=i
                index_2=j
    
    doppio_depth=nc['h'][index_1][index_2]
    
    if depth > doppio_depth:# case of bottom
            S_coordinate=1
    else:
        S_coordinate=float(depth)/float(doppio_depth)
    if 0<=S_coordinate<1:
        doppio_temp=temp[itime,39-int(S_coordinate/0.025),index_1,index_2]# because there are 0.025 between each later
    elif S_coordinate==1:
        doppio_temp=temp[itime][0][index_1][index_2]
    else:
        doppio_temp=temp[itime][0][index_1][index_2]
    return doppio_temp
def get_espresso_temp(time,lat,lon,depth) :    
    #according to doppio model structure , data is from 2009-10-12 to 2017-1-1
    time=pd.to_datetime(time)
    url=get_url(time)
    nc=netCDF4.Dataset(url).variables
    #first find the index of the grid 
    lons=nc['lon_rho'][:]
    lats=nc['lat_rho'][:]
    temp=nc['temp']
    #second find the index of time
    if time<=datetime(2013,5,18):
        espresso_time=nc['ocean_time']
    else:
        espresso_time=nc['time']
    itime = netCDF4.date2index(time,espresso_time,select='nearest')
    index = nearest_point_index2(lon,lat,lons,lats) 
    depth_layers=nc['h'][index[0][0]][index[1][0]]*nc['s_rho']
    index_depth=np.argmin(abs(depth+depth_layers))#depth_layers are negative numbers
    espresso_temp=temp[itime,index_depth,index[0][0],index[1][0]]
    return espresso_temp

def get_url(time):
    # hours = int((endtime-starttime).total_seconds()/60/60) # get total hours
    # time_r = datetime(year=2006,month=1,day=9,hour=1,minute=0)
    if (time- datetime(2013,5,18)).total_seconds()/3600>25:
        #url_oceantime = 'http://tds.marine.rutgers.edu:8080/thredds/dodsC/roms/espresso/hidden/2006_da/his?ocean_time'
        #url_oceantime = 'http://tds.marine.rutgers.edu:8080/thredds/dodsC/roms/espresso/2013_da/his_Best/ESPRESSO_Real-Time_v2_History_Best_Available_best.ncd?time'
        url_oceantime = 'http://tds.marine.rutgers.edu/thredds/dodsC/roms/espresso/2013_da/his/ESPRESSO_Real-Time_v2_History_Best?time[0:1:31931]'
        oceantime = netCDF4.Dataset(url_oceantime).variables['time'][:]    #if url2006, ocean_time.
        t1 = (time - datetime(2013,5,18)).total_seconds()/3600 # for url2006 it's 2006,01,01; for url2013, it's 2013,05,18, and needed to be devide with 3600
        index1 = closest_num(t1, oceantime)
        # url = 'http://tds.marine.rutgers.edu:8080/thredds/dodsC/roms/espresso/2006_da/his?h[0:1:81][0:1:129],s_rho[0:1:35],lon_rho[0:1:81][0:1:129],lat_rho[0:1:81][0:1:129],mask_rho[0:1:81][0:1:129],u[{0}:1:{1}][0:1:35][0:1:81][0:1:128],v[{0}:1:{1}][0:1:35][0:1:80][0:1:129]'
        #url = 'http://tds.marine.rutgers.edu:8080/thredds/dodsC/roms/espresso/hidden/2006_da/his?s_rho[0:1:35],h[0:1:81][0:1:129],lon_rho[0:1:81][0:1:129],lat_rho[0:1:81][0:1:129],temp[{0}:1:{1}][0:1:35][0:1:81][0:1:129],ocean_time'
        #url = 'http://tds.marine.rutgers.edu:8080/thredds/dodsC/roms/espresso/2013_da/his_Best/ESPRESSO_Real-Time_v2_History_Best_Available_best.ncd?h[0:1:81][0:1:129],s_rho[0:1:35],lon_rho[0:1:81][0:1:129],lat_rho[0:1:81][0:1:129],temp[{0}:1:{1}][0:1:35][0:1:81][0:1:129],time' 
        url = 'http://tds.marine.rutgers.edu/thredds/dodsC/roms/espresso/2013_da/his/ESPRESSO_Real-Time_v2_History_Best?s_rho[0:1:35],lon_rho[0:1:81][0:1:129],lat_rho[0:1:81][0:1:129],time[0:1:32387],h[0:1:81][0:1:129],temp[0:1:32387][0:1:35][0:1:81][0:1:129]'
        url = url.format(index1)
    else :
        #url_oceantime = 'http://tds.marine.rutgers.edu:8080/thredds/dodsC/roms/espresso/hidden/2006_da/his?ocean_time'
        url_oceantime='http://tds.marine.rutgers.edu/thredds/dodsC/roms/espresso/2009_da/his?ocean_time'#[0:1:19145]
        oceantime = netCDF4.Dataset(url_oceantime).variables['ocean_time'][:]    #if url2006, ocean_time.
        t1 = (time - datetime(2006,1,1)).total_seconds() # for url2006 it's 2006,01,01; for url2013, it's 2013,05,18, and needed to be devide with 3600
        index1 = closest_num(t1, oceantime)
        #print 'index1' ,index1
        #url = 'http://tds.marine.rutgers.edu:8080/thredds/dodsC/roms/espresso/hidden/2006_da/his?s_rho[0:1:35],h[0:1:81][0:1:129],lon_rho[0:1:81][0:1:129],lat_rho[0:1:81][0:1:129],temp[{0}:1:{1}][0:1:35][0:1:81][0:1:129],ocean_time'
        url='http://tds.marine.rutgers.edu/thredds/dodsC/roms/espresso/2009_da/his?s_rho[0:1:35],h[0:1:81][0:1:129],lon_rho[0:1:81][0:1:129],lat_rho[0:1:81][0:1:129],ocean_time[0:1:19145],temp[0:1:19145][0:1:35][0:1:81][0:1:129]'
        url = url.format(index1)
    return url

def nearest_point_index2(lon, lat, lons, lats):
    d = dist(lon, lat, lons ,lats)
    min_dist = np.min(d)
    index = np.where(d==min_dist)
    return index
def dist(lon1, lat1, lon2, lat2):
    R = 6371.004
    lon1, lat1 = angle_conversion(lon1), angle_conversion(lat1)
    lon2, lat2 = angle_conversion(lon2), angle_conversion(lat2)
    l = R*np.arccos(np.cos(lat1)*np.cos(lat2)*np.cos(lon1-lon2)+\
                        np.sin(lat1)*np.sin(lat2))
    return l
def angle_conversion(a):
    a = np.array(a)
    return a/180*np.pi     
def closest_num(num, numlist, i=0):
#Return index of the closest number in the list
    index1, index2 = 0, len(numlist)
    indx = int(index2/2)
    if not numlist[0] <= num < numlist[-1]:
        raise Exception('{0} is not in {1}'.format(str(num), str(numlist)))
    if index2 == 2:
        l1, l2 = num-numlist[0], numlist[-1]-num
        if l1 < l2:
            i = i
        else:
            i = i+1
    elif num == numlist[indx]:
        i = i + indx
    elif num > numlist[indx]:
        i = closest_num(num, numlist[indx:],
                          i=i+indx)
    elif num < numlist[indx]:
        i = closest_num(num, numlist[0:indx+1], i=i)
    return i
