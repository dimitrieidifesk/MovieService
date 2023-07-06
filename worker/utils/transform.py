import uuid
from datetime import datetime

from core.models import Movie


class Transformer:
    async def transform_data(self, data: dict):
        data["id"] = uuid.uuid4()
        data["created"] = datetime.now()
        data["updated_at"] = datetime.now()
        if not data["rating"]:
            data["rating"] = 0.0
        return Movie(**data)
