#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
orm.py
Author: yupbank
Email:  yupbank@gmail.com

Created on
2014-03-18
'''
from peewee import *

database = SqliteDatabase('orm_data.db')


class Activity(Model):
    name = CharField()

    class Meta:
        database = database


class Item(Model):
    name = CharField()
    user = CharField()
    id = CharField(primary_key=True)
    origin_text = TextField(null=True)

    class Meta:
        database = database


class MyTime(Model):
    stamp = CharField()
    week = IntegerField()
    month = IntegerField()
    hour = IntegerField()

    class Meta:
        database = database


class Poi(Model):
    id = CharField(primary_key=True)
    lat = FloatField()
    lng = FloatField()
    name = CharField()
    city = CharField()
    type = CharField()
    
    class Meta:
        database = database


class ActivityPoi(Model):
    activity = ForeignKeyField(Activity)
    poi = ForeignKeyField(Poi)

    class Meta:
        database = database

class ActivityItem(Model):
    activity = ForeignKeyField(Activity)
    item = ForeignKeyField(Item)

    class Meta:
        database = database

class ActivityTime(Model):
    activity = ForeignKeyField(Activity)
    mytime = ForeignKeyField(MyTime)

    class Meta:
        database = database


if __name__ == "__main__":
    Poi.create_table()
    Activity.create_table()
    MyTime.create_table(True)
    Item.create_table()
    ActivityPoi.create_table()
    ActivityItem.create_table()
    ActivityTime.create_table()
