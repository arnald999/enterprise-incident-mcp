from mcp.server.fastmcp import FastMCP
from enterprise_incident_mcp.mcp.resources.system import (
    database_health,
)
from enterprise_incident_mcp.mcp.tools.incidents import (
    assign_incident_tool,
    create_incident_tool,
    get_incident_tool,
    list_incidents_tool,
    update_incident_tool,
    get_incident_timeline_tool,
    search_incidents_tool,
    find_similar_incidents_tool,
    generate_postmortem_tool,
    build_incident_context_tool,
    generate_incident_rca_tool,
)
from enterprise_incident_mcp.mcp.tools.jira import (
    create_jira_ticket_tool,
)
from enterprise_incident_mcp.mcp.tools.github import (
    create_github_issue_tool,
)
from enterprise_incident_mcp.mcp.tools.embeddings import (
    index_incident_tool,
    semantic_search_tool,
)
from enterprise_incident_mcp.mcp.tools.investigator import (
    investigate_incident_tool,
)

mcp = FastMCP("enterprise-incident-mcp")


@mcp.resource("system://health")
def health():
    return {
        "status": "healthy",
        "database": "connected",
        "embeddings": "loaded",
        "version": "1.0.0"
    }


@mcp.resource("system://database")
async def db_health():
    return await database_health()


@mcp.tool()
async def create_incident(
    title: str,
    description: str,
    severity: str,
    owner: str | None = None,
    service: str | None = None,
) -> dict:
    """Create a new incident in PostgreSQL."""
    return await create_incident_tool(
        title=title,
        description=description,
        severity=severity,
        owner=owner,
        service=service,
    )


@mcp.tool()
async def list_incidents() -> list[dict]:
    """List all incidents from PostgreSQL."""
    return await list_incidents_tool()


@mcp.tool()
async def get_incident(incident_id: str) -> dict:
    """Get a single incident by ID from PostgreSQL."""
    return await get_incident_tool(incident_id)


@mcp.tool()
async def update_incident(
    incident_id: str,
    status: str | None = None,
    severity: str | None = None,
    owner: str | None = None,
) -> dict:
    """Update incident status, severity, or owner."""
    return await update_incident_tool(
        incident_id=incident_id,
        status=status,
        severity=severity,
        owner=owner,
    )


@mcp.tool()
async def assign_incident(incident_id: str, owner: str) -> dict:
    """Assign an incident to an owner or team."""
    return await assign_incident_tool(
        incident_id=incident_id,
        owner=owner,
    )


@mcp.tool()
async def get_incident_timeline(incident_id: str) -> list[dict]:
    """Get timeline events for an incident."""
    return await get_incident_timeline_tool(incident_id)


@mcp.tool()
async def search_incidents(
    query: str,
) -> list[dict]:
    """
    Search incidents by title, description, or service.
    """
    return await search_incidents_tool(query)


@mcp.tool()
async def find_similar_incidents(query: str) -> list[dict]:
    """Find similar incidents using keyword-based retrieval."""
    return await find_similar_incidents_tool(query)


@mcp.tool()
async def generate_postmortem(incident_id: str) -> dict:
    """Generate a draft postmortem for an incident using incident details and timeline."""
    return await generate_postmortem_tool(incident_id)


@mcp.tool()
async def create_jira_ticket(
    incident_id: str,
    project_key: str = "PLAT",
) -> dict:
    """Create Jira ticket from incident."""
    return await create_jira_ticket_tool(
        incident_id=incident_id,
        project_key=project_key,
    )


@mcp.tool()
async def create_github_issue(
    incident_id: str,
    repository: str,
) -> dict:
    """Create GitHub issue from incident."""
    return await create_github_issue_tool(
        incident_id=incident_id,
        repository=repository,
    )


@mcp.tool()
async def build_incident_context(query: str) -> dict:
    """Build incident context for RAG workflows using similar incidents and timelines."""
    return await build_incident_context_tool(query)


@mcp.tool()
async def generate_incident_rca(query: str) -> dict:
    """Generate an RCA draft using similar incidents and timelines."""
    return await generate_incident_rca_tool(query)


@mcp.tool()
async def index_incident(
    incident_id: str,
) -> dict:
    """
    Generate and store vector embedding
    for an incident.
    """
    return await index_incident_tool(
        incident_id
    )


@mcp.tool()
async def semantic_search(
    query: str,
) -> dict:
    """
    Semantic incident search using embeddings.
    """
    return await semantic_search_tool(
        query
    )


@mcp.tool()
async def investigate_incident(
    query: str,
) -> dict:
    return await investigate_incident_tool(
        query
    )


if __name__ == "__main__":
    mcp.run()