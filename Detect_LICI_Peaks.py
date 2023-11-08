# -*- coding: utf-8 -*-
"""
Created on Fri May  3 08:44:15 2019
Detect LICI peaks uisng <scipy.signal.find_peaks>
@author: Kexin Song

20190610 skx add comments, apply to NT2/ASI products
"""
import datetime as dt
import numpy as np
from netCDF4 import Dataset
from scipy.signal import find_peaks
import pickle

def ReadData(filename):
    pkl_file = open(filename, 'rb')
    data = pickle.load(pkl_file)
    s_data = sorted(data.items(),key = lambda asd:asd[0])  # sort the dictionary
    lici = []                                              # LICI means "Low Concentration in Central Arctic"
    dates = []
#    for j in s_data: 
    for j in s_data[:136]: # AMSRE_NT2
#        date = j[0]  
#        date = j[0][-12:-4]  # access date AMSRE_NT2
        date = j[0][-15:-7]  # access date ASI
        dates.append(dt.datetime.strptime(date,"%Y%m%d"))
        lici.append(j[1][2])
    pkl_file.close()
    return dates, lici

if __name__ == "__main__":

#    FilePath = 'D:\\Newdata\\LICI\\ERA5_75\\pkl\\'  # ERA5 LICI
#    FilePath = 'D:\\Newdata\\LICI\\AMSRE_NT2_75\\pkl\\'  # AMSRE NT2 LICI
#    FilePath = 'D:\\Newdata\\LICI\\AMSR2_NT2_75\\pkl\\'  # AMSR2 NT2 LICI
    FilePath = 'D:\\Newdata\\LICI\\UB_ASI_75\\pkl\\'
    
    SavePath = 'D:\\Newplot\\' 
    
    year = np.arange(2002,2003,1)
    for i in year:
        filename = FilePath+str(i)+"_LowArea_PubHole_75.pkl"
    
        # Read LICI data
        Dates,lici = ReadData(filename)    

        # Detect LICI Peaks
        p_ind,_ = find_peaks(lici,height=5,distance=7)
        
        ''' Save Peaks info in .txt file '''
        f = open(SavePath+str(i)+'_lici_Peak_ERA5.txt','w')
        
        for j in range (len(p_ind)):
            ind = p_ind[j]
            f.write('%10s %.2f'%(Dates[ind].date(),lici[ind]))
            f.write('\n')
            print('%10s %f'%(Dates[ind].date(),lici[ind]))  # ouputs：date, peak LICI value
        f.write('\n')
        print('\n')  
        f.close()

        ''' Plot lici with peaks '''
        lici = np.array(lici)    
        Dates = np.array(Dates)
        
        import matplotlib.pyplot as plt
        
#        plt.plot(Dates,lici,'seagreen',label='ERA 5')
#        plt.plot(Dates,lici,'magenta',label='NT2')
        plt.plot(Dates,lici,'blue',label='ASI')
        plt.plot(Dates[p_ind],lici[p_ind],"*",color="purple",label="Peaks")
        
        
        ''' only work for NT2 year 2012 '''
        if i==2011 or 2012:
            import matplotlib.dates as mdates
            from datetime import datetime        
            xdates = [str(i)+'0106',str(i)+'0107',str(i)+'0108',\
              str(i)+'0109',str(i)+'0110',str(i)+'0111']
            xticks = [datetime.strptime(d,'%Y%d%m').date() for d in xdates]
            xtick = plt.xticks(xticks)
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))  # 只显示月份
        ''' only work for missing data years '''
        
        plt.ylim(-1,65)
        
        plt.legend(loc=2)
        
        plt.xlabel("Time",fontsize=16)
        plt.ylabel("lici Index (%)",fontsize=16)

        plt.show()
#        plt.savefig(SavePath+str(i)+'_lici_Peak_ERA5.jpg')
        plt.savefig(SavePath+str(i)+'_lici_Peak_NT2.jpg')
        plt.close()
    
    print("finished")
        
