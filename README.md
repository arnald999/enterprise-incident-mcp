# Enterprise Incident MCP Server

Enterprise Incident MCP Server is a production-style Model Context Protocol server for AI-native incident management.

It exposes incident-management capabilities to AI agents through MCP resources, tools, and prompts. The project demonstrates backend engineering, enterprise integrations, semantic search, RAG workflows, Docker, and Kubernetes deployment patterns.

---

## Features

### MCP Resources

* `system://health`
* `system://database`

### MCP Tools

* `create_incident`
* `list_incidents`
* `get_incident`
* `search_incidents`
* `find_similar_incidents`
* `update_incident`
* `assign_incident`
* `get_incident_timeline`
* `generate_postmortem`
* `create_jira_ticket`
* `create_github_issue`
* `index_incident`
* `semantic_search`
* `build_incident_context`
* `generate_incident_rca`
* `investigate_incident`

---

## Architecture

```text
MCP Client
   ↓
Enterprise Incident MCP Server
   ↓
Service Layer
   ↓
Repository Layer
   ↓
PostgreSQL + pgvector
```

The system uses:

* MCP for AI-agent interaction
* PostgreSQL for persistent incident storage
* pgvector for semantic search
* SQLAlchemy Async for persistence
* Alembic for migrations
* Sentence Transformers for embeddings
* Docker and Kubernetes for deployment

See:

```text
docs/architecture.md
```

---

## Core Concepts

### Resources

Read-only capabilities.

Example:

```text
system://health
```

### Tools

Action-oriented capabilities.

Example:

```text
create_incident
```

### Prompts

Reusable AI workflows.

Planned examples:

```text
incident_triage
root_cause_analysis
postmortem
```

---

## RAG Workflow

The incident investigator follows a RAG-style pipeline:

```text
User Query
   ↓
Embedding Generation
   ↓
Vector Search using pgvector
   ↓
Retrieve Similar Incidents
   ↓
Retrieve Timeline Events
   ↓
Build Context
   ↓
Extract Patterns
   ↓
Generate Investigation Report
```

Example query:

```text
checkout slowdown
```

returns semantically related incidents such as:

```text
Checkout API latency spike
Payment timeout
Service degradation
```

---

## Local Setup

### 1. Create Environment

```powershell
uv venv --python 3.13
.venv\Scripts\activate
```

### 2. Install Dependencies

```powershell
uv sync
```

### 3. Start PostgreSQL

```powershell
docker compose up -d
```

### 4. Run Migrations

```powershell
$env:PYTHONPATH="src"
alembic upgrade head
```

### 5. Run MCP Server

```powershell
$env:PYTHONPATH="src"; python -m enterprise_incident_mcp.server
```

---

## MCP Inspector

Start Inspector:

```powershell
npx @modelcontextprotocol/inspector
```

Use:

```text
Command: python
Arguments: -m enterprise_incident_mcp.server
Environment: PYTHONPATH=src
```

---

## Docker

Build image:

```powershell
docker build -t enterprise-incident-mcp .
```

Run full stack:

```powershell
docker compose up -d
```

View logs:

```powershell
docker logs enterprise-incident-mcp
```

---

## Kubernetes

Apply manifests:

```powershell
kubectl apply -f k8s/
```

Check pods:

```powershell
kubectl get pods -n enterprise-incident
```

Delete:

```powershell
kubectl delete namespace enterprise-incident
```

---

## Release Milestones

```text
v0.1.0  MCP foundation
v0.2.0  Incident CRUD and timeline
v0.3.0  Search
v0.4.0  State machine
v0.5.0  Postmortem generation
v0.6.0  Jira integration foundation
v0.7.0  GitHub integration foundation
v0.8.0  RAG context and RCA
v0.9.0  Semantic search with pgvector
v1.0.0  AI incident investigator
```

---

## Portfolio Value

This project demonstrates:

* MCP server development
* AI-agent tool design
* Enterprise incident workflows
* PostgreSQL and pgvector
* Semantic search
* RAG architecture
* Domain-driven service layers
* Timeline/audit modeling
* External integration adapters
* Docker and Kubernetes deployment
