import timeit
import json
from tkinter import *
import tkinter as gui

inverted = {}
# Stopwords File Fetching
stopword_num_lines = sum(1 for line in open('Stopword-List.txt', 'r'))
Stopword = []
file = open('Stopword-List.txt', 'r')
for i in range(0, stopword_num_lines):
    line = file.readline().strip()
    if line != '':
        Stopword.append(line)
file.close()
Stopword.sort()


def RemovingStopWordsANDOthers(file_0):
    # Removing (, : " ;) --------------------------------------------
    temp = ''
    for i in range(0, len(file_0)):
        for j in range(0, len(file_0[i])):
            if file_0[i][j] != ',' and file_0[i][j] != ':' and file_0[i][j] != '"' and file_0[i][j] != ';' and \
                    file_0[i][j] != '?':
                temp += file_0[i][j]
        file_0[i] = temp
        temp = ''
    # Removing (, : " ;) Completed -----------------------------------

    # Removing (.) at end --------------------------------------------
    temp = ''
    # Remove end dot
    for i in range(0, len(file_0)):
        try:
            if file_0[i][-1] == '.':
                for j in range(0, len(file_0[i]) - 1):
                    temp += file_0[i][j]
                file_0[i] = temp
                temp = ''
            else:
                for j in range(0, len(file_0[i])):
                    temp += file_0[i][j]
                file_0[i] = temp
                temp = ''
        except IndexError:
            x = 1
    # Removing (.) at end Completed -----------------------------------

    # Removing (. and -) from middle ----------------------------------
    tempWords = []
    tempIndexes = []
    length_Of_File = 0
    # Making List of join words with middle '.'
    for i in range(0, len(file_0)):
        for j in range(0, len(file_0[i])):
            if (file_0[i][j] == '.' or file_0[i][j] == '-' or file_0[i][j] == '_') and len(file_0[i]) > 4:
                tempIndexes.append(file_0.index(file_0[i]))
                tempWords.append(file_0[i])

    length_Of_File = len(file_0)
    for i in range(0, len(file_0)):
        for j in range(0, len(tempWords)):
            try:
                if file_0[i] == tempWords[j]:
                    file_0.remove(tempWords[j])
            except IndexError:
                x = 1

    temp = ''
    seperate_index_len = 0
    merge_index_len = 0
    newWords = []
    for i in range(0, len(tempWords)):
        merge_index_len = len(tempWords[i])
        for j in range(0, len(tempWords[i])):
            if tempWords[i][j] != '.' and tempWords[i][j] != '-' and tempWords[i][j] != '_':
                temp += tempWords[i][j]
            else:
                temp += ' '
                seperate_index_len = len(temp) - 1

        for j in range(0, 1):
            temp = ''
            for a in range(0, seperate_index_len):
                temp += tempWords[i][a]
            newWords.append(temp)
            temp = ''
            for a in range(seperate_index_len + 1, merge_index_len):
                temp += tempWords[i][a]
            newWords.append(temp)
            temp = ''

    newIndexes = []
    gapBetween = 0
    tempvalue = 0
    for i in range(0, len(tempIndexes)):
        if i == 0:
            newIndexes.append(tempIndexes[i])
            newIndexes.append(tempIndexes[i] + 1)
            tempvalue = tempIndexes[i] + 1
        elif i == len(tempIndexes) - 1:
            gapBetween = tempIndexes[i] - tempIndexes[i - 1]
            newIndexes.append(tempvalue + gapBetween)
            newIndexes.append(tempvalue + gapBetween + 1)
        else:
            gapBetween = tempIndexes[i] - tempIndexes[i - 1]
            newIndexes.append(tempvalue + gapBetween)
            newIndexes.append(tempvalue + gapBetween + 1)
            tempvalue = tempvalue + gapBetween + 1

    for i in range(0, len(newIndexes)):
        file_0.insert(newIndexes[i], newWords[i])
    # Removing (. and -) from middle ----------------------------------

    # For Remove [applause], [laughter], [inaudible], (ph)
    temp = ''
    for i in range(0, len(file_0)):
        for j in range(0, len(file_0[i])):
            temp += file_0[i][j]
        temp = temp.replace('[applause]', '')
        temp = temp.replace('[laughter]', '')
        temp = temp.replace('[inaudible]', '')
        temp = temp.replace('[crosstalk]', '')
        temp = temp.replace('.....', '')
        temp = temp.replace('..', '')
        temp = temp.replace('.', '')
        temp = temp.replace('(ph)', '')
        file_0[i] = temp
        temp = ''

    # removing --
    count = file_0.count('â€”')
    for i in range(0, count):
        file_0.remove('â€”')
    count = file_0.count('â–')
    for i in range(0, count):
        file_0.remove('â–')

    # Remove Stop Words from file ---------------------------------
    stopword_count = 0
    stopword_word = ''
    for i in range(0, len(Stopword)):
        stopword_word = Stopword[i]
        stopword_count = file_0.count(stopword_word)

        for j in range(0, stopword_count):
            file_0.remove(stopword_word)
    # Remove Stop Words Completed ---------------------------------
    return file_0


