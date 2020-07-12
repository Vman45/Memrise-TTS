from bs4 import BeautifulSoup
from lxml import html
import requests
import re

# change this to your memorise username and password
from settings import MEMORISE_USERNAME, MEMORISE_PASSWORD

LOGIN_URL = "https://www.memrise.com/login/"



class Scrape_Memorise:

    def __init__(self):
        self.session = requests.Session()
        self.words = []

        #Main
        self.login()
        self.scrape()
        self.write_to_file()

    def login(self):
        
        login_page_html = self.session.get(LOGIN_URL)

        tree = html.fromstring(login_page_html.text)
        authenticity_token = list(set(tree.xpath("//input[@name='csrfmiddlewaretoken']/@value")))[0]
        payload = {'username': MEMORISE_USERNAME, 
                  'password':MEMORISE_PASSWORD,
                  'csrfmiddlewaretoken':authenticity_token}

        self.session.post(LOGIN_URL, data = payload, headers = dict(referer=LOGIN_URL))

    def scrape(self):
        res = self.session.get('https://www.memrise.com/course/5757638/daneoneun-sinaessi-wihae-baeugi-pilyohaeyo/')

        page = BeautifulSoup(res.content, 'html.parser')
        for row in page.find_all('div',attrs={"class" : "col_a col text"}):
            self.words.append(row.text+"\r")
    
    def write_to_file(self):
        with open("wordlist.txt", "w", encoding="utf-8") as f:
            f.writelines(self.words)




Scrape_Memorise()


# Navigate to the next page and scrape the data


