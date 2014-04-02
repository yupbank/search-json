#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
grep_words.py
Author: yupbank
Email:  yupbank@gmail.com

Created on
2014-03-28
'''
import sys
from collections import defaultdict
from math import log

default_cut_length = 4
word_freq = defaultdict(int)
total_word = 0
tire = {}
inverse_tire = {}


def build_trie(atree):
    def _(words):
        pointer = atree
        for word in words:
            if word not in pointer:
                pointer[word] = {}
            pointer = pointer[word]
        pointer[''] = ''
    return _


def generate_by_cut(words, cut=default_cut_length):
    word_len = len(words)
    iter_len = cut if word_len > cut else word_len
    for i in xrange(1, iter_len + 1):
        for j in xrange(0, word_len + 1):
            if len(words[j:j + i])==i:
                yield words[j:j+i]

trie_building = build_trie(tire)
inverse_tire_building = build_trie(inverse_tire)

def document_to_word(document):
    for i in document:
        i  = i.strip()
        for word in generate_by_cut(i): 
            trie_building(word)
            inverse_tire_building(word[::-1])
            yield word

def count_freq(document):
    for word in document_to_word(document):
        global total_word
        total_word += 1
        word_freq[word] += 1


def entropy(counts):
    total = float(sum(counts))
    result = 0
    for i in counts:
        proba = i/total
        result = result - proba * log(proba)
    return result


def calculate_entorpy_right(word):
    global tire
    atree = tire
    for i in word:
        if i in atree:
            atree = atree[i]
    scope = atree.keys()
    counts = filter( lambda x: x, map(lambda x: word_freq[word+x], scope) )
    return entropy(counts)

def calculate_entropy_left(word):
    global inverse_tire 
    prefix = word[::-1]
    atree = inverse_tire
    for i in prefix:
        if i in atree:
            atree = atree[i]
    scope = filter(lambda x: x, atree.keys())
    counts = map(lambda x: word_freq[(prefix+x)[::-1]], scope)
    
    return entropy(counts)

def main(): 
    print 'start reading words....'
    with open('words') as f:
        for n, line in enumerate(f):
            line = line.decode('U8')
            line = line.strip().split(' ')
            user, document = line[0], line[1:]
            count_freq(document)
    print 'finish reading words....'
    word_combination = {}
    word_freedom = {}

    print 'start aggregating results....'
    words = word_freq.keys()
    for word in words:
        if len(word) > 1:
            word_combination[word] = min(word_freq[word]/float(word_freq[word[:-1]]*word_freq[word[-1]]), word_freq[word]/float(word_freq[word[0]]*word_freq[word[1:]]))
            word_freedom[word] = min(calculate_entorpy_right(word), calculate_entropy_left(word))
    
    print 'writing....'
    top = [ [i, j] for i,j in word_combination.iteritems()]
    top.sort(key=lambda x:x[1], reverse=True)
    with open('combination', 'w') as f:
        for i, j in top:
            print >>f, i.encode('U8'), j

    print 'writing....'
    top = [ [i, j] for i,j in word_freedom.iteritems()]
    top.sort(key=lambda x:x[1], reverse=True)
    with open('freedom', 'w') as f:
        for i, j in top:
            print >>f, i.encode('U8'), j


if __name__ == '__main__':
    main()
