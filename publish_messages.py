import random
import json
import fedmsg
import time

with open('fixtures.json', 'r') as infile:
    raw_messages = json.load(infile)
    for raw_message in raw_messages:
        number = random.randint(1, 11)
        fedmsg.publish(msg=raw_message['msg'],
                       topic='buildsys.task.state.change')

