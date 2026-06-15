from enterprise_incident_mcp.domain.incidents.models import Incident
from enterprise_incident_mcp.domain.incidents.event_models import IncidentEvent


class PostmortemService:
    def generate(
        self,
        incident: Incident,
        timeline: list[IncidentEvent],
    ) -> str:
        timeline_text = self._timeline_summary(
            timeline
        )
        impact = (
                    f"Service '{incident.service}' experienced a "
                    f"{incident.severity} severity incident."
                )
        
        resolution = (
                    "Incident status is currently "
                    f"{incident.status}."
                )

        return f"""# Postmortem: {incident.title}

                ## Incident Summary

                Incident ID: {incident.id}

                Service: {incident.service or "Unknown"}

                Severity: {incident.severity}

                Final Status: {incident.status}

                Owner: {incident.owner or "Unassigned"}

                ## Impact

                {impact}

                ## Timeline

                {timeline_text}

                ## Root Cause

                Root cause is not yet determined.

                ## Resolution

                {resolution}

                ## What Went Well

                - Timeline events were captured.
                - Incident ownership was tracked.

                ## What Went Wrong

                - Add investigation findings here.

                ## Action Items

                - Add follow-up action items here.
                """
    
    
    def _timeline_summary(
        self,
        timeline: list[IncidentEvent],
    ) -> str:
        if not timeline:
            return "No timeline events recorded."

        return "\n".join(
            f"- {event.created_at.isoformat()} | {event.message}"
            for event in timeline
        )