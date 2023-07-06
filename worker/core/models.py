from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class Movie(BaseModel):
    id: UUID
    title: str
    rating: Optional[float]
    type: str
    description: Optional[str]
    created: datetime
    updated_at: datetime

    class Config:
        validate_all = True
