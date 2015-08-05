# -*- coding: utf-8 -*-

from retask import Task
from retask import Queue

import autocloud
from autocloud.models import init_model, JobDetails

import datetime
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
    jobqueue = Queue('jobqueue')
    jobqueue.connect()

    session = init_model()
    timestamp = datetime.datetime.now()
    for info in infox:
        task = Task(info)
        jobqueue.enqueue(task)

        jd = JobDetails(
            taskid=info['buildid'],
            status='q',
            created_on=timestamp,
            user='admin',
            last_updated=timestamp)
        session.add(jd)
    session.commit()


def get_image_url(task_list_output, task_relpath):
    url_template = "{file_location}/{file_name}"
    images_list = [f for f in task_list_output if f.endswith('.qcow2')]
    if not images_list:
        return None

    file_name = images_list[0]

    # extension to base URL to exact file directory
    full_file_location = autocloud.BASE_KOJI_TASK_URL + task_relpath

    return url_template.format(file_location=full_file_location,
                               file_name=file_name)
