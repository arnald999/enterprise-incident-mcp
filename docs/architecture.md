# Architecture Diagram

```mermaid
flowchart TD
    A[Claude / ChatGPT / Cursor / MCP Inspector] --> B[MCP Client]

    B --> C[Enterprise Incident MCP Server]

    C --> D[MCP Resources]
    C --> E[MCP Tools]
    C --> F[MCP Prompts]

    D --> D1[system://health]
    D --> D2[system://database]

    E --> E1[Incident CRUD]
    E --> E2[Timeline Retrieval]
    E --> E3[Jira Ticket Creation]
    E --> E4[GitHub Issue Creation]
    E --> E5[Semantic Search]
    E --> E6[Incident Investigator]

    C --> G[Service Layer]

    G --> G1[IncidentService]
    G --> G2[PostmortemService]
    G --> G3[RAGService]
    G --> G4[EmbeddingService]
    G --> G5[IncidentInvestigatorService]

    G --> H[Repository Layer]

    H --> H1[IncidentRepository]
    H --> H2[IncidentEventRepository]
    H --> H3[EmbeddingRepository]

    H --> I[(PostgreSQL + pgvector)]

    I --> I1[incidents]
    I --> I2[incident_events]
    I --> I3[incident_embeddings]

    G --> J[External Integrations]
    J --> J1[Jira Mock Adapter]
    J --> J2[GitHub Mock Adapter]

    E6 --> K[RAG Workflow]
    K --> K1[Query Embedding]
    K --> K2[Vector Similarity Search]
    K --> K3[Timeline Context]
    K --> K4[Pattern Extraction]
    K --> K5[Investigation Report]
```

## Current Runtime Flow

```text
User query
   ↓
MCP Tool
   ↓
Semantic Search
   ↓
PostgreSQL + pgvector
   ↓
Incident + Timeline Retrieval
   ↓
RAG Context Builder
   ↓
Pattern Extraction
   ↓
Incident Investigation Report
```
