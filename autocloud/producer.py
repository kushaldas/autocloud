# -*- coding: utf-8 -*-

import fedmsg
import logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


def publish_to_fedmsg(topic, image_url, image_name, status, buildid, job_id,
                      release):
    """ Publish the message to fedmsg with image_url, image_name, status and
    build_id
    """
    try:
        fedmsg.publish(topic=topic, modname="autocloud", msg={
            'image_url': image_url,
            'image_name': image_name,
            'status': status,
            'buildid': buildid,
            'job_id': job_id,
            'release': release,
        })
    except Exception as err:
        log.error(err)
