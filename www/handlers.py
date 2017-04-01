#!/usr/bin/env python
# coding=utf-8

#' url handlers '

import re, time, json, logging, hashlib, base64, asyncio, sched, os

from aiohttp import web

from apis import APIValueError, APIResourceNotFoundError, APIError

from coroweb import get, post
from models import *
from config import configs
import random
from json import *
from IpAddrGetter import IpGetter

import datetime
import collections

from dev_generator import DevGenerator

from xml.etree.ElementTree import ElementTree,Element

from XmlParser import *

import string


@get('/now_test')
def now_test():
    with open('templates/iphone_dev_model.xml') as file:
        data = file.read()
    return ' $$' + data

@get('/rd_iphone_devInfo')
async def rd_iphone_devInfo():
    tree = read_xml('templates/iphone_dev_model.xml')
    nodes = find_nodes(tree, 'dict')

    BLUEADDRESS = DevGenerator.randomAddress()
    BLUEADDRESS_KEY = create_node('key',{}, 'BLUEADDRESS')
    BLUEADDRESS_VAKUE = create_node('string', {}, BLUEADDRESS)
    add_child_node(nodes, BLUEADDRESS_KEY)
    add_child_node(nodes, BLUEADDRESS_VAKUE)

    BUILDVERSION = DevGenerator.get_iphone_buildversion()
    BUILDVERSION_KEY = create_node('key',{}, 'BUILDVERSION')
    BUILDVERSION_VALUE = create_node('string', {}, BUILDVERSION)
    add_child_node(nodes, BUILDVERSION_KEY)
    add_child_node(nodes, BUILDVERSION_VALUE)

    DEVICETOKEN = DevGenerator.get_spec_num_str(64,'0123456789abcdef')
    DEVICETOKEN_KEY = create_node('key',{}, 'DEVICETOKEN')
    DEVICETOKEN_VALUE = create_node('string', {}, DEVICETOKEN)
    add_child_node(nodes, DEVICETOKEN_KEY)
    add_child_node(nodes, DEVICETOKEN_VALUE)

    ECID = DevGenerator.get_spec_num_str(5, '0123456789ABCDEF')
    ECID_KEY = create_node('key',{},'ECID')
    ECID_VALUE = create_node('string',{}, ECID)
    add_child_node(nodes, ECID_KEY)
    add_child_node(nodes, ECID_VALUE)

    IAD_KEY = create_node('key',{}, 'IAD')
    iad1 = DevGenerator.get_spec_num_str(8, '0123456789ABCDEF')
    iad2 = DevGenerator.get_spec_num_str(4, '0123456789ABCDEF')
    iad3 = DevGenerator.get_spec_num_str(4, '0123456789ABCDEF')
    iad4 = DevGenerator.get_spec_num_str(4, '0123456789ABCDEF')
    iad5 = DevGenerator.get_spec_num_str(12, '0123456789ABCDEF')
    iad_str = iad1 + '-' + iad2 + '-' + iad3 + '-' + '-' + iad4 + '-' + iad5
    IAD_VALUE = create_node('string', {}, iad_str)
    add_child_node(nodes, IAD_KEY)
    add_child_node(nodes, IAD_VALUE)

    IDFV_KEY = create_node('key',{},'IDFV')
    idfv1 = DevGenerator.get_spec_num_str(8, '0123456789ABCDEF')
    idfv2 = DevGenerator.get_spec_num_str(4, '0123456789ABCDEF')
    idfv3 = DevGenerator.get_spec_num_str(4, '0123456789ABCDEF')
    idfv4 = DevGenerator.get_spec_num_str(4, '0123456789ABCDEF')
    idfv5 = DevGenerator.get_spec_num_str(12, '0123456789ABCDEF')
    idfv_str = idfv1 + '-' + idfv2 + '-' + idfv3 + '-' + '-' + idfv4 + '-' + idfv5
    IDFV_VALUE = create_node('string', {}, idfv_str)
    add_child_node(nodes, IDFV_KEY)
    add_child_node(nodes, IDFV_VALUE)

    IP = DevGenerator.get_random_ip()
    IP_KEY = create_node('key',{},'IP')
    IP_VALUE = create_node('string',{}, IP)
    add_child_node(nodes, IP_KEY)
    add_child_node(nodes, IP_VALUE)

    IPS = DevGenerator.get_random_ip()
    IPS_KEY = create_node('key',{},'IPS')
    IPS_VALUE = create_node('string',{}, IPS)
    add_child_node(nodes, IPS_KEY)
    add_child_node(nodes, IPS_VALUE)

    MLBSERIAL = DevGenerator.get_spec_num_str(16, '0123456789ABCDEF')
    MLBSERIAL_KEY = create_node('key', {}, 'MLBSERIAL')
    MLBSERIAL_VALUE = create_node('string', {}, MLBSERIAL)
    add_child_node(nodes, MLBSERIAL_KEY)
    add_child_node(nodes, MLBSERIAL_VALUE)

    MODEL_KEY = create_node('key',{}, 'MODEL')
    MODEL_VALUE = create_node('string', {}, 'iPhone')
    add_child_node(nodes, MODEL_KEY)
    add_child_node(nodes, MODEL_VALUE)

    MODELTYPE_KEY = create_node('key',{}, 'MODELTYPE')
    MODELTYPE_VALUE = create_node('string', {}, 'iPhone')
    add_child_node(nodes, MODEL_KEY)
    add_child_node(nodes, MODEL_VALUE)

    NAME = DevGenerator.get_spec_num_str(8, string.ascii_letters + string.digits)
    NAME_KEY = create_node('key',{},'NAME')
    NAME_VALUE = create_node('string',{},NAME)
    add_child_node(nodes, NAME_KEY)
    add_child_node(nodes, NAME_VALUE)

    ODIN = DevGenerator.get_spec_num_str(40, '0123456789abcdef')
    ODIN_KEY = create_node('key', {}, 'ODIN')
    ODIN_VALUE = create_node('string', {}, ODIN)
    add_child_node(nodes, ODIN_KEY)
    add_child_node(nodes, ODIN_VALUE)

    OPENUDID = DevGenerator.get_spec_num_str(40, '0123456789abcdef')
    OPENUDID_KEY = create_node('key', {}, 'OPENUDID')
    OPENUDID_VALUE = create_node('string', {}, OPENUDID)
    add_child_node(nodes, OPENUDID_KEY)
    add_child_node(nodes, OPENUDID_VALUE)

    ORG_KEY = create_node('key',{},'ORG')
    ORG_VALUE = create_node('string', {}, 'iPhone/7.1.2/11D257')
    add_child_node(nodes, ORG_KEY)
    add_child_node(nodes, ORG_VALUE)

    ORGMODEL_KEY = create_node('key',{},'ORGMODEL')
    ORGMODEL_VALUE = create_node('string', {}, 'iPhone')
    add_child_node(nodes, ORGMODEL_KEY)
    add_child_node(nodes, ORGMODEL_VALUE)

    PRODUCT = DevGenerator.get_iphone_dev_product()
    PRODUCT_KEY = create_node('key',{},'PRODUCT')
    PRODUCT_VALUE = create_node('string', {}, PRODUCT)
    add_child_node(nodes, PRODUCT_KEY)
    add_child_node(nodes, PRODUCT_VALUE)

    RSSID = DevGenerator.get_spec_num_str(12, string.ascii_letters + string.digits)
    RSSID_KEY = create_node('key',{},'RSSID')
    RSSID_VALUE = create_node('string',{}, RSSID)
    add_child_node(nodes, RSSID_KEY)
    add_child_node(nodes, RSSID_VALUE)

    SERIAL = DevGenerator.get_spec_num_str(12, '0123456789ABCDEF')
    SERIAL_KEY = create_node('key', {}, 'SERIAL')
    SERIAL_VALUE = create_node('string',{}, SERIAL)
    add_child_node(nodes, SERIAL_KEY)
    add_child_node(nodes, SERIAL_VALUE)

    UDID = DevGenerator.get_spec_num_str(40, '0123456789abcdef')
    UDID_KEY = create_node('key',{},'UDID')
    UDID_VALUE = create_node('string',{}, UDID)
    add_child_node(nodes, UDID_KEY)
    add_child_node(nodes, UDID_VALUE)

    VERSION = DevGenerator.get_ios_version()
    VERSION_KEY = create_node('key',{}, 'VERSION')
    VERSION_VALUE = create_node('string',{}, VERSION)
    add_child_node(nodes, VERSION_KEY)
    add_child_node(nodes, VERSION_VALUE)

    WIFIADDRESS = DevGenerator.randomAddress()
    WIFIADDRESS_KEY = create_node('key',{}, 'WIFIADDRESS')
    WIFIADDRESS_VALUE = create_node('string',{},WIFIADDRESS)
    add_child_node(nodes, WIFIADDRESS_KEY)
    add_child_node(nodes, WIFIADDRESS_VALUE)

    iGrimaceKey = DevGenerator.get_igrimacekey()
    iGrimaceKey_key = create_node('key', {}, 'iGrimaceKey')
    iGrimaceKey_value = create_node('string', {}, iGrimaceKey)
    add_child_node(nodes, iGrimaceKey_key)
    add_child_node(nodes, iGrimaceKey_value)

    rj_str = DevGenerator.get_rj_rj2()
    rj_key = create_node('key',{}, 'rj')
    rj_value = create_node('string',{}, rj_str)
    add_child_node(nodes, rj_key)
    add_child_node(nodes, rj_value)

    rj2_key = create_node('key',{}, 'rj2')
    rj2_value = create_node('string',{}, rj_str)
    add_child_node(nodes, rj2_key)
    add_child_node(nodes, rj2_value)

    rw_str = DevGenerator.get_rw_rw2()
    rw_key = create_node('key',{},'rw')
    rw_value = create_node('string', {}, rw_str)
    add_child_node(nodes, rw_key)
    add_child_node(nodes, rw_value)

    rw2_key = create_node('key',{},'rw2')
    rw2_value = create_node('string', {}, rw_str)
    add_child_node(nodes, rw2_key)
    add_child_node(nodes, rw2_value)

    iphoneDevInfo = IphoneDevInfo()
    iphoneDevInfo.BLUEADDRESS = BLUEADDRESS
    iphoneDevInfo.BUILDVERSION = BUILDVERSION
    iphoneDevInfo.DEVICETOKEN = DEVICETOKEN
    iphoneDevInfo.ECID = ECID
    iphoneDevInfo.IAD = iad_str
    iphoneDevInfo.IDFV = idfv_str
    iphoneDevInfo.IP = IP
    iphoneDevInfo.IPS = IPS
    iphoneDevInfo.MLBSERIAL = MLBSERIAL
    iphoneDevInfo.MODEL = 'iPhone'
    iphoneDevInfo.MODELTYPE = 'iPhone'
    iphoneDevInfo.NAME = NAME
    iphoneDevInfo.ODIN = ODIN
    iphoneDevInfo.OPENUDID = OPENUDID
    iphoneDevInfo.ORG = 'iPhone/7.1.2/11D257'
    iphoneDevInfo.ORGMODEL = 'iPhone'
    iphoneDevInfo.PRODUCT = PRODUCT
    iphoneDevInfo.RSSID = RSSID
    iphoneDevInfo.SERIAL = SERIAL
    iphoneDevInfo.UDID = UDID
    iphoneDevInfo.VERSION = VERSION
    iphoneDevInfo.WIFIADDRESS = WIFIADDRESS
    iphoneDevInfo.iGrimaceKey = iGrimaceKey
    iphoneDevInfo.rj = rj_str
    iphoneDevInfo.rj2 = rj_str
    iphoneDevInfo.rw = rw_str
    iphoneDevInfo.rw2 = rw_str

    row = await iphoneDevInfo.save()

    if row == 1:
        logging.debug('save iphone deviceInfo success')

        ret_ip_deviceInfo = await IphoneDevInfo.selectSpecCls('idenf', iphoneDevInfo.idenf)

        if ret_ip_deviceInfo:

            logging.debug('select iphone deviceInfo success')
            ip_dev_id = ret_ip_deviceInfo.id

            path = './iphone_dev/' + iphoneDevInfo.idenf + '.xml'

            logging.debug('iphonedeviceInfo path: %s' % path)
            write_xml(tree, path)

            with open(path) as file:
                data = file.read()

            os.remove(path)
            logging.debug('delete xml path: %s' % path)

            return str(ip_dev_id) + '$$' + data
        else:
            return 'error$$error'
    else:
        return 'error$$error'


