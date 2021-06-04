# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from douban.settings import *
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import pandas as pd
import re

def save_as_excel(list_data, columns_map=None, file_name='表格'):
  pf = pd.DataFrame(list_data)
  if columns_map:
    pf.rename(columns=columns_map, inplace=True)
  file_path = pd.ExcelWriter(f'{file_name}.xlsx')
  pf.fillna(' ', inplace=True)
  pf.to_excel(file_path, encoding='utf-8', index=False)
  file_path.save()
  print('============ DONE =============')
  print(f'已保存为: {file_name}.xlsx')

class DoubanPipeline:
  def open_spider(self, spider):
    self.book_columns_map = {
      'book_name': '书名',
      'book_rating': '豆瓣得分',
      'book_pl': '评价人数',
      'book_author': '作者',
      'book_sum_up': '评语',
      'book_url': '书链接',
      'book_cover_url': '书封面地址'
    }
    self.books = []

  def close_spider(self, spider):
    save_as_excel(list_data=self.books, columns_map=self.book_columns_map, file_name='豆瓣图书Top250')

  def process_item(self, item, spider):
    bookStr = json.dumps(ItemAdapter(item).asdict(), ensure_ascii=False)
    bookInfo = json.loads(bookStr)
    bookInfo['book_pl'] = re.findall(r"\d+\.?\d*", bookInfo['book_pl'])[0]
    self.books.append(bookInfo)
    return item


class MongoPipeline:
  def __init__(self):
    # 链接数据库
    client = pymongo.MongoClient(host=MONGODB_HOST, port=MONGODB_PORT)

    # 指向指定数据库
    mdb = client['fodder']

    # 获取要插入的表
    self.post = mdb[MONGODB_DOCNAME]

  def process_item(self, item, spider):
    data = dict(item)
    data['book_pl'] = re.findall(r"\d+\.?\d*", data['book_pl'])[0]
    self.post.insert(data)
    return item

