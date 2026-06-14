from sqlalchemy import text

from enterprise_incident_mcp.db.session import engine


async def database_health():

    async with engine.connect() as conn:
        await conn.execute(
            text("SELECT 1")
        )

    return {
        "status": "healthy",
        "database": "connected",
    }