def getDate():
    now = datetime.datetime.now()
    return now.strftime('%Y-%m-%d')

def getDateTime():
    now = datetime.datetime.now()
    return now.strftime('%Y-%m-%d %H:%M:%S')


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

#下面注释掉的方法用于获取客户端ip地址
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


@get('/netCheck')
def netCheck():
    return 'ok'

@get('/add_simple')
def addSimple():
    return {
        '__template__':'simple_add.html'
    }

@post('/api/addSimple')
async def addSimpleDeviceId(*, density,
                    dpi,
                    scaleDensity,
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
                    widthPixels,
                    heightPixels,
                    width,
                    height,
                    version,
                    tags,
                    phoneTime,
                    phoneType,
                    phoneUser,
                    host,
                    radioVersion,
                    codeName,
                    incremental,
                    buildID):
    # print('add simple')
    deviceInfo = DeviceInfo()
    deviceInfo.density = float(density)
    deviceInfo.dpi = float(dpi)
    deviceInfo.scaleDensity = float(scaleDensity)
    deviceInfo.board = board
    deviceInfo.brand = brand
    deviceInfo.bootloader = bootloader
    deviceInfo.display = display
    deviceInfo.device = device
    deviceInfo.fingerPrint = fingerPrint
    deviceInfo.hardwear = hardwear
    deviceInfo.manufacturer = manufacturer
    deviceInfo.model = model
    deviceInfo.product = product
    deviceInfo.relea = relea
    deviceInfo.sdk = int(sdk)
    deviceInfo.sdkInt = int(sdkInt)
    deviceInfo.widthPixels = widthPixels
    deviceInfo.heightPixels = heightPixels
    deviceInfo.width = int(width)
    deviceInfo.height = int(height)
    deviceInfo.version = version
    deviceInfo.tags = tags
    deviceInfo.phoneTime = phoneTime
    deviceInfo.phoneType = phoneType
    deviceInfo.phoneUser = phoneUser
    deviceInfo.host = host
    deviceInfo.radioVersion = radioVersion
    deviceInfo.codeName = codeName
    deviceInfo.incremental = incremental
    deviceInfo.buildID = buildID

    deviceInfo.bestProvider = 'network'
    deviceInfo.gclGetCid = -1
    deviceInfo.gclGetLac = -1
    deviceInfo.gclGetPsc = 0
    deviceInfo.cellLocation = '[-1,-1,0]'
    deviceInfo.deviceId = DevGenerator.getDeviceId()
    deviceInfo.androidid = DevGenerator.getAndroidId()
    deviceInfo.networkOperator, deviceInfo.networkOperatorName, deviceInfo.simOperator, deviceInfo.simOperatorName, deviceInfo.subscriberId = DevGenerator.getFive()
    deviceInfo.networkType = 0
    deviceInfo.simSerialNumber = DevGenerator.get_simSerialNumber()
    deviceInfo.getSerial = DevGenerator.get_serial()
    deviceInfo.dataActivity = 0
    wifi_name = DevGenerator.get_wifi_name()
    deviceInfo.extraInfo = wifi_name
    deviceInfo.ssid = wifi_name
    deviceInfo.reason = ''
    deviceInfo.subType = 0
    deviceInfo.subTypeName = ''
    deviceInfo.type = 1
    deviceInfo.typeName = 'WIFI'
    deviceInfo.macAddress = DevGenerator.randomAddress()
    deviceInfo.bssid = DevGenerator.randomAddress()
    deviceInfo.ipAddress = DevGenerator.get_random_ip()
    deviceInfo.networkId = 0
    deviceInfo.rssi = DevGenerator.get_rssi()
    deviceInfo.rotation = 0
    deviceInfo.line1Number = ''

    rows = await deviceInfo.save()
    return rows



