# -*- coding: utf-8 -*-

import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('/etc/autocloud/autocloud.cfg')

KOJI_SERVER_URL = config.get('autocloud', 'koji_server_url')
