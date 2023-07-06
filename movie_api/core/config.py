from fastapi import Query
from pydantic import BaseSettings, Field


class ElasticSettings(BaseSettings):
    ELASTIC_HOST: str
    ELASTIC_PORT: int
    MOVIES_INDEX: str
    SETTINGS_FILE: str
    MAPPINGS_FILE: str

    class Config:
        case_sensitive = True
        env_file = "config.env"


class ProjectSettings(BaseSettings):
    PROJECT_NAME: str = Field("Movies")
    PROJECT_VERSION: str = Field("1.0.0")

    class Config:
        case_sensitive = True
        env_file = "config.env"


project_settings = ProjectSettings()
elastic_settings = ElasticSettings()


class CommonQueryParams:
    def __init__(
        self,
        page_number: int | None = Query(default=1, ge=1),
        page_size: int | None = Query(default=10, ge=1, le=50),
    ):
        self.page_number = page_number
        self.page_size = page_size