# Stemming rules from Website...
# http://snowball.tartarus.org/algorithms/porter/stemmer.html
# Potter Stemming Function --------------------------------------
def StemmingFunction(file_0):
    file_0 = RemovingStopWordsANDOthers(file_0)
    # Potter Stemming Step 1-5 ---------------------------------------
    # Potter Stemming Step 1 ---------------------------------------
    temp = ''
    vowelflag = False
    m = 0
    for i in range(0, len(file_0)):
        n = 0
        m = 0
        wordLength = len(file_0[i])
        if wordLength > 3:
            # sses -> ss
            if file_0[i][-4:] == 'sses':
                m += 1
                for j in range(wordLength - 2):
                    temp += file_0[i][j]
                file_0[i] = temp
                temp = ''
            # ies -> i
            elif file_0[i][-3:] == 'ies':
                m += 1
                for j in range(wordLength - 2):
                    temp += file_0[i][j]
                file_0[i] = temp
                temp = ''

        temp = ''
        wordLength = len(file_0[i])
        if wordLength > 2:
            # ss -> ss and s -> --
            if file_0[i][-1] == 's' and file_0[i][-2] == 's':
                for j in range(wordLength):
                    temp += file_0[i][j]
                file_0[i] = temp
                temp = ''
            elif file_0[i][-1] == 's':
                m += 1
                for j in range(wordLength - 1):
                    temp += file_0[i][j]
                file_0[i] = temp
                temp = ''

        temp = ''
        wordLength = len(file_0[i])
        # eed -> ee if contain vowel
        for j in range(0, wordLength - 3):
            if file_0[i][j] == 'a' or file_0[i][j] == 'e' or file_0[i][j] == 'i' \
                    or file_0[i][j] == 'o' or file_0[i][j] == 'u':
                vowelflag = True
        if vowelflag and wordLength > 3:
            if (m + 1 > 0) and (file_0[i][-3:] == 'eed'):
                m += 1
                for j in range(wordLength - 1):
                    temp += file_0[i][j]
                file_0[i] = temp
                temp = ''
                vowelflag = False

        temp = ''
        vowelflag = False
        n = 0
        # ing -> --
        wordLength = len(file_0[i])
        for j in range(0, wordLength - 3):
            if file_0[i][j] == 'a' or file_0[i][j] == 'e' or file_0[i][j] == 'i' \
                    or file_0[i][j] == 'o' or file_0[i][j] == 'u':
                vowelflag = True
        if (wordLength > 4) and (vowelflag or file_0[i][-4] == 'y'):
            # ing -> --
            if file_0[i][-3:] == 'ing':
                m += 1
                for j in range(wordLength - 3):
                    temp += file_0[i][j]
                file_0[i] = temp
                n = 1
                temp = ''
                vowelflag = False
                # (cvc, if second c is not w,x or y -> add e at end)
                if (n == 1) and (len(file_0[i]) >= 3) and (
                        file_0[i][-3] != 'a' and file_0[i][-3] != 'e' and file_0[i][-3] != 'i' and file_0[i][
                    -3] != 'o' and file_0[i][-3] != 'u') \
                        and (
                        file_0[i][-2] == 'a' or file_0[i][-2] == 'e' or file_0[i][-2] == 'i' or file_0[i][-2] == 'o' or
                        file_0[i][-2] == 'u') and \
                        (file_0[i][-1] != 'a' and file_0[i][-1] != 'e' and file_0[i][-1] != 'i' and file_0[i][
                            -1] != 'o' and file_0[i][-1] != 'u') and \
                        (file_0[i][-1] != 'w' and file_0[i][-1] != 'x' and file_0[i][-1] != 'y'):
                    m += 1
                    for j in range(len(file_0[i])):
                        temp += file_0[i][j]
                    file_0[i] = temp + 'e'
                n = 0
                temp = ''
                # at -> ate, bl -> ble, iz -> ize
                if file_0[i][-2:] == 'at' or file_0[i][-2:] == 'bl' or file_0[i][-2:] == 'iz':
                    m += 1
                    for j in range(len(file_0[i])):
                        temp += file_0[i][j]
                    file_0[i] = temp + 'e'
                temp = ''
                # (*d and not (*L or *S or *Z)) -> single letter
                if (len(file_0[i]) > 3) and (file_0[i][-1] == file_0[i][-2]) and (
                        file_0[i][-1] != 'l' and file_0[i][-1] != 's' and file_0[i][-1] != 'z') \
                        and (file_0[i][-1] != 'a' and file_0[i][-1] != 'e' and file_0[i][-1] != 'i' and file_0[i][
                    -1] != 'o' and file_0[i][-1] != 'u'):
                    m += 1
                    for j in range(len(file_0[i]) - 1):
                        temp += file_0[i][j]
                    file_0[i] = temp
                temp = ''

        temp = ''
        vowelflag = False
        n = 0
        # ed -> --
        wordLength = len(file_0[i])
        for j in range(0, wordLength - 2):
            if file_0[i][j] == 'a' or file_0[i][j] == 'e' or file_0[i][j] == 'i' \
                    or file_0[i][j] == 'o' or file_0[i][j] == 'u':
                vowelflag = True
        if vowelflag and wordLength > 0:
            # ed -> --
            if file_0[i][-2:] == 'ed':
                m += 1
                for j in range(wordLength - 2):
                    temp += file_0[i][j]
                file_0[i] = temp
                n = 1
                temp = ''
                vowelflag = False
                # (cvc, if second c is not w,x or y -> add e at end)
                if (n == 1) and (len(file_0[i]) >= 3) and (
                        file_0[i][-3] != 'a' and file_0[i][-3] != 'e' and file_0[i][-3] != 'i' and file_0[i][
                    -3] != 'o' and file_0[i][-3] != 'u') \
                        and (
                        file_0[i][-2] == 'a' or file_0[i][-2] == 'e' or file_0[i][-2] == 'i' or file_0[i][-2] == 'o' or
                        file_0[i][-2] == 'u') and \
                        (file_0[i][-1] != 'a' and file_0[i][-1] != 'e' and file_0[i][-1] != 'i' and file_0[i][
                            -1] != 'o' and file_0[i][-1] != 'u') and \
                        (file_0[i][-1] != 'w' and file_0[i][-1] != 'x' and file_0[i][-1] != 'y'):
                    m += 1
                    for j in range(len(file_0[i])):
                        temp += file_0[i][j]
                    file_0[i] = temp + 'e'
                n = 0
                temp = ''
                # at -> ate, bl -> ble, iz -> ize
                if file_0[i][-2:] == 'at' or file_0[i][-2:] == 'bl' or file_0[i][-2:] == 'iz':
                    m += 1
                    for j in range(len(file_0[i])):
                        temp += file_0[i][j]
                    file_0[i] = temp + 'e'
                temp = ''
                # (*d and not (*L or *S or *Z)) -> single letter
                if (len(file_0[i]) > 3) and (file_0[i][-1] == file_0[i][-2]) and (
                        file_0[i][-1] != 'l' and file_0[i][-1] != 's' and file_0[i][-1] != 'z') \
                        and (file_0[i][-1] != 'a' and file_0[i][-1] != 'e' and file_0[i][-1] != 'i' and file_0[i][
                    -1] != 'o' and file_0[i][-1] != 'u'):
                    m += 1
                    for j in range(len(file_0[i]) - 1):
                        temp += file_0[i][j]
                    file_0[i] = temp
                temp = ''

        temp = ''
        vowelflag = False
        # y -> i if contain vowel
        wordLength = len(file_0[i])
        for j in range(0, wordLength - 1):
            if file_0[i][j] == 'a' or file_0[i][j] == 'e' or file_0[i][j] == 'i' \
                    or file_0[i][j] == 'o' or file_0[i][j] == 'u':
                vowelflag = True
        if vowelflag and wordLength > 1:
            if file_0[i][-1] == 'y':
                m += 1
                for j in range(wordLength - 1):
                    temp += file_0[i][j]
                file_0[i] = temp + 'i'
                temp = ''
                vowelflag = False
        # Porter Stemming Step 1 Completed ---------------------------------------
        # Porter Stemming Step 2 ---------------------------------------
        temp = ''
        wordLength = len(file_0[i])
        if (m + 1 > 0) and (wordLength >= 3):
            # ational -> ate
            if file_0[i][-6:] == 'ational':
                m += 1
                for j in range(wordLength - 5):
                    temp += file_0[i][j]
                if len(temp) > 0:
                    file_0[i] = temp + 'e'
                temp = ''
            # tional -> tion
            elif file_0[i][-6:] == 'tional':
                m += 1
                for j in range(wordLength - 2):
                    temp += file_0[i][j]
                if len(temp) > 0:
                    file_0[i] = temp
                temp = ''
            # enci -> ence
            elif file_0[i][-4:] == 'enci':
                m += 1
                for j in range(wordLength - 1):
                    temp += file_0[i][j]
                if len(temp) > 0:
                    file_0[i] = temp + 'e'
                temp = ''
            # anci -> ance
            elif file_0[i][-4:] == 'anci':
                m += 1
                for j in range(wordLength - 1):
                    temp += file_0[i][j]
                if len(temp) > 0:
                    file_0[i] = temp + 'e'
                temp = ''
            # izer -> ize
            elif file_0[i][-4:] == 'izer':
                m += 1
                for j in range(wordLength - 1):
                    temp += file_0[i][j]
                if len(temp) > 0:
                    file_0[i] = temp
                temp = ''
            # abli -> able
            elif file_0[i][-4:] == 'abli':
                m += 1
                for j in range(wordLength - 1):
                    temp += file_0[i][j]
                if len(temp) > 0:
                    file_0[i] = temp + 'e'
                temp = ''
            # alli -> al
            elif file_0[i][-4:] == 'alli':
                m += 1
                for j in range(wordLength - 2):
                    temp += file_0[i][j]
                if len(temp) > 0:
                    file_0[i] = temp
                temp = ''
            # entli -> ent
            elif file_0[i][-5:] == 'entli':
                m += 1
                for j in range(wordLength - 2):
                    temp += file_0[i][j]
                if len(temp) > 0:
                    file_0[i] = temp
                temp = ''
            # eli -> e
            elif file_0[i][-3:] == 'eli':
                m += 1
                for j in range(wordLength - 2):
                    temp += file_0[i][j]
                if len(temp) > 0:
                    file_0[i] = temp
                temp = ''
            # ousli -> ous
            elif file_0[i][-5:] == 'ousli':
                m += 1
                for j in range(wordLength - 2):
                    temp += file_0[i][j]
                if len(temp) > 0:
                    file_0[i] = temp
                temp = ''
            # ization -> ize
            elif file_0[i][-7:] == 'ization':
                m += 1
                for j in range(wordLength - 5):
                    temp += file_0[i][j]
                if len(temp) > 0:
                    file_0[i] = temp + 'e'
                temp = ''
            # ation -> ate
            elif file_0[i][-5:] == 'ation':
                m += 1
                for j in range(wordLength - 3):
                    temp += file_0[i][j]
                if len(temp) > 0:
                    file_0[i] = temp + 'e'
                temp = ''
            # ator -> ate
            elif file_0[i][-4:] == 'ator':
                m += 1
                for j in range(wordLength - 2):
                    temp += file_0[i][j]
                if len(temp) > 0:
                    file_0[i] = temp + 'e'
                temp = ''
            # alism -> al
            elif file_0[i][-5:] == 'alism':
                m += 1
                for j in range(wordLength - 3):
                    temp += file_0[i][j]
                if len(temp) > 0:
                    file_0[i] = temp
                temp = ''
            # iveness -> ive
            elif file_0[i][-7:] == 'iveness':
                m += 1
                for j in range(wordLength - 4):
                    temp += file_0[i][j]
                if len(temp) > 0:
                    file_0[i] = temp
                temp = ''
            # fulness -> ful
            elif file_0[i][-7:] == 'fulness':
                m += 1
                for j in range(wordLength - 4):
                    temp += file_0[i][j]
                if len(temp) > 0:
                    file_0[i] = temp
                temp = ''
            # ousness -> ous
            elif file_0[i][-7:] == 'ousness':
                m += 1
                for j in range(wordLength - 4):
                    temp += file_0[i][j]
                if len(temp) > 0:
                    file_0[i] = temp
                temp = ''
            # aliti -> al
            elif file_0[i][-5:] == 'aliti':
                m += 1
                for j in range(wordLength - 3):
                    temp += file_0[i][j]
                if len(temp) > 0:
                    file_0[i] = temp
                temp = ''
            # iviti -> ive
            elif file_0[i][-5:] == 'iviti':
                m += 1
                for j in range(wordLength - 3):
                    temp += file_0[i][j]
                if len(temp) > 0:
                    file_0[i] = temp + 'e'
                temp = ''
            # biliti -> ble
            elif file_0[i][-6:] == 'biliti':
                m += 1
                for j in range(wordLength - 5):
                    temp += file_0[i][j]
                if len(temp) > 0:
                    file_0[i] = temp + 'le'
                temp = ''
            # biliti -> ble
            elif file_0[i][-3:] == 'ite':
                m += 1
                for j in range(wordLength - 1):
                    temp += file_0[i][j]
                if len(temp) > 0:
                    file_0[i] = temp
                temp = ''
        # Porter Stemming Step 2 Completed ---------------------------------------
        # Porter Stemming Step 3 ---------------------------------------
        temp = ''
        wordLength = len(file_0[i])
        if (m + 1 > 0) and (wordLength >= 3):
            # icate -> ic
            if file_0[i][-5:] == 'icate':
                m += 1
                for j in range(wordLength - 3):
                    temp += file_0[i][j]
                if len(temp) > 0:
                    file_0[i] = temp
                temp = ''
            # ative -> --
            elif (wordLength > 5) and (file_0[i][-5:] == 'ative'):
                m += 1
                for j in range(wordLength - 5):
                    temp += file_0[i][j]
                if len(temp) > 0:
                    file_0[i] = temp
                temp = ''
            # alize -> al
            elif file_0[i][-5:] == 'alize':
                m += 1
                for j in range(wordLength - 3):
                    temp += file_0[i][j]
                if len(temp) > 0:
                    file_0[i] = temp
                temp = ''
            # iciti -> ic
            elif file_0[i][-5:] == 'iciti':
                m += 1
                for j in range(wordLength - 3):
                    temp += file_0[i][j]
                if len(temp) > 0:
                    file_0[i] = temp
                temp = ''
            # ical -> ic
            elif file_0[i][-4:] == 'ical':
                m += 1
                for j in range(wordLength - 2):
                    temp += file_0[i][j]
                if len(temp) > 0:
                    file_0[i] = temp
                temp = ''
            # ful -> --
            elif (wordLength > 3) and (file_0[i][-3:] == 'ful'):
                m += 1
                for j in range(wordLength - 3):
                    temp += file_0[i][j]
                if len(temp) > 0:
                    file_0[i] = temp
                temp = ''
            # iveness -> ive
            elif file_0[i][-7:] == 'iveness':
                m += 1
                for j in range(wordLength - 4):
                    temp += file_0[i][j]
                if len(temp) > 0:
                    file_0[i] = temp
                temp = ''
            # ness -> --
            elif (wordLength > 4) and (file_0[i][-4:] == 'ness'):
                m += 1
                for j in range(wordLength - 4):
                    temp += file_0[i][j]
                if len(temp) > 0:
                    file_0[i] = temp
                temp = ''
        # Porter Stemming Step 3 Completed ---------------------------------------
        # Porter Stemming Step 4 ---------------------------------------
        temp = ''
        wordLength = len(file_0[i])
        if wordLength >= 2:
            # al -> --
            if file_0[i][-2:] == 'al':
                m += 1
                for j in range(wordLength - 2):
                    temp += file_0[i][j]
                if len(temp) > 1:
                    file_0[i] = temp
                temp = ''
            # ance -> --
            elif file_0[i][-4:] == 'ance':
                m += 1
                for j in range(wordLength - 4):
                    temp += file_0[i][j]
                if len(temp) > 1:
                    file_0[i] = temp
                temp = ''
            # ence -> --
            elif file_0[i][-4:] == 'ence':
                m += 1
                for j in range(wordLength - 4):
                    temp += file_0[i][j]
                if len(temp) > 1:
                    file_0[i] = temp
                temp = ''
            # er -> --
            elif file_0[i][-2:] == 'er':
                m += 1
                for j in range(wordLength - 2):
                    temp += file_0[i][j]
                if len(temp) > 1:
                    file_0[i] = temp
                temp = ''
            # ic -> --
            elif file_0[i][-2:] == 'ic':
                m += 1
                for j in range(wordLength - 2):
                    temp += file_0[i][j]
                if len(temp) > 1:
                    file_0[i] = temp
                temp = ''
            # able -> --
            elif file_0[i][-4:] == 'able':
                m += 1
                for j in range(wordLength - 4):
                    temp += file_0[i][j]
                if len(temp) > 1:
                    file_0[i] = temp
                temp = ''
            # ible -> --
            elif file_0[i][-4:] == 'ible':
                m += 1
                for j in range(wordLength - 4):
                    temp += file_0[i][j]
                if len(temp) > 1:
                    file_0[i] = temp
                temp = ''
            # ant -> --
            elif file_0[i][-3:] == 'ant':
                m += 1
                for j in range(wordLength - 3):
                    temp += file_0[i][j]
                if len(temp) > 1:
                    file_0[i] = temp
                temp = ''
            # ement -> --
            elif file_0[i][-5:] == 'ement':
                m += 1
                for j in range(wordLength - 5):
                    temp += file_0[i][j]
                if len(temp) > 1:
                    file_0[i] = temp
                temp = ''
            # ment -> --
            elif file_0[i][-4:] == 'ment':
                m += 1
                for j in range(wordLength - 4):
                    temp += file_0[i][j]
                if len(temp) > 1:
                    file_0[i] = temp
                temp = ''
            # ent -> --
            elif file_0[i][-3:] == 'ent':
                m += 1
                for j in range(wordLength - 3):
                    temp += file_0[i][j]
                if len(temp) > 1:
                    file_0[i] = temp
                temp = ''
            # sion -> s or tion -> t
            elif (file_0[i][-4:] == 'sion') and (file_0[i][-4:] == 'tion'):
                m += 1
                for j in range(wordLength - 3):
                    temp += file_0[i][j]
                if len(temp) > 1:
                    file_0[i] = temp
                temp = ''
            # ou -> --
            elif file_0[i][-2:] == 'ou':
                m += 1
                for j in range(wordLength - 2):
                    temp += file_0[i][j]
                if len(temp) > 1:
                    file_0[i] = temp
                temp = ''
            # ism -> --
            elif file_0[i][-3:] == 'ism':
                m += 1
                for j in range(wordLength - 3):
                    temp += file_0[i][j]
                if len(temp) > 1:
                    file_0[i] = temp
                temp = ''
            # ate -> --
            elif file_0[i][-3:] == 'ate':
                m += 1
                for j in range(wordLength - 3):
                    temp += file_0[i][j]
                if len(temp) > 1:
                    file_0[i] = temp
                temp = ''
            # iti -> --
            elif file_0[i][-3:] == 'iti':
                m += 1
                for j in range(wordLength - 3):
                    temp += file_0[i][j]
                if len(temp) > 1:
                    file_0[i] = temp
                temp = ''
            # ous -> --
            elif file_0[i][-3:] == 'ous':
                m += 1
                for j in range(wordLength - 3):
                    temp += file_0[i][j]
                if len(temp) > 1:
                    file_0[i] = temp
                temp = ''
            # ive -> --
            elif file_0[i][-3:] == 'ive':
                m += 1
                for j in range(wordLength - 3):
                    temp += file_0[i][j]
                if len(temp) > 1:
                    file_0[i] = temp
                temp = ''
            # ize -> --
            elif file_0[i][-3:] == 'ize':
                m += 1
                for j in range(wordLength - 3):
                    temp += file_0[i][j]
                if len(temp) > 1:
                    file_0[i] = temp
                temp = ''
        # Porter Stemming Step 4 Completed ---------------------------------------
        # Porter Stemming Step 5 ---------------------------------------
        temp = ''
        wordLength = len(file_0[i])
        if wordLength > 1:
            # e -> -- if m>2
            if (m >= 2) and (file_0[i][-1] == 'e') and (file_0[i][-1] != file_0[i][-2]):
                m += 1
                for j in range(wordLength - 1):
                    temp += file_0[i][j]
                if len(temp) > 1:
                    file_0[i] = temp
                temp = ''
            if (m + 1 == 1) and (file_0[i][-1] == 'e') and (file_0[i][-1] != file_0[i][-2]):
                for j in range(wordLength - 1):
                    temp += file_0[i][j]
                if (wordLength > 4) and (
                        temp[-2] == 'a' or temp[-2] == 'e' or temp[-2] == 'i' or temp[-2] == 'o' or temp[-2] == 'u') and \
                        (temp[-1] != 'a' and temp[-1] != 'e' and temp[-1] != 'i' and temp[-1] != 'o' and temp[
                            -1] != 'u') and \
                        (temp[-3] != 'a' and temp[-3] != 'e' and temp[-3] != 'i' and temp[-3] != 'o' and temp[
                            -3] != 'u'):
                    if len(temp) > 1:
                        file_0[i] = temp + 'e'
                else:
                    if len(temp) > 1:
                        file_0[i] = temp
                temp = ''

        # Porter Stemming Step 5 Completed ---------------------------------------
        # (m > 1 and *d and *L) -> single letter ---------------------------
        temp = ''
        wordLength = len(file_0[i])
        if (m + 1 > 1) and (wordLength > 4):
            # es -> --
            if file_0[i][-2:] == 'll':
                for j in range(wordLength - 1):
                    temp += file_0[i][j]
                file_0[i] = temp
                temp = ''
    # End of Potter Stemming Loop

    # Remove Repeatation ----------------------
    try:
        file_0.remove('')
        file_0.remove('')
        file_0.remove('')
        file_0.remove('')
        file_0.remove('')
        file_0.remove('')
    except ValueError:
        x = 1

    # file_0 = list(dict.fromkeys(file_0))
    return file_0
