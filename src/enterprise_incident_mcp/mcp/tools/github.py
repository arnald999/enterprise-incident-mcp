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
from enterprise_incident_mcp.services.github_service import GitHubService


async def create_github_issue_tool(
    incident_id: str,
    repository: str,
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

        github_service = GitHubService()

        issue = await github_service.create_issue(
            incident_id=incident.id,
            repository=repository,
            title=f"[{incident.severity}] {incident.title}",
            body=(
                f"Incident ID: {incident.id}\n"
                f"Service: {incident.service}\n"
                f"Severity: {incident.severity}\n"
                f"Status: {incident.status}\n"
                f"Owner: {incident.owner}\n\n"
                f"{incident.description}"
            ),
        )

        await event_repository.create(
            IncidentEvent(
                incident_id=incident.id,
                event_type=IncidentEventType.GITHUB_ISSUE_CREATED,
                message=(
                    f"GitHub issue #{issue['issue_number']} created "
                    f"in repository {issue['repository']}"
                ),
                created_at=datetime.utcnow(),
            )
        )

        return issue