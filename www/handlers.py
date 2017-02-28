#!/usr/bin/env python
# coding=utf-8

#' url handlers '

import re, time, json, logging, hashlib, base64, asyncio

from aiohttp import web

from apis import APIValueError, APIResourceNotFoundError, APIError

from coroweb import get, post
from models import User, Comment, Blog, next_id, DeviceInfo, Remain, Task, ExDeviceInfo
from config import configs
import random
from json import *
from IpAddrGetter import IpGetter

#@get('/')
#async def index(request):
#    users = await User.findAll()
#    return {
#        '__template__' : 'test.html',
#        'users': users
#    }

create_table = ['create table if not exists %s (',
    'id integer not null primary key,' , 
    'create_time datetime not null,',
    'update_time timestamp not null,' ,
    'status integer not null,' ,
    'day_1 integer not null,' ,
    'day_2 integer not null,' ,
    'day_3 integer not null,' ,
    'day_4 integer not null,' ,
    'day_5 integer not null,' ,
    'day_6 integer not null,' ,
    'day_7 integer not null,' ,
    'day_8 integer not null,' ,
    'day_9 integer not null,' ,
    'day_10 integer not null,',
    'day_11 integer not null,',
    'day_12 integer not null,',
    'day_13 integer not null,',
    'day_14 integer not null,',
    'day_15 integer not null,',
    'day_16 integer not null,',
    'day_17 integer not null,',
    'day_18 integer not null,',
    'day_19 integer not null,',
    'day_20 integer not null,',
    'day_21 integer not null,',
    'day_22 integer not null,',
    'day_23 integer not null,',
    'day_24 integer not null,',
    'day_25 integer not null,',
    'day_26 integer not null,',
    'day_27 integer not null,',
    'day_28 integer not null,',
    'day_29 integer not null,',
    'day_30 integer not null',
') engine=innodb default charset=utf8']


@get('/')
def index(request):
    summary = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna alique.'
    blogs = [
        Blog(id='1', name='Test Blog', summary=summary, created_at=time.time()-120),
        Blog(id='2', name='Something New', summary=summary, created_at=time.time()-3600),
        Blog(id='3', name='Learn Swift', summary=summary, created_at=time.time()-7200)
    ]
    return {
        '__template__':'deviceInfo.html',
        'blogs':blogs
    }

# @get('/ipTest')
# async def index(request):
    # ip_getter = IpGetter()
    # print('request attr: %s' % dir(request))
    # print(dir(request.GET))
    # print(request.host)
    # print(request.http_range)
    # print('request %s' % request)
    # ip_addr = ip_getter.process_request(request)
    # print('ip_addr %s' % ip_addr)
    # print(request.__contains__)
    # print(request.url)
    # print(''.join(create_table) % 'table_name_remain')
    # await DeviceInfo.createTable('remain_test_1')


@get('/deviceInfo')
async def get_all_deviceInfo():
    devices = await DeviceInfo.selectAll()
    # print('deviceInfo.id %s' % devices[2].idenf)
    return {
        '__template__': 'deviceInfo.html',
        'devices':devices
    }

@get('/exDeviceInfo')
async def get_all_exDevideInfo():
    devices = await ExDeviceInfo.selectAll()
    return {
        '__template__': 'ex_deviceInfo.html',
        'devices':devices
    }

@get('/devInfo')
async def get_all_dev():
    devs = await DeviceInfo.selectAll()
    print('devInfo.id:  %s' % devs[2].id)



@get('/api/users')
async def api_get_users():
    users = await User.findAll(orderBy='created_at desc')
    for u in users:
        u.passwd = '******'
    return dict(user=users)

@get('/check')
def check_edit_info():
    return {
        '__template__':'check.html'
    }


_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
_RE_SHA1 = re.compile(r'^[0-9a-f]{40}$')
COOKIE_NAME = 'awesession'
_COOKIE_KEY = configs.session.secret

