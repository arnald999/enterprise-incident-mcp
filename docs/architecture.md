# Updated Architecture Addendum - RAG, Embeddings, and Deployment

## Current High-Level Architecture

```text
MCP Client
   ↓
Enterprise Incident MCP Server
   ↓
MCP Tools / Resources
   ↓
Service Layer
   ↓
Repository Layer
   ↓
PostgreSQL + pgvector
```

The system exposes incident-management workflows to AI agents through MCP.

---

## Runtime Modes

The project supports two runtime modes.

## Local Development Mode

Used for:

* MCP Inspector
* local debugging
* full semantic search
* local embeddings
* RAG testing
* AI investigator testing

Architecture:

```text
MCP Inspector
   ↓
STDIO MCP Server
   ↓
Incident Services
   ↓
PostgreSQL + pgvector
   ↓
Local Embedding Model
```

Entry point:

```text
enterprise_incident_mcp.server
```

Transport:

```text
STDIO
```

---

## Public Deployment Mode

Used for:

* Render
* Docker hosting
* HTTP-based MCP access
* public `/health`
* public `/mcp`

Architecture:

```text
Internet
   ↓
FastAPI Web Server
   ↓
Mounted MCP Streamable HTTP App
   ↓
Enterprise Incident MCP Server
   ↓
Render PostgreSQL
```

Entry point:

```text
enterprise_incident_mcp.web_server
```

Transport:

```text
Streamable HTTP
```

---

## Why Two Entrypoints?

STDIO is ideal for local clients.

Examples:

```text
MCP Inspector
Claude Desktop
Cursor
```

HTTP is required for public deployment.

Examples:

```text
Render
Railway
Cloud Run
ECS
Kubernetes Ingress
```

Therefore:

```text
server.py      -> local STDIO
web_server.py  -> deployed HTTP
```

The MCP tools, services, repositories, and domain logic remain the same.

Only the transport changes.

---

## RAG Architecture

The RAG workflow has three major stages.

```text
Retrieval
Augmentation
Generation
```

---

## 1. Retrieval

Purpose:

Find relevant incidents.

Current approaches:

```text
Keyword search
Semantic search
```

Keyword search:

```text
ILIKE title / description / service
```

Semantic search:

```text
embedding <=> query_embedding
```

using pgvector.

---

## 2. Augmentation

Purpose:

Build useful context for reasoning.

Retrieved incidents alone are not enough.

The system also loads:

* incident details
* timeline events
* Jira ticket events
* GitHub issue events
* ownership changes
* status changes
* severity changes

Then the context builder produces:

```text
Incident ID
Title
Description
Service
Severity
Status
Owner
Timeline
Integration Events
```

This becomes the input for RCA or investigation generation.

---

## 3. Generation

Purpose:

Produce useful operational output.

Current generation is deterministic.

Examples:

* postmortem draft
* RCA draft
* investigation report
* pattern extraction summary

Future generation can use an LLM.

Examples:

```text
OpenRouter Chat Model
OpenAI GPT
Anthropic Claude
Google Gemini
Mistral
Qwen
```

---

## AI Investigator Architecture

```text
investigate_incident(query)
   ↓
EmbeddingService
   ↓
EmbeddingRepository.semantic_search()
   ↓
IncidentRepository.get_by_id()
   ↓
IncidentEventRepository.get_timeline()
   ↓
RAGService.build_context()
   ↓
PatternService.extract_patterns()
   ↓
IncidentInvestigatorService.generate_report()
   ↓
MCP response
```

The investigator is not a single database query.

It is a multi-step workflow that retrieves, enriches, analyzes, and reports.

---

## Database Architecture

Current tables:

```text
incidents
incident_events
incident_embeddings
```

---

## incidents

Stores current state.

Example:

```text
INC-101
status=INVESTIGATING
severity=P1
owner=Platform Team
```

---

## incident_events

Stores historical timeline.

Example:

```text
INCIDENT_CREATED
INCIDENT_ASSIGNED
INCIDENT_UPDATED
JIRA_TICKET_CREATED
GITHUB_ISSUE_CREATED
```

---

## incident_embeddings

Stores vector representations.

Example:

```text
incident_id: INC-101
content: incident title + description + service
embedding: [0.01, -0.03, ...]
```

Used by:

```text
semantic_search
investigate_incident
generate_incident_rca
```

---

## Embedding Provider Architecture

Current:

```text
EmbeddingService
   ↓
SentenceTransformer
   ↓
all-MiniLM-L6-v2
```

Future:

```text
EmbeddingService
   ↓
EmbeddingProvider Interface
   ↓
+--------------------------+
| LocalEmbeddingProvider   |
| OpenRouterProvider       |
+--------------------------+
```

This allows environment-driven provider selection.

Example:

```env
EMBEDDING_PROVIDER=local
```

or:

```env
EMBEDDING_PROVIDER=openrouter
```

---

## Why OpenRouter Later?

Local embeddings are good for development.

But production deployment on small instances is memory constrained.

OpenRouter moves embedding generation out of the container.

Instead of loading:

```text
torch
transformers
sentence-transformers
model weights
```

the application sends text to an API and receives vectors.

This reduces:

* memory usage
* container size
* startup delay
* deployment failures

---

## Deployment Architecture

## Local

```text
Docker Compose
   ↓
MCP Server
   ↓
PostgreSQL + pgvector
```

## Render Free Tier

```text
Render Web Service
   ↓
FastAPI + MCP HTTP
   ↓
Render PostgreSQL
   ↓
Embeddings disabled
```

## Render Production Option

```text
Render Web Service
   ↓
FastAPI + MCP HTTP
   ↓
Render PostgreSQL + pgvector
   ↓
OpenRouter Embeddings API
   ↓
Semantic Search Enabled
```

---

## Production-Grade Future Architecture

```text
MCP Client
   ↓
Render / Cloud Web Service
   ↓
FastAPI HTTP Entrypoint
   ↓
FastMCP Tools
   ↓
Incident Services
   ↓
PostgreSQL + pgvector
   ↓
OpenRouter Embeddings
   ↓
OpenRouter LLM Generation
```

---

## Key Design Principle

The MCP interface should remain stable.

Whether retrieval is powered by:

```text
ILIKE
pgvector
OpenRouter embeddings
Pinecone
Weaviate
```

the user-facing MCP tool stays the same:

```python
investigate_incident(query: str)
```

This is what makes the architecture maintainable.

---

## Interview Summary

This project separates AI infrastructure into clean layers:

* MCP is the AI-facing interface.
* Services contain business logic.
* Repositories handle persistence.
* pgvector enables semantic retrieval.
* Embedding providers generate vectors.
* Context builders prepare RAG input.
* Generators produce RCA and investigation reports.

This separation makes it possible to evolve from local deterministic workflows to cloud-hosted LLM-powered incident investigation without rewriting the MCP interface.
