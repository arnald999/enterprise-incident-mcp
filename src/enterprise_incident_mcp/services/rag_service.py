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
    
    
    def generate_rca(
        self,
        query: str,
        context: str,
        incident_count: int,
    ) -> str:
        if incident_count == 0:
            return f"""# RCA Draft: {query}

    ## Summary

    No similar incidents were found for this query.

    ## Findings

    There is not enough historical context to infer recurring patterns.

    ## Recommended Next Steps

    - Capture more incident details.
    - Add timeline events.
    - Improve incident descriptions.
    - Re-run RCA after more operational history is available.
    """

        return f"""# RCA Draft: {query}

    ## Summary

    Found {incident_count} similar incident(s) related to: "{query}".

    ## Historical Context Used

    {context}

    ## Likely Patterns

    Based on similar incidents, this issue may involve recurring service degradation, ownership handoffs, or repeated operational symptoms.

    ## Possible Root Cause Areas

    - Application latency
    - Downstream dependency failures
    - Database/query performance
    - Queue or worker backlog
    - Infrastructure saturation

    ## Recommended Investigation Steps

    - Compare timelines across similar incidents.
    - Check when severity or ownership changed.
    - Review service metrics around incident creation time.
    - Inspect recent deployments.
    - Check downstream dependency health.
    - Review logs for repeated error patterns.

    ## Suggested Action Items

    - Improve alert metadata.
    - Add runbook links to incidents.
    - Capture mitigation steps as timeline events.
    - Link Jira/GitHub remediation work.
    - Add semantic search in a future iteration.
    """