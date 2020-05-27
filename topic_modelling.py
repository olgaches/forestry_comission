# !/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import division
import pandas as pd
from gensim import corpora, models, similarities
from gensim.models import hdpmodel, ldamodel
from nltk.corpus import stopwords
from nltk import word_tokenize
from itertools import izip
import os
import string


import codecs

stoplist = stopwords.words('english')

my_dirpath = ''
filename_input = 'geograph_forestry_comission_classified.csv'

file_result = os.path.join(my_dirpath, 'results.csv')
list_result = codecs.open(file_result,'w')

file_result_doc = os.path.join(my_dirpath, 'results_documents.csv')
list_result_doc = codecs.open(file_result_doc,'w')

input_text = pd.read_csv(os.path.join(my_dirpath, filename_input), delimiter=';;', encoding='latin1')
length = input_text.shape[0]
documents = []
for i in range(0, length):
    gridimage_id = input_text["gridimage_id"][i]
    description = input_text["description"][i]
    tokens = word_tokenize(description)
    documents.append((gridimage_id, tokens))

additional_list = ["'s", 'http',"\'\'", "``","https"]

texts = [[word.lower() for word in document[1] if word.lower() not in stoplist and word not in string.punctuation and word.lower() not in additional_list]
         for document in documents]

# remove words that appear less or equal than X times
all_tokens = sum(texts, [])
tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) <= 10)
texts = [[word for word in text if word not in tokens_once]
         for text in texts]

dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]
my_num_topics = 20

# the documents and which is the most probable topics for each doc.
lda = ldamodel.LdaModel(corpus, id2word=dictionary, num_topics=my_num_topics, alpha='auto', eval_every=5)
corpus_lda = lda[corpus]

#tf-idf version of it
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
lda = ldamodel.LdaModel(corpus_tfidf, id2word=dictionary, num_topics = my_num_topics, alpha='auto', eval_every=5)
corpus_lda = lda[corpus_tfidf]

# print the most contributing words for selected topics
for top in lda.show_topics(my_num_topics, num_words=20):
    list_result.writelines(str(top) + '\n')

for l, t in izip(corpus_lda, documents):
    selected_topic = max(l, key=lambda item: item[1])
    if selected_topic[1] != 1 / my_num_topics:
        selected_topic_number = selected_topic[0]
        # print t[0]
        # print selected_topic
        list_result_doc.writelines(str(t[0]) + ',' + str(selected_topic[0]) + '\n')