# End of Stemming Function -------------------------------------------------------------------------


# File Fetching------------------------------------
def SpeechFile(i):
    try:
        file = open('Trump Speechs/speech_'+str(i)+'.txt', 'r')
        line1 = file.readline().lower()
        line2 = file.readline().lower()
        List = line2.split()
        return List
    except IndexError:
        print("Error in File_Name")


# Timer of Stemming Document --------
start1 = timeit.default_timer()
# Making Words List After Stemming ---------------------
MergeList = []
DistintWordList = []
try:
    MergeList = json.load(open('MergeList.json'))
    DistintWordList = json.load(open('DistintWordList.json'))
except:
    print("Reading File and Applying Porter Stemming...")
    for i in range(0, 56):
        List = SpeechFile(i)
        Temp_List = StemmingFunction(List)
        DistintWordList.extend(Temp_List)
        MergeList.append(Temp_List)
    # -------------------------
    # Distinct Words List -----
    DistintWordList = list(dict.fromkeys(DistintWordList))

    with open('MergeList.json', 'w') as f:
        json.dump(MergeList, f)
        f.close()

    with open('DistintWordList.json', 'w') as f:
        json.dump(DistintWordList, f)
        f.close()

    # Time Taken to Stemmed the Document ----
    stop1 = timeit.default_timer()
    Stem_Time = stop1 - start1
    print('Time Required to Stem all Documents: ', Stem_Time)
