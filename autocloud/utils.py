# -*- coding: utf-8 -*-

from retask import Task
from retask import Queue

import autocloud
import json

import logging
log = logging.getLogger("fedmsg")

def get_redis_config():
    """ Get the redis server configuration in json
    """
    config_path = autocloud.REDIS_CONFIG_FILEPATH

    try:
        with open(config_path) as fobj:
            config = json.load(fobj)
            return config
    except Exception, e:
        log.debug('get_redis_config', str(e), 'error')
    return None


def produce_jobs(infox):
    """ Queue the jobs into jobqueue
    :args infox: list of dictionaries contains the image url and the buildid
    """
    config = get_redis_config()
    jobqueue = Queue('jobqueue', config)
    jobqueue.connect()

    for info in infox:
        task = Task(info)
        jobqueue.enqueue(task)


def get_image_url(task_result):
    url_template = "{file_location}/{file_name}"
    images_list = [f for f in result['files'] if f.endswith('.qcow2')]
    if not images_list:
        return None

    file_name = images_list[0]

    task_id = result['task_id']

    # extension to base URL to exact file directory
    koji_url_extension = "/{}/{}".format(str(task_id)[3:], str(task_id))
    full_file_location = autocloud.BASE_KOJI_TASK_URL + koji_url_extension

    return url_template.format(file_location=full_file_location,
                               file_name=file_name)
