#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
reasonable_words.py
Author: yupbank
Email:  yupbank@gmail.com

Created on
2014-04-02
'''
'total = thta*freedom+(1-thta)*combination'

def read_file(file_name):
    with open(file_name) as f:
        for line in f:
            line = line.strip().split()
            word, value = line[0], float(line[1])
            yield word, value

def main():
    thta = 0.6
    total = dict()
    for word, value in read_file('combination'):
        total[word] = (1-thta)*value
    for word, value in read_file('freedom'):
        total[word] += thta*value/3
    total = [[i, j] for i,j in total.iteritems()]
    total.sort(key=lambda x: x[1], reverse=True)
    for i, j in total:
        print i, j

if __name__ == '__main__':
    main()
