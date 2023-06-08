import scrapy
from bs4 import BeautifulSoup
from scrapy_splash import SplashRequest

class CnkiPcSpider(scrapy.Spider):
    name = "cnki_pc"
    # allowed_domains = ["kns.cnki.net"]
    # start_urls = ["http://kns.cnki.net/"]
    home_url = "https://kns.cnki.net"
    start_url = "https://kns.cnki.net/kns8/Brief/GetGridTableHtml"
    query_json_str = open(r'CnkiSpider/QueryJson.json', encoding='utf8').read()
    cur_page = 1
    form_data = {
        "IsSearch" : "false",
        "QueryJson" : query_json_str,
        "DBCode" : "CFLS",
        "CurrSortField" : 'PT',
        "CurrSortFieldType" : 'desc',
        "CurPage" : str(cur_page),
        "RecordsCntPerPage" : "50"
    }

    lua_script = """
function main(splash, args)
  assert(splash:go(args.url))
  assert(splash:wait(1))
  if splash:select("#ChDivSummaryMore") then
    local more = splash:select("#ChDivSummaryMore")
    assert(more, "Failed to select #ChDivSummaryMore element")
  
    local style = more.attributes.style
    if style and style:lower():find("display%s*:%s*none") then
      -- Element is hidden, no need to click
    else
      more:mouse_click()
      assert(splash:wait(1))
    end
  end
  
  return {
    html = splash:html(),
  }
end
    """

    def start_requests(self):
        yield scrapy.FormRequest(
            url = self.start_url,
            method = 'POST',
            formdata = self.form_data,
            callback = self.parse
        )

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        tr_nodes = soup.select('.result-table-list tr')
        for tr_node in tr_nodes:
            if tr_node.select('.date'):
                date = tr_node.select('.date')[0].get_text()
                href_articles = tr_node.select('.fz14')[0].attrs['href']
                article_url = self.home_url + href_articles
                yield SplashRequest(
                    url = article_url,
                    endpoint='execute',
                    callback = self.parse_article,
                    meta = {
                        "time" : date
                    },
                    args={
                        'wait': 3,
                        'lua_source': self.lua_script
                    } 
                )

        if soup.find('a', {'id': 'PageNext'}):
            self.cur_page += 1
            self.form_data["CurPage"] = str(self.cur_page)
            yield scrapy.FormRequest(
                url = self.start_url,
                method = 'POST',
                formdata = self.form_data,
                callback = self.parse
            )
        

    def parse_article(self,response):
        soup = BeautifulSoup(response.body, 'html.parser')
        title = soup.select('.wx-tit h1')[0].get_text()
        abstract = soup.select('.abstract-text')[0].get_text()
        keyword_str = ""
        for kw in soup.select('[name="keyword"]'):
            keyword_str += kw.get_text()
        yield {
            "title" : title,
            "abstract" : abstract,
            "time" : response.meta["time"],
            "keyword" : keyword_str
        }
