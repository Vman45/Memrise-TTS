import os

from memriseAPI import MemriseAPI
from papago_tts import PapagoTTS
from papago_translate import PapagoTranslate

# Supply the english wordlist and it will translate and upload to the course you specified
def upload_new_words(course, wordlist=False):


    if os.path.isfile(wordlist):
        print ("File {filename} found".format(filename=wordlist))
    else:
        print("File with name {filename} cannot be opened, it might not exist".format(filename=wordlist))
        return

    # Uses the generated word list to download the TTS for every word 
    PapTTS = PapagoTTS(speaker='jinho', speed='3')

    # # Download the TTS and pass the word list back to us as array
    words = PapTTS.download_TTS("wordlist.txt")
    PapTrans =  PapagoTranslate()
    PapTrans.translate_list(words)

    # init memrise with a course URL
    memAPI = MemriseAPI(course)

    # Bulk add words to wordlist
    memAPI.bulk_add_words()

    # Upload the TTS
    memAPI.update_course_TTS(words)

def add_tts(course):

    # init memrise with a course URL
    memAPI = MemriseAPI(course)

    # Loads to page into an Array
    memAPI.scrape_wordlist()

    # Uses the generated word list to download the TTS for every word 
    PapTTS = PapagoTTS(speaker='jinho', speed='3')

    # # Download the TTS and pass the word list back to us as array
    words = PapTTS.download_TTS("wordlist.txt")

    # Upload the TTS
    memAPI.update_course_TTS(words)

    pass

def delete_tts(course):
    # init memrise with a course URL
    memAPI = MemriseAPI(course)
    
    memAPI.delete_course_tts()



## MAIN FUNCTIONS

# upload_new_words(course='5757638/daneoneun-sinaessi-wihae-baeugi-pilyohaeyo/',wordlist='wordlist.txt')

add_tts(course='5757638/daneoneun-sinaessi-wihae-baeugi-pilyohaeyo/')

# delete_tts(course='5757638/daneoneun-sinaessi-wihae-baeugi-pilyohaeyo/')