from time import sleep

import psycopg2
import requests
from core.config import elastic_settings, postgres_settings


def check_elastic(sleep_time):
    elastic_started = False
    elasticsearch_url = (
        f"http://{elastic_settings.ELASTIC_HOST}:{elastic_settings.ELASTIC_PORT}"
    )
    while not elastic_started:
        try:
            response = requests.get(elasticsearch_url)
            if response.status_code == 200:
                print("Elasticsearch available")
                elastic_started = True
                return elastic_started
            else:
                print("Elasticsearch not available")
                sleep(sleep_time)
        except requests.exceptions.ConnectionError:
            print("Elasticsearch not available")
            sleep(sleep_time)


def check_postgreSQL(sleep_time):
    dsl = {
        "dbname": postgres_settings.POSTGRES_DB,
        "user": postgres_settings.POSTGRES_USER,
        "password": postgres_settings.POSTGRES_PASSWORD,
        "host": postgres_settings.POSTGRES_HOST,
        "port": postgres_settings.POSTGRES_PORT,
    }
    postgres_started = False
    while not postgres_started:
        try:
            conn = psycopg2.connect(**dsl)
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result[0] == 1:
                print("PostgreSQL available")
                postgres_started = True
                return postgres_started
            else:
                print("PostgreSQL not available")
                sleep(sleep_time)
            cursor.close()
            conn.close()
        except (Exception, psycopg2.Error) as error:
            print("Error connecting to PostgreSQL:", error)
            sleep(sleep_time)


def health_check():
    if check_elastic(4) and check_postgreSQL(4):
        return True
