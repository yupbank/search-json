#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
util.py
Author: yupbank
Email:  yupbank@gmail.com

Created on
2014-03-13
'''
from math import sin, asin, cos, radians, fabs, sqrt, degrees
import time as time_module

EARTH_RADIUS = 6371.0


def stamp_to_hour_week_month(stamp, stamp_format='%Y-%m-%dT%H:%M:%S'):
    t_struct = time_module.strptime(stamp, stamp_format)
    return t_struct.tm_hour, t_struct.tm_wday, t_struct.tm_mon


def hav(theta):
    s = sin(theta / 2)
    return s*s

def get_distance_hav_by_lat_lng(lat0, lng0, lat1, lng1):
    lat0, lng0, lat1, lng1 = map(float, [lat0, lng0, lat1, lng1])
    lat0, lng0, lat1, lng1 = map(radians, [lat0, lng0, lat1, lng1])

    dlng = fabs(lng0 - lng1)
    dlat = fabs(lat0 - lat1)
    h = hav(dlat) + cos(lat0) * cos(lat1) * hav(dlng)
    distance = 2 * EARTH_RADIUS * asin(sqrt(h))
    
    return distance


def get_lat_lng_range(lat0, lng0, distance=1.0):
    lat0, lng0 = map(float, [lat0, lng0])

    dlng = distance/(30.887*cos(lat0))
    #dlng = 2 * asin(sin(distance / (2 * EARTH_RADIUS)) / cos(lat0))
    #dlng = degrees(dlng)

    dlat = distance / EARTH_RADIUS
    dlat = degrees(dlat)
    
    lat1 = lat0 - dlat
    lat2 = lat0 + dlat

    lng1 = lng0 - dlng
    lng2 = lng0 + dlng
    
    if lat1 > lat2:
        a = lat2
        lat2 = lat1
        lat1 = a
    if lng1 > lng2:
        a = lng2
        lng2 = lng1
        lng1 = a

    return lat1, lat2, lng1, lng2

