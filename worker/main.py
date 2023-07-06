import asyncio
import logging

import asyncpg
from core.config import postgres_settings
from core.http_client import Client, get_client_session
from core.logging_setup import init_logger
from utils.load import PostgreSQLConsumer
from utils.parser import Parser
from utils.transform import Transformer

init_logger()


async def main():
    client = Client(await get_client_session())
    parser = Parser(client)
    transformer = Transformer()
    consumer = PostgreSQLConsumer(
        await asyncpg.connect(
            user=postgres_settings.POSTGRES_USER,
            password=postgres_settings.POSTGRES_PASSWORD,
            host=postgres_settings.POSTGRES_HOST,
            port=postgres_settings.POSTGRES_PORT,
            database=postgres_settings.POSTGRES_DB,
        )
    )
    batch = 50
    data_to_load = []
    async for data in parser.collect_films_data():
        data_to_load.append(await transformer.transform_data(data))
        if len(data_to_load) >= batch:
            await consumer.insert_movie(data_to_load)
            logging.info(f"-- some new movies was found and loaded --")
            data_to_load = []
    if data_to_load:
        await consumer.insert_movie(data_to_load)
        logging.info(f"-- some new movies was found and loaded --")


if __name__ == "__main__":
    logging.info("-- Parsing is running --")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    # loop.close()
