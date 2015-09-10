# -*- coding: utf-8 -*-
from autocloud.models import init_model, JobDetails
from autocloud.producer import publish_to_fedmsg
from autocloud import TIMEOUT
import datetime
import os
import sys
import json
import subprocess
import signal
import time
from retask.queue import Queue

import logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

def get_pid(process_name):
    """
    Return process pid
    """
    return subprocess.check_output(["pidof", process_name])


def handler(signum, frame):
   log.debug("signal handler called with signal %s" signum
   pid = int(get_pid('gedit').strip())
   os.kill(pid, signal.SIGKILL)

def handle_err(session, data, out, err):
    """
    Prints the details and exits.
    :param out:
    :param err:
    :return: None
    """
    # Update DB first.
    data.status = u'f'
    data.output = "%s: %s" % (out, err)
    timestamp = datetime.datetime.now()
    data.last_updated = timestamp
    session.commit()
    log.debug("%s: %s", out, err)


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

def refresh_storage_pool():
    '''Refreshes libvirt storage pool.

    http://kushaldas.in/posts/storage-volume-error-in-libvirt-with-vagrant.html
    '''
    out, err, retcode = system('virsh pool-list')
    lines = out.split('\n')
    if len(lines) > 2:
        for line in lines[2:]:
            words = line.split()
            if len(words) == 3:
                if words[1] == 'active':
                    system('virsh pool-refresh {0}'.format(words[0]))

def image_cleanup(image_path):
    """
    Delete the image if it is processed or if there is any exception occur

    :param basename: Absoulte path for image
    """
    if os.path.exists(image_path):
        try:
            os.remove(image_path)
        except OSError as e:
            log.error('Error: %s - %s.', e.filename, e.strerror)


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
    job_type = 'vm'

    session = init_model()
    timestamp = datetime.datetime.now()
    data = None
    try:
        data = session.query(JobDetails).filter(JobDetails.taskid == str(taskid)).first()
        data.status = u'r'
        data.last_updated = timestamp
    except Exception as err:
        log.error("%s" % err)
        log.error("%s: %s", taskid, image_url)
    session.commit()

    publish_to_fedmsg(topic='image.running', image_url=image_url,
                      image_name=image_name, status='running', buildid=taskid)

    # Now we have job queued, let us start the job.

    # Step 1: Download the image
    basename = os.path.basename(image_url)
    image_path = '/var/run/autocloud/%s' % basename
    out, err, ret_code = system('wget %s -O %s' % (image_url, image_path))
    if ret_code:
        image_cleanup(image_path)
        handle_err(session, data, out, err)
        log.debug("Return code: %d" % ret_code)
        publish_to_fedmsg(topic='image.failed', image_url=image_url,
                        image_name=image_name, status='failed', buildid=taskid)
        return

    # Step 2: Create the conf file with correct image path.
    if basename.find('libvirt') == -1:
        conf = {"image": "file:///var/run/autocloud/%s" % basename,
                "name": "fedora",
                "password": "passw0rd",
                "ram": 2048,
                "type": "vm",
                "user": "fedora"}

    else: # We now have a Vagrant job.
        conf = {
            "name": "fedora",
            "type": "vagrant",
            "image": "file:///var/run/autocloud/%s" % basename,
            "ram": 2048,
            "user": "vagrant",
            "port": "22"
        }
        job_type = 'vagrant'

        #Now let us refresh the storage pool
        refresh_storage_pool()

    with open('/var/run/autocloud/fedora.json', 'w') as fobj:
        fobj.write(json.dumps(conf))

    system('cp /etc/autocloud/fedora.txt /var/run/autocloud/fedora.txt')

    cmd = 'tunir --job fedora --config-dir /var/run/autocloud/ --stateless'
    if basename.find('Atomic') != -1 and job_type == 'vm':
        cmd = 'tunir --job fedora --config-dir /var/run/autocloud/ --stateless --atomic'
    # Now run tunir
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(TIMEOUT)
    out, err, ret_code = system(cmd)
    if ret_code:
        image_cleanup(image_path)
        handle_err(session, data, out, err)
        log.debug("Return code: %d" % ret_code)
        publish_to_fedmsg(topic='image.failed', image_url=image_url,
                        image_name=image_name, status='failed', buildid=taskid)
        return
    else:
        image_cleanup(image_path)
    signal.alarm(0) # unset alarm

    if job_type == 'vm':
        com_text = out[out.find('/usr/bin/qemu-kvm'):]
    else:
        com_text = out
    data.status = u's'
    timestamp = datetime.datetime.now()
    data.last_updated = timestamp
    data.output = com_text
    session.commit()

    publish_to_fedmsg(topic='image.success', image_url=image_url,
                      image_name=image_name, status='success', buildid=taskid)

def main():
    jobqueue = Queue('jobqueue')
    jobqueue.connect()
    while True:
        task = jobqueue.wait()
        log.debug("%s", task.data)
        auto_job(task.data)


if __name__ == '__main__':
    main()
