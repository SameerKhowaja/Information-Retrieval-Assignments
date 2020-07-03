import json
import math
import os
import shutil
import numpy as np
import regex
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

# document preprocessing
# nltk.download('wordnet')

# file reading
tokens_document = []

fileOpen = open("Stopword-List.txt", 'r')
outputFile = fileOpen.read()
# stopword list
stopWord = outputFile.split()

classes = ['athletics', 'cricket', 'football', 'rugby', 'tennis']
dataset_dict = {}
porter = PorterStemmer()

if os.path.exists('training_data'):
    shutil.rmtree('training_data')
os.mkdir('training_data')

if os.path.exists('testing'):
    shutil.rmtree('testing')
os.mkdir('testing')

for className in classes:
    root_path = '../bbcsport/' + className
    dataset_dict[className] = []

    for i in os.listdir(root_path):
        if os.path.isfile(os.path.join(root_path, i)):
            dataset_dict[className].append(i)

    if os.path.exists('training_data/' + className):
        shutil.rmtree('training_data/' + className)
    os.mkdir('training_data/' + className)

    if os.path.exists('testing/' + className):
        shutil.rmtree('testing/' + className)
    os.mkdir('testing/' + className)

    for file in dataset_dict[className][int(len(dataset_dict[className]) * 0.3):]:
        shutil.copy('../bbcsport/' + className + '/' + file, 'training_data/' + className)

    for file in dataset_dict[className][0:int(len(dataset_dict[className]) * 0.3)]:
        shutil.copy('../bbcsport/' + className + '/' + file, 'testing/' + className)

training_data = []
lemmatizer = WordNetLemmatizer()

for className in classes:
    root_path = 'training_data/' + className

    for i in os.listdir(root_path):
        if os.path.isfile(os.path.join(root_path, i)):
            fileOpen = open('training_data/' + className + '/' + i, 'r')
            outputFile = ''
            for line in fileOpen:
                outputFile = outputFile + line

            outputFile = outputFile.replace('\n', ' ')
            outputFile = regex.sub("'", "", outputFile)
            outputFile = regex.split('\W+', outputFile)

            training_data.append({'doc': outputFile, 'class': className})
            fileOpen.close()

for i in range(0, len(training_data)):
    for j in range(0, len(training_data[i]['doc'])):
        training_data[i]['doc'][j] = porter.stem(training_data[i]['doc'][j].lower())  # applying lemmatization

        if (not (training_data[i]['doc'][j] in tokens_document)) and (not (training_data[i]['doc'][
                                                                     j] in stopWord)):  # removes words which doesn't exist in stopword and distinct token list
            tokens_document.append(training_data[i]['doc'][j])

print("Total Tokens :: ", len(tokens_document))

idf_list = []
tf_idf_vectors_list = []
vectors_classes_list = []

# calculates  idfs
for i in range(0, len(tokens_document)):
    idf_list.append(0)
    for j in range(0, len(training_data)):
        if tokens_document[i] in training_data[j]['doc']:
            idf_list[i] = idf_list[i] + 1
    idf_list[i] = math.log(idf_list[i] / len(training_data), 2)

for i in range(0, len(training_data)):
    tf_idf_vectors_list.append([])
    vectors_classes_list.append(training_data[i]['class'])
    for j in range(0, len(tokens_document)):
        if tokens_document[j] in training_data[i]['doc']:
            tf_idf_vectors_list[i].append((idf_list[j]) * math.log(training_data[i]['doc'].count(tokens_document[j]) + 1,
                                                         2))  # using Tf = log(df/N)
        else:
            tf_idf_vectors_list[i].append(0)

    document_vector = np.array(tf_idf_vectors_list[i])
    document_vector = document_vector * document_vector
    mag_vec = math.sqrt(document_vector.sum())

    for j in range(0, len(tokens_document)):
        tf_idf_vectors_list[i][j] = tf_idf_vectors_list[i][j] / mag_vec

tf_idf_vectors_list = {'vectors': tf_idf_vectors_list, 'class': vectors_classes_list}

# saving data
with open('tf_idf_vectors_list.txt', 'w') as json_file:
    json.dump(tf_idf_vectors_list, json_file)

with open('idf_list.txt', 'w') as json_file:
    json.dump(idf_list, json_file)

with open('Tokens.txt', 'w') as json_file:
    json.dump(tokens_document, json_file)
