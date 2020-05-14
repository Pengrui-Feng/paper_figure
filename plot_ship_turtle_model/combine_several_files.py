import glob
import os
import pandas as pd
inputfile = str(os.path.dirname(os.getcwd()))+"content/drive/My Drive/PENGRUI/merge_nosplit/tu55_merge_td_gps.csv"
outputfile =  str(os.path.dirname(os.getcwd()))+"/content/drive/My Drive/all_merge_td_gps.csv"
csv_list = glob.glob(inputfile)

filepath =  csv_list [0]
df = pd.read_csv(filepath)#,encoding='ISO-8859-1')
df = df.to_csv(outputfile,index=False)

for i in range(1,len(csv_list)):
    filepath = csv_list [i]
    df = pd.read_csv(filepath)#,encoding='ISO-8859-1',lineterminator="\n",error_bad_lines=False)
    df = df.to_csv(outputfile,index=False, header=False,mode='a+')
