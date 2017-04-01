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

	@classmethod
	def get_iphone_buildversion(cls):
		buildversion_list = ['11B651','11A501','11B511','11D257','11D167','11A465']
		rs = random.randint(0, len(buildversion_list) - 1)
		return buildversion_list[rs]

	@classmethod
	def get_spec_num_str(cls, num, str):
		randomStr =  [random.choice(str) for i in range(num)]
		rs = ''.join(randomStr)
		return rs

	@classmethod
	def get_iphone_dev_product(cls):
		ip_dev_product_list = ['iPhone4,1','iphone6,2','iphone5,2','iphone6,1','iphone7,1']
		rs = random.randint(0, len(ip_dev_product_list) - 1)
		return ip_dev_product_list[rs]

	@classmethod
	def get_ios_version(cls):
		ios_version_list = ['7.0.1', '7.0.2', '7.1.1', '7.1.2', '8.0.1', '8.0.2', '8.1.1', '8.1.2', '9.0.1', '9.0.2', '9.1','9.2','10.0.2','10.1','10.2','10.3']
		rs = random.randint(0, len(ios_version_list) - 1)
		return ios_version_list[rs]

	@classmethod
	def get_igrimacekey(cls):
		return random.randint(1490854310, 1490890000)

	@classmethod
	def get_rj_rj2(cls):
		head = random.randint(75, 77)
		return '118.' + str(head) + cls.get_spec_num_str(13,'0123456789')

	@classmethod
	def get_rw_rw2(cls):
		second = random.randint(4,5)
		return '32.0' + str(second) + cls.get_spec_num_str(13,'0123456789')


# if __name__ == '__main__':
# 	addr = DevGenerator.randomAddress()
# 	androidid = DevGenerator.getAndroidId()
# 	buildversion = DevGenerator.get_iphone_buildversion()
# 	spec_num_str = DevGenerator.get_spec_num_str(5, '0123456789ABCDEF')
# 	iad1 = DevGenerator.get_spec_num_str(8, '0123456789ABCDEF')
# 	iad2 = DevGenerator.get_spec_num_str(4, '0123456789ABCDEF')
# 	iad3 = DevGenerator.get_spec_num_str(4, '0123456789ABCDEF')
# 	iad4 = DevGenerator.get_spec_num_str(4, '0123456789ABCDEF')
# 	iad5 = DevGenerator.get_spec_num_str(12, '0123456789ABCDEF')
# 	rs = iad1 + '-' + iad2 + '-' + iad3 + '-' + '-' + iad4 + '-' + iad5

# 	name = DevGenerator.get_spec_num_str(8, string.ascii_letters + string.digits)

# 	ios_version = DevGenerator.get_ios_version()

# 	rand_time = DevGenerator.get_random_time()

# 	igrimacekey = DevGenerator.get_igrimacekey()

# 	rw = DevGenerator.get_rw_rw2()
# 	print(rw)