# -*- coding: utf-8 -*-
"""
Python script for gcs2pcs, remapping and interpolation
Created on Wed Apr 10 10:34:27 2019
@author: Kexin Song
20190410 skx created from gcs2pcs_demo.ipynb
20190410 skx saved grid_z.nc
"""

from pyproj import Proj, transform
from netCDF4 import Dataset
import numpy as np


"Convert coordinate system 2"
'''EPSG 4326 to EPSG 3411'''
def ConCoor(x1,y1,z1):
    inProj = Proj(init='epsg:4326')
    outProj = Proj(init='epsg:3411')
    x2,y2,z2 = transform(inProj,outProj,x1,y1,z1)
#     x2,y2 = transform(inProj,outProj,x1,y1)
    #print(x2,y2)
    return x2,y2,z2
# return x2,y2


"Load Data"
def ReadERA(filename):
    file = Dataset(filename)
    Lon = file.variables['longitude'][:]
    Lat = file.variables['latitude'][:] 
    sic = file.variables['ci'][0][:][:]    # only read the first day
    file.close()
    return sic,Lon,Lat

"Load X and Y"
def ReadXYZ(filename):
    file = Dataset(filename)
    x = file.variables['x'][:]
    y = file.variables['y'][:] 
    z = file.variables['z'][:]
    file.close()
    return x,y,z

#------------------------------------------------------------------------
if __name__ == '__main__':
    filename = "C:\\Users\\kathy\\research\\Sea-Ice-Concentration\\data\\ERA 5\\20180904-20180906.nc"
    sic0,lon,lat0 = ReadERA(filename)
#     print(np.shape(sic0))
    lat=lat0[lat0>30]
    sic=sic0[lat0>30,:]
    print(np.mean(sic))
    print(np.shape(lon),np.shape(lat),np.shape(sic))
    print(np.min(lat),np.max(lat))
    print(np.min(lon),np.max(lon))
    
    ''' 1 - projection '''
    
    x=np.zeros((240,1440))
    y=np.zeros((240,1440))
    z=np.zeros((240,1440))
    for i in range(len(lat)):
        for j in range(len(lon)):
            x[i,j],y[i,j],z[i,j]=ConCoor(lon[j],lat[i],sic[i,j])
    row=np.shape(x)[0]
    col=np.shape(x)[1]
    print(row,col)    # row,column

    ''' 2 - griddata'''
    
    points=np.zeros((row*col,2))
    points[:,0]=np.reshape(x,row*col,1)
    points[:,1]=np.reshape(y,row*col,1)
    values=np.reshape(z,row*col,1)
    
    filename = "C:/Users/kathy/research/Sea-ice-concentration/data/UB/sic/asi-AMSR2-n6250-20180905-v5.4.nc"
    x2,y2,z2 = ReadXYZ(filename)
    grid_x,grid_y = np.meshgrid(x2,y2)
    
    from scipy.interpolate import griddata
    grid_z = griddata(points,values,(grid_x,grid_y),method='nearest')
    
    ' display grid_z'
    import matplotlib.pyplot as plt
    fig=plt.figure(figsize=(12,17))
    plt.pcolormesh(grid_z)
    plt.show()
    
    ' save grid_z.nc'
    # create nc file
    f = Dataset('grid_z.nc','w')
    # define dimensions
    x = f.createDimension("x",1216)
    y = f.createDimension("y",1792)
    # create variables
    xs = f.createVariable("xs","f4",("x",))
    ys = f.createVariable("ys","f4",("y",))
    zs = f.createVariable("zs","f4",("y","x"))
    # add attributes
    import time
    f.description = "projected and grided ERA5 sic"
    f.history = "Created "+time.ctime(time.time())
    xs.description = "x coordinates of projection"
    ys.description = "y coordinates of projection"
    zs.description = " projected and grided ERA 5 sea ice concentration"
    xs.units = "m"
    ys.units = "m"
    # write data to variables
    xs[:] = x2
    ys[:] = y2
    zs[:,:] = grid_z
    f.close()
    
#    ''' 2' - remapping'''
#    x1=np.zeros((2200,2200))
#    y1=np.zeros((2200,2200))
#    map1=np.zeros((2200,2200))
#    cnt1=np.zeros((2200,2200))
#    for i in range(row):
#        for j in range(col):
#            xx=x[i,j]
#            yy=y[i,j]
#    #         r=np.sqrt(x**2+y**2)
#            imap=int(np.round(xx/6250.0+616))
#            jmap=int(np.round(yy/6250.0+856))
#            x1[imap,jmap]=x1[imap,jmap]+xx
#            y1[imap,jmap]=x1[imap,jmap]+yy
#            map1[imap,jmap]=map1[imap,jmap]+sic[i,j]
#            cnt1[imap,jmap]=cnt1[imap,jmap]+1.0
#    x1=x1/cnt1
#    y1=y1/cnt1
#    map1=map1/cnt1
#    print(np.mean(sic))
#    print(np.nanmean(map1))
#    print('ok')
#    
#    ''' 3' - interpolation'''
#    filename = "C:/Users/kathy/research/Sea-ice-concentration/data/UB/sic/asi-AMSR2-n6250-20180905-v5.4.nc"
#    x2,y2,sic2 = ReadXYZ(filename)
#    
#    map2 = map1[0:1216,0:1792].T
#    d = sic2-map2
    
#    ''' display sic maps '''
#    import matplotlib.pyplot as plt
#    fig=plt.figure(figsize=(12,17))
#    plt.pcolormesh(map[0:1216,0:1792].T)
#    plt.show()
