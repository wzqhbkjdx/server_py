#!/usr/bin/env python
# coding=utf-8

import time, uuid

from orm import Model, StringField, BooleanField, FloatField, TextField, IntegerField

def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)

class User(Model):
    __table__ = 'users'

    id = StringField(primary_key = True, default = next_id, ddl = 'varchar(50)')
    email = StringField(ddl='varchar(50)')
    passwd = StringField(ddl='varchar(50)')
    admin = BooleanField()
    name = StringField(ddl='varchar(50)')
    image = StringField(ddl = 'varchar(500)')
    created_at = FloatField(default=time.time)

    print('create user')

class Blog(Model):
    __table__ = 'blogs'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    user_id = StringField(ddl='varchar(50)')
    user_name = StringField(ddl = 'varchar(50)')
    user_image = StringField(ddl='varchar(500)')
    name = StringField(ddl='varchar(50)')
    summary = StringField(ddl='varchar(200)')
    content = TextField()
    created_at = FloatField(default = time.time)

class Comment(Model):
    __table__ = 'comments'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    blog_id = StringField(ddl='varchar(50)')
    user_id = StringField(ddl = 'varchar(50)')
    user_name = StringField(ddl = 'varchar(50)')
    user_image = StringField(ddl = 'varchar(500)')
    content = TextField()
    created_at = FloatField(default = time.time)

class Remain(Model):
    __table__='remain'
    
    idenf = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    num = StringField(ddl='varchar(50)')

class Task(Model):
    __table__ = 'tasks'

    idenf = StringField(primary_key=True, default=next_id, ddl='varchar(100)')
    task_name = StringField(ddl='varchar(100)')
    ip_repeat_days = IntegerField()

    level_2_days = IntegerField()
    level_2_percents = FloatField()

    level_3_days = IntegerField()
    level_3_percents = FloatField()

    level_4_days = IntegerField()
    level_4_percents = FloatField()

    level_5_days = IntegerField()
    level_5_percents = FloatField()

    level_6_days = IntegerField()
    level_6_percents = FloatField()

    level_7_days = IntegerField()
    level_7_percents = FloatField()

    level_8_days = IntegerField()
    level_8_percents = FloatField()

    new_limit = IntegerField()

class RemainTask(Model):
    __table__ = 'remain_table'
    idenf = StringField(primary_key=True, default=next_id, ddl='varchar(100)')
    id = IntegerField()
    create_time = StringField(ddl='varchar(50)')
    update_time = StringField(ddl='varchar(50)')
    status = IntegerField() # status=1:新增条目    status = 2 :可以使用    status = 3 :废弃   status = 4 :占用
    last_date = StringField(ddl='varchar(50)')
    reach_date = StringField(ddl='varchar(50)')
    done_date = StringField(ddl='varchar(2000)')

