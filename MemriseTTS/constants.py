from settings import NAVER_CLIENT_ID, NAVER_CLIENT_SECRET

DEBUG = False
DEBUG_CERT = r"FiddlerRoot.pem"

# No idea why this is needed but just is
PREFIX = b'\xaeU\xae\xa1C\x9b,Uzd\xf8\xef'

TTS_TRANSLATE_REQUEST = 'https://papago.naver.com/apis/tts/makeID'
TTS_TRANSLATE_DOWNLOAD = 'https://papago.naver.com/apis/tts/{id}'

NAVER_TTS_HEADERS = {
        "DNT" : "1",
        "Referer": "http://papago.naver.com/",
        "User-Agent": 
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" 
                "AppleWebKit/537.36 (KHTML, like Gecko)" 
                "Chrome/83.0.4103.116 Safari/537.36"
}

MEMRISE_HEADERS = {
        "DNT" : "1",
        "Referer" : "https://www.memrise.com/",
        "User-Agent": 
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" 
                "AppleWebKit/537.36 (KHTML, like Gecko)" #
                
                "Chrome/83.0.4103.116 Safari/537.36"
}

PAPAGO_HEADERS = {
        "DNT" : "1",
        "X-Naver-Client-Id" : NAVER_CLIENT_ID,
        "X-Naver-Client-Secret" : NAVER_CLIENT_SECRET,
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        "User-Agent": 
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" 
                "AppleWebKit/537.36 (KHTML, like Gecko)" 
                "Chrome/83.0.4103.116 Safari/537.36"
}

MEMRISE_COURSE_URL = "https://www.memrise.com/course/"
MEMRISE_LOGIN_URL = "https://www.memrise.com/login/"
PAPAGO_TRANSLATE_URL = "https://openapi.naver.com/v1/papago/n2mt"
GOOGLE_TRANSLATE_URL = 'https://translation.googleapis.com/language/translate/v2'

LANGUAGES = {
        'en': 'English',
        'ko': 'Korean',
}

SPEAKERS = {
    'ko' : {'f' : 'kyuri',
            'm' : 'jinho'},
    'en' : {'f' : 'clara',
            'm' : 'matt'}
}