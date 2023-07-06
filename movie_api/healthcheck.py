from time import sleep

import requests
from core.config import elastic_settings


def check_elastic(sleep_time):
    elastic_started = False
    elasticsearch_url = (
        f"http://{elastic_settings.ELASTIC_HOST}:{elastic_settings.ELASTIC_PORT}"
    )
    while not elastic_started:
        try:
            response = requests.get(elasticsearch_url)
            if response.status_code == 200:
                print("Elasticsearch active")
                elastic_started = True
                return elastic_started
            else:
                print("Elasticsearch not available")
                sleep(sleep_time)
        except requests.exceptions.ConnectionError:
            print("Elasticsearch not available")
            sleep(sleep_time)


def health_check():
    if check_elastic(4):
        return True
