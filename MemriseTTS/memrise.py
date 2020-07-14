import os

from memriseAPI import MemriseAPI
from papago_tts import PapagoTTS
from papago_translate import PapagoTranslate

def main(course, wordlist=False):

    if wordlist:
        if os.path.isfile(wordlist):
            print ("File {filename} found".format(filename=wordlist))
        else:
            print("File with name {filename} cannot be opened, it might not exist".format(filename=wordlist))
            return
    else:
        return
        # Loads to page into an Array
        # memAPI.scrape_wordlist()

    # Uses the generated word list to download the TTS for every word 
    PapTTS = PapagoTTS()

    # # Download the TTS and pass the word list back to us as array
    words = PapTTS.download_TTS("wordlist.txt")
    # PapTrans =  PapagoTranslate()
    # PapTrans.translate_list(words)

    # init memrise with a course URL
    memAPI = MemriseAPI(course)

    # # Bulk add words to wordlist
    # memAPI.bulk_add_words()

    # Upload the TTS
    memAPI.update_course_TTS(words)



main(course='5761720/test_course_999/',wordlist='wordlist.txt')