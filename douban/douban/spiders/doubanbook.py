import scrapy

from douban.items import DBBookItem


class DoubanbookSpider(scrapy.Spider):
  name = 'doubanbook'
  start_url = 'https://book.douban.com/top250'
  start_index = 0
  page_size = 25
  allowed_domains = ['book.douban.com']
  start_urls = [f'https://book.douban.com/top250?start={start_index}']

  def parse(self, response):
    books = response.xpath('//div[@class="article"]//table')
    if len(books) > 0:
      for book in books:
        item = DBBookItem()
        item['book_url'] = book.xpath('.//td[1]/a/@href').get()
        item['book_cover_url'] = book.xpath('.//td[1]/a/img/@src').get()
        item['book_name'] = book.xpath('.//td[2]/div[1]/a/@title').get()
        item['book_author'] = book.xpath('.//td[2]/p[1]/text()').get()
        item['book_rating'] = book.xpath('.//td[2]/div[2]/span[@class="rating_nums"]/text()').get()
        item['book_pl'] = book.xpath('.//td[2]/div[2]/span[@class="pl"]/text()').get()
        item['book_sum_up'] = book.xpath('.//td[2]/p[2]/span/text()').get()
        yield item
      offset = 1 if self.start_index == 0 else 0
      self.start_index += (self.page_size + offset )
      next_url = '{}?start={}'.format(self.start_url, self.start_index)
      self.logger.info('继续请求下一页: %s' % next_url)
      yield scrapy.Request(next_url, callback=self.parse)
    else:
      print(' ==============  Spiders请求结束  =============')
