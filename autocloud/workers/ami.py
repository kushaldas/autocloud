# -*- coding: utf-8 -*-
# Copyright (C) 2017 Red Hat, Inc.
#
# autocloud is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# bugyou_plugins is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# bugyou_plugins.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors: Sayan Chowdhury  <sayanchowdhury@fedoraproject.org>
#
from datetime import datetime

from retask.queue import Queue

from autocloud.constants import FAILED, SUCCESS
from autocloud.models import init_model, AMIComposeDetails
from autocloud.producer import publish_to_fedmsg
from autocloud.workers.base import AutoCloudBaseWorker

import logging

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


class AMIWorker(AutoCloudBaseWorker):
    """
    Documentation for AMI Worker
    """
    def __enter__(self):
        self.session = init_model()

    def __exit__(self, exc, exc_value, traceback):
        self.session.close()

    def consume(self, msg):
        """
        Consume the messages from ami-jobqueue in Redis and process them.
        """
        ami_id = msg['ami_id']
        region = msg['region']
        compose_id = msg['compose_id']
        job_id = msg['job_id']

        try:
            self.data = self.session.query(AMIComposeDetails).get(str(job_id))
            self.data.status = u'r'
            self.data.last_updated = datetime.now()
        except Exception as err:
            log.error("%s" % err)
            log.error("%s: %s", compose_id)

        """
        cmd = "gotun --ami-id {ami_id} --region {region} --job fedora"\
              "--config /etc/autocloud/config.yaml".format(
                ami_id=ami_id,
                region=region)

        out, err, ret_code = self.system(cmd)
        """
        out, err, ret_code = "", 0, 0

        if ret_code:
            self.handle_err(out, err)
            log.debug("Return code: %d" % ret_code)
            publish_to_fedmsg(topic="ami.test.failed", **{
                'compose_id': compose_id,
                'ami_id': ami_id,
                'region': region,
                'status': FAILED,
            })
        else:
            self.data.status = u'p'
            self.data.output = ''
            self.data.last_updated = datetime.now()
            self.session.commit()

            publish_to_fedmsg(topic="ami.test.passed", **{
                'compose_id': compose_id,
                'ami_id': ami_id,
                'region': region,
                'status': SUCCESS,
            })

    def handle_err(self, out, err):
        """
        Handles the error and stores the output in the database
        """
        self.data.status = u'f'
        self.data.output = '%s: %s' % (out, err)
        timestamp = datetime.now()
        self.data.last_updated = timestamp
        self.session.commit()
        log.debug("%s: %s", out, err)


def main():
    jobqueue = Queue('ami-jobqueue')
    jobqueue.connect()

    while True:
        task = jobqueue.wait()
        task_data = task.data

        with AMIWorker() as worker:
            worker.consume(task_data)


if __name__ == '__main__':
    main()
