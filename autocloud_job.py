#!/usr/bin/env python

from autocloud.models import init_model, JobDetails
import datetime
import os
import sys
import json
import subprocess
from retask import Queue


def handle_err(session, data, out, err, ret_code):
    """
    Prints the details and exits.
    :param out:
    :param err:
    :param ret_code:
    :return: None
    """
    if ret_code:
        # Update DB first.
        data.status = u'f'
        timestamp = datetime.datetime.now()
        data.last_updated = timestamp
        session.commit()
        # Now print
        print(out, err)
        print("Return code: %d" % ret_code)
        sys.exit(ret_code)


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

def auto_job(taskid, image_url):
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
    handle_err(session, data, out, err, ret_code)
    print(out)
    data.status = u's'
    timestamp = datetime.datetime.now()
    data.last_updated = timestamp
    session.commit()


def main():
    jobqueue = Queue('jobqueue')
    jobqueue.connect()
    while True:
        task = jobqueue.wait()
        print(task.data)
        auto_job(task.data['buildid'], task.data['image_url'])


if __name__ == '__main__':
    main()