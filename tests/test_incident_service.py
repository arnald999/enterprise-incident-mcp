from enterprise_incident_mcp.models.incident import CreateIncidentRequest, Severity
from enterprise_incident_mcp.repositories.incident_repository import IncidentRepository
from enterprise_incident_mcp.services.incident_service import IncidentService


def test_create_incident():
    service = IncidentService(IncidentRepository())

    incident = service.create_incident(
        CreateIncidentRequest(
            title="API errors",
            description="5xx errors increased",
            severity=Severity.P2,
            service="api-gateway",
            owner="Platform Team",
        )
    )

    assert incident.id.startswith("INC-")
    assert incident.severity == Severity.P2
    assert incident.service == "api-gateway"


def test_search_incidents():
    service = IncidentService(IncidentRepository())

    results = service.search_incidents("checkout")

    assert len(results) >= 1
    assert results[0].service == "checkout-api"
