import nltk
from nltk.stem import WordNetLemmatizer
import numpy as np
import json
import math
import regex
import operator
import timeit
from tkinter import *
import tkinter as gui

nltk.download('punkt')
nltk.download('wordnet')

# Setting Timer ........................
process_start = timeit.default_timer()  # Start Timer for query processing

# StopWords List .......................
stopwords = []
wrds = ''
ffile1 = open('Stopword-List.txt', 'r')
for i in ffile1:
    wrds = i.lower().strip()
    stopwords.append(wrds)
ffile1.close()
wrds = ''


# Removing StopWords .......................
def RemoveStopWords(list):
    stopword_count = 0
    for word in stopwords:
        stopword_count = list.count(word)
        for j in range(0, stopword_count):
            list.remove(word)   # a, is remove
    return list


# File Fetching------------------------------------
def Speech_FileReading(i):
    List = []
    try:
        file = open('Trump Speechs/speech_'+str(i)+'.txt', 'r')
        line1 = file.readline().lower() # not used
        line2 = file.readline().lower()
        List.append(line2)
        F_List = regex.split('\W+', List[0])    # Removing ', . ' " etc'
        FinalList = RemoveStopWords(F_List)     # Stopwords Removal
        return FinalList
    except IndexError:
        print("Error in File_Name")
        return List


# Pre-processing......................
TotalDocuments = 56     # no of doc

Before_Lemmatization = []
tmp_list = []
for i in range(0, TotalDocuments):
    tmp_list = Speech_FileReading(i)
    Before_Lemmatization.append(tmp_list)   # 56 times

# lemmatization ..............................
After_Lemmatization = []
try:
    print("Lematization...From JSON File...")
    After_Lemmatization = json.load(open('Lemmatizatized_Words.json'))
except FileNotFoundError:
    print("After_Lemmatization.json :: File Not Found...")
    print("Lematization...From Scratch...")
    sentence_words = ''
    tmp_list = []
    count = 0
    wordnet_lemmatizer = WordNetLemmatizer()
    for i in range(0, len(Before_Lemmatization)):   # 56 times
        List1 = []
        for j in range(0, len(Before_Lemmatization[i])):    # document ith times
            sentence_words = Before_Lemmatization[i][j]
            tmp_list = nltk.word_tokenize(sentence_words)
            count = len(tmp_list)
            for k in range(0, count):
                List1.append(tmp_list[k].replace("\u00e2", ""))
        After_Lemmatization.append(List1)

    with open('Lemmatizatized_Words.json', 'w') as f:
        json.dump(After_Lemmatization, f)
        f.close()

# Get List for making uniqueness
ListOfTerms = []
for i in range(0, len(After_Lemmatization)):
    for j in range(0, len(After_Lemmatization[i])):
        ListOfTerms.append(After_Lemmatization[i][j])

# Distinct Words List -----
Distinct_ListOfTerms = list(dict.fromkeys(ListOfTerms))

# Creating Dictionary Document Matrix for all documents ...................................
Document_Dictonary = {}
try:
    print("Creating Document Matrix...From JSON File...")
    Document_Dictonary = json.load(open('Document_Dictonary.json'))
except FileNotFoundError:
    print("Document_Dictonary.json :: File Not Found...")
    print("Creating Document Matrix...From Scratch...")
    tmp_list = []
    count = 0
    for i in range(0, TotalDocuments):
        Document_Dictonary[i] = []

    for i in range(0, len(Distinct_ListOfTerms)):   # Contain Unique Terms
        for j in range(0, len(After_Lemmatization)):    # Terms in document 0-55
            for k in range(0, len(After_Lemmatization[j])):     # doc selection for term
                if After_Lemmatization[j][k] == Distinct_ListOfTerms[i]:
                    count += 1
            if count > 0:
                tmp_list.append(Distinct_ListOfTerms[i])
                tmp_list.append(count)
                Document_Dictonary[j].append(tmp_list)
            if count == 0:
                tmp_list.append(Distinct_ListOfTerms[i])
                tmp_list.append(count)
                Document_Dictonary[j].append(tmp_list)
            count = 0
            tmp_list = []

    with open('Document_Dictonary.json', 'w') as f:
        json.dump(Document_Dictonary, f)
        f.close()


# Creating TF Matrix using earlier created dictionary ...................................
Dictonary_TF = {}
try:
    print("Creating TF Matrix...Document_Dictonary.json File...")
    Dictonary_TF = json.load(open('Document_Dictonary.json'))
except FileNotFoundError:
    print("File Not Found...Further Process will give Error")