def user2cookie(user, max_age):
    expires = str(int(time.time() + max_age))
    s = '%s-%s-%s-%s' % (user.id, user.passwd, expires, _COOKIE_KEY)
    L = [user.id, expires, hashlib.sha1(s.encode('utf-8')).hexdigest()]
    return '-'.join(L)

async def cookie2user(cookie_str):
    if not cookie_str:
        return None
    try:
        L = cookie_str.splite('-')
        if len(L) != 3:
            return None
        uid, expires, sha1 = L
        if int(expires) < time.time():
            return None
        user = await User.find(uid)
        if user is None:
            return None
        s = '%s-%s-%s-%s' % (uid, user.passwd, expires, _COOKIE_KEY)
        if sha1 != hashlib.sha1(s.encode('utf-8')).hexdigest():
            logging.info('invalid sha1')
            return None
        user.passwd = '******'
        return user
    except Exception as e:
        logging.exception(e)
        return None

@get('/register')
def register():
    return {
        '__template__':'register.html'
    }

@get('/register3')
def register3():
    return {
        '__template__':'register3.html'
    }


@get('/signin')
def signin():
    return {
        '__template__':'signin.html'
    }

@get('/addTask')
def add_task():
    return {
        '__template__':'task.html'
    }

@get('/remain')
async def get_remain():
    max_id =  await Remain.selectMaxId('id')
    m = 0
    for k, v in max_id.items():
        m = int(v) 
        print('max: %s'% m)
    rd = random.randint(1, m)
    result = await Remain.findSpecItem('id', rd)
    return result['num']

@get('/rd_device')
async def get_random_deviceInfo():
    result = await ExDeviceInfo.selectRandom()
    k = JSONEncoder().encode(result)
    return k
    #return json.dumps(result.__dict__, ensure_ascii = False)
    #return result
    #return result.simSerialNumber

@post('/api/check')
async def check_by_idenf(* ,idenf):
    print('check by idenf: %s' % idenf)
    deviceInfo = await DeviceInfo.find(idenf)
    print('deviceInfo dpi: %s' % deviceInfo.dpi)
    print('deviceInfo idenf: %s' % deviceInfo.idenf)
    return deviceInfo

@get('/getById')
async def get_by_id(*, id):
    deviceInfo = await DeviceInfo.findById(id)
    #k = JSONEncoder.encode(deviceInfo)
    return deviceInfo

@post('/api/cc')
async def check_test(*, id):
    #print('check by id' % id)
    deviceInfo = await DeviceInfo.findById(id)
    print('deviceInfo dpi: %s' % deviceInfo.dpi)
    print('deviceInfo idenf: %s ' % deviceInfo.idenf)
    return deviceInfo


    
@post('/api/users')
async def api_register_user(*, email, name, passwd):
    print('save users')
    if not name or not name.strip():
        print('name is not right')
        raise APIValueError('name')
    if not email or not _RE_EMAIL.match(email):
        print('email is not right')
        raise APIValueError('email')
    if not passwd or not _RE_SHA1.match(passwd):
        print('passwd is not right')
        raise APIValueError('passwd')
    users = await User.findAll('email=?', [email])
    if len(users) > 0:
        print('email is already in use')
        raise APIError('register:failed', 'email', 'Email is already in use.')
    uid = next_id()
    sha1_passwd = '%s:%s' % (uid, passwd)
    user = User(id=uid, name=name.strip(), email=email, passwd=hashlib.sha1(sha1_passwd.encode('utf-8')).hexdigest(), image='http://www.gravatar.com/avatar/%s?d=mm&s=120' % hashlib.md5(email.encode('utf-8')).hexdigest())
    await user.save()
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
    user.passwd = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r

#@get('/delete')
#async def delete_test():
    #row = await DeviceInfo.deleteById(15)
    #print(delete affected row: ' % str(row))

