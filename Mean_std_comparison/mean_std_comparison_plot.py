# -*- coding: utf-8 -*-
"""
Created on Thu Apr 24 14:49:34 2020
Plot error bar and ratio of error between turtle and ship and 3 models.
@author: pengrui
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
#import netCDF4
#import turtleModule
def str2list(s, bracket=False):
    if bracket:
        s = s[:]
    s = s.split(',')
    s = [float(i) for i in s]
    return s
def str2ndlist(arg, bracket=False):
    #convert list full of str to multidimensional arrays
    ret = []
    for i in arg:
        a = str2list(i, bracket=bracket)
        ret.append(a)
    # ret = np.array(ret)
    return ret
#################ship#######################
'''
Data=pd.read_csv('/content/drive/My Drive/matched_stm.csv')
Data['ship_depth']= Data['ship_depth'].astype('str')
Data['ship_temp']= Data['ship_temp'].astype('str')
Data['turtle_depth']= Data['turtle_depth'].astype('str')
Data['turtle_temp']= Data['turtle_temp'].astype('str')
shipdepth=pd.Series(str2ndlist(Data['ship_depth'], bracket=True))
shiptemp=pd.Series(str2ndlist(Data['ship_temp'], bracket=True))
obsdepth=pd.Series(str2ndlist(Data['turtle_depth'], bracket=True))
obstemp=pd.Series(str2ndlist(Data['turtle_temp'], bracket=True))
data_ship = pd.DataFrame({'turtletemp': obstemp,'shiptemp':shiptemp,'turtledepth': obsdepth,'shipdepth':shipdepth})
'''
################### Models ########################
data = pd.read_csv('/content/drive/My Drive/matched_stm.csv',skiprows=10)
data.columns=['','ship_id',	'ship_time',	'ship_lat',	'ship_lon',	'ship_depth',	'ship_temp',	'turtle_id',	'turtle_time',	'turtle_lat',	'turtle_lon',	'turtle_depth',	'turtle_temp',	'FVCOM_temp','espresso_temp'] 
#data=data.dropna(subset=['espresso_temp'])
shipdepth=pd.Series(str2ndlist(data['ship_depth']))
shiptemp=pd.Series(str2ndlist(data['ship_temp']))
ttemp = pd.Series(str2ndlist(data['turtle_temp']))
tdepth = pd.Series(str2ndlist(data['turtle_depth']))
#doppioTemp = pd.Series(np.array(str2ndlist(data['doppio_temp'], bracket=True)))
fvcomTemp = pd.Series(np.array(str2ndlist(data['FVCOM_temp'], bracket=True)))
espressoTemp = pd.Series(np.array(str2ndlist(data['espresso_temp'], bracket=True)))
Data = pd.DataFrame({'turtle_temp':ttemp.values,'ship_temp':shiptemp,'fvcom_temp':fvcomTemp,'espresso_temp':espressoTemp,'turtle_depth':tdepth,'ship_depth':shipdepth})
############################
TEMP_ship=[]
TEMP_fvcom=[]
TEMP_espresso=[]
for i in np.arange(50):   #depth 0~50m
    TEMP_ship.append([])
    for j in Data.index:
        for q in range(len(Data['turtle_depth'][j])):
            if int(Data['turtle_depth'][j][q])==i:   #no depth<2m
                for r in range(len(Data['ship_depth'][j])):
                    if int(Data['ship_depth'][j][r])==i:
                        TEMP_ship[i].append(Data['ship_temp'][j][r]-Data['turtle_temp'][j][q])


for i in np.arange(50):   #depth 0~50m
    TEMP_fvcom.append([])
    TEMP_espresso.append([])
    for j in Data.index:
        for q in range(len(Data['turtle_depth'][j])):
            if int(Data['turtle_depth'][j][q])==i:   #no depth<2m            
                TEMP_fvcom[i].append(Data['fvcom_temp'][j][q]-Data['turtle_temp'][j][q])
                TEMP_espresso[i].append(Data['espresso_temp'][j][q]-Data['turtle_temp'][j][q])

ave_ship,std_ship=[],[]
ave_fvcom,std_fvcom=[],[]
ave_espresso,std_espresso=[],[]
#ave_doppio,std_doppio=[],[]
for i in range(50):  #depth 0~50m
    #ave_doppio.append(np.mean(TEMP_doppio[i]))
    #std_doppio.append(np.std(TEMP_doppio[i]))
    ave_ship.append(np.mean(TEMP_ship[i]))
    std_ship.append(np.std(TEMP_ship[i]))
    ave_fvcom.append(np.mean(TEMP_fvcom[i]))
    std_fvcom.append(np.std(TEMP_fvcom[i]))
    ave_espresso.append(np.mean(TEMP_espresso[i]))
    std_espresso.append(np.std(TEMP_espresso[i]))
fig=plt.figure(figsize=(8,3))
ax1=fig.add_subplot(131)
ax1.errorbar(ave_ship,range(len(ave_ship)),linewidth=1.2,xerr=std_ship,elinewidth=0.8,capsize=2.1)
plt.ylim([50,0])
plt.xlim([-6,11])
#plt.setp(ax1.get_xticklabels() ,visible=False)
plt.text(4,45,'SHIP',fontsize=10)
ax2=fig.add_subplot(132)
ax2.errorbar(ave_fvcom,range(len(ave_fvcom)),linewidth=1.2,xerr=std_fvcom,elinewidth=0.8,capsize=2.1)
plt.ylim([50,0])
plt.xlim([-6,11])
plt.setp(ax2.get_yticklabels(),visible=False)
plt.text(3,45,'FVCOM',fontsize=10)
#plt.title('Modeled-observed at multiple levels',fontsize=20)

ax3=fig.add_subplot(133)
ax3.errorbar(ave_espresso,range(len(ave_espresso)),linewidth=1.2,xerr=std_espresso,elinewidth=0.8,capsize=2.1)
plt.ylim([50,0])
plt.xlim([-6,11])
plt.setp(ax3.get_yticklabels() ,visible=False)
plt.text(1,45,'ESPRESSO',fontsize=10)

fig.text(0.5, 0.01, 'Temperature ($^\circ$C)', ha='center', va='center', fontsize=14)#  0.5 ,0.04 represent the  plotting scale of x_axis and y_axis
fig.text(0.06, 0.5, 'Depth(m)', ha='center', va='center', rotation='vertical',fontsize=14)
fig.text(0.5, 0.94, 'comparison with turtle data', ha='center', va='center', fontsize=16)
plt.savefig('comparison_statistic_mean_std.png',dpi=200)
plt.show()
