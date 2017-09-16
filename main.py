import requests
import json
import random
from search_flights import Armada
from pprint import pprint
#from bs4 import BeautifulSoup
import scrapy
from ScuttleButt.ScuttleButt.spiders import SSSpider
from scrapy import cmdline
from Database import databases
#cmdline.execute("docker run -p 8050:8050 -p 5023:5023 scrapinghub/splash".split())
#cmdline.execute("scrapy runspider ./ScuttleButt/ScuttleButt/spiders/SSSpider.py".split())

print("Working")


def start_requests():
    cmdline.execute("scrapy runspider ./ScuttleButt/ScuttleButt/spiders/gpt_spider.py".split())

    # print("BODY = {}".format(content.body))

start_requests()


#hunt = Armada()

# hunt.my_soup = hunt.search_google_page()


# for trophy in hunt.my_soup.find_all({'class': 'EIGTDNC-f-o'}):
#     print(trophy)

# spidey.start_requests()



# r = requests.post(api_url, json=json_data)

#print(r)
# print(type(loaded_data))

#r.json()
# pprint(r.json())

print('Finished Work')
