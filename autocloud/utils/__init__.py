# -*- coding: utf-8 -*-

from retask.task import Task
from retask.queue import Queue

import autocloud
from autocloud.models import init_model, JobDetails
from autocloud.producer import publish_to_fedmsg

import datetime

import logging
log = logging.getLogger("fedmsg")


def produce_jobs(infox):
    """ Queue the jobs into jobqueue
    :args infox: list of dictionaries contains the image url and the buildid
    """
    jobqueue = Queue('jobqueue')
    jobqueue.connect()

    session = init_model()
    timestamp = datetime.datetime.now()
    for info in infox:
        jd = JobDetails(
            taskid=info['buildid'],
            status='q',
            created_on=timestamp,
            user='admin',
            last_updated=timestamp,
            release=info['release'],
            arch=info['arch'],
            family=info['family'],
        )
        session.add(jd)
        session.commit()

        job_details_id = jd.id
        log.info('Save {jd_id} to database'.format(jd_id=job_details_id))

        info.update({'job_id': jd.id})
        task = Task(info)
        jobqueue.enqueue(task)
        log.info('Enqueue {jd_id} to redis'.format(jd_id=job_details_id))

        publish_to_fedmsg(topic='image.queued', image_url=info['image_url'],
                          image_name=info['name'], status='queued',
                          buildid=info['buildid'], job_id=info['job_id'],
                          release=info['release'])


def get_image_url(task_list_output, task_relpath):
    if autocloud.VIRTUALBOX:
        supported_image_ext = ('.vagrant-virtualbox.box',)
    else:
        supported_image_ext = ('.qcow2', '.vagrant-libvirt.box')
    url_template = "{file_location}/{file_name}"
    images_list = [f for f in task_list_output if f.endswith(supported_image_ext)]
    if not images_list:
        return None

    file_name = images_list[0]

    # extension to base URL to exact file directory
    full_file_location = autocloud.BASE_KOJI_TASK_URL + task_relpath

    return url_template.format(file_location=full_file_location,
                               file_name=file_name)

def get_image_name(image_name):
    if 'vagrant' in image_name.lower():
        if autocloud.VIRTUALBOX:
            image_name = '{image_name}-Virtualbox'.format(image_name=image_name)
        else:
            image_name = '{image_name}-Libvirt'.format(image_name=image_name)
    return image_name
