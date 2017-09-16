import scrapy
import time
import datetime
import json
import sqlite3
import boto3
from ScuttleButt.ScuttleButt.spiders.DynamoHelper import *
from bs4 import BeautifulSoup
from scrapy.spiders import Spider
from scrapy.selector import Selector
from ScuttleButt.ScuttleButt.items import ScuttlebuttItem
from scrapy_splash import SplashRequest
from scrapy import cmdline
from scrapy.http.headers import Headers

RENDER_HTML_URL = "http://127.0.0.1:8050/render.html"


class ScrapSpider(Spider):
        name = "gpt"

        airfare_path = 'file:Database/airfare.sqlite?mode=rwc'
        conn = sqlite3.connect(airfare_path, uri=True)
        c = conn.cursor()

        data = c.execute('SELECT airport_id FROM GPT_table')
        data = data.fetchall()
        airport_list = []
        airport_urls = []
        kayak_urls = []

        for airport in data:
            airport_list.append(airport[0])
            airport_urls.append('https://www.google.com/flights/?gl=us&f=0#search;f=GPT;t={};d=2017-09-23;r=2017-09-24;so=p;eo=e'.format(airport[0]))
        conn.close()

        allowed_domains = ["google.com"]
        start_urls = ["https://www.google.com/flights/?gl=us&f=0#search;f=GPT;t=ATL;d=2017-09-23;r=2017-09-24;so=p;eo=e"]

        def start_requests(self):
            for url in self.start_urls:
                print(url)
                time.sleep(1)
                body = json.dumps({"url": url, "wait":2.5}, sort_keys=True)
                headers = Headers({'Content-Type': 'application/json'})
                yield SplashRequest(RENDER_HTML_URL, self.parse, method='POST',
                                    body=body, headers=headers)


        def kayak_requests(self, dest):
            print('INSIDE KAYAK REQUESTS')
            kayak_url = 'https://www.kayak.com/flights/GPT-{}/2017-09-16/2017-09-17'.format(dest)
            print('kayak url = ' + kayak_url)
            body = json.dumps({"url": kayak_url, "wait": 1.5}, sort_keys=True)
            headers = Headers({'Content-Type': 'application/json'})
            yield SplashRequest(RENDER_HTML_URL, self.parse_kayak, method='POST',
                                body=body, headers=headers)

        def parse_kayak(self, response):
            sel = Selector(response)
            item = ScuttlebuttItem()

            item['Kayak_Price'] = sel.xpath(
                '/html/body/div[1]/div[1]/div[3]/div/div[1]/div[2]/div/div[2]/div/div[2]/div[8]/div[1]/div/div/div[2]/div/div[1]/div[2]/div/div[2]/div[1]/div/div[1]/div/a/span[1]').extract()
            item['Kayak_Destination'] = sel.xpath(
                '/html/body/div[1]/div[1]/div[3]/div/div[1]/div[2]/div/div[2]/div/div[2]/div[8]/div[1]/div/div/div[2]/div/div[1]/div[1]/div[1]/div/ol/li[1]/div/div/div[4]/div[2]').extract()

            dest = None
            price = None

            for d in item['Kayak_Destination']:
                soup = BeautifulSoup(d, 'lxml')
                dest = soup.find('div').string

            for p in item['Kayak_Price']:
                soup = BeautifulSoup(p, 'lxml')
                price = soup.find('span').string
                print('kayak: ' + dest + ' ' + price)

            if price and dest:
                self.updatePrice(price, dest)
            else:
                print('Kayak failed for ' + dest)

            return item

        #first parser google.com/flights
        def parse(self, response):
            sel = Selector(response)
            item = ScuttlebuttItem()
            price = None
            dest = None

            item['Price'] = sel.xpath('/html/body/div[1]/div[3]/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/div/div[3]/div[1]/div/div[2]/div[2]/div[1]/div[4]/a/div[1]/div/div[1]').extract()
            item['Destination'] = sel.xpath('/html/body/div[1]/div[3]/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/div/div[1]/div[5]/table/tbody/tr[1]/td[2]/div/div[1]/div/span').extract()

            if item['Destination'] is not None:
                for d in item['Destination']:
                    soup = BeautifulSoup(d, 'lxml')
                    print('soup = ', soup)
                    dest = soup.find('span').string

            if item['Price'] is not None:
                for p in item['Price']:
                    soup = BeautifulSoup(p, 'lxml')
                    print('soup price = ', soup)
                    price = soup.find("div").string
                    print('Google: ' + dest + " " + price)

            if price is not None and dest is not None:
                self.updatePrice(price, dest)
            else:
                print("error with soup")

            return item

        def updatePrice(self, price, destination):

            airfare_path = 'file:Database/airfare.sqlite?mode=rwc'
            conn = sqlite3.connect(airfare_path, uri=True)
            c = conn.cursor()
            destination = str(destination)
            price = price[1:]
            price = price.replace(',', '')
            price = float(price)
            date = str(datetime.datetime.now())
            date = date.split('.')
            print('Date: ', date)
            c.execute('UPDATE GPT_table SET airfare = ?, last_update = ? WHERE airport_id = ?', (price, date[0], destination))
            conn.commit()
            dynamo = DynamoHelper()

            dynamo.add_to_dynamo(destination, price, date[0])
            print('{} has been updated'.format(destination))
            conn.close()