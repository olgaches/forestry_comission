import os
import json
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

my_dirpath = '//files.geo.uzh.ch/private/ochesnok/home/Documents/2_projects/12_hansard/results_api/'

def extract_info(name_input, name_ouptut, selected_year):
    with open(os.path.join(my_dirpath, name_input), 'r') as hansard:
        lines = json.load(hansard)
        count_nospeaker = 0
        attribute_arr = []
        attribute_arr_year = []
        attribute_arr_title = []
        all_speakers = []
        for line in lines:
            try:
                speaker = line['speaker']
                attribute = 'hdate'
                year = line[attribute][0:4]
                if year == selected_year:
                    attribute_arr_year.append(line[attribute])
                    speaker_info = line['speaker']
                    attribute_arr.append(speaker_info['party'])
                    all_speakers.append(speaker_info['name'])
                    title_info = line['parent']
                    attribute_arr_title.append(title_info['body'])

                    count_speaker = count_speaker + 1
            except:
                #print line
                count_nospeaker = count_nospeaker + 1

        print 'all_speakers', len(set(all_speakers))
        print sorted(Counter(all_speakers).items(), key=lambda pair: pair[1], reverse = True)
        print sorted(Counter(attribute_arr_year).items(), key=lambda pair: pair[1], reverse=True)

        result = sorted(Counter(attribute_arr).items(), key=lambda pair: pair[0])
        print result

        print attribute_arr_title

        # x_labels_arr = []
        # count_arr = []
        # for i in result:
        #     x_labels_arr.append(i[0])
        #     count_arr.append(i[1])
        #
        # opacity = 0.8
        # n_groups = len(count_arr)
        # index = np.arange(n_groups)
        #
        # # plt.ylim(0, 50)
        # # plt.xlim(-1, 102)
        # plt.bar(index, count_arr, alpha=opacity, color='#4F97A3', align='center')
        #
        # plt.xticks(index, x_labels_arr, fontsize=12, rotation=90)
        # plt.ylabel('Number of debates', fontsize=12)
        # #plt.show()
        # plt.savefig(os.path.join(my_dirpath, name_ouptut), bbox_inches="tight")


extract_info('commons_to_check_forestry_commission.json','results_1965.png', '1965')
