####  功能

爬取 论文、摘要、发表时间

####  使用说明

用相应的```QueryJson```替换项目里的



####  反反爬设置

更改```  setting.py  ```的配置

```
# Obey robots.txt rules
ROBOTSTXT_OBEY = False
```

设置```  headers  ```，需要用到的应该只有```  Referer  ```和```  user-agent  ```（必不可少的）

```
DEFAULT_REQUEST_HEADERS = {
   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
   "Accept-Language": "en",
   "Host" : "kns.cnki.net",
   "Origin" : "https://kns.cnki.net",
   "Referer" : "https://kns.cnki.net/kns8/AdvSearch?dbcode=CFLS",
   "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.50"
}
```

####  Spider

1、重写了```start_requests()```，将```  Request  ```改为```  FormRequest  ```

2、```parse()```中先找到每个文章的链接，对文章链接```Request```的回调函数为```  parse_article()  ```,同时将每个文章的发表时间以参数的形式传给```Request```

3、```parse_article()```处理每个文章的页面



####  踩坑

1、刚开始不知道怎么写POST请求

不是直接传```JsonQuery = xx```，```JsonQuery```是传给表单的数据的一个键值对

2、BeautifulSoup选择器无法选择到tbody