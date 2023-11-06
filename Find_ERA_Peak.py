# -*- coding: utf-8 -*-
"""
Created on Sun Jun  3 09:53:29 2018
Read ERA File & Find LCCA Peak
@author: skx 
"""
import numpy as np
import struct
import matplotlib.pyplot as plt

if __name__ == "__main__":
    
    ''' Step1. Read Grid lcca'''
    fid=open('D:\\Arctic\\LC\\era_lcca_2009_2016.grd','rb')  
    m = fid.seek(0,2)  # 文件指针指向文件末尾
    fid.seek(0)  # 文件指针指向data开始的位置
    lcca = []
    where = 0
    n=1000
    try:
        while where != m:
            data = struct.unpack("f",fid.read(4))   
            lcca.append(data[0]*100)  ## 单位：%
            where = fid.tell()
    finally:
        fid.close()
    
    '''Step2. Year Loop'''
    for year in range(2009,2017):  ## 2009 - 2016年
        n = year-2009
        LCCA = lcca[122*n:122*(n+1)]
        #LCCA = lcca[0:122]  ## 2009-2016
        
        '''Step2.1 Find LCCA Peak'''
        ## GitHub py-findpeaks 
        ## (https://github.com/MonsieurV/py-findpeaks)
        ## thres 幅度阈值
        ## min_dist 最小距离
        import peakutils   
        LCCA = np.array(LCCA)
        Peak_Ind = peakutils.indexes(LCCA,thres=0.02/max(LCCA), min_dist=5)
        
        from datelist import datelist
        X = datelist(str(year)+"-06-01",str(year)+"-09-30")
        for i in range (len(Peak_Ind)):
            ind = Peak_Ind[i]
            print('%10s %f'%(X[ind],LCCA[ind]))  # 日期 峰值
            
        '''Step2.2 Plot Peak Figure'''
        
        fig = plt.subplots(figsize=(8, 6))   
        ax = plt.gca()    
        plt.plot(LCCA,'b-')
        plt.plot(Peak_Ind,LCCA[Peak_Ind],'ro')
        plt.savefig(str(year)+'.jpg')
    
    
    print('success')
    
    