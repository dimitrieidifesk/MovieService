from pydantic import BaseSettings, Field


class WorkerSettings(BaseSettings):
    PROXI_FILE_PATH: str = Field("./core/proxies.txt")
    SERVICE_URL: str = Field("https://www.film.ru")

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


postgres_settings = PostgreSQLSettings()
worker_setting = WorkerSettings()
