import pandas as pd

corpus_list = [
    'librispeech-lexicon',
    'naziba',
    'cantab',
]

for corpus in corpus_list:
    lexicon = 'data/lexicon/' + corpus + '.txt'
    phones_dict = {}
    with open(lexicon) as f:
        content = f.read()
        content_lines = content.splitlines()
        for line in content_lines:
            words_temp = line.split()

            word = words_temp[0]
            del words_temp[0]
            phones_list = words_temp
            phones_dict[word] = phones_list


    # Find frequency of phones
    unique_phones = set()
    unique_words = set()
    for word, phone_list in phones_dict.iteritems():
        #print word
        unique_words.add(word)
        unique_phones.update(phone_list)

    phone_words = []
    phone_counts = []
    for phone in unique_phones:
        word_list = []
        phone_count = 0
        for word, phone_list in phones_dict.iteritems():
            phone_count = phone_count + phone_list.count(phone)
            if phone in phone_list:
                #This word has this phone
                word_list.append(word)
        phone_words.append(word_list)
        phone_counts.append(phone_count)

    #print phone_counts
    #print len(phone_counts)

    # Write resuts
    result_folder = 'results/lexicon/'
    PhonesMap = pd.DataFrame([' '.join(i) for i in phones_dict.values()], index = phones_dict.keys())
    PhonesMap.to_csv(result_folder + corpus + '_word-phones.csv')

    PhonesWordMap = pd.DataFrame(data = {
        'words': [' '.join(i) for i in phone_words],
        'count_words': [len(i) for i in phone_words],
        'counts': phone_counts
    }, index = unique_phones)
    PhonesWordMap.to_csv(result_folder + corpus + '_phone-words.csv')
