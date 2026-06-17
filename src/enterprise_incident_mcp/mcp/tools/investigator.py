from enterprise_incident_mcp.db.session import AsyncSessionLocal
from enterprise_incident_mcp.repositories.embedding_repository import (
    EmbeddingRepository,
)
from enterprise_incident_mcp.repositories.incident_event_repository import (
    IncidentEventRepository,
)
from enterprise_incident_mcp.repositories.incident_repository import (
    IncidentRepository,
)
from enterprise_incident_mcp.services.embedding_service import (
    EmbeddingService,
)
from enterprise_incident_mcp.services.incident_investigator_service import (
    IncidentInvestigatorService,
)
from enterprise_incident_mcp.services.rag_service import (
    RAGService,
)
from enterprise_incident_mcp.services.pattern_service import (
    PatternService,
)


async def investigate_incident_tool(
    query: str,
) -> dict:
    async with AsyncSessionLocal() as session:

        embedding_repo = EmbeddingRepository(
            session
        )

        incident_repo = IncidentRepository(
            session
        )

        timeline_repo = (
            IncidentEventRepository(
                session
            )
        )

        embedding_service = (
            EmbeddingService()
        )

        rag_service = RAGService()

        investigator = (
            IncidentInvestigatorService()
        )

        pattern_service = PatternService()

        # Step 1: Embed query

        query_embedding = (
            embedding_service.embed(
                query
            )
        )

        # Step 2: Semantic search

        matches = (
            await embedding_repo.semantic_search(
                query_embedding
            )
        )

        # Step 3: Load incidents

        incidents = []
        timelines = {}
        similar_matches = []

        for match in matches:

            similar_matches.append(
                {
                    "incident_id": match.incident_id,
                    "distance": round(
                        float(match.distance),
                        4,
                    ),
                }
            )

            incident = (
                await incident_repo.get_by_id(
                    match.incident_id
                )
            )

            if incident is None:
                continue

            incidents.append(
                incident
            )

            timeline = (
                await timeline_repo.get_timeline(
                    incident.id
                )
            )

            timelines[
                incident.id
            ] = timeline

        # Step 4: Build RAG context

        context = (
            rag_service.build_context(
                incidents=incidents,
                timelines=timelines,
            )
        )

        patterns = (
            pattern_service.extract_patterns(
                incidents=incidents,
                timelines=timelines,
            )
        )

        # Step 5: Generate report

        report = investigator.generate_report(
            query=query,
            incident_count=len(
                incidents
            ),
            context=context,
            patterns=patterns,
        )

        return {
            "query": query,
            "incident_count": len(
                incidents
            ),
            "similar_incidents":
                similar_matches,
            "report": report,
        }