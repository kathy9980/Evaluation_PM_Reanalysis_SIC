# -*- coding: utf-8 -*-
"""
Create AU_S112_download.txt
@author: kathy
20190223 skx created
"""

#import numpy as np

#s="https://n5eil01u.ecs.nsidc.org/AMSA/AU_SI12.001/2012.07.02/AMSR_U2_L3_SeaIce12km_B01_20120702.he5"
#
#year=["2012","2013","2014","2015","2016","2017","2018"]
#month=["01","02","03","04","05","06","07","08","09","10","11","12"]
#day=
#for

import urllib.request

## add Cookie and User-Agent
Cookie = "_ga=GA1.2.58193538.1548172561; _gid=GA1.2.1002168608.1550498008; _ga=GA1.3.58193538.1548172561; _ga=GA1.4.58193538.1548172561; _gid=GA1.4.1002168608.1550498008; _urs-gui_session=a72687f82162745fe3e1c546bf99bc07"
User = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36"
headers = {'Cookie': Cookie,
           'User-Agent': User
           }

rawurl = "https://n5eil01u.ecs.nsidc.org/AMSA/AU_SI12.001/2012.07.02/"

## 1. use urllib
req = urllib.request.Request(url=rawurl, headers=headers)
content = urllib.request.urlopen(req)
html=content.read().decode('utf-8')


## 2. use requests
import requests
req2 = requests.get(url=rawurl,headers=headers).content

#with open('C:\Users\kathy\research\Sea-ice-concentration\p_pro\test\t.txt','wb') as f:
#    f.write(req2)


import re
urls = re.findall(r'<href="AMSR_U2_L3_SeaIce12km_B01_.*\.he5">',html)  # 正则表达式
print(urls)
#
#from bs4 import BeautifulSoup
#soup = BeautifulSoup(req2,'lxml')
##link = soup.find_all('a')[6:-216] 
#for a in soup.find_all('a'):
#    link = a['href']
#    print(link)
    
    
print('success')    
#from bs4 import BeautifulSoup
#import requests
#

#
##rawurl = "https://daacdata.apps.nsidc.org/pub/DATASETS/nsidc0081_nrt_nasateam_seaice/south/"
#rawurl = "https://n5eil01u.ecs.nsidc.org/AMSA/AU_SI12.001/2012.07.02/"
#resp = requests.get(rawurl, headers=headers).text
#soup = BeautifulSoup(resp, 'lxml')


#link = soup.find_all('a')[6:-216] # 类似于前面介绍的方法，获取文件的url
#link_dup = []
#for i in link:
#    a = i.get('href')
#    link_dup.append(a)
#link_all = list(set(link_dup)) #列表重复了一遍，可以用set进行去重，再重新排序
#link_all.sort(key=link_dup.index)
#crawler_url = []
#file_name = "C:\\Users\\kathy\\test.txt"
#for i in link_all:
#    a = rawurl + i
#    crawler_url.append(a)
#for i, url in enumerate(crawler_url):
#    r = requests.get(url, headers=headers)
#    with open(file_name, "wb") as code: 
#        code.write(r.content)
