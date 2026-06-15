from enterprise_incident_mcp.domain.incidents.models import Incident
from enterprise_incident_mcp.domain.incidents.event_models import IncidentEvent


class PostmortemService:
    def generate(
        self,
        incident: Incident,
        timeline: list[IncidentEvent],
    ) -> str:
        timeline_lines = "\n".join(
            f"- {event.created_at.isoformat()} - {event.event_type}: {event.message}"
            for event in timeline
        )

        return f"""# Postmortem: {incident.title}

## Incident Summary

Incident ID: {incident.id}

Service: {incident.service or "Unknown"}

Severity: {incident.severity}

Final Status: {incident.status}

Owner: {incident.owner or "Unassigned"}

## Impact

Describe customer impact here.

## Timeline

{timeline_lines or "No timeline events recorded."}

## Root Cause

Root cause is not yet determined.

## Resolution

Describe mitigation and recovery steps here.

## What Went Well

- Timeline events were captured.
- Incident ownership was tracked.

## What Went Wrong

- Add investigation findings here.

## Action Items

- Add follow-up action items here.
"""