# ---------------------------------------


# Building Inverted Index ---------------------------
def BuildInvertedIndex():
    # Timer of Inverted List of Document --------
    start = timeit.default_timer()
    inverted = {}
    for i in range(0, len(DistintWordList)):
        inverted[DistintWordList[i]] = []

    for i in range(0, len(MergeList)):
        for k in range(0, len(DistintWordList)):
            for j in range(0, len(MergeList[i])):
                if DistintWordList[k] == MergeList[i][j]:
                    word = DistintWordList[k]
                    docID = i
                    inverted[str(word)].append(docID)

    for i in range(0, len(DistintWordList)):
        TempList = inverted.get(DistintWordList[i])
        TempList = list(dict.fromkeys(TempList))
        inverted[DistintWordList[i]] = TempList

    j = json.dumps(inverted)
    with open("DocumentRecords.json", 'w') as f:
        f.write(j)
        f.close()

    # Time Taken to Create Inverted Index ----
    stop = timeit.default_timer()
    time2 = stop - start
    print('Time Required to Build Inverted Index and Saving Data: ', time2)
    return inverted


# Retrieve Data from json file
def RetrieveDataFromJsonFile():
    try:
        dictonary = json.load(open('DocumentRecords.json'))
        return dictonary
    except:
        print("Building Dictonary Indexes...")
        dictonary = BuildInvertedIndex()
        return dictonary
