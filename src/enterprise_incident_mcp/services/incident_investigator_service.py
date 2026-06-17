class IncidentInvestigatorService:
    def generate_report(
        self,
        query: str,
        incident_count: int,
        context: str,
    ) -> str:

        return f"""
# Incident Investigation Report

## Query

{query}

## Similar Incidents Reviewed

{incident_count}

## Findings

Historical incidents with related symptoms were identified.

Repeated patterns indicate potential service degradation,
dependency failures, operational bottlenecks,
or infrastructure-related issues.

## Recommended Investigation Areas

- Recent deployments
- Dependency health
- Database performance
- Service saturation
- Error rate changes
- Capacity limits

## Historical Context

{context}
"""