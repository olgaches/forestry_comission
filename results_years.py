import pandas as pd
import os
from collections import Counter

my_dirpath = '//files.geo.uzh.ch/private/ochesnok/home/Documents/2_projects/12_hansard/results_api/'
filename_input = 'result_ML_2classes_unigrams.csv'

input_text = pd.read_csv(os.path.join(my_dirpath, filename_input), delimiter=',', encoding='latin1')
length = input_text.shape[0]
all_files = []
for i in range(0, length):
    filename = input_text["filename"][i]
    result = input_text["result"][i]
    test = input_text["test"][i]
    if result != test:
        print filename
        all_files.append(filename[0:4])

print Counter(all_files)
