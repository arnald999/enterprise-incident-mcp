from datetime import datetime
from enum import StrEnum

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from enterprise_incident_mcp.db.base import Base


class IncidentEventType(StrEnum):
    INCIDENT_CREATED = "INCIDENT_CREATED"
    INCIDENT_ASSIGNED = "INCIDENT_ASSIGNED"
    INCIDENT_UPDATED = "INCIDENT_UPDATED"
    INCIDENT_CLOSED = "INCIDENT_CLOSED"


class IncidentEvent(Base):
    __tablename__ = "incident_events"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    incident_id: Mapped[str] = mapped_column(
        String(32),
        ForeignKey("incidents.id"),
        nullable=False,
    )

    event_type: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    message: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )