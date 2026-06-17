import os
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from enterprise_incident_mcp.server import mcp


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with mcp.session_manager.run():
        yield


app = FastAPI(
    title="Enterprise Incident MCP Server",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
async def root():
    return {
        "service": "enterprise-incident-mcp",
        "status": "healthy",
        "transport": "streamable-http",
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "database": "configured",
        "transport": "streamable-http",
    }


app.mount("/", mcp.streamable_http_app())


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))

    uvicorn.run(
        "enterprise_incident_mcp.web_server:app",
        host="0.0.0.0",
        port=port,
        reload=False,
    )