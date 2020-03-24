import json
from twfy_python import TheyWorkForYou
import os
import json

api_key = 'FeaWMyBR7XPMBCzL9sB8Mc6w'

twfy = TheyWorkForYou(api_key)

my_dirpath = '//files.geo.uzh.ch/private/ochesnok/home/Documents/2_projects/12_hansard/results_api/'

output_file = os.path.join(my_dirpath, 'lords_test2.json')
output_descriptions = open(output_file, 'w')

# Type 'Lords' or 'Commons'
length_row = 1
page = 0
count = 0
while length_row > 0:
    page = page + 1
    print page
    debates_list = twfy.api.getDebates(type='lords', search='Forestry Commission', page = page)
    length_row = len(debates_list['rows'])
    print length_row
#person?, order?
    for row in debates_list['rows']:
        try:
            dictionary = {
                "gid": row['gid'],
                "hdate": row['hdate'],
                "listurl": row['listurl'],
                "speaker": row['speaker'],
                "body": row['body'],
                "parent": row['parent']
            }

        except:
            dictionary = {
                "gid": row['gid'],
                "hdate": row['hdate'],
                "listurl": row['listurl'],
                "body": row['body'],
                "parent": row['parent']
            }
        json_object = json.dumps(dictionary, indent = 4)
        output_descriptions.write(json_object)
print count