@post('/api/task')
async def task_add(*, task_name, 
                    ip_repeat_days,
                    level_2_days,
                    level_2_percents,
                    level_3_days,
                    level_3_percents,
                    level_4_days,
                    level_4_percents,
                    level_5_days,
                    level_5_percents,
                    level_6_days,
                    level_6_percents,
                    level_7_days,
                    level_7_percents,
                    level_8_days,
                    level_8_percents):
    
    print('task_name: %s' % task_name)

    print('level_3_days: %s' % level_3_days)

    task = Task(task_name = task_name, 
            ip_repeat_days = int(ip_repeat_days),
            level_2_days = int(level_2_days),
            level_2_percents = float(level_2_percents),
            level_3_days = int(level_3_days),
            level_3_percents = float(level_3_percents),
            level_4_days = int(level_4_days),
            level_4_percents = float(level_4_percents),
            level_5_days = int(level_5_days),
            level_5_percents = float(level_5_percents),
            level_6_days = int(level_6_days),
            level_6_percents = float(level_6_percents),
            level_7_days = int(level_7_days),
            level_7_percents = float(level_6_percents),
            level_8_days = int(level_7_days),
            level_8_percents = float(level_6_percents)
            )

    result = await Task.selectSpecItem('task_name', task_name)

    if result:
        return 9900 #任务重名
    else:
        rows = await task.save()
        await Task.createTable(task_name)
        return rows



@post('/api/di')
async def add_device_info(*, density, dpi, scaleDensity,
                         bestProvider,
                         gclGetCid,
                         gclGetLac,
                         gclGetPsc,
                         cellLocation,
                         deviceId,
                         androidid,
                         networkOperator,
                         networkOperatorName,
                         networkType,
                         simSerialNumber,
                         simOperator,
                         simOperatorName,
                         subscriberId,
                         getSerial,
                         dataActivity,
                         board,
                         brand,
                         bootloader,
                         display,
                         device,
                         fingerPrint,
                         hardwear,
                         manufacturer,
                         model,
                         product,
                         relea,
                         sdk,
                         sdkInt,
                         extraInfo,
                         reason,
                         subType,
                         subTypeName,
                         type,
                         typeName,
                         macAddress,
                         bssid,
                         ipAddress,
                         networkId,
                         ssid,
                         rssi,
                         widthPixels,
                         heightPixels,
                         width,
                         height,
                         rotation,
                         version,
                         line1Number,
                         tags,
                         phoneTime,
                         phoneType,
                         phoneUser,
                         host,
                         radioVersion,
                         codeName,
                         incremental,
                         buildID
                         
                         
                         ): 

    print('density: %s' % density)
    print('add deviceInfo: %s' % dpi)
    print('scaleDensity: %s' % scaleDensity)
    print('bestProvider: %s' % bestProvider)
    #uid = next_id()
    di = DeviceInfo( 
                    density=float(density),
                    dpi = float(dpi),
                    scaleDensity = float(scaleDensity),
                    bestProvider = bestProvider,
                    gclGetCid = int(gclGetCid),
                    gclGetLac = int(gclGetLac),
                    gclGetPsc = int(gclGetPsc),
                    cellLocation = cellLocation,
                    deviceId = deviceId,
                    androidid = androidid,
                    networkOperator = networkOperator,
                    networkOperatorName = networkOperatorName,
                    networkType = networkType,
                    simSerialNumber = simSerialNumber,
                    simOperator = simOperator,
                    simOperatorName = simOperatorName,
                    subscriberId = subscriberId,
                    getSerial = getSerial,
                    dataActivity = dataActivity,
                    board = board,
                    brand = brand,
                    bootloader = bootloader,
                    display = display,
                    device = device,
                    fingerPrint = fingerPrint,
                    hardwear = hardwear,
                    manufacturer = manufacturer,
                    model = model,
                    product = product,
                    relea = relea,
                    sdk = int(sdk),
                    sdkInt = int(sdkInt),
                    extraInfo = extraInfo,
                    reason = reason,
                    subType = subType,
                    subTypeName = subTypeName,
                    type = type,
                    typeName = typeName,
                    macAddress = macAddress,
                    bssid = bssid,
                    ipAddress = ipAddress,
                    networkId = networkId,
                    ssid = ssid,
                    rssi = rssi,
                    widthPixels = widthPixels,
                    heightPixels = heightPixels,
                    width = int(width),
                    height = int(height),
                    rotation = int(rotation),
                    version = version,
                    line1Number = line1Number,
                    tags = tags,
                    phoneTime = phoneTime,
                    phoneType = phoneType,
                    phoneUser = phoneUser,
                    host = host,
                    radioVersion = radioVersion,
                    codeName = codeName,
                    incremental = incremental,
                    buildID = buildID


                   ) 
    rows = await di.save()
    return rows


