#测试单个网页能否解析成功
"""
import requests
from bs4 import BeautifulSoup as bs
from tool import *

url = 'https://book.douban.com/subject/25862578/'

data = requests.get(url,headers = get_hd())
soup = bs(data.text, 'lxml', from_encoding='utf-8')
#print(soup)
print(soup.select('#info a'))
#https://api.douban.com/v2/book/25862578

"""


import re
import random
import requests

a = "   dada \n"
print(a.strip())


aa = "moreurl(this,{i:'19',query:'',subject_id:'26878124',from:'book_subject_search'})"

items = re.findall(re.compile("subject_id:'(\d+)'",re.S), aa)
print(items)
print(random.random())

proxyHost = "http-dyn.abuyun.com"
proxyPort = "9010"
proxyUser = "H31Z30O2520S376P"
proxyPass = "7A710F5AB5940ABC"
proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host": proxyHost,
    "port": proxyPort,
    "user": proxyUser,
    "pass": proxyPass,
}
proxies = {
    "http": proxyMeta,
    "https": proxyMeta,
}

url = 'https://httpbin.org/get'
data = requests.get(url, proxies = proxies)
print(data.text)