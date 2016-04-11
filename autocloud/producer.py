# -*- coding: utf-8 -*-

import fedmsg
import logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


def publish_to_fedmsg(topic, *args, **params):
    """ Publish the message to fedmsg with image_url, image_name, status and
    build_id
    """
    try:
        fedmsg.publish(topic=topic, modname="autocloud", msg=params)
    except Exception as err:
        log.error(err)
