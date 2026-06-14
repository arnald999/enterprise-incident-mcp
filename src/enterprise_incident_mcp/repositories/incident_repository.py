from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from enterprise_incident_mcp.domain.incidents.models import Incident


class IncidentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, incident: Incident) -> Incident:
        self.session.add(incident)
        await self.session.commit()
        await self.session.refresh(incident)
        return incident

    async def list_all(self) -> list[Incident]:
        result = await self.session.execute(select(Incident))
        return list(result.scalars().all())

    async def get_by_id(self, incident_id: str) -> Incident | None:
        result = await self.session.execute(
            select(Incident).where(Incident.id == incident_id)
        )
        return result.scalar_one_or_none()