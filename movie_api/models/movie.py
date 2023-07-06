import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class BaseModelOrjson(BaseModel):
    id: str

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Movie(BaseModelOrjson):
    title: str
    rating: float


class MovieDetail(BaseModelOrjson):
    title: str
    rating: float | None
    description: str | None
    type: str
