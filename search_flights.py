import requests
from bs4 import BeautifulSoup


class Armada:
    def __init__(self):
        self.origin = "GPT"
        self.destination = "MCI"
        self.roundTrip = True
        self.depart_date = "2017-09-02"
        self.return_date = "2017-09-03"
        self.response = ""
        self.my_soup = BeautifulSoup()

    def search_google_page(self, origin="GPT", destination="MCI", roundTrip="True", depart_date="2017-09-02", return_date="2017-09-02"):
        search_url = "https://www.google.com/flights/?gl=us&f=0#search;f={};t={};d=();r={}".format(
            self.origin, self.destination, self.depart_date, self.return_date)
        response = requests.get("https://www.google.com/flights/?f=0&gl=us")
        soup = BeautifulSoup(response.content)
        return soup

