from datetime import datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from enterprise_incident_mcp.db.base import Base


class IncidentEmbedding(Base):
    __tablename__ = "incident_embeddings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    incident_id: Mapped[str] = mapped_column(
        String(32),
        ForeignKey("incidents.id"),
        nullable=False,
        index=True,
    )

    content: Mapped[str] = mapped_column(Text, nullable=False)

    embedding: Mapped[list[float]] = mapped_column(
        Vector(384),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)