#向服务器请示，查看是否允许今日新增任务
@get('/newTask')
async def newTask(*, task_name):
    rs = await check_newTask_limit(task_name)
    return rs

async def check_newTask_limit(task_name):
    counts = await Task.selectDate(task_name)
    # print('result counts: %s' % counts)
    if counts >= 0:
        result = await Task.selectSpecItem('task_name', task_name)
        # print('new_limit: %s' % result['new_limit'])
        if(counts < result['new_limit']):
            return 'yes'
        else:
            return 'no'
    else:
        return 'no_no'

#向服务器获取留存任务
@get('/remainTask')
async def remainTask(*, task_name):
    # status = 2 ; last_date > now(); reach_date < now()
    # pass
    status = 2
    remain_task = await RemainTask.selectByTableForRemain(task_name, status)
    if remain_task:
        remain_task.status = 4 #表明该task已经被申请过了
        row = await remain_task.update_by_table(task_name)
        if row:
            return str(remain_task.id)
        else:
            return '-1' #表示申请出错了
    else:
        return '0' #表示没有留存任务可做了

@get('/remainTaskPhoneNo')
async def remainTaskPhoneNo(*, task_name, phoneNo):
    status = 2
    remain_task = await RemainTask.selectByTableForRemainPhoneNo(task_name, status, phoneNo)
    if remain_task:
        remain_task.status = 4 #表明该task已经被申请过了
        row = await remain_task.update_by_table(task_name)
        if row:
            return str(remain_task.id)
        else:
            return '-1' #表示申请出错了
    else:
        return '0' #表示没有留存任务可做了