# Creating Document Frequency (DF) Matrix of all documents ...................................
Dictonary_DF = {}
try:
    print("Creating DF Matrix...From JSON File...")
    Dictonary_DF = json.load(open('Dictonary_DF.json'))
except FileNotFoundError:
    print("Dictonary_DF.json :: File Not Found...")
    print("Creating DF Matrix...From Scratch...")
    for i in Distinct_ListOfTerms:
        Dictonary_DF[i] = 0

    tmp_list = []
    tmp_list1 = []
    for i in Document_Dictonary:
        tmp_list = Document_Dictonary[i]     # First Key Value
        for j in tmp_list:
            tmp_list1 = j       # List contain [word, frequency]
            if (tmp_list1[0] in Dictonary_DF) and (tmp_list1[1] > 0):
                Dictonary_DF[tmp_list1[0]] += 1     # inc if found in doc

    with open('Dictonary_DF.json', 'w') as f:
        json.dump(Dictonary_DF, f)
        f.close()


# Creating IDF Matrix of all documents ...................................
Dictionary_IDF = {}
try:
    Dictionary_IDF = json.load(open('Dictonary_DF.json'))
except FileNotFoundError:
    print("File Not Found...Further Process will give Error")

try:
    print("Creating IDF Matrix...From JSON File...")
    Dictionary_IDF = json.load(open('Dictonary_IDF.json'))
except FileNotFoundError:
    print("Dictionary_IDF.json :: File Not Found...")
    print("Creating IDF Matrix...From Scratch...")
    for i in Dictionary_IDF:
        Dictionary_IDF[i] = round(math.log10(Dictionary_IDF[i] / TotalDocuments), 5)   # log(df/N)

    with open('Dictonary_IDF.json', 'w') as f:
        json.dump(Dictionary_IDF, f)
        f.close()


# Creating tf-idf Matrix Using Dictonary_TF and Dictionary_IDF ...................................
Dictonary_TF_IDF = {}
try:
    Dictonary_TF_IDF = json.load(open('Document_Dictonary.json'))
except FileNotFoundError:
    print("File Not Found...Further Process will give Error")

try:
    print("Creating TF-IDF Matrix...From JSON File...")
    Dictonary_TF_IDF = json.load(open('Dictonary_TF_IDF.json'))
except FileNotFoundError:
    print("Dictonary_TF_IDF.json :: File Not Found...")
    print("Creating TF-IDF Matrix...From Scratch...")
    tmp_list = []
    tmp_list1 = []
    tmp_list2 = []
    for i in Dictonary_TF_IDF: # Looking dictionary 0-55 [],[],[],...[]
        tmp_list2 = []
        tmp_list = Dictonary_TF_IDF[i]     # []
        for j in tmp_list:  # Element of List contain [word, Term-frequency] in list
            tmp_list1 = j
            if tmp_list1[0] in Dictionary_IDF:
                tmp_list1[1] = round(tmp_list1[1] * Dictionary_IDF[tmp_list1[0]], 5)    # tmp_list1=tf*idf
            tmp_list2.append(tmp_list1)
        Dictonary_TF_IDF[i] = tmp_list2

    with open('Dictonary_TF_IDF.json', 'w') as f:
        json.dump(Dictonary_TF_IDF, f)
        f.close()

# End of Document Filter Process ........................
process_stop = timeit.default_timer()  # End Time of Query Process
DocumentsProcessingTime = round(process_stop-process_start, 4)  # Query Time
print("Processing of Document Time Taken : " + str(DocumentsProcessingTime))


# --------------------------------------------------------------------
# QUERY TIME ---------------------------------------------------------

# Get Doc ID and return List of Documents Term
def ListOFDocument(doc_id):
    tmp_listx = []  # List of terms
    tmp_list1x = []
    tmp_list1x = Dictonary_TF_IDF[doc_id]
    for i in tmp_list1x:
        tmp_listx.append(i[1])
    return tmp_listx


# Magnitude Of Document
def MagnitudeOFDocument(tmp_lst):
    ArrayOFLst = np.array(tmp_lst)
    Magnitudex = round(np.linalg.norm(ArrayOFLst), 5)
    return Magnitudex


