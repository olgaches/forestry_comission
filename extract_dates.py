import os
import json
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

my_dirpath = '//files.geo.uzh.ch/private/ochesnok/home/Documents/2_projects/12_hansard/results_api/'

def extract_info(name_input, name_ouptut, attribute):
    with open(os.path.join(my_dirpath, name_input), 'r') as hansard:
        lines = json.load(hansard)
        count_nospeaker = 0
        count_speaker = 0
        attribute_arr = []
        all_speakers = []
        for line in lines:
            if attribute == 'hdate':
                try:
                    speaker = line['speaker']
                    year = line[attribute][0:4]
                    attribute_arr.append(year)
                except:
                    count_nospeaker = count_nospeaker + 1
            elif attribute == 'speaker':
                try:
                    speaker_info = line[attribute]
                    attribute_arr.append(speaker_info['party'])
                    all_speakers.append(speaker_info['name'])
                    count_speaker = count_speaker + 1
                except:
                    #print line
                    count_nospeaker = count_nospeaker + 1

        print count_nospeaker, count_speaker
        print 'all_speakers', len(set(all_speakers))
        print sorted(Counter(all_speakers).items(), key=lambda pair: pair[1], reverse = True)

        result = sorted(Counter(attribute_arr).items(), key=lambda pair: pair[0])
        print result

        all_counts_docs = []
        for i in result:
            all_counts_docs.append(i[1])
        print 'mean', np.mean(all_counts_docs)
        print 'median', np.median(all_counts_docs)

        print all_counts_docs

        x_labels_arr = []
        count_arr = []
        for i in result:
            x_labels_arr.append(i[0])
            count_arr.append(i[1])

        opacity = 0.8
        n_groups = len(count_arr)
        index = np.arange(n_groups)

        # plt.ylim(0, 50)
        # plt.xlim(-1, 102)
        plt.bar(index, count_arr, alpha=opacity, color='#4F97A3', align='center')

        plt.xticks(index, x_labels_arr, fontsize=12, rotation=90)
        plt.ylabel('Number of debates', fontsize=12)
        #plt.show()
        plt.savefig(os.path.join(my_dirpath, name_ouptut), bbox_inches="tight")


to_plot = extract_info('commons_to_check_forestry_commission.json','results_commons_hdate.png','hdate')

#extract_info('commons_to_check_forestry_commission.json','results_commons_speaker.png','speaker')
