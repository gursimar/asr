import numpy
import pandas as pd
import glob, os, string
from nltk.corpus import stopwords

class speechAnalyze():
    def __init__(self):
        # Reference text, Hypothesized text
        pass

    def bagOfWords(self, r, h):
        r = r.split()
        h = h.split()

        # Reuse of words is allowed
        words = []
        for word in h:
            if word in r:
                words.append(word)

        # If one word is used, then we don't reuse it.
        words_hey = []
        r_mod = list(r)
        for word in h:
            if word in r_mod:
                ind = r_mod.index(word)
                del r_mod[ind]
                words_hey.append(word)

        # print corr
        # print len(h)
        # print len(r)

        if len(h) ==0:
            result = {
                # normal idea
                'precision_all': float(0),  # how many selected items are relevant
                'recall_all': float(0),  # how many relevant items are selected
                'comm_words': '',

                # Take unique words in hypothesis and actual
                'precision_unique': float(0),
                'recall_unique': float(0),
                'comm_words_unique': '',

                # Remove a word once its used
                'precision_remove': float(0),  # how many selected items are relevant
                'recall_remove': float(0),  # how many relevant items are selected
                'comm_words_remove': ''
            }
        else:
            result = {
                # normal idea
                'precision_all': float(len(words)) / len(h),  # how many selected items are relevant
                'recall_all': float(len(words)) / len(r),  # how many relevant items are selected
                'comm_words': words,

                # Take unique words in hypothesis and actual
                'precision_unique': float(len(set(words))) / len(set(h)),
                'recall_unique': float(len(set(words))) / len(set(r)),
                'comm_words_unique': set(words),

                # Remove a word once its used
                'precision_remove': float(len(words_hey))/len(h), # how many selected items are relevant
                'recall_remove': float(len(words_hey))/len(r), # how many relevant items are selected
                'comm_words_remove': words_hey
            }
        return result

    def bagOfTwWords(self, r, h):
        r = r.split()
        h = h.split()
        words = []
        for word in h:
            if word in r:
                words.append(word)

        words_hey = []
        r_mod = list(r)
        for word in h:
            if word in r_mod:
                ind = r_mod.index(word)
                del r_mod[ind]
                words_hey.append(word)

        #print corr
        #print len(h)
        #print len(r)
        result = {
            # how many selected items are relevant
            'precision_all': float(len(words_hey))/len(h),
            # how many relevant items are selected
            'recall_all': float(len(words_hey))/len(r),

            # Take unique words in hypothesis and actual
            'precision_unique': float(len(set(words))) / len(set(h)),
            'recall_unique': float(len(set(words))) / len(set(r)),

            # Remove a word once its used
            #'precision_unqiue': float(len(set(words))) / len(set(h)),
            #'recall_unique': float(len(set(words))) / len(set(r)),

            'comm_words':words_hey
        }
        return result

    def wer(self, r, h):
        """
        This is a function that calculate the word error rate in ASR.
        Just provide the function with two strings
        model.predict('This is a boy','boy this is')
        """
        #
        #Store the diff text

        import sys
        import StringIO
        stdout = sys.stdout  # keep a handle on the real standard output
        sys.stdout = StringIO.StringIO()  # Choose a file-like object to write to

        #build the matrix
        r = r.split()
        h = h.split()
        d = numpy.zeros((len(r)+1)*(len(h)+1), dtype=numpy.uint8).reshape((len(r)+1, len(h)+1))
        for i in range(len(r)+1):
            for j in range(len(h)+1):
                if i == 0: d[0][j] = j
                elif j == 0: d[i][0] = i
        for i in range(1,len(r)+1):
            for j in range(1, len(h)+1):
                if r[i-1] == h[j-1]:
                    d[i][j] = d[i-1][j-1]
                else:
                    substitute = d[i-1][j-1] + 1
                    insert = d[i][j-1] + 1
                    delete = d[i-1][j] + 1
                    d[i][j] = min(substitute, insert, delete)
        result = float(d[len(r)][len(h)]) / len(r) * 100
        result = str("%.2f" % result) + "%"

        #find out the manipulation steps
        x = len(r)
        y = len(h)
        list = []
        while True:
            if x == 0 and y == 0:
                break
            else:
                if d[x][y] == d[x-1][y-1] and r[x-1] == h[y-1]:
                    list.append("e")
                    x = x-1
                    y = y-1
                elif d[x][y] == d[x][y-1]+1:
                    list.append("i")
                    x = x
                    y = y-1
                elif d[x][y] == d[x-1][y-1]+1:
                    list.append("s")
                    x = x-1
                    y = y-1
                else:
                    list.append("d")
                    x = x-1
                    y = y
        list = list[::-1]

        #print the result in aligned way
        print "REF:",
        for i in range(len(list)):
            if list[i] == "i":
                count = 0
                for j in range(i):
                    if list[j] == "d":
                        count += 1;
                index = i - count
                print " "*(len(h[index])),
            elif list[i] == "s":
                count1 = 0
                for j in range(i):
                    if list[j] == "i":
                        count1 += 1;
                index1 = i - count1
                count2 = 0
                for j in range(i):
                    if list[j] == "d":
                        count2 += 1;
                index2 = i - count2
                if len(r[index1])<len(h[index2]):
                    print r[index1]+" "*(len(h[index2])-len(r[index1])),

                else:
                    print r[index1],
            else:
                count = 0
                for j in range(i):
                    if list[j] == "i":
                        count += 1;
                index = i - count
                print r[index],
        print
        print "HYP:",
        for i in range(len(list)):
            if list[i] == "d":
                count = 0
                for j in range(i):
                    if list[j] == "i":
                        count += 1;
                index = i - count
                print " "*(len(r[index])),
            elif list[i] == "s":
                count1 = 0
                for j in range(i):
                    if list[j] == "i":
                        count1 += 1;
                index1 = i - count1
                count2 = 0
                for j in range(i):
                    if list[j] == "d":
                        count2 += 1;
                index2 = i - count2
                if len(r[index1])>len(h[index2]):
                    print h[index2]+" "*(len(r[index1])-len(h[index2])),
                else:
                    print h[index2],
            else:
                count = 0
                for j in range(i):
                    if list[j] == "d":
                        count += 1;
                index = i - count
                print h[index],
        print
        print "EVA:",
        for i in range(len(list)):
            if list[i] == "d":
                count = 0
                for j in range(i):
                    if list[j] == "i":
                        count += 1;
                index = i - count
                print "D"+" "*(len(r[index])-1),
            elif list[i] == "i":
                count = 0
                for j in range(i):
                    if list[j] == "d":
                        count += 1;
                index = i - count
                print "I"+" "*(len(h[index])-1),
            elif list[i] == "s":
                count1 = 0
                for j in range(i):
                    if list[j] == "i":
                        count1 += 1;
                index1 = i - count1
                count2 = 0
                for j in range(i):
                    if list[j] == "d":
                        count2 += 1;
                index2 = i - count2
                if len(r[index1])>len(h[index2]):
                    print "S"+" "*(len(r[index1])-1),
                else:
                    print "S"+" "*(len(h[index2])-1),
            else:
                count = 0
                for j in range(i):
                    if list[j] == "i":
                        count += 1;
                index = i - count
                print " "*(len(r[index])),
        print
        print "WER: "+result
        diffText = sys.stdout.getvalue()
        sys.stdout = stdout

        resultDict = {
            'diff': diffText,
            'wer': result
        }
        return resultDict

