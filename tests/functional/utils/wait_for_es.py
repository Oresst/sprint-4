import time

from elasticsearch import Elasticsearch
from settings import test_app_settings

if __name__ == "__main__":
    es_client = Elasticsearch(hosts=f"http://{test_app_settings.elastic_host}:{test_app_settings.elastic_port}")

    while True:
        if es_client.ping():
            break
        time.sleep(1)

    es_client.close()
