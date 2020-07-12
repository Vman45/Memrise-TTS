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

        self.course = "5757638/daneoneun-sinaessi-wihae-baeugi-pilyohaeyo"

        if constants.DEBUG == True:
            self.verify = r"FiddlerRoot.pem"
        else:
            self.verify = True

        self.csrftoken = self.login()


    def login(self):
        
        login_page_html = self.session.get(self.login_url, verify=self.verify)
        tree = html.fromstring(login_page_html.text)
        authenticity_token = list(set(tree.xpath("//input[@name='csrfmiddlewaretoken']/@value")))[0]
        payload = {'username': MEMORISE_USERNAME, 
                  'password':MEMORISE_PASSWORD,
                  'csrfmiddlewaretoken':authenticity_token}
        self.session.post(self.login_url, data = payload, headers = dict(referer=self.login_url))
        
        # Need a new csrf token now that we are logged in
        return self.session.get("https://www.memrise.com/home/").cookies['csrftoken']


    def scrape(self):
        res = self.session.get('https://www.memrise.com/course/5757638/daneoneun-sinaessi-wihae-baeugi-pilyohaeyo/', verify=self.verify)

        page = BeautifulSoup(res.content, 'html.parser')
        for row in page.find_all('div',attrs={"class" : "col_a col text"}):
            self.words.append(row.text)
        print(len(self.words))
    
    def write_to_file(self):
        with open("wordlist.txt", "w", encoding="utf-8") as f:
            for word in self.words:
                f.write(word+'\r')

    def update_course_TTS(self, course):

        word_id = ""

        # Adds the specific course to the course URL stem
        self.course_url += self.course
        print(self.course_url)

        res = self.session.get(url=self.course_url, verify=self.verify)

        page = BeautifulSoup(res.content, 'html.parser')

        for word in self.words: 
            for row in page.find_all('div',attrs={"class" : "thing text-text"}):
                # Find the 9 digit data-thing-id
                word_id = re.findall(r"\b\d{9}\b", str(row))
                self.post_TTS(word, word_id[0])


    def post_TTS(self, word, id):

        files = {
            'f':  ('{word}.mp3'.format(word=word), open("AudioFiles/{word}.mp3".format(word=word), "rb"), 'audio/mpeg'),
        }
        data = {
            'thing_id': (None,id),
            'cell_id': (None,3),
            'cell_type': (None,"column"),
            'csrfmiddlewaretoken': (None, self.csrftoken),
        }
        #test = self.session.post(url="https://www.memrise.com/ajax/thing/cell/upload_file/", headers=self.headers, data=data, files=files, verify=self.verify)
        #print(test.status_code)


sm = Scrape_Memorise()
sm.scrape()
sm.update_course_TTS('course_name')
#sm.write_to_file()

# Navigate to the next page and scrape the data


