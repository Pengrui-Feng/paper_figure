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

####################################################
path='/content/drive/My Drive/'
shipData=pd.read_csv(path+'filtered_ship_data 09-18.csv')       # output of 'filter_ship_data.py'
shiptime=pd.Series(datetime.strptime(x,'%Y-%m-%d %H:%M:%S') for x in shipData['datetime'])
ship_ids=shipData['vessel_num']

#num is 5*12,5 is 5 years,12 is 12 months
ship_Num=[]
t_Num=[]
for i in range(10):    # 2019~2018,10 years
    ship_Num.append([0]*12)    #12 months
    t_Num.append([0]*12) 

for i in shipData.index:
    for j in range(5):
        if shiptime[i].year==2009+j:
            for q in range(12):
                if shiptime[i].month==q+1:
                    ship_Num[j][q]+=1

obsData=pd.read_csv(path+'all_merge_td_gps.csv')   # output of 'combine_several_files.py'
obsTime=pd.Series(datetime.strptime(x,'%Y-%m-%d %H:%M:%S') for x in obsData['gps_date'])
turtle_ids = pd.Series(obsData['PTT'])
for i in range(len(obsData)):
    for j in range(10):
        if obsTime[i].year==2009+j:
            for q in range(12):
               if obsTime[i].month==q+1:
                    t_Num[j][q]+=1

width=0.2
color=['g','darkviolet','orange','b','hotpink','c','peru','lime','brown','orangered','k','magenta','r','cyan','gray','y','pink','olive','indigo','coral','plum','violet','salmon','tan','navy','maroon','blue','peachpuff','slateblue','khaki','gold','chocolate']
fig=plt.figure()
ax1 = fig.add_subplot(1,2,1)
for i in range(10):
    ax1.bar(np.arange(1,13)+width*(i-3.75),t_Num[i],align="center",width=width,color=color[i],label=str(i+2009))
#plt.legend(loc='best',fontsize = 'x-small')
plt.xlim([0,13]) 
plt.ylim([0,1200])
plt.xticks(range(13),fontsize=10)
plt.yticks(fontsize=10)
plt.ylabel('Quantity',fontsize=16)
plt.title('#Turtle profiles per month',fontsize=12)

ax2 = fig.add_subplot(1,2,2)
for i in range(10):
    ax2.bar(np.arange(1,13)+width*(i-3.75),ship_Num[i],align="center",width=width,color=color[i] ,label=str(i+2009))
plt.legend(loc='best',fontsize = 'x-small')
plt.xlim([1,13]) 
plt.ylim([0,600])
plt.xticks(np.arange(1,13),fontsize=10)
#plt.setp(ax2.get_yticklabels(),visible=False)
fig.text(0.5,0.04,'Month',ha='center', va='center',fontsize=16)
plt.title('#Ship profiles per month',fontsize=12)
plt.savefig('num_turtleVSship_profiles 09-18',dpi=200)
plt.show()
