import pandas as pd
import random

def get_ind(df):
    list = [i for i,x in enumerate(df) if x]
    return list

data = pd.DataFrame.from_csv('data/free-speech-stratification.csv')
data['is_test'] = 0
freq_table = data['Sid'].value_counts()
freq_table_test = freq_table * 0.25

for index, row in freq_table_test.iteritems():
    print index, row
    inds = get_ind(data['Sid'] == index)
    rand_inds = random.sample(inds, int(row))
    data['is_test'].iloc[rand_inds] = 1

data.to_csv('results/free-speech-stratification-result.csv')

