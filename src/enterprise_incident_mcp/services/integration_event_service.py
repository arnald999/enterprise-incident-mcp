from datetime import datetime

from enterprise_incident_mcp.domain.incidents.event_models import (
    IncidentEvent,
)
from enterprise_incident_mcp.repositories.incident_event_repository import (
    IncidentEventRepository,
)


class IntegrationEventService:
    def __init__(
        self,
        repository: IncidentEventRepository,
    ):
        self.repository = repository

    async def record(
        self,
        incident_id: str,
        event_type: str,
        message: str,
    ) -> None:
        await self.repository.create(
            IncidentEvent(
                incident_id=incident_id,
                event_type=event_type,
                message=message,
                created_at=datetime.utcnow(),
            )
        )