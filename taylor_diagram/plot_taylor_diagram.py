# -*- coding: utf-8 -*-
"""

Created on Mon 17 Aug  15:04:25 2020
@author: Pengrui
"""
! pip install XlsxWriter
! pip install SkillMetrics
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import skill_metrics as sm   #  ! pip install SkillMetrics
from scipy import stats
#################### functions ############################
def taylor_statistics(p, r):       
    # Calculate bias (B)
    bias = np.mean(p) - np.mean(r)
    # Calculate correlation coefficient
    ccoef = np.corrcoef(p,r)
    ccoef = ccoef[0]
    # Calculate centered root-mean-square (RMS) difference (E')^2
    crmsd = [0.0, sm.centered_rms_dev(p,r)]
    # Calculate standard deviation of predicted field w.r.t N (sigma_p)
    sdevp = np.std(p)    
    # Calculate standard deviation of reference field w.r.t N (sigma_r)
    sdevr = np.std(r)
    sdev = [sdevr, sdevp];
    # Store statistics in a dictionary
    stats = {'ccoef': ccoef, 'crmsd': crmsd, 'sdev': sdev, 'bias': bias}
    return stats
def str2list(s, bracket=False):
    if bracket:
        s = s[1:-1]
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
##################################### hardcodes ###############################
path='/content/drive/My Drive/'
data = pd.read_csv(path+'matched_ship_turtle_models.csv')
#######################main##########################
data=data[data['FVCOM_temp'].str.contains('nan') == False]   ### delate the rows if it includes 'nan' 
data=data[data['ROMS_temp'].str.contains('nan') == False]
shipdepth=pd.Series(str2ndlist(data['ship_depth']))
shiptemp=pd.Series(str2ndlist(data['ship_temp']))
ttemp = pd.Series(str2ndlist(data['turtle_temp']))
tdepth = pd.Series(str2ndlist(data['turtle_depth']))
fvcomTemp = pd.Series(np.array(str2ndlist(data['FVCOM_temp'], bracket=True)))
espressoTemp = pd.Series(np.array(str2ndlist(data['ROMS_temp'], bracket=True)))

bottom_depth=[]
t_temp=[] 
s_temp=[]
r_temp=[]
f_temp=[]
for i in range(len(data)):
    for k in range(len(shipdepth[i])):
        if tdepth[i][-1]==shipdepth[i][k]:
            bottom_depth.append(tdepth[i][-1])
            t_temp.append(ttemp[i][-1])
            s_temp.append(shiptemp[i][k])
            r_temp.append(espressoTemp.values[i][-1])
            f_temp.append(fvcomTemp.values[i][-1])  

Data = pd.DataFrame({'turtle_temp':t_temp,'ship_temp':s_temp,'fvcom_temp':f_temp,'roms_temp':r_temp,'bottom_depth':bottom_depth})
Data['ENSEMBLE_T'] = 1.000000
# Calculate statistics for Taylor diagram
taylor_stats1 = taylor_statistics(Data.ship_temp, Data.turtle_temp)
taylor_stats2 = taylor_statistics(Data.fvcom_temp, Data.turtle_temp)
taylor_stats3 = taylor_statistics(Data.roms_temp, Data.turtle_temp)
taylor_stats4 = taylor_statistics(Data.ENSEMBLE_T, Data.turtle_temp)
 # Store statistics in arrays
sdev = np.array([taylor_stats1['sdev'][0], taylor_stats4['sdev'][1], 
                 taylor_stats2['sdev'][1], taylor_stats3['sdev'][1],
                 taylor_stats1['sdev'][1]])
crmsd = np.array([taylor_stats1['crmsd'][0], taylor_stats4['crmsd'][1], 
                  taylor_stats2['crmsd'][1], taylor_stats3['crmsd'][1],
                  taylor_stats1['crmsd'][1]])
ccoef = np.array([taylor_stats1['ccoef'][0], taylor_stats4['ccoef'][1], 
                  taylor_stats2['ccoef'][1], taylor_stats3['ccoef'][1],
                  taylor_stats1['ccoef'][1]])
bias  = np.array([0, taylor_stats4['bias'], taylor_stats2['bias'],
                  taylor_stats3['bias'], taylor_stats1['bias']])
label = ['Non-Dimensional Observation', 'E', 'G', 'F', 'D']
sm.taylor_diagram(sdev, crmsd, ccoef, markerLabel = label,
                      locationColorBar = 'EastOutside',
                      markerDisplayed = 'colorbar', titleColorBar = 'Bias',# 
                      markerLabelColor='r', markerSize=10,
                      markerLegend='off', cmapzdata=bias,
                      colRMS='g', styleRMS=':', widthRMS=2.0, titleRMS='on',
                      colSTD='b', styleSTD='-.', widthSTD=1.0, titleSTD ='on',
                      colCOR='k', styleCOR='--', widthCOR=1.0, titleCOR='on')
# Write plot to file
plt.savefig('Taylor_Diagram.png')
# Show plot
plt.show()
