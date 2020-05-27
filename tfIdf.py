from __future__ import division
import string
import os
import fnmatch
import codecs
from gensim import corpora, models

stop_words = ['may', 'would', 'could', 'also', 'must', 'ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than']

my_dirpath = ''

documents = []
for dirpath, dirs, files in os.walk(my_dirpath):
    for filename in fnmatch.filter(files, '*.txt'):
        with codecs.open(os.path.join(dirpath, filename)) as text_file:
            lines = text_file.readlines()
            lines = str(lines).replace("[", '')
            lines = str(lines).replace("]", '')
            lines = str(lines).replace(",", '')
            lines = str(lines).replace(".", '')
            lines = str(lines).replace(":", '')
            lines = str(lines).replace("?", '')
            lines = str(lines).replace("!", '')
            lines = str(lines).replace("'", '')
            lines = str(lines).replace(";", '')
            lines = str(lines).replace(">", '')
            lines = str(lines).replace("<", '')
        documents.append((filename, str(lines)))

texts = [
    [word.lower() for word in document[1].split() if word.lower() not in stop_words and word not in string.punctuation and '/' not in word]
    for document in documents]


dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]

n_terms = 10

for i in range(0, len(documents)):
    top_terms = []
    for obj in sorted(tfidf[corpus[i]], key=lambda x: x[1], reverse=True)[:n_terms]:
        top_terms.append("{0:s} ({1:01.03f})".format(dictionary[obj[0]], obj[1]))
    print i, documents[i][0], top_terms
