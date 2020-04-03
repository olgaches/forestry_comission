import os
import json
import codecs
import re


my_dirpath = '//files.geo.uzh.ch/private/ochesnok/home/Documents/2_projects/12_hansard/results_api/'

def create_separated_documents(filename):
    with open(os.path.join(my_dirpath, filename), 'r') as hansard:
        lines = json.load(hansard)
        pattern = '<.*?>'
        count = 0
        for line in lines:
            count = count + 1
            if count % 10 == 0:
                print count
            try:
                speaker = line['speaker']
                gid = line['gid']
                debate = line['body']
                if 'landscape' in debate.lower():
                    debate = debate.replace('<p>','')
                    debate = debate.replace('</p>', '')
                    debate = debate.replace('<br>', '')
                    debate = debate.replace('<br/>', '')
                    debate_updated = re.sub(pattern, '', debate)
                    output_file = os.path.join(my_dirpath, 'separated_documents_landscape/', str(gid) + '.txt')
                    output_descriptions = codecs.open(output_file, 'w', 'utf-8')
                    output_descriptions.writelines(debate_updated)
            except:
                print count

result = create_separated_documents('commons_to_check_forestry_commission.json')