# ----------------------------------------


# Find Word in the List0 - 55 ------------
def list00(word, j, listInfo):
    for i in range(0, len(listInfo)):
        try:
            if listInfo[i] == word[j]:
                return 1;
        except IndexError:
            x = 1
    return -1


# Intersection of List
def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


# For Single Word Boolean
def SingleWordBoolean(newWord, temp, countWord):
    temp = ''
    documentList = []
    for i in range(0, len(MergeList)):
        temp = list00(newWord, countWord - 1, MergeList[i])
        if temp != -1:
            documentList.append(i)
        temp = ''
    return documentList


# Dealing with Single Word Query
def SingleWordQuery(word):
    countWord = len(word)
    newWord = ''
    temp = ''
    newWord = StemmingFunction(word)
    return SingleWordBoolean(newWord, temp, countWord)


# Dealing with two word with operator in middle
def TwoWordQuery(w1):
    countWord = len(w1)
    documentList1 = []
    documentList2 = []
    newDocumentList = []
    temp = ''
    newWord = StemmingFunction(w1)
    if w1[1] == 'or':
        documentList1 = SingleWordBoolean(newWord, temp, countWord - 2)
        documentList2 = SingleWordBoolean(newWord, temp, countWord)

        newDocumentList.extend(documentList1)
        newDocumentList.extend(documentList2)
        return list(dict.fromkeys(newDocumentList))
    else:
        documentList1 = SingleWordBoolean(newWord, temp, countWord - 2)
        documentList2 = SingleWordBoolean(newWord, temp, countWord - 1)
        return intersection(documentList1, documentList2)


