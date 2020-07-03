import json
import math
import os
import numpy as np
import pandas as pd
import regex
from nltk.stem import WordNetLemmatizer

# document preprocessing
# nltk.download('wordnet')

# file reading
tokens_document = []  # contains all tokens of all documents
fileOpen = open("Stopword-List.txt", 'r')
outputFile = fileOpen.read()
# stopword list
stopWord = outputFile.split()

class_list = ['athletics', 'cricket', 'football', 'rugby', 'tennis']
lemmatizer = WordNetLemmatizer()

training_data_lst = []
tokens_classes = {i: [] for i in class_list}
classes_quan = {i: 0 for i in class_list}

for class_name in class_list:
    root_path = '../bbcsport/' + class_name

    for i in os.listdir(root_path):
        if os.path.isfile(os.path.join(root_path, i)):
            fileOpen = open('../bbcsport/' + class_name + '/' + i, 'r')
            outputFile = ''
            for line in fileOpen:
                outputFile = outputFile + line

            outputFile = outputFile.replace('\n', ' ')

            outputFile = regex.sub("'", "", outputFile)
            outputFile = regex.split('\W+', outputFile)

            training_data_lst.append({'doc': outputFile, 'class': class_name})
            classes_quan[training_data_lst[len(training_data_lst) - 1]['class']] = classes_quan[training_data_lst[
                len(training_data_lst) - 1]['class']] + 1

            for j in range(0, len(training_data_lst[len(training_data_lst) - 1]['doc'])):
                training_data_lst[len(training_data_lst) - 1]['doc'][j] = lemmatizer.lemmatize(
                    training_data_lst[len(training_data_lst) - 1]['doc'][j].lower())
                if (not (training_data_lst[len(training_data_lst) - 1]['doc'][j] in stopWord)) and (
                        not (training_data_lst[len(training_data_lst) - 1]['doc'][j] in tokens_document)) and (
                        len(training_data_lst[len(training_data_lst) - 1]['doc'][
                                j]) > 1):  # removes words which doesn't exist in stopword and distinct token list
                    tokens_document.append(training_data_lst[len(training_data_lst) - 1]['doc'][j])

            doc = list(set(training_data_lst[len(training_data_lst) - 1]['doc']))
            tokens_classes[training_data_lst[len(training_data_lst) - 1]['class']] = tokens_classes[
                                                                                         training_data_lst[len(
                                                                                             training_data_lst) - 1][
                                                                                             'class']] + doc

            fileOpen.close()

dataframe_idx = []
dataframe_col = []

for i in class_list:
    dataframe_col.append(i)
    dataframe_col.append('not ' + i)

for i in tokens_document:
    dataframe_idx.append(i)
    dataframe_idx.append('not ' + i)

matrix_config = pd.DataFrame(columns=dataframe_col, index=dataframe_idx)


def Sort_list(lst):
    lst.sort(reverse=True, key=lambda x: x[0])
    return lst


