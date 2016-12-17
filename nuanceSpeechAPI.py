from ndev.core import NDEVCredentials, HEADER, red, magenta
from ndev.asr import *
import speech_recognition as sr
import pandas as pd
import glob
import os

def nuanceTranscription(filename):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    creds = NDEVCredentials(ROOT_DIR + '\credentials.json')
    if not creds.has_credentials():
        print red("Please provide NDEV credentials.")
        return

    language = 'en_US'
    #language = 'en_IN'
    desired_asr_lang = ASR.get_language_input(language)
    #print "OK. Using Language: %s (%s)\n" % (desired_asr_lang['display'], desired_asr_lang['properties']['code'])

    try:
        asr_req = ASR.make_request(creds=creds, desired_asr_lang=desired_asr_lang, filename=ROOT_DIR+ '\\' + filename)

        if asr_req.response.was_successful():
            return asr_req.response.get_recognition_result()  # instead of looping through, pick head
        else:
            return asr_req.response.error_message
    except Exception as e:
        return e.message

if __name__ == '__main__':
    r = sr.Recognizer()
    #folder = 'data/transcribed/splitin60s'
    #folder = 'data/nishant'
    folder = 'data/simexp'
    os.chdir(folder)
    files = []
    results = []
    for file in glob.glob("*.wav*"):
        with sr.AudioFile(file) as source:
            audio = r.record(source)  # read the entire audio file
        print(file)

        try:
            #result = main(file)
            result = nuanceTranscription(folder+ '//' + file)
        except Exception as exception:
            result = repr(exception)
        print result
        result = ''.join([i if ord(i) < 128 else ' ' for i in result])
        files.append(file)
        results.append(result)
        fd = open('results_inter.csv', 'a')
        fd.write(file + ',' + result + '\n')
        fd.close()
        print 'DONE'
    ds = pd.DataFrame(data = {'Files': files, 'Trans':results})
    ds.to_csv('results.csv')
    print'-----DONE ALL-----'