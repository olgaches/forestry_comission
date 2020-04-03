import os
import math
from nltk import word_tokenize
import json
from string import punctuation
stop_words = ['shall', 'may', 'would', 'could', 'also', 'must', 'ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than']


my_dirpath = '//files.geo.uzh.ch/private/ochesnok/home/Documents/2_projects/12_hansard/results_api/'


def calculate_cooccurrence(filename, window_size, word):
    dico = {}
    length_corpus = 0
    with open(os.path.join(my_dirpath, filename), 'r') as hansard:
        lines = json.load(hansard)
        count_word = 0
        for line in lines:
            try:
                debate = line['body']
                debate = debate.replace('<p>', '')
                debate = debate.replace('</p>', '')
                debate = debate.replace('<br/>', '')
                debate = debate.replace('<br>', '')
                tokens = [token for token in word_tokenize(debate.lower()) if token not in punctuation]
                length_corpus = length_corpus + len(tokens)
                if word in tokens:
                    tokens_filt = [token for token in tokens if '/' not in token and len(token) > 2 and token not in stop_words and '.' not in token and '=' not in token]
                    for pos, token in enumerate(tokens_filt):
                        if token == word:
                            count_word = count_word + 1
                            start = max(0, pos - window_size)
                            end = min(len(tokens_filt), pos + window_size + 1)
                            for pos2 in xrange(start, end):
                                new_key = str(token) + ' ' + str(tokens_filt[pos2])
                                opposite_key = str(tokens_filt[pos2]) + ' ' + str(token)

                                if not new_key in dico.keys() and not opposite_key in dico.keys():
                                    dico[new_key] = 1
                                elif new_key in dico.keys() and not opposite_key in dico.keys():
                                    dico[new_key] = dico[new_key] + 1
                                elif opposite_key in dico.keys() and not new_key in dico.keys():
                                    dico[opposite_key] = dico[opposite_key] + 1

            except:
                continue
    return dico, count_word, length_corpus, window_size

result = calculate_cooccurrence('commons_forestry_commission_speaker.json', 3, 'landscape')
# for elem in sorted(result[0].items(),   key=lambda x: x[1], reverse=True):
#     if elem[1] >= 3:
#         print elem[0] , " ::" , elem[1]

def calculate_mi(dictionary, filename, count_WordOfInterest, length_corpus, min_co_occurrence, window_size):
    final_dictionary_mi = {}
    for key,value in dictionary.iteritems():
        search_words = key.split(' ')
        co_occurence = value
        if co_occurence >= min_co_occurrence:
            with open(os.path.join(my_dirpath, filename), 'r') as hansard:
                lines = json.load(hansard)
                count_word = 0
                for line in lines:
                    debate = line['body']
                    tokens = [token for token in word_tokenize(debate.lower())]
                    if search_words[1] in tokens:
                        count_word = count_word + tokens.count(search_words[1])
                expected =  count_WordOfInterest * count_word * (2 * window_size)/float(length_corpus)
                observed = co_occurence
                mi = math.log(observed/expected, 2)
                final_dictionary_mi[key] = mi
    return final_dictionary_mi


result_mi = calculate_mi(result[0],'commons_forestry_commission_speaker.json', result[1], result[2], 3, result[3])
for elem in sorted(result_mi.items(),   key=lambda x: x[1], reverse=True):
    print elem[0] , " ::" , round(elem[1], 2)
