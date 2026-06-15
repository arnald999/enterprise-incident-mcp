from datetime import datetime
from uuid import uuid4

from datetime import datetime
from enterprise_incident_mcp.domain.incidents.event_models import (
    IncidentEvent,
    IncidentEventType,
)
from enterprise_incident_mcp.repositories.incident_event_repository import (
    IncidentEventRepository,
)
from enterprise_incident_mcp.domain.incidents.models import Incident, IncidentStatus
from enterprise_incident_mcp.domain.incidents.schemas import IncidentCreate
from enterprise_incident_mcp.repositories.incident_repository import IncidentRepository


class IncidentService:
    def __init__(
        self,
        repository: IncidentRepository,
        event_repository: IncidentEventRepository | None = None,
    ):
        self.repository = repository
        self.event_repository = event_repository

    async def create_incident(self, payload: IncidentCreate) -> Incident:
        now = datetime.utcnow()

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

        created_incident = await self.repository.create(incident)
        await self._record_event(
            incident_id=created_incident.id,
            event_type=IncidentEventType.INCIDENT_CREATED,
            message=f"Incident created with severity {created_incident.severity}",
        )

        return created_incident

    async def list_incidents(self) -> list[Incident]:
        return await self.repository.list_all()

    async def get_incident(self, incident_id: str) -> Incident | None:
        return await self.repository.get_by_id(incident_id)
    
    async def update_incident(
        self,
        incident_id: str,
        status: str | None = None,
        severity: str | None = None,
        owner: str | None = None,
    ) -> Incident:
        incident = await self.repository.update(
            incident_id=incident_id,
            status=status,
            severity=severity,
            owner=owner,
        )

        if incident is None:
            raise ValueError(f"Incident not found: {incident_id}")
        
        await self._record_event(
            incident_id=incident.id,
            event_type=IncidentEventType.INCIDENT_UPDATED,
            message=(
                f"Incident updated. "
                f"status={incident.status}, severity={incident.severity}, owner={incident.owner}"
            ),
        )

        return incident

    async def assign_incident(
        self,
        incident_id: str,
        owner: str,
    ) -> Incident:
        incident = await self.repository.update(
            incident_id=incident_id,
            owner=owner,
        )

        if incident is None:
            raise ValueError(f"Incident not found: {incident_id}")

        await self._record_event(
            incident_id=incident.id,
            event_type=IncidentEventType.INCIDENT_ASSIGNED,
            message=f"Incident assigned to {owner}",
        )

        return incident
    
    async def _record_event(
        self,
        incident_id: str,
        event_type: IncidentEventType,
        message: str,
    ) -> None:
        if self.event_repository is None:
            return

        event = IncidentEvent(
            incident_id=incident_id,
            event_type=event_type,
            message=message,
            created_at=datetime.utcnow(),
        )

        await self.event_repository.create(event)