def CheckInDocument(w1, countWord):
    documentList = []
    newDocumentList = []
    documentList1 = []
    documentList2 = []
    documentList3 = []
    newWord = ''
    temp = ''
    # Single Word Query with no Operator
    if countWord == 1:
        documentList.clear()
        documentList = SingleWordQuery(w1)
    # Single Word Query with NOT Operator
    elif countWord == 2 and w1[0] == 'not':
        documentList.clear()
        newDocumentList.clear()
        documentList = SingleWordQuery(w1)
        for i in range(0, 56):
            try:
                documentList.remove(i)
            except ValueError:
                newDocumentList.append(i)
        documentList.extend(newDocumentList)
    # Two words with Middle Operator
    elif countWord == 3 and (w1[1] == 'and' or w1[1] == 'or'):
        documentList.clear()
        newDocumentList.clear()
        documentList = TwoWordQuery(w1)
        documentList.sort()
    # Three words simple query
    elif countWord == 5 and ((w1[1] == 'and' and w1[3] == 'and') or (w1[1] == 'or' and w1[3] == 'or')):
        newDocumentList.clear()
        documentList.clear()
        newWord = StemmingFunction(w1)
        if w1[1] == 'or':
            documentList1 = SingleWordBoolean(newWord, temp, countWord - 4)
            documentList2 = SingleWordBoolean(newWord, temp, countWord - 2)
            documentList3 = SingleWordBoolean(newWord, temp, countWord)
            newDocumentList = documentList1 + documentList2 + documentList3
            documentList = list(dict.fromkeys(newDocumentList))
        else:
            documentList1 = SingleWordBoolean(newWord, temp, countWord - 4)
            documentList2 = SingleWordBoolean(newWord, temp, countWord - 3)
            documentList3 = SingleWordBoolean(newWord, temp, countWord - 2)
            temp = ''
            temp = intersection(documentList1, documentList2)
            documentList = intersection(temp, documentList3)
        documentList.sort()
    # Complex Queries t1 or ( t2 and t3 )
    elif countWord == 7 and (w1[2] == '(' and w1[6] == ')'):
        newDocumentList.clear()
        documentList.clear()
        tempWord2 = []
        tempWord = [w1[3], w1[4], w1[5]]
        newWord1 = StemmingFunction(tempWord)
        if w1[4] == 'or':
            documentList1 = SingleWordBoolean(newWord1, temp, len(tempWord) - 2)
            documentList2 = SingleWordBoolean(newWord1, temp, len(tempWord))
            newDocumentList = documentList1 + documentList2
            tempWord2 = list(dict.fromkeys(newDocumentList))
        else:
            documentList1 = SingleWordBoolean(newWord1, temp, len(tempWord) - 1)
            documentList2 = SingleWordBoolean(newWord1, temp, len(tempWord) - 2)
            tempWord2 = intersection(documentList1, documentList2)
        tempWord2.sort()
        newDocumentList.clear()
        tempWord.clear()

        tempWord = [w1[0]]
        newWord1 = StemmingFunction(tempWord)
        if w1[1] == 'or':
            documentList3 = SingleWordBoolean(tempWord, temp, len(tempWord))
            newDocumentList.clear()
            newDocumentList = documentList3 + tempWord2
            documentList = list(dict.fromkeys(newDocumentList))
        else:
            documentList3 = SingleWordBoolean(tempWord, temp, len(tempWord))
            newDocumentList.clear()
            documentList = intersection(documentList3, tempWord2)
        documentList.sort()
    # Complex Queries t1 or ( t2 and t3 and t3 )
    elif countWord == 9 and (w1[2] == '(' and w1[8] == ')') and ((w1[4] == 'and' and w1[6] == 'and') or (w1[4] == 'or' and w1[6] == 'or')):
        newDocumentList.clear()
        documentList.clear()
        tempp = []
        tempWord = [w1[3], w1[4], w1[5], w1[6], w1[7]]
        newWord1 = StemmingFunction(tempWord)

        if tempWord[1] == 'or':
            documentList1 = SingleWordBoolean(newWord1, temp, len(tempWord) - 4)
            documentList2 = SingleWordBoolean(newWord1, temp, len(tempWord) - 2)
            documentList3 = SingleWordBoolean(newWord1, temp, len(tempWord))
            tempp = documentList1 + documentList2 + documentList3
            newDocumentList = list(dict.fromkeys(tempp))
        else:
            documentList1 = SingleWordBoolean(newWord1, temp, len(tempWord) - 2)
            documentList2 = SingleWordBoolean(newWord1, temp, len(tempWord) - 4)
            documentList3 = SingleWordBoolean(newWord1, temp, len(tempWord))
            tempp = intersection(documentList1, documentList2)
            newDocumentList = intersection(tempp, documentList3)
        documentList3.clear()
        tempWord.clear()
        newWord1.clear()
        tempWord = [w1[0]]
        newWord1 = StemmingFunction(tempWord)
        documentList3 = SingleWordBoolean(newWord1, temp, len(newWord1))
        tempp.clear()
        if w1[1] == 'or':
            tempp = documentList3 + newDocumentList
            documentList = list(dict.fromkeys(tempp))
        else:
            documentList = intersection(documentList3, newDocumentList)
        documentList.sort()
    # Complex Queries not ( t1 and t2 )
    elif countWord == 6 and (w1[1] == '(' and w1[5] == ')') and w1[0] == 'not':
        newDocumentList.clear()
        documentList.clear()
        tempWord2 = []
        tempWord = [w1[2], w1[3], w1[4]]
        newWord1 = StemmingFunction(tempWord)

        if tempWord[1] == 'or':
            documentList1 = SingleWordBoolean(newWord1, temp, len(tempWord) - 2)
            documentList2 = SingleWordBoolean(newWord1, temp, len(tempWord))
            newDocumentList = documentList1 + documentList2
            tempWord2 = list(dict.fromkeys(newDocumentList))
        else:
            documentList1 = SingleWordBoolean(newWord1, temp, len(tempWord) - 1)
            documentList2 = SingleWordBoolean(newWord1, temp, len(tempWord) - 2)
            tempWord2 = intersection(documentList1, documentList2)
        for i in range(0, 56):
            try:
                tempWord2.remove(i)
            except ValueError:
                documentList.append(i)
    # Complex Queries not ( t1 and t2 and t3 )
    elif countWord == 8 and (w1[1] == '(' and w1[7] == ')') and w1[0] == 'not' and ((w1[3] == 'and' and w1[5] == 'and') or (w1[3] == 'or' and w1[5] == 'or')):
        documentList.clear()
        newDocumentList.clear()
        tempWord2 = []
        tempWord = [w1[2], w1[3], w1[4], w1[5], w1[6]]
        newWord = StemmingFunction(tempWord)

        newDocumentList.clear()
        if w1[3] == 'or':
            documentList1 = SingleWordBoolean(newWord, temp, len(tempWord) - 4)
            documentList2 = SingleWordBoolean(newWord, temp, len(tempWord) - 2)
            documentList3 = SingleWordBoolean(newWord, temp, len(tempWord))
            tempWord2 = documentList1 + documentList2 + documentList3
            newDocumentList = list(dict.fromkeys(tempWord2))
        else:
            documentList1 = SingleWordBoolean(newWord, temp, len(tempWord) - 2)
            documentList2 = SingleWordBoolean(newWord, temp, len(tempWord) - 1)
            documentList3 = SingleWordBoolean(newWord, temp, len(tempWord))
            temp = ''
            temp = intersection(documentList1, documentList2)
            newDocumentList = intersection(temp, documentList3)
        for i in range(0, 56):
            try:
                newDocumentList.remove(i)
            except ValueError:
                documentList.append(i)
    # Bi-Word Queries
    elif countWord == 2:
        newWord = StemmingFunction(w1)
        List = []
        for i in range(0, len(MergeList)):
            for j in range(0, len(MergeList[i])):
                if (MergeList[i][j] == newWord[0]) and (MergeList[i][j+1] == newWord[1]):
                    List.append(i)
        List = list(dict.fromkeys(List))
        documentList = List
    # Bi-Word with /t (space count)
    elif countWord == 3:
        word = w1
        word[2] = word[2].replace('/', '/ ').split()
        newWord = [word[2][0], word[2][1]]
        word = [word[0], word[1]]
        newWord1 = StemmingFunction(word)
        if newWord[0] == '/':
            List = []
            for i in range(0, len(MergeList)):
                for j in range(0, len(MergeList[i])):
                    gap = int(newWord[1])
                    if (MergeList[i][j] == newWord1[0]) and (MergeList[i][j + gap + 1] == newWord1[1]):
                        List.append(i)
            List = list(dict.fromkeys(List))
            documentList = List
        else:
            errorHandle = True
    else:
        print('Invalid Arg')

    return documentList