@post('/api/update')
async def update_device_info(*,
                         idenf, 
                         density, 
                         dpi, 
                         scaleDensity,
                         bestProvider,
                         gclGetCid,
                         gclGetLac,
                         gclGetPsc,
                         cellLocation,
                         deviceId,
                         androidid,
                         networkOperator,
                         networkOperatorName,
                         networkType,
                         simSerialNumber,
                         simOperator,
                         simOperatorName,
                         subscriberId,
                         getSerial,
                         dataActivity,
                         board,
                         brand,
                         bootloader,
                         display,
                         device,
                         fingerPrint,
                         hardwear,
                         manufacturer,
                         model,
                         product,
                         relea,
                         sdk,
                         sdkInt,
                         extraInfo,
                         reason,
                         subType,
                         subTypeName,
                         type,
                         typeName,
                         macAddress,
                         bssid,
                         ipAddress,
                         networkId,
                         ssid,
                         rssi,
                         widthPixels,
                         heightPixels,
                         width,
                         height,
                         rotation,
                         version,
                         line1Number,
                         tags,
                         phoneTime,
                         phoneType,
                         phoneUser,
                         host,
                         radioVersion,
                         codeName,
                         incremental,
                         buildID,
                         id):


    di = DeviceInfo( 
                    density=float(density),
                    dpi = float(dpi),
                    scaleDensity = float(scaleDensity),
                    bestProvider = bestProvider,
                    gclGetCid = int(gclGetCid),
                    gclGetLac = int(gclGetLac),
                    gclGetPsc = int(gclGetPsc),
                    cellLocation = cellLocation,
                    deviceId = deviceId,
                    androidid = androidid,
                    networkOperator = networkOperator,
                    networkOperatorName = networkOperatorName,
                    networkType = networkType,
                    simSerialNumber = simSerialNumber,
                    simOperator = simOperator,
                    simOperatorName = simOperatorName,
                    subscriberId = subscriberId,
                    getSerial = getSerial,
                    dataActivity = dataActivity,
                    board = board,
                    brand = brand,
                    bootloader = bootloader,
                    display = display,
                    device = device,
                    fingerPrint = fingerPrint,
                    hardwear = hardwear,
                    manufacturer = manufacturer,
                    model = model,
                    product = product,
                    relea = relea,
                    sdk = int(sdk),
                    sdkInt = int(sdkInt),
                    extraInfo = extraInfo,
                    reason = reason,
                    subType = subType,
                    subTypeName = subTypeName,
                    type = type,
                    typeName = typeName,
                    macAddress = macAddress,
                    bssid = bssid,
                    ipAddress = ipAddress,
                    networkId = networkId,
                    ssid = ssid,
                    rssi = rssi,
                    widthPixels = widthPixels,
                    heightPixels = heightPixels,
                    width = int(width),
                    height = int(height),
                    rotation = int(rotation),
                    version = version,
                    line1Number = line1Number,
                    tags = tags,
                    phoneTime = phoneTime,
                    phoneType = phoneType,
                    phoneUser = phoneUser,
                    host = host,
                    radioVersion = radioVersion,
                    codeName = codeName,
                    incremental = incremental,
                    buildID = buildID


                   ) 

    

    di.idenf = idenf
    
    print("update fields: %s" % di.__fields__)

    rows = await di.update_by_id(id)

    print("update rows: %s" % rows)

    return rows


