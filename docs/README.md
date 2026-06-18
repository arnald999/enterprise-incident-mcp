# Enterprise Incident MCP

## Executive Summary

Enterprise Incident MCP is a production-oriented Model Context Protocol (MCP) server that enables AI agents to interact with enterprise incident management systems through a standardized interface.

The platform evolves from traditional CRUD operations to AI-native incident investigation through:

```text
CRUD
  ↓
Search
  ↓
Timeline Analysis
  ↓
Semantic Search
  ↓
RAG
  ↓
AI Investigation
  ↓
Multi-Agent Incident Response
```

The goal is to provide a reusable AI integration layer that can be consumed by:

* Claude Desktop
* Cursor
* OpenAI Agents
* Internal AI Assistants
* Future Agent Frameworks

---

# Business Problem

Traditional incident systems are optimized for human operators.

Humans typically know:

```text
Incident IDs
Team Names
Service Names
```

AI agents typically know:

```text
Symptoms
Observations
Logs
Operational Signals
```

Example:

```text
"checkout latency spike"
```

instead of:

```text
INC-123
```

The system therefore evolves toward symptom-driven retrieval and investigation.

---

# High-Level Architecture

```text
                    MCP Clients

     Claude     Cursor     ChatGPT     Agents

                        │
                        ▼

              Enterprise Incident MCP

                        │

        ┌───────────────┼────────────────┐
        │               │                │

        ▼               ▼                ▼

  Incident APIs    Investigation     Integrations
                     Services

        │               │                │

        └───────────────┼────────────────┘
                        │

                        ▼

                PostgreSQL + pgvector
```

---

# Architectural Principles

## Separation of Concerns

The system is intentionally divided into layers.

```text
MCP Layer
    ↓
Service Layer
    ↓
Repository Layer
    ↓
Database
```

Benefits:

* Maintainability
* Testability
* Scalability
* Reusability
* Clear ownership boundaries

---

# MCP Layer

Purpose:

Expose capabilities to AI agents.

Contains:

* Resources
* Tools
* Prompts

Responsibilities:

```text
Request Validation
Tool Registration
Schema Exposure
Protocol Handling
```

No business logic should exist here.

---

# Service Layer

Purpose:

Business logic orchestration.

Examples:

* Incident lifecycle management
* Timeline generation
* Investigation workflows
* RCA generation
* Integration coordination

Responsibilities:

```text
Validation
Orchestration
Business Rules
Workflow Management
```

---

# Repository Layer

Purpose:

Persistence abstraction.

Repositories own:

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

# incidents

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

# incident_events

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

# incident_embeddings

Stores semantic representations.

Example:

```text
incident_id
embedding
content
```

Used by:

* Semantic Search
* Similar Incident Discovery
* RAG
* AI Investigation

---

# Sprint 1 - Incident Timeline and Audit Trail

## Problem

The system initially stored only current state.

Example:

```text
INC-101

status=INVESTIGATING
```

This could not answer:

* When was the incident created?
* When was ownership changed?
* When was severity escalated?
* When did investigation begin?

---

## Solution

Introduce:

```text
incident_events
```

Architecture:

```text
create_incident()

        ↓

  +------------+
  |            |
  ▼            ▼

incidents   incident_events
```

---

## Automatic Event Generation

Incident creation:

```text
INCIDENT_CREATED
```

Assignment:

```text
INCIDENT_ASSIGNED
```

Updates:

```text
INCIDENT_UPDATED
```

---

## Timeline Retrieval

Tool:

```python
get_incident_timeline()
```

Purpose:

Retrieve complete incident history.

---

## Lessons Learned

### Transaction Boundaries Matter

Issue:

```python
session.flush()
```

without commit.

Result:

```text
Timeline events disappeared.
```

Resolution:

Explicit commits.

---

# Sprint 2 - Search

## Problem

CRUD requires IDs.

AI agents know symptoms.

Example:

```text
checkout latency
```

instead of:

```text
INC-123
```

---

## Solution

Add:

```python
search_incidents()
```

Current implementation:

```text
ILIKE
```

