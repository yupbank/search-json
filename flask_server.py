#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
flask_server.py
Author: yupbank
Email:  yupbank@gmail.com

Created on
2014-03-18
'''
from flask import g, Flask, request
from orm_search import find_by_location, find_by_month, find_by_week, find_by_hour, find_by_location_and_time
import json

app = Flask(__name__)


@app.route('/location')
def search_by_location():
    lat = request.args.get('lat',None)
    lng = request.args.get('lng', None)
    radius = request.args.get('radius', 5)
    if not (lat and lng):
        return 'sorry'
    try:
        lat = float(lat)
        lng = float(lng)
    except Exception, e:
        return e

    res = find_by_location(lat, lng)
    return json.dumps(res)


@app.route('/hour')
def search_by_hour():
    hour = request.args.get('hour',None)
    if not hour:
        return 'sorry'
    try:
        hour = int(hour)
    except Exception, e:
        return e

    res = find_by_hour(hour)
    return json.dumps(res)


@app.route('/month')
def search_by_month():
    month = request.args.get('month',None)
    if not month:
        return 'sorry'
    try:
        month = int(month)
    except Exception, e:
        return e

    res = find_by_month(month)
    return json.dumps(res)


@app.route('/week')
def search_by_week():
    week = request.args.get('week',None)
    if not week:
        return 'sorry'
    try:
        week = int(week)
    except Exception, e:
        return e

    res = find_by_week(week)
    return json.dumps(res)

@app.route('/seach')
def search_by_time_and_location():
    timestamp = request.args.get('time', None)
    lat = request.args.get('lat', None)
    lng = request.args.get('lng', None)
    if not (lat and lng):
        return 'sorry'
    try:
        lat = float(lat)
        lng = float(lng)
    except Exception, e:
        return e

    res = find_by_location_and_time(lat, lng, timestamp)
    return json.dumps(res)

def main():
    app.run(host='0.0.0.0')

if __name__ == '__main__':
    main()
