from mcp.server.fastmcp import FastMCP

from enterprise_incident_mcp.integrations.github.client import GitHubClient
from enterprise_incident_mcp.integrations.jira.client import JiraClient
from enterprise_incident_mcp.models.incident import (
    CreateIncidentRequest,
    IncidentStatus,
    Severity,
    UpdateIncidentRequest,
)
from enterprise_incident_mcp.repositories.incident_repository import IncidentRepository
from enterprise_incident_mcp.services.incident_service import IncidentService

mcp = FastMCP("enterprise-incident-mcp")

incident_repository = IncidentRepository()
incident_service = IncidentService(incident_repository)
jira_client = JiraClient()
github_client = GitHubClient()


@mcp.resource("incidents://list")
def list_incidents() -> str:
    """List all incidents."""
    incidents = incident_service.list_incidents()
    return "\n".join(incident.model_dump_json() for incident in incidents)


@mcp.resource("incidents://open")
def list_open_incidents() -> str:
    """List all open incidents."""
    incidents = incident_service.list_incidents(status=IncidentStatus.OPEN)
    return "\n".join(incident.model_dump_json() for incident in incidents)


@mcp.resource("incidents://{incident_id}")
def get_incident(incident_id: str) -> str:
    """Get a single incident by ID."""
    return incident_service.get_incident(incident_id).model_dump_json()


@mcp.tool()
def search_incidents(query: str) -> list[dict]:
    """Search historical incidents by title, description, service, or owner."""
    return [incident.model_dump(mode="json") for incident in incident_service.search_incidents(query)]


@mcp.tool()
def create_incident(
    title: str,
    description: str,
    severity: Severity,
    service: str | None = None,
    owner: str | None = None,
) -> dict:
    """Create a new incident."""
    incident = incident_service.create_incident(
        CreateIncidentRequest(
            title=title,
            description=description,
            severity=severity,
            service=service,
            owner=owner,
        )
    )
    return incident.model_dump(mode="json")


@mcp.tool()
def assign_incident(incident_id: str, owner: str) -> dict:
    """Assign an incident to an owner or responder team."""
    incident = incident_service.assign_incident(incident_id=incident_id, owner=owner)
    return incident.model_dump(mode="json")


@mcp.tool()
def update_incident(
    incident_id: str,
    status: IncidentStatus | None = None,
    severity: Severity | None = None,
    owner: str | None = None,
    comment: str | None = None,
) -> dict:
    """Update incident status, severity, owner, or add a comment placeholder."""
    incident = incident_service.update_incident(
        UpdateIncidentRequest(
            incident_id=incident_id,
            status=status,
            severity=severity,
            owner=owner,
            comment=comment,
        )
    )
    return incident.model_dump(mode="json")


@mcp.tool()
def create_jira_ticket(incident_id: str, project_key: str = "PLAT") -> dict:
    """Create a Jira ticket for an incident."""
    incident = incident_service.get_incident(incident_id)
    return jira_client.create_ticket(
        incident_id=incident.id,
        project_key=project_key,
        summary=incident.title,
        description=incident.description,
    )


@mcp.tool()
def create_github_issue(incident_id: str, repo: str) -> dict:
    """Create a GitHub issue for an incident."""
    incident = incident_service.get_incident(incident_id)
    return github_client.create_issue(
        repo=repo,
        title=f"[{incident.severity}] {incident.title}",
        body=f"Incident: {incident.id}\nService: {incident.service}\n\n{incident.description}",
    )


@mcp.prompt()
def incident_triage_prompt(alert_summary: str, affected_service: str) -> str:
    """Prompt for incident triage and severity assessment."""
    return f"""
You are an incident commander. Triage the following alert.

Alert summary:
{alert_summary}

Affected service:
{affected_service}

Return:
1. Probable severity
2. Immediate checks
3. Suggested owner
4. Customer impact hypothesis
5. Whether to create an incident
"""


@mcp.prompt()
def root_cause_analysis_prompt(incident_id: str) -> str:
    """Prompt for root-cause analysis."""
    return f"""
Investigate incident {incident_id}.

Return:
1. Symptoms
2. Timeline
3. Suspected root cause
4. Contributing factors
5. Recovery actions
6. Preventive actions
"""


@mcp.prompt()
def postmortem_prompt(incident_id: str) -> str:
    """Prompt for generating a postmortem."""
    return f"""
Generate a postmortem for incident {incident_id}.

Include:
1. Executive summary
2. Customer impact
3. Timeline
4. Root cause
5. What went well
6. What went wrong
7. Action items
"""


if __name__ == "__main__":
    mcp.run()
