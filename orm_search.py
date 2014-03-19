#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
orm_search.py
Author: yupbank
Email:  yupbank@gmail.com

Created on
2014-03-18
'''
from collections import defaultdict
from orm import *
from util import get_lat_lng_range, get_distance_hav_by_lat_lng

def activit_poi_count():
    res = dict()
    ac = ActivityPoi.raw('select distinct(activity_id) as ac, count(distinct(poi_id)) as ac_count from activitypoi group by activity_id')
    for a in ac:
        res[a.ac] =  a.ac_count
    return res


def poi_activity_count():
    res = dict()
    ac = ActivityPoi.raw('select distinct(poi_id) as pc, count(distinct(activity_id)) as pc_count from activitypoi group by poi_id')
    for a in ac:
        res[a.pc] =  a.pc_count
    return res

            
APC = activit_poi_count()
PAC = poi_activity_count()

def find_by_location(lat, lng, radius=5, limit=10, offset=0):
    lat1, lat2, lng1, lng2 = get_lat_lng_range(lat, lng, radius)
    activity_poi = ActivityPoi.select(ActivityPoi, Poi).join(Poi).where(Poi.lat >= lat1 , Poi.lat <= lat2 , Poi.lng >= lng1 , Poi.lng <= lng2).group_by(Poi)
    _ = []
    for i in activity_poi:
        distance = get_distance_hav_by_lat_lng(lat, lng, i.poi.lat, i.poi.lng)
        _.append([i.activity.name, i.poi.name, i.poi.lat, i.poi.lng, distance, APC[i.activity.id]])
    _.sort(key=lambda x:x[-1], reverse=True)
    return _[offset:offset+limit]


def find_by_poi_type(type, limit=10, offset=0):
    activity_time = ActivityPoi.select(ActivityTime, Poi).join(Poi).where(Poi.type == type)
    activity_count = defaultdict(int)
    for i in  activity_time:
        activity_count[i.activity.name] += 1
    res = sorted([[i, j] for i,j in activity_count.iteritems()], key=lambda x: x[1], reverse=True)
    return res[offset:offset+limit]


def find_by_hour(hour, limit=10, offset=0):
    activity_time = ActivityTime.select(ActivityTime, MyTime).join(MyTime).where(MyTime.hour == hour)
    activity_count = defaultdict(int)
    for i in  activity_time:
        activity_count[i.activity.name] += 1
    res = sorted([[i, j] for i,j in activity_count.iteritems()], key=lambda x: x[1], reverse=True)
    return res[offset:offset+limit]

def find_by_week(week, limit=10, offset=0):
    activity_time = ActivityTime.select(ActivityTime, MyTime).join(MyTime).where(MyTime.week == week)
    activity_count = defaultdict(int)
    for i in  activity_time:
        activity_count[i.activity.name] += 1
    res = sorted([[i, j] for i,j in activity_count.iteritems()], key=lambda x: x[1], reverse=True)
    return res[offset:offset+limit]

def find_by_month(month, limit=10, offset=0):
    activity_time = ActivityTime.select(ActivityTime, MyTime).join(MyTime).where(MyTime.month == month)
    activity_count = defaultdict(int)
    for i in  activity_time:
        activity_count[i.activity.name] += 1
    res = sorted([[i, j] for i,j in activity_count.iteritems()], key=lambda x: x[1], reverse=True)
    return res[offset:offset+limit]


def main():
    for i in find_by_location(23.01646 ,113.744537, offset=0):
        for j in i:
            print j,
        print


if __name__ == '__main__':
    #main()
    for i, j in find_by_month(5)[:10]:
        print i, j
