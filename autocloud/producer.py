#!/usr/bin/env python
# -*- coding: utf-8 -*-

import fedmsg


def publish_to_fedmsg(topic, image_url, image_name, status, build_id):
    """ Publish the message to fedmsg with image_url, image_name, status and
    build_id
    """
    fedmsg.publish(topic=topic, modname="autocloud", msg={
        'image_url': image_url,
        'image_name': image_name,
        'status': status,
        'build_id': build_id,
    })
