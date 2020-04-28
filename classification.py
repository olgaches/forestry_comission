from __future__ import division
import codecs
import time
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, confusion_matrix


class FeatureGen:
    """Feature extraction, features can be turned off and on.
    for example, feat = FeatureGen(perception_verbs = False)
    creates feature set without the turned off feature"""

    def __init__(self, unigrams=True):
        self.unigrams = unigrams  # most common unigrams
        self.vectorizer = CountVectorizer(analyzer="word", max_features=250)

    def find_common_unigrams(self, input):
        length = input.shape[0]

        doc_unigr = []
        for i in range(0, length):
            tokens_input = input["unigrams"][i]
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

        matrix_file_path = '//files.geo.uzh.ch/private/ochesnok/home/Documents/2_projects/12_hansard/results_api/matrix_labels.csv'
        matrix_file = codecs.open(matrix_file_path, 'w', 'utf-8')
        self.common_unigrams = vocab_unigrams
        count = 0
        for i in self.common_unigrams:
            count = count + 1
            if count < len(self.common_unigrams):
                matrix_file.writelines(i + ';')
            else:
                matrix_file.writelines(i)

    def get_features(self, input):
        """This function creates a vector for every grid cell."""

        tokens = input["unigrams"]


        if self.unigrams:
            freq_unigrams = [[1 if word in comment else 0 for word in self.common_unigrams] for comment in tokens]
            freq_unigrams = np.array(freq_unigrams)
            # freq_unigrams_sub = [[1 if word in comment else 0 for word in self.common_unigrams] for comment in tokens]
            # freq_unigrams_sub = np.array(freq_unigrams_sub)
            # freq_unigrams = []
            # for elem_unigr in freq_unigrams_sub:
            # result_unigr = sum(elem_unigr)
            # freq_unigrams.append(result_unigr)

        # return np.column_stack([freq_unigrams,freq_bigrams,verbs_percep,birds_percep,mammals_percep,transport_percep,highway_array,length_desc,year_array,aiello_features_percep])
        return np.column_stack(
            [freq_unigrams])


start_time = time.clock()

## training and test data
training_data = '//files.geo.uzh.ch/private/ochesnok/home/Documents/2_projects/12_hansard/results_api/training.csv'
test_data = '//files.geo.uzh.ch/private/ochesnok/home/Documents/2_projects/12_hansard/results_api/test.csv'
output_data = '//files.geo.uzh.ch/private/ochesnok/home/Documents/2_projects/12_hansard/results_api/result_ML.csv'

## reading training data
train = pd.read_csv(training_data, header=0, \
                    delimiter=";;", quoting=3)

## reading test data
test = pd.read_csv(test_data, header=0, delimiter=";;", \
                   quoting=3)

feat = FeatureGen(unigrams=True)

feat.find_common_unigrams(train)

##feature extraction train
train_data_features = feat.get_features(train)
print train_data_features.shape

##feature extraction test
test_data_features = feat.get_features(test)
print test_data_features.shape

## Initialize a Random Forest classifier with 100 trees
forest = RandomForestClassifier(n_estimators=200)

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

CM = confusion_matrix(y_test, y_pred)
TP = CM[1][1]
print CM
print TP

precision = precision_score(list(y_test), list(y_pred), average=None)
print 'precision', precision

recall = recall_score(list(y_test), list(y_pred), average=None)
print 'recall', recall

f1 = f1_score(list(y_test), list(y_pred), average='micro')
print 'f1', f1

print 'time in seconds', time.clock() - start_time

input_file = '//files.geo.uzh.ch/private/ochesnok/home/Documents/2_projects/12_hansard/results_api/matrix_labels.csv'
my_input = pd.read_csv(input_file, sep=';')

doc_unigrams = []
for i in my_input:
        doc_unigrams.append(i)

print len(doc_unigrams)
print len(forest.feature_importances_)

importances = pd.DataFrame({'feature': doc_unigrams, 'importance': np.round(forest.feature_importances_, 3)})
importances = importances.sort_values('importance', ascending=False).set_index('feature')
print importances