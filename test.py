from nltk import word_tokenize
import math
from string import punctuation

my_text = ['In publishing and graphic design, ipsum is a placeholder text commonly ' \
          'used to demonstrate the visual form of a document or a typeface without relying ' \
          'on meaningful content. Lorem ipsum may be used before final copy is available,' \
          'but it may also be used to temporarily replace copy in a process called greeking, ' \
          'which allows designers to consider form without the meaning of the text influencing the design',
           'Versions of the Lorem ipsum text have been used in typesetting at least since the 1960s, when '
           'it was popularized by advertisements for Letraset transfer sheets. Lorem ipsum was introduced '
           'to the digital world in the mid-1980s Lorem']

def calculate_cooccurrence(text, window_size, word):
    dico = {}
    for line in text:
        if word in line:
            tokens = [token for token in word_tokenize(line.lower()) if token not in punctuation]
            print len(tokens)
            for pos, token in enumerate(tokens):
                if token == word:
                    start = max(0, pos - window_size)
                    end = min(len(tokens), pos + window_size + 1)
                    for pos2 in xrange(start, end):
                        new_key = str(token) + ' ' + str(tokens[pos2])
                        opposite_key = str(tokens[pos2]) + ' ' + str(token)

                        if not new_key in dico.keys() and not opposite_key in dico.keys():
                            dico[new_key] = 1
                        elif new_key in dico.keys() and not opposite_key in dico.keys():
                            dico[new_key] = dico[new_key] + 1
                        elif opposite_key in dico.keys() and not new_key in dico.keys():
                            dico[opposite_key] = dico[opposite_key] + 1
    return dico

result = calculate_cooccurrence(my_text, 5, 'ipsum')
for elem in sorted(result.items(),   key=lambda x: x[1], reverse=True):
    print elem[0] , " ::" , elem[1]

def calculate_mi(dictionary,text):
    for key,value in dictionary.iteritems():
        corpus_size = 0
        search_words = key.split(' ')
        co_occurence = value
        count_word = 0
        count_word2 = 0
        for line in text:
            tokens = [token for token in word_tokenize(line.lower()) if token not in punctuation]
            corpus_size = corpus_size + len(tokens)
            if search_words[1] in tokens:
                count_word = count_word + tokens.count(search_words[1])
            if search_words[0] in tokens:
                count_word2 = count_word2 + tokens.count(search_words[0])
        if co_occurence > 1:
            expected = count_word2  * count_word/float(corpus_size)
            print co_occurence, co_occurence/expected
            print key, math.log(co_occurence/expected, 2)



result_pmi = calculate_mi(result, my_text)