import scrapy
import time
import json
import sqlite3
from bs4 import BeautifulSoup
from scrapy.spiders import Spider
from scrapy.selector import Selector
from ScuttleButt.ScuttleButt.items import ScuttlebuttItem
from scrapy_splash import SplashRequest
from scrapy import cmdline
from scrapy.http.headers import Headers
from Database.database_helper import build_client_db

RENDER_HTML_URL = "http://127.0.0.1:8050/render.html"


class LatLongSpider(Spider):
    name = "ll"
    airfare_path = 'file:Database/airfare.sqlite?mode=rwc'
    conn = sqlite3.connect(airfare_path, uri=True)
    c = conn.cursor()

    data = c.execute('SELECT * FROM airport_info WHERE rowid > 320')
    data = data.fetchall()
    airport_list = []
    airport_urls = []

    #build urls [1] = location [2] = airport ID
    for airport in data:
        airport_list.append(airport)

        airport_urls.append('http://airnav.com/airport/K'+airport[2])
    conn.close()
    #end of building urls
    allowed_domains = ["airnav.com"]

    # start_urls = ["https://www.google.com/flights/?gl=us&f=0#search;f=GPT;t=LAX;d=2017-09-02;r=2017-09-03"]
    start_urls = airport_urls

    def start_requests(self):
        for url in self.start_urls:
            print(url)
            time.sleep(20)
            #yield scrapy.Request(url=url, callback=self.parse)
            body = json.dumps({"url": url, "wait":5.0}, sort_keys=True)
            headers = Headers({'Content-Type': 'application/json'})
            yield SplashRequest(RENDER_HTML_URL, self.parse, method='POST',
                               body=body, headers=headers)

    def parse(self, response):
        print(response.body)
        sel = Selector(response)
        item = ScuttlebuttItem()
        item['LatLong'] = sel.xpath('/html/body/table[5]/tbody/tr/td[1]/table[1]/tbody/tr[2]/td[2]').extract()
        item['Airport_Name'] = sel.xpath('/html/body/table[3]/tbody/tr/td[2]/font/b').extract()
        item['Identifier'] = sel.xpath('/html/body/table[5]/tbody/tr/td[1]/table[1]/tbody/tr[1]/td[2]').extract()

        airport_name_text = ''
        t = item['Airport_Name']
        for tee in t:
            soup = BeautifulSoup(tee)
            airport_name_text = soup.find('b').string

        airport_identifier_text = ''
        t2 = item['Identifier']
        for tee2 in t2:
            soup = BeautifulSoup(tee2)
            airport_identifier_text = soup.find('td').string

        print('Name = {}'.format(airport_name_text))
        print('Id = ', airport_identifier_text)

        #parse string to find latlong, should remove first two latlong styles
        t = item['LatLong'][0]
        lat = ''
        long = ''
        if t:
            indy = t.index('<br>')
            t = t[indy+4:]
            indy = t.index('<br>')
            #should be lat long with ' / ' in between
            t = t[indy+4:-20]
            index = t.index('/')
            #remove white space
            lat = t[:index-1].replace(" ", "")
            long = t[index+1:].replace(" ", "")

        if airport_identifier_text:
            build_client_db(airport_name_text, airport_identifier_text, lat, long)
        else:
            print('Database not building')

        return item