# -*- coding: utf-8 -*-
"""
Program for downloading AMSR2 NT2 SIC 12.5km data(AU_S125) 
URL: https://n5eil01u.ecs.nsidc.org/AMSA/AU_SI12.001/
@author: Kexin Song

20190221 skx created
20190223 skx updated
"""


## test 1
#
#from urllib.request import HTTPPasswordMgrWithDefaultRealm,HTTPBasicAuthHandler,build_opener
#from urllib.error import URLError
#
#username='put your username'
#password='put your password'
#url='https://n5eil01u.ecs.nsidc.org/AMSA/AU_SI12.001/'
#p = HTTPPasswordMgrWithDefaultRealm()
#p.add_password(None,url,username,password)
#auth_handler = HTTPBasicAuthHandler(p)
#opener = build_opener(auth_handler)
#
#try:
#    result = opener.open(url)
#    html = result.read().decode('utf-8')
#    print(html)
#except URLError as e:
#    print(e.reason)
    
    
## test 2
#from requests import session,Request
#from bs4 import BeautifulSoup as bs
#
## 创建session请求对象，保存登录会话请求u
#session_req=session()
#
## 需要传输的参数
#postData={
#    "username":"Kexin.Song",
#    "password":"Kathy-mao3gou4"
#}
#
## 需要登录的URL
#login_url="https://urs.earthdata.nasa.gov/home"
#
##PreparedRequest请求预处理
#req=Request(
#    'post',
#    login_url,
#    data=postData,
#    headers=dict(referer=login_url)
#)
#prepped=req.prepare()
#
##将处理的请求参数通过session请求对象发送过去
#resp=session_req.send(prepped)
#
##用BeautifulSoup处理登录之后返回的数据
#soup=bs(resp.content,"html.parser")
#
##打印输出
#print(soup.prettify())
#    
#theurl = 'https://n5eil01u.ecs.nsidc.org/AMSA/'
#req = urllib.request.urlopen(theurl)
#print(req.getcode())



# test 3
#!/usr/bin/python
 
  
 
#import requests # get the requsts library from https://github.com/requests/requests
# 
# 
# 
## overriding requests.Session.rebuild_auth to mantain headers when redirected
# 
#class SessionWithHeaderRedirection(requests.Session):
# 
#    AUTH_HOST = 'urs.earthdata.nasa.gov'
# 
#    def __init__(self, username, password):
# 
#        super().__init__()
# 
#        self.auth = (username, password)
# 
#  
# 
#   # Overrides from the library to keep headers when redirected to or from
# 
#   # the NASA auth host.
# 
#    def rebuild_auth(self, prepared_request, response):
# 
#        headers = prepared_request.headers
# 
#        url = prepared_request.url
# 
#  
# 
#        if 'Authorization' in headers:
# 
#            original_parsed = requests.utils.urlparse(response.request.url)
# 
#            redirect_parsed = requests.utils.urlparse(url)
# 
#  
# 
#            if (original_parsed.hostname != redirect_parsed.hostname) and redirect_parsed.hostname != self.AUTH_HOST and original_parsed.hostname != self.AUTH_HOST:
# 
#                del headers['Authorization']
# 
#  
# 
#        return
# 
#  
# 
## create session with the user credentials that will be used to authenticate access to the data
# 
#username = "Kexin.Song"
# 
#password= "Kathy-mao3gou4"
# 
#session = SessionWithHeaderRedirection(username, password)
# 
#  
# 
## the url of the file we wish to retrieve
# 
##url = "http://e4ftl01.cr.usgs.gov/MOLA/MYD17A3H.006/2009.01.01/MYD17A3H.A2009001.h12v05.006.2015198130546.hdf.xml"
#url = "https://n5eil01u.ecs.nsidc.org/AMSA/AU_SI12.001/2016.06.28/AMSR_U2_L3_SeaIce12km_B01_20160628.he5"
#  
# 
## extract the filename from the url to be used when saving the file
# 
#filename = url[url.rfind('/')+1:]  
# 
#  
# 
#try:
# 
#    # submit the request using the session
# 
#    response = session.get(url, stream=True)
# 
#    print(response.status_code)
# 
#  
# 
#    # raise an exception in case of http errors
# 
#    response.raise_for_status()  
# 
#  
# 
#    # save the file
# 
#    with open(filename, 'wb') as fd:
# 
#        for chunk in response.iter_content(chunk_size=896*608):
# 
#            fd.write(chunk)
# 
#  
# 
#except requests.exceptions.HTTPError as e:
# 
#    # handle any errors here
# 
#    print(e)




#def getResponse(url):
#    url_response = urllib.request.urlopen(url)
#    print (url_response.getcode())
#    '''
#    getcode(): 返回响应的HTTP状态代码  
#      100-199 用于指定客户端应相应的某些动作。 
#      200-299 用于表示请求成功。      ------>  200 :-)
#      300-399 用于已经移动的文件并且常被包含在定位头信息中指定新的地址信息。 
#      400-499 用于指出客户端的错误。  ------>  404 :-(
#      500-599 用于支持服务器错误。
#    '''
#    return url_response
#    
#def downLoad(hdfurl,savedir):
#    try:
#        urllib.request.urlretrieve(hdfurl,savedir+hdfurl[-25:])
#    except Exception as e:
#        print (e)
#    finally:
#        print ('%s finished' %hdfurl[-25:])   
#        
#''' main 函数'''
##start = time.clock()
#
#url = "https://n5eil01u.ecs.nsidc.org/AMSA/AU_SI12.001/"   
#saveDir = 'C:\\Users\\kathy\\Downloads\\AU_S112\\'  # 存储路径
#http_response = getResponse(url)
#html = http_response.read().decode('utf-8')  # 网页源代码

##hdflist = re.findall(r'<a.*?href="asi\-.*\-v5.hdf">(.*?)</a>',html)  # 正则表达式
#hdflist = re.findall(r'<a.*?href="asi\-.*\-v5.4.hdf">(.*?)</a>',html)  # 正则表达式
#print('数据总计：%d' %len(hdflist))
#
### 1.python 下载
##for i in hdflist:
##    hdfUrl = url+i
##    downLoad(hdfUrl,saveDir)
#
## 2.迅雷 下载  (获取下载链接xunlei，拷贝至迅雷下载)
#xunlei = []
#for j in hdflist:
#    xunlei.append(url+j)
#    
#end = time.clock()
#print('\n运行时间: %f s' %(end-start))  # 显示运行时间
#print('success')       
