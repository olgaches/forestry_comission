import string
import os
import fnmatch
import codecs
from nltk import word_tokenize

stop_words = ['may', 'would', 'could', 'also', 'must', 'ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than']

my_dirpath = '//files.geo.uzh.ch/private/ochesnok/home/Documents/2_projects/12_hansard/results_api/separated_documents/'

output_file = os.path.join(my_dirpath, '//files.geo.uzh.ch/private/ochesnok/home/Documents/2_projects/12_hansard/results_api/test_train.csv')
output_descriptions = open(output_file, 'w')

for dirpath, dirs, files in os.walk(my_dirpath):
    count1 = 0
    count2 = 0
    count3 = 0
    count4 = 0
    count5 = 0
    for filename in fnmatch.filter(files, '*.txt'):
        with codecs.open(os.path.join(dirpath, filename)) as text_file:
            lines = text_file.readlines()
            text = word_tokenize(str(lines))
            words = [word.lower() for word in text if word.lower() not in stop_words and word not in string.punctuation and '/' not in word]
            if int(filename[0:4]) < 1939:
                output_descriptions.writelines(str(filename) + ';;' + str(words) + ';;' + '1' + '\n')
                count1 = count1 + 1
            elif int(filename[0:4]) >= 1939 and int(filename[0:4]) <= 1945:
                output_descriptions.writelines(str(filename) + ';;' + str(words) + ';;' + '2' + '\n')
                count2 = count2 + 1
            elif int(filename[0:4]) > 1945 and int(filename[0:4]) < 1968:
                output_descriptions.writelines(str(filename) + ';;' + str(words) + ';;' + '3' + '\n')
                count3 = count3 + 1
            elif int(filename[0:4]) >= 1968 and int(filename[0:4]) < 2003:
                output_descriptions.writelines(str(filename) + ';;' + str(words) + ';;' + '4' + '\n')
                count4 = count4 + 1
            elif int(filename[0:4]) >= 2003:
                output_descriptions.writelines(str(filename) + ';;' + str(words) + ';;' + '5' + '\n')
                count5 = count5 + 1

print count1, count2, count3, count4, count5