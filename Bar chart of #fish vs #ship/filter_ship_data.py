# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 10:26:31 2020
'original_ship_data.csv' is so large,from 1960s. so filter and select duration we want 
@author: pengrui
"""

import pandas as pd
import numpy as np
import math
from datetime import datetime, timedelta

def numSplit(num):
    hour=int(math.floor(num))
    minn = round((num-hour),2)
    mins= int(minn*60)
    time = '{0}:{1}:00'.format(str(hour).zfill(2),str(mins).zfill(2))
    return time

### set the range of date
start_time = datetime(2009,1,1).strftime('%m-%d-%Y') 
end_time = datetime(2019,1,1).strftime('%m-%d-%Y')

### filter the data
path1= '/content/drive/My Drive/'#/content/drive/My Drive/original_ship_data.csv
ship= pd.read_csv(path1+'original_ship_data.csv',skiprows= 3100000,usecols=[1,2,3,4,5,6,7,8],header=None)#totally 4710692 rows
'''
ship.to_csv('ship_data.csv')
path2='/content/ship_data.csv'
#ship= pd.read_csv(path2,usecols=[1,2,3,4,5,6,7,8],header=None)
ship= pd.read_csv(path2,usecols=[2,3,4,5,6,7,8,9],header=None)
'''
ship.columns=['vessel_num','dive_num','date','time','lat','lon','depth','temp']
# put 'depth' and 'demp' in one line with 'str'

ship=ship.sort_values(by=['vessel_num','date','time','depth'])
ship['depth'] = ship['depth'].astype('int')
ship['depth'] = ship['depth'].astype('str')
ship['temp']= ship['temp'].astype('str')
ship=ship.groupby(['vessel_num','date','time','dive_num','lat','lon'])['depth','temp'].agg(lambda x:x.str.cat(sep=','))
'''
#list
Data['depth'] = Data.groupby(['vessel_num','datetime'])['depth'].apply(lambda x:x.tolist())
Data['temp'] = Data.groupby(['vessel_num','datetime'])['temp'].apply(lambda x:x.tolist())
'''
ship.to_csv('ship1.csv')
ship=pd.read_csv('ship1.csv')
for i in range(len(ship)):
    ship['time'][i] = numSplit(ship['time'][i])

ship['datetime']=pd.to_datetime(ship['date']+' '+ship['time'])
Time = ship['datetime']
ship['lon']=-ship['lon']
ship=ship[['vessel_num','dive_num','datetime','lat','lon','depth','temp']]
indx=np.where((Time>=start_time) & (Time<=end_time))[0]
time=Time[indx]
Data = ship.loc[time.index]
Data=Data.sort_values(by=["vessel_num","datetime",'depth'])

Data.to_csv('filtered_ship_data.csv')
