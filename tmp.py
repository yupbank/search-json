#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
tmp.py
Author: yupbank
Email:  yupbank@gmail.com

Created on
2014-03-19
'''
from orm import MyTime, database
import time

def main():
    with database.transaction():
        for i in MyTime.select():
            print i.id
            stamp_format='%Y-%m-%dT%H:%M:%S'
            t_struct = time.strptime(i.stamp[:-6], stamp_format)
            i.unix_stamp = time.mktime(t_struct)
            i.save()

if __name__ == '__main__':
    main()
