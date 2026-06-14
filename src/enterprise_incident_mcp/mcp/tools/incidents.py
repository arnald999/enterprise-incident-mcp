from enterprise_incident_mcp.db.session import AsyncSessionLocal
from enterprise_incident_mcp.domain.incidents.schemas import IncidentCreate
from enterprise_incident_mcp.repositories.incident_repository import IncidentRepository
from enterprise_incident_mcp.services.incident_service import IncidentService


async def create_incident_tool(
    title: str,
    description: str,
    severity: str,
    owner: str | None = None,
    service: str | None = None,
) -> dict:
    async with AsyncSessionLocal() as session:
        repository = IncidentRepository(session)
        service_layer = IncidentService(repository)

        incident = await service_layer.create_incident(
            IncidentCreate(
                title=title,
                description=description,
                severity=severity,
                owner=owner,
                service=service,
            )
        )

        return {
            "id": incident.id,
            "title": incident.title,
            "description": incident.description,
            "severity": incident.severity,
            "status": incident.status,
            "owner": incident.owner,
            "service": incident.service,
            "created_at": incident.created_at.isoformat(),
            "updated_at": incident.updated_at.isoformat(),
        }


async def list_incidents_tool() -> list[dict]:
    async with AsyncSessionLocal() as session:
        repository = IncidentRepository(session)
        service_layer = IncidentService(repository)

        incidents = await service_layer.list_incidents()

        return [
            {
                "id": incident.id,
                "title": incident.title,
                "description": incident.description,
                "severity": incident.severity,
                "status": incident.status,
                "owner": incident.owner,
                "service": incident.service,
                "created_at": incident.created_at.isoformat(),
                "updated_at": incident.updated_at.isoformat(),
            }
            for incident in incidents
        ]