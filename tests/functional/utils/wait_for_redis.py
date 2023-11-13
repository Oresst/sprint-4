import sys
import logging

import backoff
import coloredlogs

from redis import Redis
from redis.exceptions import ConnectionError
from settings import test_settings, WAIT_GEN_KWARGS
from utils.exceptions import BackoffTryOneMoreTime

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

fmt = '%(asctime)s %(levelname)s %(message)s'

coloredlogs.install(
    level=logging.DEBUG, logger=LOGGER, isatty=True, stream=sys.stdout,
    fmt=fmt,
    datefmt='%Y-%m-%d %H:%M:%S.%f'
)


@backoff.on_exception(backoff.expo, BackoffTryOneMoreTime, logger=LOGGER, **WAIT_GEN_KWARGS)
def check_redis(client: Redis):
    try:
        r.ping()
    except ConnectionError:
        raise BackoffTryOneMoreTime


if __name__ == '__main__':
    r = Redis(test_settings.redis_host, test_settings.redis_port, socket_connect_timeout=1)
    check_redis(r)
