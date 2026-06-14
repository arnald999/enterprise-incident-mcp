class JiraClient:
    def create_ticket(self, incident_id: str, project_key: str, summary: str, description: str) -> dict:
        # Placeholder for real Jira REST API integration.
        return {
            "ticket_id": f"{project_key}-500",
            "incident_id": incident_id,
            "status": "created",
            "summary": summary,
        }
