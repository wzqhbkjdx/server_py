#!/usr/bin/env python
# coding=utf-8

import asyncio
import orm
from models import User, Blog, Comment

#def ormTest():

#u = User(name='Test', email='test@example.com',passwd='1234567890', image='about:blank')
u2 = User(name = 'Hello', email='hello@backyard.com', passwd='kdlskdls', image='about:blank')
loop = asyncio.get_event_loop()
loop.run_until_complete(orm.get_pool(loop))
#loop.run_until_complete(u.save())
loop.run_until_complete(u2.save())
