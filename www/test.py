#!/usr/bin/env python
# coding=utf-8

import asyncio
import orm
from models import User, Blog, Comment, DeviceInfo
import random
import string
import struct, socket
import time
import datetime


#u = User(name='Test', email='test@example.com',passwd='1234567890', image='about:blank')
#u2 = User(name = 'Hello', email='hello@backyard.com', passwd='kdlskdls', image='about:blank')
#di = DeviceInfo(density=2.0, dpi = 320.0, scaleDensity=2.0) 
#u.id = '0014851368047077e7b332ae8b447b3b651f7617e76db6d000'
#u.created_at = 12345
#u.admin = False
loop = asyncio.get_event_loop()
loop.run_until_complete(orm.get_pool(loop))
deviceInfo = loop.run_until_complete(DeviceInfo.findSpecCls('id',15))

print(deviceInfo.idenf)

rd = random.randint(1,3)

#bestProvider
#networkOperator networkOperatorName simOperator simOperatorName subscriberId

subscriberList = [random.choice(string.digits) for i in range(10)]

if rd == 1:
    print('bestProvider: network')
    deviceInfo.bestProvider = 'network'

    deviceInfo.networkOperator = '46000'
    deviceInfo.networkOperatorName = 'CMCC'
    deviceInfo.simOperator = '46000'
    deviceInfo.simOperatorName = 'CMCC'

    deviceInfo.subscriberId = '46000' + ''.join(subscriberList)
    print(deviceInfo.subscriberId)

elif rd == 2:
    print('bestProvider: passive')
    deviceInfo.bestProvider = 'passive'

    deviceInfo.networkOperator = '46001'
    deviceInfo.networkOperatorName = 'CHINA TELECOM'
    deviceInfo.simOperator = '46001'
    deviceInfo.simOperatorName = 'CHINA TELECOM'

    deviceInfo.subscriberId = '46001' + ''.join(subscriberList)
    print(deviceInfo.subscriberId)

else:
    print('bestProvider: gps')
    deviceInfo.bestProvider = 'gps'

    deviceInfo.networkOperator = '46003'
    deviceInfo.networkOperatorName = 'CHINA UNICOM'
    deviceInfo.simOperator = '46003'
    deviceInfo.simOperatorName = 'CHINA UNICOM'
    
    deviceInfo.subscriberId = '46003' + ''.join(subscriberList)
    print(deviceInfo.subscriberId)

#deviceId
deviceList = [random.choice(string.digits) for i in range(15)]
deviceId = ''.join(deviceList)
print(deviceId)
deviceInfo.deviceId = deviceId

#androidid
androidList = [random.choice(string.ascii_letters + string.digits) for i in range(16)]
androidid = ''.join(androidList)
print(androidid)
deviceInfo.androidid = androidid

#networkType
deviceInfo.networkType = random.randint(1,15)

#simSerialNumber
simSerialList = [random.choice(string.digits) for i in range(15)]
simSerialNumber = '8986' + ''.join(simSerialList)
print(simSerialNumber)
deviceInfo.simSerialNumber = simSerialNumber

#getSerial
serialList = [random.choice(string.ascii_letters + string.digits) for i in range(8)]
deviceInfo.getSerial = ''.join(serialList)
print(deviceInfo.getSerial)


def randomAddress():
    addressList = []
    for i in range(1, 7):
        randomStr = ''.join(random.sample('0123456789abcdef', 2))
        addressList.append(randomStr)
    randomAddress = ':'.join(addressList)
    print(randomAddress)
    return randomAddress

RANDOM_IP_POOL = ['192.168.10.220/0']
def get_random_ip():
    str_ip = RANDOM_IP_POOL[random.randint(0, len(RANDOM_IP_POOL) - 1)] 
    str_ip_addr = str_ip.split('/')[0]
    str_ip_mark = str_ip.split('/')[1]
    ip_addr = struct.unpack('>I', socket.inet_aton(str_ip_addr))[0]
    mask = 0x0
    for i in range(31, 31-int(str_ip_mark), -1):
        mask = mask | (1 << i)
    ip_addr_min = ip_addr & (mask & 0xffffffff)
    ip_addr_max = ip_addr | (~mask & 0xffffffff)
    return socket.inet_ntoa(struct.pack('>I', random.randint(ip_addr_min, ip_addr_max)))



def get_time():
    a = '2010-01-01 10:00:00'
    time.strptime(a, '%Y-%m-%d %H:%M:%S')
    now = time.mktime(time.strptime(a,'%Y-%m-%d %H:%M:%S'))
    return now

def get_random_time():
    start = int(get_time())
    end = int(time.time())
    return random.randint(start, end)



#macAddress
deviceInfo.macAddress = randomAddress()

#bssid
deviceInfo.bssid = randomAddress()

#ipAddress
deviceInfo.ipAddress = get_random_ip()

#networkId
deviceInfo.networkId = random.randint(0, 9)

#rssi
deviceInfo.rssi = random.randint(-100, -55)
print(deviceInfo.rssi)

#phonetime
deviceInfo.phoneTime = get_random_time()
print(deviceInfo.phoneTime)


loop.run_until_complete(deviceInfo.save())


#print(deviceInfo)
#loop.run_until_complete(u.remove())
#loop.run_until_complete(u.save())
#loop.run_until_complete(di.save())
