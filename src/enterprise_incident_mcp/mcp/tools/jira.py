from datetime import datetime

from enterprise_incident_mcp.db.session import AsyncSessionLocal
from enterprise_incident_mcp.domain.incidents.event_models import (
    IncidentEvent,
    IncidentEventType,
)
from enterprise_incident_mcp.repositories.incident_event_repository import (
    IncidentEventRepository,
)
from enterprise_incident_mcp.repositories.incident_repository import IncidentRepository
from enterprise_incident_mcp.services.jira_service import JiraService


async def create_jira_ticket_tool(
    incident_id: str,
    project_key: str = "PLAT",
) -> dict:
    async with AsyncSessionLocal() as session:
        incident_repository = IncidentRepository(session)
        event_repository = IncidentEventRepository(session)

        incident = await incident_repository.get_by_id(incident_id)

        if incident is None:
            return {
                "error": "incident_not_found",
                "incident_id": incident_id,
            }

        jira_service = JiraService()

        ticket = await jira_service.create_ticket(
            incident_id=incident.id,
            title=incident.title,
            description=incident.description,
            project_key=project_key,
        )

        await event_repository.create(
            IncidentEvent(
                incident_id=incident.id,
                event_type=IncidentEventType.JIRA_TICKET_CREATED,
                message=(
                    f"Jira ticket {ticket['ticket_id']} created "
                    f"for project {ticket['project_key']}"
                ),
                created_at=datetime.utcnow(),
            )
        )

        return ticket