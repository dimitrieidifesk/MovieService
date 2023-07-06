import asyncpg
import backoff
from asyncpg.exceptions import CannotConnectNowError, TooManyConnectionsError
from core.config import postgres_settings


class PostgreSQLConsumer:
    def __init__(self, connection) -> None:
        self.connection: asyncpg.connection = connection

    @backoff.on_exception(
        backoff.expo,
        (TooManyConnectionsError, CannotConnectNowError),
        max_tries=5,
        max_time=10,
    )
    async def insert_movie(self, data: list):
        values = [
            (
                movie.id,
                movie.title,
                movie.rating,
                movie.type,
                movie.description,
                movie.created,
                movie.updated_at,
            )
            for movie in data
        ]

        return await self.connection.executemany(
            f"INSERT INTO {postgres_settings.POSTGRES_MOVIES_TABLE} "
            f"(id, title, rating, type, description, "
            f"created, updated_at) "
            f"VALUES ($1, $2, $3, $4, $5, $6, $7) "
            f"ON CONFLICT (title) DO NOTHING;",
            values,
        )
