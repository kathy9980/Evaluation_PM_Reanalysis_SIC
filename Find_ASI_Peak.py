# -*- coding: utf-8 -*-
"""
Created on Sun Jun  4 09:53:29 2018
Read ASI File & Find LCCA Peak
@author: skx 
"""
import numpy as np
import pickle
import os
import datetime as dt
import matplotlib.pyplot as plt


''' 获取路径下全部文件名 '''
def eachFile(filepath):
    pathDir =  os.listdir(filepath)
    f = []
    for allDir in pathDir:
        child = os.path.join('%s%s' % (filepath, allDir))
        f.append(child)
#        print (child) # .decode('gbk')是解决中文显示乱码问题
    return f

''' 读取yyyy_LowNum.pkl中的数据'''
"""
Input: yyyy_LowNum.pkl文件名
Output: LCCA, Low Concentration in Central Arctic  
"""
def ReadDic(filename):
    pkl_file = open(filename, 'rb')
    data = pickle.load(pkl_file)
    s_data = sorted(data.items(),key = lambda asd:asd[0])  # 字典排序
    lcca = []  # 低密集度指数 LCCA = Low Concentration in Central Arctic
    dates = []
    for j in s_data: 
        if j[0][9:12]!='NT2':
            date = j[0][-15:-7]  # 获取日期ASI
        else:
            date = j[0][-12:-4]  # 获取日期NT2
        dates.append(dt.datetime.strptime(date,"%Y%m%d"))
        lcca.append(j[1][2])
    pkl_file.close()
    return dates, lcca

if __name__ == "__main__":
    
    FilePath = 'D:\\Arctic\\result\\result_v2\\result_ASI_PubHole\\'  # ASI 75
    SavePath = 'D:\\Arctic\\figures\\LCCA_Peak_ASI\\' 
#    test file filename ='D:\\Arctic\\result\\result_v2\\result_ASI_PubHole\\2011_LowArea_PubHole.pkl'

    '''Step1. Year Loop'''
    FileName = eachFile(FilePath)
    f = open(SavePath+'LCCA_Peak_ASI.txt','w')
    for i in range(2002,2018):  ##  遍历年份 2002 2017
        num=i-2002
        year=i
        ''' Step1. Read PKL lcca'''
        date,LCCA = ReadDic(FileName[num])
        
        '''Step2.1 Find LCCA Peak'''
        ## GitHub py-findpeaks 
        ## (https://github.com/MonsieurV/py-findpeaks)
        ## thres 幅度阈值
        ## min_dist 最小距离
        ## 输出：日期 峰值
        ''' '''
        import peakutils   
        LCCA = np.array(LCCA)
        Peak_Ind = peakutils.indexes(LCCA,thres=0.02/max(LCCA), min_dist=5)
        Peak_Value = LCCA[Peak_Ind]
        Peak_Ind_2 = Peak_Ind[Peak_Value>=1]
    
        for i in range (len(Peak_Ind_2)):
            ind = Peak_Ind_2[i]
            f.write('%10s %.2f'%(date[ind].date(),LCCA[ind]))
            f.write('\n')
#            print('%10s %f'%(date[ind].date(),LCCA[ind]))  # 输出：日期 峰值
        f.write('\n')
        print('\n')  
        
        '''Step2.2 Plot Peak Figure'''
        
        fig = plt.subplots(figsize=(8, 6))   
        ax = plt.gca()    
        plt.plot(LCCA,'b-')
        
        plt.plot(Peak_Ind_2,LCCA[Peak_Ind_2],'ro')
        plt.xlim([0,365])
        plt.savefig(SavePath+str(year)+'.jpg')
        plt.close()
    f.close()
    
    print('success')
