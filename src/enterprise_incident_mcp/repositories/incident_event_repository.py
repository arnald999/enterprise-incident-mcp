from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from enterprise_incident_mcp.domain.incidents.event_models import IncidentEvent


class IncidentEventRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, event: IncidentEvent) -> IncidentEvent:
        self.session.add(event)
        await self.session.commit()
        await self.session.refresh(event)
        return event

    async def get_timeline(self, incident_id: str) -> list[IncidentEvent]:
        result = await self.session.execute(
            select(IncidentEvent)
            .where(IncidentEvent.incident_id == incident_id)
            .order_by(IncidentEvent.created_at.asc())
        )

        return list(result.scalars().all())