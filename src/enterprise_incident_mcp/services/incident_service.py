from datetime import UTC, datetime
from uuid import uuid4

from enterprise_incident_mcp.domain.incidents.models import Incident, IncidentStatus
from enterprise_incident_mcp.domain.incidents.schemas import IncidentCreate
from enterprise_incident_mcp.repositories.incident_repository import IncidentRepository


class IncidentService:
    def __init__(self, repository: IncidentRepository):
        self.repository = repository

    async def create_incident(self, payload: IncidentCreate) -> Incident:
        now = datetime.now(UTC)

        incident = Incident(
            id=f"INC-{uuid4().hex[:8].upper()}",
            title=payload.title,
            description=payload.description,
            severity=payload.severity,
            status=IncidentStatus.OPEN,
            owner=payload.owner,
            service=payload.service,
            created_at=now,
            updated_at=now,
        )

        return await self.repository.create(incident)

    async def list_incidents(self) -> list[Incident]:
        return await self.repository.list_all()

    async def get_incident(self, incident_id: str) -> Incident | None:
        return await self.repository.get_by_id(incident_id)