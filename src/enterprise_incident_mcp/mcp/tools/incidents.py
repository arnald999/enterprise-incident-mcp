from enterprise_incident_mcp.db.session import AsyncSessionLocal
from enterprise_incident_mcp.domain.incidents.schemas import IncidentCreate
from enterprise_incident_mcp.repositories.incident_repository import IncidentRepository
from enterprise_incident_mcp.services.incident_service import IncidentService
from enterprise_incident_mcp.repositories.incident_event_repository import (
    IncidentEventRepository,
)

async def create_incident_tool(
    title: str,
    description: str,
    severity: str,
    owner: str | None = None,
    service: str | None = None,
) -> dict:
    async with AsyncSessionLocal() as session:
        repository = IncidentRepository(session)
        event_repository = IncidentEventRepository(session)
        service_layer = IncidentService(repository, event_repository)

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
        event_repository = IncidentEventRepository(session)
        service_layer = IncidentService(repository, event_repository)

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
    

def serialize_incident(incident) -> dict:
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


async def get_incident_tool(incident_id: str) -> dict:
    async with AsyncSessionLocal() as session:
        repository = IncidentRepository(session)
        event_repository = IncidentEventRepository(session)
        service_layer = IncidentService(repository, event_repository)

        incident = await service_layer.get_incident(incident_id)

        if incident is None:
            return {
                "error": "incident_not_found",
                "incident_id": incident_id,
            }

        return serialize_incident(incident)


async def update_incident_tool(
    incident_id: str,
    status: str | None = None,
    severity: str | None = None,
    owner: str | None = None,
) -> dict:
    async with AsyncSessionLocal() as session:
        repository = IncidentRepository(session)
        event_repository = IncidentEventRepository(session)
        service_layer = IncidentService(repository, event_repository)

        try:
            incident = await service_layer.update_incident(
                incident_id=incident_id,
                status=status,
                severity=severity,
                owner=owner,
            )
            return serialize_incident(incident)
        except ValueError:
            return {
                "error": "incident_not_found",
                "incident_id": incident_id,
            }


async def assign_incident_tool(
    incident_id: str,
    owner: str,
) -> dict:
    async with AsyncSessionLocal() as session:
        repository = IncidentRepository(session)
        event_repository = IncidentEventRepository(session)
        service_layer = IncidentService(repository, event_repository)

        try:
            incident = await service_layer.assign_incident(
                incident_id=incident_id,
                owner=owner,
            )
            return serialize_incident(incident)
        except ValueError:
            return {
                "error": "incident_not_found",
                "incident_id": incident_id,
            }