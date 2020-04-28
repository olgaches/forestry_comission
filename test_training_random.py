import os
import pandas as pd
import random

my_dirpath = '//files.geo.uzh.ch/private/ochesnok/home/Documents/2_projects/12_hansard/results_api/'
filename_input = 'test_train.csv'

output_file_test = os.path.join(my_dirpath, 'test.csv')
output_descriptions_test = open(output_file_test, 'w')
output_descriptions_test.writelines('filename;;unigrams;;class\n')

output_file_training = os.path.join(my_dirpath, 'training.csv')
output_descriptions_training = open(output_file_training, 'w')
output_descriptions_training.writelines('filename;;unigrams;;class\n')

input_text = pd.read_csv(os.path.join(my_dirpath, filename_input), delimiter=';;', encoding='latin1')
length = input_text.shape[0]
all_files = []
for i in range(0, length):
    filename = input_text["filename"][i]
    all_files.append(filename)

selected_random = random.sample(all_files, length/2)

for i in range(0, length):
    filename = input_text["filename"][i]
    unigrams = input_text["unigrams"][i]
    time_class = input_text["class"][i]
    if filename in selected_random:
        output_descriptions_test.writelines(str(filename) + ';;' + str(unigrams) + ';;' + str(time_class) + '\n')
    else:
        output_descriptions_training.writelines(str(filename) + ';;' + str(unigrams) + ';;' + str(time_class) + '\n')