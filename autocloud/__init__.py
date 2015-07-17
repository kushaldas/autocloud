# -*- coding: utf-8 -*-

import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('/etc/autocloud/autocloud.cfg')

KOJI_SERVER_URL = config.get('autocloud', 'koji_server_url')
BASE_KOJI_TASK_URL = config.get('autocloud', 'base_koji_task_url')
REDIS_CONFIG_FILEPATH = config.get('autocloud', 'redis_config_filepath')

SQLALCHEMY_URI = config.get('sqlalchemy', 'uri')
