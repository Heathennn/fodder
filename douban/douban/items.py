# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DBBookItem(scrapy.Item):
    # define the fields for your item here like:
    # 书名
    book_name = scrapy.Field()
    # 书链接
    book_url = scrapy.Field()
    # 书封面
    book_cover_url = scrapy.Field()
    # 作者
    book_author = scrapy.Field()
    # 得分
    book_rating = scrapy.Field()
    # 评价人数
    book_pl = scrapy.Field()
    # 总结
    book_sum_up = scrapy.Field()

