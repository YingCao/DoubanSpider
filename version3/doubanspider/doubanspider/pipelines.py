# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import json

class DoubanspiderPipeline(object):
    def process_item(self, item, spider):
        return item



class douPipeline(object):
    def __init__(self):
        self.filepath = './爬虫数据'

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        if item['book_title']:
            filename = self.filepath + item['book_title'] + ".json"
            file = open(filename,'ab+')
            if not item['book_link']:
                item['book_link'] = '查找不存在'

            if not item['book_name']:
                item['book_name'] = '查找不存在'

            if not item['book_textinfo']:
                item['book_textinfo'] = '查找不存在'

            if not item['book_rating']:
                item['book_rating'] = '查找不存在'

            if not item['book_rating_nums']:
                item['book_rating_nums'] = '查找不存在'

            if not item['book_price']:
                item['book_price'] = '查找不存在'

            if not item['book_date']:
                item['book_date'] = '查找不存在'

            if not item['book_press']:
                item['book_press'] = '查找不存在'

            if not item['book_author']:
                item['book_author'] = '查找不存在'

            if not item['book_picture']:
                item['book_picture'] = '查找不存在'
            jsontext = json.dumps(dict(item),ensure_ascii=False) + ",\n"
            file.write(jsontext.encode("utf-8"))
            file.close()
        else:
            DropItem('查找失败')
        return item

    def close_spider(self, spider):
        pass
