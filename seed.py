from autocloud.models import init_model, JobDetails
import datetime
import hashlib
import random

if __name__ == '__main__':
    session = init_model()
    timestamp = datetime.datetime.now()

    for i in range(100):
        timestamp += datetime.timedelta(seconds=random.randint(1, 500))
        jd = JobDetails(
            taskid=hashlib.md5(str(timestamp)).hexdigest()[:8],
            status=random.choice('sfar'),
            created_on=timestamp,
            user='admin',
            last_updated=timestamp)
        session.add(jd)
    session.commit()

