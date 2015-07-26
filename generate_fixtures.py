#!/usr/bin/env python
import sys
import json
import logging
import requests
import fedmsg

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

url = 'https://apps.fedoraproject.org/datagrepper/raw'
params = {
    'topic': 'org.fedoraproject.prod.buildsys.task.state.change',
    'rows_per_page': 100,
}

with open('fixtures.json', 'w') as outfile:
    counter = 1
    builds = []

    while True:
        try:
            params.update({'page': counter})

            logger.debug('Sending request to datagrepper')
            resp = requests.get(url, params=params)

            if resp.status_code != 200:
                continue

            logger.debug('Fetched request from datagrepper')
            results = json.loads(resp.content)
            raw_messages = results.get('raw_messages')
            msg_ids = []
            for raw_message in raw_messages:
                # This code is taken from http://git.io/vqaAQ
                print '-'*50, raw_message['msg_id']
                msg_info = raw_message['msg']['info']
                if msg_info['method'] == 'image':
                    if isinstance(msg_info["children"], list):
                        for child in msg_info["children"]:
                            if child["method"] == "createImage":
                                if child["state"] == 2:
                                    #fedmsg.publish(msg=raw_message['msg'], topic='buildsys.task.state.change')
                                    json.dump(raw_message, outfile)
                                    print raw_message['msg_id']
                                    builds.append(child['id'])
            counter += 1
        except KeyboardInterrupt:
            choice = int(raw_input("Enter your choice (0:continue, 1:quit)\n"))
            if choice:
                sys.exit(0)
            else:
                logger.info(builds)
                print '\n'.join(msg_ids)
