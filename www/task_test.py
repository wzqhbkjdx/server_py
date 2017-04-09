#!/usr/bin/env python3
# coding=utf-8

import asyncio
import orm
from models import Task

task = Task(task_name = 'test_task_1', 
			ip_repeat_days = 20,
			level_2_days = 2,
			level_2_percents = 0.3,
			level_3_days = 3,
			level_3_percents = 0.25,
			level_4_days = 4,
			level_4_percents = 0.2,
			level_5_days = 5,
			level_5_percents = 0.2,
			level_6_days = 6,
			level_6_percents = 0.15,
			level_7_days = 7,
			level_7_percents = 0.1,
			level_8_days = 0,
			level_8_percents = 0,
			)

loop = asyncio.get_event_loop()
loop.run_until_complete(orm.get_pool(loop))
loop.run_until_complete(task.save())