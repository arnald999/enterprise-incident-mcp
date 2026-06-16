from enterprise_incident_mcp.domain.incidents.event_models import IncidentEvent
from enterprise_incident_mcp.domain.incidents.models import Incident


class RAGService:
    def build_context(
        self,
        incidents: list[Incident],
        timelines: dict[str, list[IncidentEvent]],
    ) -> str:
        sections = []

        for incident in incidents:
            events = timelines.get(incident.id, [])

            timeline_text = "\n".join(
                f"- {event.created_at.isoformat()} | {event.event_type}: {event.message}"
                for event in events
            )

            sections.append(
                f"""Incident ID: {incident.id}

Title: {incident.title}

Description: {incident.description}

Service: {incident.service or "Unknown"}

Severity: {incident.severity}

Status: {incident.status}

Owner: {incident.owner or "Unassigned"}

Timeline:
{timeline_text or "No timeline events recorded."}
"""
            )

        return "\n---\n".join(sections)