if __name__ == '__main__':
    sa = speechAnalyze()
    wer = []
    precision_all = []
    recall_all = []
    common_words_all = []
    precision_remove = []
    recall_remove = []
    common_words_remove = []
    precision_uniq = []
    recall_uniq = []
    common_words_uniq = []

    precision_all_wo_stop = []
    recall_all_wo_stop = []
    common_words_all_wo_stop = []
    precision_remove_wo_stop = []
    recall_remove_wo_stop = []
    common_words_remove_wo_stop = []
    precision_uniq_wo_stop = []
    recall_uniq_wo_stop = []
    common_words_uniq_wo_stop = []

    names = []
    transcripts = []
    actuals = []
    wer_result = []
    types = []

    folder = 'results/rslr-225'
    #folder = 'results/freespeech/500'
    os.chdir(folder)
    for file in glob.glob("input_*"):
        print file
        data = pd.DataFrame.from_csv(file, index_col='User ID')
        for index, row in data.iterrows():
            name = row['Name']
            #print name
            transcript = str(row['transcript'])
            actual = str(row['Actual'])

            # some preprocessing
            transcript = transcript.lower()
            actual = actual.lower()
            actual = "".join(c for c in actual if c not in ('!', '.', ':', ',', ';', '<', '>', '(', ')', '"', '[', ']'))

            # calculate bag of words error after removing stop words
            stop_words = set(stopwords.words('english'))
            actual_words = actual.split()
            transcript_words = transcript.split()
            resultwords = [word for word in actual_words if word.lower() not in stop_words]
            actual_wo_stop = ' '.join(resultwords)
            resultwords = [word for word in transcript_words if word.lower() not in stop_words]
            transcript_wo_stop = ' '.join(resultwords)
            if (len(transcript_wo_stop) ==0 or len(transcript) == 0):
                print 'Some panga'
                # IN THIS IMP EDGE CASE
                # WE ASSIGN ALL METICS TO BE 0
                # WER TO BE 100
                # THESE ARE SIMPLY BAD CASES
                #continue

            names.append(name)
            transcripts.append(transcript)
            actuals.append(actual)

            # calculate bag of words error
            ind = sa.bagOfWords(actual, transcript)
            precision_all.append(ind['precision_all'])
            recall_all.append(ind['recall_all'])
            common_words_all.append(ind['comm_words']),
            precision_uniq.append(ind['precision_unique'])
            recall_uniq.append(ind['recall_unique'])
            common_words_uniq.append(ind['comm_words_unique']),
            precision_remove.append(ind['precision_remove'])
            recall_remove.append(ind['recall_remove'])
            common_words_remove.append(ind['comm_words_remove']),


            ind_wo_stop = sa.bagOfWords(actual_wo_stop, transcript_wo_stop)

            precision_all_wo_stop.append(ind_wo_stop['precision_all'])
            recall_all_wo_stop.append(ind_wo_stop['recall_all'])
            common_words_all_wo_stop.append(ind_wo_stop['comm_words']),
            precision_uniq_wo_stop.append(ind_wo_stop['precision_unique'])
            recall_uniq_wo_stop.append(ind_wo_stop['recall_unique'])
            common_words_uniq_wo_stop.append(ind_wo_stop['comm_words_unique']),
            precision_remove_wo_stop.append(ind_wo_stop['precision_remove'])
            recall_remove_wo_stop.append(ind_wo_stop['recall_remove'])
            common_words_remove_wo_stop.append(ind_wo_stop['comm_words_remove']),

            # calculate wer error
            try:
                wer_result_a = sa.wer(actual, transcript)
                wer.append(float(wer_result_a['wer'].replace("%","")))
                wer_result.append(wer_result_a['diff'])
            except:
                wer.append(100) #Assumed that bad wer is 100
                wer_result.append("")

            temp = string.replace(file, 'input', '')
            temp = string.replace(temp, '.csv', '')
            temp = string.replace(temp, '_', '')
            types.append(temp)

        import collections
        results = pd.DataFrame({
            'name': names,
            'type': types,
            'transcriptsIN': transcripts,
            'Actual': actuals,
            'wer_dump': wer_result,
            'wer': wer,

            'precision_all': precision_all,
            'recall_all':recall_all,
            'common_words_all': common_words_all,
            'precision_uniq': precision_uniq,
            'recall_uniq': recall_uniq,
            'common_words_uniq': common_words_uniq,
            'precision_remove': precision_remove,
            'recall_remove': recall_remove,
            'common_words_remove': common_words_remove,

            'precision_all_wo_stop': precision_all_wo_stop,
            'recall_all_wo_stop':recall_all_wo_stop,
            'common_words_all_wo_stop': common_words_all_wo_stop,
            'precision_uniq_wo_stop': precision_uniq_wo_stop,
            'recall_uniq_wo_stop':recall_uniq_wo_stop,
            'common_words_uniq_wo_stop': common_words_uniq_wo_stop,
            'precision_remove_wo_stop': precision_remove_wo_stop,
            'recall_remove_wo_stop': recall_remove_wo_stop,
            'common_words_remove_wo_stop': common_words_remove_wo_stop,

        }, columns = ['name','type','transcriptsIN','Actual','wer','precision_all','recall_all','common_words_all','precision_uniq','recall_uniq', 'common_words_uniq', 'precision_remove', 'recall_remove','common_words_remove','precision_all_wo_stop','recall_all_wo_stop','common_words_all_wo_stop','precision_uniq_wo_stop','recall_uniq_wo_stop','common_words_uniq_wo_stop','precision_remove_wo_stop','recall_remove_wo_stop','common_words_remove_wo_stop'])

    #
    print len(results)
    results = results[results['wer'] >=0 ]
    print len(results)

    # Dump average stats
    avgs = results.groupby(['type']).mean()
    counts = results.groupby(['type']).count()
    counts = counts[['name']]
    counts.rename(columns={'name': 'Counts'}, inplace=True)
    avgs = pd.concat([avgs, counts], axis=1, join='inner')
    medians = results.groupby(['type']).median()
    medians = pd.concat([medians, counts], axis=1, join='inner')
    maxs = results.groupby(['type']).max()
    maxs = pd.concat([maxs, counts], axis=1, join='inner')
    mins = results.groupby(['type']).min()
    mins = pd.concat([mins, counts], axis=1, join='inner')

    results.to_csv('speechStatsNew.csv')
    avgs.to_csv('speechStatsNewAvg.csv')
    medians.to_csv('speechStatsNewMedian.csv')
    maxs.to_csv('speechStatsNewMax.csv')
    mins.to_csv('speechStatsNewMin.csv')