#新增任务完成提交服务器
@get('/newTaskComplete')
async def newTaskComplete(*, table_name, id, phoneNo):

    #查询扩展设备信息表，确认扩展设备信息表中有该id
    ex = await ExDeviceInfo.selectSpecCls('id',id)
    if not ex:
        return 'failed'

    rs = await check_newTask_limit(table_name)

    if rs == 'no':

        return 'failed'

    elif rs == 'yes':
        remain_task = await RemainTask.selectByTable(table_name, 'id', id)
        if remain_task:
            return 'failed'
        else:
            remain_task = RemainTask()
            remain_task.id = int(id)
            remain_task.phoneNo = phoneNo
            remain_task.create_time = getDateTime()
            remain_task.update_time = getDateTime()
            remain_task.status = 1
            remain_task.reach_date = getDate()
            remain_task.done_date = getDate()
            row = await remain_task.saveByTable(table_name)
            if row == 1:
                return 'success'
            else:
                return 'failed'



#留存任务完成提交服务器
@get('/remaintaskComplete')
async def taskComplete(*, table_name, id, phoneNo):

    remain_task = await RemainTask.selectByTable(table_name, 'id', id)
    if remain_task:
        if remain_task.status != 4: #必须是从服务器获取的留存任务,才能再次向服务器提交,否则无法提交
            return 'failed'
        remain_task.status = 2 #新增任务执行完毕后，将status恢复回2值
        remain_task.reach_date = getDate()
        remain_task.done_date = remain_task.done_date + ',' + getDate()
        row = await remain_task.update_by_table(table_name)
        if row == 1:
            return 'success'
        else:
            return 'failed'
    else:
        return 'failed'



