# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 09:07:00 2020
'plot number of dive and turtle in each month'
@author: pengrui
"""
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from turtleModule import str2list,np_datetime
import glob
####################################################
shipData=pd.read_csv('/content/drive/My Drive/filtered_ship_data.csv')
shiptime=pd.Series(datetime.strptime(x,'%Y-%m-%d %H:%M:%S') for x in shipData['datetime'])
ship_ids=shipData['vessel_num']

#num is 5*12,5 is 5 years,12 is 12 months
ship_Num=[]
t_Num=[]
for i in range(5):    # 2014~2018,5 years
    ship_Num.append([0]*12)    #12 months
    t_Num.append([0]*12) 

for i in shipData.index:
    for j in range(5):
        if shiptime[i].year==2014+j:
            for q in range(12):
                if shiptime[i].month==q+1:
                    ship_Num[j][q]+=1

csv_list = glob.glob('*_merge_td_gps.csv') #search csv files in current folder
for g in csv_list: #g is a filename which is processed
    obsData=pd.read_csv(g)
    obsTime=pd.Series(datetime.strptime(x,'%Y-%m-%d %H:%M:%S') for x in obsData['gps_date'])
    turtle_ids = pd.Series(obsData['PTT'])
    for i in range(len(obsData)):
        for j in range(5):
            if obsTime[i].year==2014+j:
                for q in range(12):
                    if obsTime[i].month==q+1:
                        t_Num[j][q]+=1

width=0.2
color=['blue','black','red','green','yellow']
fig=plt.figure()
ax1 = fig.add_subplot(1,2,1)
for i in range(5):
    ax1.bar(np.arange(1,13)+width*(i-3.75),t_Num[i],align="center",width=width,color=color[i],label=str(i+2014))
#plt.legend(loc='best',fontsize = 'x-small')
plt.xlim([0,13]) 
plt.ylim([0,600])
plt.xticks(range(13),fontsize=10)
plt.yticks(fontsize=10)
plt.ylabel('Quantity',fontsize=16)
plt.title('#Turtle profiles per month',fontsize=12)

ax2 = fig.add_subplot(1,2,2)
for i in range(5):
    ax2.bar(np.arange(1,13)+width*(i-3.75),ship_Num[i],align="center",width=width,color=color[i] ,label=str(i+2014))
plt.legend(loc='best',fontsize = 'x-small')
plt.xlim([1,13]) 
plt.ylim([0,600])
plt.xticks(np.arange(1,13),fontsize=10)
plt.setp(ax2.get_yticklabels(),visible=False)
fig.text(0.5,0.04,'Month',ha='center', va='center',fontsize=16)
plt.title('#Ship profiles per month',fontsize=12)
plt.show()
plt.savefig('num_turtleVSship_profiles',dpi=200)
