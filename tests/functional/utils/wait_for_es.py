import sys
import logging

import backoff
import coloredlogs
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError
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
def check_es(client: Elasticsearch):
    try:
        if not client.ping():
            raise BackoffTryOneMoreTime
    except ConnectionError:
        LOGGER.error('ES connection error')
        raise BackoffTryOneMoreTime


if __name__ == '__main__':
    es_client = Elasticsearch(hosts=test_settings.es_url, verify_certs=False)
    check_es(es_client)
