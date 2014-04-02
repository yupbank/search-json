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
word_to_user = defaultdict(set)
user_word_count = defaultdict(lambda : defaultdict(int)) 
word_freq = defaultdict(int)
document_freq = defaultdict(int)
word_tf_idf = defaultdict(float)
word_by_length = defaultdict(set)
term_probrablity = {}
term_condition_probrablity = {}

total_document = 0
total_word = 0
total_user = 0
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
    for i in xrange(1, iter_len+1):
        for j in xrange(0, word_len+1):
            if len(words[j:j+i])==i:
                yield words[j:j+i]

trie_building = build_trie(tire)
inverse_tire_building = build_trie(inverse_tire)

def document_to_word(document):
    for i in document:
        for word in generate_by_cut(i): 
            trie_building(word)
            inverse_tire_building(word[::-1])
            yield word

def count_tf_idf_uf(user, document):
    global total_document
    total_document += 1
    in_document_words = set()
    for word in document_to_word(document):
        global total_word
        word_by_length[len(word)].add(word)
        total_word += 1
        word_to_user[word].add(user)
        user_word_count[user][word] += 1
        word_freq[word] += 1
        in_document_words.add(word)

    for word in in_document_words:
        document_freq[word] += 1

def entropy(counts):
    total = float(sum(counts))
    result = 0
    for i in counts:
        proba = i/total
        result = result - proba * log(proba)
    return result

MAX = 10000000000


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
    scope = atree.keys()
    counts = filter(lambda x: x, map(lambda x: word_freq[(word+x)[::-1]], scope))
    
    return entropy(counts)

def main(): 
    potential_words = defaultdict(int) 
    assets = set()
    print 'start reading words....'
    with open('words') as f:
        for line in f:
            line = line.decode('U8')
            line = line.strip().split(' ')
            user, document = line[0], line[1:]
            count_tf_idf_uf(user, document)
    print 'finish reading words....'
    global total_user
    total_user = len(user_word_count.keys())
    word_combination = {}
    word_freedom = {}


    print 'start aggregating results....'

    for word in word_to_user:
        if len(word) > 1:
            word_combination[word] = min(word_freq[word]/float(word_freq[word[:-1]]*word_freq[word[-1]]), word_freq[word]/float(word_freq[word[0]]*word_freq[word[1:]]))
            word_freedom[word] = min(calculate_entorpy_right(word), calculate_entropy_left(word))
        tf = word_freq[word]/float(total_word)
        idf = log(float(total_document)/document_freq[word])
        word_tf_idf[word] = tf*idf

    print 'finish aggregating results....'
    top = [ [i, j] for i,j in word_tf_idf.iteritems()]
    top.sort(key=lambda x:x[1], reverse=True)
    with open('tf_idf', 'w') as f:
        for i, j in top:
            print >>f, i.encode('U8'), j
    
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
