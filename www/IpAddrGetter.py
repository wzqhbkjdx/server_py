#!/usr/bin/env python3
# coding=utf-8

class IpGetter(object):

	def process_request(self, request):
		try:
			real_ip = request.META['HTTP_X_FORWARDED_FOR']
		except KeyError:
			print("IpGettingException")
			return None
		else:
			real_ip = real_ip.split(',')[0]
			request.META['REMOTE_ADDR'] = real_ip
			return real_ip