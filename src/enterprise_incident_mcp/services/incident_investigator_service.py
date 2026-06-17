class IncidentInvestigatorService:
    def generate_report(
        self,
        query: str,
        incident_count: int,
        context: str,
        patterns: dict,
    ) -> str:

        top_severity = (
            patterns["top_severity"][0][0]
            if patterns["top_severity"]
            else "Unknown"
        )

        top_status = (
            patterns["top_status"][0][0]
            if patterns["top_status"]
            else "Unknown"
        )

        top_service = (
            patterns["top_service"][0][0]
            if patterns["top_service"]
            else "Unknown"
        )

        return f"""
    # Incident Investigation Report

    ## Query

    {query}

    ## Similar Incidents Reviewed

    {incident_count}

    ## Observed Patterns

    Most common severity:
    {top_severity}

    Most common status:
    {top_status}

    Most common service:
    {top_service}

    Jira tickets created:
    {patterns['jira_tickets']}

    GitHub issues created:
    {patterns['github_issues']}

    ## Findings

    Historical incidents indicate recurring operational patterns.

    ## Historical Context

    {context}
    """