from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import or_, select

from enterprise_incident_mcp.domain.incidents.models import Incident
from datetime import datetime


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
    
    async def update(
        self,
        incident_id: str,
        status: str | None = None,
        severity: str | None = None,
        owner: str | None = None,
    ) -> Incident | None:
        incident = await self.get_by_id(incident_id)

        if incident is None:
            return None

        if status is not None:
            incident.status = status

        if severity is not None:
            incident.severity = severity

        if owner is not None:
            incident.owner = owner

        incident.updated_at = datetime.utcnow()

        await self.session.commit()
        await self.session.refresh(incident)

        return incident
    
    async def search(self, query: str):
        pattern = f"%{query}%"

        stmt = (
            select(Incident)
            .where(
                or_(
                    Incident.title.ilike(pattern),
                    Incident.description.ilike(pattern),
                    Incident.service.ilike(pattern),
                )
            )
            .order_by(Incident.created_at.desc())
        )

        result = await self.session.execute(stmt)

        return list(result.scalars().all())
    
    async def find_similar(self, query: str) -> list[Incident]:
        pattern = f"%{query}%"

        stmt = (
            select(Incident)
            .where(
                or_(
                    Incident.title.ilike(pattern),
                    Incident.description.ilike(pattern),
                    Incident.service.ilike(pattern),
                    Incident.owner.ilike(pattern),
                )
            )
            .order_by(Incident.created_at.desc())
            .limit(10)
        )

        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    