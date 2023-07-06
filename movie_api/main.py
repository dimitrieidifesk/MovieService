import logging
from time import sleep

import uvicorn
from api.v1 import movie_handlers
from core.config import elastic_settings, project_settings
from core.logger import LOGGING
from db import elastic
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from healthcheck import health_check

app = FastAPI(
    title=project_settings.PROJECT_NAME,
    description="Фильмы, собранные парсером с удобным полнотекстовым поиском, пагинацией и сортировкой",
    version=project_settings.PROJECT_VERSION,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    elastic.es = AsyncElasticsearch(
        hosts=[f"{elastic_settings.ELASTIC_HOST}:{elastic_settings.ELASTIC_PORT}"]
    )


@app.on_event("shutdown")
async def shutdown():
    await elastic.es.close()


app.include_router(movie_handlers.router, prefix="/api/v1/movies", tags=["Фильмы"])


if __name__ == "__main__":
    while not health_check():
        sleep(2)
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
