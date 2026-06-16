from random import randint


class GitHubService:
    async def create_issue(
        self,
        incident_id: str,
        repository: str,
        title: str,
        body: str,
    ) -> dict:
        issue_number = randint(100, 999)

        return {
            "issue_number": issue_number,
            "issue_url": f"https://github.com/{repository}/issues/{issue_number}",
            "incident_id": incident_id,
            "repository": repository,
            "status": "created",
            "title": title,
            "body": body,
        }