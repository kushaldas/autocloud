# -*- coding: utf-8 -*-

import argparse
import ConfigParser
import datetime
import koji
import os

from retask.task import Task
from retask.queue import Queue

import autocloud

from autocloud.models import init_model, JobDetails
from autocloud.utils import get_image_name, get_image_url
from autocloud.producer import publish_to_fedmsg

import logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

def get_koji_details(taskid):

    koji_session = koji.ClientSession(autocloud.KOJI_SERVER_URL)
    task_result = koji_session.getTaskResult(int(taskid))

    name = task_result.get('name')
    name = get_image_name(image_name=name)

    task_relpath = koji.pathinfo.taskrelpath(taskid)
    image_url = get_image_url(task_result.get('files'), task_relpath)

    release = task_result.get('version')

    return {
        'image_url': image_url,
        'name': name,
        'release': release,
    }


def enqueue_job(job_id):
    jobqueue = Queue('jobqueue')
    jobqueue.connect()

    session = init_model()
    try:
        data = session.query(JobDetails).first(str(job_id))
    except:
        log.error("Matching data for job id %s not found" % job_id)
        return None

    taskid = int(data.taskid)
    koji_details = get_koji_details(taskid)
    image_name = koji_details['name']
    image_url = koji_details['image_url']
    release = koji_details['release']

    info = {
        'buildid': taskid,
        'image_url': image_url,
        'name': image_name,
        'release': release,
    }

    task = Task(info)
    jobqueue.enqueue(task)
    log.info('Enqueue {jd_id} to redis'.format(jd_id=job_id))


def abort_job(job_id):
    session = init_model()
    try:
        data = session.query(JobDetails).first(str(job_id))
    except:
        log.error("Matching data for job id %s not found" % job_id)
        return None

    taskid = int(data.taskid)
    koji_details = get_koji_details(taskid)
    image_name = koji_details['name']
    image_url = koji_details['image_url']
    release = koji_details['release']

    data = None
    try:
        data = session.query(JobDetails).get(str(job_id))
        if data.status == 'a':
            log.info('The job with id %s is already aborted.' % job_id)
            return

        data.status = u'a'
        timestamp = datetime.datetime.now()
        data.last_updated = timestamp
    except Exception as err:
        log.error("%s" % err)
        log.error("%s: %s", taskid, image_url)
    session.commit()

    publish_to_fedmsg(topic='image.aborted', image_url=image_url,
                        image_name=image_name, status='aborted',
                        buildid=taskid, job_id=data.id, release=release)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--abort', nargs='*', type=int)
    parser.add_argument('-e', '--enqueue', nargs='*', type=int)
    args = parser.parse_args()

    if args.abort:
        for arg in args.abort:
            abort_job(arg)

    if args.enqueue:
        for arg in args.enqueue:
            enqueue_job(arg)

