import abc
from time import sleep
from typing import Any

import redis


class BaseStorage:
    @abc.abstractmethod
    def save_state(state: dict) -> None:
        pass

    @abc.abstractmethod
    def retrieve_state() -> dict:
        pass

    @abc.abstractmethod
    def close_connection() -> None:
        pass


class RedisFileStorage(BaseStorage):
    def __init__(self, settings):
        self.redis_connection = redis.Redis(
            host=settings.REDIS_HOST, port=settings.REDIS_PORT
        )

    def save_state(self, timestamp):
        self.redis_connection.set("last_timestamp", timestamp)

    def retrieve_state(self):
        return self.redis_connection.get("last_timestamp").decode()

    def close_connection(self):
        self.redis_connection.close()


class State:
    def __init__(self, storage: BaseStorage):
        self.storage = storage

    def set_state(self, timestamp: Any) -> None:
        """Установить состояние"""
        self.storage.save_state(timestamp)

    def get_state(self) -> Any:
        """Получить состояние"""
        return self.storage.retrieve_state()

    def close_conn(self) -> None:
        self.storage.close_connection()
