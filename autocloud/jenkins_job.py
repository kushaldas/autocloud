#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from requests import exceptions as req_exceptions
from jenkinsapi.jenkins import Jenkins
from jenkinsapi import utils as j_utils

# Default configuration
log = logging.getLogger("fedmsg")


def create_jenkins_instance(base_url, username=None, token=None):
    """
    Create Jenkins Instance Object
    """
    try:
        requester = j_utils.requester.Requester(username=username,
                                                password=token,
                                                baseurl=base_url,
                                                ssl_verify=False)
        jenkins_instance = Jenkins(base_url, requester=requester)
        return jenkins_instance
    except req_exceptions.HTTPError as err:
        log.error(err)
    return None


def build_job(jenkins_instance, param, job_name):
    """
    Run specified upstream job for sanity check

    :args jenkins_instance: Jenkins Instance Object
    :args param: Parameter dictionary
    :args test_job: String for test jobs which are separated by newline

    :return: build result list
    """
    if not jenkins_instance:
        return None
    if job_name not in jenkins_instance.keys():
        log.error("%s Job is not available", job_name)
        return None
    else:
        job_object = jenkins_instance.get_job(job_name)
        log.info("Invoking %s Job", job_name)
        running_job = job_object.invoke(securitytoken='test', block=True,
                                        build_params=param)
        log.info("Job %s Executed", job_name)
        build_obj = running_job.get_build()
        job_state = build_obj.is_good()
        job_status = build_obj.get_status()
        job_result = build_obj.baseurl
        if not job_state:
            log.warn("%s is %s, Check %s", job_name, job_status,
                     job_result)
    return [job_state, job_status, job_result]
