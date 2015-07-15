# -*- coding: utf-8 -*-

import fedmsg.consumers

import logging
log = logging.getLogger("fedmsg")

class AutoCloudConsumer(fedmsg.consumers.FedmsgConsumer):
    topic = 'org.fedoraproject.prod.buildsys.task.state.change'
    config_key = 'autocloud.consumer.enabled'

    def __init__(self, *args, **kwargs):
        super(AutoCloudConsumer, self).__init__(*args, **kwargs)

    def consume(self, msg):
        msg_info = msg["body"]["msg"]["info"]

        print msg_info
