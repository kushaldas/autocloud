# -*- coding: utf-8 -*-

import fedmsg

def publish_to_fedmsg(topic, image_url, image_name, status, buildid):
    """ Publish the message to fedmsg with image_url, image_name, status and
    build_id
    """
    fedmsg.publish(topic=topic, modname="autocloud", msg={
        'image_url': image_url,
        'image_name': image_name,
        'status': status,
        'buildid': buildid,
    })
