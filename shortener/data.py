import os
import urlparse
import redis
import time
from datetime import datetime, timedelta


class DataHandle:
    def __init__(self):
        redis_url = os.getenv('REDIS_URL')
        if not redis_url:
            raise RuntimeError('Set up Redis first.')
        urlparse.uses_netloc.append('redis')
        url = urlparse.urlparse(redis_url)
        self.r = redis.StrictRedis(host=url.hostname, port=url.port, db=0, password=url.password)

    @staticmethod
    def generate_url_id():
        dt = datetime.now()
        timestamp = int(time.mktime(dt.timetuple()))
        return timestamp

    @staticmethod
    def get_expiration_date():
        dt = datetime.now() + timedelta(days=1)
        return dt.date()
