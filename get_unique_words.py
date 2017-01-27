import pandas as pd
import os

corpus_list = [
    'librispeech-lexicon',
    'naziba',
    'cantab',
]

for corpus in corpus_list:
    lexicon = 'data/corpus/' + corpus + '.txt'
    words = []
    phones = []
    unique_phones = set()
    with open(lexicon) as f:
        content = f.read()
        content_lines = content.splitlines()
        for line in content_lines:
            words_temp = line.split()
            words.append(words_temp[0])
            phones.append(' '.join(words_temp[1:]))
            unique_phones.update(words_temp[1:])

    # Write resuts
    result_folder = 'results/'
    PhonesMap = pd.DataFrame(phones, index = words)
    PhonesMap.to_csv(result_folder + corpus + '.csv')

    with open(result_folder + corpus + '_unique_phones.csv', 'w') as f:
        f.write('\n'.join(unique_phones))  # python will convert \n to os.linesep