# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 13:51:36 2017
draw the bottom depth of the correlation between turtle and models(fvcom,roms) and ship 
@author: pengrui
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from scipy import stats

#########################################MAIN CODE#####################################################################################################
FONTSIZE = 25
path='/content/drive/My Drive/'
data = pd.read_csv(path+'matched_ship_turtle_models.csv')

data.columns=['','ship_id',	'ship_time','ship_lat',	'ship_lon',	'ship_depth',	'ship_temp','turtle_id','turtle_time','turtle_lat',	'turtle_lon',	'turtle_depth',	'turtle_temp',	'FVCOM_temp','ROMS_temp'] 
data=data[data['FVCOM_temp'].str.contains('nan') == False]   ### delate the rows if it includes 'nan' 
data=data[data['ROMS_temp'].str.contains('nan') == False]
shipdepth=pd.Series(str2ndlist(data['ship_depth']))
#shipdepth=getlastvalue(pd.Series(str2ndlist(data['ship_depth'])))
shiptemp=pd.Series(str2ndlist(data['ship_temp']))
#shiptemp=getlastvalue(pd.Series(str2ndlist(data['ship_temp'])))
ttemp = pd.Series(str2ndlist(data['turtle_temp']))
#ttemp = getlastvalue(pd.Series(str2ndlist(data['turtle_temp'])))
tdepth = pd.Series(str2ndlist(data['turtle_depth']))
#tdepth = getlastvalue(pd.Series(str2ndlist(data['turtle_depth'])))
fvcomTemp = pd.Series(np.array(str2ndlist(data['FVCOM_temp'], bracket=True)))
espressoTemp = pd.Series(np.array(str2ndlist(data['ROMS_temp'], bracket=True)))
#fvcomTemp = getlastvalue(pd.Series(np.array(str2ndlist(data['FVCOM_temp'], bracket=True))))
#espressoTemp = getlastvalue(pd.Series(np.array(str2ndlist(data['ROMS_temp'], bracket=True))))
Data = pd.DataFrame({'turtle_temp':ttemp.values,'ship_temp':shiptemp,'fvcom_temp':fvcomTemp,'espresso_temp':espressoTemp,'turtle_depth':tdepth,'ship_depth':shipdepth})

tempObs_ship=[] 
tempMod_ship=[]
for i in Data.index:
    
    for k in range(len(shipdepth[i])):
        if tdepth[i][-1]==shipdepth[i][k]:
            tempObs_ship.append(ttemp[i][-1])
            tempMod_ship.append(shiptemp[i][k])

tempObs_roms = []
tempMod_roms = []
for i in range(len(ttemp.values)):
    if espressoTemp.values[i][-1]>100:continue
    tempObs_roms.append(ttemp.values[i][-1])
    tempMod_roms.append(espressoTemp.values[i][-1])       

tempObs_fvcom = []
tempMod_fvcom = []
for i in range(len(ttemp.values)):
    tempObs_fvcom.append(ttemp.values[i][-1])
    tempMod_fvcom.append(fvcomTemp.values[i][-1])
        
       
tempObs=[tempObs_ship ,tempObs_roms,tempObs_fvcom]
tempMod=[tempMod_ship,tempMod_roms,tempMod_fvcom]
#rng = ['25.0', '25.0~50.0', '50.0~75.0', '75.0','Using the entire profiles','<50']
rng=['bottomtemp_correlation comparison']
#number=[[0,200],[0,25],[0,12],[0,5],[0,200],[0,200]]
text=['SHIP','ROMS','FVCOM']
show2pic(rng,tempObs,tempMod,FONTSIZE,text,bins=150)
plt.show()
########################################functions######################################
def getlastvalue(series):
    b=[]
    for i in range(len(series)):
        a=series[i][-1]
        b.append(a)
    b=pd.Series(b)    
    return b 

def histogramPoints(x, y, bins):
    H, xedges, yedges = np.histogram2d(x, y, bins=bins)
    H = np.rot90(H)
    H = np.flipud(H)
    Hmasked = np.ma.masked_where(H==0, H)
    return xedges, yedges, Hmasked
def get_max_color_value(Hmasked,bins):
    m=0
    for i in range(bins):
        for j in Hmasked[i]:
            if j>m:
               m=j
    return m
def show2pic(rng,tempobs, tempmod,fontsize,text,bins):
    n = np.arange(0, 30, 0.01)
    fig = plt.figure(figsize=[12,12])
    vmax=0
    for i in range(len(text)):
        tempObs=tempobs[i]
        tempMod=tempmod[i]
        x, y ,Hmasked = histogramPoints(tempObs, tempMod, bins) 
        m=get_max_color_value(Hmasked,bins)
        if m>vmax:
           vmax=m
    for j in range(len(text)):
        print(j)
        ax = fig.add_subplot(2,2,j+1)
        tempObs=tempobs[j]
        tempMod=tempmod[j]
        x, y ,Hmasked = histogramPoints(tempObs, tempMod, bins)
        c = ax.pcolormesh(x, y, Hmasked,vmin=0,vmax=vmax)#,vmin=number[i][0],vmax=number[i][1] 
        ax.plot(n, n, 'r-')
        fit = np.polyfit(tempObs, tempMod, 1)
        fit_fn = np.poly1d(fit)
        ax.plot(tempObs, fit_fn(tempObs), 'y-', linewidth=2)
        gradient, intercept, r_value, p_value, std_err = stats.linregress(tempObs, tempMod)
        r_squared=r_value**2
        ax.set_title('%s'%text[j],fontsize=15)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.ylim([-5,35])
        plt.text(x=1,y=31,s=r'$\mathregular{R^2}$='+str(round(r_squared,3)),fontsize=15) 
        #cbar = plt.colorbar(c)
        #cbar.ax.tick_params(labelsize=10)
        if j==1 or j==3: 
           plt.setp(ax.get_yticklabels() ,visible=False)
        if j==0 or j==1:
           plt.setp(ax.get_xticklabels() ,visible=False)
    cax = fig.add_axes([0.91, 0.12, 0.025, 0.78])
    fig.colorbar(c, cax=cax)#, cax=cax
    fig.text(0.5, 0.06, 'Observed temperature($^\circ$C)', ha='center', va='center', fontsize=FONTSIZE)
    fig.text(0.06, 0.5, 'Model temperature($^\circ$C)', ha='center', va='center', rotation='vertical',fontsize=FONTSIZE)
    fig.text(0.5, 0.94, '%s' %rng[0], ha='center', va='center', fontsize=FONTSIZE)
    fig.text(0.97, 0.5, 'Quantity', ha='center', va='center', rotation='vertical',fontsize=FONTSIZE)
    #fig.tight_layout()
    plt.savefig('correlation comparison_bottom.png', dpi=200)
