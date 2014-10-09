"""
Caesar cypher module
usage: python caesar.py [option]
    options:
        b [k]
            buildVocabulary
            k - optional int to specify caesar shift, else generates random dict

        e text_file_name vocabulary_file_name
            encrypt

        d text_file_name vocabulary_file_name
            decrypt

        f text_file_name vocabulary_file_name
            frequency decrypt
"""
__author__ = 'Maksim Golunko'

import string
import random
import sys
import re
import collections


def buildVocabulary(k=None):
    a = string.ascii_lowercase
    if k:
        b = a[k:] + a[:k]
    else:
        listA = list(a)
        random.shuffle(listA)
        b = ''.join(listA)
    return a + '\n' + b


def readFiles(textFile, dictFile):
    text = open(textFile, "r").read().lower()
    [a, b] = [x.rstrip() for x in open(dictFile, "r")]
    return text, a, b


def encrypt(text, a, b):
    class keydict(dict):
        def __missing__(self, key):
            return key

    trans = keydict(zip(a, b))
    result = ''.join([trans[x] for x in text])
    return result


def decrypt(crypt, a, b):
    trans = string.maketrans(b, a)
    result = crypt.translate(trans)
    return result


def buildFrequencyTable(text):
    t = re.sub(r"[^a-z]", "", text)
    length = len(text)
    counts = collections.defaultdict(int, collections.Counter(t))
    for s in string.ascii_lowercase:
        counts[s] = float(counts[s]) / length
    return counts


def getTransTable(crypt, text):
    cryptFreq = buildFrequencyTable(crypt)
    textFreq = buildFrequencyTable(text)
    cryptLetters = ''.join(sorted(cryptFreq, key=lambda c: cryptFreq[c]))
    textLetters = ''.join(sorted(textFreq, key=lambda c: textFreq[c]))
    return textLetters, cryptLetters


def decryptFrequencyMethod(crypt, text):
    trans = getTransTable(crypt, text)
    magic = '\n'.join([''.join(x) for x in zip(*sorted(zip(*trans)))]) #magic
    return decrypt(crypt, *trans), magic


def distance(w1, w2):
    d = 0
    diff = None
    for i in xrange(len(w1)):
        if w1[i] != w2[i]:
            d += 1
            diff = (w1[i], w2[i])
    return d, diff


def continueDecrypt(crypt, text):
    trans = getTransTable(crypt, text)
    decr = decrypt(crypt, *trans)
    start = 0
    finish = 100
    decryptedWords = re.sub(r"[^a-z\s]", "", decr).split()
    learnWords = re.sub(r"[^a-z\s]", "", text).split()
    timesUpdated = 0
    maxIndex = max(len(learnWords), len(learnWords))
    while True:
        decryptedWordsTrim = decryptedWords[start:finish]
        learnWordsTrim = learnWords[start:finish]

        count = collections.Counter()
        for wordDecr in decryptedWordsTrim:
            for wordLearn in learnWordsTrim:
                if len(wordDecr) == len(wordLearn):
                    dist = distance(wordDecr, wordLearn)
                    if dist[0] == 1:
                        count.update({dist[1]: 1})

        mc = count.most_common(3)
        if len(mc) < 3:
            break

        if mc[0][1] > (mc[1][1] + mc[2][1])*2:
            (a, b) = trans
            b = list(b)
            pos1 = b.index(mc[0][0][0])
            pos2 = b.index(mc[0][0][1])
            b[pos1] = mc[0][0][1]
            b[pos2] = mc[0][0][0]
            b = ''.join(b)
            trans = (a, b)
            decr = decrypt(crypt, *trans)
            decryptedWords = re.sub(r"[^a-z\s]", "", decr).split()
            timesUpdated += 1

        if finish == maxIndex:
            break
        else:
            start = finish
            finish = finish + 100 if finish + 100 < maxIndex else maxIndex

    print "timesUpdated", timesUpdated
    magic = '\n'.join([''.join(x) for x in zip(*sorted(zip(*trans)))])
    return decr, magic


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print __doc__
        exit(0)

    if sys.argv[1] == "b":
        with open(sys.argv[2], "w") as f:
            if len(sys.argv) > 3:
                f.write(buildVocabulary(k=int(sys.argv[3])))
            else:
                f.write(buildVocabulary())

    if sys.argv[1] == "e":
        result = encrypt(*readFiles(sys.argv[2], sys.argv[3]))
        open(sys.argv[2] + ".encrypted.txt", "w").write(result)

    if sys.argv[1] == "d":
        result = decrypt(*readFiles(sys.argv[2], sys.argv[3]))
        filename = sys.argv[2]
        if filename.endswith(".encrypted.txt"):
            filename = filename.replace(".encrypted.txt", ".decrypted.txt")
        else:
            filename += ".decrypted.txt"
        open(filename, "w").write(result)

    if sys.argv[1] == "f":
        crypt = open(sys.argv[2], "r").read().lower()
        text = open(sys.argv[3], "r").read().lower()
        result, trans = decryptFrequencyMethod(crypt, text)
        print trans
        filename = sys.argv[2]
        if filename.endswith(".encrypted.txt"):
            filename = filename.replace(".encrypted.txt", ".freq.txt")
        else:
            filename += ".freq.txt"
        open(filename, "w").write(result)

    if sys.argv[1] == "fc":
        crypt = open(sys.argv[2], "r").read().lower()
        text = open(sys.argv[3], "r").read().lower()
        result, trans = continueDecrypt(crypt, text)
        print trans
        filename = sys.argv[2]
        if filename.endswith(".encrypted.txt"):
            filename = filename.replace(".encrypted.txt", ".freqC.txt")
        else:
            filename += ".freqC.txt"
        open(filename, "w").write(result)