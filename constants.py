DEBUG = False

class Speed:
    """Read Speed
    """
    SLOW = 5
    NORMAL = 0
    FAST = -5

# No idea why this is needed but just is
PREFIX = b'\xaeU\xae\xa1C\x9b,Uzd\xf8\xef'

TRANSLATE_INIT = 'https://papago.naver.com/apis/tts/makeID'
TRANSLATE_ENDPOINT = 'https://papago.naver.com/apis/tts/{id}'

NAVER_TTS_HEADERS = {
        "Referer": "http://papago.naver.com/",
        "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; WOW64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/47.0.2526.106 Safari/537.36"
}

MEMRISE_HEADERS = {
        #"Authority": "www.memrise.com",
        #"Origin": "http://www.memrise.com",
        "DNT" : "1",
        "Referer" : "https://www.memrise.com/course/{course}",
        "User-Agent": 
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" 
                "AppleWebKit/537.36 (KHTML, like Gecko)" 
                "Chrome/83.0.4103.116 Safari/537.36"
}

MEMRISE_COURSE_URL = "https://www.memrise.com/course/"
MEMRISE_LOGIN_URL = "https://www.memrise.com/login/"

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