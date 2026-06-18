import os
import uvicorn
from fastapi import FastAPI

from enterprise_incident_mcp.server import mcp

app = FastAPI()


@app.get("/")
async def root():
    return {"status": "ok"}


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "enterprise-incident-mcp",
        "transport": "streamable-http",
    }


app.mount("/", mcp.streamable_http_app())


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)