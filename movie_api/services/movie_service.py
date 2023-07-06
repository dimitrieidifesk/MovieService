from functools import lru_cache
from typing import Dict, List, Optional
from uuid import UUID

from core.config import elastic_settings
from db.elastic import get_elastic
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends


class MovieService:
    def __init__(self, storage):
        self.elastic = storage

    async def search_movie(self, query, page_number: int, page_size: int):
        """Поиск фильма по названию"""
        search_query = {"query_string": {"default_field": "title", "query": query}}
        print(1)
        docs = await self.elastic.search(
            index=elastic_settings.MOVIES_INDEX,
            body={
                "_source": ["id", "title", "rating"],
                "from": (page_number - 1) * page_size,
                "size": page_size,
                "query": search_query,
            },
            params={"filter_path": "hits.hits._source"},
        )
        if not docs:
            return None
        return [film["_source"] for film in docs["hits"]["hits"]]

    async def get_data_by_id(self, id: str) -> Optional[Dict]:
        """Получить фильм по его id"""
        try:
            doc = await self.elastic.get(elastic_settings.MOVIES_INDEX, id)
        except NotFoundError:
            return None
        return doc["_source"]

    async def get_data_list(
        self, sort: str, page_number: int, page_size: int
    ) -> Optional[List[Dict]]:
        """Список всех фильмов с сортировкой"""
        if sort[0] == "-":
            sort = {sort[1:]: "desc"}
        else:
            sort = {sort: "asc"}
        docs = await self.elastic.search(
            index=elastic_settings.MOVIES_INDEX,
            body={
                "_source": ["id", "title", "rating"],
                "sort": sort,
                "from": (page_number - 1) * page_size,
                "size": page_size,
            },
            params={"filter_path": "hits.hits._source"},
        )
        if not docs:
            return None
        return [movie["_source"] for movie in docs["hits"]["hits"]]


@lru_cache()
def get_movie_service(
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> MovieService:
    return MovieService(elastic)
