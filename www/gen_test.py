#!/usr/bin/env python3
# coding=utf-8


from dev_generator import DevGenerator

result = DevGenerator.getDeviceId()
print(result)

a,b,c,d,e = DevGenerator.getFive()
print(a + b + c + d + e)

serial = DevGenerator.get_serial()
print(serial)

androidid = DevGenerator.getAndroidId()
print(androidid)

randomAddress = DevGenerator.randomAddress()
print(randomAddress)

randomIp = DevGenerator.get_random_ip()
print(randomIp)

randomTime = DevGenerator.get_random_time()
print('randomtime %s' % randomTime)

simSerialNumber = DevGenerator.get_simSerialNumber()
print(simSerialNumber)

wifiName = DevGenerator.get_wifi_name()
print(wifiName)

rssi = DevGenerator.get_rssi()
print(rssi)




