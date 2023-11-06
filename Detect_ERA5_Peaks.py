# -*- coding: utf-8 -*-
"""
Created on Fri May  3 08:44:15 2019
Detect LCCA peaks by scipy.signal.find_peaks
@author: kathy

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
    s_data = sorted(data.items(),key = lambda asd:asd[0])  # 字典排序
    lcca = []  # 低密集度指数 LCCA = Low Concentration in Central Arctic
    dates = []
#    for j in s_data: 
    for j in s_data[:136]: # AMSRE_NT2
#        date = j[0]  # 获取日期
#        date = j[0][-12:-4]  # 获取日期 AMSRE_NT2
        date = j[0][-15:-7]  # 获取日期 ASI
        dates.append(dt.datetime.strptime(date,"%Y%m%d"))
        lcca.append(j[1][2])
    pkl_file.close()
    return dates, lcca

if __name__ == "__main__":

#    FilePath = 'D:\\Newdata\\LCCA\\ERA5_75\\pkl\\'  # ERA5 LCCA
#    FilePath = 'D:\\Newdata\\LCCA\\AMSRE_NT2_75\\pkl\\'  # AMSRE NT2 LCCA
#    FilePath = 'D:\\Newdata\\LCCA\\AMSR2_NT2_75\\pkl\\'  # AMSR2 NT2 LCCA
    FilePath = 'D:\\Newdata\\LCCA\\UB_ASI_75\\pkl\\'
    
    SavePath = 'D:\\Newplot\\' 
    
    year = np.arange(2002,2003,1)
    for i in year:
        filename = FilePath+str(i)+"_LowArea_PubHole_75.pkl"
#     filename = FilePath+"2018_LowArea_PubHole_75.pkl"
    
        # Read LCCA data
        Dates,LCCA = ReadData(filename)    

        # Detect LCCA Peaks
        p_ind,_ = find_peaks(LCCA,height=5,distance=7)
        
        ''' Save Peaks info in .txt file '''
        f = open(SavePath+str(i)+'_LCCA_Peak_ERA5.txt','w')
        
        for j in range (len(p_ind)):
            ind = p_ind[j]
            f.write('%10s %.2f'%(Dates[ind].date(),LCCA[ind]))
            f.write('\n')
            print('%10s %f'%(Dates[ind].date(),LCCA[ind]))  # 输出：日期 峰值
        f.write('\n')
        print('\n')  
        f.close()

        ''' Plot LCCA with peaks '''
        LCCA = np.array(LCCA)    
        Dates = np.array(Dates)
        
        import matplotlib.pyplot as plt
        
#        plt.plot(Dates,LCCA,'seagreen',label='ERA 5')
#        plt.plot(Dates,LCCA,'magenta',label='NT2')
        plt.plot(Dates,LCCA,'blue',label='ASI')
        plt.plot(Dates[p_ind],LCCA[p_ind],"*",color="purple",label="Peaks")
        
        
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
        plt.ylabel("LCCA Index (%)",fontsize=16)

        plt.show()
#        plt.savefig(SavePath+str(i)+'_LCCA_Peak_ERA5.jpg')
        plt.savefig(SavePath+str(i)+'_LCCA_Peak_NT2.jpg')
        plt.close()
    
    print("finished")
        
