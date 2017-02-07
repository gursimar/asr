import re
import os
import pandas as pd

allTranscripts = open('data/words_94.mlf')
all_transcripts_94 = allTranscripts.read()
all_transcripts_94 = all_transcripts_94.split('\n')

allTranscripts_ = open('data/words_97.mlf')
all_transcripts_97 = allTranscripts_.read()
all_transcripts_97 = all_transcripts_97.split('\n')

allTranscripts_ = open('data/words_226.mlf')
all_transcripts_226 = allTranscripts_.read()
all_transcripts_226 = all_transcripts_226.split('\n')


##get transcription for every audio file.
def per_audio_transcript(fileid,module_id):
    trans =[]
    flag = 0
    
    all_transcripts=[]
    if (int(module_id) == 94):  ##checks the module. Should be either 94/97. If not, return empty trans.
        all_transcripts = all_transcripts_94
    elif (int(module_id) == 97):
            all_transcripts = all_transcripts_97
    else:
        if (int(module_id) == 226):
            all_transcripts = all_transcripts_226

    for t in all_transcripts:
        if (flag==0):
            m = re.search(fileid,t)
            if (m is not None):
                flag = 1
        else:
            if (t!='.'):
                trans.append(t)
            else:
                flag = 0
    trans = trans[1:-1]
    trans = " ".join(trans)
    return trans

##gives the csv dump (candidate id, audio name, transcription)
def transcript_dump(full_folder_path):
    candidate_id = []
    file_tag = []
    transcript=[]
    for path,dirs,files in os.walk(full_folder_path):
        for d in dirs:
            print(d)
            dir_name = full_folder_path+"/"+d
            print(dir_name)
            for f in os.listdir(dir_name):
                if (f.endswith(".wav")):
                    file_id = f[:-3]
                    temp_module = file_id.split("_")
                    module_id = temp_module[1]
                    pattern = re.compile('.'+file_id+'.')
                    string='"*/'+file_id+'lab"'
                    trans = per_audio_transcript(string,module_id)
                    if (trans!=''):
                        candidate_id.append(d)
                        file_tag.append(f)
                        transcript.append(trans)
                    else:
                        print("candidate_id: " + d + ", audio file: " + f + ": Not found : Free speech")
    all_details = pd.DataFrame({'candidate_id':candidate_id,'file_tag':file_tag,'transcript':transcript})
    all_details.to_csv('sample.csv')
    
##change this.
###give full path to the folder which has all candidates.
transcript_dump('data/rslr-test')