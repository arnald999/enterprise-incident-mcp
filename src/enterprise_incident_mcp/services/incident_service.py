from enterprise_incident_mcp.models.incident import (
    CreateIncidentRequest,
    Incident,
    IncidentStatus,
    Severity,
    UpdateIncidentRequest,
)
from enterprise_incident_mcp.repositories.incident_repository import IncidentRepository


class IncidentService:
    def __init__(self, repository: IncidentRepository) -> None:
        self.repository = repository

    def list_incidents(
        self,
        status: IncidentStatus | None = None,
        severity: Severity | None = None,
    ) -> list[Incident]:
        return self.repository.list(status=status, severity=severity)

    def get_incident(self, incident_id: str) -> Incident:
        incident = self.repository.get(incident_id)
        if not incident:
            raise ValueError(f"Incident not found: {incident_id}")
        return incident

    def search_incidents(self, query: str) -> list[Incident]:
        return self.repository.search(query)

    def create_incident(self, request: CreateIncidentRequest) -> Incident:
        next_id = f"INC-{100 + len(self.repository.list()) + 1}"
        incident = Incident(
            id=next_id,
            title=request.title,
            description=request.description,
            severity=request.severity,
            owner=request.owner,
            service=request.service,
        )
        return self.repository.create(incident)

    def update_incident(self, request: UpdateIncidentRequest) -> Incident:
        incident = self.repository.update(
            incident_id=request.incident_id,
            status=request.status,
            severity=request.severity,
            owner=request.owner,
        )
        if not incident:
            raise ValueError(f"Incident not found: {request.incident_id}")
        return incident

    def assign_incident(self, incident_id: str, owner: str) -> Incident:
        incident = self.repository.update(incident_id=incident_id, owner=owner)
        if not incident:
            raise ValueError(f"Incident not found: {incident_id}")
        return incident
