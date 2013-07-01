#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import logging
import socket
import datetime
import json
import socket

"""
This module creates a logging handler than can send messages to ElasticSearch via UDP.
The format specified here is based on the open LogStash format: https://github.com/logstash/logstash/wiki/logstash's-internal-message-format
Messages stored in LogStash format are easy to view using the Kibana application: http://kibana.org/about.html#graph

I used sample code for sending UDP packets identified on the official Python wiki
as a starting point for the wire protocol: http://wiki.python.org/moin/UdpCommunication

Inspiration (and non-UDP concept code) via Pete Hoffman:
https://github.com/hoffmann/stash/blob/master/stash.py

Common use should look something like this:
    stasher = StashUdpHandler()
    my_tags = ['delicious','crispy','bacon',]
    logger = logging.getLogger(tags=my_tags)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(stasher)
    logger.debug("This is StashUDP. Have fun logging!")

Have fun! abe@thehumangeo.com
"""

LOG_LEVELS = {  0:'NOT SET',
                10:'DEBUG',
                20:'INFO',
                30:'WARNING',
                40:'ERROR',
                50:'CRITICAL'
             }

class StashUdpHandler(logging.Handler):
    """
    Creates a logging handler that can be used to pass messages to ElasticSearch (formatted according to the LogStash format).
    """
    def __init__(self, connection=None, whitelist=None, blacklist=None,record_type='record',fields=None,source=None,source_host=None,tags=None):
        logging.Handler.__init__(self)
        self.setLevel(logging.DEBUG)
        #TODO: make it easier to configure udp_host and udp_port
        self.udp_host = '192.168.1.7'
        self.udp_port = 9700
        if blacklist is None:
            blacklist = set()
            blacklist.add('funcName')
            blacklist.add('created')
            blacklist.add('msecs')
            blacklist.add('name')
            blacklist.add('processName')
            blacklist.add('relativeCreated')
            blacklist.add('thread')
            blacklist.add('threadName')
            blacklist.add('msg')
        self.whitelist = whitelist
        self.blacklist = blacklist
        self.record_type = record_type
        self.fields = fields
        self.source = source
        self.source_host = source_host
        self.tags = tags
        #don't include debug output
        self.debug = False
        #do try to look up the local ip address
        self.lookup_ip = True

    @property
    def index_name(self):
        """
        This magic string variable is the name of the index used by:
        ElasticSearch, LogStash, Kibana and related tools.
        """
        return 'logstash-'+datetime.date.today().strftime('%Y.%m.%d')

    def get_ip_address(self):
        """
        Return the IP address of the machine that is using stash_udp.
        Based on this recipe: http://goo.gl/E7Okx
        """
        try:
            ip_address = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1]
            ipv4 = ip_address[0]
            if self.source_host == None:
                self.source_host = ipv4
            return ipv4
        except:
            #TODO: add some exception handling to identify the IP address
            return ''

    def emit(self, record):
        """
        Overrides logging method emit.
        """
        if self.whitelist is None:
            d = { k: record.__dict__[k] for k in record.__dict__ if k not in self.blacklist }
        else:
            d = { k: record.__dict__[k] for k in record.__dict__ if k in self.whitelist and k not in self.blacklist }
        if self.lookup_ip:
            d['ip_address'] = self.get_ip_address()
        entry = {
            "@fields": d,
            "@message": record.msg,
            "@source": self.source,
            "@source_host": self.source_host,
            "@source_path": "/",
            "@tags": self.tags,
            "@timestamp": datetime.datetime.utcnow().isoformat(),
            "@type": self.record_type}
        #self.index(entry, self.index_name, self.record_type)
        self.index(entry)

    def index(self,entry,):
        """
        This method actually puts the content into ElasticSearch, by sending a packet
        to port UDP_PORT (9700 by default) on the target server.
        """
        index_json = """{ "index": {"_index": "%s", "_type": "%s"} }""" %(self.index_name, self.record_type)
        text_message = json.dumps(entry)
        wire_message = "%s\n%s\n"%(index_json,text_message)
        if self.debug:
            print wire_message
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        recd = s.sendto(wire_message,(self.udp_host,self.udp_port))
        s.close()
