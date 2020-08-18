# -*- coding: utf-8 -*-
'''
draw temp change of one specific turtle and rom 
'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from datetime import datetime, timedelta

path='/content/drive/My Drive/'
data = pd.read_csv(path+'tu98wModels.csv')
def smooth(v, e):
    '''
    Smooth the data, get rid of data that changes too much.
    '''
    for i in range(2, len(v)-1):
        a, b, c = v[i-1], v[i], v[i+1]
        diff1 = abs(b - c) #diff1 is not used
        diff2 = abs(b - a)
        if diff2>e:
            v[i] = a
    return v
def str2list(s, bracket=False):
    if bracket:
        s = s[:]
    s = s.split(',')
    s = [float(i) for i in s]
    return s
def str2ndlist(arg, bracket=False):
    '''
    convert list full of str to multidimensional arrays
    '''
    ret = []
    for i in arg:
        a = str2list(i, bracket=bracket)
        ret.append(a)
    # ret = np.array(ret)
    return ret
data=data[data['FVCOM_temp'].str.contains('nan') == False]   ### delate the rows if it includes 'nan' 
data=data[data['doppio_temp'].str.contains('nan') == False]
obstime = pd.Series(pd.to_datetime(data['gps_date']),index=data.index)
ttemp = pd.Series(str2ndlist(data['obs_temp']),index=data.index)
tdepth = pd.Series(str2ndlist(data['depth']),index=data.index)
#doppioTemp = pd.Series(np.array(str2ndlist(data['doppio_temp'], bracket=True)))
fvcomTemp = pd.Series(np.array(str2ndlist(data['FVCOM_temp'], bracket=True)),index=data.index)
romsTemp = pd.Series(np.array(str2ndlist(data['doppio_temp'], bracket=True)),index=data.index)
id = data['PTT'].drop_duplicates().values
tID = id[16]  #
obstime = obstime[data['PTT']==tID]
ttemp = ttemp[data['PTT']==tID]
fvcomTemp=fvcomTemp[data['PTT']==tID]
romsTemp=romsTemp[data['PTT']==tID]
#Data = pd.DataFrame({'turtle_temp':ttemp.values,'fvcom_temp':fvcomTemp,'roms_temp':romsTemp,'turtle_depth':tdepth})
t_MaxTemp, t_MinTemp = [], []
fvcom_MaxTemp, fvcom_MinTemp = [], []
roms_MaxTemp,roms_MinTemp =[],[]
for i in ttemp.index:  #this loop calculate min & max temperature of each dive
    #if len(ttemp[i])>5:
        t_MaxTemp.append(max(ttemp[i]))
        t_MinTemp.append(min(ttemp[i]))
        fvcom_MaxTemp.append(max(fvcomTemp[i]))
        fvcom_MinTemp.append(min(fvcomTemp[i]))
        roms_MaxTemp.append(max(romsTemp[i]))
        roms_MinTemp.append(min(romsTemp[i]))    
data = pd.DataFrame({'PTT':tID, 'time':obstime, 't_MaxTemp':t_MaxTemp, 't_MinTemp':t_MinTemp,
                    'fvcom_MaxTemp': fvcom_MaxTemp, 'fvcom_MinTemp': fvcom_MinTemp,'roms_MaxTemp': roms_MaxTemp, 
                    'roms_MinTemp': roms_MinTemp})
data = data.sort_values(by='time')

#data['t_MinTemp'] = smooth(data['roms_MinTemp'].values, 5)
#data['t_MinTemp'] = smooth(data['fvcom_MinTemp'].values, 5)
# data['time'] = smooth(data['time'].values, timedelta(days=20))
Date=[]
for i in data.index:
    Date.append(data['time'][i])
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(Date, data['t_MaxTemp'], color='b', linewidth=1.5, label='max-turtle')
ax.plot(Date, data['t_MinTemp'], '--',color='b', linewidth=1.5, label='min-turtle')
ax.plot(Date, data['fvcom_MaxTemp'], color='r', linewidth=1.5, label='max-fvcom')
ax.plot(Date, data['fvcom_MinTemp'], '--',color='r', linewidth=1.5, label='min-fvcom')
ax.plot(Date, data['roms_MaxTemp'], color='y', linewidth=1.5, label='max-roms')
ax.plot(Date, data['roms_MinTemp'], '-.',color='y', linewidth=1.5, label='min-roms')
plt.legend(loc=1,ncol=3,fontsize = 'x-small')
ax.set_xlabel('Time(2018)', fontsize=14)
ax.set_ylabel('Temperature('+u'°C'+')', fontsize=14)
dates = mpl.dates.drange(np.amin(obstime), np.max(obstime), timedelta(days=30))
dateFmt = mpl.dates.DateFormatter('%b')
ax.set_xticks(dates)
ax.xaxis.set_major_formatter(dateFmt)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.title('Time series of temp for turtle:{0}'.format(tID), fontsize=16)
plt.savefig('timeSeries_%s.png'% tID, dpi=200)
plt.show()
'''
fig = plt.figure()
ax2 = fig.add_subplot(212)
for i in temp.index:
    # ax2.plot(([time[i]+timedelta(hours=5)])*len(temp[i]), temp[i],color='b')
    ax2.plot([time[i]]*len(temp[i]), modTemp[i], color='r')
ax2.set_xlabel('Time', fontsize=20)
ax2.set_ylabel('Temperature', fontsize=20)
dates = mpl.dates.drange(np.amin(time), np.max(time), timedelta(days=30))
dateFmt = mpl.dates.DateFormatter('%b,%Y')
ax2.set_xticks(dates)
ax2.xaxis.set_major_formatter(dateFmt)
ax2.set_title('Model', fontsize=20)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)


ax1 = fig.add_subplot(211)
for i in temp.index:
    ax1.plot([time[i]]*len(temp[i]), temp[i], color='b')
ax1.set_ylabel('Temperature', fontsize=20)
ax1.set_xticks(dates)
ax1.xaxis.set_major_formatter(dateFmt)
ax1.set_title('Observation', fontsize=20)
plt.xticks(fontsize=10)
plt.yticks(fontsize=20)
fig.suptitle('Time series of temp for turtle:{0}'.format(tID), fontsize=25)
ax2.set_yticks(ax1.get_yticks())
plt.show()
'''
