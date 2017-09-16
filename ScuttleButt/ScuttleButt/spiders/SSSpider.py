import scrapy
import json
from bs4 import BeautifulSoup
from scrapy.spiders import Spider
from scrapy.selector import Selector
from ScuttleButt.ScuttleButt.items import ScuttlebuttItem
from scrapy_splash import SplashRequest
from scrapy import cmdline
from scrapy.http.headers import Headers

RENDER_HTML_URL = "http://127.0.0.1:8050/render.html" #?url=https://www.google.com/flights/?gl=us&f=0#search;f=GPT;t=MCI;d=2017-09-02;r=2017-09-03"


class ScrapSpider(Spider):
        name = "ss"
        allowed_domains = ["google.com"]
        start_urls = ["https://www.google.com/flights/?gl=us&f=0#search;f=GPT;t=LAX;d=2017-09-02;r=2017-09-03"]

        def start_requests(self):
            for url in self.start_urls:
                print('URL = {}', url)
                body = json.dumps({"url": url, "wait":1.5}, sort_keys=True)
                headers = Headers({'Content-Type': 'application/json'})
                yield SplashRequest(RENDER_HTML_URL, self.parse, method='POST',
                                    body=body, headers=headers)

        def parse(self, response):
            sel = Selector(response)
            item = ScuttlebuttItem()
            item['Price'] = sel.xpath('/html/body/div[1]/div[3]/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/div/div[3]/div[1]/div/div[2]/div[2]/div[1]/div[4]/a/div[2]/div[2]').extract()
            item['Content'] = sel.xpath('/html/body/div[1]/div[3]/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/div/div[3]/div[1]/div/div[2]/div[2]/div[1]/div[4]/a/div[1]/div/div[1]').extract()
            item['Source_Website'] = "https://www.google.com/flights/?gl=us&f=0#search;f=GPT;t=LAX;d=2017-09-02;r=2017-09-03"

            t = item['Price']
            for tee in t:
                soup = BeautifulSoup(tee)
                text = soup.find("span").string
                print(text)
            return item
