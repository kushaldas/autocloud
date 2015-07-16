# -*- coding: utf-8 -*-

import fedmsg.consumers
import koji

from autocloud.utils import get_image_url

import logging
log = logging.getLogger("fedmsg")

class AutoCloudConsumer(fedmsg.consumers.FedmsgConsumer):
    topic = 'org.fedoraproject.prod.buildsys.task.state.change'
    config_key = 'autocloud.consumer.enabled'

    def __init__(self, *args, **kwargs):
        super(AutoCloudConsumer, self).__init__(*args, **kwargs)

    def _get_tasks(self):
        """ Takes a list of koji createImage task IDs and returns dictionary of
        build ids and image url corresponding to that build ids"""

        for build in builds:
            log.info('Got Koji build {0}'.format(build))

        # Create a Koji connection to the Fedora Koji instance
        koji_session = koji.ClientSession(autocloud.KOJI_SERVER_URL)

        image_files = []  # list of full URLs of files

        if len(builds) == 1:
            task_result = koji_session.getTaskResult(builds[0])
            url = get_image_url(task_result)
            if url:
                data = {
                    'buildid': builds[0],
                    'image_url': url
                }
                image_files.append(data)
        elif len(builds) >= 2:
            koji_session.multicall = True
            for build in builds:
                koji_session.getTaskResult(build)
            results = koji_session.multiCall()
            for result in results:
                if not result: continue
                url = get_image_url(result[0])
                if url:
                    data = {
                        'buildid': builds[0],
                        'image_url': url
                    }
                    image_files.append(data)

        return image_files

    def consume(self, msg):
        """ This is called when we receive a message matching the topic. """

        builds = list()  # These will be the Koji build IDs to upload, if any.

        msg_info = msg["body"]["msg"]["info"]

        log.info('Received %r %r' % (msg['topic'], msg['body']['msg_id']))

        # If the build method is "image", we check to see if the child
        # task's method is "createImage".
        if msg_info["method"] == "image":
            if isinstance(msg_info["children"], list):
                for child in msg_info["children"]:
                    if child["method"] == "createImage":
                        # We only care about the image if the build
                        # completed successfully (with state code 2).
                        if child["state"] == 2:
                            builds.append(child["id"])

