# Docs for API https://apidocs.ncloud.com/en/ai-naver/papago_nmt/
# Api Usage https://developers.naver.com/apps/#/myapps/RVSabbsncGosBkd4rHM_/overview

import requests
import json
import csv

from settings import NAVER_CLIENT_ID, NAVER_CLIENT_SECRET
import constants

class PapagoTranslate:

    def __init__(self):
        self.translate_url = constants.PAPAGO_TRANSLATE_URL
        self.headers = constants.PAPAGO_HEADERS
        self.csv_name = 'wordlist.csv'

        self.translated_words = []

        if constants.DEBUG == True:
            self.verify = constants.DEBUG_CERT
        else:
            self.verify = True

    def translate_word(self, word):
        
        payload = { 
                'source': 'ko',
                'target': 'en',
                'text': word,
                }

        res = requests.post(url=self.translate_url, headers=self.headers, data=payload, verify=self.verify).json()
        return res['message']['result']['translatedText']

    def translate_list(self, wordlist):

        for word in wordlist:
            payload = { 
                'source': 'ko',
                'target': 'en',
                'text': word,
                }
            res = requests.post(url=self.translate_url, headers=self.headers, data=payload, verify=self.verify).json()
            self.translated_words.append([word, res['message']['result']['translatedText']])
        self.write_to_csv()
    
    def write_to_csv(self):

        try:
            with open('wordlist.csv', 'w', encoding='utf-8', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(self.translated_words)
            print("CSV \"wordlist.csv\" has been created")
            return
        except Exception as e:
            print("failed to create wordlist.csv")
            return

        
