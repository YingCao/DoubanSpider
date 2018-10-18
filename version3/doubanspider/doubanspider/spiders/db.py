# -*- coding: utf-8 -*-
import scrapy
import copy
import time
import random
import urllib.parse
from doubanspider.items import DoubanspiderItem
class DbSpider(scrapy.Spider):
    name = 'db'
    allowed_domains = ['douban.com']
    start_urls = ['https://book.douban.com/tag/?view=type&icn=index-sorttags-all']

    #解析全部标签页，从标签页中获取数据
    def parse(self, response):
        item = DoubanspiderItem()
        #使用Xpah选择器获取所有标签页的链接

        book_titles = response.xpath('//div[@class=""]//tbody/tr/td/a/@href').extract()

        for i in book_titles:
            item['book_title'] = i
            url = 'https://book.douban.com' + urllib.parse.quote(i)
            baseurl = {}
            baseurl['url'] = url
            yield scrapy.Request(url = url, meta = {'item1':copy.deepcopy(item),'baseurl':copy.deepcopy(baseurl)},
                                 callback= self.get_booklinks,
                                 dont_filter=True
            )

    def get_booklinks(self, response):
        item = response.meta['item1']
        baseurl = response.meta['baseurl']
        time.sleep(random.random())


        if item:
            pages = response.xpath("//div[@class='paginator']/a/text()").extract()
            page = int(pages[-1])
            if page > 50:
                page = 50
            for i in range(0,page):
                print(i)
                url = baseurl['url'] + "?start=" + str(i * 20)
                print(url)
                yield scrapy.Request(url = url, meta = {'item2' : copy.deepcopy(item)},
                                         callback = self.get_bookdetails,
                                         dont_filter=True)


    def get_bookdetails(self, response):
        item = response.meta['item2']
        if item and response.xpath('//ul[@class="subject-list"]//a[@class="nbg"]/@href').extract():
            book_links = response.xpath('//ul[@class="subject-list"]//a[@class="nbg"]/@href').extract()
            cnt = len(book_links)
            for i in range(1, cnt+1):
                book_link = response.xpath('//div[@id="subject_list"]/ul/li[' + str(i) + ']//h2/a/@href').extract_first().strip()
                book_name = response.xpath('//div[@id="subject_list"]/ul/li[' + str(i) + ']//h2/a/text()').extract_first().strip()
                book_info = response.xpath('//div[@id="subject_list"]/ul/li[' + str(i) + ']//div[@class="pub"]/text()').extract_first().strip().strip()
                book_price = book_info.split('/')[-1]
                book_date = book_info.split('/')[-2]
                book_press = book_info.split('/')[-3]
                book_author = book_info.split('/')[0:-3]
                book_picture = response.xpath("//div[@id='subject_list']/ul/li[" + str(i) + "]//a/img/@src").extract_first()
                book_rating = response.xpath('//div[@id="subject_list"]/ul/li[' + str(i) + ']//span[@class="rating_nums"]/text()').extract_first()
                book_rating_nums = response.xpath('//div[@id="subject_list"]/ul/li[' + str(i) + ']//span[@class="pl"]/text()').extract_first()
                if book_rating_nums:
                    book_rating_nums = book_rating_nums.strip()
                book_textinfo = response.xpath('//div[@id="subject_list"]/ul/li[' + str(i) + ']//p/text()').extract_first()
                item['book_textinfo'] = book_textinfo
                item['book_rating'] = book_rating
                item['book_rating_nums'] = book_rating_nums
                item['book_link'] = book_link
                item['book_name'] = book_name
                item['book_price'] = book_price
                item['book_date'] = book_date
                item['book_press'] = book_press
                item['book_author'] = book_author
                item['book_picture'] = book_picture
                yield item 