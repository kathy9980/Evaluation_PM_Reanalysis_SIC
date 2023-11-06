# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 10:30:13 2019
Change all filename in a folder
@author: kathy

20190610 skx created
"""

import os
#print(os.getcwd())

folder = 'D:\\Newdata\\LCCA\\AMSRE_NT2_75\\pkl\\'
folder = 'D:\\Newdata\\LCCA\\UB_ASI_75\\pkl\\'
os.chdir(folder)
fname = os.listdir(os.getcwd())
print(fname)

for temp in fname:
    
    new_name = temp[:-4]+'_75.pkl'
    os.rename(folder+temp,folder+new_name)
    