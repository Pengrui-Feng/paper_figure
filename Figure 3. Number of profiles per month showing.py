# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 09:07:00 2020
@author: pengrui
"""
'plot number of dive and turtle in each month'
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from turtleModule import str2list,np_datetime

####################################################
obsData=pd.read_csv('/content/drive/My Drive/PENGRUI/merge_nosplit/tu102_merge_td_gps.csv')
obsTime=pd.Series(datetime.strptime(x,'%Y-%m-%d %H:%M:%S') for x in obsData['gps_date'])
turtle_ids = pd.Series(obsData['PTT'])

shipData=pd.read_csv('/content/drive/My Drive/filtered_ship_data.csv')
shiptime=pd.Series(datetime.strptime(x,'%Y-%m-%d %H:%M:%S') for x in shipData['datetime'])
ship_ids=shipData['vessel_num']

Num=[]
num=[[[],[],[],[],[],[],[],[],[],[],[],[]],[[],[],[],[],[],[],[],[],[],[],[],[]],[[],[],[],[],[],[],[],[],[],[],[],[]],[[],[],[],[],[],[],[],[],[],[],[],[]],[[],[],[],[],[],[],[],[],[],[],[],[]]]
#num is 5*12,5 is 5 years,12 is 12 months
for i in range(5):    # 2014~2018,5 years
    Num.append([0]*12)    #12 months
for i in range(len(obsData)):
    for j in range(5):
        if obsTime[i].year==2014+j:
            for q in range(12):
                if obsTime[i].month==q+1:
                    Num[j][q]+=1
                    num[j][q].append(i)
for i in range(len(num)):
    for j in range(len(num[i])):
        num[i][j]=len(turtle_ids[num[i][j]].unique())

Num1=[]
num1=[[[],[],[],[],[],[],[],[],[],[],[],[]],[[],[],[],[],[],[],[],[],[],[],[],[]],[[],[],[],[],[],[],[],[],[],[],[],[]],[[],[],[],[],[],[],[],[],[],[],[],[]],[[],[],[],[],[],[],[],[],[],[],[],[]]]
#num is 5*12,5 is 5 years,12 is 12 months
for i in range(5):    # 2014~2018,5 years
    Num1.append([0]*12)    #12 months
for i in shipData.index:
    for j in range(5):
        if shiptime[i].year==2014+j:
            for q in range(12):
                if shiptime[i].month==q+1:
                    Num1[j][q]+=1
                    num1[j][q].append(i)
for i in range(len(num1)):
    for j in range(len(num1[i])):
        num1[i][j]=len(ship_ids[num1[i][j]].unique())


width=0.2
color=['blue','black','red','green','yellow']
fig=plt.figure()

ax = fig.add_subplot(1,2,1)
for i in range(5):
    ax.bar(np.arange(1,13)+width*(i-3.75),Num[i],align="center",width=width,color=color[i] ,label=str(i+2014))
#plt.legend(loc='best',fontsize = 'x-small')
plt.xlim([0,13]) 
plt.xticks(range(13),fontsize=10)
plt.yticks(fontsize=10)
plt.ylabel('Quantity',fontsize=16)
plt.title('#Turtle profiles per month',fontsize=12)
ax1 = fig.add_subplot(1,2,2)
for i in range(5):
    ax1.bar(np.arange(1,13)+width*(i-3.75),Num1[i],align="center",width=width,color=color[i] ,label=str(i+2014))
plt.legend(loc='best',fontsize = 'x-small')
plt.xlim([1,13]) 
plt.ylim([0,1200])
plt.xticks(np.arange(1,13),fontsize=10)
plt.setp(ax1.get_yticklabels() ,visible=False)
fig.text(0.5,0.04,'Month',ha='center', va='center',fontsize=16)
plt.title('#Ship profiles per month',fontsize=12)
plt.savefig('turtleVSship_profiles_allship',dpi=200)
