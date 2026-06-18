# Enterprise Incident MCP Server

Enterprise Incident MCP Server is a production-oriented Model Context Protocol (MCP) server that enables AI agents to interact with enterprise incident-management systems through a standardized interface.

The project demonstrates modern AI infrastructure patterns including:

* MCP Server Development
* Enterprise Incident Management
* PostgreSQL + pgvector
* Semantic Search
* Retrieval-Augmented Generation (RAG)
* AI Incident Investigation
* External Integrations
* Docker Deployment
* Kubernetes Deployment
* Public Cloud Deployment

---

# Live Deployment

### Health Endpoint

https://enterprise-incident-mcp.onrender.com/health

### Public MCP Endpoint

https://enterprise-incident-mcp.onrender.com/mcp

This endpoint can be consumed by:

* MCP Inspector
* Claude Desktop
* Cursor
* OpenAI Agents
* Future MCP-compatible clients

---

# Project Evolution

The system evolved through multiple architectural stages:

```text
Incident CRUD
      ↓
Timeline & Audit Trail
      ↓
Search
      ↓
External Integrations
      ↓
Semantic Search
      ↓
RAG
      ↓
AI Investigation
      ↓
Public MCP Deployment
```

This progression mirrors how enterprise operational systems gradually evolve into AI-native platforms.

---

# Features

## MCP Resources

```text
system://health
system://database
```

Read-only operational resources.

---

## MCP Tools

### Incident Management

```text
create_incident
list_incidents
get_incident
search_incidents
update_incident
assign_incident
get_incident_timeline
```

### Integrations

```text
create_jira_ticket
create_github_issue
```

### AI Investigation

```text
index_incident
semantic_search
find_similar_incidents
build_incident_context
generate_incident_rca
investigate_incident
generate_postmortem
```

---

# High-Level Architecture

```text
                MCP Clients

 Claude   Cursor   ChatGPT   OpenAI Agents

                       │
                       ▼

          Enterprise Incident MCP Server

                       │

     ┌─────────────────┼─────────────────┐
     │                 │                 │

     ▼                 ▼                 ▼

 Incident         Investigation     Integrations
 Services            Services

     │                 │                 │

     └─────────────────┼─────────────────┘
                       │

                       ▼

              PostgreSQL + pgvector
```

---

# Layered Architecture

```text
MCP Layer
    ↓
Service Layer
    ↓
Repository Layer
    ↓
Database Layer
```

---

## MCP Layer

Purpose:

Expose capabilities to AI agents.

Contains:

* Resources
* Tools
* Prompts

No business logic lives here.

---

## Service Layer

Purpose:

Business orchestration.

Examples:

* Incident lifecycle management
* Timeline generation
* RCA generation
* Investigation workflows
* Integration coordination

---

## Repository Layer

Purpose:

Persistence abstraction.

Responsible for:

* Queries
* Inserts
* Updates
* Deletes

Repositories understand:

```text
SQLAlchemy
PostgreSQL
pgvector
```

Services do not.

---

# Database Architecture

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

Answers:

```text
What is true right now?
```

---

## incident_events

Stores historical state.

Example:

```text
INCIDENT_CREATED
INCIDENT_ASSIGNED
INCIDENT_UPDATED
JIRA_TICKET_CREATED
GITHUB_ISSUE_CREATED
```

Answers:

```text
How did we get here?
```

---

## incident_embeddings

Stores vector representations.

Used for:

* Semantic Search
* Similar Incident Discovery
* RAG
* AI Investigation

---

# Timeline & Audit Trail

One of the first major architectural improvements was introducing a timeline system.

Before:

```text
create_incident()
      ↓
incidents
```

After:

```text
create_incident()

       ↓

 +-------------+
 |             |
 ▼             ▼

incidents   incident_events
```

Every significant operation automatically generates historical events.

Examples:

```text
INCIDENT_CREATED
INCIDENT_ASSIGNED
INCIDENT_UPDATED
JIRA_TICKET_CREATED
GITHUB_ISSUE_CREATED
```

This enables:

* Auditability
* RCA generation
* AI summarization
* Investigation workflows
* Postmortems

---

# Search Evolution

Initial implementation:

```text
ILIKE Search
```

Fields:

* title
* description
* service

Roadmap:

```text
ILIKE Search
      ↓
PostgreSQL Full Text Search
      ↓
pgvector
      ↓
Semantic Search
      ↓
RAG
      ↓
AI Investigation
```

Importantly:

The MCP interface remains stable while retrieval mechanisms evolve.

