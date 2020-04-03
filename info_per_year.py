import os
import json
from collections import Counter

my_dirpath = '//files.geo.uzh.ch/private/ochesnok/home/Documents/2_projects/12_hansard/results_api/'

def extract_info(name_input, selected_year):
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
                count_nospeaker = count_nospeaker + 1

        print 'all_speakers', len(set(all_speakers))
        print sorted(Counter(all_speakers).items(), key=lambda pair: pair[1], reverse = True)
        print sorted(Counter(attribute_arr_year).items(), key=lambda pair: pair[1], reverse=True)

        result = sorted(Counter(attribute_arr).items(), key=lambda pair: pair[0])
        print result

        print attribute_arr_title
    return
