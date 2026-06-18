import os

import uvicorn
from fastapi import FastAPI

try:
    from enterprise_incident_mcp.server import mcp

    MCP_AVAILABLE = True
    MCP_IMPORT_ERROR = None
except Exception as exc:
    print(f"MCP IMPORT FAILED: {exc}", flush=True)

    mcp = None
    MCP_AVAILABLE = False
    MCP_IMPORT_ERROR = str(exc)


app = FastAPI(
    title="Enterprise Incident MCP Server",
    version="1.0.0",
)


@app.get("/")
async def root():
    return {
        "service": "enterprise-incident-mcp",
        "status": "healthy",
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "enterprise-incident-mcp",
        "transport": "streamable-http",
        "mcp_available": MCP_AVAILABLE,
    }


@app.get("/debug")
async def debug():
    return {
        "mcp_available": MCP_AVAILABLE,
        "mcp_import_error": MCP_IMPORT_ERROR,
    }


if MCP_AVAILABLE and mcp is not None:
    app.mount("/", mcp.streamable_http_app())


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        reload=False,
    )