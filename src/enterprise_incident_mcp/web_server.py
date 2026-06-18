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
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "enterprise-incident-mcp",
        "transport": "streamable-http",
    }


@app.get("/debug/db")
async def debug_db():
    database_url = os.getenv("DATABASE_URL", "")

    safe_url = database_url
    if "@" in safe_url:
        prefix, suffix = safe_url.split("@", 1)
        safe_url = "***@" + suffix

    return {
        "database_url": safe_url,
    }


app.mount("/", mcp.streamable_http_app())


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)