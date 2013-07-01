#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import logging
from stash_udp import StashUdpHandler

TARGET_IP = '172.20.9.20'
ES_UDP_PORT = 9700

def example1():
    stasher = StashUdpHandler()
    stasher.udp_host = TARGET_IP
    stasher.udp_port = ES_UDP_PORT
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(stasher)
    logger.debug("Add another thing to Kibana!")

def example2():
    my_tags = ['delicious','crispy','bacon',]
    stasher = StashUdpHandler(tags = my_tags)
    stasher.udp_host = TARGET_IP
    stasher.udp_port = ES_UDP_PORT
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(stasher)
    logger.debug("Iocaine powder. I'm sure of it.")

example1()

