from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from enterprise_incident_mcp.domain.incidents.models import Incident


class IncidentRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, incident_id: str):
        stmt = select(Incident).where(
            Incident.id == incident_id
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def list_incidents(self):
        stmt = select(Incident)

        result = await self.session.execute(stmt)

        return result.scalars().all()

    async def create(self, incident: Incident):
        self.session.add(incident)
        await self.session.commit()
        await self.session.refresh(incident)

        return incident