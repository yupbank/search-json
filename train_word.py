#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
train_word.py
Author: yupbank
Email:  yupbank@gmail.com

Created on
2014-03-28
'''
from orm import *
import re

hashtag = re.compile('#.+#')
icon = re.compile('\[.+\]')
at_people = re.compile('\@[^ ]+')
simple_url = re.compile(r'http://t.cn/\[?\w+', re.IGNORECASE)


def main():
    text = set()
    for line in Item.select():
        if line.user:
            text.add((line.origin_text, line.user))
    for line, user in text:
        res = simple_url.findall(line)
        a = line
        for i in res:
            a = a.replace(i, '')
        res = hashtag.findall(line)
        tag = hashtag.findall(line)[0] if res else ''
        for i in res:
            a = a.replace(i, '')
        res = icon.findall(line)
        for i in res:
            a = a.replace(i, '')
        res = at_people.findall(line)
        people = at_people.findall(line)[0] if res else ''
        for i in res:
            a = a.replace(i, '')
        #print at_people.findall(line)
        a = a.replace(u'我在这里：', '')
        a = a.replace(u'我在这里:', '')
        a = a.replace(u'这里:', '')
        a = a.replace(u'我在', '')
        a = a.replace(u'//', '')
        a = a.replace(u'I\'m at', '')
        a = ''.join(map(lambda x: x if ord(x) >= 0x4e00 and ord(x) <= 0x9fa5 or x.isdigit() else ' ', a))
        while '  ' in a:
            a = a.replace('  ', ' ')
        a = a.strip()
        if a:
            print user, a.encode('U8')
        else:
            continue

if __name__ == '__main__':
    main()
