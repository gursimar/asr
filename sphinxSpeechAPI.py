from ndev.core import NDEVCredentials, HEADER, red, magenta
from ndev.asr import *
import pandas as pd
import argparse
import base64
import json
import glob
import os, re
import speech_recognition as sr

import sys
import numpy

##gives the csv dump (candidate id, audio name, transcription)
def transcript_dump(full_folder_path):
    candidate_id = []
    file_tag = []
    transcript=[]
    files = []
    results = []
    for path,dirs,files in os.walk(full_folder_path):
        for d in dirs:
            print(d)
            dir_name = full_folder_path+"/"+d
            print(dir_name)
            for f in os.listdir(dir_name):
                if (f.endswith(".wav")):
                    file_id = f[:-3]
                    file = dir_name + "/" + f
                    temp_module = file_id.split("_")
                    module_id = temp_module[1]
                    pattern = re.compile('.'+file_id+'.')
                    string='"*/'+file_id+'lab"'

                    # SIMAR CODE
                    with sr.AudioFile(file) as source:
                        audio = r.record(source)  # read the entire audio file
                    print(file)
                    try:
                        # result = main(file)
                        result = r.recognize_sphinx(audio, language='en-US')
                    except Exception as exception:
                        result = repr(exception)
                    print result

                    files.append(file)
                    results.append(result)

                    result = ''.join([i if ord(i) < 128 else ' ' for i in result])
                    fd = open('results_inter_sphinx.csv', 'a')
                    fd.write(file + ',' + result + '\n')
                    fd.close()
                    print 'DONE'

                    pass


    all_details = pd.DataFrame({'candidate_id':candidate_id,'file_tag':file_tag,'transcript':transcript})
    all_details.to_csv('transcript_candidates.csv')

if __name__ == '__main__':
    r = sr.Recognizer()
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\Gursimar\\repos\\python-docs-samples\\speech\\api-client\\simar-ae38c669c730.json"
    #folder = 'data/videos'
    #folder = 'data/nishant-all/nishant-googleleft'
    folder = 'data/rslr-test'

    transcript_dump(folder)
    exit()

    os.chdir(folder)
    files = []
    results = []
    for file in glob.glob("*.wav*"):
        with sr.AudioFile(file) as source:
            audio = r.record(source)  # read the entire audio file
        print(file)
        try:
            #result = main(file)
            result = r.recognize_google(audio ,language='en-IN')
        except Exception as exception:
            result = repr(exception)
        print result
        files.append(file)
        results.append(result)
        result = ''.join([i if ord(i) < 128 else ' ' for i in result])
        fd = open('results_inter.csv', 'a')
        fd.write(file + ',' + result + '\n')
        fd.close()
        print 'DONE'
    ds = pd.DataFrame(data = {'Files': files, 'Trans':results})
    ds.to_csv('results.csv')
    print'-----DONE ALL-----'