@get('/schedule_manul')
async def schedule_manul(*, user_name, user_password, task_name, cre_time):
    # rs = await RemainTask.selectByTableLimitDate('xiaoyun_test9','create_time',1,1,cre_time)
    # print(rs)
    if user_name == 'wzq' and user_password == 'password':

        result = await Task.selectSpecItem('task_name', task_name)

        # print(result)

        day_level = []

        day_level.append(result['level_2_days'])
        day_level.append(result['level_3_days'])
        day_level.append(result['level_4_days'])
        day_level.append(result['level_5_days'])
        day_level.append(result['level_6_days'])
        day_level.append(result['level_7_days'])
        day_level.append(result['level_8_days'])

        day_level = list(a for a in day_level if a > 0)

        print(day_level)

        day_percent = []

        day_percent.append(result['level_2_percents'])
        day_percent.append(result['level_3_percents'])
        day_percent.append(result['level_4_percents'])
        day_percent.append(result['level_5_percents'])
        day_percent.append(result['level_6_percents'])
        day_percent.append(result['level_7_percents'])
        day_percent.append(result['level_8_percents'])

        day_percent = list(a for a in day_percent if a > 0.0)

        print(day_percent)


        range_dict = collections.OrderedDict()

        #获取当前数据库中新增的任务总数
        total_counts = await Task.selectSpecDate(task_name, cre_time)
        if total_counts < 10:
            return 'the counts of new tasks are less than the limit'


        # print('total_counts: %s ' % total_counts)
        #生成关键节点上的 day-count 的键值对
        # day_level   [2,    7,    15,   30]
        # day_percent [25.0, 20.0, 10.0, 5.0]

        for i in range(len(day_level)):
            range_dict[day_level[i]] = day_percent[i]

        # print(range_dict)

        days = collections.OrderedDict() #每天留存比例dict

        #根据关键节点上的 day-count 键值对生成其他day对应的count （根据首尾节点的值计算平均值）

        for i in range(2, 31):

            for key in day_level:
                if i == key:
                    days[i] = range_dict[key]
                    break
                    # print('index: %s' % day_level.index(key))
                elif i > key:
                    continue
                elif i < key:
                    forward = day_level[day_level.index(key) - 1] # 找到day_level中的当前key的前一个key值 因为day_level中没有相同的值，所以这个方法可行，如果有相同的值，每次index都返回当前list中的第一个，会引发错误
                    forward_value = range_dict[forward]
                    # print('forward_value: %s ' % forward_value)
                    next_value = range_dict[key]
                    avrage_slice = (forward_value - next_value) / (key - forward) # 平均切片
                    slice_result = forward_value - (i - forward) * avrage_slice
                    # print('slice_result %s' % slice_result)
                    days[i] = round(slice_result, 2)
                    break

        # print(days)
        #处理每天留存比例dict
        for key in days.keys():
            days[key] = round((days[key] * total_counts) / 100, 0) # 先圆整，再转为int值，这样不会出现小于0的现象
            # days[key] = int((days[key] * total_counts) / 100)
        print(days)
        #遍历dict 从value的最小值到最大值，如果本次的和上次的value相等，则不变，如果本次的比上次多，则求差值后从数据库中选取相应个数改变它们的last_time即可

        day = []
        remain_counts = []

        # days ([(2, 12.0), (3, 12.0), (4, 12.0), (5, 11.0), (6, 10.0), (7, 10.0), (8, 9.0), (9, 9.0), (10, 8.0), (11, 8.0), (12, 7.0), 
        # (13, 6.0), (14, 6.0), (15, 5.0), (16, 5.0), (17, 5.0), (18, 4.0), (19, 4.0), (20, 4.0), (21, 4.0), (22, 4.0), (23, 4.0), (24, 4.0), 
        # (25, 3.0), (26, 3.0), (27, 3.0), (28, 3.0), (29, 3.0), (30, 2.0)])

        for key in days.keys():
            day.append(key)
            if days[key] == 0:
                days[key] = 1
            remain_counts.append(int(days[key]))

        print('day: %s' % day)
        print('remain_counts: %s' % remain_counts)

        # day:           [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
        # remain_counts: [25,24,23,22,21,20,18,17,16, 15, 13, 12, 11, 10,  9,  9,  9,  8,  8,  8,  7,  7,  7,  6,  6,  6,  5, 5,  5]

        for i in range(len(remain_counts) - 1, -1, -1): #倒序遍历

            if i == (len(remain_counts) - 1): #最后一天的那一个
                #从数据库中随机取出remain_counts[i]对应的条目,
                status = 1
                remain_items = await RemainTask.selectByTableLimitDate(task_name, 'create_time', status, remain_counts[i], cre_time)
                print(remain_items)
                for remain_item in remain_items:
                    last_date = remain_item.create_time + datetime.timedelta(days = (day[i] - 1))
                    remain_item.last_date = last_date
                    remain_item.status = 2; # 1-> 2 表示这个新增已经可以使用
                    print(remain_item.last_date)
                    await remain_item.update_by_table(task_name)

            else:
                if remain_counts[i] <= remain_counts[i + 1]:
                    continue
                elif remain_counts[i] > remain_counts[i + 1]:
                    print('>>')
                    div_counts = remain_counts[i] - remain_counts[i + 1]
                    status = 1
                    remain_items = await RemainTask.selectByTableLimitDate(task_name, 'create_time', status, div_counts, cre_time)
                    for remain_item in remain_items:
                        last_date = remain_item.create_time + datetime.timedelta(days = (day[i] - 1))
                        remain_item.last_date = last_date
                        remain_item.status = 2; # 1-> 2 表示这个新增已经可以使用
                        print(remain_item.last_date)
                        await remain_item.update_by_table(task_name)
        return 'success'

    else:
        return 'failed'



