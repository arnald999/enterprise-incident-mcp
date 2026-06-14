from datetime import datetime
from pydantic import BaseModel


class IncidentCreate(BaseModel):
    title: str
    description: str
    severity: str
    owner: str | None = None
    service: str | None = None


class IncidentUpdate(BaseModel):
    status: str | None = None
    severity: str | None = None
    owner: str | None = None


class IncidentResponse(BaseModel):
    id: str
    title: str
    description: str
    severity: str
    status: str
    owner: str | None
    service: str | None
    created_at: datetime
    updated_at: datetime