def QueryProcessing(query_str, alpha_value):
    tmp_list1 = []
    tmp_list = query_str.lower().split()
    lengthOFQuery = len(tmp_list)

    query_dictionary = {}
    query_tf = {}
    query_idf = {}
    query_tf_idf = {}
    for i in Distinct_ListOfTerms:  # Putting zeros
        query_dictionary[i] = 0
        query_tf[i] = 0
        query_idf[i] = 0

    for i in tmp_list:      # Term Counter
        if i in query_dictionary:
            query_dictionary[i] += 1    # adding 1 when word found in dictonaryOfTerms
            query_tf[i] += 1    # adding 1 when word found in dictonaryOfTerms
            query_idf[i] += 1    # adding 1 when word found in dictonaryOfTerms

    for i in tmp_list:      # IDF Maker
        if i in Dictionary_IDF:     # For check if term is present
            query_idf[i] = round(Dictionary_IDF[i], 5)

    for i in query_idf:     # TF * IDF
        query_tf_idf[i] = round(query_tf[i] * query_idf[i], 5)

    tmp_listOfQuery = []
    for i in Distinct_ListOfTerms:  # Upto end of term
        tmp_listOfQuery.append(query_tf_idf[i])

    tmp_listOfQuery_Array = np.array(tmp_listOfQuery)    # Making Array from List
    MagnitudeOfQuery = round(np.linalg.norm(tmp_listOfQuery_Array),5)  # Magnitude of Query

    # Building Cosine Similarity Matrix ........................................
    Sim_Matrix = {}
    for i in range(0, 56):
        Sim_Matrix[i] = 0    # Put zeros in matrix

    for i in range(0, TotalDocuments):      # From 0 to 55 :: Doc[i]
        tmp_listOFDoc = ListOFDocument(str(i))  # List of Doc 0-55
        MagnitudeOfDoc = MagnitudeOFDocument(tmp_listOFDoc)  # Magnitude of Doc
        Dot_Product = np.dot(tmp_listOFDoc, tmp_listOfQuery)    # Dot product of doc and query
        Magnitude_Mult = MagnitudeOfQuery * MagnitudeOfDoc
        Final_Sim = 0
        try:
            Final_Sim = Dot_Product / Magnitude_Mult
        except ValueError:
            Final_Sim = 0
        Sim_Matrix[i] = round(Final_Sim, 5)     # Matrix of all term Similarity

    # Document Retrieved as Result
    Final_RetrievedResult = {}
    for i in Sim_Matrix:
        if float(Sim_Matrix[i]) > float(alpha_value):      # Term Sim Value > Alpha
            Final_RetrievedResult[i] = Sim_Matrix[i]

    # Ranked Retrieved according to value of Alpha
    SortedDic = sorted(Final_RetrievedResult.items(), key=operator.itemgetter(1))    # According to Value
    SortedDic.reverse()   # ascending order
    Final_RetrievedDocument = []
    for i in SortedDic:     # List of Finally Ranked Order Documents
        Final_RetrievedDocument.append(i[0])

    return Final_RetrievedDocument


# ------------------------------------------------------------------------------------------
'''# For Command Prompt
alpha_value = input("Enter Alpha Value: ")
query_str = input("Enter Query: ")
start = timeit.default_timer()  # Start Timer for query processing
FinalListx = QueryProcessing(query_str, alpha_value)
stop = timeit.default_timer()       # End Time of Query Process
QueryProcessingTime = round(stop-start, 4)     # Query Time
print("Length = " + str(len(FinalListx)))
print(FinalListx)
print("Time Taken Query Process:" + str(QueryProcessingTime))
'''
# ------------------------------------------------------------------------------------------


def OnSearchButtonClicks(Query, alphaValue):
    start = timeit.default_timer()  # Start Timer for query processing
    Doc_Retrieved = []
    try:
        if len(Query) > 0:
            Doc_Retrieved = QueryProcessing(str(Query), float(alphaValue))
            QueryText.set(Query)

            word1 = []
            word2 = []
            if len(Doc_Retrieved) > 28:
                for i in range(0, 28):
                    word1.append(Doc_Retrieved[i])
                for i in range(28, len(Doc_Retrieved)):
                    word2.append(Doc_Retrieved[i])
                DocumentsFound1.set(word1)
                DocumentsFound2.set(word2)
            else:
                if len(Doc_Retrieved) == 0:
                    DocumentsFound1.set('No Document Found...!')
                    DocumentsFound2.set('...')
                    print('no doc found')
                else:
                    DocumentsFound1.set(Doc_Retrieved)
                    DocumentsFound2.set('')
        else:
            QueryText.set(" ")
            DocumentsFound1.set("[Document Found]")
            DocumentsFound1.set("...")
    except:
        QueryText.set("--ERROR--")
        print("Something Went Wrong")

    print(Doc_Retrieved)
    LengthDoc.set("Length = " + str(len(Doc_Retrieved)))
    stop = timeit.default_timer()  # End Time of Query Process
    QueryProcessingTime = round(stop-start, 4)  # Query Time
    TimeTaken.set("Search Time Taken :: " + str(QueryProcessingTime) + "\n")


