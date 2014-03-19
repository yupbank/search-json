#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
orm_search.py
Author: yupbank
Email:  yupbank@gmail.com

Created on
2014-03-18
'''
from orm import *
import json
import time as time_module

def select_existing_activies():
    res = dict()
    for i in Activity.select():
        res[i.name] = i.id
    return res

def select_all_time():
    res = dict()
    for i in MyTime.select():
        res[i.stamp] = i.id
    return res

def stamp_to_hour_week_month(stamp):
    stamp = stamp[:-6]
    stamp_format = '%Y-%m-%dT%H:%M:%S'
    t_struct = time_module.strptime(stamp, stamp_format)
    return t_struct.tm_hour, t_struct.tm_wday, t_struct.tm_mon

def load_new_activies(file_name):
    existing_activities = select_existing_activies()
    with open(file_name) as f:
        activities = set()
        for line in f:
            data = json.loads(line)
            name = data['Name'].strip()
            if name and name not in existing_activities:
                activities.add(name)
    activities = [dict(name=i) for i in activities]

    with database.transaction():
        for data_dict in activities:
            Activity.create(**data_dict)


def load_data(file_name):
    load_new_activies(file_name)
    existing_activities = select_existing_activies()
    with open(file_name) as f:
        activities_item = set()
        activities_poi = set()
        pois = dict()
        times = set()
        items = set()
        for line in f:
            data = json.loads(line)
            name = data['Name'].strip()
            poi = data['POI']
            poi_id = poi.get('Id')
            if name and poi_id:
                poi = data['POI']
                lat, lng = poi.get('lat'), poi.get('lng')
                poi_type = poi.get('Type')
                poi_city = poi.get('City')
                poi_name = poi.get('Name')
                poi_id = poi.get('Id')
                time_stamp = data['Timestamp']
                item_id = data['Entity']
                activities_item.add((existing_activities[name], item_id))
                activities_poi.add((existing_activities[name], poi_id))
                user = data['User']
                origin_text = data['OriginalText']
                pois[poi_id] = [poi_name, poi_city, poi_type, lat, lng]
                times.add((existing_activities[name], time_stamp))
                items.add((item_id, name, user, origin_text))
        _ = []
        for i in pois:
            _.append(dict(id=i, name=pois[i][0], city=pois[i][1], type=pois[i][2], lat=pois[i][3], lng=pois[i][4]))
        pois = _ 
        with database.transaction():
            for poi in pois:
                Poi.create(**poi)
            for t in times:
                hour, week, month = stamp_to_hour_week_month(t[1])
                MyTime.create(stamp=t[1], hour=hour, week=week, month=month)
            for i in items:
                Item.create(id=i[0], name=i[1], user=i[2], origin_text=i[3])
        time_to_id = select_all_time() 
        with database.transaction():
            for t in times:
                ActivityTime.create(activity=t[0], mytime=time_to_id[t[1]])
            for i in activities_item:
                ActivityItem.create(activity=i[0], item=i[1])
            for p in activities_poi:
                ActivityPoi.create(activity=p[0], poi=p[1])

        #insert_massive('poi(id, name, city, type, lat, lng)',  pois, 6)
        #insert_massive('times(activity_id, stamp)',  times, 2)
        #insert_massive('item(id, name, user, origin_text)',  items, 4)
        #insert_massive('activity_item(activity_id, item_id)',  activities_item, 2)
        #insert_massive('activity_poi(activity_id, poi_id)',  activities_poi, 2)


def main():
    load_data('weibo.med')

if __name__ == '__main__':
    main()