---

# Semantic Search

Traditional keyword search requires exact matches.

Example:

```text
checkout latency
```

Semantic search enables:

```text
checkout slowdown
payment degradation
transaction delays
```

to retrieve related incidents even when wording differs.

---

## Current Embedding Model

```text
all-MiniLM-L6-v2
```

Type:

```text
Embedding Model
```

Not:

```text
LLM
```

Purpose:

```text
Text
  ↓
Vector
```

Dimension:

```text
384
```

Stored in:

```text
pgvector
```

---

# Embedding Models vs LLMs

## Embedding Models

Purpose:

```text
Text → Vector
```

Used for:

* Semantic Search
* Similarity Matching
* Retrieval
* RAG

Examples:

```text
all-MiniLM-L6-v2
bge-small
text-embedding-3-small
```

---

## LLMs

Purpose:

```text
Context → Text
```

Used for:

* RCA Generation
* Postmortems
* Summaries
* Reasoning

Examples:

```text
GPT
Claude
Gemini
Mistral
Qwen
```

---

# RAG Workflow

The Incident Investigator follows a Retrieval-Augmented Generation workflow.

```text
User Query
      ↓
Embedding Generation
      ↓
pgvector Search
      ↓
Retrieve Similar Incidents
      ↓
Retrieve Timeline Events
      ↓
Build Incident Context
      ↓
Pattern Extraction
      ↓
Generate Investigation Report
```

Example:

```text
checkout slowdown
```

can retrieve:

```text
Checkout API latency spike
Payment timeout
Transaction degradation
```

even when exact words differ.

---

# AI Investigator

Current workflow:

```text
investigate_incident()

      ↓

Semantic Search

      ↓

Incident Retrieval

      ↓

Timeline Retrieval

      ↓

Context Builder

      ↓

Pattern Extraction

      ↓

Investigation Report
```

The investigator performs retrieval, enrichment, analysis, and report generation.

---

# External Integrations

Integrations are isolated behind service adapters.

Example:

```text
MCP Tool
     ↓
Jira Service
     ↓
Jira API
```

Benefits:

* Easier testing
* Mock implementations
* Vendor replacement
* Better separation of concerns

Current integrations:

* Jira
* GitHub

---

# Deployment Architecture

## Local Development

```text
MCP Inspector
       ↓
STDIO MCP Server
       ↓
PostgreSQL + pgvector
```

Entry point:

```text
enterprise_incident_mcp.server
```

---

## Public Deployment

```text
Internet
     ↓
FastAPI
     ↓
MCP HTTP Transport
     ↓
Enterprise Incident MCP
     ↓
Render PostgreSQL
```

Entry point:

```text
enterprise_incident_mcp.web_server
```

---

# MCP Inspector

Launch Inspector:

```powershell
npx @modelcontextprotocol/inspector
```

Use:

```text
Transport:
Streamable HTTP
```

URL:

```text
https://enterprise-incident-mcp.onrender.com/mcp
```

---

# Local Setup

## Create Environment

```powershell
uv venv --python 3.13
.venv\Scripts\activate
```

---

## Install Dependencies

```powershell
uv sync
```

---

## Start PostgreSQL

```powershell
docker compose up -d
```

---

## Run Migrations

```powershell
$env:PYTHONPATH="src"
alembic upgrade head
```

---

## Run MCP Server

```powershell
$env:PYTHONPATH="src"
python -m enterprise_incident_mcp.server
```

---

# Docker

Build:

```powershell
docker build -t enterprise-incident-mcp .
```

Run:

```powershell
docker compose up -d
```

---

# Kubernetes

Deploy:

```powershell
kubectl apply -f k8s/
```

Verify:

```powershell
kubectl get pods -n enterprise-incident
```

---

# Future Roadmap

## OpenRouter Embedding Provider

Current:

```text
Application
      ↓
Local Embedding Model
```

Future:

```text
Application
      ↓
OpenRouter Embeddings API
      ↓
Vector
```

Benefits:

* Smaller containers
* Lower memory usage
* Faster startup
* Better cloud deployment

---

## OpenRouter LLM-Powered RCA

Current:

```text
Deterministic Templates
```

Future:

```text
LLM-Generated RCA
```

Potential providers:

* GPT
* Claude
* Gemini
* Mistral
* Qwen

via OpenRouter.

---

## Incident State Machine

Current status changes are flexible.

Future:

```text
OPEN
   ↓
INVESTIGATING
   ↓
MITIGATED
   ↓
CLOSED
```

with transition validation.

