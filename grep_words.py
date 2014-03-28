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



def main(): 
    potential_words = defaultdict(int) 
    assets = set()
    with open('words') as f:
        for line in f:
            line = line.decode('U8')
            line = line.strip().split(' ')
            for conponent in line:
                if len(conponent) <= 3:
                    potential_words[conponent] += 1
                else:
                    assets.add(conponent)
    b = [[i, j] for i, j in potential_words.iteritems()]
    b.sort(key=lambda x: x[1])
    for i, j in b:
        print i, j 


if __name__ == '__main__':
    main()
