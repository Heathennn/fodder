#  框架组成

### settings

> 项目的配置项，是一些可以读取的变量，里面有系统默认名字的变量
>
> 也可以设置自己的变量，如：自定义的pipeline、自定义的middleware、要链接的数据库的信息等等

自定义数据库信息：

```
MONGODB_HOST = '127.0.0.1'
# 端口号，默认27017
MONGODB_PORT = 27017
# 设置数据库名称
MONGODB_DBNAME = 'fodder'
# 存放本数据的表名称
MONGODB_DOCNAME = 'DoubanBook'
```

自定义pipeline：

```
# Configure item pipelines
# 数字表示此pipeline或middleware的执行优先级
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # 'douban.pipelines.DoubanPipeline': 300,
    'douban.pipelines.MongoPipeline': 300,
}
```



### Items

>/items.py
>
>可以理解为interface，定义了一套数据结构

```
class DBBookItem(scrapy.Item):
	# 此处定义你的字段
	book_name = scrapy.Field()

```

### spiders

> /spiders/douban.py
>
> 爬虫业务逻辑主体部分

```python
#引入你的Item, pycharm会报错时需要右键你的目录，将其作为根目录即可
from douban.items import DBBookItem
class DoubanbookSpider(scrapy.Spider):
  start_urls = ['开始爬取的页面', '一个或多个']
  def parse(self, response):
    # 爬虫名字 会自动生成
    name="doubanbook"
    # 爬取的页面的域名
    allowed_domains = ['book.douban.com']
    # 解析网页，一般我会用xpath，可以安装xpath_helper插件，在chrome浏览器上比较好用
    html_body = respone.xpath()
    ...
    # Item类，用来定义数据结构， 配合pipline
    item = DBBookItem()
    #  交给pipeline处理
    yield item
    
    if 还有下一页：
   # 存在需要继续爬取的页面，继续交给下一个请求处理，callback还是走parse函数，也可以自定义别的逻辑，比如和列表页面结构不同的详情页
  		yield scrapy.Request(next_url, callback=self.parse)
```



### pipeline

> 管道存储
>
> 在处理完一条数据（Item）之后，在pipeline中进行处理/清洗数据，然后进行存储到数据库、导出excel表格等操作
>
> 注意几个核心的函数名都是固定的
>
> 每个功能不用的pipeline 分开定义

```
class MongoPipeline:
 # 初始化的函数
	def __init__(self):
		# 可以定义个变量，用于接收全部数据，在process_item中处理每条，然后append到里，最后转存为Excel等
		self.book = []
		# 链接数据库
    client = pymongo.MongoClient(host=MONGODB_HOST, port=MONGODB_PORT)
    # 指向指定数据库
    mdb = client['fodder']
    # 获取要插入的表
    self.post = mdb[MONGODB_DOCNAME]
  # 核心方法，从spiders里拿到的item会在此处进行处理，此方法比如返回item（交给下一个继续处理）
  def process_item(self, item, spider):
  		# 一系列操作
      bookStr = json.dumps(ItemAdapter(item).asdict(), ensure_ascii=False)
      bookInfo = json.loads(bookStr)
      # 豆瓣图书的评价人数数据需要只取数字，可在此处处理
      bookInfo['book_pl'] = re.findall(r"\d+\.?\d*", bookInfo['book_pl'])[0]
      # 插入到数据库
      self.post.insert(dict(item))
  		return item
  def open_spider(self, spider):
  	# 爬虫开启的钩子
  	# 在此处定义变量也可以
  	self.book = []
  	
  def close_spider(self, spider):
   #爬虫关闭的钩子
   # 此处可以将所有拿到的Items或组装好的Items进行存储
   # save_as_excel(...参数)
```



### middlewares

> 穿插在请求和处理之间的中间件
>
> 类似于node框架

如

- 请求前增加user-agent

- 使用代理ip、ip池

  
