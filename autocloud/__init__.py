# -*- coding: utf-8 -*-

import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('/etc/autocloud/autocloud.cfg')

KOJI_SERVER_URL = config.get('autocloud', 'koji_server_url')
BASE_KOJI_TASK_URL = config.get('autocloud', 'base_koji_task_url')
REDIS_CONFIG_FILEPATH = config.get('autocloud', 'redis_config_filepath')
JENKINS_BASE_URL = config.get('jenkins', 'baseurl')
JENKINS_USERNAME = config.get('jenkins', 'username')
JENKINS_TOKEN = config.get('jenkins', 'token')
JENKINS_JOB_NAME = config.get('jenkins', 'job_name')

SQLALCHEMY_URI = config.get('sqlalchemy', 'uri')
