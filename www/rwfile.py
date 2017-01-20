#!/usr/bin/env python
# coding=utf-8

import asyncio
import orm
from models import Remain
import random

file = open('thefile.txt')

loop = asyncio.get_event_loop()
loop.run_until_complete(orm.get_pool(loop))

try:
    all_str = file.read().strip('\n')
    print(all_str)
    a = all_str.split(',')
    print(a)
finally:
    file.close()

for str in a:
    print(str)
    r = Remain(num=str)
    loop.run_until_complete(r.save())
    #result = loop.run_until_complete(r.find(1))
    #result = loop.run_until_complete(r.findAll())
    #result = loop.run_until_complete(r.findSpecItem('id',3))
    #result = loop.run_until_complete(Remain.selectMaxId('id'))
    #a = 0
    #for k, v in result.items():
        #a = int(v)
        #print('a: %s' % a)
        #b = random.randint(1,a)
        #print('b: %s' % b)
        #result = loop.run_until_complete(Remain.findSpecItem('id', b))
        #print(result)

    
