#!/usr/bin/env python
# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Google Cloud Speech API sample application using the REST API for batch
processing."""

# [START import_libraries]
from ndev.core import NDEVCredentials, HEADER, red, magenta
from ndev.asr import *
import pandas as pd
import argparse
import base64
import json
import glob
import os, re

#-*- coding: utf-8 -*-
#!/usr/bin/env python
'''
Code re-used from https://github.com/zszyellow/WER-in-python
'''

import sys
import numpy

from googleapiclient import discovery
import httplib2
from oauth2client.client import GoogleCredentials
import speech_recognition as sr

# [END import_libraries]


# [START authenticating]
DISCOVERY_URL = ('https://{api}.googleapis.com/$discovery/rest?'
                 'version={apiVersion}')


# Application default credentials provided by env variable
# GOOGLE_APPLICATION_CREDENTIALS
def get_speech_service():
    credentials = GoogleCredentials.get_application_default().create_scoped(
        ['https://www.googleapis.com/auth/cloud-platform'])
    http = httplib2.Http()
    credentials.authorize(http)

    return discovery.build(
        'speech', 'v1beta1', http=http, discoveryServiceUrl=DISCOVERY_URL)
# [END authenticating]


def main(speech_file):
    """Transcribe the given audio file.

    Args:
        speech_file: the name of the audio file.
    """
    # [START construct_request]
    #with open(speech_file, 'rb') as speech:
    #    # Base64 encode the binary audio file for inclusion in the JSON
    #    # request.
    #    speech_content = base64.b64encode(speech.read())

    flac_data = speech_file.get_flac_data(
        convert_rate=None if speech_file.sample_rate >= 8000 else 8000,  # audio samples must be at least 8 kHz
        convert_width=2  # audio samples must be 16-bit
    )
    speech_content = base64.b64encode(flac_data)
    service = get_speech_service()
    service_request = service.speech().syncrecognize(
        body={
            'config': {
                # There are a bunch of config options you can specify. See
                # https://goo.gl/KPZn97 for the full list.
                #'encoding': 'LINEAR16',  # raw 16-bit signed LE samples
                'encoding': 'FLAC',  # raw 16-bit signed LE samples
                'sampleRate': 8000,  # 16 khz
                # See http://g.co/cloud/speech/docs/languages for a list of
                # supported languages.
                #'languageCode': 'en-US',  # a BCP-47 language tag
                'languageCode': 'en-IN',  # a BCP-47 language tag
            },
            'audio': {
                'content': speech_content.decode('UTF-8')
                }
            })
    # [END construct_request]
    # [START send_request]
    response = service_request.execute()
    print(json.dumps(response))
    return json.dumps(response)
    # [END send_request]

# [START run_application]
# SET GOOGLE_APPLICATION_CREDENTIALS=C:\Users\Gursimar\repos\python-docs-samples\speech\api-client\simar-ae38c669c730.json
# echo %GOOGLE_APPLICATION_CREDENTIALS%
# sox file.abc --channels=1 --bits=16 --rate=16000 --endian=little audio.flac

def unserializeTranslations():
    data = pd.DataFrame.from_csv('./data/freespeech/freespeech-test/results_google.csv')

    files =[]
    confidencesUS = []
    transcriptsUS = []
    confidencesIN = []
    transcriptsIN = []
    for index, row in data.iterrows():
        files.append(row['Files'])
        try:
            in_data = json.loads(row['Trans IN'])['results']
            confidence = []
            transcript = []
            for alter in in_data:
                confidence.append(alter['alternatives'][0]['confidence'])
                transcript.append(alter['alternatives'][0]['transcript'])
            confidence = sum(confidence) / len(confidence)
            transcript = ''.join(transcript)
            confidencesIN.append(confidence)
            transcriptsIN.append(transcript)
        except:
            confidencesIN.append('')
            transcriptsIN.append('')
        try:
            us_data = json.loads(row['Trans US'])['results']
            confidence = []
            transcript = []
            for alter in us_data:
                confidence.append(alter['alternatives'][0]['confidence'])
                transcript.append(alter['alternatives'][0]['transcript'])
            confidence = sum(confidence)/ len(confidence)
            transcript = ''.join(transcript)
            confidencesUS.append(confidence)
            transcriptsUS.append(transcript)
        except:
            confidencesUS.append('')
            transcriptsUS.append('')
    results = pd.DataFrame({
        'Files':files,
        'transcriptsUS':transcriptsUS,
        'transcriptsIN': transcriptsIN,
        'confidencesUS': confidencesUS,
        'confidencesIN': confidencesIN
    })
    results.to_csv('./results/google_ASR_Results.csv')



##gives the csv dump (candidate id, audio name, transcription)
def folder_spider(full_folder_path):
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
                        result = r.recognize_google(audio, language='en-IN')
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

                    pass


    all_details = pd.DataFrame({'candidate_id':candidate_id,'file_tag':file_tag,'transcript':transcript})
    all_details.to_csv('transcript_candidates.csv')

if __name__ == '__main__':
    unserializeTranslations()
    exit()
    r = sr.Recognizer()
    #os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\Gursimar\\repos\\python-docs-samples\\speech\\api-client\\simar-ae38c669c730.json"
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\Gursimar\\repos\\python-docs-samples\\speech\\api-client\\try-apis-bd5cef16b431.json"
    #folder = 'data/videos'
    folder = 'data/freespeech/freespeech-test'
    #folder = 'data/rslr-test'

    #folder_spider(folder)
    #exit()

    os.chdir(folder)
    files = []
    results = []
    for file in glob.glob("*.wav*"):
        with sr.AudioFile(file) as source:
            audio = r.record(source)  # read the entire audio file
        print(file)
        try:
            result = main(audio)
            #result = r.recognize_google(audio ,language='en-IN')
        except Exception as exception:
            result = repr(exception)
        print result
        files.append(file)
        results.append(result)
        #result = ''.join([i if ord(i) < 128 else ' ' for i in result])
        fd = open('results_inter_google_in.csv', 'a')
        fd.write(file + ',' + str(base64.b64encode(result)) + '\n')
        fd.close()
        print 'DONE'
    ds = pd.DataFrame(data = {'Files': files, 'Trans':results})
    ds.to_csv('results_google.csv')
    print'-----DONE ALL-----'