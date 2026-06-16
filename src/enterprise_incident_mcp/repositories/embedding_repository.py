from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from enterprise_incident_mcp.domain.incidents.embedding_models import (
    IncidentEmbedding,
)


class EmbeddingRepository:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def create(
        self,
        embedding: IncidentEmbedding,
    ) -> IncidentEmbedding:
        self.session.add(embedding)

        await self.session.commit()

        await self.session.refresh(
            embedding
        )

        return embedding

    async def get_by_incident_id(
        self,
        incident_id: str,
    ):
        stmt = (
            select(IncidentEmbedding)
            .where(
                IncidentEmbedding.incident_id
                == incident_id
            )
        )

        result = await self.session.execute(
            stmt
        )

        return result.scalar_one_or_none()
    
    async def semantic_search(
        self,
        query_embedding: list[float],
        limit: int = 5,
    ):
        stmt = text(
            """
            SELECT
                incident_id,
                content,
                embedding <=> CAST(:embedding AS vector)
                    AS distance
            FROM incident_embeddings
            ORDER BY embedding <=> CAST(:embedding AS vector)
            LIMIT :limit
            """
        )

        result = await self.session.execute(
            stmt,
            {
                "embedding": str(query_embedding),
                "limit": limit,
            },
        )

        return result.fetchall()