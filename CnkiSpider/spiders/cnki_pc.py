import scrapy
from bs4 import BeautifulSoup

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

    def start_requests(self):
        yield scrapy.FormRequest(
            url = self.start_url,
            method = 'POST',
            formdata = self.form_data,
            callback = self.parse
        )

    def parse(self, response):
        self.logger.debug('______________________________________1')
        # with open('test.html', 'w', encoding='utf-8') as f:
        #     f.write(response.text)
        soup = BeautifulSoup(response.body, 'html.parser')
        a_articles = soup.find_all("a", attrs={'class':'fz14'})
        for a in a_articles:
            href_article = a.attrs['href']
            article_url = self.home_url + href_article
            yield scrapy.Request(
                url = article_url,
                callback = self.parse_article
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
        


        self.logger.debug('______________________________________2')


    def parse_article(self,response):
        soup = BeautifulSoup(response.body, 'html.parser')
        title = soup.select('.class="wx-tit"')[0].get_text()
        abstract = soup.select('span[class="abstract-text"]')[0].get_text()
        yield {
            "title" : title,
            "abstract" : abstract
        }
        # self.logger.debug(title)
        # self.logger.debug(abstract)

