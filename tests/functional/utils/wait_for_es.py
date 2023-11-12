import time

from elasticsearch import Elasticsearch
from settings import test_settings

if __name__ == '__main__':
    es_client = Elasticsearch(hosts=test_settings.es_url, verify_certs=False)
    print('ES checking:')
    while True:
        if es_client.ping():
            print('ES - is ok')
            break
        print('waiting for ES')
        time.sleep(1)
