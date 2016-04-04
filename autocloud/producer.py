# -*- coding: utf-8 -*-

import fedmsg
import logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


def publish_to_fedmsg(topic, compose_url, compose_id, status, job_id, release):
    """ Publish the message to fedmsg with image_url, image_name, status and
    build_id
    """
    try:
        fedmsg.publish(topic=topic, modname="autocloud", msg={
            'compose_url': compose_url,
            'compos_id': compose_id,
            'status': status,
            'job_id': job_id,
            'release': release,
        })
    except Exception as err:
        log.error(err)
