import backoff
import psycopg2


class PostgreSQLProducer:
    def __init__(self, cursor_pg, postgres_settings) -> None:
        self.cursor_pg = cursor_pg
        self.postgres_settings = postgres_settings

    @backoff.on_exception(
        backoff.expo,
        (psycopg2.OperationalError, psycopg2.DatabaseError),
        max_tries=5,
        max_time=10,
    )
    def extract_movie(self, time):
        self.cursor_pg.execute(
            f"SELECT id, title, rating, type, description, "
            f"created, updated_at "
            f"FROM {self.postgres_settings.POSTGRES_MOVIES_TABLE} "
            f"WHERE updated_at > '{time}' "
            f"GROUP BY id ORDER BY updated_at;"
        )

    def fetch_movies(self, batch: int):
        return self.cursor_pg.fetchmany(batch)
