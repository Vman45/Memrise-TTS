from bs4 import BeautifulSoup
from lxml import html
import requests
import re
import time
import csv

import constants

# change this to your memorise username and password
from settings import MEMORISE_USERNAME, MEMORISE_PASSWORD


class MemriseAPI:

    def __init__(self, course):
        self.session = requests.Session()
        self.words = []
        self.headers = constants.MEMRISE_HEADERS
        self.login_url = constants.MEMRISE_LOGIN_URL
        
        # Creates the full course URL in format URL_STEM + "5757638/daneoneun-sinaessi-wihae-baeugi-pilyohaeyo"
        self.course_url = constants.MEMRISE_COURSE_URL + course

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

    # Get course page
    def scrap_course_page(self):
        print(self.course_url)
        word_id = ""
        res = self.session.get(url=self.course_url, verify=self.verify)
        page = BeautifulSoup(res.content, 'html.parser')
        return page

    # Iterates through all the words in the page and posts the correct TTS
    def update_course_TTS(self, wordlist):
        page = self.scrap_course_page()
        # Only update the words in the word list
        self.words = wordlist
        for row in page.find_all('div',attrs={"class" : "thing text-text"}):
            # Match the target word to it's ID
            if row.contents[2].text in self.words:
                    # Find the 9 digit data-thing-id
                    word_id = re.findall(r"\b\d{9}\b", str(row))
                    # Avoid spamming the server too hard!
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
        time.sleep(1)
    
    def delete_course_tts(self):

        page = self.scrap_course_page()
        for row in page.find_all('div',attrs={"class" : "thing text-text"}):
            word_id = re.findall(r"\b\d{9}\b", str(row))
            # Avoid spamming the server too hard!      
            self.post_delete_tts(word_id)

    def post_delete_tts(self, id):
        data = {
            'thing_id': (None,id),
            'column_key': (None,3),
            'file_id': (None, 1),
            'cell_type': (None,"column"),
            'csrfmiddlewaretoken': (None, self.csrftoken),
        }

        delete_audio = self.session.post(url="https://www.memrise.com/ajax/thing/column/delete_from/", headers=self.headers, data=data, verify=self.verify)
        print(delete_audio.status_code)
        time.sleep(1)
    
    def bulk_add_words(self):
        
        words = ""

        try:
            with open('wordlist.csv', 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    words += "{0},{1}\n".format(row[0],row[1])
            print("CSV \"wordlist.csv\" exists and has been opened")
        except Exception as e:
            print("failed to open wordlist.csv", e)
            return


        data = {
            'word_delimiter': 'comma',
            'data': words,
            # This level id needs to be made a variable
            'level_id': '12735486',
            'csrfmiddlewaretoken': (None, self.csrftoken),
        }

        res = self.session.post(url="https://www.memrise.com/ajax/level/add_things_in_bulk/", headers=self.headers, data=data, verify=self.verify)
        print(res.status_code)
        if res.status_code == "200":
            print("Words bulk added")
        else:
            print("bulk add failed")



