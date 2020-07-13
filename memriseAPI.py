from bs4 import BeautifulSoup
from lxml import html
import requests
import re
import time

import constants

# change this to your memorise username and password
from settings import MEMORISE_USERNAME, MEMORISE_PASSWORD


class MemriseAPI:

    def __init__(self, course):
        self.session = requests.Session()
        self.words = []
        self.headers = constants.MEMRISE_HEADERS
        self.login_url = constants.MEMRISE_LOGIN_URL
        
        # Creates the full course URL
        self.course_url = constants.MEMRISE_COURSE_URL + course
        #self.course = "5757638/daneoneun-sinaessi-wihae-baeugi-pilyohaeyo"

        # Used for fiddler debugging
        if constants.DEBUG == True:
            self.verify = r"FiddlerRoot.pem"
        else:
            self.verify = True

        self.csrftoken = self.login()


    def login(self):
        
        ### Maybe change this code block
        login_page_html = self.session.get(self.login_url, verify=self.verify)
        tree = html.fromstring(login_page_html.text)
        authenticity_token = list(set(tree.xpath("//input[@name='csrfmiddlewaretoken']/@value")))[0]
        ###
        payload = {'username': MEMORISE_USERNAME, 
                  'password':MEMORISE_PASSWORD,
                  'csrfmiddlewaretoken':authenticity_token}
        self.session.post(self.login_url, data = payload, headers = dict(referer=self.login_url))
        # Need a new csrf token now that we are logged in
        return self.session.get("https://www.memrise.com/home/").cookies['csrftoken']


    def scrape_wordlist(self):

        res = self.session.get(url=self.course_url, headers=self.headers, verify=self.verify)

        page = BeautifulSoup(res.content, 'html.parser')
        for row in page.find_all('div',attrs={"class" : "col_a col text"}):
            self.words.append(row.text)
        self.write_to_file()
    
    # Called when we scrape the wordlist
    def write_to_file(self):
        with open("wordlist.txt", "w", encoding="utf-8") as f:
            for word in self.words:
                f.write(word+'\r')

    # Iterates through all the words in the page and posts the correct TTS
    def update_course_TTS(self):

        print(self.course_url)
        word_id = ""
        res = self.session.get(url=self.course_url, verify=self.verify)
        page = BeautifulSoup(res.content, 'html.parser')

        for row in page.find_all('div',attrs={"class" : "thing text-text"}):
            # Match the target word to it's ID
            if row.contents[2].text in self.words:
                    # Find the 9 digit data-thing-id
                    word_id = re.findall(r"\b\d{9}\b", str(row))
                    # Avoid spamming the server too hard!
                    time.sleep(1)
                    self.post_TTS(row.contents[2].text, word_id[0])

    def post_TTS(self, word, id):
        try:
            files = {
                'f':  ('{word}.mp3'.format(word=word), open("AudioFiles/{word}.mp3".format(word=word), "rb"), 'audio/mpeg'),
            }
        except Exception as e:
            print("The file AudioFiles/{word}.mp3 does not exist... skipping word".format(word=word))
            return
        data = {
            'thing_id': (None,id),
            'cell_id': (None,3),
            'cell_type': (None,"column"),
            'csrfmiddlewaretoken': (None, self.csrftoken),
        }
        post_audio = self.session.post(url="https://www.memrise.com/ajax/thing/cell/upload_file/", headers=self.headers, data=data, files=files, verify=self.verify)
        print(post_audio.status_code)
    
    def delete_course_tts(self):

        print(self.course_url)
        word_id = ""
        res = self.session.get(url=self.course_url, verify=self.verify)
        page = BeautifulSoup(res.content, 'html.parser')

        for row in page.find_all('div',attrs={"class" : "thing text-text"}):
            word_id = re.findall(r"\b\d{9}\b", str(row))
            # Avoid spamming the server too hard!
            time.sleep(1)
            self.post_delete_tts(word_id)

    def post_delete_tts(self, id):
        #id = '246045451'
        data = {
            'thing_id': (None,id),
            'column_key': (None,3),
            'file_id': (None, 1),
            'cell_type': (None,"column"),
            'csrfmiddlewaretoken': (None, self.csrftoken),
        }

        delete_audio = self.session.post(url="https://www.memrise.com/ajax/thing/column/delete_from/", headers=self.headers, data=data, verify=self.verify)
        print(delete_audio.status_code)

# MemAPI = MemriseAPI('5707706/wordsineedtolearnforyeseul')
# MemAPI.delete_course_tts()

# sm = Scrape_Memorise()
# sm.scrape()
# sm.update_course_TTS('course_name')
# #sm.write_to_file()

# Navigate to the next page and scrape the data


