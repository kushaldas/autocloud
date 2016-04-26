#!/usr/bin/env python
import os
import sys
import json
import logging
import requests
import fedmsg

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

url = 'https://apps.fedoraproject.org/datagrepper/raw'
params = {
    'topic': 'org.fedoraproject.prod.pungi.compose.status.change',
    'rows_per_page': 100,
}

fixtures = []

for page in range(3, 20):
    params.update({'page': page})
    resp = requests.get(url, params=params)
    print page

    results = resp.json()
    fixtures = []

    for result in results['raw_messages']:
        if result['msg'] in ['FINISHED_INCOMPLETE', 'FINISHED']:
            fixtures.append(result)

with open('fixtures.json', 'r') as f:
    f.write(json.dumps(fixtures))
