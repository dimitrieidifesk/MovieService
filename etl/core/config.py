from pydantic import BaseSettings, Field


class ETLSettings(BaseSettings):
    BATCH: int = Field(500)

    class Config:
        case_sensitive = True
        env_file = "config.env"


class ElasticSettings(BaseSettings):
    ELASTIC_HOST: str
    ELASTIC_PORT: int
    MOVIES_INDEX: str
    SETTINGS_FILE: str
    MAPPINGS_FILE: str

    class Config:
        case_sensitive = True
        env_file = "config.env"


class PostgreSQLSettings(BaseSettings):
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_MOVIES_TABLE: str = Field("movies")

    class Config:
        case_sensitive = True
        env_file = "config.env"


class RedisSettings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: str

    class Config:
        case_sensitive = True
        env_file = "config.env"


elastic_settings = ElasticSettings()
redis_settings = RedisSettings()
postgres_settings = PostgreSQLSettings()
etl_setting = ETLSettings()
