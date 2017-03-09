#!/usr/bin/env python3
# coding=utf-8

# import asyncio, logging
# import aiomysql
import os
import random
import string
import struct, socket
import time
import datetime

RANDOM_IP_POOL = ['192.168.10.220/0']

class DevGenerator(object):

	@classmethod
	def getDeviceId(cls):
		deviceList = [random.choice(string.digits) for i in range(15)]
		deviceId = ''.join(deviceList)
		return deviceId

	@classmethod
	def getAndroidId(cls):
		androidList = [random.choice(string.ascii_letters + string.digits) for i in range(16)]
		androidid = ''.join(androidList)
		return androidid

	@classmethod
	def getFive(cls):
		rd = random.randint(1,3)

		subscriberList = [random.choice(string.digits) for i in range(10)]

		if rd == 1:
		    networkOperator = '46000'
		    networkOperatorName = 'CMCC'
		    simOperator = '46000'
		    simOperatorName = 'CMCC'
		    subscriberId = '46000' + ''.join(subscriberList)

		    return [networkOperator, networkOperatorName, simOperator, simOperatorName, subscriberId]

		elif rd == 2:
		    networkOperator = '46001'
		    networkOperatorName = 'CHINA UNICOM'
		    simOperator = '46001'
		    simOperatorName = 'CHINA UNICOM'
		    subscriberId = '46001' + ''.join(subscriberList)
		    return [networkOperator, networkOperatorName, simOperator, simOperatorName, subscriberId]

		else:
		    networkOperator = '46003'
		    networkOperatorName = 'CHINA TELECOM'
		    simOperator = '46003'
		    simOperatorName = 'CHINA TELECOM'
		    subscriberId = '46003' + ''.join(subscriberList)
		    return [networkOperator, networkOperatorName, simOperator, simOperatorName, subscriberId]


	@classmethod
	def randomAddress(cls):
	    addressList = []
	    for i in range(1, 7):
	        randomStr = ''.join(random.sample('0123456789abcdef', 2))
	        addressList.append(randomStr)
	    randomAddress = ':'.join(addressList)
	    return randomAddress

	@classmethod
	def get_random_ip(cls):
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

	@classmethod
	def get_time(cls):
	    a = '2010-01-01 10:00:00'
	    time.strptime(a, '%Y-%m-%d %H:%M:%S')
	    now = time.mktime(time.strptime(a,'%Y-%m-%d %H:%M:%S'))
	    return now

	@classmethod
	def get_random_time(cls):
	    start = int(cls.get_time())
	    end = int(time.time())
	    rd = random.randint(100,999)
	    result = str(random.randint(start, end)) + str(rd)
	    return result

	@classmethod
	def get_simSerialNumber(cls):
		simSerialList = [random.choice(string.digits) for i in range(16)]
		simSerialNumber = '8986' + ''.join(simSerialList)
		return simSerialNumber

	@classmethod
	def get_serial(cls):
		rd = random.randint(10,20)
		serialList = [random.choice(string.ascii_letters + string.digits) for i in range(rd)]
		getSerial = ''.join(serialList)
		return getSerial

	@classmethod
	def get_wifi_name(cls):
		rd = random.randint(7,15)
		wifiNameList = [random.choice(string.ascii_letters + string.digits) for i in range(rd)]
		wifiNameStr = ''.join(wifiNameList)
		return wifiNameStr

	@classmethod
	def get_rssi(cls):
		return random.randint(-100, -55)