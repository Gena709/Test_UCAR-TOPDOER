from pydantic import BaseModel, ConfigDict
from datetime import datetime


class Pydantic_Incident(BaseModel):
    id: int | None
    description: str
    status_id: int
    source: str
    created_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


class Pydantic_Incident_Updater(BaseModel):
    id: int | None
    status_id: int