# -------------------------------------------
# Building Inverted index from scratch
# inverted = BuildInvertedIndex()
# Loading Inverted index from json file
inverted = RetrieveDataFromJsonFile()
# --------------------------------------------


def OnSearchButtonClicks(QueryText):
    word = []
    temp = ''
    QueryText += " ."
    length = len(QueryText)
    for i in range(0, length):
        if QueryText[i] != ' ':
            temp += QueryText[i]
        else:
            word.append(temp)
            temp = ''

    for i in range(0, len(word)):
        word[i] = word[i].lower()

    try:
        countWord = len(word)
        docoumentList = CheckInDocument(word, countWord)
    except IndexError:
        docoumentList = []

    LengthofDocuments = len(docoumentList)
    word1 = []
    word2 = []
    if LengthofDocuments > 28:
        for i in range(0, 28):
            word1.append(docoumentList[i])
        for i in range(28, LengthofDocuments):
            word2.append(docoumentList[i])
        DocumentsFound1.set(word1)
        DocumentsFound2.set(word2)
    else:
        if LengthofDocuments == 0:
            DocumentsFound1.set('No Document Found...!')
            DocumentsFound2.set('...')
            print('no doc found')
        else:
            DocumentsFound1.set(docoumentList)
            DocumentsFound2.set('')

    print(docoumentList)


