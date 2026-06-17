from collections import Counter


class PatternService:

    def extract_patterns(
        self,
        incidents,
        timelines,
    ) -> dict:

        severities = Counter()
        statuses = Counter()
        services = Counter()

        jira_count = 0
        github_count = 0

        for incident in incidents:

            severities[
                str(incident.severity)
            ] += 1

            statuses[
                str(incident.status)
            ] += 1

            if incident.service:
                services[
                    incident.service
                ] += 1

            for event in timelines.get(
                incident.id,
                [],
            ):

                event_type = str(
                    event.event_type
                )

                if (
                    "JIRA"
                    in event_type
                ):
                    jira_count += 1

                if (
                    "GITHUB"
                    in event_type
                ):
                    github_count += 1

        return {
            "incident_count":
                len(incidents),

            "top_severity":
                severities.most_common(1),

            "top_status":
                statuses.most_common(1),

            "top_service":
                services.most_common(1),

            "jira_tickets":
                jira_count,

            "github_issues":
                github_count,
        }