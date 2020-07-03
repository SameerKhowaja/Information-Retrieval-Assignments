import json
import math
import numpy as np
import pandas as pd
import regex
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog, QPushButton, QGridLayout, QApplication, QDialog, QGroupBox, QVBoxLayout, QLabel
from nltk import *
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

with open('Tokens.txt') as fileOpen:
    Tokens = json.load(fileOpen)

with open('tf_idf_vectors_list.txt') as fileOpen:
    tf_idf_vectors_list = json.load(fileOpen)

with open('idf_list.txt') as fileOpen:
    idf_list = json.load(fileOpen)

classes = ['athletics', 'cricket', 'football', 'rugby', 'tennis']

# conversion
idf_list = np.array(idf_list)
unit_vectors_document = np.array(tf_idf_vectors_list['vectors'])
vector_classes_list = tf_idf_vectors_list['class']


def euclidean_distance(var1, var2):
    ans_tmp = (var1 - var2) * (var1 - var2)
    ans_tmp = math.sqrt(ans_tmp.sum())
    return ans_tmp


def cosine_distance(var1, var2):
    ans_tmp = var1 * var2
    return ans_tmp.sum()


lemmatizer = WordNetLemmatizer()
porter = PorterStemmer()


def apply_knn(k, example):
    document_distance = []
    temp = pd.Series(index=classes, dtype='int')
    vector_query = np.zeros(len(Tokens))

    for i in range(0, len(example)):
        # applying lemmatizatization to query term
        qry_term = porter.stem(str.lower(example[i]))
        if qry_term in Tokens:  # calcaltes tf
            index = Tokens.index(qry_term)
            vector_query[index] = vector_query[index] + 1

    vector_query = np.log2(vector_query + 1) * idf_list  # calculates tf-idf

    q_mag = vector_query * vector_query
    q_mag = q_mag.sum()
    q_mag = math.sqrt(q_mag)
    vector_query = vector_query / q_mag

    for i in range(0, len(unit_vectors_document)):
        ans_tmp = euclidean_distance(unit_vectors_document[i], vector_query)
        document_distance.append((ans_tmp, vector_classes_list[i]))

    for i in range(0, len(document_distance) - 1):
        for j in range(0, len(document_distance) - 1):
            if document_distance[j][0] > document_distance[j + 1][0]:
                tmp = document_distance[j]
                document_distance[j] = document_distance[j + 1]
                document_distance[j + 1] = tmp

    for i in range(0, k):
        temp.loc[document_distance[i][1]] = temp.loc[document_distance[i][1]] + 1

    return temp.idxmax()


def file_read(file):
    fileOpen = open(file, 'r')
    outputFile = ''
    for line in fileOpen:
        outputFile = outputFile + line

    outputFile = outputFile.replace('\n', ' ')
    outputFile = regex.sub("'", "", outputFile)
    outputFile = regex.split('\W+', outputFile)
    fileOpen.close()
    return outputFile


def test_accuracy(folder_name):
    testing_data = []
    for className in classes:
        root_path = folder_name + '/' + className
        for i in os.listdir(root_path):
            if os.path.isfile(os.path.join(root_path, i)):
                testing_data.append({'doc': file_read(folder_name + '/' + className + '/' + i), 'class': className})

    confusion_matrix = pd.DataFrame(columns=classes, index=classes)
    confusion_matrix.index.name = 'actual'
    confusion_matrix.columns.name = 'predicted'
    confusion_matrix.loc[classes] = 0

    # prediction actual
    for i in range(len(testing_data)):
        predict = apply_knn(3, testing_data[i]['doc'])
        confusion_matrix[predict][testing_data[i]['class']] = confusion_matrix[predict][testing_data[i]['class']] + 1

    confusion_matrix.loc['Total'] = confusion_matrix.sum(axis=0)
    confusion_matrix['Total'] = confusion_matrix.sum(axis=1)

    # accuracy ,precision and recall
    confusion_matrix_precision_recall = pd.DataFrame(columns=['precision', 'recall'], index=classes)
    accuracyy = 0
    for i in classes:
        accuracyy = accuracyy + confusion_matrix[i][i]
        confusion_matrix_precision_recall['precision'][i] = confusion_matrix[i][i] / \
                                                            confusion_matrix[i]['Total']
        confusion_matrix_precision_recall['recall'][i] = confusion_matrix[i][i] / \
                                                         confusion_matrix['Total'][i]

    print(confusion_matrix, '\n\n')
    print(confusion_matrix_precision_recall, '\n\n')
    print('accuracy : ', (accuracyy / confusion_matrix['Total']['Total']) * 100, "%\n")

    return (accuracyy / confusion_matrix['Total']['Total']) * 100


