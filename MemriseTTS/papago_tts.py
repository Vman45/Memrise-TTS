import requests
import constants
import base64
import json
import os

class PapagoTTS:

    def __init__(self, speaker, speed):
        self.speaker = speaker

        # Speed 3 is slow 0 is normal
        self.speed = speed
        self.file_ext = '.mp3'
        self.prefix = constants.PREFIX
        self.translate_req = constants.TTS_TRANSLATE_REQUEST
        self.translate_down = constants.TTS_TRANSLATE_DOWNLOAD
        self.naver_tts_headers = constants.NAVER_TTS_HEADERS
        self.folder = "AudioFiles/"
        self.words = []

        self.sucess_counter = 0
        self.already_downloaded = 0

    # Was used for testing lists in memory
    # def translate_list(self, words):
    #     self.words = words
    #     for word in self.words:
    #         payload = self.craft_request(word)
    #         audio = self.send_request(payload)
    #         self.save_file(audio, word)
    
    def download_TTS(self, file):
        with open(file, 'r', encoding='utf-8') as f:
            for line in f:
                self.words.append(line[:-1])
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
        for word in self.words:
            # Avoid sending requests for downloaded files
            if os.path.isfile("{path}{filename}{file_ext}".format(path=self.folder, filename=word, file_ext=self.file_ext)):
                self.already_downloaded += 1
                continue
            else:
                payload = self.craft_request(word)
                audio = self.send_request(payload)
                self.save_file(audio, word)
        print("Word list had {0} words, {1} were already downloaded and {2} downloaded sucessfully".format(len(self.words), self.already_downloaded, self.sucess_counter))
        return self.words

    def craft_request(self, word):   
        data = 'pitch":0,"speaker":"{speaker}","speed": "{speed}","text":"{text}"'.format(
                speaker=self.speaker,
                speed=self.speed,
                text=word) + '}'
        payload = {'data': base64.b64encode(self.prefix + bytes(data, 'utf-8')).decode()}
        return payload
        
    def send_request(self, payload):
        res = requests.get(url=self.translate_req, params=payload, headers=self.naver_tts_headers)
        #print(res.content)
        translate_id = json.loads(res.content)['id']
        endpoint_url = self.translate_down.format(id=translate_id)
        audio = requests.get(url=endpoint_url, headers=self.naver_tts_headers)     
        return audio
    
    def save_file(self, res, word):
        filename = "{path}{filename}{file_ext}".format(path=self.folder, filename=word, file_ext=self.file_ext)
        try:
            with open(filename, 'wb') as f:
                for chunk in res.iter_content(chunk_size=1024):
                    f.write(chunk)
            self.sucess_counter += 1
        except Exception as e:
            print("Could not create file with name {filename}{file_ext}, perhaps invalid characters".format(filename=word, file_ext=self.file_ext))

