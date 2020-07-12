import requests
import constants
import base64
import json
import os

class PapagoTTS:

    def __init__(self):
        self.speaker = 'kyuri'
        self.speed = constants.Speed.NORMAL
        self.prefix = constants.PREFIX
        self.translate_init = constants.TRANSLATE_INIT
        self.naver_tts_headers = constants.NAVER_TTS_HEADERS
        self.translate_endpoint = constants.TRANSLATE_ENDPOINT
        self.folder = "AudioFiles/"

        self.words = []


    def translate_list(self, words):
        self.words = words
        for word in self.words:
            payload = self.craft_request(word)
            audio = self.send_request(payload)
            self.save_file(audio, word)
    
    def translate_txt_file(self, file):
        with open(file, 'r', encoding='utf-8') as f:
            for line in f:
                self.words.append(line[:-1])
        for word in self.words:
            payload = self.craft_request(word)
            audio = self.send_request(payload)
            self.save_file(audio, word)

    def craft_request(self, word):   
        data = 'pitch":0,"speaker":"{speaker}","speed": "{speed}","text":"{text}"'.format(
                speaker=self.speaker,
                speed=self.speed,
                text=word) + '}'
        payload = {'data': base64.b64encode(self.prefix + bytes(data, 'utf-8')).decode()}
        return payload
        

    def send_request(self, payload):
        res = requests.get(url=self.translate_init, params=payload, headers=self.naver_tts_headers)
        print(res.content)
        translate_id = json.loads(res.content)['id']
        endpoint_url = self.translate_endpoint.format(id=translate_id)
        audio = requests.get(url=endpoint_url, headers=self.naver_tts_headers)     
        return audio
    
    def save_file(self, res, word):
        filename = "{path}{filename}{file_ext}".format(path=self.folder, filename=word, file_ext='.mp3')
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
        with open(filename, 'wb') as f:
            for chunk in res.iter_content(chunk_size=1024):
                f.write(chunk)

words = ['안녕하세요', '잘 지냈어요']


tts = PapagoTTS()
tts.translate_txt_file("wordlist.txt")
#tts.translate_list(words)