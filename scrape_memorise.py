from bs4 import BeautifulSoup
from lxml import html
import requests
import re

import constants

# change this to your memorise username and password
from settings import MEMORISE_USERNAME, MEMORISE_PASSWORD


class Scrape_Memorise:

    def __init__(self):
        self.session = requests.Session()
        self.words = []
        self.headers = constants.MEMRISE_HEADERS
        self.login_url = constants.MEMRISE_LOGIN_URL
        self.course_url = constants.MEMRISE_COURSE_URL

        if constants.DEBUG == True:
            self.verify = r"FiddlerRoot.pem"
        else:
            self.verify = True

        self.authenticity_token = ""

        self.course = "5757638/daneoneun-sinaessi-wihae-baeugi-pilyohaeyo/edit/"

        #Main
        # self.login()
        # self.scrape()
        # self.write_to_file()

    def login(self):
        
        #login_page_html = self.session.get(self.login_url)
        login_page_html = self.session.get(self.login_url, verify=self.verify)
        tree = html.fromstring(login_page_html.text)
        self.authenticity_token = list(set(tree.xpath("//input[@name='csrfmiddlewaretoken']/@value")))[0]
        print(self.authenticity_token)
        payload = {'username': MEMORISE_USERNAME, 
                  'password':MEMORISE_PASSWORD,
                  'csrfmiddlewaretoken':self.authenticity_token}

        #self.session.post(self.login_url, data = payload, headers = dict(referer=self.login_url))
        self.session.post(self.login_url, data = payload, headers = dict(referer=self.login_url), verify=self.verify)

    def scrape(self):
        res = self.session.get('https://www.memrise.com/course/5757638/daneoneun-sinaessi-wihae-baeugi-pilyohaeyo/', verify=self.verify)

        page = BeautifulSoup(res.content, 'html.parser')
        for row in page.find_all('div',attrs={"class" : "col_a col text"}):
            self.words.append(row.text+"\r")
    
    def write_to_file(self):
        with open("wordlist.txt", "w", encoding="utf-8") as f:
            f.writelines(self.words)
    
    def post_audio(self):
        edit = self.session.get("https://www.memrise.com/course/5757638/daneoneun-sinaessi-wihae-baeugi-pilyohaeyo/edit/")

        csrftoken = edit.cookies['csrftoken']
        print(csrftoken)
        self.headers['Referer'] = self.course_url + self.course

        files = {
            'f':  ('안녕하세요.mp3', open("AudioFiles/안녕하세요.mp3", "rb"), 'audio/mpeg'),
        }

        data = {
            'thing_id': (None,256276441),
            'cell_id': (None,3),
            'cell_type': (None,"column"),
            'csrfmiddlewaretoken': (None, csrftoken),
        }


        ##########################
############################

        test = self.session.post(url="https://www.memrise.com/ajax/thing/cell/upload_file/", headers=self.headers, data=data, files=files, verify=self.verify)
        print(test.status_code)


sm = Scrape_Memorise()
sm.login()
sm.scrape()
sm.post_audio()
#sm.write_to_file()

# Navigate to the next page and scrape the data


