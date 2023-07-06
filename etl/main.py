from contextlib import closing
from time import sleep

import backoff
import psycopg2
import psycopg2.extras
from core.config import elastic_settings, etl_setting, postgres_settings, redis_settings
from core.logging_setup import init_logger
from db.elasticsearch import ElasticConsumer
from db.postgresql import PostgreSQLProducer
from db.state import *
from healthcheck import health_check
from psycopg2.extras import DictCursor
from utils.extract import Extractor
from utils.load import Loader
from utils.transform import Transformer

init_logger()


@backoff.on_exception(
    backoff.expo,
    (psycopg2.OperationalError, psycopg2.DatabaseError),
    max_tries=5,
    max_time=10,
)
def run_etl():
    dsl = {
        "dbname": postgres_settings.POSTGRES_DB,
        "user": postgres_settings.POSTGRES_USER,
        "password": postgres_settings.POSTGRES_PASSWORD,
        "host": postgres_settings.POSTGRES_HOST,
        "port": postgres_settings.POSTGRES_PORT,
    }
    with closing(psycopg2.connect(**dsl, cursor_factory=DictCursor)) as pg_conn:
        cursor_pg = pg_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        state = State(RedisFileStorage(redis_settings))
        producer = PostgreSQLProducer(cursor_pg, postgres_settings)
        extractor = Extractor(producer, state)
        transformer = Transformer()
        loader = Loader(ElasticConsumer(elastic_settings))
        try:
            while True:
                data = extractor.extract(
                    table=postgres_settings.POSTGRES_MOVIES_TABLE,
                    batch=etl_setting.BATCH,
                )
                print(data)
                if data:
                    body = transformer.transform_data(data)
                    loader.load_data(body=body)
                sleep(5)

        finally:
            cursor_pg.close()
            pg_conn.close()
            state.close_conn()


if __name__ == "__main__":
    while not health_check():
        sleep(2)
    run_etl()
