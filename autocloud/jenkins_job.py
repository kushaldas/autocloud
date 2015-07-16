#!/usr/bin/env python

import logging
import ConfigParser
import sys
import os

from argparse import ArgumentParser
from requests import exceptions as req_exceptions
from jenkinsapi.jenkins import Jenkins
from jenkinsapi import utils as j_utils

# Default configuration
DEFAULT_CONF_LOCATION = '/etc/autocloud_config.ini'

logging.basicConfig(format='%(levelname)s:%(module)s:%(funcName)s:%(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


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
        logger.error(err)
        sys.exit(1)


def build_job(jenkins_instance, param, job_name):
    """
    Run specified upstream job for sanity check

    :args jenkins_instance: Jenkins Instance Object
    :args param: Parameter dictionary
    :args test_job: String for test jobs which are separated by newline

    :return: build result list
    """
    if job_name not in jenkins_instance.keys():
        logger.error("%s Job is not available", job_name)
        sys.exit(1)
    else:
        job_object = jenkins_instance.get_job(job_name)
        logger.info("Invoking %s Job", job_name)
        running_job = job_object.invoke(securitytoken='test', block=True,
                                        build_params=param)
        logger.info("Job %s Executed", job_name)
        build_obj = running_job.get_build()
        job_state = build_obj.is_good()
        job_status = build_obj.get_status()
        job_result = build_obj.baseurl
        if not job_state:
            logger.warn("%s is %s, Check %s", job_name, job_status,
                        job_result)
    return [job_state, job_status, job_result]


def parse_config(config_file):
    '''Takes config file location and get each section

       :args config_file: Config file like default
       :return: different section dictionary
    '''
    if os.path.isfile(config_file):
        config = ConfigParser.RawConfigParser()
        config.read(config_file)
        section_values = {}
        for section in config.sections():
            section_values[section] = dict((key, value) for (key, value) in
                                           config.items(section))
        return section_values

    else:
        logger.error("%s is not present", config_file)
        sys.exit(1)


def main():
    ''' Main function
    '''

    parser = ArgumentParser(prog='Jenkins job information')
    parser.add_argument('-j', '--jenkins_config_file',
                        help='Configuration file, sample project_deploy.cfg')
    args = parser.parse_args()
    if not args.jenkins_config_file:
        j_configs = parse_config(DEFAULT_CONF_LOCATION)
    else:
        j_configs = parse_config(os.path.join(os.path.dirname(__file__),
                                 args.jenkins_config_file))
    print j_configs
    jenkins_instance = create_jenkins_instance(
                            j_configs['jenkins'].get('baseurl'),
                            j_configs['jenkins'].get('username'),
                            j_configs['jenkins'].get('token'),
                          )
    param = {}
    job_results = build_job(jenkins_instance, param,
                            j_configs['jenkins'].get('job_name'))
    print job_results

if __name__ == '__main__':
    main()
