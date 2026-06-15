from enterprise_incident_mcp.domain.incidents.models import IncidentStatus

ALLOWED_TRANSITIONS = {
    IncidentStatus.OPEN: {
        IncidentStatus.INVESTIGATING,
    },
    IncidentStatus.INVESTIGATING: {
        IncidentStatus.MITIGATED,
    },
    IncidentStatus.MITIGATED: {
        IncidentStatus.CLOSED,
    },
    IncidentStatus.CLOSED: set(),
}


def is_valid_transition(
    current_status: str,
    new_status: str,
) -> bool:
    try:
        current = IncidentStatus(current_status)
        new = IncidentStatus(new_status)

        return new in ALLOWED_TRANSITIONS[current]

    except ValueError:
        return False