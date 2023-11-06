# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 17:05:45 2019
计算除去公共空洞后的LCCA  (AMSR2-NT2)
@author: kathy
"""

import glob
import os
import h5py
import numpy as np
#from matplotlib import pyplot  as plt
import time

''' 获取路径下全部文件名 '''
def eachFile(filepath):
    pathDir =  os.listdir(filepath)
    f = []
    for allDir in pathDir:
        child = os.path.join('%s%s' % (filepath, allDir))
        f.append(child)
#        print (child) # .decode('gbk')是解决中文显示乱码问题
    return f
    
''' 读hdf海冰密集度 '''
def ReadSIC(filename):
    f=h5py.File(filename,'r')    
    dset=f['HDFEOS']['GRIDS']['NpPolarGrid12km']['Data Fields']['SI_12km_NH_ICECON_DAY']
    print('ok')
    a = np.array(dset)
    f.close()
    return a
    
''' 统计低值出现频次 '''   
"""
Input: sic,冰密集度日数据; 
       lim1,纬度下限;
       lim2,纬度上限
Output: a_low,低值面积;
        a_total,总面积;
        LCCA,低值面积/总面积  
""" 
def CountLow(sic,lim1,lim2):
    Lat = np.load('D:\\Arctic\\data\\GeoData\\r12.5km\\Lat_12.npy')
#    Lat = np.load('D:\\Arctic\\LowValue_winter\\GeoData\\r12.5km\\Lat_12.npy')
    hLat = np.array(Lat)
    Pix_Area = np.load('D:\\Arctic\\data\\GeoData\\r12.5km\\Pix_Area_12.npy')
#    Pix_Area = np.load('D:\\Arctic\\LowValue_winter\\GeoData\\r12.5km\\Pix_Area_12.npy')
    Pix_Area = np.array(Pix_Area)
    
    hLat[hLat<lim1] = np.nan  # 小于lim1的Lat置作nan;
    sic[hLat != hLat] = 999  #  纬度小于lim1区域的SIC记作999
    sic[hLat>lim2] = 999  # 纬度大于lim2区域的SIC记作999
#    a_hole = np.sum(Pix_Area[hdata != hdata])
#    print('未去除的空洞面积(nan)：%f' %a_hole)
    '''统计研究范围总面积 —— 非999的面积'''
    a_total = np.sum(Pix_Area[sic != 999])
#    print('总面积：%f' %a_total)  #  显示总面积
    '''统计低值面积 —— 小于75%且大于15%'''
    a_low = np.sum(Pix_Area[sic<75]) - np.sum(Pix_Area[sic<15])  
#    print('低值面积：%f' %a_low)  #  显示低值个数
    return a_low,a_total,a_low/a_total*100

''' main 函数  '''
#start = time.clock()

#FilePath = "D:\\AMSR2-NT2\\2012\\B01\\test\\"  #测试路径
FilePath = "D:\\AMSR2-NT2\\2018\\" 
FileName = eachFile(FilePath)
LowArea = []
ts = []
for filename in FileName:
    s = filename.split('\\')[-1].split('_')[-1].split('.')[0]
    print(s)
    SIC = ReadSIC(filename)
    lowarea = CountLow(SIC,84,88.3)
    ts.append(s)
    LowArea.append(lowarea)
output = dict(zip(ts,LowArea))
year = filename.split('\\')[-1].split('_')[-1].split('.')[0][:4]
outname = year+'_LowArea_PubHole_75'

#  1.保存为yyyy_LowArea.pkl  ##  
import pickle
outfile = open('D:\\Newdata\\LCCA\\AMSR2_NT2_75\\'+outname+'.pkl', 'wb')
pickle.dump(output,outfile)
outfile.close()
##  2.保存为yyyy_LowArea.txt  ##  
outfile = open('D:\\Newdata\\LCCA\\AMSR2_NT2_75\\'+outname+'.txt','w')  
outfile.write(str(output)) 
outfile.close()
print(outname+' save')

#end = time.clock()
#print('\n运行时间: %f' %(end-start))  # 显示运行时间
print('success')






