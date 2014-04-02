#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
reasonable_words.py
Author: yupbank
Email:  yupbank@gmail.com

Created on
2014-04-02
'''
'total = alpha*freedom+beta*combination + (1-alpha-beta)*seq'

def read_file(file_name):
    with open(file_name) as f:
        for line in f:
            line = line.strip().split()
            word, value = line[0], float(line[1])
            yield word, value

def main():
    alpha, beta = 0.33, 0.33
    total = dict()
    for word, value in read_file('new_freedom'):
        total[word] = alpha*value
    for word, value in read_file('new_combination'):
        total[word] += beta*value
    for word, value in read_file('new_sep_freq'):
        total[word] += (1-alpha-beta)*value
    total = [[i, j] for i,j in total.iteritems()]
    total.sort(key=lambda x: x[1], reverse=True)
    with open('new_reasonable_word', 'w') as f:
        for i, j in total:
            print >>f,  i, j

if __name__ == '__main__':
    main()
