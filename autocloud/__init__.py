# -*- coding: utf-8 -*-

import ConfigParser
import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__name__))

name = '/etc/autocloud/autocloud.cfg'
if not os.path.exists(name):
    raise Exception('Please add a proper config file under /etc/autocloud/')

default = {'host': '127.0.0.1', 'port': 5000}
config = ConfigParser.RawConfigParser(default)
config.read(name)

KOJI_SERVER_URL = config.get('autocloud', 'koji_server_url')
BASE_KOJI_TASK_URL = config.get('autocloud', 'base_koji_task_url')


HOST = config.get('autocloud', 'host')
PORT = config.getint('autocloud', 'port')
DEBUG = config.getboolean('autocloud', 'debug')

SQLALCHEMY_URI = config.get('sqlalchemy', 'uri')

VIRTUALBOX = config.getboolean('autocloud', 'virtualbox')
