"""
Caesar cypher module
usage: python caesar.py [option]
    options:
        buildVocabulary [k]
            k - optional int to specify caesar shift, else generates random dict

        encrypt text_file_name vocabulary_file_name

        decrypt text_file_name vocabulary_file_name
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
    return decrypt(crypt, *trans)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print __doc__
        exit(0)

    if sys.argv[1] == "buildVocabulary":
        with open(sys.argv[2], "w") as f:
            if len(sys.argv) > 3:
                f.write(buildVocabulary(k=int(sys.argv[3])))
            else:
                f.write(buildVocabulary())

    if sys.argv[1] == "encrypt":
        result = encrypt(*readFiles(sys.argv[2], sys.argv[3]))
        open(sys.argv[2] + ".encrypted.txt", "w").write(result)

    if sys.argv[1] == "decrypt":
        result = decrypt(*readFiles(sys.argv[2], sys.argv[3]))
        filename = sys.argv[2]
        if filename.endswith(".encrypted.txt"):
            filename = filename.replace(".encrypted.txt", ".decrypted.txt")
        else:
            filename += ".decrypted.txt"
        open(filename, "w").write(result)

    if sys.argv[1] == "freq":
        crypt = open(sys.argv[2], "r").read().lower()
        text = open(sys.argv[3], "r").read().lower()
        result = decryptFrequencyMethod(crypt, text)
        filename = sys.argv[2]
        if filename.endswith(".encrypted.txt"):
            filename = filename.replace(".encrypted.txt", ".freq.txt")
        else:
            filename += ".freq.txt"
        open(filename, "w").write(result)