# Working on GUI Phase ---------------------------------------------------------------------
window = gui.Tk()
window.title('Information Retrieval Assignment no.02')
window.geometry('700x480+250+50')
window.configure(background='black')
window.resizable(width=FALSE, height=FALSE)
window.winfo_toplevel()

TimeTakenForDoc = StringVar()
TimeTakenForDoc.set("Document Processing Time Taken :: " + str(DocumentsProcessingTime))
DocumentsFoundLabel1 = gui.Label(window, textvariable=TimeTakenForDoc)
DocumentsFoundLabel1.config(fg='white', background='black')
DocumentsFoundLabel1.config(font="Verdana 10")
DocumentsFoundLabel1.pack(side=BOTTOM, anchor=NW)

QueryText_Label00 = gui.Label(window, text='\n')
QueryText_Label00.config(fg='white', background='black')
QueryText_Label00.config(font="Courier 5")
QueryText_Label00.pack()

Heading = gui.Label(window, text="VSM Search Engine", fg='white')
Heading.configure(background='black')
Heading.config(font="Courier 48")
Heading.pack()

textField = StringVar()
QueryBox = gui.Text(window, width=40, height=1, bd=7)
QueryBox.config(font=("Courier", 20))
QueryBox.pack()

QueryText_Label0 = gui.Label(window, text='')
QueryText_Label0.config(fg='white', background='black')
QueryText_Label0.config(font="Courier 10")
QueryText_Label0.pack(side=BOTTOM)

textField0 = StringVar()
AlphaBox = gui.Text(window, width=20, height=1.2, bd=2)
AlphaBox.config(font=("Courier", 15))
AlphaBox.pack(side=BOTTOM)

QueryText_Label0 = gui.Label(window, text='(Default Value is 0.0005)\nValue of Alpha:: ')
QueryText_Label0.config(fg='white', background='black')
QueryText_Label0.config(font="Courier 10")
QueryText_Label0.pack(side=BOTTOM)


def query_input():      # Query Setter
    q1 = QueryBox.get("1.0", 'end-1c')
    QueryText.set(q1)
    if q1 == '':
        QueryText.set('[]')
        DocumentsFound1.set("[Document Found]")
        DocumentsFound1.set("...")
    return q1


def alpha_input():      # Alpha Value Setter
    alpha = AlphaBox.get("1.0", 'end-1c')
    if alpha == '':
        alpha = 0.0005
    return alpha


# Button
SearchBTN = gui.Button(window, text='Search Me...!', command=lambda: OnSearchButtonClicks(query_input(), alpha_input()))
SearchBTN.config(width=25, height=1, bd=6)
SearchBTN.config(padx=10, pady=6)
SearchBTN.config(fg='#0066cc')
SearchBTN.pack(pady=7)
SearchBTN.config(font='Verdana')

TimeTaken = StringVar()
TimeTaken.set("Search Time Taken :: -\n")
DocumentsFoundLabel1 = gui.Label(window, textvariable=TimeTaken)
DocumentsFoundLabel1.config(fg='white', background='black')
DocumentsFoundLabel1.config(font="Verdana 10")
DocumentsFoundLabel1.pack()

QueryText = StringVar()
QueryText.set("[Query]")
QueryText_Label = gui.Label(window, textvariable=QueryText)
QueryText_Label.config(fg='#ff1a1a', background='#333300')
QueryText_Label.config(font="Verdana 15")
QueryText_Label.pack()

DocumentsFound1 = StringVar()
DocumentsFound1.set("[Document Found]")
DocumentsFoundLabel1 = gui.Label(window, textvariable=DocumentsFound1)
DocumentsFoundLabel1.config(fg='#00ff99', background='#333300')
DocumentsFoundLabel1.config(font="Verdana 10")
DocumentsFoundLabel1.pack()

DocumentsFound2 = StringVar()
DocumentsFound2.set("...")
DocumentsFoundLabel1 = gui.Label(window, textvariable=DocumentsFound2)
DocumentsFoundLabel1.config(fg='#00ff99', background='#333300')
DocumentsFoundLabel1.config(font="Verdana 10")
DocumentsFoundLabel1.pack()

LengthDoc = StringVar()
LengthDoc.set("Length = 0")
DocumentsFoundLabel1 = gui.Label(window, textvariable=LengthDoc)
DocumentsFoundLabel1.config(fg='white', background='black')
DocumentsFoundLabel1.config(font="Courier 10")
DocumentsFoundLabel1.pack()


window.mainloop()