def feature_selection():
    for term_in_doc in tokens_document:
        count_class_term = np.zeros(len(class_list))

        for class_name in range(len(class_list)):
            count_class_term[class_name] = tokens_classes[class_list[class_name]].count(term_in_doc)

        for class_name in range(len(class_list)):
            matrix_config.loc[term_in_doc][class_list[class_name]] = count_class_term[class_name]
            matrix_config.loc['not ' + term_in_doc][class_list[class_name]] = classes_quan[class_list[class_name]] - \
                                                                              count_class_term[class_name]
            matrix_config.loc[term_in_doc]['not ' + class_list[class_name]] = np.sum(count_class_term) - \
                                                                              count_class_term[class_name]
            matrix_config.loc['not ' + term_in_doc]['not ' + class_list[class_name]] = len(training_data_lst) - np.sum(
                count_class_term) - \
                                                                                       matrix_config.loc[term_in_doc][
                                                                                           'not ' + class_list[
                                                                                               class_name]]

    classes_relvant_features = {i: [] for i in class_list}

    for class_name in class_list:
        for term_in_doc in tokens_document:
            T1 = (matrix_config.loc['not ' + term_in_doc][class_name] + matrix_config.loc[term_in_doc][class_name] +
                  matrix_config.loc[term_in_doc]['not ' + class_name] +
                  matrix_config.loc['not ' + term_in_doc]['not ' + class_name])
            T2 = (matrix_config.loc[term_in_doc][class_name] * matrix_config.loc['not ' + term_in_doc][
                'not ' + class_name]) - (
                         matrix_config.loc['not ' + term_in_doc][class_name] * matrix_config.loc[term_in_doc][
                     'not ' + class_name])

            T3 = matrix_config.loc['not ' + term_in_doc][class_name] + matrix_config.loc[term_in_doc][class_name]
            T4 = matrix_config.loc[term_in_doc][class_name] + matrix_config.loc[term_in_doc]['not ' + class_name]

            T5 = matrix_config.loc['not ' + term_in_doc]['not ' + class_name] + matrix_config.loc['not ' + term_in_doc][
                class_name]
            T6 = matrix_config.loc['not ' + term_in_doc]['not ' + class_name] + matrix_config.loc[term_in_doc][
                'not ' + class_name]

            if T3 == 0:
                T3 = 1
            elif T4 == 0:
                T4 = 1
            elif T5 == 0:
                T5 = 1
            elif T6 == 0:
                T6 = 1

            chi_square = (T1 * (T2 * T2)) / (T3 * T4 * T5 * T6)

            classes_relvant_features[class_name].append((chi_square, term_in_doc))

    for key, lst in classes_relvant_features.items():
        classes_relvant_features[key] = Sort_list(lst)

    return classes_relvant_features


feat_sel = feature_selection()

tokens_document = []
termss = 0
for key, lst in feat_sel.items():
    if termss == 0:
        tokens_document = [tokn[1] for tokn in lst][0:int(len(lst) * (1/2))]
        termss = 1
    else:
        tokens_document = tokens_document + [tokn[1] for tokn in lst][0:int(len(lst) * (1/2))]

tokens_document = list(set(tokens_document))

with open('Tokens.txt', 'w') as json_file:
    json.dump(tokens_document, json_file)

# -----------------------------------------------------------------------------------------


idf_list = []
tf_idf_vectors_list = []
vectors_classes_list = []

# calculates  idfs
for i in range(0, len(tokens_document)):
    idf_list.append(0)
    for j in range(0, len(training_data_lst)):
        if tokens_document[i] in training_data_lst[j]['doc']:
            idf_list[i] += 1

    idf_list[i] = math.log(idf_list[i] / len(training_data_lst), 2)


for i in range(0, len(training_data_lst)):
    tf_idf_vectors_list.append([])
    vectors_classes_list.append(training_data_lst[i]['class'])
    for j in range(0, len(tokens_document)):

        if tokens_document[j] in training_data_lst[i]['doc']:
            tf_idf_vectors_list[i].append((idf_list[j]) * math.log(training_data_lst[i]['doc'].count(tokens_document[j]) + 1,
                                                         2))  # using Tf = log(df/N)
        else:
            tf_idf_vectors_list[i].append(0)

    doc_vector = np.array(tf_idf_vectors_list[i])
    doc_vector = doc_vector * doc_vector
    vector_magnitude = math.sqrt(doc_vector.sum())

    for j in range(0, len(tokens_document)):
        tf_idf_vectors_list[i][j] = tf_idf_vectors_list[i][j] / vector_magnitude

tf_idf_vectors_list = {'vectors': tf_idf_vectors_list, 'class': vectors_classes_list}

# saving unit vectors
with open('tf_idf_vectors_list.txt', 'w') as json_file:
    json.dump(tf_idf_vectors_list, json_file)

with open('idf_list.txt', 'w') as json_file:
    json.dump(idf_list, json_file)
