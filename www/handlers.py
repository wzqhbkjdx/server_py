#!/usr/bin/env python
# coding=utf-8

#' url handlers '

import re, time, json, logging, hashlib, base64, asyncio

from aiohttp import web

from apis import APIValueError, APIResourceNotFoundError, APIError

from coroweb import get, post
from models import User, Comment, Blog, next_id, DeviceInfo, Remain
from config import configs
import random

#@get('/')
#async def index(request):
#    users = await User.findAll()
#    return {
#        '__template__' : 'test.html',
#        'users': users
#    }


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

@get('/deviceInfo')
async def get_all_deviceInfo():
    devices = await DeviceInfo.findAll()
    return {
        '__template__': 'deviceInfo.html',
        'devices':devices
    }



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

@post('/api/check')
async def check_by_idenf(* ,idenf):
    print('check by idenf: %s' % idenf)
    deviceInfo = await DeviceInfo.find(idenf)
    print('deviceInfo dpi: %s' % deviceInfo.dpi)
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
                         buildID):

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

    rows = await di.update()

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
                         buildID):

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
    
    print("delete fields: %s" % di.__fields__)

    rows = await di.remove()

    print("delete rows: %s" % rows)

    return rows


