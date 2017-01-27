from ndev.core import NDEVCredentials, HEADER, red, magenta
from ndev.asr import *
import speech_recognition as sr
import pandas as pd
import glob
import os, re, base64

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

                    try:
                        # result = main(file)
                        result = nuanceTranscription(file)
                    except Exception as exception:
                        result = repr(exception)
                    print result

                    files.append(file)
                    results.append(result)

                    result = ''.join([i if ord(i) < 128 else ' ' for i in result])
                    fd = open('results_inter_nuance.csv', 'a')
                    fd.write(file + ',' + result + '\n')
                    fd.close()
                    print 'DONE'

                    pass


    all_details = pd.DataFrame({'candidate_id':candidate_id,'file_tag':file_tag,'transcript':transcript})
    all_details.to_csv('transcript_candidates.csv')


if __name__ == '__main__':
    r = sr.Recognizer()
    #folder = 'data/transcribed/splitin60s'
    folder = 'data/freespeech/freespeech-test'
    #folder = 'data/rslr-test'
    #transcript_dump(folder)
    #exit()
    os.chdir(folder)
    files = []
    results = []
    for file in glob.glob("*.wav*"):
    #for file in file_list:
        try:
            #result = main(file)
            result = nuanceTranscription(folder+ '//' + file)
            #result = nuanceTranscription(file)
            result = ''.join([i if ord(i) < 128 else ' ' for i in result])
            files.append(file)
            results.append(result)
        except Exception as exception:
            result = repr(exception)
            files.append(file)
            results.append(result)
        print result
        rsult = str(result)
        fd = open('results_inter_nuance_in.csv', 'a')
        fd.write(file + ',' + str(base64.b64encode(result)) + '\n')
        fd.close()

    print 'DONE'
    ds = pd.DataFrame(data = {'Files': files, 'Trans':results})
    ds.to_csv('results_nuance.csv')
    print'-----DONE ALL-----'