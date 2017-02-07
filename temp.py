import os
import pandas as pd

folder = '.'
os.chdir(folder)
fp1 = open('data/words_rslr_train.txt', 'r')
words_94 = fp1.readlines()
words_94 = map (str.strip, words_94)

#fp2 = open('data/sentences_rslr.txt', 'r')
#sentences_rslr = fp2.readlines()
result_folder = 'results/rslr-new/'
os.chdir(result_folder)

df_results = pd.DataFrame.from_csv('speechStatsNew.csv')
sentences_rslr = df_results['Actual'].tolist()

sentences_rslr = map (str.strip, sentences_rslr)

percents = []
counts_sw = []
total_counts = []
for sentence in sentences_rslr:
    words = sentence.split()
    count_words = len(words)
    total_counts.append(count_words)


    count_sw = 0
    for word in words:
        if word in words_94:
            count_sw = count_sw + 1
    counts_sw.append(count_sw)
    percent = float(count_sw) / float(count_words)
    percents.append(percent)

df_results['Percent_overlap'] = percents
df_results.to_csv('speechStatsNew_overlap.csv')

#df = pd.DataFrame(data = {
#    'trans' : sentences_rslr,
#    'percents' : percents,
#    'counts_sw': counts_sw,
#    'total_counts': total_counts
#})


#df.to_csv('results/similar_words.csv')
#print words_94

