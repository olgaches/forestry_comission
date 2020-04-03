from my_functions import calculate_cooccurrence
from my_functions import calculate_mi
from my_functions import extract_info
from collections import Counter
import numpy as np

my_dirpath = '//files.geo.uzh.ch/private/ochesnok/home/Documents/2_projects/12_hansard/results_api/'

descriptive_statistics = extract_info(my_dirpath, 'commons_forestry_commission_speaker.json')
print 'Number of tokens (mean, median):', sum(descriptive_statistics[0]), round(np.mean(descriptive_statistics[0]),0), round(np.median(descriptive_statistics[0]),0)
print 'Number of tokens without punctuation (mean, median):',  sum(descriptive_statistics[1]), round(np.mean(descriptive_statistics[1]),0), round(np.median(descriptive_statistics[1]),0)
print 'Number of sentences (mean, median):',  sum(descriptive_statistics[2]), round(np.mean(descriptive_statistics[2]),0), round(np.median(descriptive_statistics[2]),0)
print 'Number of unique adjectives:', len(set(descriptive_statistics[3]))
print 'Number of unique nouns:', len(set(descriptive_statistics[4]))

print 'sorted adjectives', sorted(Counter(descriptive_statistics[3]).items(), key=lambda pair: pair[1], reverse=True)
print 'sorted nouns', sorted(Counter(descriptive_statistics[4]).items(), key=lambda pair: pair[1], reverse=True)

print 'sorted all words', sorted(Counter(descriptive_statistics[5]).items(), key=lambda pair: pair[1], reverse=True)
print 'sorted all words without stop words', sorted(Counter(descriptive_statistics[6]).items(), key=lambda pair: pair[1], reverse=True)


result = calculate_cooccurrence(my_dirpath, 'commons_forestry_commission_speaker.json', 3, 'landscape')
for elem in sorted(result[0].items(),   key=lambda x: x[1], reverse=True):
    if elem[1] >= 3:
        print elem[0], " ::", elem[1]

result_mi = calculate_mi(my_dirpath, result[0],'commons_forestry_commission_speaker.json', result[1], result[2], 3, result[3])
for elem in sorted(result_mi.items(),   key=lambda x: x[1], reverse=True):
    print elem[0], " ::", round(elem[1], 2)