Fields:

* title
* description
* service

---

## Search Evolution Roadmap

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
AI Investigator
```

---

# Sprint 3 - Integrations

Integrations are isolated behind adapters.

Example:

```text
MCP Tool
    ↓
Jira Service
    ↓
Jira API
```

Benefits:

* Mock testing
* Easier replacements
* Better maintainability

Implemented:

* Jira Integration
* GitHub Integration
* Integration Event Service

---

# Sprint 4 - Postmortem Generation

Initial implementation:

Deterministic templates.

Reason:

Validate workflow before introducing AI.

Architecture:

```text
Retrieve Incident
       ↓
Retrieve Timeline
       ↓
Build Context
       ↓
Generate Report
```

Later:

```text
Generate Report
       ↓
LLM
```

without changing workflow orchestration.

---

# Sprint 5 - Semantic Search

## Why Keyword Search Is Not Enough

Keyword search:

```text
checkout latency
```

matches exact terms.

Semantic search:

```text
checkout slowdown
payment degradation
transaction delays
```

can still match.

---

## Embedding Model

Current model:

```text
all-MiniLM-L6-v2
```

Type:

```text
Embedding Model
```

Not an LLM.

Purpose:

```text
Text → Vector
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

Embedding Model:

```text
Text → Vector
```

Used for:

* Retrieval
* Similarity Search
* RAG

LLM:

```text
Context → Text
```

Used for:

* RCA
* Postmortems
* Summaries
* Reasoning

Both are required for production RAG systems.

---

# Sprint 6 - RAG and AI Investigation

Architecture:

```text
User Query
      ↓
Embedding Generation
      ↓
Vector Search
      ↓
Relevant Incidents
      ↓
Timeline Retrieval
      ↓
Context Builder
      ↓
Investigation Generator
```

---

# RAG Pipeline

## Retrieval

Retrieve relevant incidents.

## Augmentation

Build operational context.

Include:

* Incident Details
* Timeline Events
* Jira Events
* GitHub Events

## Generation

Produce:

* RCA
* Investigation Reports
* Recommendations

---

# Why pgvector?

Alternative:

* Pinecone
* Weaviate

Chosen:

```text
pgvector
```

Benefits:

* Simpler operations
* Existing PostgreSQL
* Lower infrastructure cost
* Easier local development

---

# Deployment Architecture

## Local Development

```text
Inspector
      ↓
STDIO MCP Server
      ↓
PostgreSQL + pgvector
```

Entry Point:

```text
server.py
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
PostgreSQL
```

Entry Point:

```text
web_server.py
```

---

# Render Deployment Challenge

Issue:

```text
Out of Memory
```

Cause:

```text
sentence-transformers
torch
model weights
```

loaded inside a 512 MB instance.

---

# Future OpenRouter Architecture

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
* Faster startup
* Lower memory
* Better cloud deployment

---

# OpenRouter Roadmap

Phase 1

```text
Local Embeddings
```

Phase 2

```text
OpenRouter Embeddings
```

Phase 3

```text
OpenRouter LLM Generation
```

Phase 4

```text
Fully AI-Native Incident Investigation Platform
```

---

# Key Learnings

1. MCP complements backend engineering rather than replacing it.

2. Current state and historical state are separate concerns.

3. Search is more valuable than CRUD for AI systems.

4. Transaction boundaries matter.

5. Business rules belong in services, not repositories.

6. External systems should be isolated behind adapters.

7. RAG is primarily a context-engineering problem.

8. Embeddings and LLMs solve different parts of the pipeline.

9. pgvector provides an effective first step into semantic search.

10. Stable interfaces allow implementations to evolve without breaking clients.

---

# Future Roadmap

Sprint 7

* OpenRouter Embedding Provider

Sprint 8

* OpenRouter LLM RCA Generation

Sprint 9

* Incident State Machine

Sprint 10

* Slack Integration

Sprint 11

* LangGraph Multi-Agent Investigation

Sprint 12

* Automated Incident Response Agents

Sprint 13

* Production Deployment on Kubernetes

```
```
