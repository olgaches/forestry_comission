import numpy as np
import nltk
from nltk import bigrams
import itertools
import pandas as pd
import os
from scipy import sparse
from nltk import word_tokenize,sent_tokenize
import json
from string import punctuation
from string import digits
from nltk.corpus import stopwords
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

my_dirpath = '//files.geo.uzh.ch/private/ochesnok/home/Documents/2_projects/12_hansard/results_api/'


def create_cooccurrence_matrix(filename, window_size):
    vocabulary = {}
    dico = {}
    with open(os.path.join(my_dirpath, filename), 'r') as hansard:
        lines = json.load(hansard)
        count = 0
        for line in lines:
            count = count + 1
            if count % 10 == 0:
                print count
            try:
                speaker = line['speaker']
                debate = line['body']
                debate = debate.replace('<p>','')
                debate = debate.replace('</p>', '')
                debate = debate.replace('<br>', '')
                debate_sentences = sent_tokenize(debate)
                for sentence in debate_sentences:
                    if 'forestry' in sentence.lower() and 'commission' in sentence.lower():
                        #print sentence
                        tokens = [token for token in word_tokenize(sentence.lower()) if token not in punctuation and '/' not in token and len(token) > 2 and token not in stop_words and '.' not in token and '=' not in token]
                        for pos, token in enumerate(tokens):
                            i = vocabulary.setdefault(token, len(vocabulary))
                            start = max(0, pos - window_size)
                            end = min(len(tokens), pos + window_size + 1)
                            for pos2 in xrange(start, end):
                                if pos2 == pos:
                                    continue
                                j = vocabulary.setdefault(tokens[pos2], len(vocabulary))
                                #print token, tokens[pos2], j
                                new_key = str(token) + ' ' + str(tokens[pos2])
                                opposite_key = str(tokens[pos2]) + ' ' + str(token)

                                if not new_key in dico.keys() and not opposite_key in dico.keys():
                                    dico[new_key] = j
                                elif new_key in dico.keys() and not opposite_key in dico.keys():
                                    dico[new_key] = dico[new_key] + j
                                elif opposite_key in dico.keys() and not new_key in dico.keys():
                                    dico[opposite_key] = dico[opposite_key] + j
            except:
                print 'hm'
    #print vocabulary
    return dico

result = create_cooccurrence_matrix('commons_to_check_forestry_commission.json', 10)
for elem in sorted(result.items(),   key=lambda x: x[1], reverse=True):
    print elem[0] , " ::" , elem[1]