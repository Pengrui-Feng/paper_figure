# -*- coding: utf-8 -*-
"""
Created on Thu Feb 19 12:06:47 2015
'compare temperature of turtle and roms model before and after a storm'
@author: zdong,yifan
"""
import numpy as np
import pandas as pd
import matplotlib as mpl
from datetime import datetime,timedelta
import matplotlib.pyplot as plt
from turtleModule import str2ndlist,dist,np_datetime
##################################################################
obsData=pd.read_csv('tu94wModel.csv',index_col=0)
turtle_id=obsData['PTT']
obslat = obsData['LAT']
obslon = obsData['LON']
obstime = pd.Series(np_datetime(obsData['date']),index=obsData.index)
obsDepth=pd.Series(str2ndlist(obsData['obstemp']),index=obsData.index)
obstemp=pd.Series(str2ndlist(obsData['depth']),index=obsData.index)

buoyData=pd.read_csv('ndbc_2011.csv')                          #data of wind speed and wave height in 2011
tf_index=np.where(buoyData['TF'].notnull())[0]
buoylat = pd.Series(buoyData['lat'],index=tf_index)
buoylon = pd.Series(buoyData['lon'],index=tf_index)
buoyspeed=pd.Series(buoyData['wind_speed'],index=tf_index)
buoywave=pd.Series(buoyData['wave_height'],index=tf_index)
buoytime = pd.Series(buoyData['Date'],index=tf_index)
indx=[]
for i in tf_index:
    buoytime[i]=datetime.strptime(buoytime[i], "%Y-%m-%d %H:%M")  # change str to datatime
    if 17.2<buoyspeed[i]:
        if buoywave[i]>5.5:
            indx.append(i)                                      #choose which day has storm
data=pd.DataFrame({'time':buoytime,'wind_speed':buoyspeed,'wave_height':buoywave,
                  'lat':buoylat,'lon':buoylon},index=tf_index)
data = data.sort_index(by='time')

buoyData2=pd.read_csv('ndbc_2013.csv')                           #data of wind speed and wave height in 2013
tf_index2=np.where(buoyData2['TF'].notnull())[0]
buoylat2 = pd.Series(buoyData2['lat'],index=tf_index2)
buoylon2= pd.Series(buoyData2['lon'],index=tf_index2)
buoyspeed2=pd.Series(buoyData2['wind_speed'],index=tf_index2)
buoywave2=pd.Series(buoyData2['wave_height'],index=tf_index2)
buoytime2 = pd.Series(buoyData2['Date'],index=tf_index2)
indx2=[]
for i in tf_index2:
    buoytime2[i]=datetime.strptime(buoytime2[i], "%Y-%m-%d %H:%M")  # change str to datatime
    if 17.2<buoyspeed2[i]:
        indx2.append(i)                                            #choose which day has storm
data2=pd.DataFrame({'time':buoytime2,'wind_speed':buoyspeed2,'wave_height':buoywave2,
                  'lat':buoylat2,'lon':buoylon2},index=tf_index2)
data2 = data.sort_index(by='time')

early_2011=[]
after_2011=[]
early_2013=[]
after_2013=[]
early_mod=[]
after_mod=[]
for i in obsData.index:
    for j in indx:
        if dist(buoylat[0],buoylon[0],obslat[i],obslon[i])<50:        #distance is smaller than 50km
            if obstime[i].month==8 and obstime[i].year==2011:
                if obstime[i].day>28:                                 #choose day after storm 
                    after_2011.append(i) 
        if dist(buoylat[0],buoylon[0],obslat[i],obslon[i])<50:
            if obstime[i].month==8 and obstime[i].year==2011:
                if obstime[i].day==27:                                 #choose day before storm
                    early_2011.append(i)
    for j in indx2:
        if dist(buoylat2[0],buoylon2[0],obslat[i],obslon[i])<50:
            if obstime[i].month==5 and obstime[i].year==2013:
                if obstime[i].day==26:                                 #choose day after storm
                    after_2013.append(i)
        if dist(buoylat2[0],buoylon2[0],obslat[i],obslon[i])<50:
            if obstime[i].month==5 and obstime[i].year==2013:
                if obstime[i].day==24:                                #choose day before storm
                    early_2013.append(i)
after_2011=pd.Series(after_2011).unique()
early_2011=pd.Series(early_2011).unique()
early_id_2011=pd.Series(turtle_id[early_2011])                       #get id of turtle
after_id_2011=pd.Series(turtle_id[after_2011])
name=0
for i in early_2011:
    for j in after_2011:
        if early_id_2011[i]==after_id_2011[j]:
            if max(obsDepth[i])>30:
                if max(obsDepth[j])>30:
                    name+=1
                    fig=plt.figure()
                    ax=fig.add_subplot(111)
                    plt.text(6,6,'id:'+str(early_id_2011[i]),fontsize=10)
                    ax.set_xlim([5, 25])
                    ax.set_ylim([50, 0])
                    ax.set_xlabel(u'Tempature(°C)', fontsize=14)
                    ax.set_ylabel('Depth(m)', fontsize=14)
                    ax.set_title('temperature before and after 2011 storm',fontsize=16)
                    plt.xticks(fontsize=12)
                    plt.yticks(fontsize=12)
                    ax.plot(obstemp[i],obsDepth[i],'bo--',markersize=4, label=str(obstime[i]))      
                    ax.plot(obstemp[j],obsDepth[j],'ro-',markersize=4, label=str(obstime[j]))
                    #print obstemp[j]
                    #print modtemp[j]
                    ax.legend(loc='lower right',fontsize='small')

                    '''leg = plt.gca().get_legend()
                    ltext  = leg.get_texts()
                    plt.setp(ltext,fontsize = 'medium') '''
                    plt.savefig(str(name),dpi=200)

after_2013=pd.Series(after_2013).unique()
early_2013=pd.Series(early_2013).unique()
early_id_2013=pd.Series(turtle_id[early_2013])
after_id_2013=pd.Series(turtle_id[after_2013])
for i in early_2013:
    for j in after_2013:
        if early_id_2013[i]==after_id_2013[j]:
            name+=1
            fig=plt.figure()
            ax=fig.add_subplot(111)
            plt.text(6,6,'id:'+str(early_id_2013[i]),fontsize=10)
            ax.set_xlim([5, 25])
            ax.set_ylim([50, 0])
            ax.set_xlabel(u'Tempature(°C)', fontsize=14)
            ax.set_ylabel('Depth(m)', fontsize=14)
            ax.set_title(' temperature before and after 2013 storm',fontsize=16)
            plt.xticks(fontsize=12)
            plt.yticks(fontsize=12)
            ax.plot(obstemp[i],obsDepth[i],'bo--',markersize=4, label=str(obstime[i]))      
            ax.plot(obstemp[j],obsDepth[j],'ro-',markersize=4, label=str(obstime[j]))
            #print obstemp[j]
            ax.legend(loc='lower right',fontsize='small')#, borderpad=1.5, labelspacing=1.5
            plt.savefig(str(name),dpi=200)
            
plt.show()
