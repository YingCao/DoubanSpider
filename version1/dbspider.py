import requests
from urllib3.exceptions import RequestError
import time
from tool import *
from lxml import etree
import urllib.parse
import re
from config import *
import pymongo
from multiprocessing import Pool
import xlwt
import random

lists = []
client = pymongo.MongoClient(MONGO_URL ,connect=False)
db = client[MONGO_DB]

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


def use_proxy(url,cnt =0):
    url1 = 'http://127.0.0.1:5000/get'
    try:
        url = 'https://book.douban.com/tag/?view=type&icn=index-sorttags-all'
        data = requests.get(url, headers= get_hd(), proxies = proxies)
        if data.status_code == 200:
            return data.text
        return None
    except RequestError:
        if cnt < 3:
            cnt += 1
            time.sleep(3)
            return use_proxy(url,cnt)
        else:
            return None

# 爬取首页 获取所有图书的列表
def first_page():
    try:
        url = 'https://book.douban.com/tag/?view=type&icn=index-sorttags-all'
        data = requests.get(url, headers= get_hd(), proxies = proxies)
        if data.status_code == 200:
            return data.text
        return None
    except RequestError:
        time.sleep(3)
        return first_page()
# 解析首页
def first_parse(data):
    content = etree.HTML(data)
    book_name = content.xpath('//div[@class=""]//tbody/tr/td/a/text()')
    book_link = content.xpath('//div[@class=""]//tbody/tr/td/a/@href')
    titles = [{'name':book_name[i],"link" : 'https://book.douban.com' + urllib.parse.quote(book_link[i])} for i in range(len(book_name))]
    return titles

"""
        for i in range(len(book_name)):
        yield {
            "name" : book_name[i],
            "link" : 'https://book.douban.com' + urllib.parse.quote(book_link[i])
        }
"""

#第二次爬取，抓取每个标签下所有图书的url
#
def second_page(url, cnt=0):
    try:
        data = requests.get(url, headers = get_hd(),proxies = proxies)
        if data.status_code == 200:
            return data.text
        return None
    except RequestError:
        cnt += 1
        time.sleep(3)
        if cnt < 3:
            return second_page(url, cnt)
        else:
            lists.append(url)
            return None
    # //ul[@class="subject-list"]//a[@class="nbg"]/@href
    #

#解析第二次爬取到的信息，主要是获取当前标签页的页码，以及返回所有图书的链接
def second_parse(data,url):
    content = etree.HTML(data)
    pages = content.xpath("//div[@class='paginator']/a/text()")[-1]
    book_links = content.xpath('//ul[@class="subject-list"]//a[@class="nbg"]/@href')
    book_name = content.xpath('//div[@class="info"]/h2/a/@title')
    book_author = content.xpath('//div[@class="info"]/div[@class="pub"]//text()')
    book_rating = content.xpath('//div[@class="info"]//span[@class="rating_nums"]/text()')
    book_rating_nums = content.xpath('//div[@class="info"]//span[@class="pl"]/text()')
    book_id = content.xpath('//div[@class="info"]/h2/a/@onclick')
    book_picture = content.xpath("//div[@class ='article']//img/@src")
    if book_links:
        for i in range(len(book_links)):
            yield{
                'book_author': (book_author[i] if book_author else "").strip(),
                'book_links': book_links[i] if book_links else "",
                'book_name': book_name[i] if book_name else "",
                'book_rating': book_rating[i] if book_rating_nums else "",
                'book_rating_nums': int(re.findall(re.compile('(\d+)', re.S),(book_rating_nums[i] if book_rating_nums else ""))[0]),
                'book_id': int(re.findall(re.compile("subject_id:'(\d+)'",re.S), (book_id[i] if book_id else ""))[0]),
                'book_pic':book_picture[i] if book_picture else "",
            }
    time.sleep(random.random()+0.2)

    for page in range(1,int(pages)):
        url = url + "?start=" + str(page*20)
        print(url)
        data = second_page(url)
        content = etree.HTML(data)
        links = content.xpath('//ul[@class="subject-list"]//a[@class="nbg"]/@href')

        if links:
            book_links = content.xpath('//ul[@class="subject-list"]//a[@class="nbg"]/@href')
            book_name = content.xpath('//div[@class="info"]/h2/a/@title')
            book_author = content.xpath('//div[@class="info"]/div[@class="pub"]//text()')
            book_rating = content.xpath('//div[@class="info"]//span[@class="rating_nums"]/text()')
            book_rating_nums = content.xpath('//div[@class="info"]//span[@class="pl"]/text()')
            book_id = content.xpath('//div[@class="info"]/h2/a/@onclick')
            book_picture = content.xpath("//div[@class ='article']//img/@src")
            if book_links:
                for i in range(len(book_links)):
                    yield {
                        'book_author': (book_author[i] if book_author else "").strip(),
                        'book_links': book_links[i] if book_links else "",
                        'book_name': book_name[i] if book_name else "",
                        'book_rating': book_rating[i] if book_rating_nums else "",
                        'book_rating_nums': int(re.findall(re.compile('(\d+)', re.S),(book_rating_nums[i] if book_rating_nums else ""))[0]),
                        'book_id': int(re.findall(re.compile("subject_id:'(\d+)'",re.S), (book_id[i] if book_id else ""))[0]),
                        'book_pic':book_picture[i] if book_picture else "",
                    }
            time.sleep(random.random() + 0.2)
        else:
            return None



def save_to_mongo(table,result):
    if db[table].insert(result):
        print('存储到MongoDB成功',result)
        return True
    return False

def main(title_num):
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('sheet1', cell_overwrite_ok=True)
    sheet.write(0, 0, '书名')
    sheet.write(0, 1, '评分')
    sheet.write(0, 2, '评论人数')
    sheet.write(0, 3, '图书链接')
    sheet.write(0, 4, '图书id')
    sheet.write(0, 5, '图书信息')
    data = first_page()
    titles = first_parse(data)
    url = titles[title_num]['link']
    table_name = titles[title_num]['name']
    print(table_name)
    data = second_page(url)
    count = 1
    for i in second_parse(data,url):
        print(i)
        sheet.write(count, 0, i['book_name'])
        sheet.write(count, 1, i['book_rating'])
        sheet.write(count, 2, i['book_rating_nums'])
        sheet.write(count, 3, i['book_links'])
        sheet.write(count, 4, i['book_id'])
        sheet.write(count, 5, i['book_author'])
        count += 1
        save_to_mongo(table_name, i)
    filename = table_name + '.xls'
    book.save(filename)

"""
    for i in first_parse(data):
        data = second_page(i['link'])
        second_parse(data, url)
       # print("hello")
        for j in second_parse(data,i['link']):
            print(j)
"""


        #print(i['name'],i["link"])
if __name__ == '__main__':
   # main(0)
    num = [i for i in range(0, 146)]
    pool = Pool()
    pool.map(main, num)

