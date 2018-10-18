# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 分类名
    book_title = scrapy.Field()
    # 图书链接
    book_link = scrapy.Field()
    # 图书名字
    book_name = scrapy.Field()
    # 图书简介
    book_textinfo = scrapy.Field()
    # 图书评分
    book_rating = scrapy.Field()
    # 图书评论人数
    book_rating_nums = scrapy.Field()
    # 图书图片地址
    book_picture = scrapy.Field()
    #图书价格
    book_price = scrapy.Field()
    #图书出版日期
    book_date = scrapy.Field()
    #出版社
    book_press = scrapy.Field()
    #作者/译者
    book_author = scrapy.Field()


