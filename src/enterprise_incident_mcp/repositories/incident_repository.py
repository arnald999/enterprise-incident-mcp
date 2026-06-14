from datetime import datetime, timezone
from enterprise_incident_mcp.models.incident import Incident, IncidentStatus, Severity


class IncidentRepository:
    def __init__(self) -> None:
        self._incidents: dict[str, Incident] = {
            "INC-101": Incident(
                id="INC-101",
                title="Checkout latency spike",
                description="p95 latency crossed 2.5s for checkout API.",
                severity=Severity.P1,
                status=IncidentStatus.OPEN,
                owner="Platform Team",
                service="checkout-api",
            ),
            "INC-102": Incident(
                id="INC-102",
                title="Kafka consumer lag",
                description="Order processor lag exceeded threshold.",
                severity=Severity.P2,
                status=IncidentStatus.INVESTIGATING,
                owner="Payments Team",
                service="order-processor",
            ),
        }

    def list(self, status: IncidentStatus | None = None, severity: Severity | None = None) -> list[Incident]:
        incidents = list(self._incidents.values())
        if status:
            incidents = [i for i in incidents if i.status == status]
        if severity:
            incidents = [i for i in incidents if i.severity == severity]
        return incidents

    def get(self, incident_id: str) -> Incident | None:
        return self._incidents.get(incident_id)

    def search(self, query: str) -> list[Incident]:
        q = query.lower()
        return [
            incident
            for incident in self._incidents.values()
            if q in incident.title.lower()
            or q in incident.description.lower()
            or q in (incident.service or "").lower()
            or q in (incident.owner or "").lower()
        ]

    def create(self, incident: Incident) -> Incident:
        self._incidents[incident.id] = incident
        return incident

    def update(
        self,
        incident_id: str,
        status: IncidentStatus | None = None,
        severity: Severity | None = None,
        owner: str | None = None,
    ) -> Incident | None:
        incident = self._incidents.get(incident_id)
        if not incident:
            return None

        data = incident.model_dump()
        if status:
            data["status"] = status
        if severity:
            data["severity"] = severity
        if owner:
            data["owner"] = owner
        data["updated_at"] = datetime.now(timezone.utc)

        updated = Incident(**data)
        self._incidents[incident_id] = updated
        return updated
