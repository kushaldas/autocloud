from autocloud.models import init_model, ComposeJobDetails
import datetime
import hashlib
import random

def r(data):
    return random.choice(data)

if __name__ == '__main__':
    session = init_model()
    timestamp = datetime.datetime.now()

    for i in range(100):
        arch = r(ComposeJobDetails.ARCH_TYPES)
        n = r([0,1,2,3])
        timestamp += datetime.timedelta(seconds=random.randint(1, 500))

        jd = JobDetails(
            taskid=hashlib.md5(str(timestamp)).hexdigest()[:8],
            status=random.choice('sfar'),
            created_on=timestamp,
            user='admin',
            last_updated=timestamp)
        session.add(jd)
    session.commit()

