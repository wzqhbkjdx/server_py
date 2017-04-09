#!/usr/bin/env python
# coding=utf-8

import logging
import os

logging.basicConfig(filename = os.path.join(os.getcwd(),'log.txt'), level = logging.DEBUG)
logging.debug('this is a message')
