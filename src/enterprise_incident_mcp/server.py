from mcp.server.fastmcp import FastMCP

mcp = FastMCP("enterprise-incident-mcp")


@mcp.resource("system://health")
def health():
    return {
        "status": "healthy",
        "service": "enterprise-incident-mcp",
    }


if __name__ == "__main__":
    mcp.run()