import json
from datetime import datetime
from typing import Optional
from uuid import UUID

from core.config import elastic_settings
from pydantic import BaseModel


class Movie(BaseModel):
    id: str
    title: str
    rating: Optional[float]
    type: str
    description: Optional[str] = ""
    created: datetime
    updated_at: datetime


class Transformer:
    def transform_data(self, data_list: list):
        body = []
        for data in data_list:
            data_etl_json = dict(Movie(**dict(data)))
            data_etl_json["created"] = data_etl_json["created"].strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            data_etl_json["updated_at"] = data_etl_json["updated_at"].strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            data = {
                "_index": elastic_settings.MOVIES_INDEX,
                "_id": data_etl_json.get("id"),
                "_source": json.dumps(data_etl_json, ensure_ascii=False),
            }
            body.append(data)
        return body
