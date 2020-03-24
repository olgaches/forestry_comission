import os
import json
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
import nltk
from nltk import word_tokenize,sent_tokenize
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
from string import punctuation
from string import digits
from nltk.corpus import stopwords
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

my_dirpath = '//files.geo.uzh.ch/private/ochesnok/home/Documents/2_projects/12_hansard/results_api/'

def extract_info(name_input):
    with open(os.path.join(my_dirpath, name_input), 'r') as hansard:
        lines = json.load(hansard)
        count_nospeaker = 0
        count_words = []
        count_words_no_punct = []
        count_sentences = []
        doc_pos_adj = []
        doc_pos_noun = []
        doc_all = []
        doc_all_stop_words = []
        for line in lines:
            try:
                speaker = line['speaker']
                debate = line['body']
                debate = debate.replace('<p>','')
                debate = debate.replace('</p>', '')
                debate = debate.replace('<br>', '')
                doc = word_tokenize(str(debate.lower()))
                doc2 = [word for word in doc if word not in punctuation and '/' not in word and '.' not in word]
                doc2_stopwords = [word for word in doc if word not in punctuation and '/' not in word and word not in stop_words  and '.' not in word]
                doc_all.append(doc2)
                doc_all_stop_words.append(doc2_stopwords)
                count_words.append(len(doc))
                count_words_no_punct.append(len(doc2))

                doc_sentence = sent_tokenize(str(debate))
                count_sentences.append(len(doc_sentence))

                for sentence in doc_sentence:
                    sentence = sentence.lower()
                    sentence = sentence.replace('.','')
                    doc = word_tokenize(str(sentence))
                    doc_pos = nltk.pos_tag(doc)
                    for pair in doc_pos:
                        if 'JJ' in str(pair[1]):
                            if '.' not in str(pair[0]) and '/' not in str(pair[0]) and len(str(pair[0])) > 2:
                                doc_pos_adj.append(pair[0])
                        elif 'NN' in str(pair[1]):
                            if '.' not in str(pair[0]) and '/' not in str(pair[0]) and len(str(pair[0])) > 2:
                                doc_pos_noun.append(pair[0])

            except:
                count_nospeaker = count_nospeaker + 1
    #print sorted(Counter(doc_pos_adj).items(), key=lambda pair: pair[1], reverse=True)
    #print sorted(Counter(doc_pos_noun).items(), key=lambda pair: pair[1], reverse=True)
    flat_list_all = [item for sublist in doc_all for item in sublist]
    flat_list_all_stopwords = [item for sublist in doc_all_stop_words for item in sublist]
    print sorted(Counter(flat_list_all).items(), key=lambda pair: pair[1], reverse=True)
    #print sorted(Counter(flat_list_all_stopwords).items(), key=lambda pair: pair[1], reverse=True)
    #return sum(count_words), np.mean(count_words), np.median(count_words), sum(count_words_no_punct), np.mean(count_words_no_punct), np.median(count_words_no_punct), sum(count_sentences), np.mean(count_sentences), np.median(count_sentences)
    return len(set(doc_pos_adj)), len(set(doc_pos_noun))

result = extract_info('commons_to_check_forestry_commission.json')
print result
