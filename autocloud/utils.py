# -*- coding: utf-8 -*-

import autocloud

def get_image_url(result):
    url_template = "{file_location}/{file_name}"
    images_list = [f for f in task_result['files'] if f.endswith('.qcow2')]
    if not images_list:
        return None

    file_name = images_list[0]

    task_id = task_result['task_id']

    # extension to base URL to exact file directory
    koji_url_extension = "/{}/{}".format(str(task_id)[3:], str(task_id))
    full_file_location = autocloud.BASE_KOJI_TASK_URL + koji_url_extension

    return url_template.format(file_location=full_file_location,
                               file_name=file_name)