@post('/api/delete')
async def delete_device_info(*,
                         idenf, 
                         density, 
                         dpi, 
                         scaleDensity,
                         bestProvider,
                         gclGetCid,
                         gclGetLac,
                         gclGetPsc,
                         cellLocation,
                         deviceId,
                         androidid,
                         networkOperator,
                         networkOperatorName,
                         networkType,
                         simSerialNumber,
                         simOperator,
                         simOperatorName,
                         subscriberId,
                         getSerial,
                         dataActivity,
                         board,
                         brand,
                         bootloader,
                         display,
                         device,
                         fingerPrint,
                         hardwear,
                         manufacturer,
                         model,
                         product,
                         relea,
                         sdk,
                         sdkInt,
                         extraInfo,
                         reason,
                         subType,
                         subTypeName,
                         type,
                         typeName,
                         macAddress,
                         bssid,
                         ipAddress,
                         networkId,
                         ssid,
                         rssi,
                         widthPixels,
                         heightPixels,
                         width,
                         height,
                         rotation,
                         version,
                         line1Number,
                         tags,
                         phoneTime,
                         phoneType,
                         phoneUser,
                         host,
                         radioVersion,
                         codeName,
                         incremental,
                         buildID,
                         id):

    di = DeviceInfo( 
                    density=float(density),
                    dpi = float(dpi),
                    scaleDensity = float(scaleDensity),
                    bestProvider = bestProvider,
                    gclGetCid = int(gclGetCid),
                    gclGetLac = int(gclGetLac),
                    gclGetPsc = int(gclGetPsc),
                    cellLocation = cellLocation,
                    deviceId = deviceId,
                    androidid = androidid,
                    networkOperator = networkOperator,
                    networkOperatorName = networkOperatorName,
                    networkType = networkType,
                    simSerialNumber = simSerialNumber,
                    simOperator = simOperator,
                    simOperatorName = simOperatorName,
                    subscriberId = subscriberId,
                    getSerial = getSerial,
                    dataActivity = dataActivity,
                    board = board,
                    brand = brand,
                    bootloader = bootloader,
                    display = display,
                    device = device,
                    fingerPrint = fingerPrint,
                    hardwear = hardwear,
                    manufacturer = manufacturer,
                    model = model,
                    product = product,
                    relea = relea,
                    sdk = int(sdk),
                    sdkInt = int(sdkInt),
                    extraInfo = extraInfo,
                    reason = reason,
                    subType = subType,
                    subTypeName = subTypeName,
                    type = type,
                    typeName = typeName,
                    macAddress = macAddress,
                    bssid = bssid,
                    ipAddress = ipAddress,
                    networkId = networkId,
                    ssid = ssid,
                    rssi = rssi,
                    widthPixels = widthPixels,
                    heightPixels = heightPixels,
                    width = int(width),
                    height = int(height),
                    rotation = int(rotation),
                    version = version,
                    line1Number = line1Number,
                    tags = tags,
                    phoneTime = phoneTime,
                    phoneType = phoneType,
                    phoneUser = phoneUser,
                    host = host,
                    radioVersion = radioVersion,
                    codeName = codeName,
                    incremental = incremental,
                    buildID = buildID


                   ) 

    

    di.idenf = idenf

    print('deviceInfo.id: %s' % id)
    
    print("delete fields: %s" % di.__fields__)


    rows = await DeviceInfo.deleteById(id)

    print("delete rows: %s" % rows)

    return rows