class DeviceInfo(Model):
    __table__ = 'deviceInfo'

    idenf = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    density = FloatField()
    dpi = FloatField()
    scaleDensity = FloatField()
    bestProvider = StringField(ddl='varchar(50)')
    gclGetCid = IntegerField()
    gclGetLac = IntegerField()
    gclGetPsc = IntegerField()
    
    cellLocation = StringField(ddl='varchar(50)')

    deviceId = StringField(ddl='varchar(100)')

    androidid = StringField(ddl = 'varchar(100)')

    networkOperator = StringField('varchar(50)')

    networkOperatorName = StringField('varchar(50)')

    networkType = StringField('varchar(50)')

    simSerialNumber = StringField('varchar(50)')

    simOperator = StringField('varchar(50)')

    simOperatorName = StringField('varchar(50)')

    subscriberId = StringField('varchar(50)')

    getSerial = StringField('varchar(50)')
    
    dataActivity = StringField('varchar(50)')

    board = StringField('varchar(50)')

    brand = StringField('varchar(50)')

    bootloader = StringField('varchar(50)')
    
    display = StringField('varchar(50)')

    device = StringField('varchar(50)')

    fingerPrint = StringField('varchar(100)')

    hardwear = StringField('varchar(50)')

    manufacturer = StringField('varchar(50)')

    model = StringField('varchar(50)')

    product = StringField('varchar(50)')

    relea = StringField('varchar(50)')

    sdk = IntegerField()

    sdkInt = IntegerField()

    extraInfo = StringField('varchar(50)')

    reason = StringField('varchar(50)')

    subType = StringField('varchar(50)')

    subTypeName = StringField('varchar(50)')

    type = StringField('varchar(50)')

    typeName = StringField('varchar(50)')

    macAddress = StringField('varchar(50)')

    bssid = StringField('varchar(50)')

    ipAddress = StringField('varchar(50)')

    networkId = StringField('varchar(50)')

    ssid = StringField('varchar(50)')

    rssi = StringField('varchar(50)')

    widthPixels = StringField('varchar(50)')

    heightPixels = StringField('varchar(50)')

    width = IntegerField()

    height = IntegerField()

    rotation = IntegerField()

    version = StringField('varchar(50)')

    line1Number = StringField('varchar(50)')

    tags = StringField('varchar(50)')

    phoneTime = StringField('varchar(50)')

    phoneType = StringField('varchar(50)')

    phoneUser = StringField('varchar(50)')

    host = StringField('varchar(50)')

    radioVersion = StringField('varchar(50)')

    codeName = StringField('varchar(50)')

    incremental = StringField('varchar(50)')

    buildID = StringField('varchar(50)')


class ExDeviceInfo(Model):
    __table__ = 'ex_deviceInfo'

    idenf = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    density = FloatField()
    dpi = FloatField()
    scaleDensity = FloatField()
    bestProvider = StringField(ddl='varchar(50)')
    gclGetCid = IntegerField()
    gclGetLac = IntegerField()
    gclGetPsc = IntegerField()

    ref = IntegerField()
    
    cellLocation = StringField(ddl='varchar(50)')

    deviceId = StringField(ddl='varchar(100)')

    androidid = StringField(ddl = 'varchar(100)')

    networkOperator = StringField('varchar(50)')

    networkOperatorName = StringField('varchar(50)')

    networkType = StringField('varchar(50)')

    simSerialNumber = StringField('varchar(50)')

    simOperator = StringField('varchar(50)')

    simOperatorName = StringField('varchar(50)')

    subscriberId = StringField('varchar(50)')

    getSerial = StringField('varchar(50)')
    
    dataActivity = StringField('varchar(50)')

    board = StringField('varchar(50)')

    brand = StringField('varchar(50)')

    bootloader = StringField('varchar(50)')
    
    display = StringField('varchar(50)')

    device = StringField('varchar(50)')

    fingerPrint = StringField('varchar(100)')

    hardwear = StringField('varchar(50)')

    manufacturer = StringField('varchar(50)')

    model = StringField('varchar(50)')

    product = StringField('varchar(50)')

    relea = StringField('varchar(50)')

    sdk = IntegerField()

    sdkInt = IntegerField()

    extraInfo = StringField('varchar(50)')

    reason = StringField('varchar(50)')

    subType = StringField('varchar(50)')

    subTypeName = StringField('varchar(50)')

    type = StringField('varchar(50)')

    typeName = StringField('varchar(50)')

    macAddress = StringField('varchar(50)')

    bssid = StringField('varchar(50)')

    ipAddress = StringField('varchar(50)')

    networkId = StringField('varchar(50)')

    ssid = StringField('varchar(50)')

    rssi = StringField('varchar(50)')

    widthPixels = StringField('varchar(50)')

    heightPixels = StringField('varchar(50)')

    width = IntegerField()

    height = IntegerField()

    rotation = IntegerField()

    version = StringField('varchar(50)')

    line1Number = StringField('varchar(50)')

    tags = StringField('varchar(50)')

    phoneTime = StringField('varchar(50)')

    phoneType = StringField('varchar(50)')

    phoneUser = StringField('varchar(50)')

    host = StringField('varchar(50)')

    radioVersion = StringField('varchar(50)')

    codeName = StringField('varchar(50)')

    incremental = StringField('varchar(50)')

    buildID = StringField('varchar(50)')