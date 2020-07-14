# Docs for API https://apidocs.ncloud.com/en/ai-naver/papago_nmt/

import requests
import json

from settings import NAVER_CLIENT_ID, NAVER_CLIENT_SECRET
import constants

class PapagoTranslate:

    def __init__(self):
        self.translate_url = constants.PAPAGO_TRANSLATE_URL
        self.headers = constants.PAPAGO_HEADERS

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
        print(res['message']['result']['translatedText'])
        #print(translated_word)

PapagoTranslate().translate_word('안녕')
