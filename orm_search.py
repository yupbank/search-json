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
from util import get_lat_lng_range, get_distance_hav_by_lat_lng, stamp_to_hour_week_month
import time


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

def find_by_location_and_time(lat, lng, time_stamp):
    hour, day, mon = stamp_to_hour_week_month(time_stamp)
    lat1, lat2, lng1, lng2 = get_lat_lng_range(lat, lng, 5)
    activity_poi = ActivityPoi.select(ActivityPoi, Poi).join(Poi).where(Poi.lat >= lat1 , Poi.lat <= lat2 , Poi.lng >= lng1 , Poi.lng <= lng2).limit(2000)
    res = defaultdict(set)
    for i in activity_poi:
        res[(i.activity.name, i.activity.id)].add((i.poi.name, i.poi.id, (i.poi.lat, i.poi.lng)))

    activity_time = ActivityTime.select(ActivityTime, MyTime).join(MyTime).where(MyTime.hour == hour).limit(2000)
    res_activity, res_poi = set(), set()
    for i in activity_time:
        if (i.activity.name, i.activity.id) in res:
            res_activity.add((i.activity.name, APC[i.activity.id]))
            for i in res[(i.activity.name, i.activity.id)]:
                res_poi.add((i[0], PAC[i[1]], i[2]))

    set_to_list = lambda x: [i for i in x]
    res_activity = set_to_list(res_activity)
    res_poi = set_to_list(res_poi)
    res_activity.sort(key=lambda x: x[1], reverse=True)
    res_poi.sort(key=lambda x: x[1], reverse=True)
    res_poi = map(lambda x: [ x[0], x[1], get_distance_hav_by_lat_lng(x[2][0], lat, x[2][1], lng)], res_poi[:50])
    return res_poi[:50], res_activity[:50]

def main():
    i, j = find_by_location_and_time(23.01646 ,113.744537, '2012-05-14T08:42:10')
    for x in i:
        print x[0], x[1],
    print '----------'
    for y in j:
        print y[0], y[1],
    print


if __name__ == '__main__':
    main()