---

## LangGraph Agent Workflow

Future architecture:

```text
Investigator Agent
        │
        ├── Search Agent
        │
        ├── Timeline Agent
        │
        ├── RCA Agent
        │
        └── Recommendation Agent
```

This enables autonomous incident investigations.

---

## Slack Integration

Planned capabilities:

```text
create_incident_channel()
send_incident_update()
notify_responders()
```

---

## Multi-Agent Incident Response

Future:

```text
Coordinator Agent
        │
        ├── Search Agent
        ├── Timeline Agent
        ├── RCA Agent
        ├── Jira Agent
        └── GitHub Agent
```

---

## Production Kubernetes Deployment

Future deployment target:

```text
Ingress
   ↓
FastAPI + MCP
   ↓
PostgreSQL
   ↓
OpenRouter
```

---

# Release Timeline

```text
v0.1.0  MCP Foundation
v0.2.0  Incident CRUD
v0.3.0  Timeline & Audit Trail
v0.4.0  Search
v0.5.0  Jira Integration
v0.6.0  GitHub Integration
v0.7.0  Postmortem Generation
v0.8.0  Semantic Search
v0.9.0  RAG
v1.0.0  AI Incident Investigator
v1.1.0  Public Deployment
```

---

# Portfolio Value

This project demonstrates:

* MCP Server Development
* AI-Agent Tool Design
* Enterprise Incident Workflows
* PostgreSQL + pgvector
* Semantic Search
* Retrieval-Augmented Generation
* AI Investigation Systems
* Domain-Driven Architecture
* Service/Repository Patterns
* External Integration Adapters
* Docker
* Kubernetes
* Cloud Deployment
* Production Debugging
* AI Infrastructure Engineering

The project intentionally mirrors architectural patterns used in modern AI platforms, incident-management products, internal developer platforms, and enterprise operational tooling.


# Quick Demo

The project is publicly deployed and can be tested immediately.

## Health Check

Verify service availability:

```text
https://enterprise-incident-mcp.onrender.com/health
```

Expected:

```json
{
  "status": "healthy",
  "service": "enterprise-incident-mcp"
}
```

---

## MCP Endpoint

Public MCP endpoint:

```text
https://enterprise-incident-mcp.onrender.com/mcp
```

This endpoint is intended for MCP-compatible clients and tools.

Examples:

* MCP Inspector
* Claude Desktop
* Cursor
* OpenAI Agents SDK
* Custom MCP Clients

---

## Test Using MCP Inspector

### Install / Launch Inspector

```bash
npx @modelcontextprotocol/inspector
```

Open the Inspector URL displayed in the terminal.

Example:

```text
http://localhost:6274
```

---

### Connect To Deployed MCP Server

Transport:

```text
Streamable HTTP
```

URL:

```text
https://enterprise-incident-mcp.onrender.com/mcp
```

Click:

```text
Connect
```

---

### Expected MCP Resources

```text
system://health
system://database
```

---

### Expected MCP Tools

```text
create_incident
list_incidents
get_incident
search_incidents
update_incident
assign_incident
get_incident_timeline

create_jira_ticket
create_github_issue

generate_postmortem

index_incident
semantic_search
find_similar_incidents

build_incident_context
generate_incident_rca
investigate_incident
```

---

## Example Demo Flow

### Create Incident

```json
{
  "title": "Checkout API latency spike",
  "description": "p95 latency exceeded 3 seconds",
  "severity": "P1"
}
```

---

### Assign Incident

```json
{
  "incident_id": "INC-XXXX",
  "owner": "Platform Team"
}
```

---

### Create Jira Ticket

```json
{
  "incident_id": "INC-XXXX",
  "project_key": "PLAT"
}
```

---

### Create GitHub Issue

```json
{
  "incident_id": "INC-XXXX",
  "repository": "incident-service"
}
```

---

### Retrieve Timeline

```json
{
  "incident_id": "INC-XXXX"
}
```

Expected events:

```text
INCIDENT_CREATED
INCIDENT_ASSIGNED
JIRA_TICKET_CREATED
GITHUB_ISSUE_CREATED
```

---

### AI Investigation

Example query:

```text
checkout slowdown
```

Tool:

```text
investigate_incident
```

Workflow:

```text
Query
   ↓
Semantic Search
   ↓
Retrieve Similar Incidents
   ↓
Retrieve Timeline Data
   ↓
Build Context
   ↓
Generate Investigation Report
```

This demonstrates the complete Retrieval-Augmented Generation (RAG) pipeline.
