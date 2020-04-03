import nltk
from nltk.collocations import *
import os
import json
from string import punctuation
from nltk import word_tokenize
from nltk.corpus import stopwords
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()

my_dirpath = '//files.geo.uzh.ch/private/ochesnok/home/Documents/2_projects/12_hansard/results_api/'
filename = 'commons_to_check_forestry_commission.json'

with open(os.path.join(my_dirpath, filename), 'r') as hansard:
    lines = json.load(hansard)
    count = 0
    for line in lines[0:5]:
        count = count + 1
        if count % 10 == 0:
            print count
        try:
            speaker = line['speaker']
            debate = line['body']
            debate = debate.replace('<p>','')
            debate = debate.replace('</p>', '')
            debate = debate.replace('<br>', '')
            tokens = [token for token in word_tokenize(debate.lower()) if
                      token not in punctuation and '/' not in token and len(
                          token) > 2 and token not in stop_words and '.' not in token and '=' not in token]

            finder = BigramCollocationFinder.from_words(tokens)
            print finder.nbest(bigram_measures.pmi, 10)
        except:
            print 'hm'