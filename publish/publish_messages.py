import json
import fedmsg
import time

with open('publish/fixtures.json', 'r') as infile:
    raw_messages = json.load(infile)
    for raw_message in raw_messages:
        time.sleep(1)
        fedmsg.publish(msg=raw_message['msg'],
                       topic='pungi.compose.status.change')

