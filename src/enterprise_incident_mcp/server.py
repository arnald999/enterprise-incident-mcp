from mcp.server.fastmcp import FastMCP
from enterprise_incident_mcp.mcp.resources.system import (
    database_health,
)
from enterprise_incident_mcp.mcp.tools.incidents import (
    create_incident_tool,
    list_incidents_tool,
)

mcp = FastMCP("enterprise-incident-mcp")


@mcp.resource("system://health")
def health():
    return {
        "status": "healthy",
        "service": "enterprise-incident-mcp",
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


if __name__ == "__main__":
    mcp.run()