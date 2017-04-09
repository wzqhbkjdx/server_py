#!/usr/bin/env python
# coding=utf-8

import time, os, sched

schedule = sched.scheduler(time.time, time.sleep)

def perform_command(cmd, inc):

	time_out()

	schedule.enter(inc, 0, perform_command, (cmd, inc))
	# os.system(cmd)

def timming_exe(cmd, inc=5):
	schedule.enter(inc, 0, perform_command, (cmd, inc))
	schedule.run()

def time_out():
	print('time out')

print('show time after 10 seconds:')
timming_exe('echo time', 10)