#!/usr/bin/env python
# coding=utf-8

import asyncio
import orm
from models import User, Blog, Comment, DeviceInfo

#def ormTest():

#u = User(name='Test', email='test@example.com',passwd='1234567890', image='about:blank')
#u2 = User(name = 'Hello', email='hello@backyard.com', passwd='kdlskdls', image='about:blank')
di = DeviceInfo(density=2.0, dpi = 320.0, scaleDensity=2.0) 
loop = asyncio.get_event_loop()
loop.run_until_complete(orm.get_pool(loop))
#loop.run_until_complete(u.save())
loop.run_until_complete(di.save())