@get('/schedule')
async def schedule_reamin(*, user_name, user_password, task_name):

    if user_name == 'wzq' and user_password == 'password':

        result = await Task.selectSpecItem('task_name', task_name)

        # print(result)

        day_level = []

        day_level.append(result['level_2_days'])
        day_level.append(result['level_3_days'])
        day_level.append(result['level_4_days'])
        day_level.append(result['level_5_days'])
        day_level.append(result['level_6_days'])
        day_level.append(result['level_7_days'])
        day_level.append(result['level_8_days'])

        day_level = list(a for a in day_level if a > 0)

        print(day_level)

        day_percent = []

        day_percent.append(result['level_2_percents'])
        day_percent.append(result['level_3_percents'])
        day_percent.append(result['level_4_percents'])
        day_percent.append(result['level_5_percents'])
        day_percent.append(result['level_6_percents'])
        day_percent.append(result['level_7_percents'])
        day_percent.append(result['level_8_percents'])

        day_percent = list(a for a in day_percent if a > 0.0)

        print(day_percent)


        range_dict = collections.OrderedDict()

        #获取当前数据库中新增的任务总数
        total_counts = await Task.selectDate(task_name)
        if total_counts < 10:
            return 'the counts of new tasks are less than the limit'


        # print('total_counts: %s ' % total_counts)
        #生成关键节点上的 day-count 的键值对
        # day_level   [2,    7,    15,   30]
        # day_percent [25.0, 20.0, 10.0, 5.0]

        for i in range(len(day_level)):
            range_dict[day_level[i]] = day_percent[i]

        # print(range_dict)

        days = collections.OrderedDict() #每天留存比例dict

        #根据关键节点上的 day-count 键值对生成其他day对应的count （根据首尾节点的值计算平均值）

        for i in range(2, 31):

            for key in day_level:
                if i == key:
                    days[i] = range_dict[key]
                    break
                    # print('index: %s' % day_level.index(key))
                elif i > key:
                    continue
                elif i < key:
                    forward = day_level[day_level.index(key) - 1] # 找到day_level中的当前key的前一个key值 因为day_level中没有相同的值，所以这个方法可行，如果有相同的值，每次index都返回当前list中的第一个，会引发错误
                    forward_value = range_dict[forward]
                    # print('forward_value: %s ' % forward_value)
                    next_value = range_dict[key]
                    avrage_slice = (forward_value - next_value) / (key - forward) # 平均切片
                    slice_result = forward_value - (i - forward) * avrage_slice
                    # print('slice_result %s' % slice_result)
                    days[i] = round(slice_result, 2)
                    break

        # print(days)
        #处理每天留存比例dict
        for key in days.keys():
            days[key] = round((days[key] * total_counts) / 100, 0) # 先圆整，再转为int值，这样不会出现小于0的现象
            # days[key] = int((days[key] * total_counts) / 100)
        print(days)
        #遍历dict 从value的最小值到最大值，如果本次的和上次的value相等，则不变，如果本次的比上次多，则求差值后从数据库中选取相应个数改变它们的last_time即可

        day = []
        remain_counts = []

        # days ([(2, 12.0), (3, 12.0), (4, 12.0), (5, 11.0), (6, 10.0), (7, 10.0), (8, 9.0), (9, 9.0), (10, 8.0), (11, 8.0), (12, 7.0), 
        # (13, 6.0), (14, 6.0), (15, 5.0), (16, 5.0), (17, 5.0), (18, 4.0), (19, 4.0), (20, 4.0), (21, 4.0), (22, 4.0), (23, 4.0), (24, 4.0), 
        # (25, 3.0), (26, 3.0), (27, 3.0), (28, 3.0), (29, 3.0), (30, 2.0)])

        for key in days.keys():
            day.append(key)
            if days[key] == 0:
                days[key] = 1
            remain_counts.append(int(days[key]))

        print('day: %s' % day)
        print('remain_counts: %s' % remain_counts)

        # day:           [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
        # remain_counts: [25,24,23,22,21,20,18,17,16, 15, 13, 12, 11, 10,  9,  9,  9,  8,  8,  8,  7,  7,  7,  6,  6,  6,  5, 5,  5]

        for i in range(len(remain_counts) - 1, -1, -1): #倒序遍历

            if i == (len(remain_counts) - 1): #最后一天的那一个
                #从数据库中随机取出remain_counts[i]对应的条目,
                status = 1
                remain_items = await RemainTask.selectByTableLimit(task_name, 'create_time', status, remain_counts[i])
                print(remain_items)
                for remain_item in remain_items:
                    last_date = remain_item.create_time + datetime.timedelta(days = (day[i] - 1))
                    remain_item.last_date = last_date
                    remain_item.status = 2; # 1-> 2 表示这个新增已经可以使用
                    print(remain_item.last_date)
                    await remain_item.update_by_table(task_name)

            else:
                if remain_counts[i] <= remain_counts[i + 1]:
                    continue
                elif remain_counts[i] > remain_counts[i + 1]:
                    print('>>')
                    div_counts = remain_counts[i] - remain_counts[i + 1]
                    status = 1
                    remain_items = await RemainTask.selectByTableLimit(task_name, 'create_time', status, div_counts)
                    for remain_item in remain_items:
                        last_date = remain_item.create_time + datetime.timedelta(days = (day[i] - 1))
                        remain_item.last_date = last_date
                        remain_item.status = 2; # 1-> 2 表示这个新增已经可以使用
                        print(remain_item.last_date)
                        await remain_item.update_by_table(task_name)
        return 'success'

    else:
        return 'failed'
    

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

