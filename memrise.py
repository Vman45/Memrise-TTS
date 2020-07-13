from memriseAPI import MemriseAPI
from papago_tts import PapagoTTS

def main():
    # init memrise with a courss URL
    memAPI = MemriseAPI('5737099/adamlist1/')
    PapTTS = PapagoTTS()
    
    # # Loads to page into an Array
    memAPI.scrape_wordlist()

    # # Uses the generated word list to download the TTS for every word
    # PapTTS.download_TTS("wordlist.txt")

    memAPI.update_course_TTS()


main()