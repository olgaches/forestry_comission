from __future__ import division
import codecs
import time
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
import nltk
from nltk.util import ngrams
from nltk import word_tokenize


class FeatureGen:
    """Feature extraction, features can be turned off and on.
    for example, feat = FeatureGen(perception_verbs = False)
    creates feature set without the turned off feature"""

    def __init__(self, unigrams=True, bigrams=True, length_description=True):
        self.unigrams = unigrams  # most common unigrams
        self.bigrams = bigrams  # most common bigrams
        self.length_description = length_description
        self.vectorizer = CountVectorizer(analyzer="word", max_features=300)
        self.vectorizer2 = CountVectorizer(analyzer="word", max_features=150)

    def find_common_unigrams(self, input):
        length = input.shape[0]

        doc_unigr = []
        for i in range(0, length):
            tokens_input = input["unigrams"][i]
            if len(tokens_input) > 20:
                tokens_input = tokens_input.split(', ')
                for ii in tokens_input:
                    doc_unigr.append(ii)

        tokens_unigrams = []
        for i in doc_unigr:
            i = i.replace("'", '')
            tokens_unigrams.append(i)

        self.common_unigrams_matrix = self.vectorizer.fit_transform(tokens_unigrams)
        # self.common_unigrams_matrix.toarray()

        vocab_unigrams = self.vectorizer.get_feature_names()
        # dist = np.sum(train_data_features, axis=0)
        # for tag, count in zip(vocab_unigrams, dist):
        # print count, tag
        self.common_unigrams = vocab_unigrams

        matrix_file_path = ''
        matrix_file = codecs.open(matrix_file_path, 'w', 'utf-8')
        self.common_unigrams = vocab_unigrams
        count = 0
        for i in self.common_unigrams:
            count = count + 1
            if count < len(self.common_unigrams):
                matrix_file.writelines(i + ';')
            else:
                matrix_file.writelines(i)

    def find_common_bigrams(self, input):
        length = input.shape[0]

        doc = []
        for i in range(0, length):
            tokens_input = input["unigrams"][i]
            tokens_input = str(tokens_input)
            tokens_input = tokens_input.replace('"', '')
            tokens_input = tokens_input.replace("'", '')
            tokens_input = tokens_input.replace(",", '')
            token = nltk.word_tokenize(tokens_input)
            # print token
            for i in range(len(token) - 1):
                bigram = [token[i]], [token[i + 1]]
                bigram = str(bigram).replace('[', '')
                bigram = str(bigram).replace(']', '')
                bigram = str(bigram).replace(',', '')
                bigram = str(bigram).replace("'", '')
                # print bigram
                doc.append(bigram)

        self.common_bigram_matrix = self.vectorizer2.fit_transform(doc)
        # self.common_bigram_matrix.toarray()

        vocab_bigrams = self.vectorizer2.get_feature_names()
        self.common_bigrams = vocab_bigrams

    def get_features(self, input):
        """This function creates a vector for every grid cell."""

        tokens = input["unigrams"]

        if self.unigrams:
            freq_unigrams = [[1 if word in comment else 0 for word in self.common_unigrams] for comment in tokens]
            freq_unigrams = np.array(freq_unigrams)

        if self.bigrams:
            freq_bigrams = [[1 if word in comment else 0 for word in self.common_bigrams] for comment in tokens]
            freq_bigrams = np.array(freq_bigrams)

        if self.length_description:
            length = input.shape[0]
            length_desc = []
            for i in range(0, length):
                unigrams = input["unigrams"][i]
                unigrams = unigrams.split(', ')
                length_desc.append(len(unigrams))

            length_desc = np.array(length_desc)

        # return np.column_stack([freq_unigrams,freq_bigrams,length_desc])
        return np.column_stack(
            [freq_unigrams])


start_time = time.clock()

## training and test data
training_data = ''
test_data = ''
output_data = ''

## reading training data
train = pd.read_csv(training_data, header=0, \
                    delimiter=";;", quoting=3)

## reading test data
test = pd.read_csv(test_data, header=0, delimiter=";;", \
                   quoting=3)

feat = FeatureGen(unigrams=True, bigrams=False, length_description=True)

feat.find_common_unigrams(train)
feat.find_common_bigrams(train)

##feature extraction train
train_data_features = feat.get_features(train)
print train_data_features.shape

##feature extraction test
test_data_features = feat.get_features(test)
print test_data_features.shape

## Initialize a Random Forest classifier with 100 trees
forest = RandomForestRegressor(n_estimators=200)

train_label = train['class']
## Fit the forest to the training set
forest_fit = forest.fit(train_data_features, train_label)

## Use the random forest to make average (or mode?) label predictions
result = forest.predict(test_data_features)

## Output results with an "grid_id" column and a "average" (or mode) column
output = pd.DataFrame(data={"filename": test["filename"], "test": test['class'], "result": result})

## Use pandas to write the comma-separated output file
output.to_csv(output_data, index=False, quoting=3)

y_test = test['class']
y_pred = result

r2 = metrics.r2_score(y_test, y_pred)
print 'r2', r2

mse_score = metrics.mean_squared_error(y_test, y_pred)
print 'mse score', mse_score

print 'time in seconds', time.clock() - start_time

input_file = ''
my_input = pd.read_csv(input_file, sep=';')

doc_unigrams = []
for i in my_input:
    doc_unigrams.append(i)

print len(doc_unigrams)
print len(forest.feature_importances_)

importances = pd.DataFrame({'feature': doc_unigrams, 'importance': np.round(forest.feature_importances_, 3)})
importances = importances.sort_values('importance', ascending=False).set_index('feature')
print importances