@get('/rand_device')
async def get_random_deviceInfo():
    result = await ExDeviceInfo.selectRandom()
    k = JSONEncoder().encode(result)
    return k
    #return json.dumps(result.__dict__, ensure_ascii = False)
    #return result
    #return result.simSerialNumber

@get('/rd_device')
async def generate_random_deviceInfo():
    #从模板库里读取一条数据
    base_deviceInfo = await DeviceInfo.selectRandom()
    #随机修改该数据
    ex_deviceInfo = ExDeviceInfo()
    #保存到扩展库中
    ex_deviceInfo.density = base_deviceInfo.density
    ex_deviceInfo.dpi = base_deviceInfo.dpi
    ex_deviceInfo.scaleDensity = base_deviceInfo.scaleDensity
    ex_deviceInfo.board = base_deviceInfo.board
    ex_deviceInfo.brand = base_deviceInfo.brand
    ex_deviceInfo.bootloader = base_deviceInfo.bootloader
    ex_deviceInfo.display = base_deviceInfo.display
    ex_deviceInfo.device = base_deviceInfo.device
    ex_deviceInfo.fingerPrint = base_deviceInfo.fingerPrint
    ex_deviceInfo.hardwear = base_deviceInfo.hardwear
    ex_deviceInfo.manufacturer = base_deviceInfo.manufacturer
    ex_deviceInfo.model = base_deviceInfo.model
    ex_deviceInfo.product = base_deviceInfo.product
    ex_deviceInfo.relea = base_deviceInfo.relea
    ex_deviceInfo.sdk = base_deviceInfo.sdk
    ex_deviceInfo.sdkInt = base_deviceInfo.sdkInt
    ex_deviceInfo.widthPixels = base_deviceInfo.widthPixels
    ex_deviceInfo.heightPixels = base_deviceInfo.heightPixels
    ex_deviceInfo.width = base_deviceInfo.width
    ex_deviceInfo.height = base_deviceInfo.height
    ex_deviceInfo.version = base_deviceInfo.version
    ex_deviceInfo.tags = base_deviceInfo.tags
    ex_deviceInfo.phoneTime = base_deviceInfo.phoneTime
    ex_deviceInfo.phoneType = base_deviceInfo.phoneType
    ex_deviceInfo.phoneUser = base_deviceInfo.phoneUser
    ex_deviceInfo.host = base_deviceInfo.host
    ex_deviceInfo.radioVersion = base_deviceInfo.radioVersion
    ex_deviceInfo.codeName = base_deviceInfo.codeName
    ex_deviceInfo.incremental = base_deviceInfo.incremental
    ex_deviceInfo.buildID = base_deviceInfo.buildID

    ex_deviceInfo.bestProvider = 'network'
    ex_deviceInfo.gclGetCid = -1
    ex_deviceInfo.gclGetLac = -1
    ex_deviceInfo.gclGetPsc = 0
    ex_deviceInfo.cellLocation = '[-1,-1,0]'
    ex_deviceInfo.deviceId = DevGenerator.getDeviceId()
    ex_deviceInfo.androidid = DevGenerator.getAndroidId()
    ex_deviceInfo.networkOperator, ex_deviceInfo.networkOperatorName, ex_deviceInfo.simOperator, ex_deviceInfo.simOperatorName, ex_deviceInfo.subscriberId = DevGenerator.getFive()
    ex_deviceInfo.networkType = 0
    ex_deviceInfo.simSerialNumber = DevGenerator.get_simSerialNumber()
    ex_deviceInfo.getSerial = DevGenerator.get_serial()
    ex_deviceInfo.dataActivity = 0
    wifi_name = DevGenerator.get_wifi_name()
    ex_deviceInfo.extraInfo = wifi_name
    ex_deviceInfo.ssid = wifi_name
    ex_deviceInfo.reason = ''
    ex_deviceInfo.subType = 0
    ex_deviceInfo.subTypeName = ''
    ex_deviceInfo.type = 1
    ex_deviceInfo.typeName = 'WIFI'
    ex_deviceInfo.macAddress = DevGenerator.randomAddress()
    ex_deviceInfo.bssid = DevGenerator.randomAddress()
    ex_deviceInfo.ipAddress = DevGenerator.get_random_ip()
    ex_deviceInfo.networkId = 0
    ex_deviceInfo.rssi = DevGenerator.get_rssi()
    ex_deviceInfo.rotation = 0
    ex_deviceInfo.line1Number = ''

    rows = await ex_deviceInfo.save()
    #返回json字符串给客户端

    if rows == 1:

        logging.info('save ex_deviceInfo success')

        ret_deviceInfo = await ExDeviceInfo.selectSpecCls('idenf', ex_deviceInfo.idenf)

        logging.info('exDeviceInfo: %s' % ex_deviceInfo.idenf)

        logging.info('ret_deviceInfo %s' % ret_deviceInfo)

        if ret_deviceInfo:
            ret_deviceInfo.ret = 'success'
            return ret_deviceInfo
        else:
            return {'ret':'failure'}
    else:
        logging.info('save ex_deviceInfo failure')
        return {'ret':'failure'}


@post('/api/check')
async def check_by_idenf(* ,idenf):
    print('check by idenf: %s' % idenf)
    deviceInfo = await DeviceInfo.find(idenf)
    print('deviceInfo dpi: %s' % deviceInfo.dpi)
    print('deviceInfo idenf: %s' % deviceInfo.idenf)
    return deviceInfo

@get('/getById')
async def get_by_id(*, id):
    deviceInfo = await ExDeviceInfo.findById(id)
    #k = JSONEncoder.encode(deviceInfo)
    return deviceInfo

# @get('/newTask')
# def get_new_task(*, task_name):


@post('/api/cc')
async def check_test(*, id):
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
                    level_8_percents,
                    new_limit):
    
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
            level_7_percents = float(level_7_percents),
            level_8_days = int(level_8_days),
            level_8_percents = float(level_8_percents),
            new_limit = int(new_limit)
            )

    # print('task before save %s ' % task)

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


