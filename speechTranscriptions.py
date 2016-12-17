import os, glob
import speech_recognition as sr
from config import *
import pandas as pd

def ibmSpeechToText(audio):
    # Settings - https://www.ibm.com/watson/developercloud/doc/speech-to-text/
    # Help - http://www.ibm.com/watson/developercloud/speech-to-text/api/v1/#recognize_sessionless_nonmp12
    # Languages - US, UK
    # Other features - keyword spotting, word alternatives,

    result = {}
    try:
        result['US'] =  r.recognize_ibm(audio,
                                  username=IBM_USERNAME,
                                  password=IBM_PASSWORD,
                                  language = 'en-US')
        print '  IBM US Data received - ' + result['US']
    except sr.UnknownValueError:
        print("IBM Speech to Text could not understand audio")
        result['US'] = "IBM Speech to Text could not understand audio"
    except sr.RequestError as e:
        print("Could not request results from IBM Speech to Text service; {0}".format(e))
        result['US'] = "Could not request results from IBM Speech to Text service; {0}".format(e)

    try:
        result['UK'] = r.recognize_ibm(audio,
                                 username=IBM_USERNAME,
                                 password=IBM_PASSWORD,
                                 language='en-UK')
        print '  IBM UK Data received - ' + result['UK']
    except sr.UnknownValueError:
        print("IBM Speech to Text could not understand audio")
        result['UK'] = "IBM Speech to Text could not understand audio"
    except sr.RequestError as e:
        print("Could not request results from IBM Speech to Text service; {0}".format(e))
        result['UK'] = "Could not request results from IBM Speech to Text service; {0}".format(e)
    return result

def googleSpeechToText(audio):
    # https://cloud.google.com/speech/
    # https://cloud.google.com/speech/docs/samples

    result = {}
    try:
        result['US'] = r.recognize_google(audio, language='en-US')
        print '  Google US Data received - ' + result['US']
    except sr.UnknownValueError:
        print("Google Speech to Text could not understand audio")
        result['US'] = "Google Speech to Text could not understand audio"
    except sr.RequestError as e:
        print("Could not request results from Google Speech to Text service; {0}".format(e))
        result['US'] = "Could not request results from Google Speech to Text service; {0}".format(e)

    try:
        result['IN'] = r.recognize_google(audio, language='en-IN')
        print '  Google IN Data received - ' + result['IN']
    except sr.UnknownValueError:
        print("Google Speech to Text could not understand audio")
        result['IN'] = "Google Speech to Text could not understand audio"
    except sr.RequestError as e:
        print("Could not request results from Google Speech to Text service; {0}".format(e))
        result['IN'] = "Could not request results from Google Speech to Text service; {0}".format(e)

    return result

def bingSpeechToText(audio):
    # https://www.microsoft.com/cognitive-services/en-us/speech-api
    # https://www.microsoft.com/cognitive-services/en-us/Speech-api/documentation/API-Reference-REST/BingVoiceRecognition
    # Languages - en-US, en-IN, en-CA, en-GB, en-NZ,

    result = {}
    try:
        result['US'] = r.recognize_bing(audio, key=BING_KEY, language = 'en-US')
        print '  Bing US Data received - ' + result['US']
    except sr.UnknownValueError:
        print("Bing Speech to Text could not understand audio")
        result['US'] = "Bing Speech to Text could not understand audio"
    except sr.RequestError as e:
        print("Could not request results from Bing Speech to Text service; {0}".format(e))
        result['US'] = "Could not request results from Bing Speech to Text service; {0}".format(e)

    try:
        result['IN'] = r.recognize_bing(audio, key=BING_KEY, language = 'en-IN')
        print '  Bing IN Data received - ' + result['IN']
    except sr.UnknownValueError:
        print("Bing Speech to Text could not understand audio")
        result['IN'] = "Bing Speech to Text could not understand audio"
    except sr.RequestError as e:
        print("Could not request results from Bing Speech to Text service; {0}".format(e))
        result['IN'] = "Could not request results from Bing Speech to Text service; {0}".format(e)

    return result

def sphinxSpeechToText(audio):
    result = {}
    try:
        result['A'] = r.recognize_sphinx(audio, language='en-CC')
        print 'Sphinx A Data received - ' + result['A']
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
        result['A'] = "Sphinx could not understand audio"
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))
        result['A'] = "Sphinx error; {0}".format(e)

    return result

if __name__ == '__main__':
    r = sr.Recognizer()

    #folder = 'data/videos'
    folder = 'data/flac'
    folder = 'data/transcribed'
    os.chdir(folder)

    files = []
    results_ibm_us = []
    results_bing_us = []
    results_ibm_uk = []
    results_bing_in = []
    results_sphinx_a = []
    google_in = []
    google_us = []
    bing_in = []
    bing_us = []
    sphinx = []
    ibm = []

    for AUDIO_FILE in glob.glob("*.flac*"):
        print(AUDIO_FILE)
        with sr.AudioFile(AUDIO_FILE) as source:
            audio = r.record(source)  # read the entire audio file


        # IBM Speech API
        #print ' IBM Speech to Text STARTED'
        #result_ibm = ibmSpeechToText(audio)
        #print ' IBM Speech to Text DONE'


        # Google speech recognition API
        #print ' Google Speech to Text STARTED'
        #result_google = googleSpeechToText(audio)
        #print ' Google Speech to Text DONE'

        # BING speech API
        #print ' Bing Speech to Text STARTED'
        #result_bing = bingSpeechToText(audio)
        #print ' Bing Speech to Text DONE'

        #  Sphinx
        print ' Sphinx Speech to Text STARTED'
        result_sphinx = sphinxSpeechToText(audio)
        print ' Sphinx Speech to Text DONE'

        files.append(AUDIO_FILE)

        #results_ibm_us.append(result_ibm['US'])
        #results_bing_us.append(result_bing['US'])
        results_sphinx_a.append(result_sphinx['A'])
        #results_ibm_uk.append(result_ibm['UK'])
        #results_bing_in.append(result_bing['IN'])
        print 'DONE'

    ds = pd.DataFrame(data = {
        'Files': files,
        #'IBM_US': results_ibm_us,
        #'IBM_UK': results_ibm_uk,
        'SPHINX_A': results_sphinx_a,
        #'BING_US': results_bing_us,
        #'BING_IN': results_bing_in,
    })
    ds.to_csv('results.csv')
    print'-----DONE ALL-----'