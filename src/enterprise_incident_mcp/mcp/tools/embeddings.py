from datetime import datetime

from enterprise_incident_mcp.db.session import (
    AsyncSessionLocal,
)
from enterprise_incident_mcp.domain.incidents.embedding_models import (
    IncidentEmbedding,
)
from enterprise_incident_mcp.repositories.embedding_repository import (
    EmbeddingRepository,
)
from enterprise_incident_mcp.repositories.incident_repository import (
    IncidentRepository,
)
from enterprise_incident_mcp.services.embedding_service import (
    EmbeddingService,
)



async def index_incident_tool(
    incident_id: str,
) -> dict:
    async with AsyncSessionLocal() as session:

        incident_repo = IncidentRepository(
            session
        )

        embedding_repo = (
            EmbeddingRepository(
                session
            )
        )

        incident = (
            await incident_repo.get_by_id(
                incident_id
            )
        )

        if incident is None:
            return {
                "error": "incident_not_found"
            }

        text = f"""
        Title: {incident.title}

        Description:
        {incident.description}

        Service:
        {incident.service}

        Severity:
        {incident.severity}
        """

        embedding_service = (
            EmbeddingService()
        )

        vector = (
            embedding_service.embed(
                text
            )
        )

        existing = (
            await embedding_repo.get_by_incident_id(
                incident_id
            )
        )

        if existing:
            return {
                "status": "already_indexed",
                "incident_id": incident_id,
            }

        record = IncidentEmbedding(
            incident_id=incident.id,
            content=text,
            embedding=vector,
            created_at=datetime.utcnow(),
        )

        await embedding_repo.create(
            record
        )

        return {
            "status": "indexed",
            "incident_id": incident_id,
            "dimensions": len(vector),
        }
    
async def semantic_search_tool(
    query: str,
) -> dict:
    async with AsyncSessionLocal() as session:

        embedding_repo = (
            EmbeddingRepository(
                session
            )
        )

        embedding_service = (
            EmbeddingService()
        )

        query_vector = (
            embedding_service.embed(
                query
            )
        )

        matches = (
            await embedding_repo.semantic_search(
                query_vector
            )
        )

        return {
            "query": query,
            "results": [
                {
                    "incident_id": row.incident_id,
                    "distance": float(
                        row.distance
                    ),
                }
                for row in matches
            ],
        }