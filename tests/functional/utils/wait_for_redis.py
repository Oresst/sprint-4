import time

from redis import Redis
from redis.exceptions import ConnectionError
from settings import test_settings

if __name__ == '__main__':
    r = Redis(test_settings.redis_host, test_settings.redis_port, socket_connect_timeout=1)
    print('Redis checking:')
    while True:
        try:
            r.ping()
            print('Redis - is ok')
            break
        except ConnectionError:
            print('waiting for Redis')
            time.sleep(1)
