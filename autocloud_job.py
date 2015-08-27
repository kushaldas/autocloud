#!/usr/bin/env python

from autocloud.models import init_model, JobDetails
from autocloud.producer import publish_to_fedmsg
import datetime
import os
import sys
import json
import subprocess
from retask import Queue


def handle_err(session, data, out, err):
    """
    Prints the details and exits.
    :param out:
    :param err:
    :return: None
    """
    # Update DB first.
    data.status = u'f'
    timestamp = datetime.datetime.now()
    data.last_updated = timestamp
    session.commit()
    # Now print
    print(out, err)


def system(cmd):
    """
    Runs a shell command, and returns the output, err, returncode

    :param cmd: The command to run.
    :return:  Tuple with (output, err, returncode).
    """
    ret = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
    out, err = ret.communicate()
    returncode = ret.returncode
    return out, err, returncode

def auto_job(task_data):
    """
    This fuction queues the job, and then executes the tests,
    updates the db as required.

    :param taskid: Koji taskid.
    :param image_url: URL to download the fedora image.
    :return:
    """
    # TODO:
    # We will have to update the job information on DB, rather
    # than creating it. But we will do it afterwards.

    taskid = task_data.get('buildid')
    image_url = task_data.get('image_url')
    image_name = task_data.get('name')

    session = init_model()
    timestamp = datetime.datetime.now()
    data = None
    try:
        data = session.query(JobDetails).filter(JobDetails.taskid == taskid).first()
        data.status = u'r'
        data.last_updated = timestamp
    except Exception as err:
        print(err)
        print(taskid, image_url)
        sys.exit(-1)
    session.commit()

    publish_to_fedmsg(topic='image.running', image_url=image_url,
                      image_name=image_name, status='running', buildid=taskid)

    # Now we have job queued, let us start the job.

    # Step 1: Download the image
    basename = os.path.basename(image_url)
    out, err, ret_code = system('wget %s -O /var/run/autocloud/%s' % (image_url, basename))
    handle_err(session, data, out, err, ret_code)

    # Step 2: Create the conf file with correct image path.
    conf = {"image": "file:///var/run/autocloud/%s" % basename,
            "name": "fedora",
            "password": "passw0rd",
            "ram": 2048,
            "type": "vm",
            "user": "fedora"}
    with open('/var/run/autocloud/fedora.json', 'w') as fobj:
        fobj.write(json.dumps(conf))


    with open('/var/run/autocloud/fedora.txt', 'w') as fobj:
        fobj.write('''curl -O https://kushal.fedorapeople.org/tunirtests.tar.gz
tar -xzvf tunirtests.tar.gz
sudo python -m unittest tunirtests.cloudtests
sudo systemctl stop crond.service
@@ sudo systemctl disable crond.service
@@ sudo reboot
SLEEP 30
sudo python -m unittest tunirtests.cloudservice.TestServiceManipulation
@@ sudo reboot
SLEEP 30
sudo python -m unittest tunirtests.cloudservice.TestServiceAfter''')


    cmd = 'tunir --job fedora --config-dir /var/run/autocloud/ --stateless'
    if basename.find('Atomic') != -1:
        cmd = 'tunir --job fedora --config-dir /var/run/autocloud/ --stateless --atomic'
    # Now run tunir
    out, err, ret_code = system(cmd)
    if ret_code:
        handle_err(session, data, out, err)
        print("Return code: %d" % ret_code)
        publish_to_fedmsg(topic='image.failed', image_url=image_url,
                        image_name=image_name, status='failed', buildid=taskid)
        return

    print(out)
    data.status = u's'
    timestamp = datetime.datetime.now()
    data.last_updated = timestamp
    session.commit()

    publish_to_fedmsg(topic='image.success', image_url=image_url,
                      image_name=image_name, status='success', buildid=taskid)

def main():
    jobqueue = Queue('jobqueue')
    jobqueue.connect()
    while True:
        task = jobqueue.wait()
        print(task.data)
        auto_job(task.data)


if __name__ == '__main__':
    main()
