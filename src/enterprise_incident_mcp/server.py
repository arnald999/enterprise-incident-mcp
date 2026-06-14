from mcp.server.fastmcp import FastMCP
from enterprise_incident_mcp.mcp.resources.system import (
    database_health,
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

if __name__ == "__main__":
    mcp.run()