# Working on gui ----------------------------
window = gui.Tk()
window.title('Information Retrieval Assignment no.01')
window.geometry('650x350+150+50')
window.configure(background='black')
window.resizable(width=FALSE, height=FALSE)
window.winfo_toplevel()

QueryText_Label0 = gui.Label(window, text='Follow the alignment example: running and ( jump or kick )')
QueryText_Label0.config(fg='white', background='black')
QueryText_Label0.config(font="Courier 10")
QueryText_Label0.pack(side=BOTTOM, anchor=NW)

QueryText_Label0 = gui.Label(window, text='')
QueryText_Label0.config(fg='black', background='black')
QueryText_Label0.config(font="Courier 10")
QueryText_Label0.pack(side=TOP, anchor=NW)

Heading = gui.Label(window, text="Search Engine", fg='white')
Heading.configure(background='black')
Heading.config(font="Verdana 45")
Heading.pack()

textField = StringVar()
QueryBox = gui.Text(window, width=37, height=1, bd=7)
QueryBox.config(font=("Courier", 20))
QueryBox.pack()


def retrieve_input():
    input = QueryBox.get("1.0", 'end-1c')
    QueryText.set(input)
    if input == '':
        QueryText.set('[]')
        DocumentsFound1.set("[Document Found]")
        DocumentsFound1.set("...")
    return input


SearchBTN = gui.Button(window, text='Search Me...!', command=lambda: OnSearchButtonClicks(retrieve_input()))
SearchBTN.config(width=20, height=1, bd=5)
SearchBTN.config(padx=10, pady=5)
SearchBTN.config(fg='#0066cc')
SearchBTN.pack(pady=7)
SearchBTN.config(font='Verdana')

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

window.mainloop()

# End of the Program -----------------------------------------------------
