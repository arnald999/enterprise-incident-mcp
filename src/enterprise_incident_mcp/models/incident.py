from datetime import datetime, timezone
from enum import StrEnum
from pydantic import BaseModel, Field


class Severity(StrEnum):
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    P4 = "P4"


class IncidentStatus(StrEnum):
    OPEN = "OPEN"
    INVESTIGATING = "INVESTIGATING"
    MITIGATED = "MITIGATED"
    CLOSED = "CLOSED"


class Incident(BaseModel):
    id: str
    title: str
    description: str
    severity: Severity
    status: IncidentStatus = IncidentStatus.OPEN
    owner: str | None = None
    service: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class CreateIncidentRequest(BaseModel):
    title: str
    description: str
    severity: Severity
    service: str | None = None
    owner: str | None = None


class UpdateIncidentRequest(BaseModel):
    incident_id: str
    status: IncidentStatus | None = None
    severity: Severity | None = None
    owner: str | None = None
    comment: str | None = None
