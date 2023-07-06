import json
import logging

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


class ElasticConsumer:
    def __init__(self, elastic_settings):
        self.es = Elasticsearch(
            f"http://{elastic_settings.ELASTIC_HOST}:{elastic_settings.ELASTIC_PORT}"
        )
        self.settings = elastic_settings
        self.index = self.settings.MOVIES_INDEX

    def create_index(self):
        if not self.es.indices.exists(index=self.index):

            with open(self.settings.SETTINGS_FILE) as file:
                settings = json.load(file)

            with open(self.settings.MAPPINGS_FILE) as file:
                mappings = json.load(file)

            data = {"settings": settings, "mappings": mappings}

            response = self.es.indices.create(
                index=self.index,
                headers={"Content-Type": "application/json"},
                body=data,
            )
            if response["acknowledged"]:
                logging.info(
                    f"Index '{self.index}' successfully created in Elasticsearch."
                )
            else:
                logging.error(f"Error creating index '{self.index}'.")
        else:
            logging.debug(f"Index '{self.index}' already exists in Elasticsearch.")

    def insert_request(self, body):
        response = bulk(self.es, body)
        if response:
            logging.info("Successfully loaded in Elasticsearch.")
