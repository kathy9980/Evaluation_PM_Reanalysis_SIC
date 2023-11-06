# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 15:25:51 2019
计算除去公共空洞后的LCCA  (ERA5)
@author: kathy
"""

import os
import netCDF4
from netCDF4 import Dataset
import numpy as np
from matplotlib import pyplot  as plt
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

''' Read date'''
def ReadDate(filename):
    file = Dataset(filename)
    # Read date
    T = file.variables['time']
    date = netCDF4.num2date(T[:], T.units, T.calendar)
    
    file.close()
    return date

''' 读nc海冰密集度 '''
def ReadSIC(filename,day):
    file = Dataset(filename)
    
    # Read sic
    sic = file.variables['siconc'][day]
    # Read lat
    lat = file.variables['latitude'][:]
    # 限定研究范围在84N~88.3N
    lim1 = np.where(lat==88.25)[0][0]
    lim2 = np.where(lat==83.75)[0][0]
    sic = sic[lim1:lim2,:]   
    
    file.close()
    return sic
    
''' 统计低值出现频次 '''   
"""
Input: data,冰密集度日数据; 
       lim1,纬度下限;
       lim2,纬度上限
Output: a_low,低值面积;
        a_total,总面积;
        LCCA,低值面积/总面积  
""" 

def CountLow(data,Grid_Area):

#    Grid_Area = np.load('C:\\Users\\kathy\\research\\Sea-ice-concentration\\data\\ERA 5\\Geodata\\Grid_Area_125.npy')
#    Grid_Area = Grid_Area[14:48,:]  # 84N~88.3N
    ''' 统计研究范围总面积 —— 84N~90N '''
    a_total = np.sum(Grid_Area)  
#    print('总面积：%f' %a_total)  #  显示总面积
    '''统计低值面积 —— sic小于75%且大于15%'''
    a_low = np.sum(Grid_Area[data<0.75])-np.sum(Grid_Area[data<0.15])
#    print('低值面积：%f' %a_low)  #  显示低值面积
    lcca = a_low/a_total*100 
    return a_low,a_total,lcca


''' main 函数  '''
#start = time.clock()

# 测试路径
#FilePath = "D:\\AMSR2-NT2\\2012\\B01\\test\\"  
# 测试文件
#filename = "C:\\Users\\kathy\\research\\Sea-ice-concentration\\data\\ERA 5\\2002_2018\\era5_sic_20020601_20021031.nc"

FilePath = "C:\\Users\\kathy\\research\\Sea-ice-concentration\\data\\ERA 5\\2002_2018\\"
FileName = eachFile(FilePath)

# =============================================================================
# Read cell area
# =============================================================================
f = Dataset('C:\\Users\\kathy\\research\\Sea-ice-concentration\\data\\ERA 5\\Geodata\\ERA_dot25_gridarea.nc')
cell_area = f.variables['cell_area'][:]
# Read lat
lat = f.variables['latitude'][:]
# 限定研究范围在84N~88.3N
lim1 = np.where(lat==88.25)[0][0]
lim2 = np.where(lat==83.75)[0][0]
cell_area = cell_area[lim1:lim2,:]
f.close()

# =============================================================================
# Year Loop
# =============================================================================

for filename in FileName:
    LowArea = []
    ts = []
    
    # Read date
    Date = ReadDate(filename)
    yr = Date[0].year
    
    for i in range(len(Date)):
        # Read sea-ice-concentration
        SIC = ReadSIC(filename,i)
        # Calculate lcca
        lowarea = CountLow(SIC,cell_area)
        LowArea.append(lowarea)
        # Record date
        dt = Date[i].strftime("%Y%m%d")
        ts.append(dt)
    
        output = dict(zip(ts,LowArea))

    # =============================================================================
    #  Save LCCA
    # =============================================================================
    outname = str(yr)+'_LowArea_PubHole_75'
    
    #  1.保存为yyyy_LowArea.pkl  ##  
    import pickle
    outfile = open('D:\\Newdata\\LCCA\\ERA5_75\\'+outname+'.pkl', 'wb')
    pickle.dump(output,outfile)
    outfile.close()
    
    ##  2.保存为yyyy_LowArea.txt  ##  
    outfile = open('D:\\Newdata\\LCCA\\ERA5_75\\'+outname+'.txt','w')  
    outfile.write(str(output)) 
    outfile.close()
    print(outname+' save')
    
    #end = time.clock()
    #print('\n运行时间: %f' %(end-start))  # 显示运行时间
    print('success')






