# Docs for API https://cloud.google.com/translate/docs/reference/rest/v2/translate

import requests
import json

from settings import GOOGLE_TRANSLATE_KEY
from constants import GOOGLE_TRANSLATE_URL

class GoogleTranslate:

    def __init__(self):
        self.translate_url = GOOGLE_TRANSLATE_URL

    def translate_word(self, word):
        payload = { 'q': word, 
                    'target': 'ko',
                    'format': 'text',
                    'source': 'en',
                    'model': 'nmt',
                    'key': GOOGLE_TRANSLATE_KEY
                }
        res = requests.post(url=self.translate_url, data=payload).json()
        print(res)
        translated_word = res['data']['translations'][0]['translatedText']
        print(translated_word)

GoogleTranslate().translate_word('Hello')