# GUI class
class GUI_Class(QDialog):
    def __init__(self):
        super().__init__()

        self.B1 = QPushButton('upload file Button', self)
        self.gridlayout2 = QGridLayout()
        self.groupBox = QGroupBox('KNN Prediction')
        self.L4 = QLabel()
        self.L3 = QLabel()
        self.L2 = QLabel()
        self.L1 = QLabel()
        self.setWindowTitle('KNN Prediction')
        self.setWindowIcon(QIcon('click1.png'))
        self.setStyleSheet("QDialog {background-color: '#000000'}")
        self.ret = []
        self.setGeometry(200, 200, 500, 300)
        self.vbox = QVBoxLayout()
        self.flag = 0
        self.createLayout()
        self.vbox.addWidget(self.groupBox)
        self.setLayout(self.vbox)
        self.show()

    def ClickMe(self):
        if self.L2.text() != '':
            example = file_read(self.L2.text())
            prd = apply_knn(3, example)
            self.L1.setText('Sport : ' + prd)

        if self.L4.text() != '':
            accuracyy = test_accuracy(self.L4.text())
            self.L3.setText('ACCURACY : ' + str(accuracyy))

    def getFileName(self):
        fileName, _ = QFileDialog.getOpenFileName(self, 'File', 'C:\'', '*.txt')
        self.L2.setText(fileName)

    def getFolderNamw(self):
        folder_name = QFileDialog.getExistingDirectory(self, 'Directory')
        self.L4.setText(folder_name)

    def createLayout(self):
        self.groupBox.setStyleSheet("color: #ffffff; font: bold 20px")
        gridlayout = QGridLayout()

        self.B1.setMinimumHeight(20)
        self.B1.setStyleSheet(" background: qradialgradient(cx: 0.2, cy: -0.3, fx: 0.4, fy: -0.3, radius: 1.4, stop: 0 #ad3f0c , stop: 1 #ad3f0c  ); \
                               color: #ffffff; \
                               border-style: outset; \
                               border-width: 2px; \
                               border-color: #ad3f0c; \
                               border-radius: 9px")
        self.B1.clicked.connect(self.getFileName)
        gridlayout.addWidget(self.B1, 0, 0)

        B3 = QPushButton('submit Button', self)
        B3.setIcon(QtGui.QIcon('icon'))
        B3.setIconSize(QtCore.QSize(150, 50))
        B3.setMinimumHeight(30)
        B3.setStyleSheet(" background: qradialgradient(cx: 0.2, cy: -0.3, fx: 0.4, fy: -0.3, radius: 1.4, stop: 0 #0c0fad , stop: 1 #0c0fad  ); \
                               color: #ffffff; \
                               border-style: outset; \
                               border-width: 2px; \
                               border-color: #0c0fad; \
                               border-radius: 10px")
        B3.clicked.connect(self.ClickMe)
        gridlayout.addWidget(B3, 2, 0)

        B4 = QPushButton('upload test Folder Button', self)
        B4.setIcon(QtGui.QIcon('icon'))
        B4.setIconSize(QtCore.QSize(20, 20))
        B4.setMinimumHeight(20)
        B4.setStyleSheet(" background: qradialgradient(cx: 0.2, cy: -0.3, fx: 0.4, fy: -0.3, radius: 1.4, stop: 0 #ad3f0c , stop: 1 #ad3f0c  ); \
                               color: #ffffff; \
                               border-style: outset; \
                               border-width: 2px; \
                               border-color: #ad3f0c; \
                               border-radius: 9px")
        B4.clicked.connect(self.getFolderNamw)
        gridlayout.addWidget(B4, 1, 0)
        self.L1.setStyleSheet("color:#ffffff")
        gridlayout.addWidget(self.L1, 3, 0)
        self.L2.setStyleSheet("color:#ffffff")
        gridlayout.addWidget(self.L2, 7, 0)
        self.L3.setStyleSheet("color:#ffffff")
        gridlayout.addWidget(self.L3, 4, 0)
        self.L4.setStyleSheet("color:#ffffff")
        gridlayout.addWidget(self.L4, 8, 0)
        self.groupBox.setLayout(gridlayout)


Appli = QApplication(sys.argv)
ret_model = GUI_Class()
sys.exit(Appli.exec())
