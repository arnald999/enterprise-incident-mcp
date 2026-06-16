from uuid import uuid4


class JiraService:
    async def create_ticket(
        self,
        incident_id: str,
        title: str,
        description: str,
        project_key: str = "PLAT",
    ) -> dict:
        ticket_number = str(uuid4())[:6].upper()
        ticket_id = f"{project_key}-{ticket_number}"

        return {
            "ticket_id": ticket_id,
            "ticket_url": f"https://jira.example.com/browse/{ticket_id}",
            "incident_id": incident_id,
            "project_key": project_key,
            "status": "created",
            "title": title,
            "description": description,
        }