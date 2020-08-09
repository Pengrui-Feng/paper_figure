# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 10:26:31 2020

@author: pengrui
"""

import pandas as pd
import numpy as np
import math
from datetime import datetime,timedelta
import zlconversions as zl
import matplotlib.pyplot as plt
from tqdm import tqdm

def nearlonlat(lon,lat,lonp,latp): 
    cp=np.cos(latp*np.pi/180.)
    # approximation for small distance
    dx=(lon-lonp)*cp
    dy=lat-latp
    dist2=dx*dx+dy*dy
    i=np.argmin(dist2)
    return i

path='/content/drive/My Drive/'
r1,r2 = 0,3                # the obs position that has shipboard position within (r) kilometers might be considered as good data.
day = 3                # the obs time that has shipboard time within (3 days) days might be considered as good data.


s = pd.read_csv(path+'filtered_ship_data 09-18.csv')  # input file is from 'filter_ship_data.py'
s_id = s['vessel_num']
slat = s['lat']
slon = s['lon']
stime = pd.Series(datetime.strptime(x, "%Y-%m-%d %H:%M:%S") for x in s['datetime'])
sdepth = s['depth']
stemp= s['temp']

t = pd.read_csv(path+'all_merge_td_gps.csv') # the input file includes all databases
t_id= t['PTT']
tlat = t['lat_gps']
tlon = t['lon_gps']
ttime = pd.Series(datetime.strptime(x, "%Y-%m-%d %H:%M:%S") for x in t['gps_date'])
#ttime=pd.to_datetime(t['gps_date'])
tdepth = t['depth']
ttemp= t['temp']
index = []     #index of turtle
indx=[]      #index of shipboard 


for i in tqdm(range(len(t))):
    for j in range(len(s)):
        l = zl.dist(slat[j],slon[j],tlat[i],tlon[i])
        if l<r2 and l>=r1:
            try:
                #print l        #distance
                maxtime = ttime[i]+timedelta(days=day)
                mintime = ttime[i]-timedelta(days=day)
                mx = stime[j]<maxtime
                mn = stime[j]>mintime
                TF = mx*mn  
                if TF==1:      #time
                    index.append(i)     #turtle index
                    indx.append(j)      #ship index
            except:
                continue

data=pd.DataFrame(range(len(indx)))
s_id,t_id,s_time,t_time,s_lat,s_lon,t_lat,t_lon=[],[],[],[],[],[],[],[]
s_depth,s_temp,t_depth,t_temp=[],[],[],[]
for i in range(len(indx)):
    ss=indx[i]
    tt=index[i]
    s_id.append(s['vessel_num'][ss])
    s_time.append(s['datetime'][ss])
    s_lat.append(s['lat'][ss])
    s_lon.append(s['lon'][ss])
    s_depth.append(s['depth'][ss])
    s_temp.append(s['temp'][ss])
    t_id.append(t['PTT'][tt])
    t_time.append(t['gps_date'][tt])
    t_lat.append(t['lat_gps'][tt])
    t_lon.append(t['lon_gps'][tt])
    t_depth.append(t['depth'][tt])
    t_temp.append(t['temp'][tt])

data['ship_id']=pd.Series(s_id)
data['ship_time']=pd.Series(s_time)
data['ship_lat']=pd.Series(s_lat)
data['ship_lon']=pd.Series(s_lon)
data['ship_depth']=pd.Series(s_depth)
data['ship_temp']=pd.Series(s_temp)
data['turtle_id']=pd.Series(t_id)
data['turtle_time']=pd.Series(t_time)
data['turtle_lat']=pd.Series(t_lat)
data['turtle_lon']=pd.Series(t_lon)
data['turtle_depth']=pd.Series(t_depth)
data['turtle_temp']=pd.Series(t_temp)

data.to_csv('matched_turtleVSship 09-18.csv')
#data.to_csv('/content/drive/My Drive/matched_turtleVSship_all.csv')
