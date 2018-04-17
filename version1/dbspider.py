import requests
from urllib3.exceptions import RequestError
import time
from tool import *
from lxml import etree
import urllib.parse



lists = []

# 爬取首页 获取所有图书的列表
def first_page():
    try:
        url = 'https://book.douban.com/tag/?view=type&icn=index-sorttags-all'
        data = requests.get(url, headers= get_hd())
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
    for i in range(len(book_name)):
        yield {
            "name" : book_name[i],
            "link" : 'https://book.douban.com' + urllib.parse.quote(book_link[i])
        }

def second_page(url, cnt=0):
    try:
        data = requests.get(url, headers = get_hd())
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
def second_parse(data,url):
    content = etree.HTML(data)
    pages = content.xpath("//div[@class='paginator']/a/text()")[-1]
    links = content.xpath('//ul[@class="subject-list"]//a[@class="nbg"]/@href')
    for link in links:
        yield link

    for page in range(1,pages):
        url = url + "?start=" + str(page*20)
        data = second_page(url)
        content = etree.HTML(data)
        links = content.xpath('//ul[@class="subject-list"]//a[@class="nbg"]/@href')
        if links:
            for link in links:
                yield link
        return None


def main():
    data = first_page()
    print(first_parse(data))
    for i in first_parse(data):
        print(i['name'],i["link"])
if __name__ == '__main__':
    main()